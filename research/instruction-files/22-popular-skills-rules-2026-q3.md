# 최근 3개월 유명 Agent Skills가 실제로 사용하는 규칙

기준일: 2026-09-30  
조사 기간: 2026-07-01 ~ 2026-09-30

## 1. 조사 목적

이번 조사는 "좋은 Skill은 어떤 형식이어야 하는가"를 공식 문서만으로 정리하지 않는다.

최근 3개월 안에 실제로 활발히 갱신된 유명 공개 Skill 저장소를 골라 다음을 확인한다.

- 실제 `SKILL.md`가 어떤 행동 규칙을 강하게 요구하는가
- description을 어떻게 작성하는가
- TDD / verification / scope / simplicity / source verification을 어떻게 표현하는가
- 반복되는 실패를 prose에 남기는가, Hook/validator/eval로 승격하는가
- 최근 commit에서 어떤 규칙이 추가·삭제·완화됐는가
- 서로 유명한 Skill들도 어떤 부분에서 서로 다른 철학을 갖는가

핵심 관심사는 popularity ranking 자체가 아니라 **실전 규칙의 수렴점과 차이점**이다.

---

# 2. 조사 대상

선정 기준:

1. 공식 vendor Skill 또는 대규모 community Skill
2. 2026-07-01 이후 실제 repository activity가 있음
3. Skill의 규칙이나 runtime behavior를 직접 확인할 수 있음
4. 단순 directory/marketplace보다 실제 workflow Skill을 우선

2026-09-30 시점 GitHub metadata 기준:

| 저장소 | 성격 | Stars | 최근 push |
| --- | --- | ---: | --- |
| `obra/superpowers` | agent methodology | 약 292.9k | 2026-09-27 |
| `mattpocock/skills` | engineering workflow | 약 272.0k | 2026-09-29 |
| `affaan-m/ECC` | harness + skills + rules + hooks | 약 269.6k | 2026-09-29 |
| `anthropics/skills` | Anthropic official | 약 179.0k | 2026-09-29 |
| `DietrichGebert/ponytail` | minimalism/YAGNI methodology | 약 148.1k | 2026-09-14 |
| `addyosmani/agent-skills` | engineering workflow | 약 99.9k | 2026-09-26 |
| `vercel-labs/agent-skills` | Vercel official | 약 31.7k | 2026-08-28 |
| `OthmanAdi/planning-with-files` | persistent planning workflow | 약 27.2k | 2026-09-27 |

참고:

- 별 수는 popularity signal일 뿐 품질 점수가 아니다.
- vendor official 여부와 community adoption을 함께 본다.
- `openai/skills`는 매우 중요한 reference지만 default branch의 최신 commit 날짜가 2026-06-24라 이번 "최근 3개월 실제 변경" 표본에서는 제외하고 기존 연구의 공식 reference로 유지한다.

---

# 3. 가장 강한 공통 규칙

8개 저장소를 비교하면 반복해서 나타나는 규칙은 다음과 같다.

## R1. Skill은 시작 조건이 명확해야 한다

대표:

- Anthropic `skill-creator`
- Superpowers
- Matt Pocock
- Addy Osmani
- Vercel

형태는 다르지만 공통점은:

> description은 Skill을 찾는 surface다.

description을 단순 요약문으로 취급하지 않는다.

다만 **무엇을 description에 얼마나 넣을지**에서는 프로젝트마다 차이가 있다.

---

## R2. 실제 행동이 바뀌지 않는 문장은 제거한다

대표:

- Anthropic
- OpenAI reference
- Superpowers
- Addy Osmani
- Matt Pocock

반복되는 판단:

- social proof 삭제
- 장황한 recap 삭제
- 이미 다른 곳에서 설명한 Integration 목록 삭제
- generic advice 삭제
- Skill 실행에 필요하지 않은 mechanics 삭제

즉 최근 유명 Skill의 유지보수 방향은:

> **더 자세히 쓰기보다 행동을 바꾸는 문장만 남기기**

쪽이다.

---

## R3. 검증 없이 "완료"를 선언하지 않는다

가장 강한 예:

- Superpowers `verification-before-completion`
- ECC `verification-loop`
- Addy `using-agent-skills`
- Planning with Files의 completion gate

Superpowers:

