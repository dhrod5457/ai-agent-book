# 19장. 지침 파일 리뷰 프로세스

지침 파일을 소프트웨어 artifact로 본다면 변경에도 리뷰 프로세스가 필요하다.

중요한 것은 거대한 승인 절차를 만드는 것이 아니다.

작은 변경이라도 “왜 필요한지, 어디에 적용되는지, 무엇으로 검증할지, 언제 삭제할지”를 생각하는 습관을 만드는 것이다.

## 19.1 Why

첫 질문은 문장 내용이 아니라 변경 이유다.

- 실제 실패 사례가 있었는가.
- 사용자 correction이 있었는가.
- 모델이나 host가 바뀌었는가.
- 제품 문법이 바뀌었는가.
- 새로운 workflow가 생겼는가.
- 단순히 좋아 보이는 규칙을 추가하려는가.

실패 근거가 없는 일반론은 상시 instruction에 추가하기 전에 더 엄격하게 본다.

## 19.2 Scope

다음 질문은 어디에 적용해야 하는가다.

- repository 전체
- 특정 directory
- 특정 file type
- 특정 task
- 특정 side effect
- 특정 provider

Scope를 결정하기 전에는 문장을 쓰지 않는 편이 좋다.

## 19.3 Canonical source

지침이 의존하는 사실의 owner를 확인한다.

- code
- config
- schema
- generated type
- CLI help
- official docs
- runtime state
- Skill reference

이미 canonical source가 있으면 값을 복제하지 않는다.

## 19.4 Behavior change

“문서를 더 명확하게 했다”보다 구체적으로 적는다.

예:

- migration과 query 요청이 같은 Skill로 라우팅되던 것을 분리한다.
- frontend 작업에서 backend test 지침이 노출되지 않게 한다.
- publish 전에 approval state를 Hook에서 확인한다.
- stale CLI option table을 제거하고 runtime help를 사용한다.

지침 변경은 기대 행동의 before/after로 설명할 수 있어야 한다.

## 19.5 Structural verification

기계적으로 검증 가능한 부분을 먼저 확인한다.

- parse
- required fields
- local references
- script paths
- registration
- matcher syntax
- Hook test
- state metadata

이 검사는 빠르고 결정론적이어야 한다.

## 19.6 Semantic Eval

그 다음 의미와 행동을 평가한다.

Skill description 변경이면 positive, negative, routing pair를 실행한다.

본문 변경이면 output과 process를 본다.

scope 변경이면 irrelevant-rule leakage와 필요한 rule miss를 본다.

model upgrade면 baseline과 current를 다시 비교한다.

## 19.7 Risk

지침 변경이 다음을 바꾸는지 확인한다.

- tool permission
- production side effect
- secret access
- 외부 비용
- 데이터 삭제
- 사용자 승인 경계
- 운영 시간

Markdown 변경이라고 risk가 낮다고 가정하지 않는다.

## 19.8 Portability

공통 지침인지 provider-specific instruction인지 명시한다.

Portable principle과 vendor syntax를 한 문단에 섞지 않는다.

도구별 동작이 다르면 adapter 파일에서 처리한다.

## 19.9 Removal condition

새 규칙을 넣을 때부터 삭제 조건을 생각한다.

예:

- 다음 major model에서 재평가
- upstream bug 수정 시 삭제
- validator가 배포되면 prose checklist 축소
- legacy version 지원 종료 시 alias 제거
- 해당 directory 제거 시 path rule 삭제

이 항목 하나만 있어도 instruction debt가 영구화되는 것을 줄일 수 있다.

## 19.10 Feedback에서 regression으로

좋은 유지보수 loop는 다음과 같다.

사용자 correction
→ 실패 사례 보존
→ 원인 분류
→ scope 또는 structure 수정
→ eval candidate 추가
→ regression 실행
→ 필요하면 prose 삭제

사용자의 correction을 곧바로 “한 줄 더 추가”로 처리하지 않는다.

## 19.11 최종 열 가지 질문

리뷰 마지막에는 다음을 묻는다.

1. 언제 활성화되는가.
2. 언제 활성화되면 안 되는가.
3. 시작 전에 무엇이 참이어야 하는가.
4. state와 authority owner는 누구인가.
5. 어떤 절차가 실제로 필요한가.
6. 어떤 side effect와 권한이 있는가.
7. 무엇으로 완료를 증명하는가.
8. 어디서 멈추고 handoff하는가.
9. 바뀌는 사실은 어디서 다시 읽는가.
10. 어떤 failure나 eval이 이 지침을 수정하거나 삭제하게 하는가.

모든 파일이 열 질문에 똑같이 답할 필요는 없다.

하지만 해당 failure mode와 관련된 질문에 답이 없다면 그 지점이 리뷰 대상이다.

## 19.12 이 책의 결론

지침 파일 엔지니어링은 Markdown을 잘 쓰는 기술이 아니다.

범위를 나누고, canonical source를 정하고, 반복 절차를 Skill로 만들고, 결정론적 규칙을 구조로 옮기고, 남은 자연어를 eval하며, 오래된 지침을 삭제하는 작업이다.

처음에는 “모델에게 무엇을 더 알려줄까”로 시작한다.

성숙한 시스템에서는 질문이 바뀐다.

> **이 정보가 정말 항상 필요한가. 더 좁은 곳에 둘 수 없는가. 자연어가 아니라 구조가 소유해야 하는가. 그리고 이 지침이 실제로 도움이 된다는 증거가 있는가.**

이 질문을 반복할 수 있다면 지침 파일은 더 이상 쌓이기만 하는 프롬프트 묶음이 아니다.

버전 관리되고, 테스트되고, 삭제 가능한 엔지니어링 자산이 된다.
