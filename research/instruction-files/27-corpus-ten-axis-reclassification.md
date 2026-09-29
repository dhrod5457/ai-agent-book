# 공개 지침 Corpus 10축 재분류

기준일: 2026-09-30

기준 corpus:
[11-public-instruction-corpus.md](11-public-instruction-corpus.md)

## 목적

기존 35개 공개 지침 파일을 최근 조사에서 수렴한 10개 축으로 다시 본다.

이 표는 점수표가 아니다.

특히 `CLAUDE.md`, `AGENTS.md`, path Rule은 항상-on 또는 path-scoped standing instruction이므로 `SKILL.md`의 trigger/state/handoff와 동일한 방식으로 평가하면 안 된다.

표기:

- **●** — 파일에서 명시적이고 강하게 관찰됨
- **◐** — 일부 또는 간접적으로 관찰됨
- **○** — 현재 관찰 범위에서는 뚜렷하지 않음
- **—** — 파일 유형/목적상 직접 적용하기 어려움

10개 축:

1. **T Trigger** — 언제 적용/선택되는가
2. **B Boundary** — 언제 적용되면 안 되는가
3. **P Preconditions** — 시작 전 필요한 조건
4. **S State / Authority** — 상태와 상태 변경 권한
5. **R Procedure** — 실행 순서/행동
6. **X Side effects / Permissions** — mutation, 권한, 비용, 승인
7. **E Evidence** — 완료/정확성 증거
8. **H Handoff** — stop, fallback, 다른 Skill/문서로 이관
9. **F Freshness / Canonical source** — 최신성/source of truth 전략
10. **M Maintenance / Eval** — validator, eval, 등록, 갱신 전략

---

## 1. 전체 matrix

| # | 사례 | 유형 | T | B | P | S | R | X | E | H | F | M |
| ---: | --- | --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | getsentry/skills `AGENTS.md` | AGENTS | — | ◐ | ◐ | — | ◐ | ◐ | ● | ● | ◐ | ● |
| 2 | m98/fluent `CLAUDE.md` | CLAUDE | — | ○ | ◐ | — | ● | ◐ | ◐ | ◐ | ○ | ○ |
| 3 | novotnyllc/dotnet-artisan `AGENTS.md` | AGENTS | — | ◐ | ◐ | — | ◐ | ◐ | ● | ● | ● | ● |
| 4 | duthaho/skillhub `AGENTS.md` | AGENTS | — | ● | ◐ | — | ● | ◐ | ● | ● | ● | ● |
| 5 | pinchen147/system-design-skill `CLAUDE.md` | CLAUDE | — | ● | — | — | ◐ | — | ● | ● | ◐ | ● |
| 6 | contentstack-management-dotnet `AGENTS.md` | AGENTS | — | ◐ | ◐ | — | ◐ | — | ● | ● | ◐ | ◐ |
| 7 | green-stack-starter `CLAUDE.md` | CLAUDE | — | ◐ | ◐ | — | ◐ | — | ◐ | ● | ◐ | ◐ |
| 8 | panda-pulse `CLAUDE.md` | CLAUDE | — | ◐ | ◐ | — | ● | — | ○ | ● | ○ | ○ |
| 9 | code-foundations `CLAUDE.md` | CLAUDE | — | ◐ | ◐ | ◐ | ● | ◐ | ◐ | ● | ◐ | ◐ |
| 10 | bonfire `AGENTS.md` | AGENTS | — | ● | ◐ | ◐ | ● | ● | ● | ● | ◐ | ◐ |
| 11 | ivanrvpereira/.agents `AGENTS.md` | AGENTS | — | ● | ◐ | — | ● | ◐ | ◐ | ● | ◐ | ◐ |
| 12 | tackline `CLAUDE.md` | CLAUDE | — | ● | ● | ◐ | ● | ◐ | ◐ | ● | ◐ | ◐ |
| 13 | claude-lens `CLAUDE.md` | CLAUDE | — | ● | ◐ | — | ● | — | ◐ | ● | ● | ◐ |
| 14 | flowstate `CLAUDE.md` | CLAUDE | — | ● | ◐ | — | ◐ | ◐ | ● | ● | ◐ | ● |
| 15 | codingagentsystem/cas `CLAUDE.md` | CLAUDE | — | ◐ | ● | ● | ● | ● | ◐ | ● | ◐ | ◐ |
| 16 | claude-ansible-skills `CLAUDE.md` | CLAUDE | — | ● | ◐ | — | ◐ | ◐ | ● | ● | ● | ● |
| 17 | bug-hunt `SKILL.md` | Skill | ● | ● | ● | ◐ | ● | ◐ | ● | ● | ◐ | ◐ |
| 18 | lastXdays-skill `SKILL.md` | Skill | ● | ◐ | ● | — | ● | ● | ● | ◐ | ● | ◐ |
| 19 | claude-vision `SKILL.md` | Skill | ● | ● | ● | — | ● | ● | ● | ◐ | ◐ | ◐ |
| 20 | re-skill `SKILL.md` | Skill | ● | ◐ | ● | ● | ● | ● | ● | ● | ● | ◐ |
| 21 | opencode-froggy `AGENTS.md` | AGENTS | — | ○ | ◐ | — | ● | ◐ | ● | ◐ | ○ | ○ |
| 22 | yoink `AGENTS.md` | AGENTS | — | ○ | ◐ | — | ● | ◐ | ● | ◐ | ○ | ○ |
| 23 | admin-starter `AGENTS.md` | AGENTS | — | ● | ◐ | — | ◐ | — | ● | ● | ● | ◐ |
| 24 | peepshow `AGENTS.md` | AGENTS | ● | ● | ◐ | — | ● | ◐ | ◐ | ● | ◐ | ◐ |
| 25 | skill-address-pr-review `SKILL.md` | Skill | ● | ● | ● | ◐ | ● | ● | ● | ● | ◐ | ◐ |
| 26 | claude-dynamic-workflows-codex `SKILL.md` | Skill | ● | ◐ | ● | ● | ● | ● | ◐ | ◐ | ◐ | ○ |
| 27 | Claude-Code-Wrapped-Skill `SKILL.md` | Skill | ● | ● | ● | — | ● | ● | ● | ◐ | ◐ | ◐ |
| 28 | DeepRefine-Skill `SKILL.md` | Skill | ● | ● | ● | ● | ● | ● | ● | ● | ◐ | ◐ |
| 29 | jobclaw `SKILL.md` | Skill | ● | ● | ● | ◐ | ● | ◐ | ● | ● | ◐ | ◐ |
| 30 | afsim-skill `SKILL.md` | Skill | ● | ◐ | ◐ | — | ● | ◐ | ◐ | ● | ● | ◐ |
| 31 | daxue-zhidao `SKILL.md` | Skill | ● | ● | ◐ | — | ◐ | ◐ | ◐ | ● | ● | ● |
| 32 | star-trek-voice-clone `SKILL.md` | Skill | ● | ◐ | ● | — | ● | ● | ● | ◐ | ○ | ○ |
| 33 | admin-starter `java-tests.mdc` | Rule | ● | ● | ◐ | — | ● | — | ● | ● | ● | ◐ |
| 34 | admin-starter `frontend-tests.mdc` | Rule | ● | ● | ◐ | — | ● | — | ● | ● | ● | ◐ |
| 35 | green-stack `workspace-expo-dependencies.mdc` | Rule | ● | ● | ● | — | ● | ● | ● | ● | ● | ◐ |

