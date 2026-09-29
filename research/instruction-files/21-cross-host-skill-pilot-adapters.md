# Cross-Host Skill Pilot Adapter 조사

기준일: 2026-09-30

목적: 동일한 `SKILL.md` corpus를 여러 host에서 비교할 때, 각 제품이 Skill을 발견·자동 선택·수동 호출·관측하는 방식이 실제로 같은지 확인한다.

중요:

> Agent Skills가 portable하다는 것은 파일 구조의 portable core가 있다는 뜻이지, invocation control과 observability가 모든 host에서 동일하다는 뜻이 아니다.

이 문서는 현재 공식 문서를 기준으로 pilot adapter의 가능 여부를 정리한다.

---

# 1. 비교 표

| Host | 자동 선택 | 명시 호출 | `disable-model-invocation` | 자동 activation 관측 후보 | Pilot 준비도 |
| --- | --- | --- | --- | --- | --- |
| Claude Code | Yes | `/skill-name` | Yes | 공식 plugin eval / skill eval, transcript | 높음 |
| Codex | Yes | `$skill`, `/skills`, 명시 prompt | 공식 문서에서 확인하지 못함 | `codex exec --json` JSONL trace + artifact | 높음 |
| Cursor | Yes | `/skill-name` | Yes | UI/use behavior는 문서화, machine-readable activation event는 추가 검증 필요 | 중간 |
| Gemini CLI | Yes | model의 `activate_skill` | Claude식 field는 공식 문서에서 확인하지 못함 | `activate_skill` tool call + consent | 높음, 단 consent 영향 있음 |
| GitHub Copilot CLI | Yes | `/SKILL-NAME` | Yes | CLI trace/activation event 추가 검증 필요 | 중간 |

이 표에서 "공식 문서에서 확인하지 못함"은 미지원이라고 단정하는 표현이 아니다. 이번 조사 범위의 공식 문서에서 portable하게 의존할 근거를 찾지 못했다는 뜻이다.

---

# 2. Claude Code

Official:
https://code.claude.com/docs/en/skills

## Discovery / activation

Claude Code는:

- Skill description을 보고 자동으로 Skill을 선택할 수 있다.
- 사용자가 `/skill-name`으로 직접 실행할 수 있다.
- full Skill body는 invocation 뒤 context에 들어간다.

## Manual-only

Claude Code extension:

```yaml
disable-model-invocation: true
```

이 경우:

- 사용자는 호출 가능
- Claude는 자동 호출 불가
- description도 Claude context에서 제외
- full body는 사용자가 명시 호출할 때만 로드

공식 문서는 side effect가 있는:

- commit
- deploy
- send-slack-message

같은 workflow에 이 옵션을 예로 든다.

## Eval

Claude 공식 문서는 trigger와 output quality를 분리해서 측정하라고 명시한다.

또:

- plugin skill → `claude plugin eval`
- 단일 Skill iteration → skill-creator eval

방식을 제공한다.

### Adapter 결론

Claude는 A0/A1/A1L/A2뿐 아니라 A3 manual-only control까지 직접 실험하기 가장 쉬운 host다.

---

# 3. Codex

Official sources:

- https://developers.openai.com/blog/eval-skills
- https://developers.openai.com/api/docs/guides/tools-skills
- https://developers.openai.com/plugins/build/skills

## Discovery

OpenAI 공식 Skill 문서는 Codex에서:

- Skill name
- description

이 주요 selection signal이라고 설명한다.

full Skill instructions는 선택 후 읽힌다.

## Explicit invocation

공식 eval 글은 다음을 명시한다.

- `/skills` slash command
- `$skill-name` reference

를 통한 명시적 activation.

Implicit invocation과 negative control을 별도로 테스트할 것을 권한다.

## Trace

Codex eval 공식 글은:

```bash
codex exec --json ...
```

을 사용해 JSONL event stream을 저장하고 deterministic grader를 작성하는 패턴을 제공한다.

문서에서 예시로 드는 observable evidence:

- command 실행
- file 생성
- 순서
- artifact
- structured output

## Manual-only portability

이번 공식 문서 조사에서 Claude/Cursor/Copilot의:

```yaml
disable-model-invocation: true
```

와 동일한 Codex Skill frontmatter guarantee는 확인하지 못했다.

