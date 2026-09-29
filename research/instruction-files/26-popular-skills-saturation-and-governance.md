# 유명 Skill 최종 확장 조사와 자료 수집 포화점

기준일: 2026-09-30  
조사 기간: 2026-07-01 ~ 2026-09-30

## 1. 마지막 확장 표본

앞선 조사에 이어 다음 공식/공식 조직 저장소를 추가 확인했다.

- `github/awesome-copilot`
- `stripe/ai`
- `mongodb/agent-skills`
- `hashicorp/agent-skills`

주의:

- `github/awesome-copilot`은 GitHub 조직의 공개 repository지만 community contribution도 포함한다. 모든 Skill을 GitHub 내부 authored policy로 간주하지 않는다.
- `stripe/ai`의 Skill 파일은 자주 sync되므로 개별 sync commit보다 Skill이 취하는 freshness architecture를 본다.
- MongoDB 대표 Skill path는 이번 3개월에 직접 변경 commit이 없으므로 현행 구조 사례로만 사용한다.
- HashiCorp는 2026-08 governance/skill update commit이 있어 최근 변화 근거로 사용한다.

---

# 2. GitHub Awesome Copilot: deterministic rule과 editorial judgment를 분리한다

Representative:
`.github/skills/code-review/SKILL.md`

2026-09-23 추가.

Skill의 첫 지시는 다음 구조다.

1. `.github/copilot-instructions.md`의 deterministic checklist를 먼저 적용
2. schema validation으로 환원할 수 없는 editorial/repository-fit 판단만 Skill에서 수행

이 구분이 중요하다.

## Deterministic surface

기계적으로 판단 가능한:

- required fields
- manifest/schema
- repository checklist
- structural requirements

는 instructions/checker 쪽에서 다룬다.

## Judgment surface

Skill은:

- repository fit
- meaningful value
- differentiation
- provenance
- validation evidence
- maintainability

같은 정성 판단을 맡는다.

### 핵심 원칙

> Validator가 할 수 있는 것을 reviewer Skill에게 다시 추론시키지 않는다.

이것은 기존 `prose → structure` 원칙을 code-review domain에서도 확인한다.

---

# 3. GitHub: AI-authored 여부 자체를 품질 verdict로 사용하지 않는다

같은 review Skill은 AI-authorship marker가 있더라도 그 자체를 결함으로 보고하지 않는다.

대신 다음을 본다.

- concrete need
- human validation
- useful constraints
- differentiation
- observable output quality

또 "AI-generated 같다", "low quality 같다", "marketing 같다" 같은 vague comment를 피하고 **구체적인 관찰 근거**를 요구한다.

### 책에 추가할 원칙

Agent-generated instruction을 리뷰할 때도:

> provenance label이 아니라 artifact behavior와 evidence를 평가한다.

---

# 4. GitHub: Instruction Policy 변경 자체가 보안 surface다

특히 중요하다.

review Skill은 다음 파일의 변경을 security-sensitive governance change로 본다.

- `.github/skills/code-review/`
- `.github/copilot-instructions.md`
- `AGENTS.md`
- 기타 review-policy files

이유:

Copilot Code Review는 PR head branch의 Skill과 instruction을 읽기 때문에 PR 작성자가 review policy 자체를 약화시키면 reviewer가 약해진 정책을 읽을 수 있다.

### 새 smell

**Self-Modifying Review Policy**

검토 대상 변경이 동시에 검토자의 정책을 바꾸는 구조.

### 일반화

다음도 같은 문제를 가진다.

- CI policy를 바꾸는 PR이 동일 CI로 자신을 승인
- security lint config를 완화하고 같은 run에서 green
- agent instruction을 약화한 뒤 agent review를 통과

### 책의 원칙

> Instruction policy 파일 변경은 일반 문서 변경이 아니라 governance 변경으로 분리해서 review해야 한다.

---

# 5. Stripe: snapshot에 생성일과 TTL 의미를 붙인다

Repository:
https://github.com/stripe/ai

Representative:
`skills/upgrade-stripe/SKILL.md`

이 Skill의 version strategy는 매우 명확하다.

1. 사용자가 target version을 지정하면 그것을 사용
2. 아니면 live Stripe docs에서 current version 확인
3. live source를 못 읽을 때만 bundled fallback 사용
4. fallback에는 생성 시점이 기록됨
5. Stripe stable version이 월 단위로 바뀌므로 한 달 넘은 fallback은 stale 가능성이 높다고 명시
6. live verification이 실패하면 "latest"라고 주장하지 않음
7. 더 최신 version number를 추측하지 않음

### 강한 패턴

**Dated Fallback Snapshot**

static snapshot을 완전히 금지하지 않는다.

대신:

- source date
- expected freshness interval
- fallback-only status
- verification failure behavior

