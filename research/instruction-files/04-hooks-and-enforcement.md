# Hooks와 구조적 강제 리서치

## 1. 이 장의 핵심 질문

Hooks를 "에이전트 기능 확장" 관점이 아니라 다음 질문으로 다룬다.

> 이 요구사항은 자연어 지침으로 남겨야 하는가, 아니면 Hook이나 다른 기계적 장치로 강제해야 하는가?

CLAUDE.md, Rules, Skills는 모델의 행동을 유도한다.

Hook의 command/http/mcp 계열은 특정 lifecycle event에 의해 실행될 수 있으므로 더 결정론적인 제어에 적합하다.

## 2. 자연어 지침으로 남기기 좋은 것

- 코드 설계에서 고려해야 할 판단 기준
- 상황에 따라 예외가 필요한 규칙
- 여러 대안 사이의 trade-off
- 프로젝트 특유의 의미와 맥락
- 사람이 리뷰할 수 있는 절차

예:

- public API를 변경할 때 backwards compatibility를 먼저 검토한다.
- 작은 refactor에서는 새 abstraction보다 기존 구조 단순화를 먼저 고려한다.

## 3. Hook/구조로 옮기기 좋은 것

- 특정 명령은 실행 자체를 막아야 한다.
- 파일 수정 후 formatter를 항상 실행한다.
- 특정 파일을 수정했을 때 validator를 실행한다.
- commit 전 특정 검사 결과가 필수다.
- 민감 경로에 대한 write를 차단한다.
- tool argument가 정책에 맞는지 기계적으로 검사할 수 있다.

판단 기준:

> 실패를 기계가 명확하게 판정할 수 있다면 자연어만으로 두지 않을 이유가 있는지 검토한다.

## 4. Hook scope도 지침 scope와 같다

Hook을 작성할 때 가장 먼저 event와 matcher를 최소 범위로 잡는다.

Claude Code에서 `matcher`는 Hook이 언제 실행될지 필터링한다.

예:

- 모든 tool
- Bash만
- Edit/Write만
- 특정 MCP tool namespace
- 특정 subagent type
- session start
- instructions load reason

너무 넓은 matcher는 다음 문제를 만든다.

- 불필요한 실행 비용
- false positive 차단
- 작업 속도 저하
- side effect 증가
- 예상하지 못한 권한 확장

## 5. matcher는 "대충 비슷하게" 작성하면 안 된다

현재 Claude Code는 matcher 문자열의 형태에 따라 exact match 또는 정규식으로 해석한다.

또한 일부 event는 matcher를 지원하지 않으며, 지원하지 않는 event에 matcher를 넣으면 조용히 무시될 수 있다.

따라서 Hook 설정도 코드처럼 검증해야 한다.

체크:

- 어떤 field에 matcher가 적용되는가.
- exact인가 regex인가.
- regex라면 anchor가 필요한가.
- event가 matcher를 지원하는가.
- 예상 positive/negative event로 직접 시험했는가.

## 6. Hook은 전체 사용자 권한을 가질 수 있다

Claude Code 공식 문서에서 command hook은 사용자 계정 권한으로 shell command를 실행한다고 명시한다.

따라서 Hook 파일은 단순한 프롬프트 파일보다 보안 수준을 높게 다뤄야 한다.

최소 원칙:

- input을 신뢰하지 않는다.
- shell variable을 quote한다.
- path traversal을 검사한다.
- absolute path를 사용한다.
- `.env`, key, `.git/` 등 민감한 경로를 제외한다.
- destructive command는 최소 권한과 좁은 matcher를 사용한다.
- repository에서 가져온 Hook은 실행 전에 검토한다.

## 7. repository Hook은 공급망 위험이 될 수 있다

특히 비대화형 `claude -p`나 SDK 실행에서는 repository의 `.claude/` 설정이 예상보다 강한 실행 권한을 가질 수 있다.

따라서 책에는 다음 경고가 필요하다.

