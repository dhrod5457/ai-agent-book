# 8장. Skill 본문을 실행 가능하게 쓰기

Skill이 선택된 뒤에는 본문이 실행 계약이 된다.

본문의 목적은 “이 업무에 대해 많이 설명하는 것”이 아니라 모델이 필요한 판단을 하고, 올바른 순서로 행동하고, 완료 여부를 확인할 수 있게 하는 것이다.

## 8.1 설명서보다 실행 계약

좋은 Skill 본문은 필요에 따라 다음 요소를 가진다.

- 목적
- 적용 조건과 제외 조건
- 사전 조건
- 핵심 workflow
- guardrail
- fallback
- verification
- output contract
- handoff
- 필요한 reference와 script

모든 Skill에 같은 섹션을 강제로 넣을 필요는 없다. 좁은 Skill은 몇 문단이면 충분할 수 있다.

핵심은 실제 failure mode에 필요한 계약이 빠지지 않는 것이다.

## 8.2 단계는 관찰 가능한 행동으로 쓴다

약한 절차는 다음과 같다.

1. 문제를 분석한다.
2. 잘 수정한다.
3. 충분히 테스트한다.

각 단계가 무엇을 의미하는지 확인할 방법이 없다.

더 좋은 workflow는 단계가 끝날 때 관찰 가능한 상태가 생긴다.

1. 변경 대상과 현재 behavior를 확인한다.
2. 가장 좁은 재현 경로를 선택한다.
3. 수정 전 실패를 확인한다.
4. 최소 변경을 수행한다.
5. 같은 검증을 다시 실행한다.
6. 인접 회귀를 확인한다.
7. 사용한 증거를 결과에 남긴다.

이런 단계는 성공과 실패를 구분할 수 있다.

## 8.3 모든 것을 고정하지 않는다

Skill은 workflow를 안정화하지만 모델의 모든 판단을 제거하면 안 된다.

강하게 고정할 가치가 있는 것은 다음이다.

- 안전 경계
- 순서가 정확도에 필수인 단계
- 반드시 필요한 산출물
- 완료 조건
- 금지 행동
- 승인 경계

반대로 모델 판단에 맡길 수 있는 것은 탐색 파일의 정확한 순서, 사소한 구현 방식, 몇 번 검색할지, 일반적인 코딩 습관이다.

최신 모델일수록 과도한 레시피는 오히려 성능을 제한할 수 있다.

## 8.4 Preconditions

많은 Skill 실패는 시작 조건을 확인하지 않아서 발생한다.

예를 들어 migration Skill이라면 대상 DB, migration framework, 현재 schema 상태가 필요할 수 있다.

배포 Skill이라면 대상 환경, artifact, 승인 상태가 필요할 수 있다.

사전 조건이 없을 때 모델이 임의로 값을 만들어내지 않게 해야 한다.

가능한 반응은 세 가지다.

- 안전한 기본값이 있으면 사용
- 필요한 source에서 조회
- 없으면 멈추고 사용자나 상위 workflow로 handoff

## 8.5 State owner

workflow가 여러 Skill로 나뉘면 누가 상태를 바꾸는지 중요해진다.

예를 들어 prepare, validate, deploy가 각각 독립 Skill이라면 “validated” 상태와 “deployed” 상태의 owner가 겹치면 안 된다.

좋은 설계는 각 Skill이 어떤 상태를 요구하고, 어떤 상태를 만들 수 있는지 구분한다.

이 구분이 없으면 validation Skill이 배포까지 해버리거나, prepare Skill이 승인 상태를 암묵적으로 바꿀 수 있다.

## 8.6 Side-effect intent gate

사용자가 “배포 준비해줘”라고 했다고 실제 배포까지 허용된 것은 아니다.

prepare, preview, plan과 execute, publish, deploy를 구분해야 한다.

side effect가 큰 Skill일수록 다음을 확인한다.

- 사용자 요청이 실제 mutation 의도를 포함하는가.
- 어떤 단계까지 자동으로 실행할 수 있는가.
- 어디서 승인이나 handoff가 필요한가.
- mutation 결과를 무엇으로 확인하는가.

자연어 경고 하나로 모든 위험을 해결하려 하지 않는다. 필요한 경우 permission과 Hook 같은 구조적 경계와 결합한다.

## 8.7 Freedom level

모든 Skill이 같은 정도로 구체적일 필요는 없다.

### 낮은 자유도

정확한 순서가 중요하고 side effect가 큰 작업.

예: schema migration 적용, production publish.

### 중간 자유도

검증 단계는 고정하지만 탐색과 구현 방식은 유연한 작업.

예: 버그 수정, CI failure triage.

### 높은 자유도

산출물 목표와 품질 기준만 있고 경로는 다양할 수 있는 작업.

예: 코드 설명, 리서치 요약.

Skill 본문은 업무의 위험과 결정성에 맞춰 자유도를 조절해야 한다.

## 8.8 Done when

“충분히 좋아질 때까지 반복”은 종료 조건이 아니다.

좁은 Skill은 한 문장의 completion criterion만으로도 강해질 수 있다.

예:

> 요청한 artifact가 생성되고 지정된 validator가 성공하면 완료한다.

또는:

> migration이 대상 환경에 적용된 것이 아니라, migration 파일과 검증 결과가 준비되면 이 Skill의 역할은 끝난다.

Done when은 불필요한 search loop와 over-verification을 줄인다.

## 8.9 Output contract

Skill의 마지막에는 무엇을 반환해야 하는지 필요할 수 있다.

- 변경 파일
- 검증 결과
- 실패 원인
- 다음 handoff
- 생성된 artifact 위치
- 미해결 위험

output contract는 보고서를 길게 만들기 위한 것이 아니라 다음 단계가 필요한 정보를 잃지 않게 하기 위한 것이다.

좋은 Skill 본문은 “무엇을 생각하라”보다 **무엇을 확인하고, 무엇을 바꾸고, 무엇으로 끝났음을 증명할지**를 분명히 한다.
