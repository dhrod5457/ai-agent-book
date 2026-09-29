# 공개 지침 파일에서 관찰된 작성 패턴과 Smell

기준 표본:
[11-public-instruction-corpus.md](11-public-instruction-corpus.md)

이 문서는 corpus에서 반복해서 보인 패턴을 정리한다. 특정 저장소를 평가하거나 순위를 매기는 목적이 아니라, 책에서 사용할 "관찰 가능한 작성 현상"을 추출하는 것이 목적이다.

## 1. 짧은 entry point + 상세 문서 분리

다음 사례가 대표적이다.

- `pinchen147/system-design-skill/CLAUDE.md`: 17줄
- `c-reichert/flowstate/CLAUDE.md`: 23줄
- `jinganix/admin-starter/AGENTS.md`: 43줄
- `contentstack/contentstack-management-dotnet/AGENTS.md`: 53줄

공통점:

- root 파일에서 repository 전체를 설명하려 하지 않는다.
- invariant와 routing에 집중한다.
- 긴 규칙은 Skill, reference, 별도 convention 문서로 보낸다.
- canonical file을 하나 정하려는 경향이 있다.

책에서 사용할 원리:

> 전역 파일은 "모든 것을 아는 문서"보다 "무엇을 항상 알고, 어디로 가야 하는지 알려주는 지도"에 가까울수록 context 효율을 통제하기 쉽다.

## 2. 전역 파일이 developer handbook으로 팽창하는 패턴

다음 표본은 150줄 이상이다.

- `smartfrog/opencode-froggy/AGENTS.md`: 150줄
- `FlyinPancake/yoink/AGENTS.md`: 170줄
- `ryanthedev/code-foundations/CLAUDE.md`: 213줄
- `codingagentsystem/cas/CLAUDE.md`: 271줄

이런 파일이 잘못됐다고 단정할 수는 없다. 그러나 다음 감사 질문이 필요하다.

- 모든 섹션이 모든 작업에서 필요한가.
- build/test reference를 별도 문서로 보내도 되는가.
- 특정 path에만 필요한 규칙이 섞여 있지 않은가.
- workflow procedure가 상시 context에 남아 있지 않은가.
- 현재 모델이 이미 처리하는 일반론이 남아 있지 않은가.

이 사례군은 "200줄 규칙"을 절대 숫자로 쓰기보다 **리팩터링 신호**로 설명하는 데 적합하다.

## 3. Skill 길이의 편차가 매우 크다

표본 12개 Skill의 중앙값은 77.5줄이지만 최대는 865줄이다.

짧은 사례:

- `star-trek-voice-clone/SKILL.md`: 19줄
- `Claude-Code-Wrapped-Skill/SKILL.md`: 24줄
- `daxue-zhidao/SKILL.md`: 28줄

큰 사례:

- `DeepRefine-Skill/SKILL.md`: 422줄
- `claude-dynamic-workflows-codex/SKILL.md`: 865줄

여기서 얻을 수 있는 연구 질문:

- 큰 Skill의 어떤 부분이 항상 필요한가.
- examples/reference/DSL 설명을 분리할 수 있는가.
- 큰 Skill이 실제 trigger 후 token cost를 얼마나 늘리는가.
- 안전 규칙처럼 always-needed detail과 optional knowledge를 구분했는가.

책에서는 "500줄을 넘으면 실패" 같은 이분법보다 **always-needed vs on-demand content**를 기준으로 분석하는 편이 낫다.

## 4. 좁은 Skill은 입력-행동-출력 계약이 명확하다

`star-trek-voice-clone`, `Claude-Code-Wrapped-Skill`, `claude-vision` 같은 Skill은 범위가 좁다.

공통 패턴:

- 명확한 input
- 하나의 핵심 행동
- 작은 tool set
- 짧은 success/failure path
- 고정된 output expectation

이런 Skill은 description의 trigger 범위를 좁히기 쉽고, eval도 단순하다.

반대로 여러 업무를 하나에 묶은 Skill은 trigger와 body 검증이 동시에 어려워진다.

## 5. manual-only Skill과 auto-trigger Skill을 명시적으로 구분한다