따라서 A3는 Codex에서 같은 파일을 그대로 실행하는 cross-host test가 아니라 별도 host behavior로 취급한다.

### Adapter 결론

A0/A1/A1L/A2 routing은 좋은 대상.

A3 manual-only는 Claude와 같은 semantics를 가정하지 않는다.

---

# 4. Cursor

Official:

- https://cursor.com/docs/skills
- https://cursor.com/docs/hooks

## Discovery

Cursor는 Skill directory를 자동 발견하고 Agent에게 available Skill을 제공한다.

agent는 context에 따라 관련 Skill을 선택한다.

## Explicit invocation

`/skill-name`으로 직접 호출 가능.

## Manual-only

현재 공식 문서:

```yaml
disable-model-invocation: true
```

를 지원한다.

이 경우 automatic application은 막고 slash command 형태로 사용할 수 있다.

## 추가 scope

Cursor Skill은 현재 `paths` field도 지원한다.

예:

```yaml
paths:
  - "**/*.tsx"
  - "packages/ui/**/*.ts"
```

현재 docs는 신규 Skill에는 `paths` 사용을 설명하며 legacy `globs`는 fallback으로 취급한다.

이 부분은 과거 Cursor Rule의 `globs`와 혼동하면 안 된다.

## Observability 문제

공식 Hook 문서는 많은 agent lifecycle event를 제공하지만, 이번 조사에서 **Skill auto-activation 자체를 직접 나타내는 전용 machine-readable Hook event**는 확인하지 못했다.

따라서 routing benchmark에서:

- final answer 자기보고
- 단순 slash UI badge

만으로 automatic activation을 판정하면 안 된다.

### Adapter 결론

기능 비교는 가능하지만 자동화 pilot 전에 activation evidence를 한 번 실제 CLI/IDE에서 검증해야 한다.

이건 제품 기능 부족이라는 결론이 아니라 **측정 도구의 evidence gap**이다.

---

# 5. Gemini CLI

Official:

- https://geminicli.com/docs/cli/skills/
- https://geminicli.com/docs/tools/activate-skill/
- https://geminicli.com/docs/cli/using-agent-skills/

## Lifecycle

Gemini는 lifecycle을 명시적으로 문서화한다.

1. Discovery
2. Activation
3. Consent
4. Injection
5. Execution

startup에는 Skill name과 description만 들어간다.

task가 맞으면 모델이:

```text
activate_skill(name)
```

tool을 호출한다.

사용자가 승인하면:

- SKILL.md body
- folder structure

가 conversation에 추가된다.

## Observability 장점

`activate_skill` 자체가 명시적 tool call이므로 routing 판정 surface가 분명하다.

## 실험에 추가되는 변수

문제는 **activation마다 consent가 존재**한다는 점이다.

반복 eval에서는:

- 승인 여부
- 승인 UI
- session reuse 여부

가 결과에 영향을 줄 수 있다.

따라서 prompt routing 정확도와 activation consent를 분리해서 기록해야 한다.

## Manual-only

Gemini 공식 문서에는:

- Skill enable / disable
- model-driven `activate_skill`

은 명확히 있지만, Claude식 `disable-model-invocation: true`를 Skill frontmatter portable guarantee로 이번 조사에서는 확인하지 못했다.

또 `activate_skill` tool은 모델 전용이며 사용자가 tool 자체를 직접 호출할 수 없다고 문서화돼 있다.

사용자는 자연어로 특정 Skill 사용을 요청할 수 있지만 이는 Claude의 slash-command-only semantics와 동일하지 않다.

### Adapter 결론

A0/A1/A1L/A2에는 매우 좋은 관측 host.

A3는 별도 실험 문제다.

---

# 6. GitHub Copilot CLI

Official:

- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills

## Discovery / auto invocation

Copilot은 prompt와 Skill description을 바탕으로 어떤 Skill을 사용할지 결정한다.

## Explicit invocation

```text
/SKILL-NAME
```

으로 명시 호출 가능.

## Frontmatter

현재 Copilot CLI reference는 다음을 명시한다.

- `name`
- `description`
- `argument-hint`
- `allowed-tools`
- `user-invocable`
- `disable-model-invocation`

따라서 Claude/Cursor와 비슷한 manual-only control을 구성할 수 있다.

