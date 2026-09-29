# 실제 Hook 운영 사례 리서치

## 1. 목적

Hook 문법 자체가 아니라 다음 질문에 답하기 위한 사례를 모았다.

> 어떤 규칙은 자연어 지침으로 남기고, 어떤 규칙은 Hook으로 승격해야 하는가.

이번 표본에서 특히 반복되는 패턴은 다음이다.

- 위험한 명령 차단
- write scope 차단
- 변경 후 verification
- 승인 gate
- session bootstrap
- context injection
- Hook 자체의 테스트
- platform 간 hard/soft enforcement 차이

## 2. sfc-gh-eraigosa/dotfiles: PreToolUse safety guard

Source:
- https://github.com/sfc-gh-eraigosa/dotfiles/blob/main/AGENTS.md
- https://github.com/sfc-gh-eraigosa/dotfiles/blob/main/ai/hooks/safety_guard.sh
- https://github.com/sfc-gh-eraigosa/dotfiles/blob/main/ai/hooks/safety_guard_test.sh

### 구조

`safety_guard.sh`는 Bash tool call을 받아 regex 기반으로 위험한 명령을 차단한다.

예:

- wildcard deletion
- root/system directory deletion
- disk management
- block device write
- fork bomb
- web content pipe-to-shell
- force push
- 직접 PR ready/merge 우회
- 자체 workflow approval token 우회

### 중요한 작성 패턴

#### 1. Prose 규칙보다 강한 gate

"force push 전에 승인받아라"를 AGENTS.md에만 쓰지 않고 실제 PreToolUse에서 검사한다.

#### 2. Hook contract를 명시한다

스크립트 상단에 다음이 있다.

- stdin schema
- exit 0 = allow
- exit 2 = block
- stderr = reason
- dependency

Hook도 API처럼 contract를 문서화한다.

#### 3. False positive를 별도 문제로 다룬다

예를 들어 heredoc 본문 안의 `rm -rf *` 문자열은 실제 command가 아니므로 검사 전에 제거한다.

또한 bash regex의 `.*`가 separator/newline을 넘는 문제를 따로 처리한다.

이 사례는 보안 Hook에서 **차단률만큼 정상 명령 통과율도 중요하다**는 점을 보여준다.

## 3. Hook에 positive/negative test를 붙인다

`safety_guard_test.sh`는 단순 위험 case만 확인하지 않는다.

### allow case

- 평범한 `ls`
- `git status`
- 안전한 하위 디렉터리 삭제
- read-only tool
- heredoc 안의 위험 문자열
- 정상적인 gss command

### block case

- 실제 위험 deletion
- stale approval token
- 잘못된 worktree mode
- publish verb without token

AGENTS.md도 Hook 수정 시 다음을 요구한다.

- 같은 형태의 legitimate command가 계속 통과하는 positive case
- malicious shape가 차단되는 negative case

이 패턴은 책의 Hook testing 기준으로 매우 좋다.

> 차단 Hook의 테스트는 "막아야 할 것"과 "절대로 막으면 안 되는 것"을 쌍으로 둔다.

## 4. iPzard/electron-react-python-template: 변경 후 verification Hook

Source:
- https://github.com/iPzard/electron-react-python-template/blob/master/CLAUDE.md
- https://github.com/iPzard/electron-react-python-template/blob/master/.claude/settings.json
- https://github.com/iPzard/electron-react-python-template/blob/master/.claude/hooks/verify-on-change.py
- https://github.com/iPzard/electron-react-python-template/blob/master/.claude/hooks/test_verify_on_change.py

### 구조

`.claude/settings.json`:

- event: `PostToolUse`
- matcher: `Edit|Write|MultiEdit`
- command: `verify-on-change.py`
- timeout: 10

Hook script는 모든 edit에서 검증을 실행하지 않는다.

먼저 path를 분류한다.

### in-scope

- source
- scripts
- tests
- 주요 build/config 파일

### excluded

- Markdown
- `.claude/`
- docs
- node_modules
- build/dist/resources

in-scope일 때만 change-verifier를 실행하라는 context를 반환한다.

### 배울 점

> "수정할 때마다 테스트"를 그대로 Hook으로 만들면 너무 비싸다. 먼저 verification surface를 정의해야 한다.

즉 Hook 설계에도 scope engineering이 필요하다.

## 5. Verification Hook도 테스트한다

