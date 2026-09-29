# 지침 파일 작성의 핵심 원칙

## 1. 먼저 "어디에 쓸지"를 결정한다

지침을 발견했다고 바로 `CLAUDE.md`에 추가하지 않는다.

먼저 다음 질문으로 분류한다.

| 질문 | 권장 위치 |
| --- | --- |
| 거의 모든 작업에서 알아야 하는가 | 루트 CLAUDE.md, AGENTS.md, GEMINI.md 같은 상시 컨텍스트 |
| 특정 파일이나 디렉터리에만 적용되는가 | path-scoped Rule |
| 특정 업무를 할 때만 필요한 절차인가 | SKILL.md |
| 매번 반드시 실행하거나 차단해야 하는가 | Hook, lint, script, CI, permission 설정 |
| 설명보다 코드나 설정 자체가 더 정확한가 | 코드, schema, type, config를 source of truth로 사용 |

지침 파일의 품질은 문장력보다 **적절한 스코프 선택**에서 시작한다.

## 2. 상시 컨텍스트에는 상시 필요한 것만 둔다

좋은 전역 지침의 후보:

- 저장소의 핵심 구조
- 실제 빌드, 테스트, lint 명령
- 모든 변경에 적용되는 팀 규칙
- 프로젝트 전체에서 의미가 고정된 용어
- 반복적으로 잘못 추론하는 비자명한 사실
- 관련 세부 문서로 가는 짧은 포인터

나쁜 후보:

- 특정 기능 개발 때만 필요한 긴 체크리스트
- 특정 언어나 폴더에서만 쓰는 규칙
- 장황한 아키텍처 설명 전문
- 이미 코드나 설정에서 쉽게 확인되는 정보
- "항상 모든 문서를 먼저 읽어라" 같은 과잉 사전 읽기
- 모델이 원래 잘 수행하는 행동을 중복해서 강제하는 지침

Anthropic과 OpenAI의 최신 가이드는 공통적으로 불필요한 상시 컨텍스트를 줄이는 방향이다.

## 3. 한 지침은 하나의 판단을 바꾸게 한다

지침 파일의 문장을 평가할 때 질문한다.

> 이 문장을 삭제하면 모델의 중요한 판단이 실제로 달라지는가?

아니라면 삭제 후보이다.

pstack의 `authoring-a-skill.md`도 같은 방향으로, 의사결정을 바꾸는 문장만 남기고 다른 Skill의 내용을 복제하지 말라고 한다.

### 나쁜 예

- 코드를 신중하게 작성한다.
- 항상 품질을 중요하게 생각한다.
- 좋은 아키텍처를 만든다.
- 테스트를 충분히 한다.

행동 기준이 없다.

### 더 나은 형태

- 외부 JSON은 service layer에 전달하기 전에 schema로 parse한다.
- `db/migrations/**`의 기존 migration 파일은 수정하지 않는다.
- 버그 수정은 재현 가능한 로컬 검증 경로가 있으면 수정 전 실패를 먼저 확인한다.
- 기존 API를 대체할 때 동일 저장소의 caller를 모두 이전한 뒤 legacy API를 제거한다.

## 4. 모호한 가치보다 관찰 가능한 행동을 쓴다

"깨끗하게", "적절하게", "가능하면", "품질 높게" 같은 표현은 판단 기준을 외부에 남긴다.

가능하면 다음 중 하나를 제공한다.

- 적용 조건
- 금지 조건
- 파일 범위
- 실제 명령
- 완료 조건
- 실패 조건
- 증거의 형태
- 예외 조건

## 5. positive trigger와 negative boundary를 같이 설계한다

특히 Skill은 "언제 사용한다"만 쓰면 범위가 퍼지기 쉽다.

좋은 트리거는 인접하지만 대상이 아닌 요청을 구분한다.

pstack의 TDD Skill은 좋은 사례다. 사용 조건뿐 아니라 테스트 경로가 불명확하거나 비싸고 integration-heavy한 경우에는 강제하지 않는다고 명시한다.

이 패턴을 일반화하면:

- Use when: 실제 대상 업무를 좁게 정의
- Skip when: 자주 혼동되는 인접 업무를 정의

## 6. 조건을 먼저, 행동을 뒤에 쓴다

독자는 사람뿐 아니라 모델이다.

다음 형태가 안정적이다.

- "API handler를 수정할 때 입력 schema를 함께 확인한다."
- "production migration을 작성할 때 destructive operation이면 rollout 문서를 작성한다."
- "실제 UI 동작이 완료 조건이면 screenshot 또는 browser automation 결과를 남긴다."

적용 범위를 뒤에서 뒤집는 문장보다 파싱하기 쉽다.

## 7. 명령형 문장을 기본으로 한다

