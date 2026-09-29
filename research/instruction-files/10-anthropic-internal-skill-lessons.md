# Anthropic 내부 Skill 운영에서 얻을 수 있는 작성 원칙

기준 자료:
Anthropic, "Lessons from building Claude Code: How we use skills", 2026-06-03.

이 자료는 Anthropic이 내부에서 수백 개의 Skill을 운영하면서 얻은 경험을 정리한 글이다. 이 책의 관점에서는 "어떤 Skill을 만들 것인가"보다 **SKILL.md를 어떻게 작성하고 유지할 것인가**에 집중해 읽는다.

## 1. Skill 하나는 가능하면 하나의 범주에 집중한다

Anthropic은 잘 작동하는 Skill이 대체로 하나의 명확한 범주에 들어맞는다고 설명한다. 여러 범주의 책임을 한 Skill에 동시에 넣으면 에이전트가 언제, 왜 이 Skill을 사용해야 하는지 판단하기 어려워질 수 있다.

작성 시 확인한다.

- 이 Skill의 핵심 작업을 한 문장으로 설명할 수 있는가.
- 서로 다른 두 개 이상의 업무를 `and`로 묶어 놓지 않았는가.
- 하나의 Skill 안에서 서로 다른 완료 조건을 가진 workflow가 경쟁하지 않는가.
- 분리된 Skill이 더 명확한 trigger를 가질 수 있지 않은가.

이 원칙은 "큰 Skill이 나쁘다"는 뜻이 아니다. 하나의 workflow를 완성하기 위해 여러 단계가 필요한 것은 자연스럽다. 문제는 **서로 다른 사용 이유를 하나의 Skill에 섞는 것**이다.

## 2. 모델이 이미 아는 내용을 다시 쓰지 않는다

Anthropic이 강조하는 실전 원칙 중 하나는 "Don't state the obvious"다.

Skill에 다음과 같은 일반론을 계속 적는 것은 context 비용만 증가시킬 수 있다.

- 코드를 신중하게 작성한다.
- 테스트를 잘한다.
- 좋은 이름을 쓴다.
- 에러를 처리한다.
- 사용자의 요구사항을 이해한다.

지침에 남길 가치가 있는 것은 보통 다음 중 하나다.

- 모델이 반복적으로 틀리는 프로젝트 특유의 사실
- 일반적인 관행과 다른 팀 규칙
- 중요한 예외
- 실제 실패에서 확인된 gotcha
- 자동으로 추론하기 어려운 완료 조건
- 특정 도구나 저장소의 비자명한 사용법

책에서는 다음 질문을 리뷰 기준으로 사용할 수 있다.

> 이 문장을 제거했을 때 실제 행동이 나빠지는가?

아니라면 삭제 후보다.

## 3. "Gotchas"는 매우 높은 신호를 가진다

Anthropic 내부 경험에서는 자주 발생하는 실패와 비자명한 함정을 모은 gotcha가 Skill에서 특히 가치가 높은 내용으로 나타났다.

좋은 gotcha의 출처:

- 실제 실패한 작업
- 사람이 반복해서 수정한 부분
- 잘못된 API 사용
- 자주 놓치는 repository convention
- 특정 도구의 예상 밖 동작
- 테스트가 통과해도 실제 제품에서 실패했던 사례

좋은 gotcha는 추상적인 경고가 아니다.

나쁜 예:

> 주의해서 migration을 작성한다.

더 나은 예:

> 기존 production migration 파일은 수정하지 않는다. schema 변경은 새 migration으로 추가한다.

### 유지보수 원칙

Gotcha는 처음부터 가능한 모든 실패를 상상해서 채우는 것이 아니다.

작게 시작하고 실제 실패에서 추가한다.

이는 CLAUDE.md에도 적용할 수 있다. "미래에 필요할 것 같은 규칙"보다 실제 반복 correction에서 출발하는 편이 낫다.

## 4. SKILL.md는 모든 지식을 담는 문서가 아니다

Anthropic은 filesystem 기반 progressive disclosure를 적극적으로 사용한다.

역할 분리:

- `SKILL.md`: 진입점, 핵심 workflow, 필요한 파일로의 라우팅
- `references/`: 상세 정책과 긴 배경
- `scripts/`: 반복 가능하고 결정론적인 작업
- 기타 resource: 필요할 때만 로드

장점:

- Skill의 핵심 지침을 빠르게 읽을 수 있다.
- 관련 없는 세부 사항이 context를 차지하지 않는다.
- 상세 문서를 별도로 유지할 수 있다.
- 필요할 때만 추가 context를 소비한다.

중요한 점은 파일을 많이 나누는 것 자체가 아니다. **언제 어떤 파일을 읽어야 하는지가 root Skill에서 명확해야 한다.**

## 5. 모델을 지나치게 레일 위에 올리지 않는다

Anthropic은 Skill이 너무 세세한 순서를 강제하면 모델의 문제 해결 능력을 제한할 수 있다고 설명한다.

다음은 구분해서 작성한다.

### 고정할 것

- 안전 경계
- 반드시 필요한 선행 조건
- 순서가 정확성에 필수적인 단계
- 산출물 형식
- 검증 조건
- 금지 행동

### 모델에게 맡길 것

- 파일 탐색의 세부 순서
- 상황에 따라 달라지는 조사 범위
- 중요하지 않은 구현 단계
- 모델이 이미 안정적으로 수행하는 일반 작업

핵심은 **목표와 제약을 명확하게 하되, 필요하지 않은 micro-management를 하지 않는 것**이다.

