# CLAUDE.md와 Rules 작성법 리서치

## 1. CLAUDE.md는 설정 파일이 아니라 상시 컨텍스트다

Claude Code 공식 문서는 CLAUDE.md를 "enforced configuration"이 아니라 context로 명확히 구분한다.

이 차이는 중요하다.

- CLAUDE.md: 모델이 판단할 때 참고하는 행동 지침
- permissions/settings/hooks: 클라이언트가 실제로 실행을 허용하거나 차단하는 기계적 통제

따라서 "절대로 실행하면 안 되는 명령"처럼 반드시 강제해야 하는 요구사항을 CLAUDE.md 문장 하나에만 의존하면 안 된다.

## 2. 무엇을 CLAUDE.md에 넣는가

공식 문서는 다음과 같은 내용을 상시 유지할 정보로 본다.

- build 명령
- test 명령
- coding convention
- project layout
- architecture decision
- naming convention
- 반복적으로 설명해야 하는 프로젝트 사실

반면 다음은 다른 위치가 더 적합하다.

- multi-step procedure → Skill
- 특정 파일 범위에서만 필요한 규칙 → path-scoped Rule
- 기계적으로 차단해야 하는 행동 → Hook/settings/lint/CI

## 3. "두 번째 반복"은 좋은 추가 신호다

Anthropic 문서는 CLAUDE.md에 추가할 시점으로 다음과 같은 반복 신호를 든다.

- 같은 실수를 다시 한다.
- 코드 리뷰에서 "Claude가 알았어야 할" 프로젝트 사실이 반복된다.
- 이전 세션과 같은 correction을 다시 입력한다.
- 새 팀원도 같은 정보를 알아야 한다.

이 기준은 "생각나는 모든 규칙을 미리 넣기"보다 낫다.

책에서는 다음 원칙으로 일반화할 수 있다.

> 실제 실패나 반복 설명에서 출발하고, 추상적인 예방 문장을 무한히 쌓지 않는다.

## 4. 길이 목표

2026-09-30 현재 Claude Code 공식 문서는 CLAUDE.md 파일 하나를 **200줄 미만**으로 목표하라고 권장한다.

긴 파일의 문제:

- startup context를 소비한다.
- 관련 없는 규칙도 매 세션 들어온다.
- adherence가 떨어질 수 있다.
- 충돌 지침을 발견하기 어려워진다.

200줄은 절대 법칙이 아니라 리팩터링 신호로 다루는 것이 적합하다.

## 5. 좋은 문장은 구체적이고 검증 가능하다

공식 예시의 방향은 명확하다.

모호한 표현:

- code를 제대로 format한다.
- 변경사항을 test한다.
- 파일을 잘 정리한다.

더 나은 표현:

- indentation 수치를 정한다.
- 실행할 test command를 적는다.
- API handler의 실제 경로를 적는다.

핵심은 "좋은 결과"를 요구하는 것이 아니라 모델이 행동으로 옮길 수 있는 사실을 주는 것이다.

## 6. 전역 사용자 지침과 프로젝트 지침을 분리한다

Claude Code의 주요 scope:

| Scope | 위치 | 적합한 내용 |
| --- | --- | --- |
| User | `~/.claude/CLAUDE.md` | 개인의 모든 프로젝트 공통 선호 |
| Project | `./CLAUDE.md`, `./.claude/CLAUDE.md` | 팀 공유 프로젝트 규칙 |
| Local | `./CLAUDE.local.md` | 개인의 해당 프로젝트 전용 설정 |
| Managed | OS별 관리 경로 | 조직 공통 지침 |

프로젝트 파일에 개인 취향을 넣으면 팀 전체의 context와 규칙이 불필요하게 오염된다.

## 7. 전역 Rule과 프로젝트 Rule은 "override"가 아니다

Claude Code 공식 문서는 user-level Rules와 project Rules가 충돌할 때 한쪽이 hard override되는 것으로 보장하지 않는다.

프로젝트 Rule이 context에서 뒤에 놓이더라도 충돌 시 모델이 어느 쪽을 따를지 보장되지 않는다.

따라서:

- 전역과 프로젝트 지침의 충돌을 설계하지 않는다.
- "더 구체적인 파일이 알아서 덮어쓰겠지"라고 기대하지 않는다.
- 의도적 예외라면 상위 규칙을 제거하거나 scope를 좁힌다.

## 8. Rules는 topic 단위로 분리한다

공식 문서는 `.claude/rules/`에서 파일 하나가 하나의 topic을 다루고 설명적인 파일명을 쓰는 것을 권장한다.

예:

```text
.claude/
├── CLAUDE.md
└── rules/
    ├── testing.md
    ├── api-design.md
    └── security.md
```

장점:

- ownership이 분명해진다.
- 충돌 탐지가 쉬워진다.
- path scope를 줄 수 있다.
- 특정 규칙을 삭제하거나 이동하기 쉽다.

## 9. path-scoped Rule

현재 Claude Code Rule frontmatter에서 읽는 필드는 `paths`다.

예:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API rules

- Parse external input before calling domain services.
- Return errors through the shared API error shape.
```

적합한 사례:

- migration은 append-only
- React component 규칙
- 특정 언어의 테스트 규칙
- API handler 입력 검증
- generated file 수정 금지

Rule에 `paths`가 없으면 항상 로드된다.

## 10. Rule frontmatter의 함정

현재 공식 문서 기준:

- `paths` 이외의 Rule frontmatter 필드는 무시된다.
- 지원하지 않는 필드를 넣어도 오류 없이 무시될 수 있다.
- YAML parsing이 실패하면 path 조건이 없는 Rule처럼 로드될 수 있다.

책에서는 "예제가 그럴듯해 보인다"보다 제품 문서의 실제 지원 필드를 확인하는 습관을 강조해야 한다.

## 11. imports는 조직화일 뿐 context 절약이 아니다

CLAUDE.md는 `@path`로 다른 파일을 import할 수 있다.

그러나 import된 내용도 startup context에 들어간다.

따라서:

- 한 파일을 여러 파일로 나눈다고 자동으로 context가 줄지 않는다.
- context 절감이 목적이면 path-scoped Rule 또는 Skill로 이동해야 한다.
- import는 소유권과 가독성 개선 수단으로 이해한다.

## 12. 하위 CLAUDE.md는 on-demand가 가능하다

현재 working directory 아래의 subdirectory에 있는 CLAUDE.md는 Claude가 해당 하위 경로의 파일을 읽을 때 로드될 수 있다.

모노레포에서 활용 가능하다.

다만 cross-cutting concern이 여러 위치에 퍼져 있으면 path-scoped Rule이 더 명확할 수 있다.

## 13. HTML maintainer comment

현재 Claude Code는 CLAUDE.md의 block-level HTML comment를 context에 주입할 때 제거한다.

따라서 사람을 위한 유지보수 메모를 다음과 같이 남길 수 있다.

```html
<!-- 이 규칙은 2026-Q4 migration 종료 후 삭제 검토 -->
```

이런 메모는 지침의 lifecycle을 관리하는 데 유용하다.

## 14. AGENTS.md와의 상호운용성

2026년 현재 Claude Code는 AGENTS.md도 직접 읽을 수 있다.

다만 CLAUDE.md와 AGENTS.md가 함께 있을 때의 기본 로딩 조건이 있으므로 "둘 다 있으면 항상 합쳐진다"고 단순화하면 안 된다.

책에서는 다음 두 전략을 비교할 수 있다.

### Claude 중심 저장소

- CLAUDE.md를 canonical instruction으로 사용
- 필요한 vendor-specific Rule/Skill을 `.claude/`에 둠

### 다중 도구 저장소

- 공통 standing rules를 AGENTS.md에 둠
- Claude-specific 지침은 CLAUDE.md/Rules에 둠
- 중복 내용을 복사하지 않고 가능한 경우 import/reference 사용
- 각 도구의 실제 loading semantics를 검증

## 15. CLAUDE.md 리뷰 체크리스트

- [ ] 매 세션 필요한 내용만 있는가.
- [ ] 프로젝트 사실과 개인 취향이 분리되어 있는가.
- [ ] multi-step procedure가 들어와 있지 않은가.
- [ ] 특정 path에만 필요한 규칙을 전역으로 넣지 않았는가.
- [ ] 기계적으로 강제 가능한 규칙을 prose로만 두지 않았는가.
- [ ] 실제 command/path/symbol을 사용했는가.
- [ ] 서로 충돌하는 규칙이 없는가.
- [ ] 이미 코드에서 명확히 알 수 있는 내용을 장황하게 복제하지 않았는가.
- [ ] 200줄을 넘기기 시작했다면 분리 후보를 검토했는가.
- [ ] 오래된 모델을 위해 추가했던 scaffolding이 남아 있지 않은가.
- [ ] 링크와 명령이 지금도 존재하는가.

## 주요 출처

- Claude Code, How Claude remembers your project
  - https://code.claude.com/docs/en/memory
- Anthropic, Steering Claude Code
  - https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
- Anthropic, Effective context engineering for AI agents
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- OpenAI, Rethinking skills and prompts for GPT-6 Astra
  - https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
