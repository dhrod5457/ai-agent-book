# Trigger Eval Corpus v0.1

목적: `feature`, `bugfix`, `refactor`, `review`, `none` 사이의 routing을 description variant별로 비교하기 위한 80개 prompt corpus.

이 corpus는 **실험 입력**이지 결과가 아니다.

## Label contract

| Label | 정의 |
| --- | --- |
| `feature` | 기존에 없던 동작/기능을 추가하거나 제품 동작을 확장 |
| `bugfix` | 이미 기대되는 동작이 깨졌거나 회귀/오류를 수정 |
| `refactor` | 외부 동작을 유지하면서 내부 구조를 개선 |
| `review` | 구현하지 않고 변경/설계/코드의 문제를 검토 |
| `none` | 위 네 workflow를 실행할 필요가 없는 설명/질문/탐색 |

판정 원칙:

- prompt의 단어가 아니라 사용자의 **요청 결과**로 label을 정한다.
- "clean", "improve", "review" 같은 단어 자체를 trigger로 보지 않는다.
- 한 prompt에 여러 맥락이 있어도 최종적으로 요청된 작업을 기준으로 한다.

---

# P1. Explicit Positive — 16

## Feature

| ID | Prompt | Expected |
| --- | --- | --- |
| EP-F01 | 공개 API에 rate limiting 기능을 추가해줘. | feature |
| EP-F02 | 사용자 프로필에서 다크 모드를 켜고 끌 수 있는 설정을 추가해줘. | feature |
| EP-F03 | 주문 목록에 CSV 내보내기 기능을 구현해줘. | feature |
| EP-F04 | 관리자 화면에서 계정을 일괄 비활성화하는 기능을 추가해줘. | feature |

## Bugfix

| ID | Prompt | Expected |
| --- | --- | --- |
| EP-B01 | 비밀번호가 비어 있으면 로그인 API가 500을 반환한다. 이 버그를 고쳐줘. | bugfix |
| EP-B02 | 페이지를 새로고침하면 장바구니가 사라지는 버그를 수정해줘. | bugfix |
| EP-B03 | 같은 알림이 두 번 발송되는 문제를 고쳐줘. | bugfix |
| EP-B04 | Windows에서만 테스트가 실패하는 경로 처리 버그를 수정해줘. | bugfix |

## Refactor

| ID | Prompt | Expected |
| --- | --- | --- |
| EP-R01 | 이 서비스 클래스가 너무 커졌다. 동작은 그대로 두고 책임별로 리팩터링해줘. | refactor |
| EP-R02 | 중복된 validation 코드를 공통화하되 외부 동작은 바꾸지 마. | refactor |
| EP-R03 | 이 패키지의 의존성 방향을 정리해줘. 기능 변경은 없어야 한다. | refactor |
| EP-R04 | 오래된 helper 구조를 정리해서 읽기 쉽게 리팩터링해줘. | refactor |

## Review

| ID | Prompt | Expected |
| --- | --- | --- |
| EP-V01 | 이 PR을 코드 리뷰해줘. 수정은 하지 말고 문제만 알려줘. | review |
| EP-V02 | 이번 변경에 보안 문제가 있는지 검토만 해줘. | review |
| EP-V03 | 이 설계가 현재 구조와 충돌하는지 리뷰해줘. 구현은 하지 마. | review |
| EP-V04 | 커밋 diff를 보고 성능 회귀 가능성만 검토해줘. | review |

---

# P2. Implicit Positive — 16

직접적인 workflow 이름을 최대한 사용하지 않는다.

## Feature

| ID | Prompt | Expected |
| --- | --- | --- |
| IP-F01 | 지금은 이메일로만 알림을 보내는데 Slack으로도 받을 수 있게 해줘. | feature |
| IP-F02 | 검색 결과를 날짜와 상태로 좁혀 볼 수 있었으면 좋겠어. | feature |
| IP-F03 | 로그인한 사용자가 자기 활성 세션을 보고 종료할 수 있게 만들어줘. | feature |
| IP-F04 | 업로드한 파일 처리 진행률을 화면에서 볼 수 있게 해줘. | feature |

## Bugfix

| ID | Prompt | Expected |
| --- | --- | --- |
| IP-B01 | 만료된 토큰이면 401이 나와야 하는데 지금은 NullPointerException이 난다. | bugfix |
| IP-B02 | 할인 코드 하나를 적용했는데 결제 금액에서 두 번 차감된다. | bugfix |
| IP-B03 | 저장 버튼을 한 번 눌렀는데 요청이 두 번 전송된다. | bugfix |
| IP-B04 | 정렬을 내림차순으로 선택해도 두 번째 페이지부터 다시 오름차순이 된다. | bugfix |