- 신뢰하지 않는 저장소에서 committed Hook을 바로 실행하지 않는다.
- automation 환경에서는 Hook enable 상태를 명시적으로 관리한다.
- CI/agent runner에서 repository instruction과 executable hook을 같은 신뢰 수준으로 취급하지 않는다.

## 8. Hook script의 출력도 계약이다

좋은 Hook은 성공 여부만 내는 것이 아니라 소비자가 해석할 수 있는 안정적인 결과를 낸다.

설계할 항목:

- stdin schema
- exit code 의미
- stdout/stderr 의미
- blocking 여부
- 실패 시 사용자/모델에게 전달할 메시지
- 재실행 안전성
- timeout
- async 여부

## 9. async Hook은 중복 실행을 고려한다

Claude Code 공식 문서는 async Hook 실행 사이에 자동 deduplication이 없다고 설명한다.

따라서 async Hook이 외부 side effect를 만들면 idempotency가 중요하다.

예:

- 동일 파일 write가 짧은 시간에 여러 번 발생
- 동일 notification을 반복 전송
- 동일 test job이 중복 실행
- 동일 artifact를 동시에 갱신

Hook 자체나 호출 대상에서 중복에 안전한 구조를 설계해야 한다.

## 10. "Hook으로 만들지 말아야 할 것"

다음은 Hook보다 지침이 나을 가능성이 높다.

- 아키텍처 설계 선택
- 코드의 읽기 쉬움 판단
- 명확한 기계적 판정식이 없는 리뷰 기준
- 다양한 예외와 맥락이 있는 품질 판단
- 항상 실행할 필요가 없는 고비용 분석

모든 규칙을 Hook으로 바꾸면 개발 흐름이 경직되고 false positive가 늘어난다.

## 11. prose → structure 승격 사다리

반복되는 문제를 발견하면 다음 순서로 더 강한 표현 수단을 검토한다.

1. 코드 구조나 type으로 불가능하게 만들 수 있는가.
2. schema/validator로 판정할 수 있는가.
3. lint/CI로 검사할 수 있는가.
4. Hook으로 lifecycle에 연결할 수 있는가.
5. canonical helper/script로 한 경로만 제공할 수 있는가.
6. 그래도 판단이 필요하면 Rule/Skill/CLAUDE.md에 남긴다.

이 원칙은 pstack의 `principle-encode-lessons-in-structure`와도 일치한다.

## 12. 책에서 다룰 실전 예제 후보

- formatter 지침을 PostToolUse Hook으로 이전
- 위험한 `rm -rf` 패턴을 PreToolUse에서 차단
- migration file 수정 금지를 Rule + CI check로 이중화
- 문서 작성 금칙어를 Hook으로 검사하되 의도적 예외 escape hatch 제공
- Skill reference link validation을 PR 검사로 자동화
- generated file 직접 수정 금지를 path Rule + checker로 구현

핵심은 Hook 문법 자체가 아니라 "자연어 규칙을 언제 실행 가능한 정책으로 바꾸는가"를 보여주는 것이다.

## 13. Hook 리뷰 체크리스트

- [ ] 자연어 지침보다 Hook이 적합한 결정론적 문제인가.
- [ ] event가 최소 범위인가.
- [ ] matcher가 최소 범위인가.
- [ ] positive case를 시험했는가.
- [ ] negative case를 시험했는가.
- [ ] unsupported matcher가 조용히 무시되지 않는지 확인했는가.
- [ ] shell input을 sanitize하는가.
- [ ] variable을 quote하는가.
- [ ] path traversal을 막는가.
- [ ] 민감 파일을 피하는가.
- [ ] absolute path를 사용하는가.
- [ ] 중복 실행에 안전한가.
- [ ] 실패 메시지가 원인을 설명하는가.
- [ ] 사용자가 합법적인 예외를 처리할 escape hatch가 있는가.

## 주요 출처

- Claude Code Hooks reference
  - https://code.claude.com/docs/en/hooks
- Claude Code Hooks guide
  - https://code.claude.com/docs/en/hooks-guide
- Anthropic, Steering Claude Code
  - https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
- Cursor pstack, Encode Lessons in Structure
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md
