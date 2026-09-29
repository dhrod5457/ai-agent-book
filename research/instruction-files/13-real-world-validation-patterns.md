# 실제 저장소의 지침 파일 Validation / Eval 패턴

## 1. 왜 이 자료를 별도로 모으는가

지침 파일을 "잘 쓰는 법"만 설명하면 결국 스타일 가이드가 된다.

실제 운영에서는 다음 문제가 더 중요하다.

- frontmatter가 깨짐
- folder name과 skill name 불일치
- referenced file 누락
- marketplace 등록 누락
- description이 너무 길어짐
- built-in command와 이름 충돌
- description 변경으로 trigger가 달라짐
- Skill 구조 개선이 실제 산출물 품질을 악화시킴

이 문제를 실제 저장소가 어떻게 검증하는지 수집했다.

# Case 1. duthaho/skillhub

## 2. 두 층으로 validation을 분리한다

`skillhub/evals/README.md`는 검증을 명시적으로 두 층으로 나눈다.

### Layer 1. Mechanical validation

결정론적으로 검사 가능한 것을 Python validator가 확인한다.

### Layer 2. Trigger eval

description의 routing 품질은 별도의 fresh model judge로 평가한다.

이 분리가 중요하다.

> 구조적으로 참/거짓인 문제와, semantic routing 문제를 같은 validator로 해결하려 하지 않는다.

Source:
https://github.com/duthaho/skillhub/blob/main/evals/README.md

## 3. Mechanical validator가 검사하는 항목

`scripts/validate-skills.py`에서 확인되는 항목:

- Skill directory에 `SKILL.md`가 있는가
- YAML frontmatter가 parse 가능한가
- `name`이 존재하는가
- `name`이 folder name과 같은가
- harness built-in command와 이름이 충돌하지 않는가
- `description`이 존재하는가
- description이 1024자 이하인가
- references에 언급된 파일이 실제 존재하는가
- marketplace path가 실제 존재하는가
- 모든 Skill이 marketplace에 등록되어 있는가
- duplicate registration이 없는가
- README table에 모든 Skill이 노출되어 있는가

validator가 하지 않는 것:

- Skill이 실제로 좋은가
- description trigger가 semantic하게 맞는가
- workflow가 유용한가
- prose가 적절한가

이 구분 자체가 좋은 설계 원칙이다.

Source:
https://github.com/duthaho/skillhub/blob/main/scripts/validate-skills.py

## 4. Description을 실제 routing surface로 추출한다

validator에는 `--descriptions` 모드가 있다.

동작:

1. structural failure가 있으면 description dump 자체를 거부한다.
2. valid frontmatter만 사용한다.
3. `disable-model-invocation`인 Skill은 제외한다.
4. model-visible `{name: description}` JSON을 만든다.

즉 eval input이 실제 routing surface를 최대한 비슷하게 모사한다.

이 패턴은 다른 Skill repository에도 재사용할 수 있다.

## 5. Trigger eval은 body를 보여주지 않는다

`skillhub`의 trigger eval에서 judge에게 주는 것은:

- description 목록
- organic user prompts
- 기대 Skill

judge instruction은 각 prompt에서 하나의 Skill 또는 `none`을 고르는 것이다.

이 방식이 좋은 이유:

- body 품질과 routing 품질이 섞이지 않는다.
- Skill 이름을 직접 부르는 synthetic prompt가 아니라 실제 사용자가 쓸 법한 문장을 사용한다.
- fresh sub-agent를 사용해 다른 context 영향을 줄인다.

## 6. Routing pair를 명시한다

`evals/triggers.json`에서 특히 좋은 부분은 단순 positive case 외에 **비슷한 Skill 두 개가 경쟁하는 사례**가 들어간다는 점이다.

예:

- map / blueprint
- feature / bugfix
- pulse / verdict
- priorart / verdict
- scout / verdict
- ideate / priorart
- revisit / daybrief
- tune / cachewise

각 case에는 때때로 `route` 설명이 붙는다.

이 자료는 다음 원칙을 강하게 뒷받침한다.

