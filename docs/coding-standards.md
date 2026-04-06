# Salesforce 개발 표준 — 코딩 컨벤션 및 주석 규칙

## 프로젝트 개요

Salesforce DX(SFDX) 기반 프로젝트입니다.

## 기술 스택

- **플랫폼**: Salesforce (API v65.0)
- **개발 도구**: Salesforce CLI (`sf`)
- **메타데이터 형식**: Source format
- **소스 경로**: `force-app/main/default/`

## Salesforce 개발 컨벤션

### Apex 네이밍

- 클래스명: PascalCase (예: `AccountService`, `OpportunityTriggerHandler`)
- 테스트 클래스: `{클래스명}Test` (예: `AccountServiceTest`)
- 트리거: `{오브젝트명}Trigger` (예: `AccountTrigger`)
- 트리거 핸들러: `{오브젝트명}TriggerHandler` (예: `AccountTriggerHandler`)
- 테스트 커버리지: 최소 75% (배포 요건)

### 주석 규칙 (필수)

코드 생성 시 반드시 아래 주석 형식을 따릅니다.

#### Apex 클래스 상단 주석

```apex
/****************************************************************************************
* File Name : AccountService.cls
* Description : 고객 관련 비즈니스 로직 처리 Service
* Author: {{AUTHOR_NAME}}
* Last Modified By : {{AUTHOR_EMAIL}}
* Created date : DD/MM/YYYY
* Modification Log
* ===========================================================================
* Ver  Date           Author        Modification        Description
* ===========================================================================
* 1.0  DD/MM/YYYY   {{AUTHOR_NAME}}         Create
****************************************************************************************
* //TO-DO
****************************************************************************************/
public with sharing class AccountService {
    // ...
}
```

#### 테스트 클래스 상단 주석

```apex
/****************************************************************************************
* File Name : AccountServiceTest.cls
* Description : AccountService 테스트 클래스
* Target: AccountService.cls
* Author: {{AUTHOR_NAME}}
* Modification Log
* ===========================================================================
* Ver  Date           Author        Modification        Description
* ===========================================================================
* 1.0  DD/MM/YYYY   {{AUTHOR_NAME}}         Create
****************************************************************************************/
@isTest
public class AccountServiceTest {
    // ...
}
```

#### 메서드 주석

```apex
/**
* @author {{AUTHOR_NAME}} | DD/MM/YYYY
* @param accountId 고객 레코드 ID
* @description : 고객 정보를 조회하여 반환
* @return Account 고객 레코드
**/
public Account getAccountById(Id accountId) {
    // ...
}
```

#### 범용 주석 (짧은 설명)

```apex
/**
* @description : 입력값 유효성 검증
* @author {{AUTHOR_NAME}} | DD/MM/YYYY
**/
private void validateInput(String input) {
    // ...
}
```

#### LWC/Aura HTML 주석

```html
<!--
* ===========================================================================
* File Name     : customerList.html
* Description   : 고객 목록 화면 컴포넌트
* Author        : {{AUTHOR_NAME}}
* Last Modified By : {{AUTHOR_EMAIL}}
* Created date  : DD/MM/YYYY
* Modification Log
* ===========================================================================
* Ver  Date           Author        Modification        Description
* ===========================================================================
* 1.0  DD/MM/YYYY     {{AUTHOR_NAME}}         Create
****************************************************************************************
* //TO-DO
****************************************************************************************/
-->
<template>
    <!-- ... -->
</template>
```

#### LWC JavaScript 주석

```javascript
/****************************************************************************************
* File Name : customerList.js
* Description : 고객 목록 화면 컴포넌트 컨트롤러
* Author: {{AUTHOR_NAME}}
* Last Modified By : {{AUTHOR_EMAIL}}
* Created date : DD/MM/YYYY
* Modification Log
* ===========================================================================
* Ver  Date           Author        Modification        Description
* ===========================================================================
* 1.0  DD/MM/YYYY   {{AUTHOR_NAME}}         Create
****************************************************************************************/
import { LightningElement } from 'lwc';

export default class CustomerList extends LightningElement {
    // ...
}
```

### LWC (Lightning Web Components)

- 컴포넌트명: camelCase (예: `accountList`, `opportunityCard`)
- 디렉토리: `force-app/main/default/lwc/{컴포넌트명}/`
- 필수 파일: `.js`, `.html`, `.js-meta.xml`

### 디렉토리 구조

