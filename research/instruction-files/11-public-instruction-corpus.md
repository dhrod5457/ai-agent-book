# 공개 저장소 지침 파일 Corpus

수집일: 2026-09-30

## 목적

공식 문서가 말하는 "좋은 지침"을 반복하는 데서 멈추지 않고, 실제 공개 저장소에서 `CLAUDE.md`, `AGENTS.md`, `SKILL.md`, path-scoped Rule이 어떻게 작성되고 있는지 관찰하기 위한 corpus다.

이 목록의 항목은 "모범 사례" 순위가 아니다. 좋은 패턴, 과도한 패턴, 지침 부채, portability 문제, trigger 설계 등 서로 다른 현상을 비교하기 위한 표본이다.

## 표본 요약

| 유형 | 파일 수 | 평균 줄 수 | 중앙값 | 최소 | 최대 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `AGENTS.md` | 10 | 91.1 | 83.5 | 39 | 170 |
| `CLAUDE.md` | 10 | 110.6 | 108 | 17 | 271 |
| `SKILL.md` | 12 | 180.6 | 77.5 | 19 | 865 |
| Cursor Rule | 3 | 36.3 | 28 | 26 | 55 |
| 전체 | 35 | 122.7 | 78 | 17 | 865 |

주의:

- 이 표본은 무작위 모집단이 아니다. 작성 패턴을 폭넓게 보기 위해 의도적으로 다양한 사례를 골랐다.
- 줄 수가 짧다고 자동으로 좋은 파일은 아니며, 길다고 자동으로 나쁜 파일도 아니다.
- 현재 표본 중 5개 파일이 200줄을 넘고, 1개 Skill은 865줄이다.
- 줄 수 자체보다 상시 로드 범위, progressive disclosure, trigger 정밀도, 중복, 검증 가능성을 함께 봐야 한다.

## Corpus

