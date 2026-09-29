# 지침 파일 평가와 Skill Smell 리서치

## 1. 왜 별도의 평가 장이 필요한가

지침 파일은 자연어라서 code review만으로 품질을 판정하기 쉽다고 느끼지만 실제로는 그렇지 않다.

문장이 좋아 보여도 다음 문제가 발생할 수 있다.

- Skill이 필요한 요청에서 trigger되지 않는다.
- 관련 없는 요청에서 trigger된다.
- 본문은 읽었지만 중요한 단계가 누락된다.
- 긴 지침 때문에 다른 중요한 context가 희석된다.
- 특정 모델에서는 도움이 되지만 다른 모델에서는 방해가 된다.
- 지침이 없을 때보다 token과 작업량만 증가한다.
- 오래된 workaround가 최신 모델을 과도하게 구속한다.

따라서 instruction file은 "실행 가능한 specification"처럼 평가해야 한다.

## 2. 평가를 routing과 execution으로 분리한다

### Routing eval

질문:

- 필요한 요청에서 Skill/Rule이 적용되는가.
- 적용하지 않아야 할 요청에서 빠지는가.

지표 후보:

- trigger recall
- false positive rate
- false negative rate

### Execution eval

질문:

- 적용된 뒤 목표 행동이 실제로 수행되는가.
- 필요한 artifact가 생성되는가.
- 금지 행동을 피하는가.
- 불필요한 step을 추가하지 않는가.

## 3. OpenAI의 Skill eval 패턴

OpenAI의 2026 Skill eval 가이드는 성공 조건을 먼저 쓰고 다음을 구분한다.

- Outcome goals
- Process goals
- Style goals
- Efficiency goals

그리고 prompt set에 positive와 negative control을 함께 넣는다.

이 구조는 제품에 상관없이 사용할 수 있다.

## 4. 최소 테스트 세트

하나의 Skill마다 처음부터 거대한 benchmark가 필요하지 않다.

최소 후보:

| 유형 | 목적 |
| --- | --- |
| explicit positive | Skill 이름을 직접 불렀을 때 동작 |
| implicit positive | 자연어 요청만으로 올바르게 선택 |
| noisy positive | 주변 맥락이 있어도 핵심 trigger 탐지 |
| adjacent negative | 비슷하지만 대상이 아닌 요청에서 미선택 |
| ambiguous boundary | 경계 사례에서 의도한 방식으로 처리 |
| partial precondition | 일부 조건이 없을 때 적절히 skip/fallback |

실제 failure가 발생할 때마다 회귀 사례를 추가한다.

## 5. baseline이 반드시 필요하다

Skill이 있는 결과만 보고 "잘 됐다"고 판단하면 안 된다.

최소 비교:

- without Skill
- with Skill

더 엄격한 비교:

- current Skill
- proposed Skill
- length-matched irrelevant instruction
- 다른 model

왜 필요한가:

- 모델 자체가 이미 문제를 잘 풀 수 있다.
- Skill이 결과를 바꾸지 않고 token만 늘릴 수 있다.
- 개선처럼 보이는 차이가 지침 내용이 아니라 단순 context length 변화 때문일 수 있다.

## 6. self-report를 증거로 쓰지 않는다

"나는 Skill을 따랐다"라는 모델의 설명은 실행 증거가 아니다.

가능하면 확인한다.

- 실제 tool trace
- 읽은 파일
- 실행한 command
- 생성 artifact
- git diff
- test result
- structured event log

pstack eval playbook도 candidate 자기 보고가 아니라 transcript와 output을 확인한다.

## 7. blinded comparison

지침 A와 B를 비교할 때 judge가 어느 것이 새 버전인지 알면 편향될 수 있다.

가능하면:

- candidate prompt에 실험 목적을 노출하지 않는다.
- 같은 organic user request를 사용한다.
- candidate에게 rubric을 주지 않는다.
- judge에게 model/variant 이름 대신 중립 label을 준다.
- 동일 rubric으로 한 번에 비교한다.

## 8. 연구: From Anatomy to Smells

2026년 7월 preprint:

**From Anatomy to Smells: An Empirical Study of SKILL.md in Agent Skills**

연구 개요:

- 실제 Skill 238개 정성 분석
- 13개 상위, 44개 하위 semantic component taxonomy
- 29개 자료의 multivocal literature review
- best practice 위반을 "skill smells"로 정의
- 자동 detector를 실제 Skill에 적용

주요 보고:

- 분석 대상의 99% 이상에서 최소 하나의 skill smell 발견
- smell이 한 번 들어오면 이후 진화 과정에서도 잘 사라지지 않는 경향

의미:

- Skill 품질 문제는 일부 초보자의 예외가 아니라 유지보수 문제일 수 있다.
- lint와 automated review의 연구 가치가 크다.

주의:

- preprint이므로 peer-reviewed 확정 결과처럼 표현하지 않는다.
- detector가 정의한 smell이 실제 성능 저하와 항상 1:1로 연결된다고 가정하지 않는다.

Source:
- https://arxiv.org/abs/2607.01456

## 9. 연구: 재사용성을 막는 결함

2026년 8월 preprint:

**What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files**

대상:

- 138,133개 공개 SKILL.md
- 20,556개 repository

보고된 결과:

- 91.8%에서 하나 이상의 탐지 결함
- dominant failure는 이국적인 공격보다 일반적 packaging 문제
  - weak routing metadata
  - bloated/non-actionable body
  - poor resource organization
- valid routing metadata가 있는 Skill이 routing stress test에서 더 안정적으로 retrieval됨

연구가 제안하는 방향:

