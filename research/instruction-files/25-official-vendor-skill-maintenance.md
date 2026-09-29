# 공식 Vendor Skills 추가 검증: 최신성, Eval 격리, Router 압축

기준일: 2026-09-30  
조사 기간: 2026-07-01 ~ 2026-09-30

## 1. 목적

앞선 조사에서는 유명 방법론형 Skill과 업무형 Skill을 분석했다.

이번 라운드는 공식 vendor가 배포하는 Skill을 추가로 살펴 다음 질문을 검증한다.

- description은 실제로 어떻게 다듬어지는가
- 빠르게 변하는 API/CLI 지식을 Skill에 어떻게 보존하는가
- router Skill이 커졌을 때 어떻게 분리하는가
- Skill 자체를 평가할 때 어떤 contamination 문제가 생기는가
- domain-specific Skill과 generic engineering procedure의 경계를 어떻게 잡는가
- 사용자 피드백을 Skill maintenance로 어떻게 연결하는가

추가 표본:

- `firebase/agent-skills`
- `expo/skills`
- `supabase/agent-skills`
- `cloudflare/skills`
- `firecrawl/cli`
- `google-labs-code/stitch-skills`

인기도 탐색에는 `LinklyAI/best-skills`의 2026-09-29 public snapshot을 보조 자료로 사용했다.

이 ranking은 후보 발굴용이며 품질 순위로 사용하지 않는다.

---

# 2. Firebase: description은 짧아져도 trigger coverage는 넓어질 수 있다

Repository:
https://github.com/firebase/agent-skills

대표:
`skills/firebase-security-rules-auditor/SKILL.md`

현재 Skill은 약 85줄이다.

## 현재 description 구조

description에 다음을 동시에 담는다.

- 무엇을 감사하는가
- 어떤 취약점 class를 보는가
- 언제 호출하는가
- 언제 호출하지 않는가

특히 다음 negative boundary가 명시적이다.

- Firebase CLI 작업 아님
- Auth 아님
- Crashlytics 아님
- Remote Config 아님
- database query 작업 아님

## 최근 실제 변경

2026-07-27 commit `97090866a309bfa22d12be8410dba63d73be5a16`

변경 전 description은 대략:

> Firestore security rules가 안전한지 평가한다.

수정 후:

- Firestore + Cloud Storage
- privilege escalation
- role bypass
- create/update inconsistency
- resource exhaustion
- type safety
- size limit
- ownership check
- red-team audit
- explicit exclusions

까지 포함했다.

그런데 commit message는 동시에:

> description을 약 69 token으로 압축

했다고 기록한다.

그리고 activation eval 결과를 근거로 변경했다.

### 중요한 교훈

다음 둘은 반대말이 아니다.

- description을 짧게 만들기
- trigger coverage를 넓히기

좋은 압축은 keyword를 줄이는 것이 아니라 **중복 설명을 제거하고 distinct trigger branch를 남기는 것**이다.

### 책의 규칙 후보

> Description budget을 글자 수 절감 문제로 보지 말고 distinct routing branch 밀도 문제로 본다.

---

# 3. Firebase Security Auditor: adversarial Skill은 공격자 관점을 명시한다

동일 Skill의 body는 일반적인 보안 checklist보다 더 구체적이다.

예:

- create가 안전해도 update로 우회 가능한가
- 권한 판단이 user-provided field를 신뢰하는가
- field allowlist가 identity authorization으로 오해되고 있지 않은가
- size/type limit이 빠져 DoS/data corruption이 가능한가
- 실제 app business logic과 rule이 충돌하지 않는가

출력도 JSON으로 고정한다.

- score
- summary
- findings
- severity
- issue
- recommendation

### 중요한 교훈

judgment-heavy Skill도 모든 것을 자유 서술로 둘 필요는 없다.

**탐색은 adversarial하게 열어 두고, 결과 계약은 구조화할 수 있다.**

---

# 4. Expo: Skill eval 자체도 격리가 필요하다

Repository:
https://github.com/expo/skills

대표:
`.claude/skills/expo-skill-eval/SKILL.md`

이 Skill은 약 315줄이며 Skill을 평가하는 maintainer Skill이다.

평가 축:

