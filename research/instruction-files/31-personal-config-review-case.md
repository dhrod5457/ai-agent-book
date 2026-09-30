# 개인 Claude Code 구성 점검 사례

기준일: 2026-09-30

## 목적

이 research 의 기준(27 §7, 12 §18, 28 §13, 30 체크리스트)을 실제 개인 구성 하나에 적용한 결과를 기록한다.
공개 corpus 관찰(11 · 27)이 아니라 한 사용자의 구성을 하루 동안 점검 · 수정 · 측정한 사례다.
20 의 Gap 4(모델 업그레이드 후 지침 정리)와 Gap 6(문장 규칙과 Hook 강제)에 사례 근거로 쓸 수 있다. controlled 비교는 아니다.

## 대상과 방법

| 구분 | 내용 |
|---|---|
| 대상 | `~/.claude` 전역 구성. `CLAUDE.md` 166줄, 개인 Skill 13개(외부 설치 1개 포함), 등록 Hook 12개, custom agent 4개 |
| host | Claude Code 2.1.284 ~ 2.1.285, 기본 권한 모드 `auto` |
| 대조 기준 | 27 §7 유형별 최소 contract, 12 §18 smell, 28 §13 decision tree, 30 체크리스트 |
| 판정 절차 | 사용자의 `anthropic-practice-review` Skill. REVIEW(권고표) 뒤 사용자 결정, APPLY-NOW 후보는 쓰기 도구가 없는 subagent 에게 반박 검토를 맡긴다 |
| native 도구 | `/doctor prompt-audit`, `claude plugin validate`, `/skill-doctor`, `claude auto-mode config` |

research 문서는 공식 근거가 아니어서, APPLY-NOW 는 Claude Code 공식 문서 원문 인용이 있는 항목만으로 제한했다.

## 1. 발견과 조치

| # | 발견 | 해당 분류 | 조치 | 확인 방법 |
|---|---|---|---|---|
| 1 | Claude Code 기본 Git 지시 "If on the default branch, branch first" 가 사용자 규칙 "확인한 변경은 기본 브랜치에 커밋" 과 경쟁 | 12 에 없는 유형. 아래 §4 후보 S36 | `includeGitInstructions: false`, 기본 지시 중 필요한 두 문장(대화형 플래그 금지, `gh` 사용)을 사용자 규칙으로 이관 | `claude -p --settings '{"includeGitInstructions":false}'` 로 Bash 도구 설명의 `# Git` 네 문장이 빠지는 것을 확인 |
| 2 | 같은 `CLAUDE.md` 안의 충돌 2건. 위임 절 "모호하면 먼저 묻는다" 대 기본 원칙 "승인 대상이 아니면 묻지 않는다", Git 절 "섞인 변경은 묻는다" 대 같은 기본 원칙 | 27 §7 standing contract 의 conflict | 위임 절 문장 수정, 기본 원칙에 예외 명시 | 두 번째는 `/doctor prompt-audit` 가 찾음 |
| 3 | Skill 이 "전역 CLAUDE.md 의 승인 대상" 이라고 가리키는 규칙이 전역에 없음(운영 배포 Jenkins 잡) | 12 S6 Registration Drift 의 계층 간 형태 | 승인 목록에 추가(사용자 결정), 같은 날 Hook 으로 강제 | `/doctor prompt-audit` 가 찾음 |
| 4 | Skill 본문 안의 절차 충돌. "완료를 기다리지 않는다" 대 "노드별로 SUCCESS 확인 뒤 다음 노드" | 27 §7 Handoff · Evidence | 순차 배포만 전경 대기, `SUCCESS` 이외 값과 도구 오류는 멈춤, 실패 노드 재실행 금지 | 반박 검토가 처음 수정안(Monitor 대기)을 전역 규칙과의 새 충돌로 지적해 바꿈 |
| 5 | 문장으로만 있던 안전 규칙 2건(`--no-verify` 우회 금지, 운영 배포 잡 승인) | 12 S9 Prose-Enforced Determinism | PreToolUse Hook 두 갈래 추가 | 30 §9 대로 차단 사례 · 인접 통과 사례 시험. 고치기 전 코드에서 차단 사례가 "기대 차단, 실제 통과" 로 실패, 결함을 넣은 사본에서 인접 통과 사례가 실패 |
| 6 | `autoMode.environment` 가 probe 저장소에서 만든 `/auto-mode-setup` 초안 그대로. `"$defaults"` 없이 신뢰 저장소가 probe 경로 하나 | 12 에 없는 유형. 아래 §4 후보 S37 | `"$defaults"` 와 사용자 항목 셋만 남김 | `claude auto-mode config` 에서 신뢰 저장소가 기본 문장으로 복원된 것을 확인 |
| 7 | 한 번도 호출되지 않은 Skill 22개가 매 턴 목록에 포함. 합계 약 4,200 토큰 | 20 §8 Context Cost | 사용자가 끌 수 있는 12개를 `skillOverrides` `name-only` 로 | `/skill-doctor` 재실행에서 12개 모두 20 토큰 미만. 합계 약 2,700 토큰 감소 |
| 8 | 등록이 해제된 Hook 파일과 그 시험이 남아 있고, 다른 Hook 시험이 그 파일을 표본으로 사용 | 12 S6 | 파일 삭제, 표본을 등록된 Hook 으로 교체 | 전체 Hook 시험 통과 |
| 9 | 테스트 실행 위치 규칙("맥에서 실행")과 Testcontainers Skill("로컬 도커 금지")이 충돌 | 27 §7 standing contract 의 conflict | 두 저장소로 측정한 뒤 "맥에서 실행, Testcontainers 시험과 3-OS 검증만 노드" 로 확정 | 아래 §3 |

