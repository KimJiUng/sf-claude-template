#!/usr/bin/env python3
"""
Org-aware 배포 전 검사

1. UTF-8 인코딩 검사
2. 한글 깨짐 검사
3. Org 현재본 retrieve → git base ref 3-way 비교
   - 로컬만 변경: 그대로 배포
   - Org만 변경: org 버전으로 로컬 갱신 (배포 시 덮어쓰기 방지)
   - 양쪽 변경: git merge-file 자동 병합 → 실패 시 배포 중단
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


RED = "\033[0;31m"
GREEN = "\033[0;32m"
CYAN = "\033[0;36m"
YELLOW = "\033[1;33m"
NC = "\033[0m"

TEXT_EXTENSIONS = {
    ".cls", ".trigger", ".page", ".component",
    ".xml", ".html", ".js", ".css",
}

METADATA_TYPE_MAP = {
    "classes": "ApexClass",
    "triggers": "ApexTrigger",
    "lwc": "LightningComponentBundle",
    "aura": "AuraDefinitionBundle",
    "pages": "ApexPage",
    "components": "ApexComponent",
    "objects": "CustomObject",
    "layouts": "Layout",
    "permissionsets": "PermissionSet",
    "permissionsetGroups": "PermissionSetGroup",
    "flows": "Flow",
    "flexipages": "FlexiPage",
    "staticresources": "StaticResource",
    "customMetadata": "CustomMetadata",
    "labels": "CustomLabels",
    "tabs": "CustomTab",
}

BUNDLE_TYPES = {"lwc", "aura"}


# ──────────────────────────────────────────────
# Git helpers
# ──────────────────────────────────────────────

def get_base_ref(root: Path) -> str | None:
    for ref in ["origin/HEAD", "origin/master", "origin/main"]:
        r = subprocess.run(
            ["git", "rev-parse", "--verify", ref],
            capture_output=True, text=True, cwd=root,
        )
        if r.returncode == 0:
            return ref
    r = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD~1"],
        capture_output=True, text=True, cwd=root,
    )
    return "HEAD~1" if r.returncode == 0 else None


def get_changed_files(base_ref: str, root: Path) -> list[str]:
    r = subprocess.run(
        ["git", "diff", "--name-only", base_ref, "--", "force-app/"],
        capture_output=True, text=True, cwd=root,
    )
    if r.returncode != 0:
        return []
    return [f for f in r.stdout.strip().split("\n") if f]


def git_show(root: Path, ref: str, rel_path: str) -> str | None:
    r = subprocess.run(
        ["git", "show", f"{ref}:{rel_path}"],
        capture_output=True, text=True, cwd=root,
    )
    return r.stdout if r.returncode == 0 else None


# ──────────────────────────────────────────────
# Metadata helpers
# ──────────────────────────────────────────────

def file_to_metadata(rel_path: str) -> str | None:
    """force-app 경로 → Metadata API type:name"""
    parts = Path(rel_path).parts
    if len(parts) < 5 or parts[0] != "force-app":
        return None
    type_dir = parts[3]
    meta_type = METADATA_TYPE_MAP.get(type_dir)
    if not meta_type:
        return None
    if type_dir in BUNDLE_TYPES:
        return f"{meta_type}:{parts[4]}"
    name = Path(parts[4]).stem
    if name.endswith("-meta"):
        name = name[:-5]
    return f"{meta_type}:{name}"


def get_api_version(root: Path) -> str:
    cfg = root / "sfdx-project.json"
    if cfg.exists():
        with open(cfg, encoding="utf-8") as f:
            return json.load(f).get("sourceApiVersion", "65.0")
    return "65.0"


# ──────────────────────────────────────────────
# Encoding checks (기존)
# ──────────────────────────────────────────────

def check_utf8_encoding(root: Path, files: list[str]) -> list[str]:
    violations = []
    for rel in files:
        fp = root / rel
        if not fp.exists() or fp.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            fp.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            violations.append(f"  - {rel}: Not valid UTF-8 encoding")
    return violations


def check_korean_corruption(root: Path, files: list[str]) -> list[str]:
    violations = []
    for rel in files:
        fp = root / rel
        if not fp.exists() or fp.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            content = fp.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "\ufffd" in content:
            violations.append(
                f"  - {rel}: Contains replacement character (possible Korean corruption)"
            )
    return violations


# ──────────────────────────────────────────────
# Org retrieve
# ──────────────────────────────────────────────

def retrieve_from_org(
    root: Path, target_org: str, metadata_items: set[str],
) -> tuple[Path | None, bool]:
    """Org에서 메타데이터를 임시 프로젝트로 retrieve. (temp_dir, success)"""
    temp_dir = Path(tempfile.mkdtemp(prefix="org-retrieve-"))
    try:
        (temp_dir / "force-app" / "main" / "default").mkdir(parents=True)
        sfdx_cfg = {
            "packageDirectories": [{"path": "force-app", "default": True}],
            "sourceApiVersion": get_api_version(root),
        }
        with open(temp_dir / "sfdx-project.json", "w", encoding="utf-8") as f:
            json.dump(sfdx_cfg, f)

        cmd = ["sf", "project", "retrieve", "start", "--target-org", target_org]
        for m in sorted(metadata_items):
            cmd.extend(["--metadata", m])

        r = subprocess.run(cmd, capture_output=True, text=True, cwd=temp_dir)
        if r.returncode != 0:
            print(f"{YELLOW}  Org retrieve warning: {r.stderr.strip()}{NC}")
            return temp_dir, False
        return temp_dir, True
    except FileNotFoundError:
        print(f"{YELLOW}  sf CLI not found. Skipping org comparison.{NC}")
        return temp_dir, False


# ──────────────────────────────────────────────
# 3-way merge
# ──────────────────────────────────────────────

def try_merge(
    root: Path, base: str, local: str, org: str,
) -> dict:
    """git merge-file -p 로 3-way 병합 시도."""
    tmp = Path(tempfile.mkdtemp(prefix="merge-"))
    try:
        (tmp / "base").write_text(base, encoding="utf-8")
        (tmp / "local").write_text(local, encoding="utf-8")
        (tmp / "org").write_text(org, encoding="utf-8")

        r = subprocess.run(
            ["git", "merge-file", "-p",
             str(tmp / "local"), str(tmp / "base"), str(tmp / "org")],
            capture_output=True, text=True, cwd=root,
        )
        return {
            "success": r.returncode == 0,
            "content": r.stdout,
            "conflicts": max(0, r.returncode),
        }
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ──────────────────────────────────────────────
# 3-way comparison (핵심)
# ──────────────────────────────────────────────

def do_three_way_check(
    root: Path, target_org: str, changed_files: list[str], base_ref: str,
) -> tuple[list[str], list[str]]:
    """
    Returns (violations, summaries).
    violations → 비어 있지 않으면 배포 중단.
    summaries  → 사용자 안내 메시지.
    """
    metadata_items: set[str] = set()
    for f in changed_files:
        m = file_to_metadata(f)
        if m:
            metadata_items.add(m)

    if not metadata_items:
        return [], []

    print(f"{CYAN}Retrieving {len(metadata_items)} metadata item(s) from org [{target_org}]...{NC}")
    temp_dir, ok = retrieve_from_org(root, target_org, metadata_items)
    if not ok:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
        return [], [f"{YELLOW}  Org retrieve 실패 — 3-way 비교를 건너뜁니다.{NC}"]

    violations: list[str] = []
    summaries: list[str] = []
    org_only_files: list[str] = []
    merged_files: list[str] = []

    try:
        for f in changed_files:
            local_path = root / f
            if not local_path.exists():
                continue
            if local_path.suffix.lower() not in TEXT_EXTENSIONS:
                continue

            try:
                local_content = local_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            base_content = git_show(root, base_ref, f)
            org_path = temp_dir / f
            if not org_path.exists():
                continue
            try:
                org_content = org_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            if base_content is None:
                continue

            local_changed = base_content != local_content
            org_changed = base_content != org_content

            if not org_changed:
                continue

            if not local_changed:
                local_path.write_text(org_content, encoding="utf-8")
                org_only_files.append(f)
                continue

            merge = try_merge(root, base_content, local_content, org_content)
            if merge["success"]:
                local_path.write_text(merge["content"], encoding="utf-8")
                merged_files.append(f)
            else:
                violations.append(
                    f"  - {f}: 로컬과 Org 양쪽에서 같은 영역 수정 — "
                    f"충돌 {merge['conflicts']}건"
                )

        if org_only_files:
            summaries.append(
                f"{CYAN}  [org-only] {len(org_only_files)}개 파일: "
                f"Org 버전으로 갱신 (로컬 미변경){NC}"
            )
            for f in org_only_files:
                summaries.append(f"    → {f}")

        if merged_files:
            summaries.append(
                f"{GREEN}  [auto-merge] {len(merged_files)}개 파일: "
                f"로컬+Org 변경사항 자동 병합 완료{NC}"
            )
            for f in merged_files:
                summaries.append(f"    → {f}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return violations, summaries


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print(f"{RED}Usage: {sys.argv[0]} <ROOT_PATH> <TARGET_ORG> [deploy args...]{NC}")
        sys.exit(2)

    root = Path(sys.argv[1]).resolve()
    target_org = sys.argv[2]

    base_ref = get_base_ref(root)
    if not base_ref:
        print(f"{YELLOW}Git base ref를 결정할 수 없습니다. Org-aware 검사를 건너뜁니다.{NC}")
        sys.exit(0)

    print(f"{CYAN}Using git base ref: {base_ref}{NC}")

    changed_files = get_changed_files(base_ref, root)
    if not changed_files:
        print(f"{GREEN}No force-app changes detected. Skipping org-aware check.{NC}")
        sys.exit(0)

    print(f"{CYAN}Checking {len(changed_files)} changed file(s)...{NC}")

    all_violations: list[str] = []

    # ── 1. UTF-8 인코딩 검사 ──
    utf8 = check_utf8_encoding(root, changed_files)
    if utf8:
        all_violations.append(f"{YELLOW}[Rule] encoding-check{NC}")
        all_violations.extend(utf8)

    # ── 2. 한글 깨짐 검사 ──
    korean = check_korean_corruption(root, changed_files)
    if korean:
        all_violations.append(f"{YELLOW}[Rule] korean-corruption{NC}")
        all_violations.extend(korean)

    # ── 3. 3-way 비교 (Org retrieve → compare → merge) ──
    three_way_violations, three_way_summaries = do_three_way_check(
        root, target_org, changed_files, base_ref,
    )
    if three_way_violations:
        all_violations.append(f"{YELLOW}[Rule] org-conflict{NC}")
        all_violations.extend(three_way_violations)

    for s in three_way_summaries:
        print(s)

    # ── 결과 ──
    if all_violations:
        print()
        print(f"{RED}Org-aware pre-deploy check failed: deployment will be stopped.{NC}")
        print()
        for line in all_violations:
            print(line)
        sys.exit(2)

    print(f"{GREEN}Org-aware pre-deploy check passed.{NC}")
    sys.exit(0)


if __name__ == "__main__":
    main()
