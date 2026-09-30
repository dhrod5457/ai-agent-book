# 5장. Path-scoped Rules

전역 지침을 줄이는 가장 직접적인 방법은 규칙을 실제 적용 경로로 내리는 것이다.

백엔드 규칙은 백엔드에서만, 문서 규칙은 문서에서만, 배포 규칙은 배포 파일에서만 보이게 한다.

## 5.1 왜 path scope가 필요한가

모노레포에는 Java backend, TypeScript frontend, infrastructure, docs, mobile이 함께 있을 수 있다. 각 영역의 테스트 도구와 규칙이 다르다.

이 모든 내용을 root instruction에 넣으면 어떤 작업에서도 모든 규칙이 노출된다. 모델은 관련 없는 규칙을 무시해야 하고 때로는 잘못 적용한다.

path scope는 불필요한 선택지를 줄인다.

## 5.2 제품별 문법보다 먼저 책임을 정한다

Claude, Cursor, Copilot, nested AGENTS.md는 서로 다른 문법으로 scope를 표현한다. 하지만 먼저 정해야 할 것은 책임이다.

좋은 path rule은 다음 질문에 답할 수 있어야 한다.

> 이 규칙이 이 경로 밖에서는 왜 필요하지 않은가.

답이 없다면 path rule이 아니라 전역 규칙일 수 있다.

## 5.3 하나의 Rule에는 하나의 주제

Rule 파일을 작게 나누면 적용 이유가 명확해지고 matcher를 좁힐 수 있으며 변경 영향 범위가 줄어든다.

“backend rule” 하나에 DB, API, 테스트, 문서 규칙을 모두 넣기보다 실제 scope가 다르면 더 나눈다.

## 5.4 Style guide를 Rule로 복제하지 않는다

formatter나 linter가 이미 판정하는 스타일을 자연어 Rule로 다시 적는 것은 중복이다.

Rule이 적합한 것은 기계가 바로 알기 어려운 local invariant다. 예를 들어 특정 패키지는 외부 API 타입을 직접 노출하지 않는다거나, migration 기존 파일은 수정하지 않는다거나, generated 디렉터리는 generator를 통해서만 바꾼다는 정책이 여기에 속한다.

## 5.5 Scope drift

path rule도 시간이 지나면 낡는다. 디렉터리가 이동하고 확장자가 바뀌고 모노레포 구조가 재편되면 matcher가 아무 파일에도 맞지 않을 수 있다.

따라서 structural validator가 matcher 문법, 실제 match 존재 여부, nested instruction 위치를 검사할 가치가 있다.

## 5.6 Parent와 child의 관계

좋은 구조는 같은 정책을 parent와 child에 복제하지 않는다.

root에는 “가장 좁은 충분한 검증부터 수행한다”는 공통 원칙을 두고, backend에는 해당 모듈 테스트, frontend에는 해당 패키지 test/lint처럼 local specialization을 둔다.

## 5.7 완료 기준

path-scoped 설계가 잘 되었는지는 unrelated task에서 local 규칙이 노출되지 않는지, 필요한 path에서 규칙이 빠지지 않는지, parent와 child가 모순되지 않는지, formatter가 잡는 내용이 중복되지 않는지로 확인한다.

path scope의 목적은 파일을 나누는 것이 아니다.

> **작업에 필요한 지침만 작업 가까이에 두는 것**이 목적이다.
