# Instruction File Structural Validator 설계

기준일: 2026-09-30

## 목적

지침 파일 품질을 regex 점수로 평가하는 도구를 만들지 않는다.

validator의 역할은:

> **기계적으로 참/거짓을 판정할 수 있는 structural fact만 검사하는 것**

이다.

다음은 validator가 판정하지 않는다.

- description이 좋은가
- workflow가 합리적인가
- 문장이 전문적인가
- Skill이 실제 task 성능을 높이는가

이것들은 eval/human review 영역이다.

## 검사 계층

1. **Parse** — 파일과 frontmatter가 읽히는가
2. **Local structure** — name, description, reference, script가 일관적인가
3. **Repository graph** — directory, manifest, catalog, allowlist가 맞는가
4. **Portability** — portable core와 provider extension이 충돌하지 않는가
5. **Runtime-risk static checks** — broken path, unsupported matcher, dangling command처럼 정적으로 잡을 수 있는 오류가 있는가

## Severity

### ERROR

실행·발견·파싱을 깨거나 명백한 drift를 만든다.

예:

- YAML parse failure
- required field 없음
- referenced local file 없음
- duplicate registration
- manifest가 없는 Skill을 가리킴

### WARNING

현재는 동작할 수 있지만 debt/portability 위험이 높다.

예:

- description hard limit 근접
- static fallback snapshot에 date/source 없음
- manual-only Skill이 auto-trigger eval에 들어감
- broad permission

### INFO

리팩터링 검토 신호.

예:

- root standing file이 매우 길어짐
- reference depth가 깊음
- CLI option table이 길게 embedded됨
- broad Hook matcher

INFO를 CI hard failure로 만들지 않는다.

# SKILL.md checks

## V001 — SKILL.md exists

Skill로 등록됐는데 `SKILL.md`가 없음. ERROR.

## V002 — YAML frontmatter parses

ERROR.

## V003 — name exists

ERROR.

## V004 — name matches directory policy

repository가 folder=name 정책을 선언한 경우만 검사. ERROR.

모든 repository에 보편 규칙으로 강제하지 않는다.

## V005 — description exists

auto-trigger Skill이면 필수.

- auto-trigger: ERROR
- manual-only: WARNING 또는 repository policy

## V006 — description hard limit

target spec/host hard limit 초과. ERROR.

## V007 — description soft budget

repository가 정한 warning budget을 넘으면 WARNING.

soft budget을 quality score로 사용하지 않는다.

## V008 — local references exist

repository-relative link가 실제 파일을 가리키는지 검사. ERROR.

## V009 — script paths exist

본문이 가리키는 local script가 존재하는지 검사. ERROR.

## V010 — bundle path escape

Skill bundle policy가 있을 때 `references/`, `scripts/`, `assets/` 밖으로 비정상 escape하는 path를 검사. ERROR/WARNING.

# Registration graph

Skill 하나는 다음 여러 surface에 존재할 수 있다.

- directory
- manifest
- marketplace
- README/catalog
- allowlist
- provider plugin
- generated registry

## V020 — registered Skill exists

manifest가 없는 Skill directory를 가리킴. ERROR.

## V021 — required bidirectional coverage

repository policy가 모든 Skill file의 manifest 등록을 요구할 때 역방향도 검사. ERROR.

## V022 — duplicate registration

동일 name/path 중복. ERROR.

## V023 — duplicate canonical owner

같은 alias group에서 둘 이상이 canonical owner. ERROR.

## V024 — deprecated alias replacement exists

deprecated Skill이 가리키는 replacement가 존재하는지 검사. ERROR.

## V025 — manual-only excluded from auto-trigger eval

eval manifest가 있다면 manual-only Skill이 auto-trigger corpus에 들어가지 않는지 검사. ERROR/WARNING.

# Provider / portability

## V030 — provider extension placement

portable core를 표방하는 repository에서 provider-only field가 dedicated metadata/file에 있는지 검사. WARNING 또는 policy ERROR.

## V031 — allowed-tools tokenization

target loader가 whitespace-separated syntax를 요구할 때 comma-suffixed token을 잡는다.

Sentry의 Host-Tolerated Invalidity 같은 문제를 방지한다. ERROR.

## V032 — unknown allowed tool

known tool schema가 있을 때 unknown token 검사. ERROR/WARNING.

## V033 — broad permission surface

예:

```text
Bash(*)
Read(all)
Write(all)
```

정적으로 탐지 가능하지만 의도 판단이 필요하므로 WARNING.

# Freshness

## V040 — declared snapshot without freshness metadata

snapshot 구조를 사용하는 repository에서 source/date 없이 version snapshot만 있으면 WARNING.

예:

```yaml
metadata:
  snapshot-date: 2026-09-29
  source: https://...
```

일반 prose의 모든 숫자를 regex로 찾지는 않는다.

## V041 — expired fallback snapshot

repository가 TTL을 선언한 경우:

```yaml
metadata:
  snapshot-date: 2026-09-29
  freshness-days: 30
```

TTL 초과 시 WARNING.

## V042 — generated canonical source duplication

generated block/checksum처럼 기계적으로 비교 가능한 경우만 검사한다.

자연어 semantic duplication은 자동 판정하지 않는다.

# Scope

## V050 — scoped matcher matches nothing

