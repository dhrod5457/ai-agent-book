# Popular Skill Rule Pattern Matrix

기준일: 2026-09-30

## 목적

최근 유명 Skill에서 관찰한 규칙을 코드화해서 비교한다.

주의:

- 통계적으로 무작위 추출한 corpus가 아니다.
- "N개 중 몇 개"는 prevalence 추정치가 아니다.
- 유명/공식/활성 프로젝트에서 어떤 패턴이 반복 관찰되는지 확인하는 질적 비교 matrix다.
- 한 repository에서 여러 Skill을 골랐으므로 독립 표본도 아니다.

## 표본

20개 representative Skill/문서:

1. Anthropic `skill-creator`
2. Anthropic `frontend-design`
3. Superpowers `using-superpowers`
4. Superpowers `test-driven-development`
5. Superpowers `verification-before-completion`
6. Matt Pocock `implement`
7. Matt Pocock `tdd`
8. Addy Osmani `using-agent-skills`
9. Vercel `agent-browser`
10. Vercel `find-skills`
11. Remotion `remotion-best-practices`
12. Microsoft `azure-prepare`
13. Microsoft `azure-validate`
14. Microsoft `azure-deploy`
15. Prisma `prisma-database-setup`
16. Prisma `prisma-upgrade-v7`
17. Firebase `firebase-tools-pr-review`
18. Sentry `skill-scanner`
19. Planning with Files
20. Ponytail

## Pattern coding

| Pattern | 관찰 수 | 대표 사례 | 의미 |
| --- | ---: | --- | --- |
| 명시적 trigger / when | 18/20 | Anthropic, Azure, Sentry | 언제 적용할지 description/body에 드러냄 |
| 명시적 exclusion / negative boundary | 11/20 | Azure Prepare/Deploy, Prisma Upgrade, Ponytail | 잘못된 자동 호출 방지 |
| progressive disclosure / references | 14/20 | Anthropic, Remotion, Vercel, Azure | top-level context 축소 |
| observable verification/evidence | 13/20 | Superpowers, Azure, Addy, Firebase | 완료를 self-report로 판정하지 않음 |
| handoff to another Skill/process | 10/20 | Azure chain, Prisma alias, Matt composition | Skill 책임 경계 |
| user approval / explicit intent gate | 7/20 | Azure, Remotion, Anthropic creator | side effect 또는 scope 결정 전에 human gate |
| deterministic script/validator | 8/20 | Azure Validate, Sentry Scanner, Planning with Files | 순서/검사를 executable로 이동 |
| persistent artifact/state file | 5/20 | Azure, Planning with Files | workflow 상태를 대화 밖에 보존 |
| source/version freshness strategy | 7/20 | agent-browser, Prisma, Vercel, Addy | stale knowledge 대응 |
| allowed-tools / least privilege | 4/20 | agent-browser, Sentry, Planning with Files | permission을 Skill contract로 관리 |
| manual-only invocation | 3/20 | Matt implement, grill-me 계열 | timing을 user가 통제 |
| explicit output contract | 8/20 | Firebase review, Sentry scanner, Superpowers verification | 결과 형식/판정 구조 고정 |
| preserve existing/user changes | 4/20 | Remotion, Addy scope discipline, Ponytail | unsolicited overwrite 방지 |
| anti-rationalization / red flags | 7/20 | Superpowers, Addy | shortcut 압력 대응 |
| priority/risk tiers | 6/20 | Vercel React, Prisma Upgrade, Sentry Scanner | 모든 규칙을 같은 강도로 다루지 않음 |
| compatibility/deprecation routing | 3/20 | Prisma | 옛 entrypoint 유지와 canonical logic 분리 |
| explicit abstention/no-match path | 4/20 | find-skills, Prisma, Azure boundaries | 무조건 Skill을 적용하지 않음 |

숫자는 현재 문서를 기준으로 사람이 코딩한 값이며, 자동 corpus 분석 결과가 아니다.

## 해석 1. 가장 반복되는 것은 "절차"보다 Trigger + Verification이다

20개 표본 중 가장 자주 보인 것은 trigger, references, verification이다.

즉 좋은 Skill을 단지 "단계가 잘 정리된 절차서"라고 보는 것은 부족하다.

들어오는 조건 → 필요한 context → 수행 → 증거

가 핵심 골격이다.

