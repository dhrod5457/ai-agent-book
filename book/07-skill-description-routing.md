# 7장. description이 Skill의 절반이다

Skill 작성에서 가장 과소평가되는 부분은 본문이 아니라 description이다.

description은 소개 문장이 아니다. 모델이 수많은 Skill 후보 중 무엇을 선택할지 판단하는 **라우팅 인터페이스**다.

## 7.1 무엇을 하는가와 언제 쓰는가

좋은 description은 두 질문에 답한다.

- 이 Skill은 무엇을 하는가.
- 어떤 요청에서 사용해야 하는가.

둘 중 하나만 있으면 부족하다.

“DB 작업을 돕는다”는 무엇을 하는지조차 넓고, 언제 쓰는지 알 수 없다.

“migration을 추가하거나 수정하거나 rollout을 검토할 때 사용한다”는 실제 작업 유형을 trigger로 제공한다.

## 7.2 도메인을 trigger로 쓰지 않는다

Skill을 과잉 호출시키는 가장 흔한 패턴은 도메인 전체를 trigger로 잡는 것이다.

예:

> 데이터베이스 관련 작업에 사용한다.

이 문장은 query 작성, schema 탐색, migration, 성능 조사, 단순 질문까지 모두 끌어들일 수 있다.

더 좋은 description은 **사건**을 쓴다.

- 새로운 migration을 만든다.
- 기존 migration의 rollout 안전성을 검토한다.
- migration 실패를 복구한다.

Skill은 주제 분류기가 아니라 업무 라우터다.

## 7.3 Adjacent negative

positive trigger만 적으면 인접 Skill과 충돌할 수 있다.

feature, bugfix, refactor, review를 예로 들어보자.

“코드를 변경할 때 사용한다”는 네 Skill 모두에 적용될 수 있다.

경계를 더 명확하게 하려면 가까운 반례를 생각해야 한다.

- 이미 있어야 할 동작이 깨졌다면 bugfix
- 동작 변화 없이 구조만 바꾸면 refactor
- 구현 없이 검토만 하면 review
- 새로운 사용자 동작을 추가하면 feature

이렇게 인접 책임을 구분하면 keyword가 아니라 의도로 라우팅할 수 있다.

## 7.4 Negative boundary는 금지문 목록이 아니다

negative boundary를 작성한다고 “이때 쓰지 마라”를 수십 개 나열할 필요는 없다.

가장 혼동하기 쉬운 경계만 적는다.

좋은 negative boundary는 domain 전체를 막지 않는다. 인접한 잘못된 선택을 줄인다.

예:

> 기존 migration의 동작을 분석만 하는 요청에는 사용하지 않는다. 실제 migration 변경이나 rollout 검토에서 사용한다.

## 7.5 Keyword stuffing

description에 가능한 모든 동의어와 키워드를 넣으면 recall이 좋아질 것 같지만 항상 그렇지 않다.

문제가 되는 이유는 세 가지다.

첫째, 다른 Skill과 metadata가 비슷해진다.

둘째, routing에 필요 없는 실행 세부사항이 항상 노출된다.

셋째, 넓은 단어가 false positive를 만든다.

description은 검색 엔진용 SEO 문구가 아니다.

## 7.6 Skill inventory 전체를 함께 본다

새 Skill의 description만 보고 품질을 판단하면 안 된다.

설치된 Skill들은 서로 경쟁한다.

따라서 리뷰할 때 다음을 묻는다.

- 이 요청은 A와 B 중 어디로 가야 하는가.
- description만 보고 그 차이를 알 수 있는가.
- 둘 다 호출되어야 하는 경우가 있는가.
- 둘 다 호출되면 안 되는 요청은 무엇인가.
- 아무 Skill도 선택하지 않는 none 상태가 가능한가.

Skill 수가 늘어날수록 개별 문장보다 inventory 전체의 분리도가 중요하다.

## 7.7 Manual-only Skill

배포, 비용 발생, destructive operation처럼 명시적 호출이 필요한 Skill은 자동 routing 경쟁에서 빼는 것이 더 안전할 수 있다.

manual-only Skill은 자연어 trigger 정확도를 높이는 대신, 사용자가 명시적으로 시작한다는 계약을 가진다.

이 경우 중요한 것은 auto-trigger eval에서 제외하고, explicit invocation과 argument contract를 검증하는 것이다.

## 7.8 Description budget

짧다고 무조건 좋은 것은 아니다.

중요한 branch를 지나치게 줄이면 필요한 Skill이 호출되지 않는다. 실제 공개 Skill 유지보수에서도 router와 description을 줄인 뒤 중요한 adoption trigger가 사라져 다시 복구한 사례가 있다.

따라서 목표는 최소 길이가 아니다.

> 필요한 경계를 보존하면서 불필요한 설명을 제거하는 것.

## 7.9 Trigger-Driven Development

Skill을 먼저 쓰고 나중에 trigger를 생각하지 않는다.

description 초안을 만들기 전에 최소한 다음 요청을 준비한다.

- 명시적 positive
- 자연스러운 implicit positive
- 긴 맥락 속 noisy positive
- adjacent negative
- ambiguous routing pair
- none

이 사례를 먼저 작성하면 description이 실제 업무 경계를 표현하는지 확인하기 쉽다.

## 7.10 좋은 description의 완료 기준

좋은 description은 멋지게 읽히는 문장이 아니다.

같은 prompt corpus를 반복했을 때 필요한 Skill을 안정적으로 고르고, 인접 요청에서는 빠지고, none 상황에서 억지로 선택되지 않을 때 좋은 description이다.

결국 description 품질은 문장 평가가 아니라 **라우팅 결과**로 판단해야 한다.