를 같이 둔다.

### 기존 Snapshot Freshness Debt의 개선형

나쁜 형태:

`Latest version: 2026-X`

좋은 형태:

`Fallback snapshot: X, generated at Y. Prefer live source. After Z interval treat as suspect. Never invent newer value.`

---

# 6. Stripe: Latest와 Explicit User Target의 우선순위를 구분한다

upgrade Skill은 무조건 latest로 강제하지 않는다.

- user가 target을 지정했으면 target
- 기존 pinned version들을 inventory
- stable pin을 preview로 임의 이동하지 않음
- target과 이미 같은 pin은 unchanged로 보고
- target의 source를 명시

### 원칙

> Freshness strategy는 "최신 사용"이 아니라 **어떤 source가 어떤 상황에서 우선하는가**를 정의하는 일이다.

---

# 7. MongoDB: Context Before Configuration

Repository:
https://github.com/mongodb/agent-skills

Representative:
`skills/mongodb-connection/SKILL.md`

현행 Skill의 Core Principle:

> connection pool이나 timeout 값을 application context 없이 임의로 추가하지 않는다.

값을 제안하기 전에:

- deployment type
- workload
- concurrency
- latency
- topology
- server version
- driver version
- OS limits

등 실제 context를 본다.

질문도 한꺼번에 interview하지 않고 **한 번에 한 질문**을 권한다.

### 중요한 원칙

**No Magic Numbers Without Context**

Skill이 숫자를 잘 알고 있는 것과 사용자 system에 맞는 숫자를 아는 것은 다르다.

따라서:

- generic default
- measured value
- inferred value
- user-provided target

을 구분해야 한다.

---

# 8. MongoDB Query Optimizer: 관측 가능한 evidence가 없으면 권고의 강도를 낮춘다

Representative:
`skills/mongodb-query-optimizer/SKILL.md`

명시적 trigger boundary:

- optimization/performance/indexing일 때만 사용
- 일반 query 작성에는 사용하지 않음

가능하면 다음 evidence를 수집한다.

- existing indexes
- `explain`
- sample document
- slow query logs
- Atlas Performance Advisor

그리고:

- 가장 큰 영향의 개선부터 제안
- 인덱스 제거는 Performance Advisor 근거가 있을 때만 제안
- 실제 index 생성은 user approval 없이 수행하지 않음
- 확실하지 않은 권고를 "definitely improve" 같은 강한 언어로 말하지 않음

### 원칙

> Evidence quality가 낮으면 action authority와 assertion strength도 낮춰야 한다.

이를 다음처럼 표현할 수 있다.

