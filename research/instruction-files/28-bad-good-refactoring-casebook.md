# Bad → Good Instruction Refactoring Casebook

기준일: 2026-09-30

## 목적

공식 문서와 실제 공개 저장소에서 반복해서 관찰한 문제를 합성한 **교육용 composite 사례**다.

특정 저장소의 원문을 그대로 옮긴 예제가 아니다.

목표는 독자가 다음을 한 번에 볼 수 있게 하는 것이다.

- 무엇이 왜 나쁜가
- 어느 파일로 옮겨야 하는가
- prose를 어디까지 줄여야 하는가
- 무엇을 validator/script/Hook으로 승격해야 하는가
- trigger와 side-effect boundary를 어떻게 분리해야 하는가

---

# Case 1. 800줄 CLAUDE.md

## Before

가상의 repository root:

```text
CLAUDE.md
```

내용:

- 프로젝트 소개 80줄
- 모든 package 설명 120줄
- Java test convention 100줄
- frontend test convention 90줄
- DB migration 절차 80줄
- release 절차 100줄
- PR 작성법 60줄
- formatting rule 50줄
- 현재 library version 목록 60줄
- "항상 테스트", "반드시 lint" 등 반복 지시
```

문제:

- 모든 작업에 모든 지침이 로드됨
- path-local rule이 root에 있음
- procedure가 standing context에 있음
- current version snapshot이 stale해짐
- formatter/linter가 잡을 일을 prose가 반복
- root file이 source of truth인지 handbook인지 불명확

## Failure mode

작은 frontend typo 수정에서도:

- DB migration rule
- backend test rule
- release process
- package inventory

까지 상시 context에 섞인다.

문제는 단순 token 수가 아니다.

관련 없는 규칙이 많으면:

- 무엇이 이번 작업에 중요한지 약해지고
- 모델이 과도한 verification을 할 수 있으며
- 동일 정책이 여러 위치에 중복될 가능성이 커진다.

## Good architecture

```text
CLAUDE.md
├─ repo-wide invariants only
├─ build/test entry commands
└─ routing pointers

backend/
└─ AGENTS.md

frontend/
└─ AGENTS.md

.claude/rules/
├─ java-tests.md
└─ frontend-tests.md

skills/
├─ db-migration/
│  └─ SKILL.md
└─ release/
   └─ SKILL.md

scripts/
└─ validate-instructions.py

lint / formatter / CI
└─ deterministic style + structural checks
```

## After: root

```md
# Repository Instructions

Use `pnpm` for JavaScript work and `./gradlew` for backend work.

Read the nearest scoped instruction before editing a subsystem:

- `backend/AGENTS.md`
- `frontend/AGENTS.md`

Database schema changes use the `db-migration` Skill.
Release work uses the `release` Skill.

Do not duplicate formatter or lint rules here. Run the repository checks relevant
to the files you changed.
```

## Why this is better

- root owns repo-wide facts
- subsystem files own local invariants
- procedures become Skills
- machine-checkable rules leave prose
- stale version inventory can come from package/config files directly

## Related real-world patterns

- `pinchen147/system-design-skill`
- `contentstack-management-dotnet`
- `jinganix/admin-starter`
- nested AGENTS case studies
- pstack "encode lessons in structure"

---

# Case 2. Broad auto-trigger Skill

## Before

```yaml
---
name: code-helper
description: Use this whenever you are coding, fixing bugs, reviewing code,
refactoring, testing, planning, or working on software.
---
```

body:

```md
Always think carefully.
Always write tests.
Always review your work.
Always use best practices.
```

## Failure mode

거의 모든 software task가 이 Skill을 trigger할 수 있다.

문제:

- adjacent Skill과 collision
- default model capability를 중복
- 실제 workflow가 없음
- 완료/evidence 정의 없음
- negative boundary 없음

## Good decomposition

### `bug-fix`

```yaml
---
name: bug-fix
description: Diagnose and fix a reproducible software defect. Use when the user
reports incorrect behavior, a failing regression, or a specific defect to repair.
Do not use for feature requests, architecture-only refactors, or general review.
---
```

body:

```md
1. Reproduce or identify the failing behavior.
2. Locate the smallest responsible code path.
3. Add or identify a test that fails for the reported defect.
4. Make the smallest correction that addresses the cause.
5. Run the focused test and the repository checks relevant to the changed files.

Done when the reported behavior is fixed and the regression test passes.
```

### `feature`

separate Skill:

- trigger: new capability
- boundary: not defect repair
- procedure: requirements → implementation → focused verification

## Improvement

Before:

```text
software task
→ code-helper
```

After:

```text
defect
→ bug-fix

new behavior
→ feature

review only
→ review