| # | 저장소 | 파일 | 유형 | 줄 | 관찰 포인트 |
| ---: | --- | --- | --- | ---: | --- |
| 1 | getsentry/skills | `AGENTS.md` | AGENTS | 39 | 짧은 repo 정책. Skill 작성은 canonical `skill-writer`로 위임. 등록·frontmatter·500줄 기준을 명시 |
| 2 | m98/fluent | `CLAUDE.md` | CLAUDE | 120 | 역할/identity가 강한 상시 prompt. 매 세션 다수 파일을 읽도록 요구하는 형태 |
| 3 | novotnyllc/dotnet-artisan | `AGENTS.md` | AGENTS | 110 | cross-provider frontmatter 차이를 명시. machine-parseable skill reference 사용 |
| 4 | duthaho/skillhub | `AGENTS.md` | AGENTS | 78 | description trigger eval, deterministic validator, registration drift 검사 |
| 5 | pinchen147/system-design-skill | `CLAUDE.md` | CLAUDE | 17 | 매우 짧은 invariant 중심 파일. script로 못 잡는 것만 prose에 둔다고 선언 |
| 6 | contentstack/contentstack-management-dotnet | `AGENTS.md` | AGENTS | 53 | universal entry point. 상세 규칙을 `skills/*/SKILL.md`로 위임 |
| 7 | FullProduct-dev/green-stack-starter-demo | `CLAUDE.md` | CLAUDE | 77 | core convention + 관련 상세 문서 포인터. 특정 규칙은 Cursor Rule로 분리 |
| 8 | ethpandaops/panda-pulse | `CLAUDE.md` | CLAUDE | 45 | 여러 Cursor Rule을 반드시 읽도록 하지만 현재 참조 경로가 기본 브랜치에서 사라진 stale reference 사례 |
| 9 | ryanthedev/code-foundations | `CLAUDE.md` | CLAUDE | 213 | plugin/skill family와 workflow가 많이 들어간 대형 상시 지침 사례 |
| 10 | vieko/bonfire | `AGENTS.md` | AGENTS | 89 | cross-agent memory 프로젝트. manual-only Skill, outcome-oriented spec를 명시 |
| 11 | ivanrvpereira/.agents | `AGENTS.md` | AGENTS | 115 | shared vs agent-specific config 분리. auto/on-demand Skill을 directory 구조로 구분 |
| 12 | tyevans/tackline | `CLAUDE.md` | CLAUDE | 124 | content project/code project에 따라 posture를 나눔. orchestrator 성격이 강한 전역 지침 |
| 13 | foyzulkarim/claude-lens | `CLAUDE.md` | CLAUDE | 109 | CLAUDE=process, AGENTS=code로 책임 분할. 일부 시점 정보가 stale 가능성을 스스로 언급 |
| 14 | c-reichert/flowstate | `CLAUDE.md` | CLAUDE | 23 | 아주 짧은 구조/버전/Skill invocation 규칙 중심 |
| 15 | codingagentsystem/cas | `CLAUDE.md` | CLAUDE | 271 | 특정 task/memory 도구 사용을 강하게 강제. 관리 블록과 큰 제품 설명이 함께 있음 |
| 16 | leogallego/claude-ansible-skills | `CLAUDE.md` | CLAUDE | 107 | portable Agent Skills와 Claude extension의 충돌·차이를 명시 |
| 17 | danpeg/bug-hunt | `SKILL.md` | Skill | 89 | manual-only. argument parsing과 exact-order workflow가 명확 |
| 18 | levineam/lastXdays-skill | `SKILL.md` | Skill | 66 | 대부분의 복잡성을 script로 넘기는 script-backed Skill |
| 19 | mikefutia/claude-vision | `SKILL.md` | Skill | 57 | prerequisite, argument, script 실행, 실패 조건이 단순하고 명확 |
| 20 | vgrichina/re-skill | `SKILL.md` | Skill | 196 | live context command, 여러 task category, 상태 파일을 적극 사용 |
| 21 | smartfrog/opencode-froggy | `AGENTS.md` | AGENTS | 150 | 일반적인 build/test/style 지침을 한 파일에 폭넓게 담는 형태 |
| 22 | FlyinPancake/yoink | `AGENTS.md` | AGENTS | 170 | repo-wide 개발자 guide에 가까운 대형 AGENTS 파일 |
| 23 | jinganix/admin-starter | `AGENTS.md` | AGENTS | 43 | 상세 테스트 규칙을 별도 문서와 Cursor Rule로 분리한 짧은 router |
| 24 | t0mtaylor/peepshow | `AGENTS.md` | AGENTS | 64 | explicit Trigger + Don't fire for를 모두 제공하는 standing instruction |
| 25 | mnapoli/skill-address-pr-review | `SKILL.md` | Skill | 62 | review/CI 처리 절차가 간결. helper script가 data retrieval/action 담당 |
| 26 | scasella/claude-dynamic-workflows-codex | `SKILL.md` | Skill | 865 | 단일 SKILL.md가 매우 비대한 반례 후보. 상세 DSL/reference가 runtime root에 집중 |
| 27 | natedemoss/Claude-Code-Wrapped-Skill | `SKILL.md` | Skill | 24 | 한 기능 + 한 command + 고정 output. 매우 좁은 Skill |
| 28 | HKUST-KnowComp/DeepRefine-Skill | `SKILL.md` | Skill | 422 | safety approval gate와 forbidden behavior를 매우 상세히 기술 |
| 29 | NewWorkFoundation/jobclaw | `SKILL.md` | Skill | 107 | accepted input, intake contract, output contract 중심 |
| 30 | qingzhoupro/afsim-skill | `SKILL.md` | Skill | 232 | 명시적 progressive disclosure layer를 Skill 본문에 문서화 |
| 31 | sai-7i/daxue-zhidao | `SKILL.md` | Skill | 28 | 여러 host adapter를 references로 분리한 아주 짧은 portable router |
| 32 | jarombouts/star-trek-voice-clone | `SKILL.md` | Skill | 19 | command + voice/style example만 있는 최소 Skill |
| 33 | jinganix/admin-starter | `.cursor/rules/java-tests.mdc` | Rule | 55 | test path에 scoped. canonical spec를 링크하고 high-signal hard rule만 요약 |
| 34 | jinganix/admin-starter | `.cursor/rules/frontend-tests.mdc` | Rule | 28 | frontend test glob에만 적용되는 path-scoped 규칙 |
| 35 | FullProduct-dev/green-stack-starter-demo | `.cursor/rules/workspace-expo-dependencies.mdc` | Rule | 26 | 특정 package.json 문제만 다루는 좁은 Rule. 명령과 검증까지 포함 |