다수 사례가 `disable-model-invocation`을 사용한다.

중요한 관찰:

- manual-only Skill은 description이 모델 routing보다 사람의 slash-command discovery에 더 가까운 역할을 할 수 있다.
- auto-trigger Skill은 description이 실제 routing surface가 된다.
- 두 종류를 같은 기준으로 평가하면 안 된다.

`duthaho/skillhub`는 manual-only Skill을 trigger eval에서 제외한다.

책에서 권장할 구분:

### Auto-trigger Skill

- description precision을 eval한다.
- false positive/false negative를 측정한다.
- 인접 Skill과 routing pair를 둔다.

### Manual-only Skill

- command discoverability
- argument clarity
- body execution correctness
- safety gate

를 중심으로 본다.

## 6. "Use when"보다 "Not when"이 더 중요한 사례가 있다

`t0mtaylor/peepshow/AGENTS.md`는 video/animated image에서 trigger하고 static image에는 사용하지 말라고 명시한다.

`duthaho/skillhub`의 trigger corpus는 다음처럼 routing pair를 둔다.

- map vs blueprint
- feature vs bugfix
- verdict vs pulse
- priorart vs verdict
- ideate vs priorart
- tune vs cachewise

이 패턴이 중요한 이유:

> 실제 routing 실패는 "관련 있는 요청을 못 찾는 것"뿐 아니라 "비슷한 다른 요청을 잘못 가져가는 것"에서 많이 발생한다.

따라서 Skill description과 Rule description에 **인접 경계**를 설계해야 한다.

## 7. Description은 실제 테스트 대상이 될 수 있다

`duthaho/skillhub`는 description만 추출해 별도의 trigger eval을 수행한다.

이 구조는 책에 매우 중요하다.

- runtime body를 보지 않는다.
- 실제 model-visible description만 judge에게 준다.
- organic prompt에서 어느 Skill이 선택돼야 하는지 확인한다.
- 비슷한 Skill 두 개가 경쟁하는 routing pair를 포함한다.
- description 변경 시 eval 재실행을 요구한다.

이는 description을 문서 metadata가 아니라 **라우팅 코드에 가까운 interface**로 취급하는 접근이다.

## 8. 지침 파일도 structural validation이 가능하다

`duthaho/skillhub/scripts/validate-skills.py`는 다음을 기계적으로 검사한다.

- SKILL.md 존재
- YAML frontmatter parse
- name 존재
- name = folder
- built-in command name collision
- description 존재
- description 길이
- referenced file 존재
- marketplace registration 양방향 일치
- duplicate registration
- README catalog row

주목할 점:

> semantic quality를 validator로 억지 판정하지 않는다.

validator는 구조적 사실을 검사하고 trigger/quality는 eval로 분리한다.

이 구분은 매우 재사용 가치가 높다.

## 9. "등록 surface drift"도 지침 파일 버그다

Skill 하나가 실제로 여러 surface에 존재할 수 있다.

예:

- directory
- marketplace/plugin manifest
- README inventory
- allowlist
- model-visible description registry
- provider-specific invocation policy

`duthaho/skillhub`는 이 네 surface가 어긋나는 것을 drift라고 보고 CI에서 검사한다.

`getsentry/skills`도 Skill 생성/수정 시 등록과 validation을 canonical `skill-writer` workflow에 포함한다.

책에서 확장할 원리:

> 지침 파일 자체만 맞아도 충분하지 않다. 그 파일이 발견되고 호출되고 배포되는 registration graph도 일관되어야 한다.

## 10. Cross-provider compatibility가 새로운 작성 문제다

`novotnyllc/dotnet-artisan`, `pinchen147/system-design-skill`, `leogallego/claude-ansible-skills`는 provider마다 frontmatter 의미가 다른 문제를 직접 다룬다.

대표 문제:

- Claude의 invocation field를 Codex가 읽지 않음
- Agent Skills validator에는 경고가 나지만 Claude에는 필요한 extension field
- 동일 Skill의 invocation policy를 여러 provider 설정에서 맞춰야 함

책에서는 frontmatter를 다음처럼 분류해야 한다.