`test_verify_on_change.py`는 path classification을 table-driven case로 검사한다.

포함해야 하는 파일과 제외해야 하는 파일을 모두 검증한다.

특히 Windows path와 Unix/MSYS path를 같이 다룬다.

책에서 일반화할 수 있다.

### Hook matcher test

- positive event
- negative event
- platform-specific path
- generated/output directory
- docs/config self-edit
- malformed payload
- missing field

## 6. rizukirr/no-vibe: Prose guard와 hard block의 차이

Source:
- https://github.com/rizukirr/no-vibe/blob/main/AGENTS.md
- https://github.com/rizukirr/no-vibe/blob/main/hooks/block-writes.sh

프로젝트 목표는 학습 모드에서 AI가 사용자의 project file을 직접 쓰지 못하게 하는 것이다.

Claude에서는 PreToolUse Hook으로 다음 write tool을 실제 차단한다.

- Edit
- Write
- NotebookEdit
- MultiEdit
- ApplyPatch

그리고 허용 경로만 예외 처리한다.

AGENTS.md에는 흥미로운 비교가 있다.

- Claude/OpenCode/Pi: hard block 가능
- Gemini surface: equivalent PreToolUse가 없어 instruction-based soft block

### 책에서 중요한 메시지

같은 prose instruction도 host가 enforcement primitive를 제공하느냐에 따라 실제 보장 수준이 달라진다.

따라서 cross-agent portability를 설명할 때는 다음을 분리해야 한다.

- semantic portability
- enforcement portability

## 7. Hook에서 fail-open/fail-closed를 명시한다

`no-vibe`의 write Hook은 target path를 알아낼 수 없으면 fail closed로 차단한다.

반면 activation marker가 없으면 조용히 allow한다.

이것은 Hook마다 정의해야 할 정책이다.

### 질문

- malformed input이면 allow할 것인가.
- Hook 내부 오류면 block할 것인가.
- target을 식별할 수 없으면?
- dependency가 없으면?
- timeout이면?

보안 Hook과 convenience Hook의 답은 다를 수 있다.

## 8. VibeFlow: prose + Hook + Skill의 중복이 의도적인 경우

Source:
https://github.com/hardness1020/VibeFlow/blob/main/CLAUDE.md

VibeFlow는 일부 checkpoint를 두 층으로 검사한다.

- UserPromptSubmit Hook
- manage-work Skill

이것은 보통의 "중복 지침을 피하라" 원칙과 충돌해 보인다.

하지만 여기서는 역할이 다르다.

- Hook: deterministic safety net
- Skill: normal workflow semantics

책에서 중요한 구분:

> 같은 규칙을 두 파일에 복붙하는 것은 smell이지만, 서로 다른 실패 모드를 막는 defense-in-depth는 중복이 아닐 수 있다.

## 9. AWS Skills: Skill-scoped Hook 가능성

Source:
https://github.com/zxkane/aws-skills/blob/main/CLAUDE.md

이 저장소의 문서는 Skill frontmatter에서 Hook을 연결하는 예를 제공한다.

예:

- deploy command 전에 account identity 확인
- once per session

의미:

모든 Hook이 global이어야 하는 것은 아니다.

특정 위험 Skill이 활성화될 때만 필요한 Hook을 붙이면 global false positive와 비용을 줄일 수 있다.

## 10. petekp/claude-code-setup: Hook wiring 자체도 maintenance 대상

Source:
https://github.com/petekp/claude-code-setup/blob/main/CLAUDE.md

관찰:

- SessionStart에서 skill wiring doctor 실행
- PostToolUse/UserPromptSubmit로 skill usage 기록
- hook script 변경 시 test 요구
- settings symlink health 검사
- stale/dangling skill link 정리

이 사례는 Hook이 규칙을 강제하는 도구이면서 동시에 **Hook 자체가 instruction infrastructure**라는 점을 보여준다.

따라서 Hook도 다음 maintenance가 필요하다.

- registration
- install/sync
- versioning
- test
- dangling dependency
- usage observation

## 11. umputun/cc-thingz: 제품의 Hook UX/동작 차이도 기록해야 한다

Source:
https://github.com/umputun/cc-thingz/blob/master/CLAUDE.md

이 저장소는 plugin Hook과 settings Hook의 deny rendering 차이 같은 제품 제한을 문서화한다.

책에서 얻을 수 있는 원칙:

> Hook 작성 가이드는 spec만 설명하면 부족하다. 실제 host runtime의 UX, exit-code 처리, rendering 차이도 검증해야 한다.

## 12. Layered enforcement 사례

`xwtro0tk1t-cloud/harness/SKILL.md`는 enforcement를 계층으로 설명한다.

- Hook = system-level
- CLAUDE.md = directive-level
- Skill description = trigger

이 구조를 그대로 표준으로 삼을 필요는 없지만, 책의 개념 모델로는 유용하다.

### 제안하는 일반 모델

| 레이어 | 목적 | 보장 수준 |
| --- | --- | --- |
| Prose instruction | 판단, 맥락, 정책 설명 | 모델 순응 |
| Skill workflow | 절차와 조건 | 모델 순응 + on-demand context |
| Hook | lifecycle 강제 | host runtime 수준 |
| Script/validator | 결정론적 판정 | 프로그램 수준 |
| CI/type/schema | 저장소/빌드 불변식 | 시스템 수준 |

핵심은 중요한 규칙일수록 가능한 더 강한 레이어를 검토하는 것이다.

## 13. Hook smell 후보

### H1. Global Hook Overreach

모든 event/file에 Hook을 붙여 비용과 false positive가 커진다.

### H2. Untested Deny Rule

위험 command만 test하고 legitimate near-match를 test하지 않는다.

### H3. Regex Cross-Talk

shell regex가 separator, newline, heredoc을 넘어 잘못 match한다.

### H4. Silent Matcher Drift

host 버전 변화로 matcher/event semantics가 달라졌는데 test가 없다.

### H5. Prose-Only Critical Gate

반드시 차단해야 하는 행동을 CLAUDE.md의 MUST 문장으로만 둔다.

### H6. Hook-Only Intent

Hook이 차단은 하지만 왜 그런 정책인지 사람이 읽을 source가 없다.

### H7. Self-Trigger Loop

Hook이 자신의 generated/edit artifact까지 다시 trigger한다.

### H8. Non-Idempotent Side Effect

PostToolUse/async Hook이 중복 실행되면 외부 side effect가 중복된다.

### H9. Unbounded Verification

사소한 edit마다 전체 회귀를 실행한다.

### H10. No Escape Hatch

정상적인 예외 workflow가 필요한데 영구 deny만 존재한다.

## 14. Hook 작성 체크리스트 보강

### Scope

- [ ] event가 최소 범위인가.
- [ ] matcher가 최소 범위인가.
- [ ] file/path scope가 별도로 필요한가.
- [ ] docs/generated/self files를 제외해야 하는가.

### Contract

- [ ] stdin schema가 문서화됐는가.
- [ ] allow/block exit 의미가 명확한가.
- [ ] malformed input 정책이 있는가.
- [ ] timeout 정책이 있는가.
- [ ] 사용자에게 보여 줄 실패 이유가 구체적인가.

### Safety

- [ ] external/untrusted text를 command로 재해석하지 않는가.
- [ ] path normalization이 필요한가.
- [ ] symlink/`..` 우회를 고려했는가.
- [ ] secret이나 credential을 출력하지 않는가.

### Test

- [ ] block positive case가 있는가.
- [ ] legitimate near-match가 통과하는가.
- [ ] Windows/Unix path를 모두 시험했는가.
- [ ] malformed event를 시험했는가.
- [ ] self-trigger를 시험했는가.

### Maintenance

- [ ] Hook 등록 파일과 script 경로가 함께 검증되는가.
- [ ] Hook 변경이 CI에서 test되는가.
- [ ] host version 변화 시 재검증할 수 있는가.

## 15. 이번 수집에서 나온 핵심 결론

1. Hook도 "설정"이 아니라 테스트 가능한 코드 artifact로 다뤄야 한다.
2. deny Hook은 malicious case와 legitimate near-match를 반드시 함께 테스트해야 한다.
3. "모든 변경 후 검증" 같은 규칙도 path scope가 없으면 비싸고 시끄럽다.
4. prose + Hook이 항상 나쁜 중복은 아니다. 서로 다른 failure mode를 막는 defense-in-depth일 수 있다.
5. portability는 파일 형식뿐 아니라 enforcement primitive의 차이까지 포함한다.
6. critical MUST 규칙은 가능한 경우 prose보다 강한 구조적 enforcement 후보를 검토해야 한다.