## 2. 반박 검토가 바꾼 판정

APPLY-NOW 후보 8건을 쓰기 도구가 없는 subagent 에게 원문 인용, 현재 상태, 새 충돌 여부를 다시 확인하게 했다.

| 결과 | 건수 | 내용 |
|---|---|---|
| 그대로 확인 | 1 | 위임 절과 기본 원칙의 충돌(§1 #2) |
| 수정안 변경 | 4 | 기본 Git 지시 끄기(필요한 문장 이관 추가), 근거 문서 정정(날짜 분리, 이유를 사용자에게 묻지 않고 "확인하지 않음"), Skill 순차 배포(전경 대기), 삭제 조건 기록(다섯 항목 중 외부 기본값에 기대는 둘로 축소) |
| 하향(EXPERIMENT · 보류) | 2 | 이름이 겹치는 두 Skill 의 description 경계(호출 0회라 사고 근거 없음), description 안의 모델 이름 중복 제거(공식 근거 아님) |
| 철회 | 1 | 정의가 없는 용어의 괄호 삭제(같은 줄의 조건이 이미 구체적) |

8건 중 5건은 반박 검토 뒤 수정안이 바뀌거나 철회됐다. 그중 순차 배포 수정안은 그대로 적용했으면 전역 규칙과 새로 충돌했다.

## 3. 테스트 실행 위치 측정

같은 커밋을 위치마다 두 번 실행하고 두 번째 값을 쓴다.

| 저장소 · 대상 | 맥 | vm94 한 대 | 다른 위치 |
|---|---|---|---|
| agent-run-mesh `063c0a3`, `node test/lanes.ts` 1,418건, Testcontainers 없음 | 59초 | 52초(전달 · 빌드 포함) | Linux 4노드 분산 28초 |
| lotecs-ai-platform `c7e87955`, `:campus-ai-api:integrationTest` 551건 | 맥 + 로컬 도커 205초 | 343초 | 맥 JVM + 원격 도커(37) 435초 |

- 실행 위치는 로그 대신 `pgvector` 컨테이너가 뜬 도커로 판정했다
- vm94 집계가 564건인 것은 하네스가 저장소 전체 결과 XML 을 세고, 대상 태스크가 의존하는 샘플 플러그인 빌드가 시험 13건을 함께 실행하기 때문이다
- 맥 로컬 도커가 가장 빨랐지만 기본으로 두지 않았다. 공용 `~/.testcontainers.properties` 와 저장소의 보호 확장이 원격 도커를 요구하고, 맥 도커에는 사내 미러 레지스트리 인증이 없다. 손해는 전수 한 번에 약 2분 20초다

## 4. research 에 반영할 후보 [제안]

**smell 후보.**

- **S36 Host Instruction Competition.** host 가 스스로 넣는 기본 지시(도구 설명, 기본 Git 지시)가 사용자 지침과 다른 동작을 요구한다.
  사용자 파일끼리의 충돌(S11 · 02 §7)과 달리 파일을 읽어서는 보이지 않는다. 공식 문서(https://code.claude.com/docs/en/memory
  「Claude isn't following my CLAUDE.md」)가 "Check whether your instruction competes with guidance Claude Code adds on its own" 로 점검을 권한다.
  이 사례에서 `~/.claude/CLAUDE.md` 를 대상으로 실행한 `/doctor prompt-audit` 는 이 경쟁을 보고하지 않았다
- **S37 Setup Draft Residue.** 설정 도우미가 특정 저장소 기준으로 만든 초안이 전역 설정에 남아 다른 저장소의 판단을 바꾼다.
  이 사례에서는 `"$defaults"` 가 빠져 기본 목록 전체가 대체됐다

**30 체크리스트 추가 후보.**

- §2 CLAUDE.md: host 기본 지시(`includeGitInstructions` 로 제어하는 commit · PR 지시 등)와 경쟁하는 규칙이 있는지 본다
- §9 Hook: 설정 목록형 값(`autoMode.environment` 등)에 기본값 유지 표시(`"$defaults"`)가 있는지 본다

**측정 주의.** 최근 14일 transcript 로 센 Skill 호출이 0회였던 항목이 `/skill-doctor` 에서는 12회(마지막 21일 전)였다.
호출 빈도로 삭제 후보를 정할 때 측정 창을 함께 적는다.

## 5. 이 사례로 확인하지 않은 것

- 수정 전후 Claude 의 실제 동작 차이(위임 횟수, 커밋 브랜치 선택)는 재지 않았다. 다음 세션들에서 관찰 대상이다
- `/doctor prompt-audit` 가 제안한 옛 모델용 문구 정리(위임 권장 문장, 계획 지시)는 적용하지 않았다. Gap 4 의 controlled 비교 대상이다
- 여러 세션이 동시에 맥에서 전수 시험을 실행하는 조건은 재지 않았다
