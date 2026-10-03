# 부록 E. 주요 출처

기준일: 2026-09-30

본문은 제품 공식 문서, 공개 규격, 공식 저장소, 실증 연구, 공개 Skill 사례를 바탕으로 작성했다.

상세 조사 메모와 원문 링크는 research/instruction-files 디렉터리에 보존한다.

## E.1 공개 규격

### Agent Skills Specification

https://agentskills.io/specification

핵심 사용 영역:

- SKILL.md 구조
- name/description 제약
- scripts/references/assets
- 필요한 정보를 단계적으로 공개하는 방식(progressive disclosure)
- 검증

## E.2 Anthropic / Claude

### Agent Skills Overview

https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

### Skill Authoring Best Practices

https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

### Claude Code Documentation

https://code.claude.com/docs/

핵심 사용 영역:

- 모델에 제공할 정보의 분량 한도
- Skill 찾기
- 무엇을 하는지와 언제 쓰는지를 설명하는 description
- 필요한 정보를 단계적으로 공개하는 방식
- scripts
- Hooks
- 작업 공간의 신뢰 여부

## E.3 OpenAI

### Rethinking skills and prompts for GPT-6 Astra

https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra

Published: 2026-09-11

핵심 사용 영역:

- 지침 분량 줄이기
- 오래된 AGENTS.md 감사
- 모델의 부족한 부분을 보완하던 과도한 보조 지침(scaffolding) 제거
- Skill description 축소와 재평가

### Testing Agent Skills Systematically with Evals

https://developers.openai.com/blog/eval-skills

Published: 2026-01-22

핵심 사용 영역:

- outcome/process/style/efficiency
- 실행 기록 수집
- 기계적으로 판정하는 검사
- 평가 기준표(rubric)에 따른 채점
- 기준 결과와의 비교

## E.4 Cursor

### Cursor Rules

https://cursor.com/docs/rules

핵심 사용 영역:

- Project Rules
- User/Team Rules
- description/globs/alwaysApply
- AGENTS.md
- nested AGENTS.md

### Cursor Plugins / pstack

https://github.com/cursor/plugins/tree/main/pstack

중점 분석 파일:

- authoring-a-skill 실무 절차서
- tdd Skill
- how / why Skills
- principle-encode-lessons-in-structure
- 평가 실무 절차서

## E.5 Gemini CLI

### Agent Skills

https://geminicli.com/docs/cli/skills/

### Creating Agent Skills

https://geminicli.com/docs/cli/creating-skills/

### Agent Skill Best Practices

https://geminicli.com/docs/cli/skills-best-practices/

핵심 사용 영역:

- discovery/activation
- .gemini/skills
- .agents/skills 별칭
- 필요한 정보를 단계적으로 공개하는 방식
- 자유도
- 같은 조건에서 같은 결과를 내는 스크립트

## E.6 GitHub Copilot

### Custom Instructions Support

https://docs.github.com/en/copilot/reference/custom-instructions-support

### Repository Instructions

https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide

핵심 사용 영역:

- .github/copilot-instructions.md
- .github/instructions
- applyTo
- AGENTS.md
- 적용 영역별 지원 차이

## E.7 공개 Skill 사례

리서치에서는 다음과 같은 공개 저장소의 Skill과 최근 유지보수 사례를 비교했다.

- anthropics/skills
- cursor/plugins pstack
- obra/superpowers
- mattpocock/skills
- addyosmani/agent-skills
- vercel-labs/agent-skills
- OthmanAdi/planning-with-files
- duthaho/skillhub
- getsentry/skills
- Firebase 관련 Skills
- Expo 관련 Skills
- Supabase 관련 Skills
- Cloudflare 관련 Skills
- Firecrawl CLI Skills
- Google Stitch Skills

각 사례의 별표 즐겨찾기 수나 유명세는 품질 점수가 아니라 관찰 표본을 고르기 위한 판단 신호로만 사용했다.

## E.8 리서치 문서

이 저장소의 다음 문서를 책의 근거층으로 유지한다.

- 01-core-authoring-principles.md
- 02-claude-md-and-rules.md
- 03-skill-md-authoring.md
- 04-hooks-and-enforcement.md
- 05-pstack-case-study.md
- 06-cross-vendor-comparison.md
- 07-evaluation-and-skill-smells.md
- 08-source-catalog.md
- 10-anthropic-internal-skill-lessons.md
- 11-public-instruction-corpus.md
- 12-observed-patterns-and-smells.md
- 13-real-world-validation-patterns.md
- 14-real-world-hook-patterns.md
- 15-instruction-debt-history.md
- 16-nested-scope-case-studies.md
- 17-experiment-protocol.md
- 18-trigger-eval-corpus.md
- 19-scope-eval-fixture.md
- 20-evidence-gap-matrix.md
- 21-cross-host-skill-pilot-adapters.md
- 22-popular-skills-rules-2026-q3.md
- 23-operational-skill-rule-patterns.md
- 24-popular-skill-rule-matrix.md
- 25-official-vendor-skill-maintenance.md
- 26-popular-skills-saturation-and-governance.md
- 27-corpus-ten-axis-reclassification.md
- 28-bad-good-refactoring-casebook.md
- 29-structural-validator-spec.md
- 30-instruction-review-checklist.md

## E.9 출처 사용 원칙

출처 우선순위는 다음과 같다.

1. 제품 공식 문서와 공식 블로그
2. 공개 표준 명세
3. 공식 저장소의 실제 지침 파일
4. 실증 연구와 정식 출판 전 논문
5. 커뮤니티 자료는 보조 사례

제품 문법은 빠르게 변한다. 따라서 본문의 설계 원리와 이 부록의 현재 문법을 분리해서 읽어야 한다.