1. portable core
2. provider extension
3. repository policy
4. generated/synchronized metadata

## 11. Stale reference는 실제 instruction debt다

`ethpandaops/panda-pulse/CLAUDE.md`는 다음 세 파일을 반드시 읽으라고 지시한다.

- `.cursor/rules/project_architecture.mdc`
- `.cursor/rules/code_standards.mdc`
- `.cursor/rules/development_workflow.mdc`

하지만 현재 기본 브랜치에서는 해당 경로를 찾을 수 없었다.

이 사례가 보여주는 것:

- 링크/경로 존재 여부도 CI에서 검사할 가치가 있다.
- "반드시 읽어라"는 지침일수록 broken reference의 영향이 크다.
- 문서가 존재하지 않으면 모델은 추측하거나 지침을 무시할 수 있다.
- instruction file maintenance는 일반 documentation maintenance보다 실행 영향이 직접적이다.

책에서는 이를 **Instruction Dependency Drift** 사례로 다룰 수 있다.

## 12. "이 파일은 stale해질 수 있다"를 스스로 인정하는 사례

`foyzulkarim/claude-lens/CLAUDE.md`는 현재 상태를 문서화하면서 특정 줄이 stale해질 수 있으므로 실제 GitHub 상태를 다시 확인하라고 적는다.

이건 흥미로운 중간 단계다.

- snapshot 정보를 지침에 넣음
- 동시에 freshness 한계를 문서화
- 실제 source of truth를 조회하도록 지시

더 나은 구조가 가능한지 연구할 수 있다.

예:

- snapshot을 제거하고 source of truth만 가리키기
- generated section으로 자동 갱신
- freshness date/TTL metadata
- Hook/session-start에서 동적으로 주입

## 13. Canonical source와 요약 Rule을 같이 쓰는 패턴

`jinganix/admin-starter`는 좋은 비교 사례다.

- 상세 테스트 convention 문서가 canonical source
- `.cursor/rules/*.mdc`에는 path scope와 high-signal hard rule
- `AGENTS.md`는 관련 문서와 Rule로 라우팅

장점:

- 전체 규칙을 모든 작업에 넣지 않는다.
- 특정 test file에서만 Rule이 활성화된다.
- 상세 정책은 한 문서에 유지된다.
- root entry point는 짧다.

다만 같은 규칙을 요약본과 canonical spec 양쪽에서 수정해야 하는 drift 위험은 여전히 존재한다. 자동 검증 후보다.

## 14. Progressive disclosure를 명시적으로 설계한 사례

`qingzhoupro/afsim-skill`은 본문에 layer를 명시한다.

- root
- error reference
- lesson index
- root-cause detail
- quick reference
- demo index
- complete reference

이 구조는 progressive disclosure의 실제 구현 사례로 유용하다.

연구해야 할 질문:

- layer가 너무 깊어지면 필요한 정보를 못 찾지 않는가.
- root가 각 leaf를 직접 가리키는 방식이 더 좋은가.
- index → index → detail 구조가 retrieval 실패를 만들지 않는가.

즉 progressive disclosure 자체도 과도하게 계층화되면 smell이 될 수 있다.

## 15. Script-backed Skill은 prose를 크게 줄일 수 있다

`lastXdays-skill`, `claude-vision`, `skill-address-pr-review`, `Claude-Code-Wrapped-Skill`에서 반복적으로 보인다.

Skill은 다음만 소유한다.

- 언제 실행
- 입력 해석
- 어떤 script 실행
- script 결과를 어떻게 처리
- 실패/출력 contract

실제 결정론적 작업은 script가 한다.

책에서 다음 원칙으로 연결할 수 있다.

> 자연어로 매번 재구성할 필요가 없는 algorithm과 integration은 script로 옮기고, SKILL.md는 routing과 판단에 집중한다.

## 16. Safety gate를 prose에 둘 때의 한계

`DeepRefine-Skill`은 graph write 전에 explicit approval을 요구하고 forbidden behavior를 상세히 적는다.

이런 safety rule은 중요하지만 추가 질문이 생긴다.