- trigger accuracy
- generated code quality
- runtime screenshots
- iOS / Android
- optional web

## 가장 중요한 부분: Skill-under-test 충돌

Expo eval은 두 단계를 다르게 로드한다.

### Executor / runtime phase

로컬 repo의 Skill 파일을 path로 직접 읽는다.

### Trigger eval phase

로컬 plugin을 `--plugin-dir` 방식으로 로드해 model이 description으로 자동 선택하게 한다.

문제:

이미 published Expo plugin이 설치/활성화되어 있으면:

- local Skill
- installed published Skill

이 동시에 보일 수 있다.

그 결과 model이 published Skill을 선택해도 evaluator가 이름만 보면 local Skill이 trigger된 것으로 잘못 점수화할 수 있다.

현재 eval Skill은 그래서 trigger eval 전에 published plugin이 비활성화되었는지 **명시적 사용자 확인**을 요구한다.

### 새 smell

**Eval Skill Collision**

평가하려는 Skill과 기존 설치본/동명이인 Skill이 동시에 discovery surface에 존재해 잘못된 대상을 측정하는 문제.

### 책에 추가할 원칙

> Routing eval은 model만 fresh session이면 충분하지 않다. Skill inventory 자체도 격리해야 한다.

즉 eval isolation에는:

- fresh conversation
- fixed available skill set
- no duplicate installed version
- local/candidate path identity
- raw activation evidence

가 필요하다.

---

# 5. Expo: Evaluator의 권한도 최소화한다

`expo-skill-eval`은 `allowed-tools`를 매우 구체적으로 제한한다.

예:

- 특정 temp/cache 경로 Read
- 특정 temp 경로 Write/Edit
- eval script 형태의 Bash

즉 Skill을 평가하는 evaluator가 전체 파일시스템과 무제한 shell을 자동으로 갖지 않는다.

### 새 원칙

**Evaluator Least Privilege**

평가 harness도 production agent 못지않게 권한 경계를 가져야 한다.

특히:

- 사용자 repo
- global plugin config
- emulator
- temp artifacts

를 함께 다루는 eval은 권한 과잉이 결과 오염과 안전 문제를 동시에 만든다.

---

# 6. Expo Upgrade: "최신"보다 대상 version의 실제 경로가 우선이다

대표:
`plugins/expo/skills/expo-upgrade/SKILL.md`

이 Skill은 SDK별 reference를 분리한다.

예:

- React 19
- New Architecture
- React Compiler
- Native Tabs
- expo-av migration
- Expo Router migration

## Version-sensitive rule

upgrade 전에:

- target release
- beta/preview 여부
- native project 존재 여부
- CNG 여부

를 먼저 본다.

최근 실제 수정:

- 2026-07-16 versioned docs link 관리
- 2026-08-13 Hermes V1 memory regression guidance 추가
- 2026-09-02 실제 feedback 기반 upgrade guidance 수정

### 중요한 원칙

> Framework Skill은 "항상 최신으로 올려라"가 아니라 현재 project state → target version → 알려진 migration path 순으로 판단해야 한다.

이것은 Prisma의 version-preserving repair와 같은 방향이다.

---

# 7. Expo: feedback를 Skill maintenance input으로 만든다

2026-07-22 commit은 Expo Skill 전체에 canonical actionable-feedback block을 추가하고 validator/CI에서 이를 관리하도록 했다.

2026-08-04에는 eval 후보 signal 수집 category를 추가했다.

즉 production 사용 중 발견되는:

- 잘못된 instruction
- 빠진 edge case
- runtime failure
- eval 후보

를 Skill authoring loop로 다시 가져온다.

### 책에 추가할 maintenance loop

사용 → correction/feedback → candidate eval → instruction change → regression eval

Skill maintenance는 문서 리뷰 일정만으로 이루어지지 않는다.

**실제 사용 실패가 가장 좋은 backlog source다.**

---

# 8. Supabase: under-trigger를 description에서 교정한다

Repository:
https://github.com/supabase/agent-skills

대표:
`skills/supabase-postgres-best-practices/SKILL.md`

현재 entrypoint는 약 65줄이다.

본문은 rule index 역할을 한다.

우선순위:

1. Query Performance — CRITICAL
2. Connection Management — CRITICAL
3. Security & RLS — CRITICAL
4. Schema Design — HIGH
5. Concurrency & Locking — MEDIUM-HIGH
6. Data Access Patterns — MEDIUM
7. Monitoring — LOW-MEDIUM
8. Advanced — LOW

## 최근 실제 변경

2026-07-30 commit `32912161e2732c3e5001c6811a76c1f8308ed0da`

description이 performance Skill처럼만 보이면:

- schema
- migration
- RLS
- SQL authoring

작업에서 under-trigger된다는 문제가 있었다.

그래서 description을 "Postgres performance"에서 다음 영역까지 확장했다.

- table/column change
- schema
- migration
- RLS
- index
- trigger
- function
- pg_cron/pgmq
- pgvector
- restore/import
- slow query
- lock/bloat/connection issue

### 중요한 교훈

Skill 이름이나 제목이 narrow하면 description이 그 좁은 mental model을 보완해야 할 수 있다.

다만 이것도 keyword 나열을 무한히 늘리라는 뜻은 아니다.

**실제로 놓치는 branch를 추가한다.**

---

# 9. Cloudflare: pretraining보다 retrieval을 우선한다

Repository:
https://github.com/cloudflare/skills

대표:
`skills/workers-best-practices/SKILL.md`

현재 파일은 약 61줄.

첫 문장이 매우 분명하다.

> 모델의 Cloudflare Workers API/types/config 지식은 오래됐을 수 있으므로 retrieval을 pre-training보다 우선한다.

## 그러나 "무조건 최신 docs"도 아니다

기존 codebase에서는 먼저:

- installed package versions
- generated types
- Wrangler compatibility settings

을 baseline으로 본다.

그 뒤 필요한 API/config/runtime/limit만 current Cloudflare docs로 검증한다.

즉:

\`\`\`text
project configured reality
    +
current official source
\`\`\`

를 같이 쓴다.

"새 최신 package가 존재한다"는 이유만으로 기존 target을 틀렸다고 판정하지 않는다.

### 이 원칙은 중요하다

> Latest is not the same as applicable.

---

# 10. Cloudflare: generic process를 지우고 domain evidence만 남긴다

2026-09-05에 관련 commit이 연속으로 있었다.

변화:

- description을 distinct trigger 중심으로 축소
- retrieval/validation을 affected task scope로 제한
- generic review procedure 삭제
- observability rule은 유지
- concrete Workers anti-pattern은 entrypoint에 복구
- 상세 내용을 configuration/runtime/platform references로 분리
- retrieval-first 문장을 다시 명시적으로 복구

### 중요한 판단 기준

삭제 대상:

- 어디서나 통하는 generic code review 절차

유지 대상:

- Workers에서 실제로 틀리기 쉬운 API/runtime/config 규칙
- 즉시 판단에 필요한 concrete anti-pattern

### 책의 원칙 후보

> Domain Skill에는 일반 개발 프로세스보다 domain-specific surprise를 남긴다.

generic engineering process는 별도 Skill 또는 host 기본 능력에 맡기는 편이 낫다.

---

# 11. Firecrawl: Router 329줄을 141줄로 줄였다

Repository:
https://github.com/firecrawl/cli

대표:
`skills/firecrawl/SKILL.md`

현재 entrypoint는 약 158줄이다.

중요한 최근 refactor:

2026-08-20 commit `41cc07c7e1b63473033e7e3811f27ebb2512403f`

- Router `SKILL.md` 329 → 141 lines
- monitor detail을 monitor Skill로 이동
- install/auth detail을 rules로 이동
- search feedback detail을 search Skill로 이동
- single source of truth 구성

현재 약간 늘어난 것은 이후 기능 추가 때문이다.

### 중요한 원칙

Router는:

- capability 선택
- escalation order
- handoff pointer

를 담당하고, 각 capability의 full manual까지 소유하지 않는다.

---

# 12. Firecrawl: Cached CLI Manual을 삭제했다

같은 날 commit `980163d726adc77b41efb36ffa88774eca642bcd`

핵심 변화:

- static CLI option table 삭제
- `firecrawl <command> --help` pointer로 교체
- frontmatter와 중복되던 `When to use` section 삭제
- monitor detail을 conditional reference로 이동
- negative phrasing을 가능한 곳에서 positive instruction으로 변경
- 각 narrow Skill에 정확히 하나의 `Done when` completion criterion 추가

전체 `SKILL.md` line 수:

1045 → 723

### 새 smell

**Cached CLI Manual**

CLI의 옵션/flag 목록을 SKILL.md에 복제해 시간이 지나면 CLI와 Skill이 서로 다른 truth를 갖는 문제.

### 대응

- `--help`
- installed-version docs
- generated schema
- live official docs

중 적절한 source를 canonical로 둔다.

---

# 13. Firecrawl: 너무 줄이면 trigger가 사라질 수 있다

중요한 점은 Firecrawl이 단순 압축만 한 것이 아니라는 것이다.

2026-08-20 commit `1d5be95508184e110d4ee61e4593310e798f7f40`

실험/forensics에서 neutral web-research task에서 Firecrawl adoption trigger가 빠진 것을 관찰했다.

또:

- 429 rate limit에서 반복 retry loop
- bad auth에서 동일 실패 반복

도 확인했다.

그래서:

- neutral-task web research trigger를 다시 복구
- rate-limit/auth terminal rule을 추가

했다.

### Superpowers와 같은 교훈

압축은 목적이 아니다.

**행동에 필요한 trigger/guard가 사라지면 다시 넣는다.**

---

# 14. Firecrawl: completion criterion을 한 문장으로 만든다

각 narrow Skill은 다음과 비슷한 `Done when`을 가진다.

- output file이 실제 요청에 답하는 valid JSON인가
- crawl이 terminal status에 도달하고 기대 page가 저장됐는가
- requested content/action result가 capture되고 session이 stop됐는가

### 중요한 패턴

Skill 끝에 큰 checklist가 항상 필요한 것은 아니다.

narrow procedure는:

> **한 개의 checkable completion sentence**

가 더 효율적일 수 있다.

---

# 15. Firecrawl: escalation ladder는 비용과 복잡도를 같이 줄인다

현재 router의 기본 순서:

1. Search
2. Inspect + Scrape
3. Map + Scrape
4. Crawl
5. Monitor
6. Interact

예:

- scrape로 되면 interact하지 않음
- known URL이면 search하지 않음
- 이미 fetched content가 있으면 재-fetch하지 않음
- `.firecrawl/` 결과를 재사용

### 책에 추가할 패턴

**Cheapest Sufficient Primitive First**

Skill이 여러 도구를 가질 때:

> 가장 강한 도구부터 쓰지 말고 가장 좁고 싼 primitive부터 escalation한다.

Ponytail의 최소화 ladder와 operational tool routing에서 같은 형태가 관찰된다.

---

# 16. Google Stitch: design-system source of truth를 prompt와 분리한다

Repository:
https://github.com/google-labs-code/stitch-skills

대표:
`plugins/stitch-design/skills/generate-design/SKILL.md`

현재 파일은 약 340줄.

이번 3개월에 해당 파일의 변경 이력은 없으므로 **현행 구조 사례**로만 사용한다.

## 중요한 책임 경계

화면 생성 전에 design system 존재 여부를 확인한다.

design system이 있으면 generation prompt에는:

- color
- font
- theme
- roundness

를 다시 쓰지 않는다.

이 값들의 owner는 project-level design system이기 때문이다.

generation Skill은:

- layout
- content
- structure

에 집중한다.

### 새 smell

**Duplicated Domain Tokens**

동일한 rule/token이:

- project design system
- screen prompt

양쪽에 존재해 서로 충돌하는 문제.

### 일반화

이것은 디자인에만 해당하지 않는다.

예:

- DB schema와 Skill 안의 복제 schema
- generated types와 수동 type 설명
- CI threshold와 prose threshold
- config file과 Skill 안의 duplicated setting

### 책의 원칙

> 이미 machine-readable canonical source가 있으면 Skill은 값을 복사하지 말고 그 source를 읽는 절차를 적는다.

---

# 17. 공식 Vendor 사례가 추가로 지지하는 유지보수 방향

## V1. Trigger는 eval로 수정한다

Firebase, Supabase.

## V2. Router는 얇아진다

Firecrawl, agent-browser, Remotion.

## V3. Fast-changing detail은 canonical runtime/source에 위임한다

- agent-browser: installed CLI skill content
- Firecrawl: CLI `--help`
- Cloudflare: installed schema + live docs
- Expo: version-specific refs + release endpoint
- Prisma: version router

## V4. Eval도 contamination과 permission을 설계해야 한다

Expo.

## V5. Narrow Skill은 completion criterion을 더 명확히 만들 수 있다

Firecrawl.

## V6. Generic process보다 domain-specific surprises가 우선한다

Cloudflare.

## V7. Feedback가 Skill backlog의 source가 된다

Expo.

---

# 18. 새 smell 후보

## S23. Cached CLI Manual

CLI flags/options를 Skill에 복제.

결과:

- stale syntax
- duplicate source of truth
- instruction bloat

## S24. Eval Skill Collision

candidate와 installed Skill이 동시에 보이면서 다른 Skill을 평가.

## S25. Latest-Version Override

현재 project compatibility target을 무시하고 최신 문서/타입만 기준으로 판정.

## S26. Duplicated Domain Tokens

canonical config/design system/schema 값이 Skill prompt에 다시 복제.

## S27. Generic Process in Domain Skill

domain Skill이 이미 다른 Skill/agent가 잘하는 일반 code review/planning 절차까지 중복.

## S28. Unbounded Evaluator Permission

eval Skill이 필요 이상으로 global filesystem/config/shell 권한을 가짐.

## S29. Missing Completion Bound

절차는 있지만 어떤 observable state가 되면 끝인지 정의되지 않음.

---

# 19. 기존 품질 모델에 추가할 항목

앞선 연구의:

- Boundary completeness
- State integrity
- Freshness strategy
- Side-effect discipline

에 다음 두 항목을 추가할 가치가 있다.

## Canonical-source alignment

Skill이 설명하는 값/명령/버전이 실제 canonical source와 중복돼 drift하지 않는가.

## Eval isolation

Skill eval이:

- 동일 inventory
- 동일 candidate
- fresh session
- duplicate installed skill 없음
- restricted evaluator permissions

조건에서 수행되는가.

---

# 20. 책에 사용할 실전 체크

## Description

- distinct trigger branch가 들어 있는가
- exclusion이 필요한가
- 줄였는데 중요한 branch가 사라지지 않았는가
- eval로 수정했는가

## Body

- generic process를 중복하고 있지 않은가
- domain-specific surprise가 남아 있는가
- `Done when`이 있는가
- 더 강한 tool로 escalation하기 전에 좁은 primitive를 시도하는가

## References

- cached CLI manual을 복사하지 않았는가
- installed version / config / schema / official docs 중 canonical source가 무엇인가
- reference가 task별로 조건부 로드되는가

## Eval

- candidate와 installed Skill이 충돌하지 않는가
- available Skill inventory가 고정됐는가
- evaluator 권한이 필요한 범위로 제한됐는가
- trigger와 output/runtime 평가를 분리했는가

## Maintenance

- 실제 사용자 correction을 backlog로 받는가
- stale Skill을 삭제할 수 있는가
- generic prose가 늘어날 때 다시 분리하는가
- model/platform upgrade 후 old workaround를 제거하는가

---

# 21. 결론

공식 vendor Skill까지 넓혀도 방향은 일관된다.

좋은 Skill은 시간이 갈수록:

- 더 많은 설명을 축적하기보다
- canonical source를 명확히 하고
- router를 줄이고
- trigger를 eval로 조정하고
- stale detail을 runtime/docs/schema에 위임하고
- 완료 상태를 관측 가능하게 만들고
- 필요 없는 Skill 자체를 삭제한다.

따라서 Skill authoring을 다음처럼 볼 수 있다.

> **Skill 작성은 Markdown 작성이 아니라, context에 무엇을 복제하지 않을지와 어떤 source를 언제 읽을지를 설계하는 작업이다.**

그리고 maintenance 관점에서는:

> **좋은 Skill 저장소는 Skill 수가 계속 늘어나는 저장소가 아니라, 중복 router와 stale guidance를 계속 합치고 지우는 저장소다.**
