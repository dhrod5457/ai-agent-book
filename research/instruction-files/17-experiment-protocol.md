# 자체 실험 프로토콜: 지침 파일은 어떻게 검증할 것인가

기준일: 2026-09-30

## 1. 목적

이 책의 핵심 주장을 공식 문서와 공개 저장소 사례만으로 끝내지 않고, 재현 가능한 실험으로 검증하기 위한 프로토콜이다.

첫 실험은 세 축을 다룬다.

1. **Skill routing** — description을 어떻게 쓰느냐가 선택 정확도에 미치는 영향
2. **Instruction scope** — root에 몰아넣는 것과 path/nested scope로 나누는 것의 차이
3. **Instruction debt** — 오래된 scaffolding을 제거했을 때 품질과 비용이 어떻게 달라지는지

이 문서는 결과를 미리 가정하지 않는다. 실험 조건, 측정값, 실패 기준을 먼저 고정한다.

---

# Experiment A. Skill Description Routing

## 2. 연구 질문

동일한 Skill body를 유지하고 description만 바꿀 때 다음 차이가 실제 routing에 영향을 주는가.

- 너무 넓고 긴 description
- 짧은 what + when
- what + when + adjacent boundary
- manual-only

## 3. 공식 근거

Agent Skills specification:

- 모든 Skill의 `name`과 `description` metadata는 startup 단계에서 먼저 노출된다.
- `description`은 무엇을 하는지와 언제 사용할지를 설명해야 한다.
- description 최대 길이는 1024자다.
- Skill body는 activation 뒤 전체가 로드된다.
- reference는 필요한 경우에만 로드된다.

Sources:

- https://agentskills.io/specification
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Anthropic best practice는 description이 100개 이상의 후보 중 Skill selection에 사용될 수 있다고 명시한다.

따라서 description은 단순 문서 metadata가 아니라 routing interface로 취급한다.

## 4. 공개 저장소 근거

`duthaho/skillhub`:

- description만 judge에게 제공하는 trigger eval
- positive case
- routing pair
- user-only Skill 제외
- description diet 후 regression eval

Sources:

- https://github.com/duthaho/skillhub/blob/main/evals/triggers.json
- https://github.com/duthaho/skillhub/blob/main/evals/README.md
- https://github.com/duthaho/skillhub/commit/429242bd4f6c05c5695a25720f7684da1b9e01ad

`getsentry/skills`:

- broad trigger를 가진 bad Skill을 fixture로 만들고
- trigger 축소
- runtime body 축소
- 불필요 reference 삭제
- structural validation

을 평가한다.

Source:

- https://github.com/getsentry/skills/blob/main/skills/skill-writer/evals/scenarios/iteration-from-bad-output.json

## 5. Skill set

실험에서는 일부러 경계가 가까운 네 종류를 사용한다.

| Skill | 책임 |
| --- | --- |
| `feature` | 새로운 동작 추가 |
| `bugfix` | 이미 있어야 할 동작이 깨진 문제 수정 |
| `refactor` | 동작 변화 없이 구조 개선 |
| `review` | 구현하지 않고 변경 사항 검토 |

추가로 `none` label을 둔다.

이 구성이 좋은 이유:

- 실제 coding workflow에서 자주 겹친다.
- keyword 하나로만 구분하기 어렵다.
- 신규 기능과 버그 수정, refactor와 review 사이에 현실적인 boundary가 있다.

## 6. Description variant

### A0. Broad

특징:

- 분야 관련 keyword를 많이 나열
- Skill body의 mechanism까지 description에 포함
- 인접 Skill 경계 없음
- 같은 언어의 A1보다 충분히 길고 넓게 작성

목적:

과도하게 넓고 장황한 description이 false positive와 collision을 늘리는지 확인.

문자 수 절대값을 고정하지 않는다. 한국어와 영어의 문자/토큰 밀도가 다르므로 variant별 실제 char/token 수를 함께 기록한다.

### A1. Concise What + When

특징:

- 무엇을 하는지
- 언제 사용하는지
- 대표 trigger 2~4개
- 250~450자 범위

목적:

공식 권고에 가까운 baseline.

### A1L. Length Control

A1과 같은 trigger 의미를 유지하되 실행 메커니즘, 검증 방식 등 **routing에는 필요 없는 정보**를 추가해 A0에 가까운 길이로 만든다.

목적:

- A1 vs A1L: 길이 증가 자체의 영향
- A0 vs A1L: 비슷한 길이에서 broadness의 영향

을 분리해서 본다.

### A2. Boundary-Aware

A1에 다음을 추가한다.

- "깨진 기존 동작이면 bugfix"
- "동작 변화 없이 구조만 바꾸면 refactor"
- "구현 없이 검토만 요청하면 review"

처럼 인접 Skill로 라우팅해야 하는 조건을 짧게 명시한다.

목적:

negative boundary가 routing collision을 줄이는지 확인.

### A3. Manual-only

고비용 또는 사용자의 명시적 승인이 필요한 workflow 하나를 manual-only로 만든다.

이 조건은 accuracy 경쟁에 그대로 넣지 않는다.

측정 질문:

- natural-language 요청에서 manual-only Skill이 후보에서 빠지는가.
- 모델이 가장 가까운 자동 Skill을 고르는가.
- 사용자에게 explicit invocation을 안내하는가.

## 7. Prompt class

각 Skill당 최소 다음 유형을 만든다.

### P1. Explicit positive

예:

- "로그인 500 오류 고쳐줘"

### P2. Implicit positive

Skill 이름이나 "bug"라는 단어 없이 의도를 표현.

예:

- "비밀번호를 비우면 원래 validation 메시지가 나와야 하는데 서버가 죽는다"

### P3. Noisy positive

긴 맥락 안에 핵심 요청이 섞임.

### P4. Adjacent negative

다른 Skill과 쉽게 혼동되는 case.

예:

- "이 모듈이 복잡하긴 한데 동작은 바꾸지 말고 정리해줘" → refactor, not feature

### P5. Routing pair

둘 이상의 Skill이 표면적으로 관련 있지만 하나만 맞는 case.

### P6. None

아무 Skill도 호출할 필요가 없는 질문.

예:

- "이 함수 이름이 무슨 뜻이야?"

## 8. 최소 corpus 크기

1차 pilot:

- explicit positive: 16
- implicit positive: 16
- noisy positive: 12
- adjacent negative/routing pair: 24
- none: 12

합계: **80 prompts**

각 model/host에서 prompt당 최소 5회 반복 권장.

이유:

AI routing은 deterministic하지 않을 수 있으므로 단일 실행 성공률만으로 결론을 내리지 않는다.

## 9. Primary metrics

### Accuracy

```text
correct selections / all prompts
```

### Macro-F1

Skill별 case 수 차이의 영향을 줄인다.

### False Positive Rate

`none` 또는 adjacent negative에서 잘못 Skill을 선택한 비율.

### Collision Error Rate

routing pair에서 인접 Skill을 잘못 선택한 비율.

### Abstention Accuracy

Skill을 선택하지 말아야 할 때 `none`을 선택하는 정확도.

### Run Consistency

같은 prompt를 반복했을 때 같은 label이 나온 비율.

## 10. Secondary metrics

- description chars
- metadata token estimate
- startup metadata total
- selected Skill body token count
- 추가 reference reads
- end-to-end latency
- total model input/output tokens

비용은 품질 metric과 별도로 기록한다.

짧다고 좋은 것이 아니라:

> 같은 정확도를 더 작은 항상-노출 context로 달성했는가

를 본다.

## 11. 결과 해석 규칙

### Boundary-aware가 이겼다고 말하려면

- overall accuracy가 개선되거나 유지
- collision error가 감소
- false positive가 증가하지 않음

을 함께 만족해야 한다.

### Description 축소가 성공이라고 말하려면

- token/char 감소
- accuracy 비열화 없음
- 특정 Skill recall 급락 없음

을 확인한다.

단순 평균만 보고 결론 내리지 않는다.

---

# Experiment B. Root vs Scoped Instructions

## 12. 연구 질문

동일한 규칙 집합을 어디에 배치하느냐가 agent 행동에 영향을 주는가.

