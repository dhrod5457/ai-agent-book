# 유명 Agent Skills 추가 조사: 업무형 Skill의 규칙 구조

기준일: 2026-09-30  
조사 기간: 2026-07-01 ~ 2026-09-30

## 1. 왜 추가 조사가 필요했는가

`22-popular-skills-rules-2026-q3.md`의 첫 표본은 Superpowers, Matt Pocock, Addy Osmani, ECC처럼 **개발 방법론 자체를 바꾸는 Skill** 비중이 높았다.

이번 추가 조사는 실제 설치 상위권과 공식 vendor Skill에서 다음 유형을 더 본다.

- 브라우저 자동화
- Skill 검색/설치
- 영상 제작
- 클라우드 배포
- 데이터베이스 업그레이드
- PR 리뷰
- Skill 보안 스캔
- UI 디자인

목표는:

> 실제 업무형 Skill에서도 방법론형 Skill과 같은 규칙이 반복되는가, 아니면 다른 설계 규칙이 필요한가?

를 확인하는 것이다.

## 2. 인기 표본 선정 근거

보조 자료로 `LinklyAI/best-skills`의 2026-09-29 집계 snapshot을 사용했다.

이 집계는 skills.sh, ClawHub, SkillHub, GitHub 등 여러 공개 신호를 합친 제3자 ranking이다. 품질의 객관적 순위를 의미하지 않으며, 이번 연구에서는 "많이 설치되거나 널리 노출된 Skill 후보를 찾는 용도"로만 사용한다.

해당 snapshot에서 상위권에는 다음이 포함됐다.

- `vercel-labs/agent-browser/agent-browser`
- `anthropics/skills/frontend-design`
- `vercel-labs/skills/find-skills`
- `mattpocock/skills/grill-me`
- `anthropics/skills/skill-creator`
- `mattpocock/skills/grill-with-docs`
- `vercel-labs/agent-skills/web-design-guidelines`
- `remotion-dev/skills/remotion-best-practices`
- `vercel-labs/agent-skills/vercel-react-best-practices`
- Microsoft Azure Skill 군

이번 추가 분석에서는 이미 충분히 분석한 표본과 중복을 줄이고 다음을 집중해서 읽었다.

1. `vercel-labs/agent-browser`
2. `vercel-labs/skills/find-skills`
3. `remotion-dev/skills`
4. `microsoft/azure-skills`
5. canonical source인 `microsoft/GitHub-Copilot-for-Azure`
6. `prisma/skills`
7. `firebase/firebase-tools`
8. `getsentry/skills`
9. `anthropics/skills/frontend-design`
10. Matt Pocock의 `grill-me`, `grill-with-docs`

## 3. 가장 중요한 추가 결론

첫 조사와 추가 조사를 합치면 Skill은 크게 두 종류의 규칙을 가진다.

### A. Methodology Rules

에이전트의 사고/개발 절차를 바꾸는 규칙.

예:

- TDD
- planning
- review
- minimalism
- verification
- source checking

### B. Operational Contract Rules

실제 외부 시스템을 다룰 때 필요한 계약.

예:

- prerequisite state
- user approval
- destructive-action gate
- allowed tools
- version compatibility
- deployment status
- output schema
- live-source freshness
- deprecated alias routing
- host-specific runtime

추가 조사에서 업무형 Skill은 B 비중이 훨씬 높았다.

# 4. agent-browser: Skill 본문을 설치 버전과 같이 배포한다

Repository:
https://github.com/vercel-labs/agent-browser

대표:
`skills/agent-browser/SKILL.md`

현재 공개 Skill은 약 53줄이다.

핵심은 이 `SKILL.md`가 실제 usage guide가 아니라 discovery stub이라는 점이다.

본문은 먼저:

`agent-browser skills get core`

를 호출하게 하고, 더 상세한 내용은:

`agent-browser skills get core --full`

로 읽게 한다.

## 이 설계의 이유

Skill 파일에 CLI command surface를 길게 박아 두면 CLI version은 올라가는데 설치된 Skill snapshot은 오래되어 명령/flag가 어긋날 수 있다.

agent-browser는 이를 다음처럼 해결한다.

static discovery stub → installed CLI → version-matched skill content

본문도 CLI가 제공하는 Skill content는 설치 버전과 맞으므로 instructions가 stale하지 않는다는 구조를 취한다.

## Specialized Skill routing

