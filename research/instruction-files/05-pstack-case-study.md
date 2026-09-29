# pstack 지침 파일 사례 분석

## 1. 분석 목적

pstack을 "좋은 에이전트 구조"의 정답으로 사용하지 않는다.

이 연구에서 pstack을 보는 이유는 공개 저장소 안에 실제로 많은 Skill, Rule, principle, playbook이 있고, 작성 규칙 자체도 명시되어 있기 때문이다.

분석 질문:

- 큰 지침을 어떻게 나누는가.
- Skill description을 어떻게 좁히는가.
- 서로 다른 Skill 사이에서 중복을 어떻게 피하는가.
- 원칙과 workflow를 어떻게 분리하는가.
- 지침 변경을 어떻게 검증하려 하는가.
- 반복 지시를 언제 구조적 장치로 옮기는가.

공식 저장소:

- https://github.com/cursor/plugins/tree/main/pstack

## 2. 가장 직접적인 자료: authoring-a-skill

pstack에는 Skill을 작성하거나 수정할 때 쓰는 별도 playbook이 있다.

핵심 패턴:

1. frontmatter의 `name`과 `description`을 확인한다.
2. referenced file의 존재 여부를 확인한다.
3. cross-skill link가 실제로 resolve되는지 확인한다.
4. structural change라면 test case를 둔다.
5. 불필요한 prose를 지운다.
6. 다른 Skill의 책임이면 경로로 위임하고 다시 설명하지 않는다.
7. 구조적 source가 있다면 text보다 그 source를 가리킨다.

특히 "Keep only prose that changes a decision"이라는 기준은 지침 파일 편집의 좋은 휴리스틱이다.

Source:
- https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md

## 3. description에 사용 조건과 제외 조건을 함께 둔다

`tdd/SKILL.md`의 description은 좁은 trigger를 사용한다.

대상:

- 사용자가 TDD/failing test/regression test를 명시적으로 요청
- 또는 bug에 cheap local test target이 있음

제외:

- test path가 불명확
- 비쌈
- integration-heavy
- 요청되지 않았고 강제할 이유가 없음

배울 점:

> Skill 설명은 "이 Skill이 관련 있는 모든 주제"를 쓰는 곳이 아니라 "이 Skill을 실제로 실행해야 하는 사건"을 쓰는 곳이다.

Source:
- https://github.com/cursor/plugins/blob/main/pstack/skills/tdd/SKILL.md

## 4. 비슷한 Skill은 책임 경계를 description에서 분리한다

`how`와 `why`는 비슷해 보이지만 책임을 분리한다.

- how: 현재 subsystem이 어떻게 동작하는지
- why: 왜 그런 형태가 되었는지, 역사와 동기

이런 분리는 Skill routing에 중요하다.

나쁜 Skill library:

- analyze-code
- understand-code
- inspect-code
- investigate-code

설명이 겹치면 라우팅이 불안정해진다.

더 나은 library는 각 Skill의 질문 유형과 산출물을 구분한다.

Source:
- https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md
- https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md

## 5. 작은 Skill과 큰 router Skill을 구분한다

pstack에는 한 원칙만 담는 매우 작은 Skill들이 있고, `poteto-mode/SKILL.md`처럼 여러 playbook으로 라우팅하는 큰 Skill도 있다.

이 대비에서 얻을 수 있는 교훈:

### 작은 leaf Skill

장점:

- 의미가 명확하다.
- 재사용하기 쉽다.
- 다른 workflow가 참조하기 쉽다.
- 수정 영향 범위가 작다.

### 큰 router Skill

장점:

- 진입점 하나로 workflow를 고를 수 있다.

위험:

- metadata와 본문이 비대해질 수 있다.
- 많은 trigger가 서로 영향을 준다.
- 특정 제품 기능과 강하게 결합된다.
- 모델 변경 시 과도한 routing rule이 부채가 될 수 있다.

책에서는 pstack의 구조를 그대로 복제하라고 하기보다 leaf와 router 사이의 trade-off 사례로 제시하는 것이 적합하다.

## 6. 원칙을 별도 Skill로 분리한 이유

pstack은 다음과 같은 원칙을 leaf Skill로 분리한다.

- 작은 변경 선호
- domain을 구조로 모델링
- boundary에서 validation
- 실제 artifact로 검증
- behavior를 test
- context window 보호
- 반복 지침을 구조로 승격

이 방식의 장점은 하나의 원칙을 여러 workflow가 참조할 수 있다는 점이다.

하지만 같은 원칙의 요약을 router에 복제하면 다시 중복 문제가 생긴다.

