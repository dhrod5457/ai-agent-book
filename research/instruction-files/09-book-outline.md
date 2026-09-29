# 책 목차 후보: AI 코딩 지침 파일 작성 가이드

## 책의 한 문장 정의

> Claude Code, Codex, Cursor, Gemini CLI 등 AI 코딩 도구가 프로젝트 규칙과 반복 절차를 정확히 이해하도록 CLAUDE.md, AGENTS.md, Rules, SKILL.md, Hooks를 작성하고 검증하는 방법을 다루는 실전 가이드.

## 다루지 않는 것

- 범용 AI Agent 개발 프레임워크
- multi-agent orchestration 자체
- LLM API를 이용한 agent 구현
- MCP server 개발이 중심인 내용
- 특정 모델을 이용한 자동 개발 조직 설계

필요할 때 언급하더라도 "지침 파일의 위치와 품질"을 설명하기 위한 배경으로 제한한다.

# Part 1. 지침 파일은 왜 별도 엔지니어링 대상인가

## 1장. 프롬프트에서 저장소 지침으로

- 일회성 prompt와 persistent instruction
- 지침 파일의 등장
- CLAUDE.md, AGENTS.md, Rules, SKILL.md
- 자연어 파일이지만 소프트웨어 동작을 바꾸는 artifact
- GitSkills와 2026년 Skill 연구

## 2장. 컨텍스트는 공짜가 아니다

- 항상 로드되는 instruction의 비용
- context engineering
- Lost in the Middle
- 너무 많은 지침의 문제
- 최신 모델이 오래된 scaffolding을 싫어할 수 있는 이유
- instruction debt

# Part 2. 어디에 무엇을 써야 하는가

## 3장. CLAUDE.md를 올바르게 쓰기

- user/project/local/managed scope
- 상시 필요한 사실
- 실제 command/path/symbol
- 200줄 목표의 의미
- import의 오해
- nested CLAUDE.md
- 충돌 Rule
- 유지보수 comment
- prompt audit

## 4장. AGENTS.md와 다중 도구 호환성

- AGENTS.md의 역할
- Codex hierarchy
- Claude Code 지원
- Cursor nested AGENTS.md
- Copilot 지원
- 공통 파일과 vendor file 분리
- "하나의 파일로 모든 제품 통일"의 한계

## 5장. Path-scoped Rules

- 왜 전역 Rule을 줄여야 하는가
- Claude `paths`
- Cursor `globs`
- Copilot `applyTo`
- folder/file type별 규칙
- precedence와 conflict
- Rule 파일 하나에 topic 하나
- style guide 대신 linter

# Part 3. SKILL.md를 쓰는 법

## 6장. Skill의 구조와 공개 표준

- Agent Skills specification
- SKILL.md
- scripts/references/assets
- portable core
- vendor extension
- progressive disclosure

## 7장. description이 Skill의 절반이다

- discovery와 activation
- what + when
- keyword stuffing 문제
- 너무 넓은 trigger
- positive trigger
- negative boundary
- 인접 Skill 간 overlap
- description budget
- concise하지만 trigger-rich한 description
- negative applicability와 no-match/abstention
- deprecated alias와 canonical router
- Skill inventory collision

## 8장. Skill 본문을 실행 가능하게 쓰기

- 목적
- precondition
- steps
- guardrail
- fallback
- verification
- output contract
- precondition과 persistent workflow state
- state owner와 허용된 transition
- side-effect intent gate: prepare/preview와 deploy/render의 차이
- stop / handoff / user approval
- high/medium/low freedom
- 과도한 recipe를 피하는 법

## 9장. References와 Scripts

- root Skill은 router
- 언제 reference를 읽게 할지
- reference depth
- 큰 문서를 나누는 법
- scripts가 prose보다 나은 경우
- script contract
- executable state-machine driver
- cached CLI manual 대신 --help / generated schema
- live official source vs installed-version-matched source
- canonical source를 Skill에 복제하지 않는 법
- 오류 출력과 재실행

# Part 4. 자연어로 쓰지 말아야 할 규칙

## 10장. Hook, lint, CI, type으로 승격하기

- 지침과 enforcement의 차이
- "반드시"라는 단어의 함정
- formatter
- lint
- schema/type
- CI
- Hook
- permission
- pstack Encode Lessons in Structure
- Azure Validate: prose 9-step workflow → script-driven state machine
- evaluator permission도 최소화해야 하는 이유

## 11장. Claude Code Hook 작성

- lifecycle event
- matcher
- exact vs regex
- blocking
- output/exit contract
- async
- idempotency
- security
- workspace trust
- Hook도 테스트해야 하는 이유

