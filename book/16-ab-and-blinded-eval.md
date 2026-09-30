# 16장. A/B와 Blinded Eval

지침 A와 B를 비교할 때 새 버전이 무엇인지 알고 평가하면 쉽게 편향된다.

“이번에 description을 개선했다”는 사실을 알고 있으면 작은 차이도 개선처럼 보일 수 있다.

그래서 지침 평가에도 blinded comparison이 유용하다.

## 16.1 기본 비교 단위

가장 단순한 비교는 다음이다.

- Baseline: Skill 없음
- Current: 현재 지침
- Proposed: 변경 지침

필요하면 length control이나 다른 model을 추가한다.

중요한 것은 같은 task와 같은 repository state에서 비교하는 것이다.

## 16.2 Organic prompt

candidate에게 “이것은 Skill 평가입니다”라고 알려주면 실제 사용과 다른 행동을 할 수 있다.

가능하면 실제 사용자 요청처럼 prompt를 작성한다.

trigger eval에서도 Skill 이름을 직접 넣은 prompt만 사용하면 자연어 discovery 능력을 평가할 수 없다.

## 16.3 Judge blind

결과를 평가하는 judge에게 어느 것이 current이고 proposed인지 숨긴다.

A, B 같은 임의 label을 사용하고 model identity도 필요하면 숨긴다.

이렇게 하면 “새 버전이 더 좋아야 한다”는 기대를 줄일 수 있다.

## 16.4 Candidate blind

candidate에게 rubric 전체를 보여주는 것도 조심한다.

rubric을 알고 있으면 실제 업무보다 grader를 만족시키는 행동을 할 수 있다.

실행자는 일반 사용자 요청만 받고, 평가는 별도 단계에서 수행하는 편이 더 현실적이다.

## 16.5 Root monolith vs scoped instruction

A/B 평가는 description뿐 아니라 지침 배치에도 사용할 수 있다.

예:

- B0: 모든 규칙을 root AGENTS.md에 둔다.
- B1: root + nested AGENTS.md
- B2: root + path-scoped Rules
- B3: root + path Rule + on-demand Skill

측정할 수 있는 항목:

- 필요한 규칙 준수율
- irrelevant-rule leakage
- 적절한 verification 선택
- over-verification
- 노출 instruction token
- 추가 retrieval 수
- completion cost

이 실험은 “nested가 항상 더 좋다”를 증명하기 위한 것이 아니다. 저장소 규모와 host에 따라 trade-off가 다를 수 있다.

## 16.6 Instruction Debt A/B

오래된 scaffolding을 제거할 때도 같은 방법을 쓴다.

- C0: legacy instruction
- C1: generic 반복과 old workaround를 제거한 diet
- C2: diet + machine-checkable rule을 구조로 이동

측정:

- task success
- rule violation
- 불필요한 tool call
- over-verification
- token
- latency
- 반복 self-check
- clarification count

삭제 후 품질이 유지되면서 비용이 줄면 debt 제거의 근거가 된다.

## 16.7 Eval isolation

A/B가 정확하려면 candidate 외 조건이 최대한 같아야 한다.

- 같은 fixture
- 같은 prompt
- 같은 host
- 같은 model
- 같은 Skill inventory
- 같은 repository state
- fresh session
- installed duplicate 없음

특히 candidate Skill과 기존 installed Skill이 동시에 보이면 routing 결과가 오염될 수 있다.

## 16.8 Evaluator permission

평가 도구도 필요 이상으로 강한 권한을 갖지 않는다.

trigger eval인데 global filesystem write나 config 변경 권한이 필요하지 않을 수 있다.

평가 과정의 side effect가 결과를 바꾸면 실험이 아니라 운영 변경이 된다.

## 16.9 Judge와 사람의 불일치

LLM judge 결과와 사람이 실제 artifact를 읽은 판단이 크게 다를 수 있다.

이때 즉시 사람 또는 judge가 틀렸다고 결론 내리지 않는다.

먼저 본다.

- rubric이 모호한가.
- 길이가 긴 답을 과대평가하는가.
- 정답 label이 노출됐는가.
- 실제 outcome보다 문체를 평가했는가.
- deterministic evidence가 누락됐는가.

Eval도 디버깅 대상이다.

## 16.10 결과 해석의 절제

A2가 A1보다 좋았다고 해서 “negative boundary는 항상 좋다”고 일반화하면 안 된다.

최소한 다음 맥락을 기록한다.

- model
- host
- version
- date
- Skill inventory
- task corpus
- repository fixture

이 책이 권장하는 것은 특정 variant의 승리가 아니다.

> 지침 변경도 다른 소프트웨어 변경처럼 **비교 가능한 조건에서 검증하고 회귀를 남기는 습관**이다.
