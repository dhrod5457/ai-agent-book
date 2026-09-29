# SKILL.md 작성법 리서치

## 1. SKILL.md의 가장 중요한 두 부분

Skill은 크게 두 단계로 읽힌다.

1. discovery 단계에서 `name`과 `description`이 노출된다.
2. 모델이 관련 Skill이라고 판단한 뒤에야 본문이 로드된다.

따라서 Skill 품질을 두 문제로 분리해야 한다.

- **routing quality**: 올바른 요청에서 선택되는가.
- **execution quality**: 선택된 뒤 올바르게 수행하는가.

본문이 아무리 훌륭해도 description이 나쁘면 Skill은 사용되지 않거나 잘못 사용된다.

## 2. portable core와 제품 확장을 분리한다

Agent Skills 공개 명세의 최소 구조는 다음과 같다.

- Skill directory
- `SKILL.md`
- YAML frontmatter
  - `name`
  - `description`
- Markdown body
- 선택적으로 `scripts/`, `references/`, `assets/`

제품은 추가 frontmatter를 제공할 수 있다.

예를 들어 Claude Code는 호출 방식, 허용 도구 등 제품별 필드를 지원할 수 있고 Cursor의 실제 Skill에는 Cursor 전용 metadata가 나타난다.

책에서는 반드시 다음을 구분해야 한다.

- 표준에 속하는 필드
- Claude Code 확장
- Cursor 확장
- Gemini/Codex의 구현 차이

그렇지 않으면 한 제품에서 동작하는 예제를 "SKILL.md 표준"으로 잘못 설명하게 된다.

## 3. name 작성 원칙

Agent Skills/Anthropic 명세 기준 핵심:

- 짧고 명확한 기능 이름
- 소문자, 숫자, 하이픈 중심의 portable naming
- 같은 저장소의 다른 Skill과 의미가 겹치지 않게 작성
- 구현 조직이 아니라 사용자가 기대하는 기능 중심

나쁜 후보:

- `helper`
- `common`
- `developer`
- `backend`

좋은 후보:

- `review-db-migration`
- `triage-ci-failure`
- `write-release-notes`

## 4. description은 "무엇 + 언제"를 쓴다

Anthropic 공식 best practices는 description에 다음 두 항목을 모두 넣도록 권장한다.

1. Skill이 무엇을 하는가.
2. 언제 사용해야 하는가.

OpenAI의 2026년 GPT-6 Astra 가이드도 description을 가능한 짧게 유지하면서 적용 시점을 명확히 하라고 권고한다.

### 흔한 실패: 도메인을 trigger로 쓴다

나쁜 형태:

> DB 작업에 사용한다.

이 표현은 query, model, persistence, migration 등 너무 많은 인접 요청을 끌어들인다.

더 나은 형태:

> migration을 추가하거나 변경할 때, 또는 rollout을 검토할 때 사용한다.

핵심은 "관련 분야"가 아니라 **실제 작업 유형**을 trigger로 쓰는 것이다.

## 5. negative boundary를 설계한다

공식 명세에서 반드시 필요한 필드는 아니지만 실전에서는 매우 유용하다.

예:

- Use when: 기존 migration을 추가/수정하거나 rollout을 리뷰한다.
- Skip when: 단순 query 작성, ORM model 탐색, 일반 DB 질문이다.

pstack의 `tdd/SKILL.md`는 이 패턴을 잘 보여준다. TDD를 사용할 조건뿐 아니라 테스트 경로가 비싸거나 불명확한 경우에는 강제하지 않는다고 경계를 둔다.

## 6. description끼리 경쟁한다는 사실을 고려한다

설치된 모든 Skill의 metadata가 라우팅 후보가 된다.

따라서 다음 문제가 생긴다.

- 서로 너무 비슷한 description
- 모든 Skill이 "non-trivial task" 같은 넓은 표현 사용
- "always", "whenever" 같은 과잉 trigger
- 같은 키워드를 여러 Skill이 독점하려고 함