따라서 책에서 연구할 포인트:

- index에는 trigger/한 줄 요약
- canonical detail은 leaf 파일 하나
- 다른 Skill은 canonical path만 참조
- 같은 규칙을 여러 파일에 장문 복사하지 않음

## 7. "Encode Lessons in Structure"

pstack의 meta principle은 이 책과 직접 관련 있다.

반복 correction이 발생하면 다음을 먼저 검토한다.

- lint
- metadata
- runtime check
- script
- type/structure

판단이 필요한 경우에만 text instruction을 강화한다.

이 방식은 "CLAUDE.md가 계속 커지는 현상"에 대한 실전 해법이다.

Source:
- https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md

## 8. 전역 Rule은 작게 유지하는 사례

`setup-pstack`은 `~/.cursor/rules/pstack-models.mdc`에 역할별 model 선택 정보를 저장한다.

주목할 점은 이것이 거대한 전역 prompt가 아니라 작은 configuration-like rule이라는 점이다.

기본값과 다른 부분만 override하고, 기본값으로 돌아가려면 해당 line을 제거하는 형태다.

지침 파일 설계 관점에서는 다음 교훈을 준다.

- 글로벌 파일은 전체 workflow를 복제하는 곳이 아니다.
- 자주 바뀌는 환경별 선택값과 canonical workflow를 분리할 수 있다.
- default와 override의 관계를 명확히 해야 한다.

Source:
- https://github.com/cursor/plugins/blob/main/pstack/skills/setup-pstack/SKILL.md
- https://github.com/cursor/plugins/blob/main/pstack/docs/guide/01-setup.md

## 9. eval playbook에서 배울 점

pstack의 eval playbook은 Skill/Prompt 변경을 단순 자기평가로 확인하지 않는다.

주요 아이디어:

- candidate에게 "eval 중"이라는 사실을 노출하지 않는다.
- organic user request처럼 prompt를 만든다.
- candidate가 rubric을 보지 않게 한다.
- 비교 대상의 label/model identity를 judge에게 숨긴다.
- 모델의 자기 보고가 아니라 실제 transcript와 산출물을 확인한다.
- judge verdict와 사람이 직접 읽은 결과가 다르면 rubric/판정 편향을 의심한다.

이 방식은 지침 파일 변경의 "A/B 테스트" 장에 좋은 사례다.

Source:
- https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md

## 10. pstack에서 그대로 가져오지 말아야 할 것

pstack은 특정 제작자의 업무 방식과 Cursor 기능에 맞춘 opinionated system이다.

따라서 다음은 일반 표준처럼 쓰면 안 된다.

- 특정 model slug
- 특정 agent/subagent routing 방식
- 제품 전용 metadata
- pstack의 특정 autonomy 정책
- 특정 PR 운영 규칙
- 모든 프로젝트에 동일한 principle set이 필요하다는 가정

책의 목적은 pstack 복제가 아니라 "잘 작성된 지침 파일에서 추출할 수 있는 일반 작성 원리"를 찾는 것이다.

## 11. pstack에서 추출한 일반 원리

1. description을 좁게 쓴다.
2. 인접 Skill과 책임 경계를 명시한다.
3. 반복 내용을 복제하지 말고 canonical file을 참조한다.
4. leaf rule과 router를 구분한다.
5. 지침 변경도 test/eval한다.
6. structural constraint는 prose보다 강한 메커니즘으로 옮긴다.
7. default와 override를 분리한다.
8. 지침에는 실제 파일 경로와 검증 가능한 산출물을 사용한다.
9. subjective rule과 structural rule의 검증 방법을 구분한다.
10. 지침이 계속 커질 때 추가보다 삭제와 분리를 먼저 검토한다.

## 추가 분석 후보

다음 pstack 파일은 책 집필 단계에서 세부 사례로 더 분석할 가치가 있다.

- `skills/technical-writing/SKILL.md`
  - 지침 문장의 문체와 ambiguity 관리
- `skills/how/SKILL.md`
  - 단순/복잡 분기와 reference 분리
- `skills/tdd/SKILL.md`
  - positive/negative trigger
- `skills/reflect/SKILL.md`
  - 반복 학습을 지침/구조로 승격하는 과정
- `skills/principle-encode-lessons-in-structure/SKILL.md`
  - prose instruction debt 감소
- `skills/poteto-mode/playbooks/eval.md`
  - blinded prompt evaluation
- `skills/poteto-mode/playbooks/authoring-a-skill.md`
  - Skill 자체 작성 규칙