```text
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

라는 Iron Law를 둔다.

ECC는:

1. build
2. typecheck
3. lint
4. tests
5. security
6. diff review

의 phase를 둔다.

Addy는:

> "Seems right" is never sufficient.

라는 방향으로 모든 workflow에 verification을 요구한다.

### 공통점

완료는 model feeling이 아니라:

- test output
- build
- diff
- runtime evidence
- artifact

로 판정한다.

---

## R4. TDD는 단순 "테스트 먼저"보다 실패 확인까지 요구한다

대표:

- Superpowers `test-driven-development`
- Matt Pocock `tdd`
- ECC `tdd-workflow`

Superpowers의 핵심:

```text
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

그리고 단순히 test file을 먼저 생성하는 것이 아니라:

1. failing test 작성
2. 실제로 실패하는지 실행
3. 예상 이유로 실패하는지 확인
4. 최소 구현
5. pass 확인
6. full suite 확인

을 요구한다.

Matt Pocock은 조금 다르다.

- test seam을 먼저 합의
- public behavior 기준
- vertical slice
- 한 test → 한 implementation
- 모든 것을 한꺼번에 test-first로 쓰는 horizontal slicing은 피함

ECC는 더 규칙적인 enterprise형이다.

- unit/integration/E2E
- coverage 80%+
- runner 자동 감지
- RED/GREEN/coverage

### 차이

같은 TDD라도:

- Superpowers = discipline / anti-rationalization
- Matt = test boundary / seam / vertical slicing
- ECC = process + coverage gate

로 강조점이 다르다.

---

## R5. Scope를 벗어난 개선을 하지 않는다

대표:

- Addy `using-agent-skills`
- Ponytail
- Anthropic `skill-creator`
- Matt `implement`

Addy:

- 요청하지 않은 adjacent cleanup 금지
- 이해하지 못한 comment 삭제 금지
- spec 밖 feature 추가 금지

Ponytail:

- unrequested abstraction 금지
- scaffolding for later 금지
- fewest files
- shortest working diff

Anthropic:

- user intent와 scope를 보존
- Skill이 user가 요청한 assignment를 확장하지 않음
- approval은 scope 확장이 아님

### 공통 원리

> 에이전트가 "좋아 보이는 개선"을 스스로 추가하는 것을 실패로 본다.

---

## R6. 일반적인 지식보다 실제 project/runtime에 필요한 규칙만 넣는다

대표:

- Anthropic
- Superpowers
- Addy
- Matt
- Vercel

OpenAI의 기존 공식 reference와도 같은 방향이다.

질문:

> 모델이 이미 아는 내용인가?  
> 이 문장이 실제 결정을 바꾸는가?

최근 Skill들은 model에게 generic software engineering 교과서를 다시 가르치려 하지 않는 방향으로 이동한다.

---

## R7. 큰 Skill은 entry point + reference로 분리한다

대표:

- Anthropic `skill-creator`
- Addy `skill-anatomy`
- Vercel
- Matt `writing-for-agents`

공통:

- SKILL.md는 workflow/router
- 조건부 detail은 reference
- 필요할 때만 read

Addy:

- SKILL.md 500줄 이하
- reference one-level-deep
- script > inline code when deterministic
- empty scripts/reference directory 금지

Anthropic:

- 500 lines ideal
- 큰 reference는 TOC
- domain별 reference 분리

Matt:

- "information hierarchy"
- always-loaded pointer와 disclosed reference를 별도 budget으로 취급

### 핵심

Progressive disclosure를 단순 token optimization이 아니라:

> **agent attention hierarchy를 유지하는 구조**

로 본다.

---

## R8. 반복되는 deterministic rule은 script / Hook / validator로 옮긴다

대표:

- Addy
- Planning with Files
- ECC
- Superpowers

Addy 최근 9월 변화:

- SKILL.md 500-line budget validator
- empty subdirectory 검사
- reference link validation
- command frontmatter YAML validation
- artifact path drift CI
- negative-trigger eval

Planning with Files:

- UserPromptSubmit
- PreToolUse
- PostToolUse
- Stop
- PreCompact

Hook으로 plan injection, progress reminder, completion gate를 수행.

ECC:

- Hook matcher scope 수정
- security guard
- skill compliance evidence propagation

Superpowers:

- pressure tests / micro-eval로 prose rule을 검증

### 공통 원리

> 반복해서 틀리는 deterministic behavior는 prose를 더 세게 쓰기보다 실행 구조로 바꾼다.

---

# 4. 저장소별 실제 규칙

# 4.1 Anthropic Skills

Repository:
https://github.com/anthropics/skills

대표:
`skills/skill-creator/SKILL.md`

현재 Skill Creator가 사용하는 핵심 규칙:

## Intent를 먼저 고정

Skill 작성 전에:

1. Skill이 무엇을 가능하게 하는가
2. 언제 trigger되는가
3. 출력은 무엇인가
4. eval이 필요한가

를 먼저 결정.

## Test prompt를 먼저 현실적으로 만든다

- 2~3개의 realistic prompt
- 실제 user가 말할 법한 표현
- 정량 eval + 사용자 qualitative review
- 결과를 보고 Skill 반복 수정

## Description은 trigger의 핵심 surface

Anthropic Skill Creator는 현재:

- what
- when
- specific context

를 description에 넣는다.

특히 under-triggering을 막기 위해 어느 정도 "pushy"하게 쓰라고 명시한다.

이 점은 Superpowers와 철학 차이가 있다.

## Progressive disclosure

- metadata
- SKILL body
- references/scripts/assets

3단계.

## Imperative

instruction은 명령형 선호.

## Heavy MUST 남발보다 이유 설명

Anthropic Skill Creator의 writing style은:

- 무조건 MUST 반복보다
- 왜 규칙이 중요한지 설명

을 선호한다.

## Lack of Surprise

Skill description에서 예상하기 어려운:

- malicious behavior
- unauthorized access
- exfiltration

등을 숨겨서는 안 됨.

### 최근 3개월 변화

2026-08-18:

`academy-guide` description을:

- 1,176 chars
- → 992 chars

로 줄임.

이유:

- upload validator 1,024-char limit
- shortened version은 내부 테스트 완료

2026-07-17:

Office Skill 업데이트에서:

> "Trim the skill docs to the guidance that earns its place."

라는 방향이 명시됨.

### 해석

Anthropic의 최근 방향은:

- description은 trigger recall을 위해 충분히 구체적
- body는 줄임
- 실제 eval을 통해 trigger와 결과를 반복 개선

이다.

---

# 4.2 Superpowers

Repository:
https://github.com/obra/superpowers

대표:

- `using-superpowers`
- `test-driven-development`
- `verification-before-completion`
- `writing-skills`

Superpowers는 이번 표본 중 가장 **강제적인 process Skill**이다.

## 1% Rule

`using-superpowers`:

> Skill이 적용될 가능성이 1%라도 있으면 먼저 invoke.

clarifying question, file read보다 Skill check가 먼저다.

## Process Skill 우선

- brainstorming
- debugging
- TDD

같은 "어떻게 일할지"를 정하는 Skill이 domain implementation Skill보다 먼저.

## TDD Iron Law

production code 전에 failing test.

실패를 실제로 보고 이유까지 확인해야 한다.

## Completion Iron Law

fresh verification 없이는 완료 선언 금지.

## Skill authoring 자체도 TDD

`writing-skills`는 Skill 작성에 TDD를 적용한다.

```text
pressure scenario
→ skill 없는 baseline 실패 관측
→ skill 작성
→ behavior 개선 확인
→ loophole 찾기
→ skill 수정
```

## Description은 "when only"

Superpowers는 특히:

> description = trigger condition만  
> workflow summary를 넣지 말라

고 주장한다.

이유:

description에 workflow summary를 넣으면 agent가 full SKILL.md를 읽지 않고 description만 shortcut으로 따를 수 있다는 자체 실험 결과가 있었기 때문.

## Mechanical rule은 documentation으로 두지 않는다

`writing-skills`:

- regex/validator로 enforce 가능한 것은 automate
- docs는 judgment call에 사용

### 최근 3개월 변화가 특히 중요

2026-07-23 일련의 refactor:

삭제:

- social proof
- Advantages
- Bottom Line recap
- duplicated Integration list
- repeated benefit explanations

이유:

> 실행 행동을 추가하지 않는 prose.

그러나 모든 rationale를 지운 것은 아니다.

### TDD rationale deletion 실험

