# 지침 파일 교차 제품 비교

기준일: 2026-09-30

## 1. 비교 목적

제품별 파일명을 외우는 것이 목적이 아니다.

책에서 구분해야 할 것은 다음 두 층이다.

- **보편 원리**: scope, trigger, progressive disclosure, single source of truth, verification
- **제품 문법**: 파일 위치, frontmatter field, loading/precedence semantics

보편 원리는 오래가지만 제품 문법은 빠르게 변한다.

## 2. 상시 지침 비교

| 제품 | 주요 상시 지침 | 특징 |
| --- | --- | --- |
| Claude Code | `CLAUDE.md`, `AGENTS.md` | user/project/local/managed scope, 하위 CLAUDE.md lazy load, Rules 지원 |
| OpenAI Codex | `AGENTS.md` | root-to-leaf instruction hierarchy와 directory scope |
| Cursor | `.cursor/rules/*.mdc`, User Rules, `AGENTS.md` | Always/agent-selected/glob/manual rule type |
| Gemini CLI | `GEMINI.md` | global/project/subdirectory hierarchy |
| GitHub Copilot | `.github/copilot-instructions.md`, path-specific instructions, `AGENTS.md` | repo-wide, path-specific, agent instructions 분리 |

공통점:

- 모든 것을 한 전역 파일에 넣는 방식보다 scope 분리를 제공하는 방향
- 팀 공유 지침과 개인 지침을 구분
- directory/path에 따라 더 구체적인 지침을 제공
- 반복 절차는 on-demand Skill로 이동하는 방향

## 3. Claude Code

### Global/personal

- `~/.claude/CLAUDE.md`
- `~/.claude/rules/`

### Project

- `./CLAUDE.md`
- `./.claude/CLAUDE.md`
- `.claude/rules/*.md`
- `.claude/skills/<name>/SKILL.md`

### Local

- `CLAUDE.local.md`

작성상 중요한 특성:

- CLAUDE.md는 context이지 hard enforcement가 아니다.
- path-scoped Rule은 `paths`로 범위를 제한한다.
- Rule frontmatter에서 지원되지 않는 필드는 조용히 무시될 수 있다.
- Skill description은 routing 신호다.
- 2026년 현재 AGENTS.md 직접 지원도 존재한다.
- 충돌한 user/project rule에 hard override를 기대하면 안 된다.

## 4. Cursor

### User Rules

개인 환경 전체에 적용되는 global preference다.

### Project Rules

`.cursor/rules/*.mdc`

현재 Rule type은 frontmatter 조합으로 결정된다.

- Always Apply
- Apply Intelligently
- Apply to Specific Files
- Apply Manually

핵심 fields:

- `alwaysApply`
- `description`
- `globs`

Cursor 공식 best practices:

- focused
- actionable
- scoped
- 500줄 미만 권장
- 큰 Rule 분리
- concrete example/reference 사용
- vague guidance 회피
- canonical file을 reference하고 내용을 복제하지 않음
- style guide 전체를 복사하기보다 linter 사용
- 드문 edge case를 모두 전역 규칙으로 만들지 않음

### AGENTS.md

Cursor는 root와 nested AGENTS.md를 지원하며 더 구체적인 하위 instruction을 적용할 수 있다.

## 5. OpenAI Codex

Codex 생태계에서 `AGENTS.md`는 standing repository instructions의 핵심 포맷이다.

OpenAI의 2026년 최신 지침에서 특히 강조되는 점:

- 오래된 AGENTS.md를 정기적으로 감사한다.
- 모든 변경 전에 모든 문서를 읽게 하지 않는다.
- 문서 포인터는 task condition과 연결한다.
- 최신 모델이 스스로 하는 행동을 과도하게 중복 지시하지 않는다.
- 과거 모델을 위해 추가했던 강한 경계가 새 모델을 멈추게 할 수 있는지 검토한다.

Skill 작성에서는:

- description을 짧고 좁게
- progressive disclosure
- root Skill을 minimal router로
- 과도한 recipe를 경계
- 모델별 eval 필요

## 6. Gemini CLI

### GEMINI.md

공식 문서가 제시하는 hierarchy:

- global: `~/.gemini/GEMINI.md`
- project root: `./GEMINI.md`
- subdirectory: 하위 `GEMINI.md`

공식 best practice:

- focused하게 유지
- actionable/relevant instructions
- 명확한 negative constraint
- 오래된 Rule 정기 삭제

### Skills

Gemini CLI는 Agent Skills open standard 기반 Skill을 지원한다.

discovery에서는 name/description, activation 후 본문과 resource를 읽는 progressive disclosure 모델이다.

또한 `.agents/skills/` alias를 제공해 도구 간 이식성을 고려한다.

## 7. GitHub Copilot

현재 공식 문서에서 instruction 종류를 분리한다.

### Repository-wide

`.github/copilot-instructions.md`

### Path-specific

`.github/instructions/**/*.instructions.md`

frontmatter의 `applyTo`로 파일 범위를 지정한다.

### Agent instructions

`AGENTS.md`

### Skills

task-specific workflow에 적합한 별도 Skill 체계를 지원하는 기능들이 있다.

GitHub 문서 역시 repo-wide rule, path-specific instruction, AGENTS.md standing rule, Skill workflow를 서로 다른 용도로 구분한다.

## 8. AGENTS.md의 의미

AGENTS.md는 vendor-neutral standing instruction의 중심 후보가 되었다.

장점:

- 여러 coding agent에서 인식
- plain Markdown
- repository와 함께 version control
- nested scope 지원 제품 증가

하지만 주의:

- 각 제품의 정확한 탐색/precedence/loading semantics는 동일하지 않다.
- 제품 전용 feature를 AGENTS.md 하나로 모두 표현할 수 없다.
- "한 AGENTS.md를 만들면 모든 도구가 완전히 같은 방식으로 따른다"는 설명은 피해야 한다.

## 9. Agent Skills 표준의 의미

`SKILL.md`의 portable core:

- directory
- YAML frontmatter
- `name`
- `description`
- Markdown instructions
- optional resources/scripts/assets

제품별로 추가 metadata와 실행 기능이 다르다.

책의 예제는 다음처럼 표시하는 것이 좋다.

- [Portable] Agent Skills 표준
- [Claude Code] 제품 확장
- [Cursor] 제품 확장
- [Gemini] 제품 확장
- [Codex] 제품 동작

## 10. 공통으로 수렴하는 작성 원리

제품이 달라도 반복해서 나타나는 원칙은 다음과 같다.

1. 전역 지침을 작게 유지한다.
2. 특정 path의 규칙은 해당 path로 scope한다.
3. 반복 procedure는 on-demand Skill로 분리한다.
4. description은 routing을 위해 구체적으로 쓴다.
5. 긴 상세 정보는 필요할 때만 읽게 한다.
6. canonical source를 reference하고 복제하지 않는다.
7. 반복되는 기계적 규칙은 lint/script/hook으로 승격한다.
8. 지침은 정기적으로 삭제/감사한다.
9. 실제 behavior로 검증한다.
10. 모델과 제품 버전이 바뀌면 다시 평가한다.

## 11. 책의 표기 전략 제안

각 장의 규칙을 다음 세 종류로 표시한다.

### Principle

제품 독립적인 작성 원칙.

예:
- "항상 필요한 정보만 상시 context에 둔다."

### Portable syntax

공개 표준으로 이동 가능한 부분.

예:
- Agent Skills의 `name`, `description`

### Vendor syntax

현재 특정 제품에서만 유효하거나 semantics가 다른 부분.

예:
- Claude Rule의 `paths`
- Cursor Rule의 `globs`, `alwaysApply`
- Copilot path instruction의 `applyTo`

이 구분이 있어야 책이 제품 업데이트에 덜 취약하다.

## 주요 출처

- Claude Code memory/rules
  - https://code.claude.com/docs/en/memory
- Claude Code skills
  - https://code.claude.com/docs/en/skills
- Cursor Rules
  - https://cursor.com/docs/rules
- OpenAI, Rethinking skills and prompts for GPT-6 Astra
  - https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- Gemini CLI, Manage context and memory
  - https://geminicli.com/docs/cli/tutorials/memory-management/
- Gemini CLI, Agent Skills
  - https://geminicli.com/docs/cli/skills/
- GitHub Copilot, custom instruction support
  - https://docs.github.com/en/copilot/reference/custom-instructions-support
- GitHub Copilot, code review customization comparison
  - https://docs.github.com/en/copilot/concepts/agents/code-review
- Agent Skills Specification
  - https://agentskills.io/specification
