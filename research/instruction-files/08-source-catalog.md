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


## I. 실제 변경 이력 / Instruction Debt 사례

### duthaho/skillhub — Description diet + invocation audit

URL:
https://github.com/duthaho/skillhub/commit/429242bd4f6c05c5695a25720f7684da1b9e01ad

사용할 근거:

- near-limit description 축소
- body detail과 trigger surface 분리
- manual-only 전환
- built-in collision validator
- description soft limit
- trigger eval surface가 실제 model-visible skill과 일치해야 함

### duthaho/skillhub — Trigger-first Skill 추가

URL:
https://github.com/duthaho/skillhub/commit/fd6a387ac86e4f71ff1885480d3fd9e324b727ad

사용할 근거:

- Skill 구현 전 trigger eval case 추가
- routing pair
- description을 TDD 대상으로 취급

### duthaho/skillhub — Validator CI gate

URL:
https://github.com/duthaho/skillhub/commit/f61a5d89ee4d5480da1b2acb888a1f167e000b0f

사용할 근거:

- structural validation을 PR gate로 승격
- semantic/LLM eval은 별도 유지
- registration drift를 CI에서 방지

### getsentry/skills — Runtime instruction 축소

URL:
https://github.com/getsentry/skills/commit/412f2368ee3ec90ce042826b57533f080d531aaf

사용할 근거:

- commit Skill 178 → 62 lines
- PR Writer 302 → 160 lines
- runtime에 실제 판단에 필요한 내용만 남김
- maintenance/spec/eval 책임 분리

### getsentry/skills — AXIS eval 도입

URL:
https://github.com/getsentry/skills/commit/5a64b36c62d042d3981b7937d9d6ca7bd1753b9a

사용할 근거:

- 실제 Codex harness 기반 Skill eval
- baseline/artifact/transcript
- small-inline, reference-backed, bad-output iteration case

### getsentry/skills — Skill-root-relative path 수정

URL:
https://github.com/getsentry/skills/commit/c81373583417504de2d3be1ae3d81977b11b2981

사용할 근거:

- provider path variable이 permission/runtime failure를 만든 사례
- portable relative path

### getsentry/skills — allowed-tools portability

URL:
https://github.com/getsentry/skills/commit/21af067ff3397fa35f5a0f22f05f6138d9e03307

사용할 근거:

- Claude에서는 허용되지만 공개 spec/다른 loader에서 깨지는 syntax
- Host-Tolerated Invalidity

### getsentry/skills — Runtime/SPEC 분리

URL:
https://github.com/getsentry/skills/commit/32fdf36273ac530120134ac484b3ab09717f3410

사용할 근거:

- runtime Skill 압축
- scope/maintenance contract를 SPEC으로 분리

### petekp/claude-code-setup — Opus 5.5 Skill audit

URL:
https://github.com/petekp/claude-code-setup/commit/0de2cbc2e9d2777743be990d6812b4d1820c3094

사용할 근거:

- model upgrade audit
- closing self-check 제거
- broad trigger wording 완화
- prompt style leakage
- 오래된 scaffolding 삭제

### c-reichert/flowstate — plugin guidance audit

URL:
https://github.com/c-reichert/flowstate/commit/756a19ae9fcc44cc44b49329dae57273b23be250

사용할 근거:

- stale metadata
- XML prompting guidance → Markdown
- 중복 invocation gate 제거
- trigger description 개선
- non-standard frontmatter 정리

### sfc-gh-eraigosa/dotfiles — Safety gate overcorrection

URL:
https://github.com/sfc-gh-eraigosa/dotfiles/commit/530d68bd0ee792884c85c58f5f528e39d354237d

사용할 근거:

- routine reversible action까지 막은 approval gate 제거
- 실제 publish 위험 경계만 유지
- alternate CLI bypass에 confirmation gate 추가

### sfc-gh-eraigosa/dotfiles — Hook semantic drift

URL:
https://github.com/sfc-gh-eraigosa/dotfiles/commit/fe438db541a1d53f1b6bd45c5e4c48fed2c60674

사용할 근거:

- Hook target resolution과 실제 tool semantics 불일치
- global flag 우회
- false-green test harness
- 실제 semantics와 Hook을 맞춘 regression test

### petekp/claude-code-setup — Skill infrastructure doctor

URL:
https://github.com/petekp/claude-code-setup/commit/aa756fd543657d2fb80ce20b34af50d7958dc3e5

사용할 근거:

- self-parent symlink loop
- content 외 instruction infrastructure health

## J. Nested scope 실제 사례

### sfc-gh-eraigosa/dotfiles

URLs:
- https://github.com/sfc-gh-eraigosa/dotfiles/blob/main/AGENTS.md
- https://github.com/sfc-gh-eraigosa/dotfiles/blob/main/sdk/AGENTS.md
- https://github.com/sfc-gh-eraigosa/dotfiles/blob/main/docker/AGENTS.md
- https://github.com/sfc-gh-eraigosa/dotfiles/blob/main/ai/skills/AGENTS.md

사용할 근거:

- root → subtree → module progressive scope
- Docker local invariant
- Skill authoring local policy
- AGENTS/CLAUDE symlink 기반 shared source

### radio4000/r4-svelte

URLs:
- https://github.com/radio4000/r4-svelte/blob/main/AGENTS.md
- https://github.com/radio4000/r4-svelte/blob/main/src/lib/components/AGENTS.md

사용할 근거:

- nearest nested instruction
- local gotcha만 담는 매우 작은 AGENTS
- 더 깊은 detail은 source header comment로 이동

### pulumi/customer-managed-workflow-agent

URLs:
- https://github.com/pulumi/customer-managed-workflow-agent/blob/main/AGENTS.md
- https://github.com/pulumi/customer-managed-workflow-agent/blob/main/kubernetes/AGENTS.md

사용할 근거:

- repository-wide restriction과 Kubernetes-specific convention 분리
- parent-child 일부 중복 사례

### BlackBeltTechnology/pi-agent-dashboard

URLs:
- https://github.com/BlackBeltTechnology/pi-agent-dashboard/blob/develop/AGENTS.md
- https://github.com/BlackBeltTechnology/pi-agent-dashboard/blob/develop/openspec/specs/dox-directory-foldering/spec.md

사용할 근거:

- AGENTS size/row lint
- byte cap과 row cap 분리
- parent roll-up 금지
- filesystem ownership과 instruction ownership 정렬
- sidecar progressive disclosure


## K. Cross-host Skill runtime / pilot adapter 공식 자료

### Claude Code Skills

URL:
https://code.claude.com/docs/en/skills

사용할 근거:

- description 기반 자동 invocation
- `/skill-name` 명시 호출
- `disable-model-invocation: true`
- manual-only일 때 description도 model context에서 제외
- Skill body lifecycle
- trigger와 output eval을 분리
- `claude plugin eval` 및 skill-creator eval
- nested project Skill loading

### OpenAI / Codex Skill Evals

URL:
https://developers.openai.com/blog/eval-skills

사용할 근거:

- name/description이 primary selection signal
- explicit / implicit / contextual / negative control
- `$skill` / `/skills` explicit activation
- `codex exec --json` JSONL trace
- deterministic grader + rubric grader

### OpenAI Skills Guide

URL:
https://developers.openai.com/api/docs/guides/tools-skills

사용할 근거:

- Skill discovery 시 name/description
- full SKILL.md on selection
- Agent Skills standard compatibility
- skill instruction priority/runtime notes

### Cursor Agent Skills

URL:
https://cursor.com/docs/skills

사용할 근거:

- automatic relevance-based Skill use
- `/skill-name` manual use
- `disable-model-invocation`
- Skill `paths` scope
- legacy `globs` fallback
- Claude/Codex Skill directory compatibility

### Cursor Hooks

URL:
https://cursor.com/docs/hooks

사용할 근거:

- agent lifecycle observability hooks
- 현재 조사에서는 Skill-specific auto-activation event를 별도 확인하지 못함

### Gemini CLI Agent Skills

URL:
https://geminicli.com/docs/cli/skills/

사용할 근거:

- discovery → activation → consent → injection → execution
- startup name/description metadata
- `activate_skill`
- enabled/disabled Skill management

### Gemini `activate_skill`

URL:
https://geminicli.com/docs/tools/activate-skill/

사용할 근거:

- tool argument로 Skill name이 노출됨
- tool은 agent 전용
- activation 관측 surface

### GitHub Copilot CLI Skill reference

URL:
https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference

사용할 근거:

- auto invocation
- `/SKILL-NAME`
- `disable-model-invocation`
- `user-invocable`
- `copilot skill list --json`
- Skill frontmatter limits

### GitHub Copilot Skills how-to

URL:
https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills

사용할 근거:

- prompt + description 기반 선택
- explicit invocation
- enable/disable/reload workflow