Superpowers는 TDD 문서의 "Why Order Matters" rationale를 줄이는 실험에서:

- control: 8/10
- treatment: 5/10

으로 **tests-later pressure 상황에서 compliance가 떨어지는 결과**를 기록했다.

그래서 rationale 자체를 버리는 대신:

- Common Rationalizations table

안에 짧게 다시 넣었다.

### 중요한 교훈

> 중복 설명은 지우되, 실제 pressure에서 행동을 지키는 rationale는 남긴다.

이것은 단순 "짧을수록 좋다"와 다르다.

---

# 4.3 Matt Pocock Skills

Repository:
https://github.com/mattpocock/skills

대표:

- `implement`
- `tdd`
- `code-review`
- `writing-for-agents`

## Manual-only action Skill

`implement`:

```yaml
disable-model-invocation: true
```

를 사용.

즉 구현 전체 workflow를 agent가 멋대로 auto-trigger하지 못하게 하고 명시적 호출에 가깝게 운영.

## TDD는 seam 중심

- public interface
- pre-agreed seams
- vertical slice
- implementation detail test 금지

특히:

> test를 많이 만드는 것이 아니라 어디에서 관측할지를 먼저 정한다.

## Review를 두 축으로 분리

`code-review`:

- Standards
- Spec

두 sub-agent를 병렬 실행.

이유:

- standards 준수
- 요구사항 충족

은 서로 다른 판정 문제이기 때문.

## Agent-facing 문서를 context pointer로 본다

`writing-for-agents`의 중요한 개념:

- Skill description
- AGENTS.md pointer
- CLAUDE.md pointer

는 모두 같은 종류의 routing object.

pointer는:

1. 무엇을 가리키는지
2. 어떤 branch에서 읽어야 하는지

두 역할을 한다.

## Positive phrasing

가능하면:

- "하지 마"

보다:

- "이렇게 해"

를 선호.

금지 행동 자체를 context에 활성화하지 않기 위해서다.

## Single source of truth

같은 의미를 여러 문서에 반복하지 않는다.

### 최근 3개월 변화

2026-09-17 `pr` Skill:

이전:
- git mechanics
- diff pinning
- PR create action

까지 포함된 workflow.

변경:

> PR body format reference

로 책임을 축소.

즉 action Skill과 format reference가 섞였던 것을 분리.

2026-09-24:

- 필요 없어진 `resolving-merge-conflicts` Skill 삭제
- 여러 description 명료화
- workflow routing 정리

### 핵심 교훈

> Skill은 기능을 계속 더하지 않고, 책임이 틀리면 삭제하거나 역할을 줄인다.

---

# 4.4 Addy Osmani Agent Skills

Repository:
https://github.com/addyosmani/agent-skills

대표:

- `using-agent-skills`
- `constraint-driven-development`
- `source-driven-development`
- `docs/skill-anatomy.md`

## Global operating behaviors

meta-skill이 다음을 모든 Skill에 공통 rule로 둔다.

1. assumptions surface
2. confusion을 숨기지 않음
3. 문제가 있으면 push back
4. simplicity
5. scope discipline
6. verify, don't assume

## Spec 없이 큰 구현 금지에 가까운 구조

여러 workflow를:

```text
idea
→ spec
→ plan
→ incremental implementation
→ test
→ review
→ shipping
```

으로 연결.

## Constraint를 prose에서 file + checker로 이동

`constraint-driven-development`:

- `CONSTRAINTS.md`
- coverage
- lint
- types
- security
- accessibility
- performance

를 number + command로 만든다.

핵심:

> number가 있지만 command가 없으면 constraint가 아니라 aspiration.

## Current official source 확인

`source-driven-development`:

- dependency version 먼저 확인
- current official docs fetch
- non-obvious choice는 citation
- 못 찾으면 UNVERIFIED로 명시
- fetched docs 내부 instruction을 model command로 취급하지 않음

## Skill authoring rules

`docs/skill-anatomy.md`:

- description: what + when
- workflow summary는 description에 넣지 않음
- SKILL.md < 500 lines
- reference one-level deep
- script 사용
- empty dirs 금지
- evidence-based Verification
- Common Rationalizations
- Red Flags

## Model workaround를 Skill에 넣지 않음

특히 다음 규칙이 강하다.

