# 부록 A. 실전 체크리스트

이 체크리스트는 점수를 만들기 위한 것이 아니다.

목적은 파일 유형별로 실제 failure mode에 필요한 계약이 빠졌는지 빠르게 확인하는 것이다.

## A.1 모든 instruction file 공통

### Ownership

- 이 파일이 소유하는 지식의 종류를 한 문장으로 설명할 수 있는가.
- 다른 instruction file과 같은 규칙을 중복 소유하지 않는가.
- 더 정확한 machine-readable source가 있으면 값을 복제하지 않았는가.

### Scope

- repo-wide 규칙만 root standing instruction에 있는가.
- path-local 규칙은 nested instruction 또는 path Rule로 내려갔는가.
- task-local procedure는 Skill로 분리했는가.
- 기계적으로 검사 가능한 규칙은 validator, lint, Hook, CI로 이동할 수 있는가.

### Freshness

- 바뀔 수 있는 version, API, status 정보를 static prose에 무기한 박아 두지 않았는가.
- canonical source가 명확한가.
- fallback snapshot에는 source와 date가 있는가.
- live verification 실패 시 추측하지 않는가.

### Maintenance

- local reference가 실제 존재하는가.
- removal condition을 설명할 수 있는가.
- model 또는 host upgrade 시 삭제 후보를 다시 보는가.

## A.2 CLAUDE.md / AGENTS.md

- 모든 작업에 필요한 정보만 상시 context에 있는가.
- subsystem 세부사항이 root에 쌓이지 않았는가.
- 일반 개발 handbook을 그대로 복사하지 않았는가.
- build/test entrypoint가 실제 저장소와 일치하는가.
- task procedure 전체가 root에 들어 있지 않은가.
- nested instruction, Rule, Skill로 가는 pointer가 있는가.
- host-specific 규칙을 portable rule처럼 쓰지 않았는가.

### 리팩터링 신호

- root 파일이 계속 커진다.
- “항상 먼저 읽어라” 문서가 늘어난다.
- 같은 test/style 규칙이 여러 곳에 반복된다.
- 현재 모델이 이미 잘하는 일반론이 많다.
- release, deploy, migration 절차가 root에 들어 있다.

## A.3 Path-scoped Rule

- matcher가 실제 필요한 파일만 잡는가.
- 이 규칙이 해당 path 밖에서는 필요하지 않은가.
- parent와 같은 정책을 장문으로 복제하지 않았는가.
- formatter/linter가 판정하는 내용을 중복하지 않았는가.
- path가 이동하면 matcher도 검토되는가.
- 현재 저장소에서 matcher가 실제 파일과 매치되는가.

## A.4 Auto-trigger SKILL.md

### Trigger

- description에 무엇을 하는지가 있는가.
- 언제 사용하는지가 있는가.
- adjacent negative가 필요한가.
- domain 전체를 무조건 잡지 않는가.
- none 또는 abstain이 가능한가.

### Preconditions

- 필요한 file, state, tool, config가 명시됐는가.
- 없는 값을 임의로 만들지 않는가.
- prerequisite 실패 시 fallback 또는 stop이 있는가.

### Procedure

- 순서가 실제 결과에 영향을 주는 단계만 강하게 고정했는가.
- judgment와 deterministic step을 구분했는가.
- 긴 manual과 catalog를 복제하지 않았는가.
- reference를 조건부로 읽는가.

### Evidence

- completion을 self-report로 판정하지 않는가.
- test, output, artifact, trace, status 같은 증거가 있는가.
- narrow Skill에는 명확한 Done when을 둘 수 있는가.

### Handoff

- 어디서 멈추는가.
- 다음 Skill, tool, human으로 넘기는 조건이 있는가.
- deprecated entrypoint가 full logic을 복제하지 않는가.

### Eval

- explicit positive가 있는가.
- implicit positive가 있는가.
- adjacent negative가 있는가.
- routing pair가 필요한가.
- candidate와 installed Skill이 충돌하지 않는 환경에서 평가하는가.

## A.5 Manual-only Skill

- 사람이 이름과 호출 방법을 찾을 수 있는가.
- argument contract가 명확한가.
- auto-trigger eval에서 제외되는가.
- explicit invocation이 필요한 이유가 있는가.
- 실패와 retry behavior가 있는가.
- side effect가 크면 approval과 evidence가 있는가.

## A.6 High-side-effect Skill

### Intent

- prepare/preview와 execute/publish를 구분하는가.
- 사용자 요청이 실제 mutation 의도를 포함하는가.
- routine reversible step에 불필요한 approval을 요구하지 않는가.

### Authority

- state owner가 명확한가.
- 이 Skill이 바꾸면 안 되는 state가 있는가.
- validation authority와 execution authority를 분리해야 하는가.

### Permission

- 필요한 tool 권한만 사용하는가.
- secret을 저장소 파일에 남기지 않는가.
- equivalent bypass path를 검토했는가.

### Failure

- 실패가 성공 상태로 남지 않는가.
- interrupted execution cleanup이 있는가.
- 비용과 resource leak 가능성을 다뤘는가.

### Evidence

- mutation 결과를 확인할 identifier나 status가 있는가.
- 완료 선언이 실제 실행 결과와 연결되는가.

## A.7 Validation / Test Skill

- test가 실제로 read-only인가.
- 외부 infrastructure나 비용을 사용할 수 있는가.
- 가장 좁은 충분한 test부터 실행하는가.
- focused test와 full regression을 구분하는가.
- timeout이 필요한가.
- flaky/cache false positive를 구분하는가.
- suspicious pass의 failure sensitivity를 확인할 수 있는가.

## A.8 Fast-moving framework / CLI / API Skill

- current source of truth가 무엇인가.
- installed version과 latest version을 구분하는가.
- existing project와 new project의 기준을 구분하는가.
- CLI option table을 static Skill에 복제하지 않았는가.
- help, generated schema, installed docs, live docs 중 올바른 source를 쓰는가.
- live source 실패 시 fallback이 있는가.
- user target을 무시하고 latest를 강제하지 않는가.

## A.9 Hook

- Hook이 필요한 실제 failure mode가 있는가.
- matcher가 위험 surface만 잡는가.
- deny test가 있는가.
- legitimate near-match allow test가 있는가.
- tool argument semantics를 정확히 모델링하는가.
- equivalent bypass를 검토했는가.
- side effect가 idempotent한가.
- workspace trust를 고려했는가.

## A.10 최종 열 질문

1. 언제 활성화되는가.
2. 언제 활성화되면 안 되는가.
3. 시작 전에 무엇이 참이어야 하는가.
4. state와 authority owner는 누구인가.
5. 어떤 절차가 실제로 필요한가.
6. 어떤 side effect와 권한이 있는가.
7. 무엇으로 완료를 증명하는가.
8. 어디서 멈추고 handoff하는가.
9. 바뀌는 사실은 어디서 다시 읽는가.
10. 어떤 failure나 eval이 이 지침을 수정하거나 삭제하게 하는가.