## 13. 비교 조건

### B0. Monolithic Root

모든 규칙을 root `AGENTS.md` 하나에 둔다.

예:

- backend Java 규칙
- frontend TypeScript 규칙
- test 규칙
- deployment 규칙
- docs 규칙

모두 상시 노출.

### B1. Root + Nested AGENTS

root:

- repo identity
- 공통 command
- global invariant
- nested navigation

하위:

- `backend/AGENTS.md`
- `frontend/AGENTS.md`
- `tests/AGENTS.md`
- `deploy/AGENTS.md`

### B2. Root + Path-scoped Rules

root에는 공통 규칙만 두고 file/path-specific 규칙을 host의 path rule에 둔다.

예:

- GitHub Copilot: `.github/instructions/*.instructions.md` + `applyTo`
- Cursor: `.cursor/rules/*.mdc` + `globs`
- Claude Code: 해당 제품이 지원하는 scoped rule mechanism

### B3. Root + Scoped Rule + Skill

procedure는 항상-on instruction에서 제거하고 on-demand Skill로 이동한다.

예:

- release
- migration
- dependency upgrade
- screenshot comparison

## 14. 공식 근거

GitHub Copilot은 repository-wide instruction과 path-specific instruction을 별도 개념으로 지원하며, 특정 path에만 필요한 정보로 repository-wide instruction을 과적재하지 않도록 설명한다.

Sources:

- https://docs.github.com/en/copilot/concepts/prompting/response-customization
- https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions

Cursor도 project rule에 `globs`와 `alwaysApply`를 구분한다.

Source:

- https://cursor.com/docs/rules

## 15. Fixture repository

작은 synthetic monorepo를 사용한다.

```text
fixture/
  backend/
    src/
    test/
  frontend/
    src/
    test/
  deploy/
  docs/
```

분야별로 일부러 충돌 가능한 규칙을 둔다.

예:

Backend:
- Java test는 JUnit 5
- package naming
- service-layer transaction rule

Frontend:
- Vitest
- React testing rule
- npm command

Deploy:
- manifest 변경 시 별도 validation
- production secret 금지

Docs:
- code test 대신 link validation

## 16. Task set

최소 40개.

- backend-only 10
- frontend-only 10
- test-only 6
- deployment-only 6
- docs-only 4
- cross-cutting 4

일부 task에는 misleading context를 넣는다.

예:

- frontend 파일을 수정하면서 backend 규칙과 비슷한 이름을 언급
- docs 변경인데 root에 "항상 전체 test"가 존재
- Java test와 TypeScript test가 같은 task description에 같이 등장

## 17. 측정값

### Correct Rule Application

해당 path에 필요한 규칙 준수율.

### Irrelevant Rule Leakage

다른 subsystem 규칙을 잘못 적용한 횟수.

### Verification Precision

해당 변경에 적절한 validation만 실행했는가.

### Over-Verification

필요하지 않은 전체 build/test를 실행했는가.

### Instruction Exposure

task 시점에 실제로 모델에 노출된 instruction bytes/tokens.

### Retrieval Overhead

추가 instruction/reference를 읽기 위한 tool call 수.

### Completion Cost

time/token/tool call.

## 18. 핵심 가설

실험 전 provisional hypothesis:

- B0는 작은 repo에서는 단순하지만 repository가 커질수록 irrelevant instruction 노출이 증가할 가능성이 있다.
- B1/B2는 local rule 적용에는 유리할 수 있지만 scope discovery가 잘못되면 필요한 규칙을 놓칠 수 있다.
- B3는 task-specific procedure의 상시 context 비용을 줄일 가능성이 있다.

이것은 가설이며 결과가 아니다.

---

# Experiment C. Instruction Debt Removal

## 19. 연구 질문

이전 모델을 보조하기 위해 추가된 scaffolding을 최신 모델에서도 유지해야 하는가.

## 20. 비교 조건

### C0. Legacy

기존 지침 유지.

예:

- 반복 closing checklist
- "think carefully"
- "always double-check"
- broad trigger
- 동일 제약 반복
- 과도한 step-by-step recipe