- spec-aware prompting
- lightweight lint
- automated repair
- safety gating

Source:
- https://arxiv.org/abs/2608.08453

## 10. 연구: Skill은 항상 성능을 높이지 않는다

2026년 8월 preprint:

**Signal or Noise? A Benchmark Study of Agent Skills in Web Development**

연구 설정:

- 31개 공개 WebDev Skill
- 50개 Web-Bench project
- 1,000 ordered task
- 4개 model
- length-matched irrelevant control 포함

보고된 결과:

- target Skill injection이 평균 Pass@2를 1.3~4.2% 낮춘 조건
- token cost 72~394% 증가
- Skill-project pair 중 이득이 관찰된 비율은 17~36%
- 일부 모델은 길이에 방해받고, 일부는 Skill 내용 자체에 잘못 유도됨
- 유용한 Skill 안에서는 anti-pattern rule이 example-heavy content보다 나은 경향 보고

이 연구의 핵심 메시지:

> Skill이 "관련 있다"는 것만으로 주입 가치가 보장되지 않는다.

책에서 중요한 이유:

- 무조건 많은 Skill 설치를 권장하면 안 된다.
- context cost를 실제로 측정해야 한다.
- model별 audit가 필요하다.
- routing 자체가 품질 문제다.

주의:

- web development라는 특정 domain의 preprint이다.
- 다른 domain/agent/product로 수치를 그대로 일반화하면 안 된다.

Source:
- https://arxiv.org/abs/2608.23067

## 11. 연구: GitSkills dataset

2026년 8월 preprint:

**GitSkills: A Dataset of Agent Skills on GitHub**

수집 보고:

- 2026년 7월 기준 3,797,117개의 SKILL.md occurrence
- 282,200개 public repository
- 1,877,981개 distinct content

이 자료는 Skill이 이미 대규모 소프트웨어 아티팩트가 되었고, 복제와 유지보수 문제를 연구할 수 있음을 보여준다.

Source:
- https://arxiv.org/abs/2608.10906

## 12. 연구: interaction trajectory에서 Skill 생성

2026년 6월 preprint:

**Automating SKILL.md Generation for Computer-Using Agents via Interaction Trajectory Mining**

연구는 interaction trajectory를 segment하고 cluster해 candidate skill을 추출하는 방식을 탐구한다.

이 책에 직접 가져올 수 있는 관점:

- Skill은 처음부터 사람이 상상해서 쓰는 것만이 아니다.
- 실제 반복 작업 trace에서 재사용 procedure 후보를 발견할 수 있다.
- 향후 "실패/성공 기록에서 Skill 후보 추출"이라는 유지보수 workflow를 다룰 수 있다.

Source:
- https://arxiv.org/abs/2606.20363

## 13. 장기 context 연구와 연결

**Lost in the Middle** 연구는 긴 context에서 중요한 정보 위치에 따라 활용 성능이 달라질 수 있음을 보여줬다.

이 연구는 Skill 전용 연구는 아니지만 "context window가 크므로 지침을 많이 넣어도 된다"는 단순 가정을 경계하는 배경 근거로 사용할 수 있다.

Source:
- https://arxiv.org/abs/2307.03172

## 14. 연구에서 도출할 책의 품질 모델

지침 파일 품질을 다음 축으로 평가할 수 있다.

### Discoverability

필요할 때 발견되는가.

### Selectivity

필요하지 않을 때 빠지는가.

### Clarity

문장이 한 가지 의미로 읽히는가.

### Actionability

실행 가능한 행동을 지시하는가.

### Scope fit

전역/경로/Skill/Hook 중 맞는 위치인가.

### Context efficiency

필요 이상의 token을 소비하지 않는가.

### Structural integrity

reference, script, frontmatter가 유효한가.

### Portability

표준과 vendor extension이 구분되는가.

### Verifiability

성공과 실패를 관찰할 수 있는가.

### Maintainability

중복과 충돌 없이 수정 가능한가.

### Model robustness

여러 모델/새 모델에서 과도한 제약이 되지 않는가.

## 15. 향후 실험 후보

책 자체에서 다음 실험을 수행하면 독자적인 근거를 만들 수 있다.

1. 동일 Skill description의 넓은 버전 vs 좁은 버전 trigger 정확도
2. 50줄, 200줄, 500줄 Skill의 수행/토큰 비교
3. example-heavy vs anti-pattern-heavy Skill 비교
4. Skill reference depth 1단계 vs 3단계
5. 전역 CLAUDE.md 300줄 vs path-scoped 분리 버전
6. 자연어 "반드시 lint" vs PostToolUse Hook
7. 같은 Skill을 Claude/Codex/Gemini에서 평가
8. 오래된 model-specific instruction 삭제 전후 비교

이 실험 결과를 책에 포함하면 단순 문서 요약이 아니라 실증적인 작성 가이드가 된다.

## 주요 출처

- OpenAI, Testing Agent Skills Systematically with Evals
  - https://developers.openai.com/blog/eval-skills
- Anthropic, Skill authoring best practices
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Claude Code Skills
  - https://code.claude.com/docs/en/skills
- pstack eval playbook
  - https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md
- From Anatomy to Smells
  - https://arxiv.org/abs/2607.01456
- What Keeps Agent Skills from Being Reusable?
  - https://arxiv.org/abs/2608.08453
- Signal or Noise?
  - https://arxiv.org/abs/2608.23067
- GitSkills
  - https://arxiv.org/abs/2608.10906
- Automating SKILL.md Generation
  - https://arxiv.org/abs/2606.20363
- Lost in the Middle
  - https://arxiv.org/abs/2307.03172
