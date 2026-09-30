# 14장. Trigger Eval

Skill description이 routing interface라면 description도 테스트해야 한다.

“읽어 보니 충분히 명확하다”는 평가는 시작점일 뿐이다.

실제로 필요한 요청에서 호출되는지, 비슷하지만 다른 요청에서는 빠지는지 측정해야 한다.

## 14.1 Trigger Eval이 답하는 질문

- 필요한 요청에서 Skill이 선택되는가.
- 관련 없는 요청에서 선택되지 않는가.
- 인접 Skill 중 올바른 Skill을 고르는가.
- 아무 Skill도 필요 없을 때 abstain하는가.
- 같은 prompt를 반복했을 때 안정적인가.

이 질문은 Skill 본문 품질과 분리한다.

routing eval에서는 body를 최대한 고정하고 description 차이를 본다.

## 14.2 최소 corpus

처음부터 거대한 benchmark가 필요하지 않다.

최소한 여섯 종류를 둔다.

### Explicit positive

Skill 이름이나 작업 의도가 직접 드러난다.

### Implicit positive

Skill 이름 없이 자연스럽게 요청한다.

### Noisy positive

긴 맥락 안에 실제 trigger가 섞여 있다.

### Adjacent negative

표면적으로 비슷하지만 다른 Skill이 맞다.

### Routing pair

둘 이상의 Skill이 관련 있어 보이지만 하나만 정답이다.

### None

어떤 Skill도 필요하지 않다.

positive만 테스트하면 과잉 호출을 찾을 수 없다.

## 14.3 같은 body, 다른 description

description 효과를 보려면 실행 본문을 바꾸지 않는다.

비교 예:

- A0: 길고 넓은 description
- A1: 짧은 what + when
- A1L: 같은 의미를 유지하지만 길이만 늘린 control
- A2: adjacent boundary를 포함
- A3: manual-only

이렇게 하면 길이와 broadness의 영향을 어느 정도 분리해 볼 수 있다.

## 14.4 왜 Length Control이 필요한가

짧은 description이 좋은 결과를 냈다고 해서 원인이 “짧아서”라고 단정할 수 없다.

짧은 버전이 동시에 더 구체적이었을 수 있다.

A1과 같은 trigger 의미를 유지하면서 routing에 필요 없는 설명만 늘린 A1L을 두면 길이 증가 자체의 영향을 더 잘 볼 수 있다.

Eval은 이런 식으로 원인을 분리하는 설계가 필요하다.

## 14.5 지표

### Accuracy

전체 prompt 중 기대 route와 일치한 비율.

### Macro-F1

Skill별 case 수가 다를 때 특정 Skill이 평균을 지배하지 않게 본다.

### False Positive Rate

none 또는 adjacent negative에서 잘못 호출된 비율.

### Collision Error Rate

routing pair에서 인접 Skill을 잘못 고른 비율.

### Abstention Accuracy

아무 Skill도 필요 없을 때 선택하지 않는 정확도.

### Run Consistency

같은 prompt를 여러 번 실행했을 때 같은 결과가 나온 비율.

## 14.6 반복 실행

LLM routing은 완전히 deterministic하지 않을 수 있다.

한 번 성공한 사례를 pass로 끝내지 않는다.

중요한 prompt는 여러 번 실행하고 model, host, version, date를 함께 기록한다.

한 모델의 결과를 모든 host에 일반화하지 않는다.

## 14.7 Manual-only는 별도로 평가한다

manual-only Skill을 auto-trigger 정확도 경쟁에 넣으면 평가 목적이 섞인다.

manual-only에서 확인할 것은 다음이다.

- 자연어 요청에서 자동 호출되지 않는가.
- 사용자가 명시적으로 호출하면 정확히 실행되는가.
- argument contract가 지켜지는가.
- side effect와 approval 경계가 맞는가.

## 14.8 False Positive의 비용

Skill이 호출되지 않는 false negative도 문제지만, 과잉 호출은 더 넓게 시스템을 오염시킬 수 있다.

관련 없는 Skill body가 로드되고 추가 tool call, 검증, 질문, side effect가 발생할 수 있다.

따라서 routing quality는 recall만 보지 않는다.

## 14.9 Failure를 corpus로 승격한다

실제 운영에서 잘못 호출된 요청은 가장 가치 있는 eval case다.

문장을 바로 고치기 전에 해당 prompt를 corpus에 추가한다.

그 다음 description을 수정하고 기존 positive와 negative가 모두 유지되는지 확인한다.

이렇게 하면 correction이 다시 퇴행하지 않는다.

## 14.10 Trigger-Driven Development

좋은 Skill 개발 순서는 다음에 가깝다.

1. 업무 책임을 정의한다.
2. positive와 negative prompt를 만든다.
3. description을 작성한다.
4. routing을 측정한다.
5. 경계를 조정한다.
6. body를 작성한다.
7. output eval을 추가한다.

즉 Skill 개발도 test-first 사고를 적용할 수 있다.

description은 문서 metadata가 아니라 **실행 전 라우터**이기 때문이다.
