# 18장. 모델이 바뀌면 지침도 다시 본다

모델 업그레이드는 지침 파일을 그대로 유지하고 model name만 바꾸는 이벤트가 아니다.

새 모델이 이전보다 더 잘하는 영역이 생기면 과거 scaffolding이 불필요해질 수 있다. 반대로 tool use나 routing 특성이 달라져 새로운 failure가 나타날 수도 있다.

따라서 모델 변경은 instruction audit의 trigger다.

## 18.1 무엇을 먼저 의심할 것인가

모델이 바뀌면 다음 유형의 지침을 우선 검토한다.

- think carefully 같은 일반 handholding
- 동일 의미의 반복 강조
- 모든 답변 끝에 붙는 self-check
- broad trigger booster
- 매우 세세한 step-by-step recipe
- 모델 기본 행동과 중복되는 clean code 일반론
- 과거 특정 모델의 약점을 보완한 workaround
- 오래된 tool limitation을 전제로 한 규칙

이것들을 무조건 삭제하는 것은 아니다. 현재 모델에서도 실제 효과가 있는지 다시 검증한다.

## 18.2 Safety rule은 함부로 지우지 않는다

모델이 강해졌다고 safety boundary가 사라지는 것은 아니다.

특히 publish, deploy, production write, destructive migration처럼 side effect가 큰 규칙은 모델 능력이 아니라 risk model에 의해 결정된다.

다만 안전을 이유로 과도한 차단을 넣은 경우는 다시 볼 수 있다.

예를 들어 checkpoint 이후 모든 관련 명령을 막았는데 실제로는 status 조회나 preview까지 차단한다면 legitimate near-match를 허용하도록 좁혀야 한다.

## 18.3 Broad trigger 재감사

새 모델은 description을 해석하는 방식이나 Skill 선택 성향이 달라질 수 있다.

이전 모델에서 recall을 높이기 위해 키워드를 많이 넣은 description이 새 모델에서는 false positive를 늘릴 수 있다.

따라서 model upgrade 시 trigger corpus를 그대로 다시 실행한다.

중요한 것은 새 corpus만 만드는 것이 아니라 기존 회귀 사례를 보존하는 것이다.

## 18.4 Closing checklist

과거에는 모델이 자주 완료 검증을 놓쳐 Skill 끝에 긴 체크리스트를 넣었을 수 있다.

새 모델에서 동일 체크리스트가 반복 self-check와 불필요한 test를 만든다면 더 좁은 completion criterion으로 줄일 수 있다.

예:

긴 열 항목 checklist보다

> 요청 artifact가 존재하고 지정된 validator가 성공하면 완료한다.

한 문장이 더 안정적일 수 있다.

## 18.5 Overly Strict Boundary

과거 failure를 막기 위해 특정 상황에서 무조건 stop하도록 만들었을 수 있다.

새 모델이 더 잘 판단할 수 있어도 stop rule은 계속 작업을 막는다.

다음 질문을 한다.

- 이 boundary가 실제 risk 때문인가.
- 아니면 과거 모델의 추론 한계 때문인가.
- 값싼 검증으로 대체할 수 있는가.
- stop 대신 fallback이나 escalation이 가능한가.

## 18.6 Portable instruction

여러 모델을 쓰는 팀은 특정 모델에 최적화된 세세한 행동 규칙을 repository 공통 지침에 넣는 것을 조심해야 한다.

공통 파일에는 project invariant와 task contract를 두고 model-specific workaround는 adapter layer나 별도 vendor file에 둔다.

그러면 한 모델을 교체할 때 전체 repository instruction을 다시 쓸 필요가 줄어든다.

## 18.7 Host-Tolerated Invalidity 재검사

새 host나 새 버전은 이전에 우연히 허용하던 잘못된 metadata를 더 엄격하게 거부할 수 있다.

따라서 upgrade audit에는 syntax와 packaging smoke test도 포함한다.

- frontmatter field
- allowed tools
- matcher
- path discovery
- nested instruction
- Skill registration

동작하던 것이 표준에 맞았다는 뜻은 아니다.

## 18.8 삭제도 변경이다

지침 삭제는 위험하게 느껴진다.

하지만 삭제 전후를 같은 eval corpus로 비교하면 통제할 수 있다.

- current
- diet
- structural

세 조건을 비교하고 task success가 유지되면서 token, tool call, over-verification이 줄어드는지 본다.

삭제는 감이 아니라 regression으로 수행할 수 있다.

## 18.9 모델 업그레이드 체크

업그레이드마다 최소한 다음을 수행한다.

1. root instruction에서 generic scaffolding 후보를 찾는다.
2. Skill description corpus를 재실행한다.
3. closing checklist와 recipe를 검토한다.
4. safety gate의 near-match false positive를 확인한다.
5. provider syntax와 packaging을 검증한다.
6. baseline 대비 Skill의 추가 가치가 남아 있는지 본다.
7. 제거한 지침도 회귀 기록을 남긴다.

모델이 좋아질수록 지침도 같이 좋아져야 한다.

그 방향은 대개 “더 많은 설명”보다 **더 적은 중복, 더 정확한 경계, 더 강한 evidence**다.