OpenAI는 Skill 수가 많아지면 description이 context budget 때문에 축약될 수 있고, 서로 모순되거나 과도한 trigger가 선택 품질을 떨어뜨릴 수 있다고 지적한다.

### 권장 검사

Skill을 추가할 때 해당 Skill만 보지 말고 인접 Skill의 description도 함께 비교한다.

질문:

- 이 요청은 A와 B 중 어느 Skill이어야 하는가.
- 그 차이를 description만 보고 구분할 수 있는가.
- 둘 다 호출되는 것이 맞는가.
- 어떤 요청에서는 둘 다 호출되면 안 되는가.

## 7. 본문은 설명서보다 실행 계약에 가깝게 쓴다

좋은 본문의 기본 구성 후보:

1. 목적
2. 적용/제외 조건
3. 필요한 입력 또는 사전 확인
4. 핵심 workflow
5. guardrails
6. verification / definition of done
7. output contract
8. 필요할 때 읽을 references/scripts

모든 Skill에 이 섹션을 기계적으로 강제할 필요는 없다. 필요한 섹션만 쓴다.

## 8. 한 단계씩 실행 가능한 workflow를 쓴다

나쁜 예:

1. 분석한다.
2. 잘 구현한다.
3. 충분히 테스트한다.

좋은 workflow는 단계마다 관찰 가능한 상태가 생긴다.

예:

1. 변경 대상과 기존 behavior를 확인한다.
2. 재현 가능한 가장 좁은 검증 경로를 선택한다.
3. 수정 전 현재 실패를 확인한다.
4. 최소 변경을 한다.
5. 같은 검증을 다시 실행한다.
6. 인접 회귀 검사를 실행한다.
7. 사용한 증거를 결과에 남긴다.

## 9. "모든 경우"를 레시피로 고정하지 않는다

2026년 OpenAI 가이드는 최신 모델이 더 강해지면서 지나치게 상세한 itinerary/recipe가 오히려 성능을 제한할 수 있다고 지적한다.

따라서 다음을 구분한다.

### 고정해야 하는 것

- 안전 경계
- 반드시 남겨야 하는 산출물
- 순서가 결과 정확도에 필수적인 단계
- 검증 조건
- 금지 행동

### 모델 판단에 맡길 수 있는 것

- 검색 파일의 정확한 순서
- 사소한 구현 세부
- 상황마다 달라지는 탐색 횟수
- 이미 모델이 안정적으로 수행하는 일반적 코딩 행동

## 10. progressive disclosure

Anthropic 가이드는 `SKILL.md`를 상세 자료 전체가 아니라 목차 겸 실행 진입점처럼 구성하도록 권장한다.

권장 구조:

```text
my-skill/
├── SKILL.md
├── references/
│   ├── api.md
│   ├── rollout.md
│   └── examples.md
├── scripts/
│   └── verify.sh
└── assets/
    └── template.md
```

원칙:

- 본문은 500줄 미만을 목표로 한다.
- 상세 자료는 별도 파일로 분리한다.
- 필요한 reference만 읽도록 조건을 적는다.
- reference에서 또 다른 reference를 연쇄적으로 찾게 만들지 않는다.
- 긴 reference는 자체 목차를 둔다.

## 11. scripts는 "설명을 대신하는 실행 가능한 지식"이다

같은 기계적 작업을 매번 자연어로 설명해야 한다면 script 후보이다.

예:

- 특정 결과를 검증하는 checker
- formatter
- 반복 변환
- API payload 생성
- repository structure 검사
- Skill 자체 validation

script를 쓸 때도 다음을 명시한다.

- 언제 실행하는가.
- 입력은 무엇인가.
- 성공/실패 exit code가 무엇인가.
- 출력이 어떤 의미인가.
- destructive behavior가 있는가.

## 12. references는 백과사전이 아니라 필요할 때 읽는 근거다

reference로 옮기기 좋은 내용:

