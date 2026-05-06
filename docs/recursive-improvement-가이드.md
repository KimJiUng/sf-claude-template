# 재귀 개선 가이드

## 목적

프로젝트를 사용할수록 반복되는 문제, 반복되는 사용자 요청, 반복되는 확인 질문을 문서 규칙으로 승격하여 다음 작업 품질을 높입니다.

재귀 개선은 코드를 자동으로 바꾸는 절차가 아니라, **반복 패턴을 발견하고 적절한 Markdown 문서에 반영하는 운영 루프**입니다.

## 기본 흐름

```text
발견 → 기록 → 승격 → 적용 → 검증
```

| 단계 | 설명 | 주요 산출물 |
|---|---|---|
| 발견 | 반복 문제, 반복 요청, 반복 확인 질문, 반복 게이트 위반을 감지 | 작업 보고, Review Gate 결과 |
| 기록 | 현재 작업 맥락과 원인을 짧게 남김 | `context/session_summary.md`, `context/open_tasks.md` |
| 승격 | 다음에도 적용할 가치가 있으면 운영 문서에 규칙으로 반영 | `AGENTS.md`, `CLAUDE.md`, `docs/**` |
| 적용 | 이후 작업 시작 시 문서 규칙을 읽고 반영 | 작업 사이클 시작 문서 읽기 |
| 검증 | Deploy Gate, Review Gate, 사용자 피드백으로 효과 확인 | 검증 결과, 후속 문서 수정 |

## 승격 대상

아래에 해당하면 문서 반영 후보로 봅니다.

1. 같은 유형의 실수나 실패가 반복됨
2. 사용자가 같은 요청이나 선호를 여러 번 말함
3. AI가 매번 같은 확인 질문을 해야 함
4. Deploy Gate 또는 Review Gate에서 같은 유형의 항목이 반복됨
5. 기술부채 후보가 특정 패턴으로 계속 쌓임
6. 작업 후 사람이 매번 같은 방식으로 수정 지시를 내림

## 문서 반영 위치

반복 패턴을 발견하면 먼저 기존 문서를 수정합니다. 기존 문서에 자연스럽게 들어갈 곳이 없을 때만 새 문서를 추가합니다.

| 상황 | 반영 위치 |
|---|---|
| AI 작업 방식, 금지/필수 행동 | `AGENTS.md`, `CLAUDE.md` |
| 사람 기준 사용법, 승인 흐름 | `README.md` |
| 템플릿 적용 절차 | `BOOTSTRAP.md` |
| 요구사항 → 설계 → 구현 → 배포 흐름 | `docs/orchestration-가이드.md` |
| 배포 전 검증/병합/승인 규칙 | `docs/deploy-gate-가이드.md` |
| Salesforce 설계/계층/품질 기준 | `docs/architecture.md` |
| Apex/LWC 코딩 패턴 | `docs/coding-standards.md` |
| 반복 실패와 재발 방지 | `context/failure_playbook.md` |
| 기술부채 후보와 처리 상태 | `docs/technical-debt/register.md` |
| 진행 중/대기 중 개선 작업 | `context/open_tasks.md` |
| 의미 있는 운영 결정 | `context/decisions.md` |

## 운영 규칙

- 반복 패턴은 긴 설명보다 짧고 실행 가능한 규칙으로 남깁니다.
- 한 번만 발생한 취향이나 예외는 바로 규칙화하지 않고 `context/session_summary.md`나 `context/open_tasks.md`에 남깁니다.
- 사용자 지시가 명확한 경우에는 관련 Markdown 문서를 바로 수정합니다.
- 정책, 배포, 데이터 삭제, 보안처럼 영향이 큰 규칙 변경은 작업 보고에 포함하여 사용자가 확인할 수 있게 합니다.
- 문서를 수정했으면 어떤 문서가 왜 바뀌었는지 최종 보고에 포함합니다.
- `backups/` 아래 파일은 재귀 개선 대상이 아닙니다. 백업은 참고만 하고 수정/삭제하지 않습니다.

## 예시

### 반복 요청

사용자가 여러 번 "배포 전에 생성/수정/삭제 파일을 먼저 보여줘"라고 요청했다면:

1. `AGENTS.md`, `CLAUDE.md`의 기본 실행/반영 원칙에 규칙 추가
2. `docs/orchestration-가이드.md`의 승인 단계 갱신
3. `README.md`의 사람 확인 항목 갱신

### 반복 실패

Org 충돌을 놓쳐 배포 중단이 반복된다면:

1. `context/failure_playbook.md`에 실패 패턴 추가
2. `docs/deploy-gate-가이드.md`의 검사 기준 보강
3. 필요하면 `scripts/deploy_org_check.py`에 검사 로직 추가

### 반복 기술부채 후보

하드코딩 ID 후보가 계속 발견된다면:

1. `docs/coding-standards.md`의 금지 예시 보강
2. `docs/technical-debt/register.md`에서 관련 항목을 `accepted`로 정리
3. 필요하면 Review Gate 감지 규칙 보강