## 원문 링크

- https://github.com/getsentry/skills/blob/main/AGENTS.md
- https://github.com/m98/fluent/blob/main/CLAUDE.md
- https://github.com/novotnyllc/dotnet-artisan/blob/main/AGENTS.md
- https://github.com/duthaho/skillhub/blob/main/AGENTS.md
- https://github.com/pinchen147/system-design-skill/blob/main/CLAUDE.md
- https://github.com/contentstack/contentstack-management-dotnet/blob/main/AGENTS.md
- https://github.com/FullProduct-dev/green-stack-starter-demo/blob/main/CLAUDE.md
- https://github.com/ethpandaops/panda-pulse/blob/master/CLAUDE.md
- https://github.com/ryanthedev/code-foundations/blob/main/CLAUDE.md
- https://github.com/vieko/bonfire/blob/main/AGENTS.md
- https://github.com/ivanrvpereira/.agents/blob/main/AGENTS.md
- https://github.com/tyevans/tackline/blob/main/CLAUDE.md
- https://github.com/foyzulkarim/claude-lens/blob/main/CLAUDE.md
- https://github.com/c-reichert/flowstate/blob/main/CLAUDE.md
- https://github.com/codingagentsystem/cas/blob/main/CLAUDE.md
- https://github.com/leogallego/claude-ansible-skills/blob/main/CLAUDE.md
- https://github.com/danpeg/bug-hunt/blob/main/SKILL.md
- https://github.com/levineam/lastXdays-skill/blob/main/SKILL.md
- https://github.com/mikefutia/claude-vision/blob/main/SKILL.md
- https://github.com/vgrichina/re-skill/blob/main/SKILL.md
- https://github.com/smartfrog/opencode-froggy/blob/main/AGENTS.md
- https://github.com/FlyinPancake/yoink/blob/main/AGENTS.md
- https://github.com/jinganix/admin-starter/blob/master/AGENTS.md
- https://github.com/t0mtaylor/peepshow/blob/main/AGENTS.md
- https://github.com/mnapoli/skill-address-pr-review/blob/main/SKILL.md
- https://github.com/scasella/claude-dynamic-workflows-codex/blob/main/SKILL.md
- https://github.com/natedemoss/Claude-Code-Wrapped-Skill/blob/main/SKILL.md
- https://github.com/HKUST-KnowComp/DeepRefine-Skill/blob/main/SKILL.md
- https://github.com/NewWorkFoundation/jobclaw/blob/main/SKILL.md
- https://github.com/qingzhoupro/afsim-skill/blob/master/SKILL.md
- https://github.com/sai-7i/daxue-zhidao/blob/guide/SKILL.md
- https://github.com/jarombouts/star-trek-voice-clone/blob/main/SKILL.md
- https://github.com/jinganix/admin-starter/blob/master/.cursor/rules/java-tests.mdc
- https://github.com/jinganix/admin-starter/blob/master/.cursor/rules/frontend-tests.mdc
- https://github.com/FullProduct-dev/green-stack-starter-demo/blob/main/.cursor/rules/workspace-expo-dependencies.mdc

## 다음 corpus 확장 기준

현재 35개는 1차 표본이다. 다음 확장에서는 개수를 무작정 늘리지 않고 빈 범주를 채운다.

1. nested `AGENTS.md` 실제 운영 사례
2. `.claude/rules/*.md` 실제 path-scoped 사례
3. 조직 managed instruction 사례
4. Hook + prose rule이 함께 있는 저장소
5. Skill이 실제 eval을 CI gate로 사용하는 저장소
6. 같은 지침 파일의 6개월 이상 commit history가 있는 저장소
7. 실제 지침 삭제/축소 PR 사례
8. vendor-neutral AGENTS + vendor-specific CLAUDE/Cursor Rule을 함께 운영하는 사례