core 외에도 electron, slack, dogfood, derive-client, vercel-sandbox, protected-vercel-deployments, agentcore를 필요할 때 별도로 로드한다.

즉 top-level Skill은 거대한 browser automation manual이 아니라 router 역할을 한다.

## allowed-tools

frontmatter에서 `Bash(agent-browser:*)`, `Bash(npx agent-browser:*)`처럼 실행 surface를 제한한다.

### 책에 추가할 패턴

**Version-Coupled Instruction Pattern**

도구의 CLI/API가 빠르게 변할 때:

- static SKILL.md에는 stable discovery contract만 둔다.
- detailed command guidance는 설치된 executable/package에서 읽는다.

이 방식은 live web docs와도 다르다. 웹 최신 문서가 아니라 **현재 설치된 버전과 일치하는 문서**를 읽는 전략이다.

# 5. find-skills: discovery Skill도 fallback이 필요하다

Repository:
https://github.com/vercel-labs/skills

대표:
`skills/find-skills/SKILL.md`

약 142줄.

## 핵심 workflow

1. user need 파악
2. leaderboard 확인
3. CLI 검색
4. quality signal 확인
5. option 제시
6. user가 원하면 설치

## 중요한 규칙

검색 결과를 바로 추천하지 않는다.

현재 Skill은 install count, source reputation, GitHub stars를 확인하게 한다.

이것은 해당 Skill의 quality heuristic이지 보편적인 품질 판정 기준으로 채택하면 안 된다.

특히 popularity != safety, stars != instruction quality, official source도 bug가 있을 수 있기 때문이다.

## No-result fallback

검색 결과가 없으면:

1. 없다고 말함
2. 일반 능력으로 직접 도와줌
3. 반복 작업이면 custom Skill 생성을 제안

### 책에 추가할 패턴

**Discovery Must Degrade Gracefully**

Router/discovery Skill은 "적합한 Skill 없음"을 정상 결과로 지원해야 한다. 무조건 어떤 Skill이든 선택하는 router는 over-routing을 만든다.

# 6. Remotion: 사용자 변경 보존과 side-effect gate

Repository:
https://github.com/remotion-dev/skills

대표:
`skills/remotion-best-practices/SKILL.md`

## 첫 규칙: Preserve user changes

대화 밖에서 사용자가 파일을 수정했을 수 있으므로 예상 밖 변경을 보면 덮어쓰지 않고 intentional이라고 가정하거나 확인한다.

이는 일반적인 coding Skill에 적용할 가치가 높다.

## Router 중심 구조

대표 Skill 자체는 대부분 routing이다.

- create
- markup
- maps
- multimedia
- interactivity
- studio
- render
- captions
- SaaS
- docs
- upgrade

각 세부 영역을 별도 reference로 나눈다.

## Preview와 Render를 분리

사용자가 "make/create video"라고 했다고 바로 render하지 않는다.

기본은 interactive preview다.

명시적으로 render, export, MP4를 요청했을 때만 실제 render한다.

### 중요한 원리

**Expensive action requires stronger intent than preparation.**

prepare / preview와 execute / publish / render를 구분한다.

# 7. Microsoft Azure: Skill을 상태 머신으로 만든다

Published repository:
https://github.com/microsoft/azure-skills

Canonical source:
https://github.com/microsoft/GitHub-Copilot-for-Azure

대표:

- `azure-prepare`
- `azure-validate`
- `azure-deploy`

이 사례는 이번 추가 조사에서 가장 중요하다.

## 전체 workflow

azure-prepare → Approved plan → azure-validate → Validated + proof → azure-deploy

각 Skill이 전체 deploy 절차를 모두 수행하지 않는다.

## azure-prepare

핵심:

- `.azure/deployment-plan.md`를 실제 file artifact로 생성
- user approval
- infrastructure 생성
- destructive action은 ask_user
- validate 전에 status를 `Ready for Validation`
- deployment command는 직접 실행하지 않음

description에도 USE ONLY, DO NOT USE FOR, WHEN을 함께 둔다.

## azure-validate

prerequisite:

- plan 존재
- status Approved 이상

모든 검증이 pass해야 다음 단계로 진행한다.

## azure-deploy

prerequisite:

- plan 존재
- status `Validated`
- Validation Proof 존재

중요한 점은 deploy Skill 자신이 status를 Validated로 바꾸는 것을 금지한다는 것이다.

### Authority Separation

