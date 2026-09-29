# 지침 파일 변경 이력으로 본 Instruction Debt

기준일: 2026-09-30

## 1. 목적

현재의 `CLAUDE.md`, `AGENTS.md`, `SKILL.md`, Hook만 읽으면 왜 그런 구조가 되었는지 알기 어렵다.

이 문서는 공개 저장소의 실제 commit history를 추적해 다음 질문을 본다.

- 어떤 지침이 실제 실패 때문에 추가됐는가.
- 어떤 지침이 너무 길어져 다시 줄어들었는가.
- 모델이나 host가 발전한 뒤 어떤 규칙이 삭제됐는가.
- prose rule이 validator/CI/Hook으로 승격된 사례가 있는가.
- 특정 provider에서는 동작하지만 portable format에서는 깨지는 지침이 있는가.
- safety gate가 너무 강해져 다시 완화된 사례가 있는가.

Instruction Debt를 단순 "낡은 문서"가 아니라 **시간에 따라 축적되는 실행 규칙의 부채**로 보기 위한 자료다.

# Case 1. duthaho/skillhub — Description Diet

Commit:
https://github.com/duthaho/skillhub/commit/429242bd4f6c05c5695a25720f7684da1b9e01ad

Date:
2026-07-14

## 2. 무엇이 바뀌었는가

여러 Skill description이 Claude Code의 1024자 한계에 가까워져 있었다.

commit에서 기록된 축소:

- refactor: 1023 → 767 chars
- scout: 1020 → 801
- learn: 1020 → 747
- jobfit: 1020 → 782
- tune: 1019 → 726

단순 압축이 아니라 다음 기준으로 줄였다.

1. leading concept를 먼저
2. 같은 trigger branch의 synonym 반복 제거
3. body에 있는 mechanism 설명을 description에서 제거
4. 인접 Skill routing hint는 유지

## 3. Auto-trigger에서 manual-only로 바꾼 사례

`autopilot`은 description을 399자 정도로 줄이고:

```yaml
disable-model-invocation: true
```

를 추가했다.

이유는 단순 token 절약이 아니다.

이 Skill은 한 번 실행되면 큰 작업 charter를 승인하고 branch push까지 수행하므로 자동 trigger가 적절하지 않다고 판단했다.

그 결과 trigger eval의 기대값도 바꿨다.

이전:
- 자연어 "전체 작업 맡아서 PR까지" → autopilot

변경:
- 같은 자연어 요청 → feature
- autopilot은 사용자가 명시적으로 실행

### 원리

> Description 작성과 invocation policy는 별개의 문제가 아니다.

위험하거나 비용이 큰 Skill은 description을 아무리 잘 써도 auto-trigger가 적절하지 않을 수 있다.

## 4. Description 길이를 validator 대상으로 승격

같은 commit에서 validator에:

- hard limit: 1024
- soft warning: 950
- built-in command collision 검사

를 추가했다.

즉 description 팽창 문제를 한 번 수동으로 고친 뒤 **재발을 방지하는 structural check**로 승격했다.

이것이 instruction debt 관리의 중요한 패턴이다.

> 반복 correction → 규칙 → validator.

# Case 2. skillhub — Trigger Test를 구현보다 먼저 추가

Commit:
https://github.com/duthaho/skillhub/commit/fd6a387ac86e4f71ff1885480d3fd9e324b727ad

Date:
2026-07

## 5. Skill을 만들기 전에 trigger case를 먼저 넣는다

`priorart` Skill을 추가할 때 commit history는 먼저 trigger case를 추가했다고 명시한다.

> TDD: red until the description exists

추가된 prompt에는 단순 positive뿐 아니라:

- "is there already an open-source project..." → priorart
- not verdict
- not feature

같은 routing boundary가 포함됐다.

### 원리

일반적으로 Skill을 먼저 작성하고 나중에 "잘 trigger되는지" 확인한다.

이 사례는 반대로:

1. 사용자 문장을 먼저 적는다.
2. 어떤 Skill이 선택돼야 하는지 적는다.
3. 현재 상태에서 실패함을 확인한다.
4. description/Skill을 추가한다.

