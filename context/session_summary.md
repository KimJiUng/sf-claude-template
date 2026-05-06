# 세션 요약

최종 업데이트: 2026-05-06

## 최근 세션

### 2026-05-06 — GPT-5.5 프롬프트 가이드 반영

1. `AGENTS.md`, `CLAUDE.md`를 결과/성공 기준/제약/출력/중단 조건 중심으로 정리
2. 질문 기준을 "누락 정보가 결과나 리스크를 실질적으로 바꾸는 경우"로 좁히고, 저위험 작업은 명시적 가정 후 진행하도록 보강
3. 공통 컨텍스트 읽기와 작업 유형별 추가 문서 읽기 기준을 `context/README.md`와 에이전트 규칙에 동기화
4. Salesforce 소스/Org 영향 작업에만 snapshot을 요구하도록 `README.md`, `docs/orchestration-가이드.md`, `docs/deploy-gate-가이드.md`, `docs/architecture.md`를 정리
5. `BOOTSTRAP.md`에 전역 설치/패키지 설치/시스템 설정 변경은 사용자 명시 동의 후 실행한다는 규칙 추가
6. `docs/coding-standards.md` 주석 템플릿의 미완료 표시 기본 문구 제거
7. 추가 점검으로 `AGENTS.md`/`CLAUDE.md` 지침 차이, snapshot 문구 잔여, 코딩 표준 예외/최신성, Deploy Gate 필수 파일 범위를 정리
8. `README.md`의 템플릿 적용 예시 URL을 현재 저장소명(`sf-ai-agent-template`)에 맞게 갱신

### 2026-04-24 — 승인 기반 배포/기술부채 Review Gate 개편

1. 작업 전 `backups/`에 로컬 백업과 Org 시작 snapshot을 생성하는 `scripts/work_snapshot.py` 추가
2. `scripts/deploy_org_check.py`를 저장소 이력 기준 비교에서 Org snapshot 기반 3-way 비교로 변경
3. 서로 다른 영역 변경은 자동 병합하고, 같은 영역/삭제/의도 불명 변경은 배포 중단하도록 정리
4. `scripts/debt_scan.py` 추가 — 수정 영향 파일의 기술부채 후보를 `review-needed`로 자동 누적
5. 문서 전반을 사용자 승인 전 Org 배포 금지, 변경 목록/기술부채 보고 후 승인 배포 흐름으로 갱신
6. `README.md`에 사람 기준 사용 흐름, 승인 방식, snapshot/Review Gate 설명 추가
7. 반복 문제/반복 요청을 Markdown 규칙으로 승격하는 재귀 개선 루프 문서화

### 2026-04-24 — Codex 호환성 확장

1. `AGENTS.md` 추가 — Codex가 자동으로 읽을 작업 규칙 진입점 구성
2. `README.md`, `BOOTSTRAP.md`를 Claude/Codex 공용 템플릿 설명으로 갱신
3. Deploy Gate 필수 파일/텍스트 계약에 `AGENTS.md`와 OS 공통 실행 래퍼 추가
4. `scripts/run_deploy_gate.js` 추가 — npm 명령이 PowerShell 전용에 묶이지 않도록 개선
5. 기존 Claude 흐름은 `CLAUDE.md`로 유지하고, 변경 시 두 규칙 파일을 함께 갱신하도록 명시

### 2026-04-06 — 오픈소스 배포 준비

1. 프로젝트 구조 점검 및 누락 폴더/스크립트 보완
2. 오픈소스 배포를 위한 회사 참조 제거 → `{{PROJECT_NAME}}` 플레이스홀더 적용
3. `BOOTSTRAP.md` 작성 — Claude가 읽고 프로젝트에 적용하는 지침서
4. `README.md` 작성 — 사람용 소개 문서
5. MIT `LICENSE` 파일 추가
6. Deploy Gate 검증 통과 확인