> Skill trigger eval에서 어려운 문제는 "호출되느냐"가 아니라 "비슷한 후보 중 정확한 하나를 고르느냐"다.

Source:
https://github.com/duthaho/skillhub/blob/main/evals/triggers.json

## 7. Description authoring lint

`skillhub`는 description 작성 규칙도 별도로 둔다.

핵심:

- invocation에 중요한 leading concept를 앞에 둔다.
- 하나의 trigger branch를 synonym으로 반복하지 않는다.
- body에 있는 mechanism detail을 description에 다시 쓰지 않는다.
- 삭제해도 behavior가 안 바뀌는 no-op sentence를 지운다.
- negation만 쓰지 말고 replacement behavior를 함께 적는다.

이것은 단순 "짧게 쓰라"보다 훨씬 실전적인 기준이다.

# Case 2. getsentry/skills

## 8. Skill 작성 자체를 canonical Skill로 만든다

`getsentry/skills`는 repository AGENTS.md에서 Skill 생성/수정 시 `/skill-writer`를 사용하도록 한다.

`skill-writer`는 다음을 한 workflow로 묶는다.

- source 수집
- 작성
- description 개선
- reference 구조 결정
- registration
- validation
- eval
- maintenance artifact

Source:
https://github.com/getsentry/skills/blob/main/skills/skill-writer/SKILL.md

이 접근의 의미:

> Skill 작성 규칙을 여러 문서에 흩어 놓기보다, Skill을 만드는 절차 자체를 재사용 가능한 executable instruction으로 만든다.

## 9. SKILL.md를 router로 정의한다

`getsentry/skills/skills/skill-writer/SKILL.md`는 root SKILL을 큰 reference 본문으로 쓰지 않는다.

대신 "언제 어떤 reference를 열어야 하는가"를 표로 제공한다.

예:

- mode selection이 필요할 때
- execution shape가 필요할 때
- source discovery가 필요할 때
- description optimization이 필요할 때
- eval 작성이 필요할 때
- registration validation이 필요할 때

핵심 원칙:

> flat reference + direct open-when routing.

이 방식은 progressive disclosure를 구조적으로 표현한다.

## 10. Runtime Skill과 maintainer eval을 분리한다

`skills/skill-writer/EVAL.md` 첫 부분에서 eval 파일은 maintainer용이며 runtime `SKILL.md`에서 링크하지 말라고 명시한다.

이 분리가 중요한 이유:

- Skill을 실행할 때 eval 방법론을 매번 context에 넣지 않는다.
- runtime behavior와 maintenance behavior를 분리한다.
- eval은 개발자 도구이고 사용 workflow가 아니다.

책에서 다음 원칙으로 일반화할 수 있다.

> 실행 시 필요한 지식과, 그 지식을 검증/유지하는 지식은 별도 artifact로 관리한다.

Source:
https://github.com/getsentry/skills/blob/main/skills/skill-writer/EVAL.md

## 11. Eval을 실제 coding agent harness로 실행한다

`skill-writer/EVAL.md`는 AXIS를 사용한다.

평가 대상:

- trigger
- structure
- generated quality
- regression
- timing/token/interaction waste

관찰 가능한 evidence:

- 생성 파일
- 금지 파일 부재
- validation output
- transcript
- artifact
- baseline comparison

subjective dimension은 LLM judge와 human review를 함께 사용한다.

## 12. Baseline과 holdout을 둔다

`skill-writer` eval은 일회성 점수보다 baseline 비교를 권장한다.

또한 반복 regression이 생기면 holdout example을 유지한다.

Adoption gate에는 다음이 포함된다.

- critical dimension regression 없음
- 변경 목적과 관련된 target dimension 개선
- structural validation 통과
- runtime Skill의 router 구조 유지

이는 Skill 변경을 일반 코드 변경과 비슷한 regression 관리 대상으로 보는 접근이다.

## 13. Eval dimension

getsentry가 사용하는 평가 축은 책의 품질 모델로 재사용 가치가 높다.