path Rule matcher가 현재 repository에서 어떤 file에도 match하지 않으면 WARNING.

## V051 — invalid matcher syntax

target host parser가 받지 못하는 matcher. ERROR.

## V052 — nested instruction orphan

host discovery semantics를 알고 있고 nested file이 discovery되지 않는 위치라면 WARNING/ERROR.

## V053 — parent/child explicit rule-id duplication

자연어 similarity가 아니라 명시적 `rule-id`가 parent/child 양쪽에 중복된 경우만 검사. WARNING.

# Hook / enforcement

## V060 — referenced Hook command exists

ERROR.

## V061 — Hook script parse/basic execution check

가능한 범위에서 syntax 확인. ERROR.

## V062 — unsupported event/matcher

target host schema가 알려진 경우. ERROR.

## V063 — blocking Hook without test fixture

repository policy가 blocking Hook test를 요구하는 경우 ERROR/WARNING.

## V064 — broad Hook matcher

모든 tool call을 잡는 식의 넓은 matcher. WARNING.

## V065 — equivalent command-set coverage

publish-class command set을 machine-readable policy로 관리한다면 Hook이 전체 set을 cover하는지 검사. ERROR.

# State / completion

이 영역은 semantic lint로 오버리치하기 쉽다.

machine-readable contract가 있을 때만 검증한다.

예:

```yaml
metadata:
  workflow:
    state-file: .deploy/state.json
    owns-states:
      - Validated
    requires-states:
      - Approved
```

## V070 — state-file contract valid

declared path/schema가 유효한지 검사. ERROR.

## V071 — state owner collision

둘 이상의 Skill이 동일 exclusive state를 소유. ERROR.

## V072 — missing prerequisite state owner

required state가 있는데 해당 state를 생산/소유하는 workflow가 등록되지 않음. WARNING.

## V073 — invalid transition graph

declared transition graph가 repository policy와 충돌. WARNING/ERROR.

# 금지할 validator anti-pattern

## A. MUST 개수로 품질 판정

`MUST`가 많다고 나쁜 Skill로 처리하지 않는다.

## B. line count hard fail

`SKILL.md > 500 lines = fail` 같은 보편 hard rule은 두지 않는다.

line count는 refactor signal이지 correctness criterion이 아니다.

## C. negative wording 금지

`don't`, `never`가 있다고 fail하지 않는다.

실제 safety/boundary에는 필요하다.

## D. description keyword stuffing regex

단어 수만 보고 trigger quality를 판정하지 않는다.

routing eval에서 측정한다.

## E. generic best-practice detector

semantic lint overreach다.

LLM judge로 CI hard fail을 만드는 것도 신중해야 한다.

# Validator와 Eval의 경계

## Validator가 답하는 질문

- 파일이 있는가
- parse되는가
- registration이 맞는가
- reference가 존재하는가
- metadata가 target spec에 맞는가
- machine-readable state owner가 충돌하는가
- Hook event/matcher가 schema에 맞는가

## Eval이 답하는 질문

- 올바른 prompt에서 trigger되는가
- adjacent negative에서 abstain하는가
- procedure를 실제로 따르는가
- output이 좋아지는가
- token/time/tool-call 비용이 합리적인가
- 새 model에서도 old workaround가 필요한가

## Human review가 답하는 질문

- 이 Skill이 존재할 가치가 있는가
- 이 규칙은 repository 실제 risk와 맞는가
- user intent threshold가 적절한가
- 이 detail을 Skill body에 둘 가치가 있는가
- 삭제할 지침은 무엇인가

# 권장 validator config

```yaml
version: 1

skills:
  roots:
    - skills
  name_matches_directory: true
  description:
    warning_chars: 950
    error_chars: 1024

registration:
  manifests:
    - .claude-plugin/marketplace.json
  require_bidirectional_coverage: true

references:
  check_local_links: true

portability:
  agent_skills_core: true

hooks:
  require_tests_for_blocking: true

snapshots:
  require_date_when_declared: true
```

repository가 사용하지 않는 정책은 기본 활성화하지 않는다.

# 권장 출력

```text
ERROR V008 skills/foo/SKILL.md:42
  Missing local reference: references/setup.md

WARNING V041 skills/upgrade/SKILL.md
  Fallback snapshot is 46 days old; declared freshness is 30 days.

WARNING V033 skills/deploy/SKILL.md
  Broad tool permission: Bash(*)

INFO V080 CLAUDE.md
  Standing instruction is 287 lines. Review whether local sections can move.
```

# CI 배치

## PR fast gate

- parse
- local references
- manifest coverage
- duplicate registration
- spec fields
- Hook syntax
- state metadata

## Optional slower job

- external link check
- generated registry consistency
- provider packaging smoke test

## Manual / separate eval

- trigger routing
- output quality
- model/host regression

LLM key가 없다고 deterministic validator까지 CI에서 빼면 안 된다.

반대로 LLM eval을 CI에 넣을 수 있다고 structural validator를 LLM judge로 대체해서도 안 된다.

# 핵심 문장

> **Validator는 지침의 의미를 평가하는 도구가 아니다. 지침 시스템에서 사람이 판단할 필요가 없는 오류를 제거하는 도구다.**

> **정확히 판정할 수 없는 것을 hard fail로 만들지 않는 것이 좋은 validator의 중요한 품질이다.**