## Refactor

| ID | Prompt | Expected |
| --- | --- | --- |
| IP-R01 | 기능은 잘 되는데 controller가 repository까지 직접 호출하고 있다. 계층을 정리하고 싶다. | refactor |
| IP-R02 | 같은 문자열 파싱 로직이 네 군데 복사돼 있다. 결과는 그대로 유지하면서 정리해줘. | refactor |
| IP-R03 | 이 모듈은 테스트하기 어렵게 전역 상태에 묶여 있다. 동작은 그대로 두고 의존성을 분리해줘. | refactor |
| IP-R04 | 현재 API 결과는 바꾸지 말고 내부 DTO 변환 흐름만 단순하게 만들어줘. | refactor |

## Review

| ID | Prompt | Expected |
| --- | --- | --- |
| IP-V01 | 이 변경을 merge하기 전에 놓친 edge case가 있는지만 찾아줘. | review |
| IP-V02 | 코드 건드리지 말고 이 인증 흐름에서 공격 가능한 지점을 찾아줘. | review |
| IP-V03 | 이 두 구현 중 현재 코드베이스 규칙을 어긴 부분이 있는지 확인해줘. | review |
| IP-V04 | 테스트는 통과한다. 그래도 배포 전에 위험한 부분이 있는지 diff 기준으로 봐줘. | review |

---

# P3. Noisy Positive — 12

길거나 관련 없는 맥락 안에서 최종 요청을 구분해야 한다.

## Feature

| ID | Prompt | Expected |
| --- | --- | --- |
| NP-F01 | 지난주에 로그인 장애는 해결했고 캐시도 정리했다. 지금 급한 건 그게 아니다. 고객이 관리자 화면에서 사용자별 API 사용량을 보고 싶다고 한다. 이 조회 기능을 추가해줘. | feature |
| NP-F02 | 이 저장소는 오래됐고 테스트도 느리지만 이번에는 손대지 말자. 요구사항은 기존 다운로드 버튼 옆에 PDF 출력 옵션을 하나 더 제공하는 것이다. | feature |
| NP-F03 | 메시지 큐 설정은 그대로 두고 싶다. 운영팀 요청은 실패한 배치 작업을 관리자 화면에서 다시 실행할 수 있게 하는 것이다. | feature |

## Bugfix

| ID | Prompt | Expected |
| --- | --- | --- |
| NP-B01 | 새 기능을 추가하려는 건 아니다. 최근 배포 이후 사용자 이름에 한글이 있으면 프로필 저장이 실패한다. 이전에는 됐다. 원인을 찾아 정상 동작으로 돌려줘. | bugfix |
| NP-B02 | 로그 구조나 예외 계층을 정리할 생각은 나중에 하자. 지금은 파일이 10MB를 넘으면 정상적인 validation 메시지 대신 connection reset이 발생하는 문제만 해결해줘. | bugfix |
| NP-B03 | API 문서가 낡았지만 이번 작업 범위에서는 제외한다. 동일한 결제를 빠르게 두 번 누르면 주문이 두 개 생기는 회귀를 막아줘. | bugfix |

## Refactor

| ID | Prompt | Expected |
| --- | --- | --- |
| NP-R01 | 성능 문제는 없고 사용자 요구사항도 바뀐 게 없다. 다만 결제 서비스가 이메일 발송, 재고, 영수증 생성까지 직접 알고 있어 다음 변경이 어렵다. 외부 동작을 유지하면서 책임을 나눠줘. | refactor |
| NP-R02 | 테스트가 모두 녹색이고 현재 결과도 맞다. 이번에는 기능을 추가하지 않는다. 중복된 세 개의 query builder를 하나의 일관된 구조로 정리해줘. | refactor |
| NP-R03 | API contract와 DB schema는 건드리면 안 된다. 지금 목표는 생성자 인자가 14개인 클래스를 유지보수하기 쉬운 내부 구조로 바꾸는 것이다. | refactor |

## Review

| ID | Prompt | Expected |
| --- | --- | --- |
| NP-V01 | 팀원이 이미 구현을 끝냈고 테스트도 추가했다. 네가 직접 고칠 필요는 없다. diff를 보고 concurrency 문제나 데이터 손실 위험이 있는지만 지적해줘. | review |
| NP-V02 | 새로운 설계를 다시 만들 필요는 없다. 제안된 migration plan을 읽고 rollback이 어려운 단계와 누락된 검증만 찾아줘. | review |
| NP-V03 | 이 PR은 UI 변경이 대부분이지만 서버 endpoint도 하나 건드렸다. 코드는 수정하지 말고 권한 검사가 빠졌는지와 review해야 할 부분을 정리해줘. | review |

