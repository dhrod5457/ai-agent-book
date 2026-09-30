# AI 코딩 지침 파일 엔지니어링

Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot 같은 AI 코딩 도구가 저장소의 규칙과 반복 절차를 안정적으로 이해하도록 CLAUDE.md, AGENTS.md, Rules, SKILL.md, Hooks를 설계하고 검증하는 방법을 다룬다.

이 책은 에이전트를 만드는 책이 아니다. 멀티 에이전트 오케스트레이션이나 LLM API 구현이 중심도 아니다. 관심 대상은 사람이 저장소에 남기는 **지침 파일**이다.

## 핵심 질문

- 어떤 내용은 루트 지침에 남겨야 하는가.
- 어떤 내용은 경로별 Rule로 내려야 하는가.
- 어떤 절차는 Skill로 만들어야 하는가.
- 어떤 규칙은 자연어가 아니라 Hook, lint, type, schema, CI로 강제해야 하는가.
- Skill description은 어떻게 작성해야 정확히 선택되는가.
- 지침 파일의 품질은 어떻게 테스트할 것인가.
- 모델과 도구가 바뀌면 무엇을 삭제해야 하는가.

## 읽는 순서

### Part 1. 지침 파일은 왜 별도 엔지니어링 대상인가

1. [프롬프트에서 저장소 지침으로](01-from-prompt-to-repository-instructions.md)
2. [컨텍스트는 공짜가 아니다](02-context-is-not-free.md)

### Part 2. 어디에 무엇을 써야 하는가

3. [CLAUDE.md를 올바르게 쓰기](03-writing-claude-md.md)
4. [AGENTS.md와 다중 도구 호환성](04-agents-md-and-portability.md)
5. [Path-scoped Rules](05-path-scoped-rules.md)

### Part 3. SKILL.md를 쓰는 법

6. [Skill의 구조와 공개 표준](06-skill-structure.md)
7. [description이 Skill의 절반이다](07-skill-description-routing.md)
8. [Skill 본문을 실행 가능하게 쓰기](08-executable-skill-body.md)
9. [References와 Scripts](09-references-and-scripts.md)

### Part 4. 자연어로 쓰지 말아야 할 규칙

10. [Hook, lint, CI, type으로 승격하기](10-promote-prose-to-structure.md)
11. [Claude Code Hook 작성](11-claude-code-hooks.md)

### Part 5. 실제 사례 해부

12. [pstack의 Skill 파일을 뜯어보기](12-pstack-case-study.md)
13. [나쁜 지침 파일 리팩터링](13-refactoring-bad-instructions.md)

### Part 6. 지침 파일도 테스트한다

14. [Trigger Eval](14-trigger-eval.md)
15. [Output Eval](15-output-eval.md)
16. [A/B와 Blinded Eval](16-ab-and-blinded-eval.md)

### Part 7. 유지보수

17. [Skill Smell과 Instruction Debt](17-skill-smells-and-debt.md)
18. [모델이 바뀌면 지침도 다시 본다](18-model-upgrade-audit.md)
19. [지침 파일 리뷰 프로세스](19-review-process.md)

## 부록

- [A. 실전 체크리스트](appendix-a-checklists.md)
- [B. Skill Eval 템플릿](appendix-b-eval-template.md)
- [C. 제품별 지침 파일 참조](appendix-c-product-reference.md)
- [D. Anti-pattern Catalog](appendix-d-antipatterns.md)
- [E. 주요 출처](appendix-e-sources.md)

## 이 책의 중심 원칙

이 책 전체를 한 문장으로 줄이면 다음과 같다.

> 지침을 더 많이 쓰는 것이 목표가 아니다. 필요한 지식을 가장 좁은 범위에 두고, 기계가 판정할 수 있는 규칙은 구조로 옮기며, 남은 자연어 지침은 실제 행동으로 검증하는 것이 목표다.

리서치 근거와 조사 원문은 [research/instruction-files](../research/instruction-files/)에 유지한다.