- prose만으로 충분한가.
- permission이나 Hook으로도 막을 수 있는가.
- approval state가 실제 tool argument validation에 연결되는가.
- Skill을 우회한 직접 tool call에서는 같은 정책이 유지되는가.

책에서는 **중요도가 높을수록 prose + structural enforcement를 함께 검토**하는 사례로 사용할 수 있다.

## 17. 지침 파일의 책임 분할도 설계 대상이다

`claude-lens`는 다음처럼 명시적으로 분할한다.

- CLAUDE.md = process
- AGENTS.md = code

`contentstack-management-dotnet`은:

- AGENTS.md = universal entry point
- skills = detailed conventions

`system-design-skill`은:

- CLAUDE.md = script로 못 잡는 invariant
- AGENTS.md = CLAUDE.md symlink

이처럼 파일명보다 중요한 것은 **각 파일의 ownership contract**다.

책에서 독자에게 다음을 요구할 수 있다.

> 지침 파일을 만들기 전에 "이 파일이 소유하는 종류의 지식"을 한 문장으로 정의한다.

## 18. 현재 corpus에서 추출된 Smell 후보

### S1. Global Handbook Bloat

상시 파일이 일반 개발자 handbook처럼 팽창한다.

### S2. Always-Read Cascade

전역 지침이 여러 긴 문서를 매 작업마다 먼저 읽게 한다.

### S3. Broad Trigger

Skill description이 분야 전체를 trigger로 잡는다.

### S4. Trigger Collision

인접 Skill들이 같은 요청을 서로 가져가려 한다.

### S5. Stale Instruction Reference

지침이 존재하지 않는 경로, command, tool을 가리킨다.

### S6. Registration Drift

SKILL.md, marketplace, README, allowlist가 서로 다르다.

### S7. Provider Leakage

특정 provider 전용 field/경로가 portable rule처럼 작성된다.

### S8. Optional Knowledge in Runtime Root

드물게 필요한 reference가 SKILL.md 본문에 항상 들어 있다.

### S9. Prose-Enforced Determinism

기계적으로 검사 가능한 정책을 "MUST" 문장으로만 강제한다.

### S10. Snapshot Freshness Debt

현재 issue 수, version, open state 같은 변하는 사실을 static instruction에 박아 둔다.

### S11. Duplicate Canonical Rules

동일 규칙을 AGENTS, CLAUDE, Rule, Skill에 복사한다.

### S12. Deep Disclosure Chain

필요 정보가 여러 index/reference 단계를 거쳐야 발견된다.

### S13. Semantic Lint Overreach

주관적인 품질을 brittle regex/validator로 억지 판정한다.

### S14. Eval Blind Spot

Skill body는 상세하지만 trigger negative test가 없다.

### S15. Workflow Ownership Collision

둘 이상의 Skill이 같은 prompt와 같은 workflow state transition을 소유한다.

실제 사례:

- Prisma의 `prisma-orm-setup`과 `prisma-database-setup`이 version routing을 중복 소유했다가 2026-09-29 하나의 canonical owner로 통합됐다.

### S16. Unowned State Transition

workflow status를 바꿀 권한이 어느 Skill에도 명확히 귀속되지 않는다.

고위험 결과:

- 검증을 실행하지 않고 상태 문자열만 `Validated`로 바꾸는 우회가 가능해진다.

Microsoft Azure Skills는 prepare / validate / deploy의 상태 ownership을 분리한다.

### S17. Side-Effect Intent Collapse

준비와 실행을 같은 trigger 강도로 취급한다.

예:

- preview = render로 오해
- prepare = deploy로 오해
- review = submit으로 오해
- discover = install로 오해

### S18. Stale Embedded Command Surface

빠르게 바뀌는 CLI flag와 option catalog를 static SKILL.md에 복제한다.

Firecrawl은 cached option table을 `<command> --help` pointer로 교체했고, agent-browser는 installed CLI가 version-matched Skill content를 제공한다.

### S19. Compatibility Logic Duplication

deprecated Skill이 replacement Skill과 같은 full workflow를 계속 보유한다.

대응:

```text
old entrypoint
→ tiny compatibility redirect
→ canonical owner
```