---

# 2. 이 matrix에서 바로 보이는 것

## 2.1 Standing instruction과 Skill은 구조가 다르다

`CLAUDE.md`, `AGENTS.md`는 T가 대부분 `—`다.

이것은 trigger가 나쁘다는 뜻이 아니다.

이 파일들은 대개:

- repository root
- directory scope
- host scope

자체가 activation 조건이기 때문이다.

따라서 standing instruction의 핵심 축은 다음이다.

- Boundary
- Procedure
- Handoff
- Freshness
- Maintenance

반면 Skill은:

- Trigger
- Preconditions
- Procedure
- Evidence
- Handoff

가 더 중요하다.

즉 하나의 checklist로 모든 instruction file을 평가하면 안 된다.

---

# 3. 파일 유형별 핵심 축

## CLAUDE.md / AGENTS.md

우선 질문:

1. 이 파일이 소유하는 지식은 무엇인가?
2. repo-wide가 아닌 규칙이 섞였는가?
3. procedure를 Skill로 내릴 수 있는가?
4. 특정 path 규칙을 nested file/Rule로 내릴 수 있는가?
5. canonical source를 중복하고 있지 않은가?
6. stale snapshot이나 broken reference가 있는가?
7. 더 강한 validator/Hook이 소유해야 할 규칙이 있는가?

핵심 위험:

- Global Handbook Bloat
- Always-Read Cascade
- Duplicate Canonical Rules
- Snapshot Freshness Debt
- Stale Instruction Reference

## Path Rule

우선 질문:

1. glob/path가 실제 필요한 파일만 잡는가?
2. parent/root rule과 중복되는가?
3. local rule이 canonical source를 가리키는가?
4. mechanically checkable rule을 prose로만 쓰고 있지 않은가?

핵심 위험:

- scope overreach
- parent-child duplication
- matcher drift
- duplicated threshold

## SKILL.md

우선 질문:

1. 무엇이 trigger하는가?
2. 인접 요청에서 abstain하는가?
3. 시작 조건은 무엇인가?
4. side effect 전에 어떤 approval/evidence가 필요한가?
5. 완료는 무엇으로 증명하는가?
6. 언제 다른 Skill/tool/human으로 넘기는가?
7. 바뀌는 사실은 어디서 읽는가?
8. 어떤 eval/feedback이 이 Skill을 유지하는가?

핵심 위험:

- Broad Trigger
- Trigger Collision
- Workflow Ownership Collision
- Side-Effect Intent Collapse
- Cached CLI Manual
- Missing Completion Bound

---

# 4. 35개 corpus를 다시 보면 가장 강한 사례군