# Part 5. 실제 사례 해부

## 12장. pstack의 Skill 파일을 뜯어보기

- authoring-a-skill
- tdd의 trigger/skip 경계
- how/why 책임 분리
- principle leaf Skill
- router Skill
- global model Rule
- duplicate instruction 회피
- 그대로 복제하면 안 되는 제품 종속 부분

## 13장. 나쁜 지침 파일 리팩터링

하나의 거대한 예제:

- 800줄 CLAUDE.md
- 중복 rules
- broad Skill description
- 긴 reference chain
- "항상 테스트" 자연어
- 오래된 command

리팩터링:

- always-on 핵심만 남김
- path rule 분리
- procedure를 Skill로
- machine-checkable rule을 Hook/lint로
- eval 추가

# Part 6. 지침 파일도 테스트한다

## 14장. Trigger Eval

- description은 routing interface다
- Trigger-Driven Development: Skill보다 eval case를 먼저 쓴다
- explicit positive
- implicit positive
- noisy positive
- adjacent negative
- routing pair
- none / abstention
- manual-only와 auto-trigger의 다른 평가 기준
- accuracy, macro-F1, false positive, collision error
- 반복 실행과 run consistency

## 15장. Output Eval

- outcome
- process
- style
- efficiency
- trace
- artifact
- deterministic grader
- rubric grader

## 16장. A/B와 Blinded Eval

- baseline
- current/proposed
- judge bias
- deterministic grader와 semantic grader 분리
- length-matched control
- raw trace와 artifact 보존
- root monolith vs nested AGENTS vs path rule
- scope efficiency와 irrelevant-rule leakage
- model/host/version별 비교

# Part 7. 유지보수

## 17장. Skill Smell과 Instruction Debt

- 2026년 empirical studies
- weak routing metadata
- bloated body
- poor resource organization
- duplicated instruction
- stale reference
- conflict
- non-actionable prose
- vendor leakage
- workflow ownership collision
- unowned state transition
- side-effect intent collapse
- cached CLI manual
- compatibility logic duplication
- host-tolerated invalidity
- eval skill collision
- latest-version override
- duplicated domain tokens
- missing completion bound

## 18장. 모델이 바뀌면 지침도 다시 본다

- OpenAI GPT-6 Astra 사례
- 실제 Opus 5.5 Skill audit 사례
- 오래된 handholding 제거
- closing self-check와 broad trigger 재검토
- 모델이 이미 하는 행동 삭제
- overly strict boundary 완화 검토
- safety gate overcorrection과 되돌림
- 여러 모델을 쓰는 팀의 portable instruction
- Host-Tolerated Invalidity

## 19장. 지침 파일 리뷰 프로세스

- 변경 이유
- ownership
- lint
- link validation
- positive/negative eval
- baseline
- human review
- version note
- removal condition
- canonical source와 freshness strategy
- candidate/installed Skill eval isolation
- feedback → eval candidate → regression loop

# Appendix

## A. CLAUDE.md 체크리스트

## B. AGENTS.md 체크리스트

## C. Rule 체크리스트

## D. SKILL.md 체크리스트

## E. Hook 보안 체크리스트

## F. Skill eval template

## G. 제품별 frontmatter reference

## H. 지침 파일 anti-pattern catalog

## I. 연구 논문과 공식 문서 목록

# 책의 차별점

이 책이 단순 공식 문서 모음과 달라지려면 다음을 포함해야 한다.

1. 같은 규칙을 어느 파일에 둘지 판단하는 decision tree
2. 실제 bad → good 리팩터링
3. Skill trigger negative test
4. 지침 파일 A/B eval
5. pstack 같은 실제 공개 프로젝트 분석
6. 2026년 Skill empirical research 반영
7. vendor-neutral principle과 vendor syntax의 명시적 분리
8. 모델 업데이트 시 지침을 삭제하는 maintenance 전략
9. prose → lint/hook/type으로 승격하는 기준
10. 독자가 자신의 저장소 지침을 직접 진단할 수 있는 checklist와 scoring rubric

# 우선 집필 추천 순서

처음부터 1장부터 쓰기보다 다음 순서로 실증 자료를 먼저 만든다.

1. 3장 CLAUDE.md
2. 7장 Skill description
3. 8장 Skill body
4. 10장 구조적 enforcement
5. 14~16장 eval
6. 12장 pstack 사례
7. 17장 Skill smell
8. 나머지 개념 장

이 순서가 좋은 이유는 책의 핵심 주장을 실제 예제와 평가 데이터로 먼저 검증할 수 있기 때문이다.
