# Nested AGENTS.md와 Scope 분할 사례

기준일: 2026-09-30

## 1. 왜 nested scope가 중요한가

큰 저장소에서 모든 규칙을 root `AGENTS.md`나 `CLAUDE.md`에 넣으면 상시 context가 커지고, 특정 subsystem에만 필요한 규칙이 모든 작업에 노출된다.

nested instruction은 이 문제를 다음 방식으로 해결한다.

- root: repository-wide invariant, navigation, 공통 command
- nested: 해당 subtree의 local invariant, build/test/gotcha
- 더 깊은 nested: 더 좁은 module-specific contract

핵심은 "파일을 많이 만든다"가 아니다.

> 특정 규칙이 필요한 code scope와 instruction scope를 맞추는 것.

# Case 1. sfc-gh-eraigosa/dotfiles

Sources:
- https://github.com/sfc-gh-eraigosa/dotfiles/blob/main/AGENTS.md
- https://github.com/sfc-gh-eraigosa/dotfiles/blob/main/sdk/AGENTS.md
- https://github.com/sfc-gh-eraigosa/dotfiles/blob/main/docker/AGENTS.md
- https://github.com/sfc-gh-eraigosa/dotfiles/blob/main/ai/skills/AGENTS.md

## 2. Root AGENTS.md는 tree router 역할

root는 주요 subtree마다 더 구체적인 AGENTS.md를 가리킨다.

예:

- `sdk/AGENTS.md`
- `sdk/gff/AGENTS.md`
- `docker/AGENTS.md`
- `ai/skills/AGENTS.md`
- Windows automation subtree
- archive subtree

특히 `docker/`는 root에 자세한 Docker 규칙을 복제하지 않고:

> Docker 관련 수정 전에 docker/AGENTS.md를 읽으라

는 pointer 중심으로 둔다.

## 3. docker/AGENTS.md는 local invariant만 깊게 가진다

`docker/AGENTS.md`는 77줄이며 Docker subtree에서만 필요한 내용을 다룬다.

핵심:

- build context
- base/deps/config 3-tier layering
- cache invalidation
- install step이 어느 layer에 가야 하는지
- 특정 flag list 누락 시 발생하는 correctness/performance bug

이 정보는 repository의 다른 작업에는 거의 필요 없다.

### 관찰

root에 이 77줄을 넣으면 모든 작업의 context cost가 된다.

nested에 두면 Docker 편집 시에만 필요한 high-signal context가 된다.

## 4. sdk/AGENTS.md는 "subtree handbook" 수준

`sdk/AGENTS.md`는 95줄이다.

담는 내용:

- Go module path 규칙
- release tag convention
- module inventory
- 새 module 추가 checklist
- README/AGENTS 등록 surface
- install wiring
- 실제 output demo 검증

그리고 각 개별 module은 다시 nested AGENTS를 가진다.

즉:

```text
root AGENTS
  → sdk/AGENTS
      → sdk/gss/AGENTS
      → sdk/gff/AGENTS
      → sdk/fleet/AGENTS
      ...
```

형태다.

### 중요한 점

root → sdk → module로 갈수록:

- scope는 좁아지고
- local detail은 증가한다.

이게 nested instruction의 정상적인 정보 밀도 방향이다.

## 5. ai/skills/AGENTS.md는 지침 파일 자체의 local policy

이 subtree는 Skill authoring만 다룬다.

내용:

- Skill folder anatomy
- `evals/evals.json`
- deterministic eval corpus validation
- model-driven behavioral eval
- skill name/folder consistency
- commit 전 검증 command

즉 repository 전체 개발 규칙이 아니라 **Skill authoring 규칙만** 둔다.

책의 관점에서 매우 좋은 사례다.

# Case 2. radio4000/r4-svelte

Sources:
- https://github.com/radio4000/r4-svelte/blob/main/AGENTS.md
- https://github.com/radio4000/r4-svelte/blob/main/src/lib/components/AGENTS.md

## 6. Root는 "nearest nested AGENTS를 읽으라"고 명시

root 파일은 작업 전에:

- docs
- relevant API
- 해당 directory의 nested AGENTS

를 먼저 확인하도록 한다.

중요한 부분:

> 대부분의 세부 설명을 root에 넣지 않고 module 근처에 둔다.

## 7. Component AGENTS는 7줄뿐이다

`src/lib/components/AGENTS.md`는 매우 작다.

내용은 사실상 두 local gotcha다.

- 유사 render branch 3개 이상일 때 Svelte snippet 사용 패턴
- map component family는 source header comment 참고