즉 **Trigger-Driven Development**라고 부를 만한 패턴이다.

책에서 별도 실습으로 만들 가치가 높다.

# Case 3. skillhub — Validator를 CI gate로 승격

Commit:
https://github.com/duthaho/skillhub/commit/f61a5d89ee4d5480da1b2acb888a1f167e000b0f

Date:
2026-07-17

## 6. "검사하라"에서 "PR이 통과하지 못하게 하라"로 이동

기존에는 local validator가 있었다.

이 commit에서 GitHub Actions가 추가되어 다음 변경이 있을 때 validator를 실행한다.

- `.claude/skills/**`
- marketplace manifest
- README
- evals
- validator 자체

이 workflow의 주석은 Skill이 여러 surface에 존재하고 서로 어긋나는 것을 **drift**로 정의한다.

### 의도적으로 CI에 넣지 않은 것도 있다

LLM trigger eval은 CI에 넣지 않았다.

이유:
- model judge가 필요
- keyless action에서는 직접 실행하지 않음

즉 모든 검증을 자동화하려 하지 않았다.

### 원리

> 자동화할 수 있는 deterministic drift만 CI gate로 만들고 semantic eval은 별도 유지한다.

# Case 4. getsentry/skills — Runtime Skill 대폭 축소

Commit:
https://github.com/getsentry/skills/commit/412f2368ee3ec90ce042826b57533f080d531aaf

Date:
2026-07-15

## 7. Commit Skill: 178 → 62 lines

`skills/commit/SKILL.md`는 178줄에서 62줄로 줄었다.

삭제/축소된 것:

- 일반적인 conventional commit 장황한 설명
- 반복되는 format/example
- AI attribution 정책
- CLI hygiene의 중복 설명
- body에서 충분히 추론 가능한 detail

남긴 것:

- main/master branch 보호
- repository-specific commit format
- privacy
- issue footer
- 실제 commit 시 필요한 결정

## 8. PR Writer: 302 → 160 lines

`pr-writer/SKILL.md`도 302줄에서 160줄로 줄었다.

핵심은 "내용을 덜 알려준다"가 아니다.

Runtime에 필요한 의사결정만 남기고:

- intent
- evaluation
- maintenance
- source/evidence

같은 정보는 SPEC/EVAL 등 maintenance artifact로 옮긴다.

### 원리

> runtime instruction과 maintainer documentation을 분리하면 Skill을 줄여도 지식이 사라지지 않는다.

이 책에서 "짧게 써라"는 조언 대신 이 구조를 보여줘야 한다.

# Case 5. getsentry/skills — 실제 agent eval을 표준 개발 과정으로 추가

Commit:
https://github.com/getsentry/skills/commit/5a64b36c62d042d3981b7937d9d6ca7bd1753b9a

Date:
2026-06-30

## 9. Custom runner보다 repeatable harness

이 commit은 AXIS를 Skill eval 표준으로 도입했다.

초기 case:

### small-inline-workflow

단순 Skill이 불필요하게:

- references
- scripts
- 큰 source research

로 과설계되지 않는지 확인.

### reference-backed-integration

복잡한 Skill에서:

- SKILL.md는 router
- optional depth는 reference

구조를 확인.

### iteration-from-bad-output

이미 비대한 Skill을 입력으로 주고:

- trigger 축소
- 불필요 artifact 삭제
- 구조 개선

을 실제로 수행하는지 확인.

### 중요한 점

Eval이 "정답 문구가 나왔는가"가 아니라 **작성 원칙을 실제 artifact에서 지키는지** 검사한다.

책에서 자체 eval을 만들 때 그대로 참고할 수 있다.

# Case 6. getsentry/skills — Provider Path Debt

Commit:
https://github.com/getsentry/skills/commit/c81373583417504de2d3be1ae3d81977b11b2981

Date:
2026-05-09

## 10. Claude 전용처럼 보였던 경로 사용이 실제 runtime에서 실패

여러 Skill이 다음 형식을 사용했다.

```text
${CLAUDE_SKILL_ROOT}/scripts/...
```

실제 문제:

1. Bash variable expansion이 permission friction을 만듦
2. runtime에서 variable이 존재하지 않아 `/scripts/foo.py`로 해석되어 실패

수정:

```text
scripts/foo.py
references/bar.md
```

처럼 skill-root-relative path로 통일.

### 원리

> provider-specific convenience를 portable default로 가정하면 실제 runtime portability debt가 생긴다.

이 사례는 "공개 spec과 실제 host runtime을 모두 검증해야 한다"는 근거다.

# Case 7. getsentry/skills — Claude에서는 되지만 표준/다른 loader에서는 깨진 frontmatter

Commit:
https://github.com/getsentry/skills/commit/21af067ff3397fa35f5a0f22f05f6138d9e03307

Date:
2026-09-29

## 11. allowed-tools 구분자 문제

commit message의 핵심:

- comma-separated allowed-tools는 Claude에서 동작
- Agent Skills spec과 다른 loader는 whitespace-separated 형태를 기대
- 다른 host에서는 첫 tool만 제대로 사용하는 문제가 발생

### 의미

이 사례는 매우 중요하다.

"Claude Code에서 잘 된다"와 "Agent Skills로 portable하다"는 동일하지 않다.

책에서는 예제를 다음처럼 구분해야 한다.

- portable syntax
- Claude extension
- Claude-tolerated but non-portable syntax

### 새로운 Smell

**Host-Tolerated Invalidity**

한 host가 관대하게 해석해 오류가 드러나지 않지만 다른 host/validator에서 깨지는 상태.

# Case 8. getsentry/skills — Runtime/Spec 분리

Commit:
https://github.com/getsentry/skills/commit/32fdf36273ac530120134ac484b3ab09717f3410

Date:
2026-05-19

## 12. 실행 지침은 압축하고 범위 계약은 SPEC으로 이동

`iterate-pr`에서:

- runtime 문서를 table/checklist로 압축
- Skill scope를 명확히 하기 위해 `SPEC.md` 추가

또한 "pending CI"와 "human review gate"를 혼동하던 동작도 수정했다.

이 사례의 핵심:

> 설명이 길어진 이유가 runtime logic과 maintenance contract가 섞여 있었기 때문이다.

즉 파일 분리는 단순 token optimization이 아니라 responsibility separation이다.

# Case 9. petekp/claude-code-setup — 모델 업그레이드가 지침 삭제를 요구

Commit:
https://github.com/petekp/claude-code-setup/commit/0de2cbc2e9d2777743be990d6812b4d1820c3094

Date:
2026-09-23

## 13. Opus 5.5 Skill Audit

이 저장소는 최근 60일 사용량이 높은 Skill 9개를 최신 Anthropic prompting guide와 비교했다.

발견:

### Closing self-check

일부 Skill 끝에 앞의 규칙을 다시 확인하는 checklist가 있었다.

최신 모델 가이드에서는 모델이 이미 self-check하는 경향이 있어 이런 지침이 over-verification을 만들 수 있다고 보고 삭제 대상으로 판단했다.

### Broad trigger language

기존:

- "Trigger even if..."
- "Use whenever..."

새 방향:

- 평범한 "Use when..."

새 모델에서는 과거 under-triggering을 막으려 추가한 강한 문구가 **over-triggering debt**가 될 수 있기 때문이다.

### Prompt style leakage

Skill 자체가 금지한 문체를 본문에서 사용하고 있었고 실제 output transcript에서도 같은 문체가 나타났다.

### 원리

> 모델 버전이 바뀌면 "무엇을 추가할까"보다 "어떤 scaffolding을 지울까"를 먼저 감사해야 한다.

Instruction Debt의 핵심 사례다.

# Case 10. flowstate — 오래된 prompting guidance를 뒤집은 audit

Commit:
https://github.com/c-reichert/flowstate/commit/756a19ae9fcc44cc44b49329dae57273b23be250

Date:
2026-09

## 14. 구조적 drift와 중복 gate를 한 번에 정리

commit 설명은 audit에서 다음을 발견했다고 기록한다.

- stale metadata
- structural drift
- 같은 일을 두 번 하는 gate
- unreliable auto-trigger descriptions
- 오래된 prompt-format guidance

변경:

### XML → Markdown

이전 CLAUDE.md는 Skill 구조에 XML tag 사용을 권장했다.

audit 후 최신 prompting guidance에 맞춰 Markdown/blockquotes로 변경했다.

### disable-model-invocation 제거

11개 workflow command에 있던 model-invocation disable을 제거했다.

이유:

- Skill body 자체에 user-approval gate가 이미 있음
- command-level gate는 중복
- 정상적인 dispatch에서 마찰을 만듦

### Description 개선

auto-trigger가 불안정했던 Skill description에 explicit trigger phrase를 추가.

### Non-standard frontmatter 제거

일부 Skill의 provider-specific/non-standard field를 줄이고 필요한 precondition은 description/body로 이동.

### 중요 포인트

모든 "중복 보호"가 defense-in-depth는 아니다.

두 gate가 같은 failure mode만 막고 정상 흐름을 방해한다면 **중복 enforcement debt**가 된다.

# Case 11. sfc-gh-eraigosa/dotfiles — Safety Gate의 Overcorrection

Commit:
https://github.com/sfc-gh-eraigosa/dotfiles/commit/530d68bd0ee792884c85c58f5f528e39d354237d

Date:
2026-09-18

## 15. 안전 규칙이 너무 강하면 다시 제거해야 한다

이전 변경은 `checkpoint`에도 approval token을 요구했다.

문제:

- checkpoint는 draft PR까지만 만든다.
- merge/ready 전환을 하지 않는다.
- routine WIP push에도 사람이 token을 만들어야 함
- agent가 token을 스스로 만들면 gate 의미가 없음
- 스스로 만들지 못하게 막으면 정상 작업이 멈춤

결론:

- checkpoint gate 제거
- 실제 publish-class operation만 gate 유지

### 동시에 실제 bypass는 보강

남긴 gate를 우회할 수 있는:

- `gh pr ready`
- `gh pr merge`

에는 confirmation-tier Hook을 추가.

### 원리

> 안전한 지침은 "가장 많이 막는 규칙"이 아니라, 실제 위험 경계와 정확히 일치하는 규칙이다.

이건 Hook chapter에서 반드시 다룰 사례다.

# Case 12. dotfiles — Hook이 대상 도구의 semantics를 잘못 모델링한 사례

Commit:
https://github.com/sfc-gh-eraigosa/dotfiles/commit/fe438db541a1d53f1b6bd45c5e4c48fed2c60674

Date:
2026-09-06

## 16. Hook의 target resolution이 실제 command와 달랐다

Hook은 approval token을 현재 작업 디렉터리 기준으로 확인했다.

그러나 실제 tool은:

1. `--repo/-r`
2. command의 cwd

순서로 target repo를 결정했다.

결과:

- 올바른 repo에서 token을 생성해도 stale로 오판
- global flag 위치에 따라 gate 자체를 건너뛸 가능성
- 일부 test는 subshell counter 문제로 실패를 놓침

수정:

- Hook이 실제 tool의 resolution semantics를 그대로 모사
- `~`, `$HOME`, `${HOME}` 처리
- resolve 실패는 잘못된 cwd fallback 대신 deny
- 30개 이상의 관련 test 추가
- test harness 자체의 false green도 수정

### 원리

> Hook은 명령 문자열을 대충 검사하는 wrapper가 아니다. 보호하려는 실제 tool의 semantics를 정확히 모델링해야 한다.

# Case 13. petekp — Instruction Infrastructure Doctor

Commit:
https://github.com/petekp/claude-code-setup/commit/aa756fd543657d2fb80ce20b34af50d7958dc3e5

Date:
2026-09-23

## 17. 지침 infrastructure 자체의 health check

Skill symlink가 자기 parent를 가리키는 loop가 실제로 발생했고:

- 일반 symlink 검사 통과
- path도 resolve됨
- recursive walker는 무한 구조
- 앱 bundle signing에서 실패

`skill-doctor.sh`에 해당 loop 탐지를 추가했다.

### 의미

Instruction ecosystem이 커지면 content quality 외에도:

- symlink
- registration
- manifest
- installer
- shadowing
- dangling reference