- 긴 API 규약
- 예외 사례 목록
- 복잡한 schema
- style guide
- rollout 정책
- 실제 예시

본문에서 reference를 가리킬 때는 "참고하라"보다 **언제 읽는지**를 쓴다.

예:

- schema 변경이면 `references/schema-migrations.md`를 읽는다.
- 외부 공개 API 변경이면 `references/api-compatibility.md`를 읽는다.

## 13. Skill을 작성하면서 동시에 eval 사례를 만든다

OpenAI의 Skill eval 가이드는 작성 전에 성공 조건을 정의하고 다음을 분리해 평가하는 방식을 제안한다.

- Outcome: 결과가 완료됐는가.
- Process: 원하는 Skill/도구/절차를 사용했는가.
- Style: 원하는 형태인가.
- Efficiency: 불필요한 작업이나 토큰 낭비가 없는가.

최소 prompt set에는 다음이 필요하다.

- explicit positive
- implicit positive
- noisy/contextual positive
- adjacent negative
- ambiguous boundary case

특히 `should_trigger=false` 사례가 없으면 과잉 호출 회귀를 잡기 어렵다.

## 14. pstack에서 배울 작성 패턴

### authoring-a-skill playbook

현재 pstack은 Skill 작성 시 다음을 강조한다.

- frontmatter의 name/description 검증
- 참조 파일 존재 여부 확인
- cross-skill link 검증
- 구조적 변화라면 test
- 불필요한 prose 삭제
- 다른 Skill을 경로로 위임하고 내용을 복제하지 않음

### tdd Skill

- 좁은 positive trigger
- 명확한 skip condition
- 실패 전/성공 후 증거
- 새 test가 오히려 나쁜 경우 대체 검증 허용

### how Skill

- `how`와 `why`의 책임을 description에서 구분
- 단순/복잡 질문을 먼저 분류
- 의심될 때 더 단순한 경로 선택
- 상세 prompt는 references에 분리

## 15. SKILL.md 리뷰 체크리스트

### Routing

- [ ] name이 기능을 구분할 수 있는가.
- [ ] description에 what과 when이 있는가.
- [ ] trigger가 도메인 전체로 퍼지지 않는가.
- [ ] 인접 Skill과 구별되는가.
- [ ] negative example이 준비되어 있는가.

### Body

- [ ] 첫 화면만 읽어도 목적과 workflow가 보이는가.
- [ ] 단계가 관찰 가능한 행동인가.
- [ ] 판단이 필요한 지점과 고정 규칙이 구분되는가.
- [ ] 같은 설명이 다른 파일과 중복되지 않는가.
- [ ] 지나친 이유 설명과 철학이 없는가.
- [ ] 완료 조건과 evidence가 있는가.

### Resources

- [ ] 긴 내용은 reference로 빠졌는가.
- [ ] reference link가 실제 존재하는가.
- [ ] reference depth가 얕은가.
- [ ] 반복/결정론 작업은 script 후보를 검토했는가.

### Evaluation

- [ ] positive trigger를 시험했는가.
- [ ] negative trigger를 시험했는가.
- [ ] fresh session에서 시험했는가.
- [ ] Skill 없는 baseline과 비교했는가.
- [ ] 실제 산출물과 trace를 확인했는가.
- [ ] 모델이 바뀌어도 재평가할 수 있는가.

## 주요 출처

- Agent Skills Specification
  - https://agentskills.io/specification
- Anthropic, Skill authoring best practices
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Anthropic, Agent Skills overview
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- OpenAI, Rethinking skills and prompts for GPT-6 Astra
  - https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- OpenAI, Testing Agent Skills Systematically with Evals
  - https://developers.openai.com/blog/eval-skills
- Cursor pstack, authoring-a-skill
  - https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md
- Cursor pstack, tdd
  - https://github.com/cursor/plugins/blob/main/pstack/skills/tdd/SKILL.md
- Cursor pstack, how
  - https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md
