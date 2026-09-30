# 부록 B. Skill Eval 템플릿

이 템플릿은 Skill을 “느낌”이 아니라 반복 가능한 평가 대상으로 만들기 위한 최소 구조다.

## B.1 Eval Metadata

- date:
- model:
- model version:
- host:
- host version:
- repository commit:
- Skill name:
- candidate revision:
- available Skill inventory:
- evaluator:
- notes:

## B.2 Success Definition

### Outcome

무엇이 실제로 완료되어야 하는가.

### Process

반드시 수행되어야 하는 절차나 tool 사용이 있는가.

### Style

산출물 형식에 필수 요구가 있는가.

### Efficiency

불필요한 tool call, reference read, 전체 회귀, 반복 탐색의 허용 범위는 무엇인가.

## B.3 Trigger Corpus

각 case는 다음 필드를 가진다.

- id
- class
- prompt
- expected route
- forbidden route
- notes

권장 class:

- explicit-positive
- implicit-positive
- noisy-positive
- adjacent-negative
- routing-pair
- none
- boundary
- missing-precondition

## B.4 반복 실행

중요한 case는 한 번만 실행하지 않는다.

기록 항목:

- run number
- actual route
- selected Skill source
- latency
- input tokens
- output tokens
- reference reads
- notes

## B.5 Routing Metrics

### Accuracy

기대 route와 실제 route가 일치한 비율.

### False Positive Rate

none 또는 adjacent negative에서 잘못 호출된 비율.

### Collision Error Rate

routing pair에서 인접 Skill을 잘못 선택한 비율.

### Abstention Accuracy

Skill이 필요 없을 때 호출하지 않은 비율.

### Run Consistency

동일 prompt 반복 실행에서 동일 route가 나온 비율.

## B.6 Output Checks

### Deterministic Checks

예:

- expected file exists
- forbidden file unchanged
- schema valid
- focused test passed
- required command executed
- output contains required identifier

### Rubric Checks

예:

- 사용자의 실제 문제를 해결했는가.
- 핵심 위험을 빠뜨리지 않았는가.
- 근거와 결론을 구분했는가.
- 과도한 검증을 하지 않았는가.

## B.7 Baseline Matrix

최소 비교:

- without Skill
- current Skill
- proposed Skill

필요한 경우:

- length-control instruction
- different model
- different host
- manual-only variant

## B.8 Blinding

가능하면 candidate에게 eval 목적을 노출하지 않는다.

judge에게 current/proposed label을 숨긴다.

동일 task, 동일 repository state, 동일 Skill inventory를 사용한다.

## B.9 Artifact Preservation

최종 답변만 남기지 않는다.

보존 후보:

- prompt
- trace
- selected Skill source
- files read
- files changed
- command output
- test output
- final artifact
- token/time metadata

## B.10 결과 해석

한 지표만 보고 승자를 정하지 않는다.

예를 들어 description 축소가 성공이라고 하려면 보통 다음을 함께 본다.

- metadata token 감소
- accuracy 비열화 없음
- 특정 Skill recall 급락 없음
- false positive 증가 없음

Boundary-aware description이 개선이라고 하려면 다음을 함께 본다.

- overall accuracy 유지 또는 개선
- collision error 감소
- false positive 증가 없음

## B.11 Regression Loop

실제 운영 실패가 발생하면:

1. 실패 prompt와 trace를 저장한다.
2. 가장 가까운 기존 corpus class를 정한다.
3. 수정 전 재현한다.
4. 지침을 변경한다.
5. 해당 case와 전체 regression을 실행한다.
6. 결과와 원인을 기록한다.

이 과정을 통해 correction이 일회성 문장 추가가 아니라 재발 방지 자산이 된다.
