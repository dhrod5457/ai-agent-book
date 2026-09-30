# 부록 C. 제품별 지침 파일 참조

기준일: 2026-09-30

이 부록은 원리가 아니라 현재 제품 문법을 빠르게 찾기 위한 참조다. 제품 기능은 빠르게 바뀌므로 실제 적용 전 공식 문서를 다시 확인한다.

## C.1 Agent Skills 공개 규격

공개 Specification 기준 최소 구조:

- Skill directory
- SKILL.md
- YAML frontmatter
- required: name
- required: description
- optional: license
- optional: compatibility
- optional: metadata
- optional experimental: allowed-tools
- optional directories: scripts, references, assets

현재 규격에서 name은 최대 64자이며 소문자 영숫자와 하이픈 제약이 있다. description은 최대 1024자이며 무엇을 하는지와 언제 사용하는지를 설명해야 한다.

Specification:
https://agentskills.io/specification

## C.2 Claude / Anthropic Skills

Anthropic 공식 문서는 Skill metadata가 먼저 노출되고 Skill이 관련 있을 때 본문을 읽는 progressive disclosure를 설명한다.

공식 작성 가이드의 핵심:

- description에 what과 when
- name은 구체적으로
- SKILL.md를 focused하게 유지
- 상세 reference는 분리
- deterministic task는 scripts 활용
- 실제 사용으로 test
- 신뢰하지 않는 Skill의 script와 instruction 검토

Official:
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## C.3 Claude Code

프로젝트에서 사용할 수 있는 핵심 지침 surface는 CLAUDE.md, Rules, Skills, Hooks 계열이다.

정확한 scope, loading, matcher, event 문법은 Claude Code 버전에 따라 달라질 수 있으므로 현재 공식 문서를 source of truth로 사용한다.

Docs:
https://code.claude.com/docs/

## C.4 OpenAI Codex

Codex 계열에서는 AGENTS.md와 Skills를 저장소 지침과 반복 workflow에 사용할 수 있다.

2026-09-11 OpenAI의 GPT-6 Astra 관련 가이드는 오래된 AGENTS.md, 과도한 Skill description, 과거 모델용 scaffolding을 다시 감사할 것을 강조한다.

Skill 평가 가이드는 prompt → captured run → checks → score 형태의 lightweight end-to-end eval과 outcome/process/style/efficiency 분리를 제안한다.

Official:
https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra

https://developers.openai.com/blog/eval-skills

## C.5 Cursor

현재 Cursor Project Rules는 .cursor/rules 아래의 .mdc 파일을 사용하며 적용 방식은 크게 다음으로 나뉜다.

- Always Apply
- Apply Intelligently
- Apply to Specific Files
- Apply Manually

핵심 frontmatter는 description, globs, alwaysApply다.

Cursor는 AGENTS.md를 plain Markdown 지침으로 지원하며 nested AGENTS.md도 지원한다.

Official:
https://cursor.com/docs/rules

## C.6 Gemini CLI

Gemini CLI는 GEMINI.md를 persistent context에 사용하고 Agent Skills를 on-demand expertise로 구분한다.

현재 Agent Skills discovery에서는 enabled Skill의 name과 description이 먼저 노출되고 activation 이후 SKILL.md body와 resource가 사용된다.

workspace Skill 경로로 .gemini/skills와 .agents/skills alias를 지원한다.

Official:
https://geminicli.com/docs/cli/skills/

https://geminicli.com/docs/cli/creating-skills/

https://geminicli.com/docs/cli/skills-best-practices/

## C.7 GitHub Copilot

GitHub Copilot의 custom instruction surface에는 다음이 있다.

- repository-wide: .github/copilot-instructions.md
- path-specific: .github/instructions/**/*.instructions.md
- agent instructions: AGENTS.md
- 일부 surface에서 CLAUDE.md, GEMINI.md도 인식

path-specific instruction은 applyTo로 대상을 지정한다.

지원 범위는 Copilot Chat, code review, CLI, cloud agent 등 surface별로 다를 수 있으므로 support matrix를 확인한다.

Official:
https://docs.github.com/en/copilot/reference/custom-instructions-support

https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide

## C.8 책에서의 표기 규칙

본문에서는 제품별 기능을 다음처럼 해석한다.

### Principle

제품과 무관한 설계 원칙.

### Portable syntax

Agent Skills처럼 공개 규격으로 이식 가능한 부분.

### Vendor syntax

특정 제품의 frontmatter, matcher, loading semantics.

이 구분을 유지해야 제품 문법이 바뀌어도 책의 핵심 원리는 오래 유지된다.