none match
→ no Skill
```

## Add trigger tests

Positive:

- "로그인 버튼 누르면 500 나는데 고쳐줘"
- "이 failing test regression을 수정해줘"

Negative:

- "사용자 초대 기능 추가해줘"
- "이 PR 리뷰해줘"
- "폴더 구조만 정리하고 싶어"

Routing pair:

- bugfix vs feature
- bugfix vs review

## Related real-world patterns

- duthaho/skillhub routing pairs
- Firebase activation-eval description refactor
- Sentry stale over-triggering Skill deletion
- Prisma duplicate router consolidation

---

# Case 3. One Skill owns prepare + validate + deploy

## Before

```yaml
---
name: deploy-app
description: Set up, validate, and deploy the application.
---
```

body:

```md
1. Create deployment config.
2. Check it.
3. Deploy.
4. Mark deployment successful.
```

## Failure mode

한 Skill이:

- preparation
- validation authority
- deployment mutation
- final status

를 모두 소유한다.

잠재적 우회:

- 실제 validation 없이 status만 "validated"로 변경
- 사용자가 준비만 요청했는데 deploy까지 수행
- deploy 실패 후 state가 success로 남음
- 승인 경계 없음

## Good decomposition

### prepare

```text
input
→ plan artifact
→ user review
→ Ready for Validation
```

### validate

```text
Approved plan
→ deterministic checks
→ validation proof
→ Validated
```

### deploy

```text
Validated + proof + explicit deploy intent
→ deploy
→ deployment evidence
```

## State ownership

| State | Owner |
| --- | --- |
| Draft | prepare |
| Approved | human |
| Ready for Validation | prepare |
| Validated | validate |
| Deployed | deploy/runtime evidence |

## Better contract

`deploy` Skill:

```md
Preconditions:

- deployment plan exists
- plan status is `Validated`
- validation proof is present
- the user explicitly asked to deploy

Do not change a plan to `Validated`. Validation authority belongs to the
validation workflow.

After deployment, record the command/result or deployment identifier as evidence.
```

## If state order keeps failing

prose table을 더 길게 쓰지 않는다.

다음으로 승격:

```text
workflow script
→ next valid transition
→ state file update
→ evidence check
```

## Related real-world patterns

- Microsoft Azure `prepare → validate → deploy`
- Azure Validate 9-step prose → workflow script
- Remotion preview vs render
- safety-gate overcorrection cases

---

# Case 4. SKILL.md contains a full CLI manual

## Before

```md
# Tool Skill

Current version: 4.8.2

## Every command

tool login ...
tool init ...
tool create ...
tool update ...
tool delete ...
tool export ...
tool sync ...
tool inspect ...
tool migrate ...

## Every option

--foo
--bar
--baz
...
```

600줄.

## Failure mode

CLI 4.9가 나오면:

- SKILL.md
- CLI `--help`
- official docs

가 서로 다른 truth가 될 수 있다.

### Smell

Cached CLI Manual.

## Good version A: installed runtime is source of truth

```md
Use `tool --help` and `tool <command> --help` for complete syntax.

This Skill owns:

- how to select the right command
- prerequisites
- dangerous-operation gates
- how to inspect output
- completion criteria

Do not duplicate the complete option catalog here.
```

## Good version B: installed-version Skill content

```text
static SKILL.md
→ tool skills get core
→ version-matched instructions
```

## Good version C: live source + dated fallback

```md
Read the current official version page first.

Fallback snapshot: 2026-09-29, version X.
Use the fallback only when live verification is unavailable.
Treat a fallback older than the product's expected release interval as suspect.
Never invent a newer version number.
```

## Related real-world patterns

- Firecrawl `--help`
- agent-browser installed-version Skill content
- Cloudflare retrieval-first
- Stripe dated fallback snapshot
- Expo version-specific migration references

---

# Case 5. "Always run tests" with hidden cost

## Before

```md
After every change, ALWAYS run the full acceptance test suite.
```

## Failure mode

acceptance test가:

- real cloud resources 생성
- 비용 발생
- live credential 사용
- 40분 이상 실행
- interruption 시 resource leak

을 일으키는 경우 이 한 문장은 위험하다.

## Good contract

```md
For ordinary code changes, run the focused unit/static checks first.

Acceptance tests create real infrastructure and may incur cost.

Before running them:

1. Confirm the credentials target a test account.
2. Use invocation-local environment variables for secrets.
3. Run only the affected acceptance tests unless the user requested full regression.
4. Set an explicit timeout.
5. If interrupted, check whether provider sweepers/cleanup are required.