이 사례는 nested AGENTS가 반드시 작은 handbook일 필요가 없음을 보여준다.

> 하나의 local gotcha만 있어도 그 규칙이 root에 섞이는 것보다 code 근처에 있는 편이 낫다.

## 8. Deep detail을 code header comment에 더 내리는 패턴

root AGENTS는 다음 철학도 명시한다.

- docs는 brief
- deep platform gotcha/workaround rationale는 module header comment에 둠

즉 knowledge hierarchy가:

```text
root AGENTS
→ nested AGENTS
→ source header comment
→ code
```

처럼 내려간다.

이 관점은 중요하다.

모든 개발 지식을 instruction file로 만들 필요가 없다.

코드와 가장 가까워야 하는 detail은 source documentation이 더 적절할 수 있다.

# Case 3. Pulumi customer-managed-workflow-agent

Sources:
- https://github.com/pulumi/customer-managed-workflow-agent/blob/main/AGENTS.md
- https://github.com/pulumi/customer-managed-workflow-agent/blob/main/kubernetes/AGENTS.md

## 9. Root가 repository-wide restriction을 소유

root 119줄에는:

- repository purpose
- release/build 구조
- submodule 정책
- package manager 차이
- release process
- forbidden pattern
- 전체 repository structure

가 있다.

특히:

- `pulumi-service/` 직접 수정 금지
- build artifact commit 금지
- package manager 혼용 금지

등은 repo-wide contract다.

## 10. kubernetes/AGENTS.md는 Kubernetes deployment만 소유

nested 55줄에는:

- K8s component key files
- Pulumi config
- K8s architecture
- worker container naming
- CA certificate gotcha
- rendered YAML secret 위험

이 들어 있다.

root에 이미 있는 release/goreleaser/AMI 내용은 반복하지 않는다.

### 좋은 분할의 특징

부모:
- 전체 repo를 이해하는 데 필요한 공통 invariant

자식:
- subtree에서만 의미 있는 configuration/convention

## 11. 단점도 있다

이 사례의 root는 Kubernetes build command 일부를 이미 포함한다.

nested에도 Kubernetes setup이 있다.

즉 parent-child 간 부분 중복이 있다.

질문:

- root에는 "어떻게 검증하는가" 한 줄만 두고 nested로 위임할 수 있는가.
- root command가 모든 개발자에게 필요한 high-signal command인가.

nested 구조를 쓴다고 자동으로 중복이 사라지는 것은 아니다.

# Case 4. BlackBeltTechnology/pi-agent-dashboard

Sources:
- https://github.com/BlackBeltTechnology/pi-agent-dashboard/blob/develop/AGENTS.md
- https://github.com/BlackBeltTechnology/pi-agent-dashboard/blob/develop/openspec/specs/dox-directory-foldering/spec.md

## 12. AGENTS 규모를 lint 대상으로 만든 사례

이 repository는 instruction file 규모와 directory ownership을 명시적인 lint/spec 대상으로 다룬다.

주요 개념:

- `ROW_CAP = 40`
- `AGENTS_BYTE_CAP = 30000`
- byte over와 row over를 별도 문제로 분류
- 긴 row는 per-file sidecar로 승격 가능
- parent AGENTS가 child directory의 file을 roll-up하지 않도록 함

숫자 자체를 일반 규칙으로 복제할 필요는 없다.

중요한 것은 **instruction scope 자체를 repository architecture로 관리한다는 것**이다.

## 13. "부모가 자식 파일을 소유하지 않는다"

spec은 다음 원칙을 명시한다.

> directory AGENTS.md는 자기 directory의 파일만 문서화한다.

하위 directory의 파일은 해당 하위 AGENTS가 소유한다.

예:

```text
qa/AGENTS.md
qa/packer/AGENTS.md
qa/tests/AGENTS.md
qa/fixtures/AGENTS.md
qa/scripts/AGENTS.md
```

부모에서 모든 파일을 roll-up하는 구조를 분해한다.

### 장점

- instruction ownership과 filesystem ownership이 일치
- parent 파일 팽창 억제
- 파일 이동 시 어느 instruction을 고쳐야 하는지 명확
- nearest context의 locality 증가

## 14. Row cap과 byte cap을 다르게 취급

이 사례가 특히 좋은 이유는 단순히 "40줄 넘으면 쪼개라"가 아니다.

### byte cap 초과

실제 per-turn injection/context 비용 문제로 보아 actionable.

### row cap만 초과

파일 구조 복잡성 문제지만 byte가 작다면 informational일 수 있음.

즉:

> line count와 context cost를 동일시하지 않는다.

책에서 매우 중요한 nuance다.

"200줄 이하" 같은 기준도 hard law가 아니라:

- byte/token cost
- 정보 밀도
- scope
- local relevance

와 함께 봐야 한다.

## 15. Sidecar도 progressive disclosure

긴 한 row의 설명을 별도 per-file AGENTS sidecar로 보내고 parent에는 pointer만 남기는 구조도 사용한다.

이는 Skill의 `references/`와 같은 원리다.

공통 추상화:

> always-visible index + on-demand deep detail.

파일 형식은 달라도 context engineering 원리는 같다.

# Nested Scope의 작성 원칙

## 16. Root에 남길 것

다음은 보통 root 후보다.

- repository identity
- global safety boundary
- canonical package/build command
- source-of-truth 위치
- cross-cutting architecture invariant
- nested instruction navigation
- 모든 subtree에 공통인 verification

## 17. Nested로 내릴 것

- 특정 framework/module convention
- 특정 test style
- 특정 build subsystem rule
- local file ownership
- local gotcha
- 특정 deployment/security concern
- 해당 path에서만 필요한 command

## 18. Source comment/doc로 더 내릴 것

- 특정 function/class의 surprising behavior
- 한 파일에서만 필요한 workaround
- implementation rationale가 code와 함께 바뀌어야 하는 경우
- API contract detail

# Scope Smell

## N1. Root Roll-up

root AGENTS가 모든 하위 파일을 catalog하고 local 규칙까지 품음.

증상:
- root가 계속 커짐
- module 추가 때 root 변경
- unrelated task에서도 모든 detail 노출

## N2. Shadow Without Contract

nested AGENTS가 존재하지만 부모 규칙과 어떤 관계인지 설명하지 않음.

개선:
- inherit / override / local-only semantics를 명시

## N3. Parent-Child Duplication

부모와 자식이 같은 command/rule을 복사.

위험:
- drift
- 어느 쪽이 canonical인지 불명확

## N4. Empty Nested Boilerplate

local rule이 없는데 형식 맞추려고 AGENTS를 생성.

결과:
- navigation noise
- maintenance surface만 증가

## N5. Deep Scope Maze

너무 많은 계층을 만들어 실제 필요한 규칙을 찾기 어려움.

질문:
- 해당 detail을 source comment로 두는 게 더 낫지 않은가.
- parent pointer가 충분한가.

## N6. Filesystem/Instruction Ownership Mismatch

부모 AGENTS가 여러 child subtree의 개별 파일 규칙까지 소유.

파일 이동/삭제 때 stale row가 생기기 쉬움.

# Scope 설계 Decision Tree

## 질문 1

이 규칙이 repository의 거의 모든 작업에서 필요한가?

- Yes → root candidate
- No → 다음

## 질문 2

특정 directory/file type에만 필요한가?

- Yes → nested AGENTS / path Rule
- No → 다음

## 질문 3

특정 procedure를 수행할 때만 필요한가?

- Yes → Skill
- No → 다음

## 질문 4

한 implementation unit의 이유/주의사항인가?

- Yes → source comment / local docs
- No → scope를 다시 정의

# AGENTS vs Path Rule

두 방식은 목적이 비슷하지만 semantics가 다를 수 있다.

## Nested AGENTS

장점:
- vendor-neutral성이 높음
- filesystem locality가 직관적
- subtree handbook에 적합

## Path-scoped Rule

장점:
- glob 기준으로 file type을 정밀하게 선택
- directory 경계와 다른 cross-cutting pattern에 적합

예:

```text
**/*.test.ts
service/**/src/test/**/*.java
**/package.json
```

처럼 path가 여러 subtree를 가로지를 때 Rule이 더 자연스럽다.

# 책에 반영할 핵심 주장

1. root instruction은 모든 detail의 저장소가 아니라 navigation + global invariant여야 한다.
2. nested instruction은 code ownership boundary와 맞출수록 유지보수하기 쉽다.
3. line 수보다 byte/token/context cost와 scope relevance가 중요하다.
4. local gotcha가 하나뿐이어도 nested file이 더 적절할 수 있다.
5. 너무 깊은 nesting은 또 다른 retrieval cost를 만든다.
6. nested AGENTS, path Rule, Skill, source comment는 경쟁 관계가 아니라 서로 다른 scope 도구다.

한 문장으로 요약하면:

> 지침을 짧게 만드는 가장 좋은 방법은 문장을 압축하는 것이 아니라, 그 지침이 필요한 위치로 옮기는 것이다.
