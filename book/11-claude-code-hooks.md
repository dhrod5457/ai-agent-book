# 11장. Claude Code Hook 작성

Claude Code Hook은 지침 파일 시스템에서 특별한 위치를 가진다.

CLAUDE.md와 Skill은 모델 행동을 유도하지만, Hook은 특정 lifecycle event에 따라 실제 command나 검사를 실행할 수 있다.

따라서 Hook은 더 결정론적이면서 더 위험하다.

## 11.1 먼저 event를 좁힌다

Hook을 만들 때 가장 먼저 정해야 하는 것은 “무슨 코드를 실행할까”가 아니다.

어떤 event에서 필요한가를 정한다.

모든 tool call을 감시하는 Hook은 구현하기 쉽지만 비용과 false positive가 크다.

Edit나 Write 이후에만 필요한 검사라면 그 event에 좁힌다. 특정 tool namespace에만 필요한 정책이라면 해당 matcher에 제한한다.

## 11.2 Matcher는 정책의 일부다

matcher가 넓으면 좋은 script도 잘못된 순간에 실행된다.

반대로 matcher가 실제 tool semantics와 맞지 않으면 Hook이 존재하지만 아무것도 막지 못할 수 있다.

따라서 matcher는 다음을 검증한다.

- exact match인가 regex인가.
- anchor가 필요한가.
- 해당 event가 matcher를 지원하는가.
- positive event에서 실행되는가.
- near-match에서는 실행되지 않는가.

지원되지 않는 matcher가 조용히 무시되는 종류의 설정은 특히 위험하다.

## 11.3 Hook은 사용자 권한으로 실행된다

command Hook은 단순한 프롬프트보다 높은 신뢰 수준이 필요하다.

repository에서 전달되는 input을 그대로 shell에 넣지 않는다.

최소한 다음을 고려한다.

- 입력 sanitize
- 변수 quoting
- path traversal
- absolute path 사용
- secret과 .git 같은 민감 경로
- destructive command
- timeout
- workspace trust

신뢰하지 않는 저장소의 committed Hook을 검토 없이 실행하는 것은 공급망 위험이 될 수 있다.

## 11.4 출력과 exit code도 계약이다

Hook의 성공과 실패가 소비자에게 어떻게 전달되는지 명확해야 한다.

정해야 할 항목은 다음과 같다.

- stdin 구조
- exit code 의미
- stdout과 stderr 의미
- blocking 여부
- 실패 메시지
- 재실행 안전성
- timeout
- async 여부

“실패하면 뭔가 출력한다”는 정도로는 운영하기 어렵다.

## 11.5 Idempotency

async Hook이나 빠르게 반복되는 event에서는 동일 Hook이 여러 번 실행될 수 있다.

외부 side effect가 있다면 중복 실행에 안전해야 한다.

예:

- 같은 notification 여러 번 전송
- 같은 test job 중복 실행
- 같은 artifact 동시 갱신

가능하면 Hook 자체나 호출 대상이 idempotent하게 설계되어야 한다.

## 11.6 Blocking Hook은 양쪽을 테스트한다

차단 Hook을 만들면 deny case만 시험하기 쉽다.

하지만 실제 운영에서 더 위험한 것은 legitimate operation까지 막는 false positive다.

따라서 최소한 두 종류의 테스트가 필요하다.

- 실제로 막아야 하는 명령
- 비슷하지만 허용해야 하는 명령

publish를 막는 Hook이라면 draft 생성, preview, status 조회 같은 near-match가 정상 허용되는지 확인한다.

## 11.7 Equivalent bypass

한 명령만 문자열로 막으면 같은 의미의 다른 명령으로 우회될 수 있다.

정책이 “production publish를 막는다”라면 실제 위험 surface를 command-set이나 semantic category로 모델링하는 편이 낫다.

가능하면 machine-readable allowlist 또는 deny class를 둔다.

## 11.8 Escape hatch

좋은 enforcement는 합법적인 예외 처리 경로도 가진다.

예외가 가능한 정책을 절대 차단으로 만들면 사용자는 Hook을 비활성화하는 더 위험한 방법을 택할 수 있다.

승인 토큰, explicit override, 별도 관리 절차처럼 통제된 escape hatch를 설계한다.

## 11.9 Hook을 만들지 말아야 할 때

다음은 Hook보다 지침이나 리뷰가 낫다.

- 아키텍처 선택
- 코드 가독성
- 다양한 예외가 있는 품질 판단
- 고비용이어서 항상 실행할 수 없는 분석
- 사람의 trade-off 판단이 핵심인 기준

Hook은 강하기 때문에 좁게 사용해야 한다.

좋은 Hook은 많은 것을 통제하는 Hook이 아니라 **정확히 판정할 수 있는 위험을 최소 범위에서 통제하는 Hook**이다.