```
force-app/main/default/
├── classes/          # Apex 클래스
├── triggers/         # Apex 트리거
├── lwc/              # Lightning Web Components
├── aura/             # Aura Components
├── objects/          # Custom Objects & Fields
├── permissionsets/   # Permission Sets
├── layouts/          # Page Layouts
├── flexipages/       # Lightning Pages
└── staticresources/  # Static Resources
```

## 자주 쓰는 SF CLI 명령

```bash
sf org login web                          # Org 로그인
sf org create scratch -f config/project-scratch-def.json -a my-scratch
sf project deploy start                   # 소스 배포
sf project retrieve start                 # 소스 가져오기
sf apex run test --code-coverage          # 테스트 실행
sf org open                               # Org 열기
```

---

## Apex 개발 표준

### 필수 규칙

1. **with sharing 기본**: 모든 Apex 클래스는 `with sharing` 사용
2. **FLS/CRUD 체크 필수**: `Security.stripInaccessible()` 또는 `WITH SECURITY_ENFORCED`
3. **Loop 내 DML/SOQL 금지**: Bulkify 필수
4. **Trigger.new/old 직접 접근 금지**: Map으로 변환하여 사용
5. **상수 사용 필수**: ID나 조건값(Magic Number/String) 하드코딩을 금지하며, 클래스 상단에 상수(`private static final`)로 선언하거나 Custom Label/Metadata를 사용
6. **안전한 에러 핸들링**: DML 작업 시 `try-catch` 블록을 필수로 사용하고, LWC와 통신하는 메서드는 예외 발생 시 `AuraHandledException`를 던져 사용자에게 명확한 에러를 전달
7. **비동기 재귀 호출 방지**: `@future`나 `Queueable` 등 비동기 처리 시 무한 루프 방지 로직(static boolean 플래그 등) 필수 적용
8. **ID 하드코딩 금지**: Custom Metadata 또는 Custom Setting 사용

### 개발 패턴

- **Trigger**: 오브젝트당 1개 트리거, TriggerHandler 패턴 필수
- **Selector**: SOQL은 Selector 클래스로 분리 (예: `AccountSelector`)
- **Service**: 비즈니스 로직은 Service 클래스로 분리 (예: `AccountService`)
- **Test**: 모든 Apex 클래스에 테스트 클래스 필수 (75%+ 커버리지)

### Trigger Handler 패턴

```apex
// AccountTrigger.trigger
trigger AccountTrigger on Account (before insert, before update, after insert, after update) {
    AccountTriggerHandler handler = new AccountTriggerHandler();
    handler.run();
}

// AccountTriggerHandler.cls
public with sharing class AccountTriggerHandler {
    public void run() {
        if (Trigger.isBefore && Trigger.isInsert) {
            beforeInsert(Trigger.new);
        }
        // ...
    }
    
    private void beforeInsert(List<Account> newRecords) {
        // 비즈니스 로직
    }
}
```

### Selector 패턴

```apex
public with sharing class AccountSelector {
    public List<Account> findByIds(Set<Id> ids) {
        return [
            SELECT Id, Name, Phone
            FROM Account
            WHERE Id IN :ids
            WITH SECURITY_ENFORCED
        ];
    }
}
```

### Service 패턴

```apex
public with sharing class AccountService {
    private AccountSelector selector = new AccountSelector();
    
    public void processAccounts(List<Account> accounts) {
        // 비즈니스 로직
    }
}
```

---

## LWC 개발 규칙

### 필수 규칙

1. **@api**: 외부 공개 속성
2. **@track**: 상태 관리 (반응형)
3. **@wire**: Salesforce 데이터 조회
4. **UI 안정성 (Spinner)**: 서버(Apex) 호출 등 대기 시간이 발생하는 작업 시 반드시 Loading Spinner를 노출하여 중복 클릭 방지
5. **명시적 에러 피드백**: Imperative Apex 호출 시 `catch` 블록에서 Toast 이벤트를 발생시켜 사용자에게 에러 상황을 명시적으로 알림

### Custom Label 사용 (선택)

> **참고**: 다국어 지원이 필요한 경우에만 사용합니다.
> 국내 단일 언어 프로젝트에서는 직접 문자열 사용이 유지보수에 유리할 수 있습니다.

**사용 권장 케이스:**
- 다국어 지원 필요 시
- 여러 법인/권역에서 사용하는 경우
- 텍스트 변경이 빈번한 경우 (배포 없이 수정 가능)

**직접 문자열 사용 가능 케이스:**
- 국내 단일 언어 프로젝트
- 텍스트 변경이 거의 없는 경우
- 빠른 개발이 필요한 경우

