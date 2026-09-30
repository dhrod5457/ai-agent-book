# 부록 D. Anti-pattern Catalog

이 목록은 자동 점수표가 아니다. 지침 시스템을 리뷰할 때 자주 나타나는 실패를 빠르게 찾기 위한 catalog다.

## D.1 Root Bloat

### 증상

모든 규칙과 workflow가 root CLAUDE.md 또는 AGENTS.md에 들어 있다.

### 위험

irrelevant instruction 노출, 충돌, context 비용.

### 개선

root invariant만 남기고 path Rule, Skill, validator로 분리한다.

## D.2 Broad Trigger

### 증상

“backend 작업에 사용”, “문서 작업에 사용”처럼 domain 전체를 trigger로 잡는다.

### 위험

false positive, Skill collision.

### 개선

실제 작업 사건을 쓰고 adjacent negative를 테스트한다.

## D.3 Keyword Stuffing

### 증상

description에 가능한 동의어를 모두 넣는다.

### 위험

metadata bloat와 overlap.

### 개선

what + when + 핵심 경계만 남긴다.

## D.4 No Abstention

### 증상

어떤 요청에서도 반드시 Skill 하나를 골라야 하는 구조다.

### 위험

none 요청에서 불필요한 Skill activation.

### 개선

none/abstention case를 eval에 포함한다.

## D.5 State Collision

### 증상

여러 Skill이 동일 workflow state를 소유한다.

### 위험

validation이 mutation으로 번지고 handoff가 불명확해진다.

### 개선

requires-state와 owns-state를 분리한다.

## D.6 Side-effect Intent Collapse

### 증상

prepare, preview, deploy가 구분되지 않는다.

### 위험

사용자가 준비만 요청했는데 실제 mutation까지 실행.

### 개선

intent threshold, permission, approval, evidence를 분리한다.

## D.7 Cached CLI Manual

### 증상

CLI option과 flag를 Skill에 장문 복제한다.

### 위험

실제 버전과 drift.

### 개선

installed help, schema, current official source를 canonical로 사용한다.

## D.8 Duplicated Canonical Config

### 증상

design token, schema, threshold, type을 Skill에 다시 적는다.

### 위험

어느 값이 진짜인지 모호해진다.

### 개선

machine-readable source를 읽는 절차만 남긴다.

## D.9 Generic Process in Domain Skill

### 증상

모든 domain Skill에 계획, clean code, 테스트, 리뷰 일반론이 반복된다.

### 위험

body bloat와 불필요한 제약.

### 개선

domain-specific surprise와 invariant만 남긴다.

## D.10 Prose-only Safety Gate

### 증상

“절대 publish하지 마라” 같은 자연어만 존재한다.

### 위험

다른 tool path에서 우회.

### 개선

permission, Hook, deny/allow test와 결합한다.

## D.11 Deep Reference Chain

### 증상

SKILL.md → A → B → C 형태로 자료가 깊게 연결된다.

### 위험

retrieval overhead와 missed reference.

### 개선

진입점에서 필요한 reference로 직접 연결한다.

## D.12 Deprecated Full Copy

### 증상

old Skill과 new Skill이 같은 workflow를 각각 소유한다.

### 위험

bugfix와 policy drift.

### 개선

old Skill은 compatibility alias로 남기고 canonical owner 하나로 위임한다.

## D.13 Eval Contamination

### 증상

candidate와 installed Skill이 동시에 보인다.

### 위험

다른 Skill을 평가하고도 pass로 기록.

### 개선

inventory 격리와 activation source 기록.

## D.14 Latest-Version Override

### 증상

모든 기존 프로젝트에 최신 문서와 최신 타입을 강제한다.

### 위험

의도적으로 고정된 target을 깨뜨린다.

### 개선

user target → project target → installed source → current official source 순으로 본다.

## D.15 Missing Completion Bound

### 증상

“좋아질 때까지 반복”한다.

### 위험

search loop, over-verification, tool thrashing.

### 개선

observable Done when을 둔다.

## D.16 Host-Tolerated Invalidity

### 증상

현재 host에서 우연히 동작하는 잘못된 metadata.

### 위험

다른 host 또는 upgrade에서 실패.

### 개선

spec validation과 provider smoke test.

## D.17 Line-count Cargo Cult

### 증상

500줄 초과를 자동 실패로 본다.

### 위험

실제 책임과 failure mode를 보지 못한다.

### 개선

줄 수는 refactor signal로만 사용한다.

## D.18 MUST Counter

### 증상

MUST, NEVER 개수로 품질을 점수화한다.

### 위험

실제 안전 경계와 단순 강조를 구분하지 못한다.

### 개선

semantic eval과 human review.

## D.19 LLM-as-Validator Everywhere

### 증상

parse, link, schema 같은 결정론적 오류까지 LLM judge로 판정한다.

### 위험

느리고 비결정적이며 재현성이 낮다.

### 개선

deterministic validator를 먼저 사용한다.

## D.20 Instruction Accumulation

### 증상

실패마다 한 줄을 추가하지만 아무것도 삭제하지 않는다.

### 위험

instruction debt.

### 개선

correction → regression case → scope/structure 개선 → removal audit의 순환을 만든다.
