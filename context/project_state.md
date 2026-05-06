# 프로젝트 상태

최종 업데이트: 2026-05-06

## 현재 목표

오픈소스 배포 가능한 Salesforce + AI Agent 프로젝트 템플릿 완성

## 구현 상태

- 프로젝트 템플릿 골격 완료 (디렉토리 구조, 설정 파일, 운영 문서)
- Claude/Codex 동시 사용을 위한 에이전트 규칙 진입점 구성 완료
- 저장소 이력 전제 제거 및 작업 snapshot 기반 변경 추적 흐름 반영
- Org snapshot 기반 3-way 비교/자동 병합 흐름 반영
- 기술부채 Review Gate 자동 누적 흐름 반영
- 반복 문제/반복 요청을 문서 규칙으로 승격하는 재귀 개선 루프 반영
- OpenAI GPT-5.5 prompt guidance 기준으로 에이전트 규칙을 결과 중심, 좁은 질문, 명시적 중단 조건 중심으로 정리
- `AGENTS.md`와 `CLAUDE.md`의 운영 지침 차이를 에이전트명 차이만 남도록 재정렬
- 문서/설정 작업에는 Org snapshot을 요구하지 않고, Salesforce 소스/Org 영향 작업에만 snapshot을 적용하도록 정리
- 전역 설치/패키지 설치/시스템 설정 변경은 사용자 명시 동의 후에만 실행하도록 BOOTSTRAP 안전 규칙 보강
- 주석 템플릿의 미완료 표시 기본 문구 제거로 Review Gate 거짓 양성 가능성 축소
- Deploy Gate required files에 README, BOOTSTRAP, `context/**`, 기술부채 등록부를 포함해 핵심 운영 문서 누락을 감지하도록 보강
- Apex/LWC 코딩 표준에서 `with sharing`, FLS/CRUD, `@track` 규칙을 최신 Salesforce 사용 기준에 맞게 완화/명확화
- 오픈소스 배포 준비 완료 (회사 참조 제거, 플레이스홀더 적용, LICENSE/README/BOOTSTRAP 추가)
- Deploy Gate 정적 검사 통과 확인됨

## 변경 파일

- `AGENTS.md` — Codex용 작업 규칙 진입점
- `CLAUDE.md` — Claude용 작업 규칙 진입점
- `BOOTSTRAP.md` — AI 에이전트용 프로젝트 적용 지침서
- `README.md` — 사람용 소개 및 사용법
- `LICENSE` — MIT License (신규)
- `sfdx-project.json`, `package.json`, `config/project-scratch-def.json` — `{{PROJECT_NAME}}` 플레이스홀더 적용
- `scripts/run_deploy_gate.js` — OS 공통 Deploy Gate 실행 래퍼
- `scripts/work_snapshot.py` — Salesforce 소스/Org 영향 작업 전 로컬 백업 및 Org snapshot 생성
- `scripts/deploy_org_check.py` — Org snapshot 기반 3-way 비교/자동 병합
- `scripts/debt_scan.py` — 기술부채 후보 자동 수집
- `docs/technical-debt/register.md` — `review-needed` 중심 등록부로 개편
- `docs/recursive-improvement-가이드.md` — 재귀 개선 루프 운영 기준
- `context/README.md` — 작업 유형별 필수/추가 컨텍스트 읽기 기준 정리
- `docs/orchestration-가이드.md`, `docs/deploy-gate-가이드.md`, `docs/architecture.md` — snapshot 적용 범위 명확화
- `docs/coding-standards.md` — 주석 템플릿의 미완료 표시 기본 문구 제거
- `config/deploy-gate-rules.json` — 필수 운영 문서 검사 범위 보강
- `scripts/work_snapshot.py` — 스크립트 설명을 Salesforce/Org 영향 작업 기준으로 정리
- `README.md` — 템플릿 적용 예시 URL을 현재 저장소명으로 갱신

## 테스트

- Deploy Gate 정적 검사: 통과
- Deploy Gate 정적 검사: 통과 (2026-05-06 재확인)
- 스크립트 단위 테스트: 통과 (2026-05-06 재확인)
- Review Gate: 작업 snapshot 파일 없음으로 스킵
- 스크립트 단위 테스트: 통과
- 회사 참조(KOLON) 잔존 검사: 0건

## 남은 작업

- 팀원 대상 사용 테스트 (Claude/Codex에게 URL 주고 적용 확인)
- 실제 Salesforce org 대상 snapshot/배포 리허설

## 리스크

- `CLAUDE.md`와 `AGENTS.md` 규칙이 장기적으로 어긋나지 않도록 변경 시 함께 갱신 필요
- 자동 병합은 텍스트 범위 기준이므로 의도 충돌 의심 시 사용자 확인 필요