절차 파일에서는 서술보다 행동을 직접 지시한다.

- "검토되어야 한다"보다 "검토한다."
- "테스트가 실행되는 것이 권장된다"보다 "영향받는 테스트를 실행한다."
- "필요할 수도 있다"보다 조건을 정의한 뒤 실제 동작을 쓴다.

다만 판단이 필요한 영역을 거짓 결정론으로 만들지 않는다.

## 8. 이유는 규칙 이해에 필요한 만큼만 쓴다

모든 규칙 뒤에 장문의 철학을 붙이지 않는다.

이유가 필요한 경우:

- 규칙이 직관과 반대일 때
- 예외를 판단하려면 목적을 알아야 할 때
- 잘못 적용했을 때 위험이 클 때

그 외에는 명령 자체가 더 강한 신호다.

## 9. 단일 진실 원천을 유지한다

같은 규칙을 `CLAUDE.md`, `SKILL.md`, README, Hook 설명에 복제하지 않는다.

복제하면 시간이 지나면서 서로 다른 버전이 된다.

권장 방식:

- 소유 파일 하나를 정한다.
- 다른 지침 파일은 해당 파일을 가리킨다.
- 코드나 schema가 진실 원천이면 문서에 값을 복사하지 말고 해당 구조를 가리킨다.

## 10. progressive disclosure를 사용한다

Skill과 긴 지침 세트는 한 번에 모두 읽히지 않게 한다.

- root 문서: 라우팅과 핵심 절차
- references: 상세 배경과 정책
- scripts: 반복 가능한 기계적 작업
- assets: 출력 템플릿

Anthropic은 `SKILL.md` 본문을 대략 500줄 미만으로 유지하고 세부 자료를 별도 파일로 분리하는 것을 권장한다.

## 11. 참조 깊이를 얕게 유지한다

`SKILL.md -> reference A -> reference B -> reference C`처럼 연결하면 필요한 정보를 찾기 어렵다.

가능하면 root Skill이 필요한 reference를 직접 가리킨다.

Anthropic 가이드도 reference를 한 단계 깊이로 유지하는 것을 권장한다.

## 12. 기계가 판정 가능한 규칙은 자연어에만 맡기지 않는다

다음과 같은 규칙은 텍스트보다 구조가 강하다.

- formatting: formatter
- import 금지: lint
- schema: type/schema validator
- 반드시 통과해야 하는 검사: CI
- 특정 shell 명령 차단: PreToolUse Hook/permission
- 생성 파일 일관성: generator
- 참조 링크 유효성: validation script

pstack의 "Encode Lessons in Structure" 원칙도 반복되는 교정을 lint, metadata, runtime check, script 등으로 옮기도록 한다.

## 13. 완료의 정의를 관찰 가능하게 쓴다

"완료되면 확인한다"가 아니라 무엇이 완료인지 정한다.

예:

- 명령의 exit code가 0이다.
- 변경된 테스트가 통과한다.
- 특정 파일이 생성된다.
- UI에서 상태 전이가 확인된다.
- 실제 API 응답이 expected schema와 일치한다.

## 14. 지침은 모델 버전과 함께 노후화된다

OpenAI는 2026-09 GPT-6 Astra 지침에서 과거 모델을 보조하기 위해 쌓은 장황한 scaffolding이 새 모델을 오히려 방해할 수 있다고 설명한다.

따라서 지침에는 "추가"뿐 아니라 "삭제" 유지보수가 필요하다.

정기 감사 질문:

1. 이 지침이 지금도 필요한가.
2. 이미 모델 기본 행동과 중복되는가.
3. 특정 과거 실패에 과잉 적응한 것은 아닌가.
4. 다른 지침과 충돌하지 않는가.
5. 더 좁은 scope로 옮길 수 있는가.
6. text 대신 구조로 강제할 수 있는가.

## 15. 검증하지 않은 지침은 가설이다

좋아 보이는 문장을 쓰는 것만으로 품질을 판단하지 않는다.

최소 검증:

- 기대하는 요청에서 trigger되는가.
- 인접 요청에서는 trigger되지 않는가.
- 필요한 reference를 실제로 읽는가.
- 요구한 핵심 행동을 수행하는가.
- 불필요한 작업을 늘리지 않는가.
- Skill이 없는 baseline보다 나은가.
- 다른 모델에서도 같은 방향으로 작동하는가.

## 주요 출처

- Anthropic, Effective context engineering for AI agents
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic, Steering Claude Code
  - https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
- Anthropic, Skill authoring best practices
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- OpenAI, Rethinking skills and prompts for GPT-6 Astra
  - https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
- Cursor pstack, authoring-a-skill
  - https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md
- Cursor pstack, Encode Lessons in Structure
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md