prepare owns preparation state  
validate owns validation authority  
deploy consumes validation proof

## 가장 중요한 최근 변경

2026-08-03 canonical source commit `97cd69e`에서 `azure-validate`의 inline 9-step table을 script driver로 교체했다.

이전:

- agent가 9개 step을 직접 기억
- status file도 직접 edit

변경 후:

workflow.ps1 / workflow.sh → 다음 action 출력 → agent 수행 → completed-step 전달 → script가 progress 기록

commit 설명에는 per-step tool call을 줄이고 progress를 script가 기록한다고 적혀 있다.

### 책에 추가할 매우 강한 사례

이것은 **Prose → Executable State Machine Graduation**의 실제 사례다.

반복 순서가 중요하고 상태 누락이 위험하면 prose checklist를 더 강하게 쓰는 것보다 state transition을 script가 소유하게 한다.

# 8. Prisma: 중복 router는 deprecated alias로 축소한다

Repository:
https://github.com/prisma/skills

## 2026-09-29 실제 refactor

기존에는 `prisma-orm-setup`과 `prisma-database-setup`이 둘 다 version을 감지하고 서로 routing했으며 description도 유사 prompt를 잡았다.

문제:

- responsibility duplication
- trigger collision
- version routing duplicated

해결:

- `prisma-orm-setup`을 single owner로 지정
- `prisma-database-setup`은 compatibility redirect로 축소

현재 deprecated Skill은 약 15줄이다.

description은 기존 integration이나 사용자가 명시적으로 옛 이름을 호출할 때만 사용하고 그 외에는 replacement를 선택하도록 한다.

body에는 setup recipe가 없다.

## 중요한 패턴

**Deprecated Skill Should Not Keep Competing Logic**

compatibility 때문에 옛 이름을 유지해야 해도:

- full workflow를 복제하지 않음
- 새 auto-routing 대상으로 경쟁하지 않음
- canonical Skill로 redirect

## Migration without forced upgrade

기존 application을 repair하기 위해 major upgrade를 선행 조건으로 강제하지 않는다.

즉 Skill이 "최신 버전"을 이유로 user task를 확대하지 않는다.

## Negative applicability

`prisma-upgrade-v7`은 MongoDB 프로젝트에 이 guide가 적용되지 않는다고 명확하게 둔다.

### 책에 추가할 패턴

- compatibility alias
- version-preserving repair
- negative applicability gate
- canonical router ownership

# 9. Firebase: repository-specific Skill은 정확한 convention을 담는다

Repository:
https://github.com/firebase/firebase-tools

대표:
`.agent/skills/firebase-tools-pr-review/SKILL.md`

2026-09-28 추가.

이 Skill은 일반적인 "좋은 TypeScript 코드" 설명보다 해당 repository의 실제 review rule을 많이 담는다.

예:

- enum보다 union literal
- null보다 undefined
- CLI startup에서 network/subprocess 금지
- public interface 기준 test
- mock teardown
- MCP schema는 실제 LLM API smoke test
- JSON mode에서 stdout은 machine-readable JSON only
- changelog format
- blocking vs `Nit:`/`Optional:` 구분

## 중요한 패턴

**Repository-local Skill earns specificity**

portable Skill에서는 지나친 repo-specific rule이 문제지만 이 Skill의 purpose 자체가 `firebase/firebase-tools` PR review이므로 구체적인 convention이 정당하다.

### 최근 변경

Skill 추가 직후 changelog rule을 실제 repo convention 변화에 맞춰 수정했다.

즉 repo-specific Skill은 codebase convention과 함께 versioned되어야 한다.

# 10. Sentry Skill Scanner: Skill을 공급망 입력물로 본다

Repository:
https://github.com/getsentry/skills

대표:
`skills/skill-scanner/SKILL.md`

## Static + semantic two-layer scan

1. bundled static scanner
2. agent가 intent/context 평가

정규식 match만으로 악성 판단하지 않는다.

security Skill에 "prompt injection" 문자열이 있는 것은 공격일 수도 있고 공격을 설명하는 문서일 수도 있으므로 주변 context를 읽는다.

## 검사 범위

- prompt injection
- malicious scripts
- excessive permissions
- secrets
- supply chain
- symlink escape
- frontmatter hooks
- npm lifecycle
- hidden image metadata
- config/memory poisoning
- unnecessary file/data access

## Least privilege