Do not run production-account acceptance tests without explicit user approval.
```

## Better evidence ladder

```text
static validation
→ focused unit test
→ integration test
→ acceptance test
→ production mutation
```

강한 verification을 무조건 먼저 수행하지 않는다.

가장 싼 충분한 검증부터 올라간다.

## Test validity

test가 suspiciously pass하면:

```text
temporarily perturb expected condition
→ verify RED
→ restore
→ verify GREEN
```

## Related real-world patterns

- HashiCorp acceptance-test Skill
- Superpowers RED/GREEN discipline
- Firecrawl cheapest sufficient primitive
- targeted validation in Firebase/Cloudflare

---

# Case 6. Safety gate is prose only

## Before

```md
IMPORTANT: Never publish without user approval.
```

그리고 같은 agent가 직접:

```text
gh pr ready
gh pr merge
publish script
release API
```

를 호출할 수 있다.

## Failure mode

Skill을 우회한 tool call에는 prose policy가 적용되지 않을 수 있다.

또 명령 하나만 막으면 equivalent bypass가 남을 수 있다.

## Good architecture

```text
intent rule in Skill
+
permission/tool policy
+
Hook matcher
+
deny test
+
legitimate near-match test
```

예:

```md
Publishing requires explicit approval from the user.

Drafting, local validation, and creating a draft PR do not count as publishing.
```

Hook:

- publish-class command 차단
- explicit approval token/state 확인
- equivalent bypass command 포함

Tests:

- blocked publish command
- blocked equivalent alias
- allowed draft PR
- allowed local preview
- allowed status/read operation

## 중요한 점

"더 많이 막는 것"이 목적이 아니다.

실제 위험 경계에만 gate를 둔다.

## Related real-world patterns

- dotfiles checkpoint overcorrection reversal
- `gh pr ready` / merge bypass handling
- Hook semantic drift 사례
- DeepRefine prose approval gate

---

# Case 7. Deprecated Skill keeps full logic

## Before

```text
prisma-old-setup/SKILL.md
  full version detection
  full setup
  full troubleshooting

prisma-new-setup/SKILL.md
  full version detection
  full setup
  full troubleshooting
```

description도 거의 동일.

## Failure mode

- trigger collision
- bugfix를 두 군데 해야 함
- 서로 다른 version policy
- 어느 Skill이 canonical owner인지 모름

## Good

old:

```yaml
---
name: old-setup
description: Compatibility alias for existing users that explicitly invoke the
old name. Do not auto-select for new setup work; use `new-setup`.
---
```

body:

```md
This entrypoint is retained for compatibility.

Load and follow `../new-setup/SKILL.md`.
```

new:

- single owner of version detection
- single setup workflow
- single source of references

## Related real-world patterns

- Prisma setup consolidation
- Matt Pocock composition alias
- canonical router ownership

---

# Case 8. Candidate Skill eval is contaminated

## Before

개발 중인 local Skill:

```text
repo/plugins/foo/skills/bar/SKILL.md
```

이미 사용자 환경에 installed Skill:

```text
~/.plugins/foo/skills/bar/SKILL.md
```

trigger eval은 단순히:

```text
"bar Skill was invoked" = pass
```

로 판단.

## Failure mode

모델이 installed Skill을 골라도 evaluator가 pass라고 기록한다.

즉 candidate description을 평가하지 않았다.

## Good eval isolation

trigger eval 전에:

1. candidate Skill identity 확인
2. published/installed duplicate 비활성화
3. available Skill inventory 기록
4. fresh session
5. activation trace에서 exact candidate source 확인
6. prompt corpus 고정
7. candidate 변경 후 동일 corpus 반복

## Evaluator permissions

eval harness도 최소 권한.

예:

- temp workspace만 Write
- candidate repo는 Read
- 필요한 runner script만 Bash
- global config 변경은 explicit step

## Related real-world patterns

- Expo Skill eval
- Sentry/skillhub trigger eval
- cross-host pilot 설계

---

# Case 9. Latest docs overwrite project reality

## Before

```md
Always use the latest framework/API version.
If a newer type package exists, update the code to match it.
```

## Failure mode

기존 project가:

- pinned runtime
- compatibility date
- old supported API
- stable version

에 의도적으로 묶여 있을 수 있다.

latest 문서만 보면 현재 코드를 잘못된 것으로 오판할 수 있다.

## Good freshness hierarchy

```text
1. user-specified target
2. project configured target
3. installed/generated types/schema
4. current official source
5. dated fallback snapshot
```

각 source의 역할을 다르게 둔다.

예:

- 기존 code review → project target 기준
- 새 project → current recommended target
- upgrade task → user target 또는 verified current
- live lookup 실패 → fallback + uncertainty

## Related real-world patterns

- Cloudflare compatibility date
- Stripe upgrade target selection
- Expo SDK migration
- Prisma version-preserving repair

---

# Case 10. Canonical config is copied into prose

## Before

```md
Use brand color #0057ff.
Use Inter.
Use 12px radius.
Use 16px spacing.
```

동시에:

```text
design-system.json
```

에도 같은 값이 있음.

## Failure mode

디자인 시스템이 바뀌면 prose가 stale.

같은 문제는 다음에도 생긴다.

- generated `Env` type + Skill manual
- DB schema + Skill copy
- CI threshold + CLAUDE.md copy
- API schema + README/Skill copy

## Good

```md
Read the project's design system before generating UI.