## 해석 2. Operational Skill은 Handoff가 중요하다

Azure/Prisma/Remotion 같은 업무형 Skill에서는:

- 여기까지 내가 한다
- 그 다음은 다른 Skill
- 이 조건에서는 여기서 stop

이 자주 나온다.

따라서 Skill 품질 평가 항목에 `Handoff correctness`를 추가할 가치가 있다.

질문:

- 책임이 끝나는 지점이 있는가?
- 다음 Skill을 잘못 건너뛰지 않는가?
- handoff 전에 필요한 artifact/status가 남는가?

## 해석 3. Negative trigger는 여전히 부족하다

대부분 positive trigger를 갖지만 명확한 exclusion은 그보다 적다.

즉 실제 유명 Skill에서도 "언제 쓰는가"보다 "언제 쓰지 않는가"가 덜 체계적이다.

이는 기존 trigger-eval 연구 방향을 지지한다.

## 해석 4. Persistent state는 소수지만 고위험 workflow에서 중요하다

빈도는 낮지만 사용되는 곳은 deployment, long-running planning처럼 state drift 비용이 큰 workflow다.

따라서 모든 Skill에 state file이 필요한 것이 아니라 state loss가 실제 failure mode일 때만 persistent artifact로 승격한다.

## 해석 5. Permission metadata는 아직 보편적이지 않다

`allowed-tools` 같은 permission contract는 소수다.

하지만 Sentry 사례에서 잘못된 separator 하나가 실제 capability loss를 만들었다.

따라서 빈도와 중요도는 다르다.

책에서는 permission metadata가 존재하면 문법/portability를 반드시 validator로 검사하는 방향이 맞다.

# 유지보수 변화 matrix

최근 3개월 commit history에서 실제 관찰된 변화:

| 변화 | 저장소 | 방향 |
| --- | --- | --- |
| 장황한/중복 prose 제거 | Superpowers | context 축소 |
| rationale 삭제 후 compliance 하락, 일부 복구 | Superpowers | 행동 기반 편집 |
| Skill 삭제 | Sentry | stale/over-trigger 제거 |
| duplicate router 통합 | Prisma | canonical owner |
| old name을 compatibility redirect로 축소 | Prisma | deprecation hygiene |
| inline validation steps를 script로 이동 | Microsoft Azure | executable state |
| metadata separator 수정 | Sentry | spec portability |
| absolute rule scope 축소 | Vercel | false-positive 감소 |
| Hook matcher scope 축소 | ECC | over-enforcement 감소 |
| Hook runtime/schema 수정 | Planning with Files | host portability |
| canonical command alias 제거 | Vercel find-skills | duplication 감소 |
| static detailed docs 대신 installed-version content | agent-browser | freshness |
| repo-specific review convention Skill 신설 | Firebase | local specificity |

# 새 품질 축 후보

기존 품질 축:

- Discoverability
- Selectivity
- Clarity
- Actionability
- Scope fit
- Context efficiency
- Structural integrity
- Portability
- Verifiability
- Maintainability
- Model robustness

추가 검토할 축:

## Boundary completeness

positive trigger뿐 아니라:

- negative boundary
- stop
- no-match
- explicit-only
- handoff

가 정의돼 있는가.

## State integrity

workflow state가 있다면:

- owner
- allowed transition
- proof
- persistence

가 일관적인가.

## Freshness strategy

외부 API/CLI/framework 지식이:

- pinned snapshot
- live official source
- installed-version source
- migration alias

중 어떤 전략으로 유지되는가.

## Side-effect discipline

조회/preview/prepare와 write/deploy/publish/render/install을 같은 trigger 강도로 취급하지 않는가.

# 책에서 사용할 압축 모델

이번 matrix를 바탕으로 Skill을 다음 8개 질문으로 리뷰할 수 있다.

1. 언제 이 Skill이 선택되는가?
2. 언제 선택되면 안 되는가?
3. 시작 전 무엇이 참이어야 하는가?
4. 무엇을 어떤 순서로 하는가?
5. 어떤 도구·side effect가 허용되는가?
6. 완료를 무엇으로 증명하는가?
7. 어디서 멈추고 무엇으로 넘기는가?
8. 이 지식은 어떻게 최신 상태를 유지하는가?

이 8개 질문은 방법론형/업무형 Skill을 모두 커버한다.
