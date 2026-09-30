# 15장. Output Eval

Skill이 올바르게 호출되었다고 해서 작업이 성공한 것은 아니다.

Routing Eval이 “선택”을 본다면 Output Eval은 “선택된 뒤 실제로 무엇이 달라졌는가”를 본다.

## 15.1 평가 목표를 분해한다

하나의 총점만 두면 무엇이 좋아졌는지 알기 어렵다.

최소한 다음 네 축으로 나눈다.

### Outcome

요청한 결과가 실제로 완성되었는가.

### Process

필요한 절차, tool, validation을 사용했는가.

### Style

산출물 형식과 표현 요구를 지켰는가.

### Efficiency

불필요한 tool call, reference read, 반복 검증이 없는가.

업무에 따라 trace와 artifact를 별도 축으로 둘 수도 있다.

## 15.2 Self-report를 증거로 쓰지 않는다

모델이 “검증했습니다”라고 말하는 것은 검증 증거가 아니다.

가능하면 실제 artifact를 본다.

- test output
- build result
- git diff
- 생성 파일
- tool trace
- event log
- API response
- 상태 identifier

지침 시스템에서 가장 위험한 완료 조건은 모델의 자기 선언이다.

## 15.3 Deterministic grader

기계적으로 판정 가능한 항목은 먼저 deterministic grader로 처리한다.

예:

- 파일이 생성됐는가.
- JSON schema를 만족하는가.
- 금지 파일이 수정되지 않았는가.
- test가 성공했는가.
- 특정 command가 호출됐는가.
- 링크가 유효한가.

이 영역에 LLM judge를 사용할 이유가 적다.

## 15.4 Rubric grader

정확성, 설명 품질, trade-off 적절성처럼 기계적으로 바로 판정하기 어려운 것은 rubric 기반 평가가 필요할 수 있다.

좋은 rubric은 추상적인 “좋음”보다 관찰 가능한 기준을 가진다.

예:

- 사용자가 요구한 세 가지 위험을 모두 다뤘는가.
- 주장마다 실제 source가 연결되는가.
- 대안의 조건과 trade-off가 구분되는가.

LLM judge를 사용할 수 있지만 절대적인 truth로 취급하지 않는다.

## 15.5 Process goal의 함정

Skill이 특정 절차를 강제한다고 해서 항상 그 절차를 많이 수행할수록 좋은 것은 아니다.

예를 들어 “검증을 철저히 하라”는 Skill이 모든 변경에서 full regression을 실행하면 outcome은 좋아 보일 수 있지만 비용이 폭증한다.

따라서 process goal은 필요한 evidence와 최소 충분 경로를 함께 정의해야 한다.

## 15.6 Evidence ladder

검증 강도를 단계적으로 올린다.

1. static validation
2. focused unit test
3. integration test
4. acceptance test
5. production mutation

항상 가장 강한 검증부터 실행하지 않는다.

가장 싼 충분한 evidence를 먼저 사용하고, 불확실성이 남을 때 escalation한다.

## 15.7 Suspicious pass

테스트가 너무 쉽게 통과하면 실제 실패를 감지하는지 확인할 수 있다.

가능한 경우 조건을 의도적으로 깨뜨려 RED를 확인하고 복구 후 GREEN을 확인한다.

특히 새 validator나 Hook test는 “성공한다”만으로 충분하지 않다. 실제 위반을 잡는지 확인해야 한다.

## 15.8 Artifact와 Trace를 함께 남긴다

최종 답변만 저장하면 왜 성공했는지 분석하기 어렵다.

가능하면 다음을 보존한다.

- input prompt
- 적용된 instruction/Skill
- tool calls
- 읽은 reference
- 실행 command
- 변경 파일
- test result
- 최종 artifact
- token/time metadata

이 기록은 나중에 instruction debt를 제거할 때도 중요하다.

## 15.9 Baseline

Skill이 있는 결과만 평가하면 Skill이 정말 필요한지 알 수 없다.

최소한 다음을 비교한다.

- without Skill
- with Skill

더 엄격한 실험에서는 current와 proposed Skill, length-matched irrelevant instruction, 다른 model을 비교할 수 있다.

모델 자체가 이미 잘하는 일을 Skill이 중복하고 있는지 확인해야 한다.

## 15.10 좋은 Output Eval

좋은 평가는 “결과가 괜찮아 보인다”에서 끝나지 않는다.

- 결과가 실제로 완성됐는가.
- 필요한 절차가 수행됐는가.
- 불필요한 절차는 줄었는가.
- 완료 증거가 있는가.
- baseline보다 개선됐는가.
- 개선 비용은 합리적인가.

Skill의 가치는 존재 여부가 아니라 **실제 행동과 결과의 차이**로 판단한다.