### S20. Host-Tolerated Invalidity

한 host가 비표준 metadata를 관대하게 받아줘 오류가 감춰지고 다른 loader에서 silent failure가 난다.

실제 사례:

- Sentry Skills의 comma-separated `allowed-tools`는 Claude에서는 동작했지만 다른 loader에서는 `Read,` 같은 이름이 invalid tool로 해석되어 capability가 빠졌다.

### S21. Discovery Without Abstention

router가 적합한 Skill이 없어도 무조건 무엇인가 선택한다.

좋은 discovery Skill에는 `none`, fallback, direct-help path가 필요하다.

### S22. User-Change Clobbering

대화 밖에서 사용자가 변경한 파일을 agent가 예상 밖 변경이라는 이유로 덮어쓴다.

Remotion Skill은 surprise change를 intentional user edit으로 우선 취급하거나 확인하도록 한다.

### S23. Cached CLI Manual

CLI documentation을 Skill에 장황하게 복제해 runtime help와 두 개의 truth를 만든다.

S18과 비슷하지만 S23은 특히 **정식 CLI help surface가 이미 존재하는데도 이를 복제하는 유지보수 smell**이다.

### S24. Eval Skill Collision

candidate Skill과 이미 설치된 동명/동패키지 Skill이 동시에 discovery surface에 노출돼 evaluator가 잘못된 Skill을 측정한다.

Expo의 trigger eval은 published plugin과 local plugin의 collision을 명시적으로 차단한다.

### S25. Latest-Version Override

현재 project의 configured target을 무시하고 최신 package/docs만 기준으로 기존 코드를 잘못 판정한다.

Cloudflare는 installed versions, generated types, compatibility date를 baseline으로 두고 current docs를 검증 근거로 결합한다.

### S26. Duplicated Domain Tokens

machine-readable canonical source의 값을 Skill prompt에 다시 복제한다.

예:

- design system token + generation prompt의 색/폰트 중복
- generated schema + 수동 schema 설명
- CI threshold + prose threshold

Google Stitch는 project design system이 theme를 소유하면 generation prompt에서 theme token을 다시 쓰지 않게 한다.

### S27. Generic Process in Domain Skill

특정 domain Skill이 일반 planning/review/debugging 절차까지 중복 소유한다.

Cloudflare는 최근 Workers Skill에서 generic review procedure를 제거하고 Workers-specific anti-pattern과 retrieval rule만 남겼다.

### S28. Unbounded Evaluator Permission

Skill eval harness가 실제 평가에 필요하지 않은 global filesystem, config, shell 권한까지 가진다.

Expo eval Skill은 temp/cache path와 특정 eval script로 allowed-tools를 좁힌다.

### S29. Missing Completion Bound

단계는 상세하지만 observable한 완료 조건이 없다.

Firecrawl은 좁은 Skill마다 하나의 `Done when` 문장을 두는 방향으로 refactor했다.


## 19. 다음 실제 실험으로 연결할 항목

Corpus를 더 늘리기 전에 아래 실험이 더 가치 있다.

1. broad vs narrow description trigger eval
2. routing pair가 있는 description vs 없는 description
3. 865줄 Skill을 router + reference로 분리했을 때 token/성공률 변화
4. stale reference validator
5. root CLAUDE 200+줄 vs path-scoped 분리
6. prose-only safety gate vs Hook/permission 병행
7. nested reference depth 1 vs 3
8. static snapshot state vs source-of-truth lookup
9. cross-provider field를 그대로 복사했을 때 validator/runtime 차이
10. description 변경에 regression eval을 붙였을 때 routing drift 감소

## 핵심 결론

첫 corpus에서 가장 강하게 보이는 것은 "좋은 문장을 쓰는 기술"보다 다음 네 가지다.

1. **지식의 위치를 정한다.**
2. **Skill의 trigger 경계를 설계한다.**
3. **기계적으로 검사 가능한 것은 validator/script로 옮긴다.**
4. **지침 자체의 drift와 regression을 테스트한다.**

이 네 축을 책의 주된 품질 모델로 발전시킬 가치가 있다.
