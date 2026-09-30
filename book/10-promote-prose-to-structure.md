# 10장. Hook, lint, CI, type으로 승격하기

지침 파일이 계속 커지는 가장 큰 이유 중 하나는 반복 실패를 모두 자연어 규칙으로 고치려 하기 때문이다.

“이 파일은 수정하지 마라.”
“이 명령은 실행하지 마라.”
“변경 후 formatter를 실행하라.”
“frontmatter에는 이 필드가 있어야 한다.”

이런 규칙을 계속 CLAUDE.md나 Skill에 추가하면 모델은 매번 읽고 기억하고 판단해야 한다.

하지만 일부 규칙은 판단이 필요 없다.

## 10.1 지침과 enforcement의 차이

자연어 지침은 행동을 유도한다.

lint, type, schema, CI, Hook은 기계적으로 허용 여부를 판정한다.

따라서 먼저 묻는다.

> 이 규칙의 위반을 기계가 명확하게 판정할 수 있는가.

그렇다면 prose만으로 둘 이유가 약하다.

## 10.2 구조적 승격 사다리

반복되는 correction이 있으면 다음 순서로 더 강한 표현 수단을 검토한다.

1. 코드 구조나 type으로 불가능하게 만들 수 있는가.
2. schema나 validator로 판정할 수 있는가.
3. lint나 CI로 검사할 수 있는가.
4. Hook으로 lifecycle에 연결할 수 있는가.
5. canonical helper나 script로 한 경로만 제공할 수 있는가.
6. 그래도 판단이 필요하면 Rule, Skill, CLAUDE.md에 남긴다.

이 순서는 강한 장치가 항상 더 좋다는 뜻이 아니다. 가장 자연스러운 source of truth를 먼저 찾는다는 뜻이다.

## 10.3 Type과 schema

가능하면 잘못된 상태를 표현하기 어렵게 만든다.

예를 들어 metadata 필수 필드는 prose로 “반드시 넣어라”라고 적는 것보다 schema validation이 더 강하다.

상태 전이가 machine-readable하다면 exclusive owner 충돌도 validator가 잡을 수 있다.

## 10.4 Lint와 CI

정적 파일 내용이나 repository graph를 검사할 수 있다면 lint와 CI가 적합하다.

- broken local reference
- duplicate registration
- invalid frontmatter
- manifest 누락
- 금지된 generated file 직접 수정
- 존재하지 않는 script 경로

이런 오류를 LLM judge로 판정할 필요가 없다.

## 10.5 Hook

Hook은 특정 lifecycle event에서 검사를 실행하거나 작업을 막아야 할 때 유용하다.

예:

- Bash 명령 실행 전 위험한 패턴 검사
- 파일 수정 후 formatter 실행
- 특정 파일 변경 후 validator 실행
- publish 계열 mutation 전에 승인 상태 검사

Hook은 지침보다 결정론적이지만 실행 권한과 side effect를 가지므로 더 높은 보안 기준이 필요하다.

## 10.6 모든 것을 Hook으로 만들지 않는다

아키텍처 선택, 읽기 쉬움, 작은 변경 선호, 호환성 trade-off처럼 맥락과 판단이 필요한 기준은 Hook에 적합하지 않다.

기계적으로 명확하지 않은 품질을 regex나 blocking Hook으로 만들면 false positive가 늘어난다.

구조적 강제의 목적은 자연어를 없애는 것이 아니다.

> 사람이 판단할 필요가 없는 문제를 자연어 추론에서 빼는 것.

## 10.7 Prose-only safety gate의 한계

“절대 승인 없이 publish하지 마라”라는 Skill 문장만으로는 우회 경로를 모두 막기 어렵다.

다른 Skill이나 직접 tool call이 같은 mutation을 실행할 수 있다.

side effect가 큰 작업은 필요에 따라 다음을 조합한다.

- intent rule
- permission policy
- Hook
- deny test
- legitimate near-match allow test

중요한 것은 모든 것을 막는 것이 아니라 실제 위험 경계를 정확히 모델링하는 것이다.

## 10.8 Structural validator의 경계

좋은 validator는 의미를 평가하지 않는다.

잘하는 질문:

- 파일이 존재하는가.
- YAML이 parse되는가.
- 필수 필드가 있는가.
- reference가 존재하는가.
- matcher가 유효한가.
- duplicate registration이 있는가.

하지 말아야 할 질문:

- description이 좋은가.
- workflow가 합리적인가.
- 500줄을 넘었으니 나쁜가.
- MUST가 많으니 나쁜가.

이런 항목은 semantic eval이나 human review로 보내야 한다.

## 10.9 승격 후 prose도 줄인다

기계적 강제를 추가하고도 기존 자연어 규칙을 그대로 남기면 중복이 생긴다.

예를 들어 validator가 frontmatter schema를 완전히 검사한다면 CLAUDE.md에 필드 목록을 장문으로 유지할 필요가 없다.

대신 다음처럼 줄일 수 있다.

> Skill 변경 후 repository validator를 실행한다.

구조적 승격의 최종 목적은 **규칙을 더 많이 만드는 것**이 아니라 **single source of truth를 만드는 것**이다.