Do not duplicate project-level color, typography, or radius tokens in the
generation prompt. The design system is the source of truth.

This Skill should describe layout, content, interaction, and task-specific
constraints.
```

## Related real-world patterns

- Google Stitch design-system ownership
- Cloudflare generated binding types
- canonical source + scoped summary pattern

---

# Case 11. Domain Skill duplicates generic engineering process

## Before

`workers-best-practices`:

```md
Think step by step.
Read the code.
Make a plan.
Use clean code.
Keep functions small.
Write tests.
Review your changes.
```

## Failure mode

이런 내용은 domain-specific Skill이 없어도 모델/standing instruction이 이미 수행할 수 있다.

항상 loaded body를 차지하지만 Workers에서만 필요한 정보는 아니다.

## Good

entrypoint:

```md
Prefer project-installed versions and generated types over memory.
Retrieve current Cloudflare documentation for runtime/config/API claims.

Flag these Workers-specific failures:
- unbounded response buffering
- request-global mutable state
- unmanaged async lifetime
- hand-written Env that drifts from bindings
...
```

generic planning/review는 다른 layer에 맡긴다.

## Related real-world patterns

- Cloudflare generic review procedure removal
- OpenAI instruction-diet guidance
- model-upgrade audits

---

# Case 12. No completion bound

## Before

```md
1. Search.
2. Analyze.
3. Improve the result.
4. Continue until it looks good.
```

## Failure mode

- 언제 끝나는지 불명확
- 반복 search
- over-verification
- unnecessary tool calls

## Good

```md
Done when:
- the requested source set has been collected,
- the answer cites the saved evidence,
- no unresolved blocking source gap remains.
```

또는 narrow command Skill:

```md
Done when the command exits successfully and the expected output file exists.
```

## Related real-world patterns

- Firecrawl one `Done when`
- verification-before-completion
- artifact-backed validation

---

# 13. 리팩터링 decision tree

문장을 발견했을 때 다음 순서로 본다.

## Q1. 모든 작업에서 필요한가?

- Yes → root CLAUDE/AGENTS 후보
- No → Q2

## Q2. 특정 path에서만 필요한가?

- Yes → nested AGENTS / path Rule
- No → Q3

## Q3. 특정 task/procedure에서만 필요한가?

- Yes → Skill
- No → Q4

## Q4. 기계적으로 참/거짓 판정 가능한가?

- Yes → schema / type / lint / CI / Hook / script
- No → prose instruction

## Q5. 값이 자주 바뀌는가?

- Yes → canonical runtime/config/live source에서 조회
- No → static reference 가능

## Q6. side effect가 큰가?

- Yes → explicit intent + permission + evidence + cleanup
- No → normal execution contract

---

# 14. 리팩터링 완료 기준

좋은 리팩터링은 단순히 줄 수가 감소한 상태가 아니다.

다음이 만족되어야 한다.

- root context에서 unrelated instruction이 빠짐
- trigger와 adjacent negative가 구분됨
- state owner가 겹치지 않음
- deterministic rule이 prose에만 남지 않음
- canonical source가 하나로 줄어듦
- high-side-effect action의 intent threshold가 높아짐
- completion evidence가 존재
- compatibility alias가 canonical logic을 복제하지 않음
- live/cached version strategy가 명확
- 변경 후 regression을 확인할 수 있는 validator/eval surface가 생김

---

# 15. 책 13장에 바로 사용할 구성

`나쁜 지침 파일 리팩터링` 장은 하나의 거대한 예제보다 다음 순서가 더 실전적이다.

1. 거대한 root instruction
2. broad Skill trigger
3. procedure/state collision
4. cached CLI manual
5. prose-only safety gate
6. compatibility duplication
7. eval contamination
8. freshness conflict
9. duplicated canonical config
10. missing completion bound

마지막에 하나의 repository를 합성해서 전체 구조를 보여준다.

```text
CLAUDE.md
backend/AGENTS.md
frontend/AGENTS.md
.claude/rules/
skills/
scripts/
hooks/
CI
```

독자는 "문장을 더 잘 쓰는 법"보다:

> **어떤 지식을 어디로 옮겨야 하는가**

를 배우게 된다.