## 6. description은 사람에게 보여 주는 요약이 아니라 모델의 trigger다

Skill description은 README의 마케팅 문구와 다르다.

모델은 description을 보고 해당 Skill을 현재 요청에 적용할지 판단한다.

따라서 description은 다음을 우선한다.

1. 실제 업무 유형
2. 명확한 trigger
3. 인접 Skill과 구분되는 경계

좋지 않은 description:

> High-quality software development를 지원하는 powerful skill.

이 문장은 어떤 요청에서 사용해야 하는지 알려주지 않는다.

더 나은 방향:

> Use when adding or changing a database migration, or reviewing its rollout. Do not use for ordinary query or ORM model questions.

## 7. 반복 가능한 기계 작업은 script나 library로 만든다

Anthropic 내부 Skill은 반복적으로 재구성해야 하는 작업을 scripts와 libraries로 제공하는 방식을 활용한다.

이 방식의 장점:

- 모델이 매번 같은 boilerplate를 다시 만들 필요가 없다.
- 동작이 더 결정론적이다.
- 테스트 가능한 artifact가 된다.
- instruction token을 줄일 수 있다.
- 결과의 편차를 줄인다.

판단 기준:

> 같은 작업을 Skill 본문에서 여러 문장으로 매번 설명한다면 실행 가능한 helper로 바꿀 수 있는지 확인한다.

## 8. 항상 필요한 Hook과 Skill 전용 Hook을 구분한다

모든 guardrail이 전역 Hook이어야 하는 것은 아니다.

Anthropic 내부 사례에서는 특정 Skill을 사용하는 동안에만 필요한 보호 동작을 on-demand Hook으로 적용하는 패턴도 사용한다.

의미:

- 전역 Hook: 거의 모든 작업에서 반드시 필요한 정책
- Skill-scoped/on-demand Hook: 특정 위험 작업이나 workflow에서만 필요한 정책

이 구분은 Hook의 false positive와 실행 비용을 줄이는 데 중요하다.

## 9. Skill 사용량과 trigger 실패를 관찰한다

좋은 Skill을 작성했다고 가정하지 않는다.

운영에서 확인할 항목:

- 예상한 요청에서 Skill이 실제로 호출되는가.
- 사용자가 반복해서 Skill 이름을 직접 말해야 하는가.
- 관련 없는 요청에서 과잉 호출되는가.
- Skill을 읽었는데도 반복적으로 같은 단계가 누락되는가.
- 특정 reference는 전혀 읽히지 않는가.
- 특정 instruction은 결과에 아무 영향이 없는가.

Skill 사용량이 낮다면 두 가지 가능성이 있다.

1. 실제로 필요 없는 Skill이다.
2. description/routing이 잘못됐다.

둘을 구분하려면 eval과 실제 trace가 필요하다.

## 10. Skill은 작게 시작하고 실제 실패에서 성장시킨다

Anthropic의 내부 경험은 Skill을 처음부터 거대한 완성 문서로 만들기보다 작은 useful core로 시작하고 실제 사용에서 얻은 gotcha를 추가하는 방향을 지지한다.

권장 lifecycle:

1. 하나의 분명한 업무로 시작한다.
2. 최소 workflow와 완료 조건을 작성한다.
3. 실제 작업에서 사용한다.
4. 실패나 반복 correction을 기록한다.
5. 필요한 gotcha만 추가한다.
6. 기계화 가능한 correction은 script/lint/hook으로 옮긴다.
7. description의 trigger precision을 다시 평가한다.
8. 불필요해진 지침은 삭제한다.

## 11. 책에 반영할 수 있는 작성 규칙

Anthropic 내부 경험에서 추출할 수 있는 지침 파일 작성 규칙은 다음과 같다.

- 한 Skill에 하나의 분명한 사용 이유를 둔다.
- 모델이 이미 아는 일반론은 쓰지 않는다.
- 실제 실패에서 나온 gotcha를 우선한다.
- root Skill은 상세 문서 전체가 아니라 필요한 정보로 가는 hub가 된다.
- 목표와 제약을 쓰고 필요 없는 세부 행동 순서를 강제하지 않는다.
- description은 사람용 소개가 아니라 모델의 routing contract로 작성한다.
- 반복 가능한 기계 작업은 script/library로 옮긴다.
- Hook의 적용 범위를 최소화한다.
- 실제 Skill usage와 trigger failure를 관찰한다.
- 작게 시작하고 실제 correction으로 성장시킨다.
- 추가만 하지 말고 삭제도 유지보수 작업으로 취급한다.

## 12. pstack과 비교했을 때의 공통점

Anthropic 내부 운영 경험과 pstack의 공개 작성 규칙에는 흥미로운 공통점이 있다.

- prose를 불필요하게 늘리지 않는다.
- Skill의 책임을 좁힌다.
- 반복된 실패를 지침 개선 신호로 본다.
- 자세한 자료는 필요할 때만 읽게 한다.
- 기계적 반복은 script 또는 구조로 이동한다.
- 지침을 실제 사용과 eval로 검증한다.

서로 독립적인 공식/실전 사례에서 같은 방향이 반복된다는 점은 책의 핵심 원칙을 뒷받침하는 근거로 사용할 수 있다.

## 주요 출처

- Anthropic, Lessons from building Claude Code: How we use skills
  - https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills
- Anthropic, Skill authoring best practices
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Anthropic, Effective context engineering for AI agents
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Cursor pstack, authoring-a-skill
  - https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md
- Cursor pstack, Encode Lessons in Structure
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md