---

# P4/P5. Adjacent Negative & Routing Pair — 24

각 case는 두 개 이상의 Skill이 표면적으로 관련 있어야 한다.

## Feature vs Bugfix

| ID | Prompt | Expected | Boundary |
| --- | --- | --- | --- |
| RP-01 | 기존에는 첨부파일 미리보기가 없었다. 이제 PDF 미리보기를 지원해줘. | feature | not bugfix |
| RP-02 | PDF 미리보기는 원래 되는데 20페이지가 넘으면 빈 화면이 된다. | bugfix | not feature |
| RP-03 | 현재 이메일 알림만 있다. SMS 알림도 선택할 수 있게 해줘. | feature | not bugfix |
| RP-04 | SMS 알림 기능은 이미 있는데 전화번호에 하이픈이 있으면 발송되지 않는다. | bugfix | not feature |
| RP-05 | 검색에 상태 필터가 아예 없다. 상태 필터를 추가해줘. | feature | not bugfix |
| RP-06 | 상태 필터가 있는데 두 번째 페이지에서는 선택값을 무시한다. | bugfix | not feature |

## Feature vs Refactor

| ID | Prompt | Expected | Boundary |
| --- | --- | --- | --- |
| RP-07 | 응답 형식은 그대로 두고 service와 repository 경계를 정리해줘. | refactor | not feature |
| RP-08 | service 구조는 지금대로 두고 응답에 마지막 로그인 시간을 새로 추가해줘. | feature | not refactor |
| RP-09 | 사용자에게 보이는 동작은 하나도 바꾸지 말고 4개의 중복 adapter를 통합해줘. | refactor | not feature |
| RP-10 | adapter 정리는 하지 말고 새로운 S3-compatible storage provider를 지원해줘. | feature | not refactor |
| RP-11 | API contract를 유지하면서 예외 변환을 한 계층으로 모아줘. | refactor | not feature |
| RP-12 | 기존 오류 응답에 requestId를 새 필드로 노출해줘. | feature | not refactor |

## Bugfix vs Refactor

| ID | Prompt | Expected | Boundary |
| --- | --- | --- | --- |
| RP-13 | 코드가 지저분한 건 맞지만 지금은 잘못 계산되는 세금 금액만 정상화해줘. 구조 개선은 하지 마. | bugfix | not refactor |
| RP-14 | 세금 계산 결과는 현재 맞다. 계산 규칙이 세 파일에 흩어져 있으니 동작을 유지하면서 한곳으로 정리해줘. | refactor | not bugfix |
| RP-15 | flaky test의 원인이 production code의 race condition이다. 실제 race를 고쳐줘. | bugfix | not refactor |
| RP-16 | 동작 문제는 없다. 비동기 처리 코드가 callback과 future가 섞여 있으니 한 방식으로 정리해줘. | refactor | not bugfix |
| RP-17 | 캐시 계층을 다시 설계할 필요는 없다. TTL이 60초 설정인데 실제로 60분 유지되는 문제만 수정해줘. | bugfix | not refactor |
| RP-18 | 캐시 동작은 맞다. TTL 계산 코드가 각 adapter에 복제되어 있으니 중복만 제거해줘. | refactor | not bugfix |

## Review vs Execution

| ID | Prompt | Expected | Boundary |
| --- | --- | --- | --- |
| RP-19 | 이 PR에서 발견한 문제를 직접 수정하지 말고 리뷰 코멘트 형태로만 정리해줘. | review | not bugfix/refactor |
| RP-20 | 리뷰는 이미 끝났다. 지적된 null 처리 문제를 실제 코드에서 고쳐줘. | bugfix | not review |
| RP-21 | 아키텍처를 바꾸기 전에 현재 의존성 구조의 문제점만 검토해줘. 아직 수정하지 마. | review | not refactor |
| RP-22 | 검토는 끝났고 방향도 승인됐다. 이제 외부 동작 유지하면서 의존성 방향을 실제로 정리해줘. | refactor | not review |
| RP-23 | 요구사항 문서를 보고 구현상 빠진 요구사항이 있는지만 확인해줘. | review | not feature |
| RP-24 | 검토 결과 누락된 것으로 확인된 계정 잠금 기능을 이제 구현해줘. | feature | not review |

---

# P6. None / Abstention — 12

Skill을 실행하지 않는 것이 맞는 case.