```javascript
// Custom Label 사용 시
import TITLE from '@salesforce/label/c.CustomerMgmt_List_Title';
import SEARCH from '@salesforce/label/c.Common_Button_Search';

export default class CustomerList extends LightningElement {
    labels = { TITLE, SEARCH };
}

// 직접 문자열 사용 시 (국내 단일 언어)
export default class CustomerList extends LightningElement {
    title = '고객 목록';
    searchLabel = '검색';
}
```

### Custom Label 명명 규칙 (사용 시)

```
{기능영역}_{화면}_{용도}

예시:
- CustomerMgmt_List_Title
- CustomerMgmt_Registration_SaveButton
- Common_Button_Save
- Common_Message_Required
```

---

## Custom Metadata Type 활용

환경별/권역별로 달라지는 설정값은 반드시 Custom Metadata Type을 사용합니다.

| 용도 | Custom Metadata 예시 |
|------|---------------------|
| 권역별 세율 | `RegionTaxRate__mdt` |
| 권역별 비즈니스 규칙 | `RegionConfig__mdt` |
| 외부 시스템 엔드포인트 | `IntegrationEndpoint__mdt` |
| 공통 설정값 | `AppConfig__mdt` |

---

## 데이터 모델 분석 순서

공통 오브젝트/필드 식별 시 순서:

1. **Standard Object 우선 확인**: Account, Contact, Opportunity, Case 등
2. **Standard Object + Custom Field**: Standard에 Custom Field 추가로 해결 가능한지
3. **Custom Object 생성**: Standard로 커버 불가능한 경우에만 (사유 명시)

---

## 보안 규칙

- ApexSharingViolation 방지
- SOQL Injection 방지 (Dynamic SOQL 시 escape 처리)
- XSS 방지
- HTTPS Endpoint만 허용
- Debug 로그에 개인정보 출력 금지
- Named Credential 사용 (Credential 하드코딩 금지)

---

## 테스트 규칙

- `@isTest(seeAllData=false)` 필수
- Assert 없는 테스트 금지
- TestDataFactory 패턴 사용
- Batch/Future/Queueable 테스트는 `Test.startTest()` / `Test.stopTest()` 사용

---

## 디자인 명세 연동 (LWC 개발)

### 입력 기준

LWC 구현은 외부 디자인 링크가 아니라 저장소 내 디자인 명세를 기준으로 진행합니다.

- 기본 경로: `docs/design/specs/{업무영역}/디자인명세-{기능명}.md`
- 인덱스: `docs/design/design-artifacts.md`

### 디자인-LWC 매핑

| 디자인 명세 항목 | LWC/SLDS 반영 |
|------------------|--------------|
| 레이아웃 | `slds-grid`, `lightning-layout`, `div/section` |
| 컴포넌트 규격 | LWC 컴포넌트 경계(`c-*`) |
| 상태(기본/로딩/오류) | 조건부 렌더링, skeleton, error panel |
| 인터랙션 | 이벤트 핸들러, validation, toast |
| 접근성 | aria 속성, 키보드 네비게이션, 포커스 순서 |

### 구현 규칙

1. 디자인 명세에 없는 동작을 임의로 추가하지 않습니다.
2. 설계 변경이 필요하면 디자인 문서를 먼저 갱신합니다.
3. 색상은 SLDS 토큰 우선, 필요한 경우에만 CSS 변수 추가합니다.
4. 디자이너는 기본적으로 SLDS 표준을 참고해 설계하고, SLDS로 구현이 어려운 경우에만 커스텀 디자인을 허용합니다.
5. 화면 내 컴포넌트는 상태/간격/타이포 기준을 통일해 일관적인 디자인을 유지합니다.

```css
/* SLDS 토큰 우선 */
.my-component {
  background-color: var(--slds-g-color-brand-base-50);
}

/* SLDS에 없는 값만 커스텀 변수 */
:host {
  --c-brand-primary: #1a73e8;
}
```

### LWC 구현 체크리스트

- [ ] SLDS 클래스 활용 (커스텀 CSS 최소화)
- [ ] 반응형 고려 (`slds-size_*` 클래스)
- [ ] 접근성 (aria 속성, 키보드 네비게이션)
- [ ] 디자인 명세의 상태 정의(기본/로딩/오류) 반영
- [ ] QA 인수 기준과 동기화

### QA 검증 기준

- QA의 기본 검증 기준은 요구사항 문서와 디자인 명세입니다.
- 사용성 불편 요소를 발견하면 요구사항 범위를 벗어나지 않는 개선안을 별도 제안으로 기록합니다.