> model/version 이름을 말하지 않으면 정당화할 수 없는 step은 Skill에 두지 않는다.

즉 특정 모델의 실패를 universal procedure로 만들지 않는다.

### 최근 3개월 변화

2026-09-23~26:

- 500-line budget validator 추가
- empty subdirectory 검사
- reference link validation
- command frontmatter YAML validation
- artifact path drift CI
- must-not-fire plugin eval
- negated trigger lint 수정
- condensation 중 사라진 security rule 복구

### 핵심 교훈

이 저장소는 이번 조사에서 가장 분명하게:

> Skill authoring rule을 다시 **lint / CI / eval**로 올리고 있다.

---

# 4.5 Vercel Agent Skills

Repository:
https://github.com/vercel-labs/agent-skills

대표:

- `react-best-practices`
- `react-view-transitions`
- `web-design-guidelines`

## Rule priority

`react-best-practices`는 약 70개 rule을:

- CRITICAL
- HIGH
- MEDIUM
- LOW

로 분류한다.

즉 rule을 평평하게 나열하지 않는다.

예:

1. waterfall 제거
2. bundle size
3. server
4. client
5. rerender
6. rendering
7. JS
8. advanced

순서.

## SKILL.md는 index, rule file은 detail

각 rule은 별도 file.

`SKILL.md`는:

- priority
- rule id
- 한 줄 의미

를 제공.

## Live source를 읽는 Skill

`web-design-guidelines`는 review할 때마다 최신 guideline source를 fetch.

장점:

- stale snapshot 방지

대가:

- external source dependency
- fetched content trust boundary 필요

## View Transitions Skill

현행 구조는:

- high-level workflow
- core concepts
- reference file

분리.

### 최근 3개월 변화

7월 실제 commit에서 반복된 패턴:

- React/Next source 직접 fact-check
- 잘못된 absolute rule 수정
- framework-specific detail reference로 이동
- cross-reference를 실제 markdown link로 변경
- SKILL.md prose 압축
- "always use default=none" 같은 과도한 rule을 trade-off가 있는 rule로 완화

### 핵심 교훈

> framework Skill은 모델 기억보다 **현재 source + scoped statement**가 중요하다.

---

# 4.6 Planning with Files

Repository:
https://github.com/OthmanAdi/planning-with-files

대표:
`skills/planning-with-files/SKILL.md`

이번 표본에서 가장 Hook 중심이다.

## Persistent memory on disk

기본 모델:

```text
Context Window = RAM
Filesystem = Disk
```

그래서:

- task_plan.md
- findings.md
- progress.md

에 상태를 기록.

## Critical Rules

1. complex task면 plan first
2. 2-action rule
3. read before decide
4. update after act
5. log all errors
6. never repeat failures
7. completion 후 추가 작업은 plan phase 추가

## 3-Strike Protocol

같은 실패를 반복하지 않는다.

1차:
- diagnose

2차:
- alternative

3차:
- assumptions / search / replan

## Hook으로 보강

- UserPromptSubmit
- PreToolUse
- PostToolUse
- Stop
- PreCompact

Skill 본문에서 "기억해라"라고만 하지 않고 host lifecycle에 연결.

## Security boundary

현재 Skill은:

- automatic recovery는 project plan file만
- session history는 explicit 요청 필요
- replay는 bounded
- replay content는 untrusted data
- network upload path 없음

을 명시.

### 최근 3개월 변화

특히 9월:

- Cursor/Gemini hook schema 변경 대응
- hook executable 문제 수정
- Python import isolation
- stop hook이 불필요한 follow-up을 만들지 않도록 수정
- explicit attestation target
- stale plan pointer 처리

### 핵심 교훈

> 동일 Skill이라도 host별 Hook runtime semantics는 계속 달라진다.

portable SKILL.md와 host adapter를 분리해야 한다.

---

# 4.7 Ponytail

Repository:
https://github.com/DietrichGebert/ponytail

대표:
`skills/ponytail/SKILL.md`

Ponytail의 목적은:

> 적게 만드는 것.

## Minimalism ladder

순서:

1. 이 기능 자체가 필요한가
2. repo에 이미 있는가
3. stdlib가 하는가
4. platform native가 하는가
5. 설치된 dependency가 하는가
6. one-line인가
7. 그 다음 최소 코드