`allowed-tools`가 실제 body에서 필요한지 확인한다.

## Confidence

HIGH / MEDIUM / LOW로 나눈다. LOW theoretical best-practice는 finding으로 올리지 않는다.

### 최근 maintenance가 주는 교훈

2026-09-28 여러 Skill의 `allowed-tools`가 comma-separated였던 문제를 whitespace-separated로 변경했다.

Claude에서는 동작했지만 다른 loader는 `Read,`, `Grep,`를 unknown tool로 해석해 capability가 조용히 빠졌다.

즉 **Host-Tolerated Invalidity**의 실제 사례다.

한 runtime에서 "작동한다"가 spec-valid/portable을 의미하지 않는다.

## Outdated Skill 삭제

2026-08-19 `replay-ux-research` 삭제.

이유:

- outdated
- 가끔 불필요하게 auto-invoke

### 책에 추가할 강한 사례

**Outdated + Over-triggering = Delete, not Patch Forever**

# 11. Anthropic Frontend Design: default를 깨는 판단 규칙

Repository:
https://github.com/anthropics/skills

대표:
`skills/frontend-design/SKILL.md`

이 Skill은 deterministic workflow보다 judgment-heavy Skill의 사례다.

## Subject grounding

디자인하기 전에 product, audience, primary job을 구체화한다.

## Generated-default 회피

현재 Skill은 AI-generated UI에서 반복되는 여러 default cluster를 명시하지만, 사용자가 그 방향을 실제로 요청했다면 그대로 따르게 한다.

즉 anti-pattern이 absolute ban이 아니다.

## Plan → brief review → build → critique

코드 전에 color, type, layout, principles를 짧게 계획하고 이 선택이 해당 brief에 특화된 것인지 비슷한 prompt에도 똑같이 나올 default인지 self-review한다.

### 중요한 패턴

**Judgment Skill에는 binary rule보다 comparison criterion이 유용할 수 있다.**

"이 색 쓰지 마"가 아니라 "이 선택이 subject-specific인가 generic default인가?"를 판정하게 한다.

# 12. Matt Pocock의 grill-me: 작은 Skill이 orchestration alias가 될 수 있다

Repository:
https://github.com/mattpocock/skills

`grill-me`는 약 8줄이며 `disable-model-invocation: true`를 사용하고 body에서는 `grilling` Skill을 호출한다.

`grill-with-docs`도 약 8줄이며 `grilling`과 `domain-modeling` 두 Skill을 호출한다.

## 중요한 패턴

모든 Skill이 자체 workflow를 가져야 하는 것은 아니다.

**Composition Alias Skill**

사용자가 기억하기 좋은 entrypoint를 만들되:

- 실제 logic은 기존 canonical Skill에 남김
- 중복 workflow를 복사하지 않음
- manual-only로 accidental auto-trigger 방지

# 13. 업무형 Skill에서 추가로 확인된 규칙

## O1. State owner를 명확히 한다

특히 deployment/migration에서 한 Skill이 prepare, validate, deploy를 모두 소유하지 않는다.

## O2. Side effect는 intent threshold를 높인다

예:

- preview vs render
- prepare vs deploy
- review vs submit
- discover vs install

## O3. User artifact를 workflow state로 사용한다

예:

- `.azure/deployment-plan.md`
- validation proof
- plan/progress files

대화 내 hidden state보다 inspectable, reviewable, versionable하다.

## O4. Tool permission도 Skill 계약의 일부다

`allowed-tools`는 portability, least privilege, actual capability를 바꾼다.

## O5. Version strategy를 명시해야 한다

도구/API Skill은 최소 하나가 필요하다.

1. static snapshot + explicit version
2. live official docs
3. installed-version-matched docs
4. compatibility router

## O6. Deprecated entrypoint는 logic owner가 되면 안 된다

alias는 redirect만 한다.

## O7. No-skill / stop / handoff가 정상 상태여야 한다

모든 요청을 현재 Skill이 끝까지 소유하려 하지 않는다.

# 14. 최근 3개월 실제 변경에서 반복된 maintenance 유형

## M1. Duplicate routing consolidation

Prisma: 두 setup Skill의 유사 description / routing을 하나로 합침.

## M2. Prose workflow → script state driver

Microsoft Azure Validate: 9-step prose → workflow script.

## M3. Stale Skill deletion

Sentry: outdated + unnecessary invocation Skill 삭제.

