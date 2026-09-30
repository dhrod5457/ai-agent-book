# 13장. 나쁜 지침 파일 리팩터링

나쁜 지침 파일은 문장이 어색해서 나쁜 경우보다 **책임이 섞여서** 나쁜 경우가 많다.

이 장에서는 자주 나타나는 실패를 “문장 다듬기”가 아니라 구조 변경으로 고친다.

## 13.1 거대한 root instruction

처음에는 root 파일 하나가 편하다.

프로젝트 구조, Java 규칙, TypeScript 규칙, 배포 절차, 문서 규칙, 테스트 정책을 한 곳에서 찾을 수 있다.

하지만 저장소가 커지면 모든 작업에서 모든 규칙이 노출된다.

### 리팩터링

root에는 repo identity, 공통 명령, 전역 invariant, 하위 지침으로 가는 pointer만 남긴다.

backend와 frontend 규칙은 nested instruction이나 path rule로 내린다.

release, migration 같은 절차는 Skill로 옮긴다.

기계적 검사는 validator, lint, Hook으로 옮긴다.

좋은 결과는 root 줄 수가 줄었다는 사실이 아니라 unrelated task에서 불필요한 규칙이 사라졌다는 것이다.

## 13.2 Broad auto-trigger Skill

나쁜 description:

> backend 개발과 데이터베이스 작업에 사용한다.

이 Skill은 너무 많은 요청에서 후보가 된다.

### 리팩터링

도메인이 아니라 사건을 쓴다.

> 새로운 migration을 추가하거나 기존 migration을 변경하고 rollout 위험을 검토할 때 사용한다.

그리고 가장 가까운 adjacent negative를 둔다.

> 단순 query 작성이나 ORM model 탐색에는 사용하지 않는다.

변경 후 positive와 negative corpus로 trigger를 다시 측정한다.

## 13.3 Procedure와 state owner 충돌

prepare, validate, deploy Skill이 모두 같은 상태를 바꾸면 책임이 흐려진다.

예를 들어 validation Skill이 실제 배포 상태까지 바꾸거나, prepare Skill이 승인까지 암묵적으로 처리하면 handoff가 무너진다.

### 리팩터링

각 Skill의 requires-state와 owns-state를 구분한다.

prepare는 artifact 준비까지.

validate는 검증 결과 생성까지.

deploy는 승인된 artifact의 mutation까지.

필요하면 state transition을 machine-readable하게 만들어 validator가 exclusive owner 충돌을 잡게 한다.

## 13.4 Cached CLI Manual

Skill 본문에 CLI flag 전체를 복제하면 시간이 지날수록 실제 도구와 어긋난다.

### 리팩터링

설치된 버전의 help, generated schema, 공식 문서를 canonical source로 둔다.

Skill은 “어떤 옵션이 있다”를 모두 외우게 하지 않고 “어떤 source에서 현재 옵션을 확인할지”를 가르친다.

## 13.5 Prose-only Safety Gate

나쁜 형태:

> IMPORTANT: 사용자 승인 없이는 절대 publish하지 않는다.

문제는 다른 tool call이나 다른 Skill이 동일 mutation을 수행할 수 있다는 것이다.

### 리팩터링

의도 경계는 Skill에 남긴다.

실제 publish surface는 permission과 Hook으로 보강한다.

deny test와 near-match allow test를 둔다.

목표는 더 많이 차단하는 것이 아니다. 실제 위험 action만 정확히 차단하는 것이다.

## 13.6 Deprecated Skill의 full copy

old-setup과 new-setup이 모두 전체 setup logic을 가지면 bugfix와 version policy가 갈라진다.

### 리팩터링

old entrypoint는 compatibility alias로만 남긴다.

자동 선택에서는 제외하고, 명시적으로 old name을 호출한 경우 canonical new Skill로 위임한다.

logic owner는 하나만 둔다.

## 13.7 Eval contamination

개발 중인 candidate Skill과 사용자 환경의 installed Skill이 같은 이름으로 동시에 보이면 trigger eval이 잘못된 대상을 평가할 수 있다.

### 리팩터링

- candidate identity를 고정한다.
- installed duplicate를 비활성화한다.
- available Skill inventory를 기록한다.
- fresh session을 사용한다.
- activation source를 확인한다.

Eval도 환경 격리가 필요하다.

## 13.8 Latest-Version Override

“항상 최신 API를 사용한다”는 지침은 기존 프로젝트를 깨뜨릴 수 있다.

프로젝트가 특정 SDK, runtime, compatibility date에 고정되어 있을 수 있기 때문이다.

### 리팩터링

source 우선순위를 둔다.

1. user target
2. project target
3. installed/generated source
4. current official source
5. dated fallback

새 프로젝트 추천과 기존 프로젝트 리뷰를 같은 기준으로 처리하지 않는다.

## 13.9 Duplicated Domain Tokens

디자인 시스템에 색상과 radius가 있는데 Skill에도 같은 값이 복제되어 있으면 어느 쪽이 source of truth인지 모호해진다.

DB schema, generated types, CI threshold에서도 같은 문제가 생긴다.

### 리팩터링

값을 복제하지 않는다.

Skill에는 canonical source를 읽는 절차만 둔다.

## 13.10 Generic Process in Domain Skill

Cloud, DB, frontend 같은 domain Skill에 다음이 가득할 수 있다.

- 계획해라.
- clean code를 써라.
- 테스트해라.
- 리뷰해라.

이런 일반론은 domain Skill이 없어도 수행 가능한 경우가 많다.

### 리팩터링

domain-specific surprise만 남긴다.

예:

- 이 runtime에서 자주 발생하는 lifecycle 함정
- 이 플랫폼의 binding drift
- 이 DB migration의 rollout 위험
- 이 API의 version target 규칙

generic engineering process는 상위 공통 규칙이나 모델 기본 능력에 맡긴다.

## 13.11 Missing Completion Bound

나쁜 workflow:

1. 검색한다.
2. 분석한다.
3. 개선한다.
4. 좋아질 때까지 반복한다.

언제 끝나는지 알 수 없다.

### 리팩터링

관측 가능한 완료 조건을 둔다.

> 요청한 source set이 수집되고, 답변이 저장된 근거를 참조하며, blocking source gap이 없으면 완료한다.

좁은 Skill은 Done when 한 문장만으로도 충분할 수 있다.

## 13.12 통합 구조

리팩터링 후 저장소는 다음 책임을 갖는다.

- root instruction: 공통 identity와 invariant
- nested instruction/path Rule: local invariant
- Skill: task-specific procedure
- reference: 조건부 상세 지식
- script: 반복 결정론 절차
- Hook: lifecycle enforcement
- CI/validator: structural correctness
- eval: routing과 semantic behavior

이 장의 핵심은 “더 좋은 문장”이 아니다.

> 나쁜 지침을 고치는 가장 강한 방법은 문장을 고치는 것이 아니라 **지식의 위치와 소유권을 다시 설계하는 것**이다.
