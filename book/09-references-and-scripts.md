# 9장. References와 Scripts

Skill이 커질 때 가장 흔한 반응은 SKILL.md에 섹션을 계속 추가하는 것이다.

하지만 세부 정보와 반복 작업을 모두 본문에 두면 Skill은 다시 상시 매뉴얼처럼 변한다.

References와 Scripts는 단순한 파일 분리가 아니라 context와 책임을 분리하는 도구다.

## 9.1 Root Skill은 router에 가깝게

Skill 본문에는 시작 조건, 핵심 workflow, 필요한 분기, 완료 조건이 있어야 한다.

긴 API 규약, 모든 edge case, 상세 예제, 전체 CLI 옵션 표까지 넣을 필요는 없다.

필요한 세부 자료는 reference로 분리한다.

핵심은 본문이 “자세한 내용은 references를 보라”고만 하지 않는 것이다.

언제 어떤 reference를 읽어야 하는지 조건을 적는다.

## 9.2 Reference에 적합한 내용

다음은 reference 후보가 된다.

- 긴 API 규약
- 복잡한 schema
- 예외 사례 목록
- compatibility 정책
- rollout 정책
- 상세 예제
- 장문의 style guide
- 특정 버전 migration notes

이 정보는 매번 필요하지 않다.

## 9.3 Reference depth를 얕게 유지한다

SKILL.md가 reference A를 가리키고, A가 B를 가리키고, B가 다시 C를 가리키면 모델은 필요한 정보를 찾기 위해 깊은 탐색을 해야 한다.

좋은 구조는 진입점에서 필요한 자료를 직접 찾기 쉽다.

긴 reference 자체에는 목차를 둘 수 있지만, reference 체인을 계속 늘리지는 않는다.

## 9.4 Cached CLI Manual

빠르게 변하는 CLI의 옵션과 flag를 SKILL.md에 복제하면 시간이 지나면서 두 개의 truth가 생긴다.

실제 CLI와 Skill의 설명이 어긋나기 시작한다.

이때 더 좋은 source는 상황에 따라 다음이 될 수 있다.

- 설치된 CLI의 help
- generated schema
- installed-version documentation
- 공식 live documentation

Skill은 옵션 전체를 복제하는 대신 **어떤 source를 언제 읽을지** 알려준다.

## 9.5 Latest가 항상 정답은 아니다

빠르게 변하는 framework나 API를 다룰 때 current official docs만 보면 충분하지 않을 수 있다.

기존 프로젝트는 특정 runtime, compatibility date, SDK, type version에 의도적으로 고정되어 있을 수 있다.

따라서 source hierarchy를 둔다.

1. 사용자가 지정한 target
2. 프로젝트 설정의 target
3. 설치된 package와 generated schema
4. 현재 공식 source
5. 날짜가 있는 fallback snapshot

업그레이드 작업과 기존 코드 리뷰는 같은 기준을 사용하지 않는다.

## 9.6 Script가 prose보다 나은 경우

같은 기계적 절차를 매번 자연어로 설명한다면 script 후보다.

예:

- link checker
- Skill reference validator
- formatter
- 반복 변환
- artifact 비교
- schema 검사
- payload 생성

script는 지식을 숨기는 장치가 아니다. 결정론적으로 실행 가능한 부분을 자연어 추론에서 분리하는 장치다.

## 9.7 Script contract

Skill에서 script를 호출하려면 다음이 분명해야 한다.

- 언제 실행하는가.
- 입력은 무엇인가.
- 성공과 실패 exit code가 무엇인가.
- 출력이 무엇을 의미하는가.
- 파일이나 외부 시스템을 변경하는가.
- 재실행해도 안전한가.
- timeout이나 cleanup이 필요한가.

script가 있다고 해서 자동으로 신뢰할 수 있는 것은 아니다.

## 9.8 Executable state machine

복잡한 workflow는 prose 10단계를 길게 설명하기보다 상태를 machine-readable하게 두고 script가 transition을 검증하게 하는 것이 나을 수 있다.

예를 들어 prepare → validated → approved → deployed 같은 workflow에서 어떤 상태를 누가 만들 수 있는지 코드로 검사할 수 있다면 자연어 중복이 줄어든다.

다만 모든 workflow를 state machine으로 만들 필요는 없다. 기계적 판정이 명확하고 상태 충돌이 실제 문제일 때 사용한다.

## 9.9 Canonical source를 복제하지 않는다

디자인 토큰, DB schema, generated type, CI threshold, API contract가 이미 machine-readable source에 있다면 Skill에 값을 다시 적지 않는다.

Skill은 다음을 말하면 된다.

> 이 작업에서는 해당 canonical source를 먼저 읽고, 그 값을 사용한다.

복제하지 않는 것이 최신성을 유지하는 가장 강한 방법이다.

## 9.10 본문과 resource의 경계

SKILL.md에는 라우팅 후 즉시 필요한 판단을 남긴다.

references에는 조건부 상세 지식을 둔다.

scripts에는 결정론적 절차를 둔다.

assets에는 산출물 재료를 둔다.

이 경계가 선명할수록 Skill은 커져도 필요한 순간에 필요한 정보만 읽는 구조를 유지할 수 있다.