## 주요 rules

- unrequested abstraction 금지
- future scaffolding 금지
- deletion over addition
- boring over clever
- fewest files
- shortest working diff

그러나 다음은 줄이지 않음:

- trust-boundary validation
- data-loss prevention
- security
- accessibility
- explicit requirement

## "작게 만들기"와 "대충 만들기"를 구분

Ponytail은:

- 먼저 전체 flow 이해
- 그 다음 최소 change

를 요구.

"작은 diff"가 목적이 아니라:

> **올바른 위치의 작은 diff**

가 목적.

### 최근 3개월 변화

2026-07-10:

`ponytail:` marker가 trivial code에 과도하게 붙는 문제 때문에 rule을 좁힘.

즉 marker는:

- deliberate simplification
- known ceiling
- future upgrade path

가 실제로 존재할 때만 사용.

2026-09-14:

Cursor native hook 지원 추가.

### 핵심 교훈

> 강한 규칙도 over-application이 생기면 scope를 다시 줄인다.

---

# 4.8 ECC

Repository:
https://github.com/affaan-m/ECC

대표:

- `tdd-workflow`
- `verification-loop`
- rules/hooks ecosystem

## TDD

- tests first
- unit/integration/E2E
- 80% coverage
- test runner 자동 감지
- package manager와 test runner를 구분

## Verification

- build
- types
- lint
- test
- security
- diff

## Rules + Hooks

ECC는 Skill만 쓰지 않는다.

- Skill
- Rules
- Hooks
- profiles

를 함께 운영.

### 최근 3개월 변화

2026-09:

- MCP health hook을 MCP tool에만 scope
- failed step이 downstream evidence로 쓰이지 않게 함
- destructive SQL detection 강화
- hook isolation
- security hardening
- Lean / Full profile + Auto selection

### 핵심 교훈

> Hook이 유용하다고 전역으로 거는 것이 아니라 matcher scope를 계속 줄인다.

---

# 5. 최근 3개월에 실제로 수렴한 유지보수 패턴

이번 조사의 가장 중요한 결과다.

# P1. 규칙 추가보다 삭제가 많아지고 있다

Superpowers:

- duplicate section 삭제
- social proof 삭제
- recap 삭제

Vercel:

- detail을 reference로 이동
- terse style로 압축

Matt:

- PR skill에서 action mechanics 삭제
- stale Skill 삭제

Anthropic:

- office Skill docs trim

---

# P2. 그러나 이유 설명을 무조건 지우지는 않는다

Superpowers TDD 실험이 대표적이다.

rationale 삭제 후 pressure compliance가:

- 8/10
- → 5/10

으로 낮아짐.

따라서:

> 불필요한 explanation은 삭제하되, 실제 agent rationalization을 막는 explanation은 유지.

---

# P3. Absolute rule을 scope한다

Vercel:

- nested View Transition rule을 절대 금지처럼 쓰던 문구 수정
- 실제 실패 조건으로 범위 축소

Ponytail:

- comment marker 적용 범위 축소

ECC:

- Hook matcher를 MCP tool로 좁힘

Addy:

- negated trigger lint edge cases 수정

### 핵심

> "항상", "절대", "모든"은 최근 유명 Skill에서도 계속 문제를 만들고 수정되고 있다.

---

# P4. 현재 source에 근거 없는 규칙은 위험하다

Vercel:

- React/Next source 직접 검증
- 잘못된 버전/동작 설명 교정

Addy:

- official docs 기반 source-driven workflow

Anthropic:

- live sources / migration guide

### 핵심

framework/API Skill은 오래된 snapshot을 들고 있는 것보다:

- version detection
- live official source
- scoped current rule

이 더 중요하다.

---

# P5. Skill 자체도 eval 대상이다

Anthropic:

- realistic test prompts
- quantitative + qualitative eval
- description optimizer

Superpowers:

- pressure test
- micro-test
- control/treatment

Addy:

- plugin eval
- must-not-fire case

Ponytail:

- benchmark arms
- model별 반복

### 핵심

> 유명 Skill은 "잘 써 보인다"로 유지되지 않는다.

실제로 behavior test를 사용한다.

---

# 6. Description 철학은 아직 통일되지 않았다

이 부분은 책에서 단일 정답처럼 쓰면 안 된다.

