# 리서치 출처 카탈로그

기준일: 2026-09-30

## A. Anthropic / Claude Code

### How Claude remembers your project

URL:
https://code.claude.com/docs/en/memory

사용할 근거:

- CLAUDE.md의 scope
- user/project/local/managed instruction 위치
- CLAUDE.md는 context이며 hard enforcement가 아님
- 구체적이고 간결한 지침 권장
- CLAUDE.md 200줄 미만 목표
- path-scoped Rules
- Rule의 `paths` frontmatter
- user/project Rule 충돌 주의
- import는 context 절감 수단이 아님
- AGENTS.md 지원
- prompt audit 기능

### Extend Claude with skills

URL:
https://code.claude.com/docs/en/skills

사용할 근거:

- Skill discovery/loading semantics
- `description`과 `when_to_use`
- description listing 길이 제한
- unknown frontmatter field silent ignore 가능성
- malformed YAML 문제
- model invocation 설정
- Skill trigger debugging
- Skill eval workflow

### Skill authoring best practices

URL:
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

사용할 근거:

- context window는 공유 자원
- description = what + when
- progressive disclosure
- SKILL.md 500줄 미만 권장
- reference depth를 얕게
- 실제 사용 기반 iteration
- examples, scripts, validation

### Agent Skills overview

URL:
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

사용할 근거:

- metadata first
- body on activation
- resources on demand

### Steering Claude Code

URL:
https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more

발행:
2026-06-18

사용할 근거:

- CLAUDE.md, Rules, Skills, Hooks의 역할 분리
- context cost와 authority 차이
- procedure는 Skill
- deterministic action은 Hook

### Lessons from building Claude Code: How we use skills

URL:
https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills

발행:
2026-06-03

사용할 근거:

- Anthropic 내부 Skill 운영 경험
- Skill 구조/공유/운영에 대한 실무 관찰

### Effective context engineering for AI agents

URL:
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

발행:
2025-09-29

사용할 근거:

- context는 finite resource
- 최소 high-signal token
- brittle if/else prompt와 vague prompt 사이의 적절한 구체성
- 최소하지만 충분한 context

### Hooks reference

URL:
https://code.claude.com/docs/en/hooks

사용할 근거:

- event/matcher semantics
- unsupported matcher silent ignore
- command hook security
- full user permissions
- input sanitization
- path traversal
- sensitive files
- async deduplication 부재

## B. Agent Skills 공개 표준

### Specification

URL:
https://agentskills.io/specification

사용할 근거:

- portable SKILL.md directory structure
- required metadata
- scripts/references/assets
- vendor-specific field와 표준 field 구분

### Overview

URL:
https://agentskills.io/home

사용할 근거:

- discovery → activation → execution
- metadata와 body의 progressive disclosure

## C. OpenAI / Codex

### Rethinking skills and prompts for GPT-6 Astra

URL:
https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra

발행:
2026-09-11

사용할 근거:

- description 과잉 문제
- 너무 많은 Skill과 context budget
- broad trigger의 오작동
- minimal router
- 과도한 recipe가 최신 모델을 제한할 수 있음
- AGENTS.md instruction debt
- task-conditioned document pointers
- model evolution에 따른 지침 감사

### Testing Agent Skills Systematically with Evals

URL:
https://developers.openai.com/blog/eval-skills

발행:
2026-01-22

사용할 근거:

- Skill을 prompt처럼 eval
- outcome/process/style/efficiency
- trigger positive/negative control
- trace/artifact 기반 평가
- regression dataset

### Model guidance / AGENTS.md hierarchy

URL:
https://developers.openai.com/api/docs/guides/latest-model

사용할 근거:

- AGENTS.md root-to-leaf injection
- directory-specific instruction model

### Using PLANS.md for multi-hour problem solving

URL:
https://developers.openai.com/cookbook/articles/codex_exec_plans

사용할 근거:

- AGENTS.md에서 세부 procedure 문서를 가리키는 사례
- standing instruction과 detailed execution document 분리

## D. Cursor

### Rules

URL:
https://cursor.com/docs/rules

사용할 근거:

- Project/User/Team Rules
- `.cursor/rules/*.mdc`
- Always / Intelligent / Specific Files / Manual
- description/globs/alwaysApply
- 500줄 미만 권장
- rule 분리
- reference 사용
- style guide 복사 대신 linter
- 반복 mistake에서 rule 추가
- nested AGENTS.md

### pstack repository

URL:
https://github.com/cursor/plugins/tree/main/pstack