\`\`\`text
weak evidence
→ suggestion

strong evidence
→ recommendation

strong evidence + user approval
→ mutation
\`\`\`

---

# 9. HashiCorp: acceptance test는 "테스트 실행"이 아니라 operational side effect다

Repository:
https://github.com/hashicorp/agent-skills

Representative:
`plugins/terraform/skills/run-acceptance-tests/SKILL.md`

이 Skill은 test command를 단순 verification으로 취급하지 않는다.

Terraform provider acceptance test는:

- 실제 infrastructure 생성 가능
- 비용 발생 가능
- live API credential 필요
- 중단 시 resource가 남을 수 있음

따라서 시작 전에:

- credential이 test account를 가리키는지 확인
- secret은 repository/file에 기록하지 않음
- invocation-local env를 선호
- explicit timeout
- interruption cleanup/sweeper

를 다룬다.

### 중요한 교훈

**Verification Side Effect**

"테스트를 실행하라"도 항상 안전한 read-only action은 아니다.

Skill author는 verification command의 side effect까지 알아야 한다.

---

# 10. HashiCorp: suspiciously passing test도 검증한다

Acceptance test가 pass했다고 끝내지 않는다.

Skill은 의심스러운 pass의 경우 test condition을 일부러 바꿔:

1. failure가 실제로 발생하는지 확인
2. 다시 원상 복구

하는 flip test를 설명한다.

이는 Superpowers의 RED 확인과 같은 계열이다.

### 원칙

> PASS만으로 test validity를 증명할 수 없는 경우 failure sensitivity를 확인한다.

---

# 11. HashiCorp: raw state보다 stable interface를 우선한다

2026-08-10 commit `4451ceca5456e79cc776efee96a744f7ac96e5bf`에는 Terraform state access를 token-efficient하게 개선한 내용이 포함된다.

현재 `refactor-module`은:

- `terraform state list`
- `terraform show -json`

같은 documented interface를 먼저 사용한다.

raw state는:

- provider unavailable
- init 불가
- coarse info만 필요
- Terraform 실행을 피해야 함

같은 제한된 경우에 fallback한다.

또 state는 어떤 format에서도 sensitive value를 포함할 수 있으므로 로그에 출력하지 않는다.

### 원칙

> 내부/raw representation보다 stable, scoped, lower-noise interface를 우선한다.

이것은 context engineering과 security를 동시에 개선한다.

---

# 12. HashiCorp: Skill 변경 자체에 governance template를 둔다

같은 2026-08 governance update에서 repository는 Skill 관련 issue/PR template에 다음을 요구한다.

새 Skill:

- authoritative source
- inclusion driver
- owner
- reviewers
- security/privacy
- credential handling
- operational impact
- positive routing
- negative routing
- functional behavior eval
- operational safety

기존 Skill 업데이트:

- affected workflow
- authoritative source
- supported-model impact
- owner/reviewer
- security/credential/operational impact
- evaluation plan

PR:

- affected surfaces
- source docs
- eval evidence
- model impact
- security/privacy/credential considerations
- structural validation
- marketplace checks

### 중요한 교훈

> 성숙한 Skill repository에서는 Skill 작성 규칙뿐 아니라 **Skill 변경 절차 자체**가 관리 대상이다.

---

# 13. 마지막 표본이 추가한 smell

## S30. Self-Modifying Review Policy

검토 대상이 reviewer의 instruction/policy를 같은 변경에서 약화할 수 있다.

## S31. Undated Fallback Snapshot

fallback snapshot은 있지만:

- 생성일
- TTL
- canonical live source
- stale behavior

가 없다.

## S32. Context-Free Magic Number

실측/context 없이 pool size, timeout, threshold 같은 숫자를 보편값으로 제시한다.

## S33. Verification Side-Effect Blindness

test/validation command를 read-only라고 가정해:

- 비용
- resource 생성
- credential
- cleanup

을 고려하지 않는다.

## S34. Pass-Only Verification

test가 pass하는지만 보고 실제로 failure를 감지할 수 있는지는 확인하지 않는다.

## S35. Raw-State First

stable command/API/schema가 있는데 raw internal representation 전체를 읽어 context와 secret exposure를 키운다.

---

# 14. 최근 3개월 연구의 수렴점

총 세 라운드에서:

- 방법론형 유명 Skill
- 실제 업무형 Skill
- 공식 vendor Skill
- 추가 official-org 표본

까지 확장했다.

새 표본을 추가할수록 완전히 새로운 문법보다 기존 축이 반복되기 시작했다.

반복되는 축:

1. Trigger
2. Negative boundary
3. Preconditions
4. State/authority ownership
5. Procedure
6. Permission/side effect
7. Evidence/verification
8. Handoff/stop
9. Freshness/canonical source
10. Eval/maintenance

### 결론

이제 "유명 Skill을 더 많이 수집"하는 작업의 marginal value는 낮아졌다.

다음에 더 가치 있는 연구는 **개수 확장**이 아니라 다음 중 하나다.

- 특정 패턴의 commit-history deep dive
- bad → refactor 사례 만들기
- 책 본문에 실제 사례 배치
- 실측 없이 가능한 structural validator 설계
- public corpus를 위 10개 축으로 재분류

사용자가 실측을 보류했으므로 현재 가장 적절한 다음 단계는:

> **수집을 멈추고, 이번 규칙 taxonomy를 책의 작성 규칙과 checklist로 통합하는 것**

이다.

---

# 15. 최종 Skill review 질문 10개

이번 최근 3개월 연구를 압축하면 Skill 하나를 다음 10개 질문으로 리뷰할 수 있다.

1. **Trigger** — 어떤 요청에서 선택되는가?
2. **Boundary** — 언제 선택되면 안 되는가?
3. **Precondition** — 시작 전에 무엇이 참이어야 하는가?
4. **State** — workflow state와 그 owner는 누구인가?
5. **Procedure** — agent가 실제로 무엇을 어떤 순서로 하는가?
6. **Side effect** — 어떤 mutation, 비용, 권한, approval이 필요한가?
7. **Evidence** — 완료/정확성을 무엇으로 증명하는가?
8. **Handoff** — 어디서 멈추고 다음 Skill/tool/human에게 넘기는가?
9. **Freshness** — 어떤 canonical source와 version strategy를 쓰는가?
10. **Maintenance** — 어떤 feedback/eval로 수정하고 언제 삭제하는가?

이 10개가 현재 연구에서 가장 안정적으로 반복된 구조다.

---

# 16. 책에 사용할 최종 압축 문장

> **좋은 SKILL.md는 지식을 많이 담은 문서가 아니다. 올바른 요청에서만 활성화되고, 시작 조건과 권한을 확인하며, 필요한 절차만 실행하고, 증거를 남긴 뒤 정확한 지점에서 멈추며, 바뀌는 사실은 canonical source에서 다시 읽고, 더 이상 필요하지 않으면 삭제할 수 있는 작은 실행 프로토콜이다.**
