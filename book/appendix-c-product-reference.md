# 부록 C. 제품별 지침 파일 참조

기준일: 2026-09-30

이 부록은 원리가 아니라 현재 제품 문법을 빠르게 찾기 위한 참조다. 제품 기능은 빠르게 바뀌므로 실제 적용 전 공식 문서를 다시 확인한다.

## C.1 Agent Skills 공개 규격

공개 규격(Specification)에 따른 최소 구조:

- Skill 디렉터리
- SKILL.md
- YAML 문서 앞부분의 설정 영역(frontmatter)
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

Anthropic 공식 문서는 필요한 정보를 단계적으로 공개하는 방식(progressive disclosure)을 설명한다. 먼저 Skill을 설명하는 메타데이터가 보이고, 관련 있는 Skill이 선택되면 본문을 읽는 방식이다.

공식 작성 가이드의 핵심:

- description에 무엇을 하는지와 언제 쓰는지 설명
- name은 구체적으로
- SKILL.md가 맡은 작업에 집중하도록 유지
- 상세 참고 자료는 분리
- 같은 조건에서 같은 결과를 내는 작업은 scripts 활용
- 실제 사용으로 테스트
- 신뢰하지 않는 Skill의 스크립트와 지침 검토

Official:
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## C.3 Claude Code

프로젝트에서 사용할 수 있는 핵심 지침 적용 영역은 CLAUDE.md, Rules, Skills, Hooks 계열이다.

정확한 적용 범위, 읽어 들이는 시점, 대상 선택 조건, 사건 문법은 Claude Code 버전에 따라 달라질 수 있으므로 현재 공식 문서를 판단의 기준이 되는 원본으로 사용한다.

문서:
https://code.claude.com/docs/

## C.4 OpenAI Codex

Codex 계열에서는 AGENTS.md와 Skills를 저장소 지침과 반복 작업 절차(workflow)에 사용할 수 있다.

2026-09-11 OpenAI의 GPT-6 Astra 관련 가이드는 오래된 AGENTS.md, 과도한 Skill description, 과거 모델의 부족한 부분을 보완하던 보조 지침(scaffolding)을 다시 점검할 것을 강조한다.

Skill 평가 가이드는 요청문 → 실행 기록 수집 → 검사 → 채점 형태의 전체 흐름을 간단히 확인하는 평가와 결과·절차·표현 방식·효율의 분리를 제안한다.

Official:
https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra

https://developers.openai.com/blog/eval-skills

## C.5 Cursor

현재 Cursor Project Rules는 .cursor/rules 아래의 .mdc 파일을 사용하며 적용 방식은 크게 다음으로 나뉜다.

- Always Apply
- Apply Intelligently
- Apply to Specific Files
- Apply Manually

문서 앞부분의 설정 영역에서 핵심 필드는 description, globs, alwaysApply다.

Cursor는 AGENTS.md를 일반 Markdown 지침으로 지원하며 하위 디렉터리의 AGENTS.md도 지원한다.

Official:
https://cursor.com/docs/rules

## C.6 Gemini CLI

Gemini CLI는 GEMINI.md를 계속 유지되는 문맥 정보에 사용하고 Agent Skills를 필요할 때 불러오는 전문 지식으로 구분한다.

현재 Agent Skills를 찾는 과정에서는 사용하도록 설정한 Skill의 name과 description이 먼저 노출되고 실제 호출 이후 SKILL.md 본문과 자료가 사용된다.

작업 공간의 Skill 경로로 .gemini/skills와 .agents/skills 별칭을 지원한다.

Official:
https://geminicli.com/docs/cli/skills/

https://geminicli.com/docs/cli/creating-skills/

https://geminicli.com/docs/cli/skills-best-practices/

## C.7 GitHub Copilot

GitHub Copilot의 사용자 지정 지침 기능에는 다음이 있다.

- repository-wide: .github/copilot-instructions.md
- path-specific: .github/instructions/**/*.instructions.md
- agent instructions: AGENTS.md
- 일부 적용 영역에서 CLAUDE.md, GEMINI.md도 인식

경로별 지침(path-specific instruction)은 applyTo로 대상을 지정한다.

지원 범위는 Copilot Chat, code review, CLI, cloud agent 등 적용 영역별로 다를 수 있으므로 기능별 지원 표를 확인한다.

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

특정 제품의 문서 앞부분의 설정 영역, 대상 선택 조건, 읽어 들이는 방식과 의미.

이 구분을 유지해야 제품 문법이 바뀌어도 책의 핵심 원리는 오래 유지된다.