분석 파일:

- `skills/poteto-mode/playbooks/authoring-a-skill.md`
- `skills/poteto-mode/playbooks/eval.md`
- `skills/tdd/SKILL.md`
- `skills/how/SKILL.md`
- `skills/why/SKILL.md`
- `skills/technical-writing/SKILL.md`
- `skills/principle-encode-lessons-in-structure/SKILL.md`
- `skills/setup-pstack/SKILL.md`

사용할 근거:

- prose 최소화
- cross-skill reference
- trigger/skip boundary
- structural enforcement
- blinded evaluation
- small global configuration rule

## E. Gemini CLI

### Manage context and memory

URL:
https://geminicli.com/docs/cli/tutorials/memory-management/

사용할 근거:

- global/project/subdirectory GEMINI.md
- focused/actionable rule
- negative constraint
- periodic cleanup

### Agent Skills

URL:
https://geminicli.com/docs/cli/skills/

사용할 근거:

- Agent Skills 표준 기반
- discovery/activation/resource loading
- user/workspace scope
- `.agents/skills/` interoperability alias

### Extension guidance

URL:
https://geminicli.com/docs/extensions/writing-extensions/

사용할 근거:

- GEMINI.md always-on context와 Skill on-demand의 구분
- Hook lifecycle 역할

## F. GitHub Copilot

### Custom instructions support

URL:
https://docs.github.com/en/copilot/reference/custom-instructions-support

사용할 근거:

- repository-wide
- path-specific
- AGENTS.md/CLAUDE.md/GEMINI.md 지원 범위

### Adding repository custom instructions

URL:
https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide

사용할 근거:

- `.github/copilot-instructions.md`
- `.github/instructions/*.instructions.md`
- `applyTo`
- nearest AGENTS.md

### Code review customization comparison

URL:
https://docs.github.com/en/copilot/concepts/agents/code-review

사용할 근거:

- repo-wide instruction vs path instruction vs AGENTS.md vs Skills

## G. 학술/실증 자료

### From Anatomy to Smells: An Empirical Study of SKILL.md in Agent Skills

URL:
https://arxiv.org/abs/2607.01456

발행:
2026-07

핵심:
- 238개 Skill 정성 분석
- skill smell taxonomy
- 99% 이상 최소 하나 smell 보고

주의:
preprint.

### What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files

URL:
https://arxiv.org/abs/2608.08453

발행:
2026-08

핵심:
- 138,133 SKILL.md
- 91.8% 최소 하나 탐지 결함
- weak routing metadata, bloated/non-actionable body, poor resource organization

주의:
preprint.

### Signal or Noise? A Benchmark Study of Agent Skills in Web Development

URL:
https://arxiv.org/abs/2608.23067

발행:
2026-08

핵심:
- Skill 주입이 항상 성능 향상을 보장하지 않음
- context length/content 영향 분리 시도
- model별 차이
- anti-pattern rule의 유용성 관찰

주의:
특정 web development benchmark의 preprint. 수치 일반화 금지.

### GitSkills: A Dataset of Agent Skills on GitHub

URL:
https://arxiv.org/abs/2608.10906

발행:
2026-08

핵심:
- 수백만 SKILL.md occurrence 규모 dataset
- Skill을 소프트웨어 유지보수 아티팩트로 연구할 기반

주의:
preprint.

### Automating SKILL.md Generation for Computer-Using Agents via Interaction Trajectory Mining

URL:
https://arxiv.org/abs/2606.20363

발행:
2026-06

핵심:
- 실제 interaction trajectory에서 candidate skill을 추출하는 연구
- 실제 업무 trace 기반 Skill 생성/개선 아이디어

주의:
preprint.

### Lost in the Middle

URL:
https://arxiv.org/abs/2307.03172

핵심:
- 긴 context에서 중요한 정보의 위치에 따라 활용 성능 저하 가능
- "context가 크면 전부 넣어도 된다"는 가정의 배경 반례

## H. 추가 수집할 자료

다음은 책 집필 전 추가 조사 가치가 있다.

- Claude Code `/doctor prompt-audit` 실제 출력 사례
- Cursor rule lint/validation 방법
- Codex skill-creator 최신 원문
- Gemini Skill best practices 최신 원문
- Copilot path-specific instruction의 precedence edge case
- AGENTS.md 공개 표준의 nested semantics와 제품별 차이
- 실제 대규모 repository의 CLAUDE.md/AGENTS.md 사례 20~30개
- 지침 파일 변경 전후 실제 coding task eval 데이터