## A. Scope / routing이 강한 사례

- `pinchen147/system-design-skill`
- `contentstack-management-dotnet`
- `jinganix/admin-starter`
- `sai-7i/daxue-zhidao`
- `t0mtaylor/peepshow`

공통점:

- root를 router로 사용
- local/canonical detail로 handoff
- 적용/비적용 경계를 드러냄

## B. Deterministic enforcement가 강한 사례

- `duthaho/skillhub`
- `getsentry/skills`
- `pinchen147/system-design-skill`
- `green-stack` path Rule

공통점:

- prose와 validator/script 역할을 나눔
- registration/reference/eval을 maintenance surface로 봄

## C. Operational contract가 강한 사례

- `bug-hunt`
- `re-skill`
- `skill-address-pr-review`
- `DeepRefine`
- `jobclaw`

공통점:

- input/precondition
- ordered procedure
- output/evidence
- 일부 state/approval

## D. instruction debt 관찰에 좋은 사례

- `panda-pulse`: stale reference
- `claude-dynamic-workflows-codex`: runtime-root bloat
- `code-foundations`: large standing context
- `cas`: product/manual/instruction 혼합
- `afsim`: deep disclosure chain 연구 후보

---

# 5. 기존 corpus의 빈 축

기존 35개 corpus는 다음 축의 실사례가 상대적으로 약했다.

- state authority
- explicit side-effect policy
- live freshness strategy
- eval isolation
- deletion/retirement

그래서 최근 유명/공식 Skill 추가 조사에서 다음 사례가 중요해졌다.

- Microsoft Azure: state authority
- Remotion: preview vs render
- agent-browser: installed-version content
- Cloudflare: retrieval-first
- Stripe: dated fallback snapshot
- Expo: eval isolation
- Sentry: stale Skill deletion
- Prisma: deprecated alias → redirect

즉 초기 35개 corpus와 최근 vendor corpus는 서로 대체 관계가 아니라 보완 관계다.

---

# 6. 10축 모델을 점수화하지 않는 이유

이 10축을 10점 만점 score로 만들지 않는다.

이유:

- 모든 Skill에 persistent state가 필요한 것은 아니다.
- 모든 Rule에 handoff가 필요한 것은 아니다.
- manual-only Skill은 auto-trigger precision이 핵심이 아니다.
- read-only formatter Skill과 cloud deploy Skill의 side-effect 기준은 다르다.
- static domain knowledge와 fast-moving CLI의 freshness 요구가 다르다.

따라서 올바른 사용법은:

> 결여된 축을 무조건 채우는 것이 아니라, **해당 Skill의 failure mode에 필요한 축이 빠졌는지** 본다.

---

# 7. 유형별 최소 Review Contract

## Standing instruction 최소 contract

- ownership
- scope
- canonical source
- routing/handoff
- mechanically enforceable rule 분리
- stale reference 검사

## Path Rule 최소 contract

- precise matcher
- local invariant
- canonical reference
- conflict/precedence 고려
- deterministic checker 연결

## Auto-trigger Skill 최소 contract

- positive trigger
- adjacent negative boundary
- precondition
- observable completion
- fallback/handoff
- freshness strategy
- trigger regression eval

## Manual-only Skill 최소 contract

- discoverable name/description
- argument contract
- procedure
- side-effect warning
- completion/evidence
- failure/retry behavior

## High-side-effect Skill 추가 contract

- explicit intent/approval
- state owner
- permission scope
- cost/security implication
- failure cleanup
- mutation evidence

---

# 8. 책에서 사용할 10축 진단 질문

1. **Trigger** — 이 지침은 정확히 언제 활성화되는가?
2. **Boundary** — 가장 헷갈리는 인접 요청에서 언제 활성화되면 안 되는가?
3. **Preconditions** — 실행 전에 반드시 확인해야 하는 상태는 무엇인가?
4. **State** — workflow state가 있다면 누가 읽고 누가 바꿀 수 있는가?
5. **Procedure** — 어떤 순서가 결과에 실제 영향을 주는가?
6. **Side effects** — 비용·mutation·권한·승인이 필요한 행동은 무엇인가?
7. **Evidence** — 완료/정확성을 self-report가 아닌 무엇으로 증명하는가?
8. **Handoff** — 언제 멈추고 다른 Skill/tool/human에게 넘기는가?
9. **Freshness** — 바뀔 수 있는 사실의 canonical source는 무엇인가?
10. **Maintenance** — 어떤 failure/eval/feedback이 이 지침을 수정하거나 삭제하게 하는가?

---

# 9. 결론

초기 corpus는 파일 길이와 작성 스타일을 비교하는 자료였다.

이번 재분류 이후에는 그보다 더 유용한 질문으로 바뀐다.

> 이 파일이 짧은가?

가 아니라:

> **이 파일의 failure mode에 필요한 실행 계약이 있는가, 그리고 필요 없는 계약을 상시 context에 싣고 있지 않은가?**

이 기준이 이후 bad → good 리팩터링의 기준이 된다.