| ID | Prompt | Expected | 이유 |
| --- | --- | --- | --- |
| NO-01 | 이 repository가 어떤 역할을 하는지 설명해줘. | none | 설명 요청 |
| NO-02 | 이 함수 이름에서 reconcile은 무슨 의미야? | none | 의미 설명 |
| NO-03 | Java record와 일반 class 차이를 알려줘. | none | 일반 지식 |
| NO-04 | 이 에러 로그가 의미하는 바만 설명해줘. 아직 수정하지 마. | none | 진단 설명만 요청 |
| NO-05 | 현재 브랜치 이름이 뭐야? | none | 상태 조회 |
| NO-06 | 이 API endpoint가 어디서 호출되는지 찾아줘. | none | 탐색 |
| NO-07 | 테스트가 몇 개인지 확인해줘. 실행은 하지 말고 파일 기준으로만. | none | 조사 |
| NO-08 | 이 설계 문서를 세 문장으로 요약해줘. | none | 요약 |
| NO-09 | dependency injection이 왜 필요한지 이 코드 기준으로 설명해줘. | none | 설명 |
| NO-10 | 지금 변경된 파일 목록만 보여줘. | none | 상태 조회 |
| NO-11 | 이 두 commit의 차이를 설명만 해줘. | none | 비교 설명 |
| NO-12 | 이 TODO가 언제 추가됐는지 git history에서 찾아줘. | none | 이력 조사 |

---

# Corpus Quality Checks

## 1. Keyword leakage

다음 단어를 label 근거로 사용하지 않는다.

- feature
- bugfix
- refactor
- review

Explicit Positive 그룹에는 자연스럽게 일부 사용해도 되지만, implicit/routing 그룹은 가능한 한 workflow 이름 없이 의도를 표현한다.

## 2. Pair symmetry

가능한 pair는 대칭 case를 둔다.

예:

- 기능이 없음 → feature
- 기능은 있는데 깨짐 → bugfix

- 동작은 맞고 구조만 변경 → refactor
- 구조는 그대로 두고 새 동작 → feature

이렇게 해야 특정 keyword가 아니라 boundary를 검증할 수 있다.

## 3. None은 쉬운 질문만 두지 않는다

`NO-04`, `NO-06`, `NO-12`처럼 coding context는 있지만 실행 workflow는 필요 없는 case를 포함한다.

false-positive를 제대로 보기 위함이다.

## 4. Paraphrase Holdout

실험 전 corpus의 20%를 holdout으로 분리한다.

description을 수정할 때 holdout prompt를 보지 않는다.

추천:

- train/tuning set: 64
- holdout: 16

최종 숫자는 random seed와 함께 고정한다.

## 5. Model별 번역 금지

한국어 corpus를 영어로 자동 번역해 같은 case라고 취급하지 않는다.

언어 자체가 routing behavior에 영향을 줄 수 있다.

영문 실험이 필요하면 별도 English corpus를 만든다.

## 6. 결과 기록

각 prompt의 raw result를 보존한다.

최소:

- expected
- selected
- run index
- model
- host
- model/host version
- description variant
- available Skill metadata snapshot
- latency/token 정보

---

# 예상되는 실패 유형

이 항목도 결과를 보기 전에 정의한다.

## F1. Broad Capture

너무 넓은 Skill이 인접 요청을 가져감.

## F2. Keyword Capture

의도보다 특정 단어 하나에 반응.

## F3. Under-trigger

implicit/noisy positive를 놓침.

## F4. Boundary Collapse

feature/bugfix 또는 feature/refactor를 구분하지 못함.

## F5. Abstention Failure

설명/탐색 요청에서도 workflow Skill을 호출.

## F6. Run Instability

동일 prompt 반복에서 label이 자주 바뀜.

## F7. Manual-only Leakage

model-visible 목록에서 제외돼야 할 Skill을 여전히 자동 선택.

---

# 이 corpus로 검증할 주장

실험 결과에 따라 다음 문장을 책에 유지하거나 수정한다.

1. what + when description은 broad description보다 routing에 유리하다.
2. 인접 boundary 문장은 collision을 줄인다.
3. description은 body의 요약이 아니라 selection을 위한 interface다.
4. negative/none case 없는 trigger eval은 충분하지 않다.
5. manual-only와 auto-trigger Skill은 서로 다른 eval 기준이 필요하다.
6. description을 짧게 만드는 것 자체보다 routing 정보를 남기는 것이 중요하다.

이 주장들은 현재 **가설**이며 실험 결과가 나오기 전에는 사실로 서술하지 않는다.