같은 **infrastructure health**가 별도 문제 영역이 된다.

# Instruction Debt Taxonomy

실제 commit history에서 다음 debt 유형을 구체화할 수 있다.

## D1. Accumulation Debt

실패를 고칠 때마다 description/CLAUDE.md에 문장을 더해 결국 비대해짐.

대응:
- description diet
- runtime compression
- reference/SPEC 분리

## D2. Model-Version Debt

이전 모델의 under-triggering, self-check 부족 등을 보완한 문구가 최신 모델에서 over-trigger/over-verification을 만듦.

대응:
- model upgrade audit
- old scaffolding deletion

## D3. Provider Debt

한 host에서 우연히 동작하는 syntax/path가 표준 또는 다른 host에서 실패.

대응:
- portable core 검증
- cross-provider test

## D4. Registration Debt

Skill file, manifest, catalog, allowlist가 서로 어긋남.

대응:
- validator
- CI gate

## D5. Enforcement Debt

같은 gate가 중복되거나 위험하지 않은 operation까지 차단.

대응:
- actual risk boundary 재정의
- redundant gate 삭제

## D6. Enforcement Bypass Debt

정상 path는 막았지만 equivalent raw command가 우회 가능.

대응:
- effect 기준 threat model
- alternate path test

## D7. Semantic Drift

Hook/Skill이 보호하는 실제 tool의 semantics와 다른 가정을 가짐.

대응:
- executable contract test
- real command grammar를 fixture에 반영

## D8. Trigger Debt

Skill 수 증가로 description 간 충돌이 증가.

대응:
- routing pair eval
- negative case
- manual-only 전환

## D9. Terminology Debt

본문에 과거 설계 단계의 이름이나 더 이상 존재하지 않는 추상화가 남음.

대응:
- 현재 executable/test terminology와 맞춤
- stale term lint 후보

## D10. Infrastructure Debt

symlink, manifest, installer, shadowing 등 instruction distribution layer가 깨짐.

대응:
- doctor
- validation
- health check

# Instruction Debt Audit 제안

모델이나 coding-agent 버전이 올라갈 때 다음 순서로 검사한다.

## 1. 삭제 후보

- 모델이 이제 기본적으로 잘하는 행동
- closing self-check
- "think carefully"류
- 일반적인 coding best practice
- 오래된 workaround

## 2. Trigger 후보

- "always", "whenever", "trigger even if" 같은 과도한 표현
- 인접 Skill과 겹치는 keyword
- manual-only여야 할 고비용 workflow

## 3. Runtime 후보

- body에 이미 있는 내용을 description에서 반복
- maintenance/eval/source 설명이 runtime Skill에 들어 있음
- rarely-needed reference가 root Skill에 들어 있음

## 4. Enforcement 후보

- prose MUST만 존재하는 critical invariant
- 중복 gate
- equivalent bypass path
- false-positive가 많은 matcher

## 5. Portability 후보

- host-specific env var
- host-tolerated non-standard syntax
- absolute path
- provider extension field

## 6. Infrastructure 후보

- broken link
- dangling symlink
- manifest/catalog drift
- built-in name collision
- version mismatch

# 책에 반영할 핵심 주장

이번 history 조사가 정적인 공식 문서 수집보다 중요한 이유는 다음이다.

1. 좋은 지침 파일은 처음부터 완성되는 것이 아니다.
2. 실제 실패에서 규칙이 추가되고, 반복되면 validator/Hook으로 승격된다.
3. 규칙은 계속 추가되는 것이 아니라 모델과 host 변화에 맞춰 삭제된다.
4. safety rule도 과도하면 정상 작업을 막는 부채가 된다.
5. provider에서 동작한다는 사실은 portable하다는 증거가 아니다.
6. Skill의 품질은 현재 내용뿐 아니라 변경 이력과 회귀 방지 구조까지 봐야 한다.

따라서 이 책의 유지보수 원칙은 다음 한 문장으로 요약할 수 있다.

> 지침 파일은 작성해서 끝나는 문서가 아니라, 실패에서 학습하고 모델 변화에 따라 덜어내며 회귀를 테스트하는 실행 구성이다.