## Skill inventory

`copilot skill list --json`은:

- name
- description
- source
- path
- enabled

을 제공한다.

하지만 이것은 **discovery inventory**이지 특정 prompt에서 실제 Skill activation이 일어났다는 증거는 아니다.

### Adapter 결론

A0/A1/A1L/A2/A3 모두 기능적으로 구성 가능.

다만 automatic activation의 machine-readable trace를 pilot 전 추가 확인해야 한다.

---

# 7. Cross-host 실험을 하나의 "portable benchmark"로 만들 때 생기는 문제

## P1. Invocation-control portability

Claude/Cursor/Copilot:

```yaml
disable-model-invocation: true
```

를 공식적으로 지원한다.

Codex/Gemini:

같은 semantics를 이번 공식 문서에서 확인하지 못했다.

따라서 이 field를 Agent Skills portable core라고 설명하면 안 된다.

## P2. Activation evidence portability

Host마다 Skill activation의 증거가 다르다.

- Claude: Skill invocation/eval surface
- Codex: JSONL trace 및 artifact
- Gemini: `activate_skill` tool
- Cursor: 추가 관측 검증 필요
- Copilot: 추가 관측 검증 필요

따라서 "Skill을 사용했는가" grader도 host adapter가 필요하다.

## P3. Consent portability

Gemini는 activation에 사용자 consent가 들어간다.

다른 host와 latency/tool count를 그대로 비교하면 불공정할 수 있다.

## P4. Skill metadata extension

portable core:

- name
- description
- body
- resources

host extension:

- invocation control
- path scope
- tool permission
- custom mode/subagent semantics

을 분리해야 한다.

---

# 8. Pilot Adapter Interface

각 host adapter는 다음 결과를 공통 schema로 반환해야 한다.

```text
host
host_version
model
model_version
prompt_id
variant
run_index
available_skills
selected_skill
activation_observable
activation_evidence
consent_required
consent_result
body_loaded
tokens
latency
raw_trace_path
```

## selected_skill 판정 우선순위

1. host-native activation event/tool call
2. structured trace에서 Skill body/path loading 증거
3. host-native eval result
4. 명시적인 deterministic instrumentation

다음은 사용하지 않는다.

- 모델의 최종 답변 자기보고만으로 판정
- 결과가 Skill 스타일과 비슷하다는 이유로 추측

---

# 9. A3 Manual-only 실험을 분리해야 하는 이유

A0/A1/A1L/A2는 공통 질문이다.

> 자동 Skill routing description 품질은 어떤가.

A3는 다른 질문이다.

> 이 host는 사용자가 timing을 통제하는 Skill을 어떤 primitive로 제공하는가.

따라서 책에서도 분리하는 편이 맞다.

### Portable authoring question

- 언제 자동 Skill이어야 하는가.
- 언제 explicit-only가 적절한가.

### Vendor implementation question

- Claude: `disable-model-invocation`
- Cursor: `disable-model-invocation`
- Copilot CLI: `disable-model-invocation`
- Gemini: enable/disable + model `activate_skill` + consent
- Codex: 현재 공식 동작에 맞는 별도 explicit-control 방법을 사용하고, Claude field를 portable하다고 가정하지 않음

---

# 10. 현재 실험 순서 수정

기존 계획:

1. 모든 host 동시 실행

수정:

### Phase A

Claude Code + Codex + Gemini CLI

이유:

- automatic routing을 비교할 수 있는 공식/구조적 observability가 상대적으로 명확

### Phase B

Cursor + Copilot CLI

먼저 한두 prompt로 activation evidence를 확정한 뒤 전체 corpus 실행.

### Phase C

manual-only control

각 host의 native primitive를 사용해 별도 표 작성.

---

# 11. 책에 추가할 핵심 원칙

이번 조사로 한 가지 원칙을 추가한다.

> **Portable Skill은 portable file format이지 portable runtime semantics가 아니다.**

따라서 Skill 가이드에서는 항상:

1. portable core
2. discovery semantics
3. invocation semantics
4. permission semantics
5. observability/eval semantics

을 분리해야 한다.

같은 `SKILL.md`가 여러 도구에서 읽힌다는 사실만으로 같은 방식으로 trigger되고 강제되고 측정된다고 가정하지 않는다.