### C1. Diet

다음만 제거.

- 모델 기본 행동과 중복되는 일반론
- body 앞뒤 반복
- 같은 의미의 강조
- 과거 workaround
- broad trigger booster

실제 project-specific invariant는 유지.

### C2. Structural

C1 + machine-checkable rule을 validator/Hook으로 이동.

## 21. 측정값

- task success
- rule violation
- over-verification action 수
- unnecessary tool calls
- total tokens
- repeated self-check loops
- clarification count
- latency

## 22. 반드시 지켜야 할 실험 원칙

### 같은 task

variant마다 task를 바꾸지 않는다.

### 같은 code fixture

repository state를 실행마다 reset한다.

### blind label

결과를 평가하는 사람/LLM judge에게 variant 이름을 숨긴다.

### raw trace 보존

최종 답변만 평가하지 않는다.

- tool calls
- files changed
- commands
- transcript
- tokens
- timings

을 보존한다.

### 결과와 원인을 구분

A2가 A1보다 좋았다고 해서 "negative boundary는 항상 좋다"고 일반화하지 않는다.

최소한:

- model
- host
- Skill set
- task corpus
- version
- date

를 함께 기록한다.

---

# 23. Cross-host matrix

동일 corpus를 가능한 범위에서 다음 host에 반복한다.

| Host | AGENTS | Path Rule | Skill | Hook/Enforcement |
| --- | --- | --- | --- | --- |
| Claude Code | 확인 | 확인 | 핵심 | 강함 |
| Codex | 확인 | 제품 문법 확인 | 확인 | 별도 확인 |
| Cursor | AGENTS 지원 | MDC Rules | Skills | 제품별 |
| GitHub Copilot | AGENTS 지원 | instructions.md | Skills 지원 surface 확인 | surface별 |
| Gemini CLI | instruction 지원 | 제품별 | Skills | Hooks 지원 |

제품별 기능은 실험 실행 시점의 공식 문서로 다시 고정한다.

---

# 24. 결과 저장 형식

각 실행 결과에 최소 다음 metadata를 저장한다.

| 필드 | 설명 |
| --- | --- |
| date | 실행 날짜 |
| model | 정확한 모델/버전 |
| host | Claude Code/Codex 등 |
| host_version | CLI/IDE 버전 |
| variant | A0/A1/... |
| prompt_id | corpus case |
| expected | 기대 route/outcome |
| actual | 실제 route/outcome |
| tokens_in | 가능하면 기록 |
| tokens_out | 가능하면 기록 |
| latency | 가능하면 기록 |
| tool_calls | 수 |
| files_changed | 수 |
| rule_violations | deterministic grader 결과 |
| notes | runtime anomaly |

결과 CSV/JSON은 book prose와 분리한다.

---

# 25. 실험에서 하지 말아야 할 것

- 한 번 실행하고 결론 내리기
- 자기 Skill을 같은 모델에게 주고 "좋아졌나요?"만 묻기
- prompt에 Skill 이름을 직접 넣고 trigger 정확도라고 부르기
- positive case만 테스트하기
- model version을 기록하지 않기
- token 절감만 보고 품질 개선이라 주장하기
- judge score만 남기고 raw artifact를 버리기
- vendor 한 곳의 behavior를 Agent Skills 표준 동작으로 일반화하기

---

# 26. 현재 단계의 결론

이 책의 자체 실험은 벤치마크 순위를 만드는 것이 목적이 아니다.

검증하려는 것은 다음 작성 원칙이다.

1. description은 routing interface인가.
2. adjacent boundary가 collision을 줄이는가.
3. 지침을 필요한 scope로 옮기면 불필요한 간섭이 줄어드는가.
4. procedure를 Skill로 보내면 항상-on context를 줄일 수 있는가.
5. 모델이 좋아진 뒤 오래된 scaffolding을 제거해도 품질을 유지할 수 있는가.
6. prose rule을 구조적 enforcement로 옮길 때 실제 violation이 줄어드는가.

결과가 예상과 다르면 책의 원칙을 수정한다.

그 자체가 이 실험의 목적이다.