## M4. Spec portability fix

Sentry: Claude가 관대하게 읽던 comma-separated `allowed-tools`를 표준에 맞게 수정.

## M5. Canonical command deduplication

Vercel `find-skills`: alias command를 제거하고 하나의 canonical command만 문서화.

## M6. User-change preservation

Remotion: agent 외부에서 바뀐 파일을 surprise로 인식하고 덮어쓰지 않음.

## M7. Version-matched instruction retrieval

agent-browser: 상세 workflow를 installed CLI에서 제공.

# 15. 첫 조사와 합쳤을 때 더 강해진 책의 원칙

## Principle A — Skill은 문서가 아니라 작은 protocol이다

특히 업무형 Skill은 precondition, state, authority, transition, evidence, handoff를 가진다.

Skill = Trigger + Preconditions + Procedure + Side-effect policy + Evidence + Handoff

## Principle B — "언제 멈추는가"를 써야 한다

Skill author는 보통 "언제 사용"만 쓴다.

하지만 다음도 똑같이 중요하다.

- 언제 다른 Skill로 넘기는가
- 언제 user approval을 기다리는가
- 언제 아무 작업도 하지 않는가
- 언제 validation failure로 stop하는가
- 언제 compatibility alias가 redirect만 하는가

## Principle C — Workflow state가 중요하면 prose에만 두지 않는다

prose checklist → persistent artifact → script / validator → hook / permission / CI

Azure Validate는 이 ladder의 좋은 실사례다.

## Principle D — Freshness strategy는 Skill 설계 항목이다

framework, cloud, CLI, API Skill에서는 "이 지침은 6개월 뒤 어떻게 최신 상태를 유지하는가?"에 답해야 한다.

## Principle E — Compatibility는 복제를 의미하지 않는다

old entrypoint → tiny redirect → canonical owner가 낫다.

# 16. 책에 추가할 새 smell 후보

## S15. Workflow Ownership Collision

둘 이상의 Skill이 같은 prompt와 state transition을 소유.

## S16. Unowned State Transition

어떤 Skill도 status 변경 권한을 명확히 소유하지 않음.

## S17. Side-Effect Intent Collapse

"만들어줘"와 "배포해줘"를 같은 trigger로 취급.

## S18. Stale Embedded Command Surface

빠르게 변하는 CLI command를 static Skill body에 대량 복사.

## S19. Compatibility Logic Duplication

deprecated alias가 canonical Skill과 같은 full workflow를 계속 보유.

## S20. Host-Tolerated Invalidity

한 host가 느슨하게 받아줘서 잘못된 metadata가 발견되지 않고 다른 loader에서 silent failure.

## S21. Discovery Without Abstention

router가 적합한 Skill이 없어도 무엇인가 추천/호출.

## S22. User-Change Clobbering

agent가 대화 밖에서 발생한 user edit을 자기 예상과 다르다는 이유로 덮어씀.

# 17. 책 목차에 미치는 영향

## 7장 Description

추가:

- positive trigger
- negative applicability
- handoff
- abstention
- deprecated alias
- compatibility redirect

## 8장 Skill Body

추가:

- precondition
- state owner
- side-effect gate
- user approval
- exit/handoff

## 9장 References / Scripts

추가:

- version-coupled instruction
- live source vs installed-version source
- executable state driver

## 10장 Prose → Enforcement

Azure Validate를 대표 사례로 사용:

9-step Markdown → script-driven state machine

## 17장 Instruction Debt

추가 대표 사례:

- Sentry stale Skill deletion
- Prisma duplicate router consolidation
- Sentry host-tolerated invalid metadata
- stale embedded command surface

# 18. 결론

두 차례의 유명 Skill 조사를 합치면 단순한 "Skill writing tips"보다 강한 구조가 보인다.

방법론형 Skill의 핵심은:

행동 규율 + rationalization 방지 + 검증

업무형 Skill의 핵심은:

trigger + precondition + state ownership + side-effect policy + evidence + handoff + freshness

따라서 책에서 Skill을 다음처럼 정의하는 편이 더 정확하다.

> **SKILL.md는 특정 작업을 설명하는 Markdown 파일이 아니라, 에이전트가 언제 들어오고, 무엇을 확인하고, 무엇을 수행하고, 어떤 증거를 남기고, 어디에서 멈추거나 다음 Skill로 넘길지를 정의하는 작은 실행 프로토콜이다.**