## Anthropic

현재 Skill Creator:

- what + when
- under-triggering을 막기 위해 pushy
- trigger recall 강조

## Addy

- what + when
- workflow summary 금지

## Superpowers

가장 강하게:

> description에는 WHEN만

workflow summary가 body를 읽지 않는 shortcut이 될 수 있기 때문.

## Matt

context pointer라는 관점:

- leading concept
- branch별 trigger
- pointer 자체의 token cost

## Vercel

대체로:

- domain
- task type
- trigger keyword

을 명시.

### 책에서의 정리 방향

"description은 반드시 한 형식"이라고 하기보다:

1. 무엇을 하는 Skill인지 구분 가능해야 함
2. 언제 선택해야 하는지 분명해야 함
3. body workflow를 description이 대체하지 않아야 함
4. adjacent Skill과 경계가 있어야 함
5. 실제 trigger eval로 조정

이라고 쓰는 편이 근거와 더 잘 맞는다.

---

# 7. 유명 Skill의 공통 규칙을 책의 규칙으로 압축하면

## Rule 1

**Scope before prose.**

어디에 적용되는 rule인지 먼저 정한다.

## Rule 2

**Trigger is an interface.**

description은 검색/선택 surface다.

## Rule 3

**Do not encode generic intelligence.**

모델이 이미 아는 설명은 줄인다.

## Rule 4

**Make completion observable.**

"잘 해라" 대신 command, output, artifact, checklist.

## Rule 5

**Pressure-test the rule.**

평상시보다 shortcut 압력이 있을 때 rule이 지켜지는지 본다.

## Rule 6

**Move deterministic constraints into structure.**

validator, Hook, lint, CI, script.

## Rule 7

**Keep the entry point small.**

조건부 detail은 reference로.

## Rule 8

**Do not universalize a workaround.**

한 model/version의 실패는 Skill의 universal rule이 아니다.

## Rule 9

**Delete instruction debt.**

model/host가 좋아지거나 책임이 바뀌면 지침을 지운다.

## Rule 10

**Narrow absolute rules using real failures.**

"always/never"는 실제 failure boundary가 증명될 때만.

---

# 8. 책에 새로 반영할 가치가 높은 내용

기존 연구에 비해 이번 조사에서 특히 추가 가치가 있는 것은 다음이다.

## 8.1 Rationalization table의 역할

단순 anti-pattern 목록이 아니라:

> agent가 규칙을 우회할 때 실제 사용하는 논리를 미리 막는 장치.

Superpowers와 Addy에서 반복.

## 8.2 Rationale는 행동 효과로 삭제 여부를 결정

문장이 장황하다고 바로 지우지 않는다.

삭제 A/B에서 compliance가 떨어지면 남긴다.

## 8.3 Rule priority

Vercel처럼 70개 rule을 모두 같은 강도로 쓰지 않는다.

CRITICAL/HIGH/MEDIUM/LOW처럼 영향도를 구분.

## 8.4 Completion criteria

Matt의 agent-facing writing에서 강조.

각 step의 끝을:

- 이해했다
- 충분히 확인했다

같은 fuzzy state가 아니라 observable bound로 만든다.

## 8.5 Source freshness

Skill이 framework/API 지식을 담으면:

- snapshot
- version
- live source

전략을 명시해야 한다.

## 8.6 Hook scope regression

Hook은 한번 만들고 끝이 아니다.

최근 ECC/Ponytail/Planning-with-files 변경은 대부분:

- matcher
- schema
- host lifecycle
- noisy output
- platform portability

문제를 수정하고 있다.

---

# 9. 결론

최근 3개월의 유명 Skill들을 보면 좋은 Skill의 핵심은 "엄격한 규칙을 많이 넣는 것"이 아니다.

실제 방향은 다음과 같다.

```text
넓은 규칙
→ 실제 failure 확인
→ scope 좁힘
→ trigger 정밀화
→ 중복 prose 삭제
→ deterministic 부분 자동화
→ behavior eval
→ model/host 변화 후 다시 삭제
```

특히 중요한 변화는:

> **좋은 Skill은 규칙을 축적하는 문서가 아니라 규칙을 계속 압축하고 검증하는 실행 artifact다.**

최근 유명 프로젝트들은 이미 이 방향으로 움직이고 있다.