- trigger precision
- artifact minimality
- runtime concision
- source coverage
- progressive disclosure
- validation
- portability

특히 **artifact minimality**는 중요하다.

Skill 품질을 "내용이 많을수록 좋다"가 아니라:

> 생성/유지하는 파일 각각이 명확한 runtime, validation, source, maintenance 역할을 갖는가

로 평가한다.

## 14. Structural validator의 한계를 명시한다

`registration-validation.md`는 validator가 구조 검사일 뿐 semantic completeness를 증명하지 못한다고 명시한다.

자동 검사하지 않는 항목:

- skill class 판단
- source coverage quality
- trigger quality
- qualitative guidance

이런 항목까지 regex로 강제하면 false positive가 늘 수 있다.

책에서 매우 중요한 원칙:

> 자동화는 자동으로 정확히 판정 가능한 것까지만 강제한다.

# 두 사례에서 공통으로 추출되는 구조

## 15. Three-layer Quality Model

### Layer A. Structural validation

기계적으로 판정:

- syntax
- path
- registration
- reference integrity
- naming
- deterministic constraints

### Layer B. Behavioral eval

실제 agent를 실행:

- trigger
- workflow
- artifact
- output
- efficiency
- negative cases

### Layer C. Human review

여전히 사람이 판단:

- usefulness
- clarity
- overfitting
- taste
- surprising omission
- whether the skill solves the actual task

이 세 층을 섞지 않는 것이 핵심이다.

# 책에서 만들 수 있는 실전 도구

## 16. instruction-lint

책 companion repository에서 만들 수 있는 validator 후보:

### CLAUDE/AGENTS

- broken relative link
- 존재하지 않는 command/path
- absolute user-specific path
- duplicated exact rule
- stale date/version metadata warning
- 파일 줄 수 warning

### SKILL.md

- frontmatter parse
- name/folder mismatch
- description 존재/길이
- provider-specific field 표시
- referenced file existence
- deep reference chain warning
- manual-only/auto-trigger consistency
- script path existence

### Rules

- supported frontmatter
- glob/path syntax
- alwaysApply와 glob 조합
- referenced canonical doc existence

## 17. trigger-eval fixture

책에서 제공할 최소 fixture:

```json
[
  {"prompt": "...", "expect": "skill-a"},
  {"prompt": "...", "expect": "skill-a"},
  {"prompt": "...", "expect": "none"},
  {"prompt": "...", "expect": "skill-b", "route": "not skill-a"}
]
```

이 구조를 Claude, Codex, Gemini 등에 같은 방식으로 적용해 routing portability를 비교할 수 있다.

# 핵심 결론

이번 추가 수집에서 가장 중요한 발견은 다음이다.

1. 지침 파일 validation은 이미 실제 프로젝트에서 **코드처럼 CI 대상**이 되고 있다.
2. structural lint와 semantic eval을 분리하는 것이 핵심이다.
3. description은 실제 routing surface이므로 별도 regression test가 필요하다.
4. positive case보다 인접 Skill 간 routing pair가 더 가치 있는 경우가 많다.
5. Skill runtime 지침과 maintainer eval 지침은 분리하는 편이 context 효율에 유리하다.
6. baseline, holdout, artifact evidence를 사용하면 Skill 수정도 일반 소프트웨어 regression처럼 관리할 수 있다.

## 원문

- https://github.com/duthaho/skillhub/blob/main/evals/README.md
- https://github.com/duthaho/skillhub/blob/main/evals/triggers.json
- https://github.com/duthaho/skillhub/blob/main/scripts/validate-skills.py
- https://github.com/getsentry/skills/blob/main/AGENTS.md
- https://github.com/getsentry/skills/blob/main/skills/skill-writer/SKILL.md
- https://github.com/getsentry/skills/blob/main/skills/skill-writer/EVAL.md
- https://github.com/getsentry/skills/blob/main/skills/skill-writer/references/skill-evals.md
- https://github.com/getsentry/skills/blob/main/skills/skill-writer/references/registration-validation.md
