# 12장. pstack의 Skill 파일을 뜯어보기

실제 지침 시스템을 공부할 때 가장 위험한 태도는 유명한 저장소를 정답으로 받아들이는 것이다.

pstack을 보는 목적도 복제하기 위해서가 아니다. 공개 저장소 안에 많은 Skill, Rule, principle, playbook이 함께 있고, Skill을 어떻게 작성해야 하는지에 대한 작성 규칙까지 존재하기 때문에 **지침 시스템이 성장하면서 어떤 구조가 나타나는지** 관찰하기 좋다.

## 12.1 좋은 사례를 볼 때의 질문

pstack을 분석할 때는 다음을 본다.

- 큰 지침을 어떻게 나누는가.
- description을 얼마나 좁히는가.
- 인접 Skill의 책임을 어떻게 구분하는가.
- 원칙과 workflow를 어떻게 분리하는가.
- 중복 내용을 어떻게 줄이는가.
- 지침 변경을 무엇으로 검증하는가.
- 반복 correction을 언제 구조로 승격하는가.

특정 model slug나 Cursor 전용 metadata는 일반 원칙으로 가져오지 않는다.

## 12.2 Authoring a Skill

pstack에는 Skill 작성 자체를 위한 playbook이 있다.

여기서 가장 중요한 생각은 “좋은 문장을 많이 쓰는 법”이 아니다.

- frontmatter를 검증한다.
- 참조 파일 존재 여부를 확인한다.
- cross-skill link를 확인한다.
- 구조 변경에는 test를 둔다.
- 불필요한 prose를 제거한다.
- 다른 Skill의 책임을 복제하지 않는다.
- 구조적 source가 있으면 text보다 그것을 참조한다.

특히 다음 기준은 이 책 전체와 잘 맞는다.

> 행동 결정을 바꾸는 prose만 남긴다.

이 기준을 적용하면 배경 설명과 철학이 자동으로 사라지는 것은 아니다. 실제 decision에 영향을 주는 배경은 남는다. 그러나 읽기 좋은 문장이라는 이유만으로 상시 instruction에 남지는 않는다.

## 12.3 TDD Skill의 경계

TDD는 넓게 잡기 쉬운 Skill이다.

“코드를 수정할 때 항상 TDD를 사용한다”고 쓰면 거의 모든 개발 요청을 잡게 된다.

pstack의 TDD 사례에서 배울 점은 positive뿐 아니라 skip condition을 둔다는 것이다.

- 사용자가 명시적으로 TDD나 regression test를 요청했다.
- bug에 값싼 local test seam이 있다.

반대로 다음 조건에서는 자동 강제를 피한다.

- test path가 불명확하다.
- 비용이 크다.
- integration-heavy하다.
- 사용자가 요청하지 않았고 강제할 이유도 없다.

핵심은 TDD가 좋은가 나쁜가가 아니다.

> Skill description은 철학의 적용 범위가 아니라 실제 호출 사건을 표현해야 한다.

## 12.4 How와 Why

코드를 이해하는 Skill은 쉽게 겹친다.

analyze-code, understand-code, inspect-code, investigate-code 같은 이름을 여러 개 만들면 description이 유사해지고 routing이 불안정해진다.

pstack의 how와 why 구분은 책임을 질문 유형으로 나눈 사례다.

- how: 현재 subsystem이 어떻게 동작하는가.
- why: 왜 지금 구조가 되었는가. 역사와 동기는 무엇인가.

이렇게 산출물과 질문 유형이 다르면 같은 코드베이스를 대상으로 해도 Skill 경계가 생긴다.

## 12.5 Leaf Skill과 Router

pstack에는 작은 원칙 Skill과 큰 router Skill이 함께 있다.

작은 leaf Skill은 한 원칙을 다른 workflow에서 재사용하기 쉽다.

큰 router는 하나의 진입점에서 여러 playbook을 선택할 수 있다.

문제는 router가 세부 절차까지 소유하기 시작할 때다.

좋은 router는 다음을 담당한다.

- 어떤 capability가 있는가.
- 어떤 조건에서 어느 capability로 가는가.
- 다음 Skill이나 playbook은 어디인가.

각 capability의 상세 절차는 leaf 쪽에 남긴다.

## 12.6 원칙을 별도 Skill로 둔 이유

pstack에는 작은 변경 선호, boundary validation, artifact 검증, behavior test, context 보호, 구조적 학습 같은 원칙이 분리되어 있다.

이 구조의 장점은 여러 workflow가 동일 원칙을 재사용할 수 있다는 것이다.

단, router와 각 Skill이 같은 설명을 계속 복제하면 효과가 사라진다.

따라서 원칙의 canonical owner는 하나여야 한다.

## 12.7 Encode Lessons in Structure

이 책과 가장 직접적으로 맞닿는 원칙이다.

반복 correction이 생겼을 때 먼저 검토한다.

- lint로 잡을 수 있는가.
- metadata로 표현할 수 있는가.
- runtime check가 가능한가.
- script로 고정할 수 있는가.
- type이나 구조로 잘못된 상태를 막을 수 있는가.

그래도 judgment가 필요할 때 자연어 instruction을 강화한다.

이 순서를 지키면 CLAUDE.md가 실패 사례의 묘지처럼 커지는 것을 막을 수 있다.

## 12.8 Eval playbook

pstack의 평가 방식에서 중요한 점은 자기평가를 믿지 않는다는 것이다.

- candidate에게 실험 목적을 노출하지 않는다.
- organic user request처럼 prompt를 만든다.
- candidate가 rubric을 보지 않게 한다.
- judge에게 어느 결과가 새 버전인지 숨긴다.
- 실제 transcript와 artifact를 본다.
- judge와 사람이 크게 다르면 rubric 편향을 의심한다.

이 방식은 지침 파일 A/B 평가에도 그대로 적용할 수 있다.

## 12.9 그대로 가져오면 안 되는 것

pstack은 특정 제작자의 workflow와 Cursor 환경에 맞춘 opinionated system이다.

따라서 다음은 일반 표준이 아니다.

- 특정 model 선택 규칙
- 특정 agent/subagent routing
- Cursor 전용 metadata
- 특정 autonomy 정책
- 특정 PR 운영 방식
- 모든 프로젝트에 같은 principle set이 필요하다는 가정

좋은 사례 분석은 복제가 아니라 원리 추출이다.

## 12.10 pstack에서 가져갈 열 가지 질문

1. description이 실제 사건을 trigger로 쓰는가.
2. 인접 Skill과 책임이 구분되는가.
3. canonical detail이 한 곳에만 있는가.
4. router가 상세 매뉴얼까지 소유하지 않는가.
5. leaf Skill의 책임이 좁은가.
6. 구조적 rule은 prose 밖으로 이동했는가.
7. default와 override가 구분되는가.
8. 실제 파일과 artifact를 근거로 삼는가.
9. 변경을 eval이나 test로 확인하는가.
10. 지침이 커질 때 추가보다 삭제와 분리를 먼저 검토하는가.

사례 연구의 목적은 이 질문들을 자신의 저장소에 가져오는 것이다.
