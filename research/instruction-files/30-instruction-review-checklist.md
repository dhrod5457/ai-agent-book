# Instruction Review Checklist Template

기준일: 2026-09-30

이 체크리스트는 점수를 매기기 위한 것이 아니다.

목적은:

> **이 파일의 실제 failure mode에 필요한 계약이 빠졌는지 확인하는 것**

이다.

---

# 1. 모든 instruction file 공통

## Ownership

- [ ] 이 파일이 소유하는 지식의 종류를 한 문장으로 설명할 수 있다.
- [ ] 다른 instruction file과 같은 규칙을 중복 소유하지 않는다.
- [ ] 더 canonical한 machine-readable source가 있다면 그 값을 복사하지 않는다.

## Scope

- [ ] repo-wide 규칙만 root standing instruction에 있다.
- [ ] path-local 규칙은 nested instruction 또는 path Rule로 내려갔다.
- [ ] task-local 절차는 Skill로 분리되어 있다.
- [ ] 기계적으로 검사 가능한 규칙은 lint/schema/type/Hook/CI로 이동할 수 있는지 검토했다.

## Freshness

- [ ] 바뀔 수 있는 version/API/status 정보를 static prose에 무기한 박아 두지 않았다.
- [ ] canonical source가 명확하다.
- [ ] fallback snapshot이 필요하면 source/date/freshness policy가 있다.
- [ ] live verification 실패 시 추측하지 않는다.

## Maintenance

- [ ] referenced local path가 존재한다.
- [ ] removal condition을 설명할 수 있다.
- [ ] model/host upgrade 시 삭제 후보를 다시 검토한다.
- [ ] instruction change가 registration/manifest/catalog에도 반영되는지 확인한다.

---

# 2. CLAUDE.md / AGENTS.md

- [ ] 모든 작업에 필요한 정보만 상시 context에 있다.
- [ ] subsystem-specific detail이 root에 쌓이지 않았다.
- [ ] 일반 개발 handbook을 그대로 복사하지 않았다.
- [ ] build/test entry command는 실제 repository와 일치한다.
- [ ] procedure 전체를 상시 지침에 넣지 않았다.
- [ ] 관련 nested instruction/Skill/Rule로 가는 routing pointer가 있다.
- [ ] stale snapshot/state를 현재 사실처럼 단정하지 않는다.
- [ ] host/provider-specific rule을 portable repository rule처럼 표현하지 않는다.

### 리팩터링 신호

다음은 자동 실패 조건이 아니라 검토 신호다.

- root 파일이 계속 커진다.
- "항상 먼저 읽어라" 문서가 늘어난다.
- 같은 test/style rule이 여러 곳에 반복된다.
- 현재 모델이 이미 잘하는 일반론이 많다.
- release/deploy/migration 절차가 root에 들어 있다.

---

# 3. Path-scoped Rule / nested instruction

- [ ] matcher/path가 실제 필요한 대상만 잡는다.
- [ ] 해당 path에서만 필요한 local invariant다.
- [ ] parent/root rule과 literal policy를 중복하지 않는다.
- [ ] canonical 상세 문서가 있다면 Rule은 high-signal summary만 가진다.
- [ ] path matcher가 현재 repository structure와 일치한다.
- [ ] file 이동/rename 시 Rule도 함께 검토된다.
- [ ] formatter/linter가 잡을 수 있는 style rule을 prose로 중복하지 않는다.

---

# 4. Auto-trigger SKILL.md

## Trigger

- [ ] description이 무엇을 하는지 말한다.
- [ ] 언제 사용해야 하는지 말한다.
- [ ] 가장 헷갈리는 adjacent negative가 정의돼 있다.
- [ ] broad domain 전체를 무조건 잡지 않는다.
- [ ] 적합한 Skill이 없을 때 abstain할 수 있다.

## Preconditions

- [ ] 시작 전에 필요한 file/state/tool/config가 명시돼 있다.
- [ ] 없는 precondition을 agent가 임의로 만들어내지 않는다.
- [ ] prerequisite failure 시 fallback/stop이 있다.

## Procedure

- [ ] 순서가 결과에 실제 영향을 주는 단계만 강하게 고정한다.
- [ ] judgment가 필요한 곳과 deterministic step을 구분한다.
- [ ] 긴 option/catalog/manual을 그대로 복제하지 않는다.
- [ ] 필요한 reference를 조건부로 읽는다.

## Evidence

- [ ] completion을 self-report만으로 판정하지 않는다.
- [ ] test/output/artifact/trace/file 같은 관측 가능한 증거가 있다.
- [ ] narrow Skill이면 하나의 명확한 `Done when`을 둘 수 있다.

## Handoff

- [ ] 어디서 멈추는지 명시돼 있다.
- [ ] 다음 Skill/tool/human으로 넘기는 조건이 있다.
- [ ] deprecated/compatibility entrypoint가 full logic을 복제하지 않는다.

## Eval

- [ ] explicit positive case가 있다.
- [ ] implicit positive case가 있다.
- [ ] adjacent negative case가 있다.
- [ ] routing pair가 필요한지 검토했다.
- [ ] candidate Skill과 installed Skill이 충돌하지 않는 환경에서 평가한다.

---

# 5. Manual-only Skill

- [ ] 사람에게 이름이 발견 가능하다.
- [ ] argument contract가 명확하다.
- [ ] auto-trigger eval 대상에서 제외된다.
- [ ] explicit invocation이 필요한 이유가 있다.
- [ ] procedure와 completion condition이 있다.
- [ ] 실패/retry behavior가 있다.
- [ ] side effect가 크면 approval과 evidence가 있다.

---

# 6. High-side-effect Skill

대상 예:

- deploy
- publish
- merge
- release
- billing mutation
- infrastructure creation
- destructive migration
- production data write

## Intent

- [ ] prepare/preview와 execute/publish를 구분한다.
- [ ] user request가 실제 mutation 의도를 포함하는지 확인한다.
- [ ] routine reversible step에 불필요한 approval gate를 걸지 않는다.

## Authority

- [ ] state owner가 명확하다.
- [ ] 현재 Skill이 바꾸면 안 되는 state가 있다면 명시한다.
- [ ] validation authority와 execution authority를 분리할 필요가 있는지 검토했다.

## Permission

- [ ] 필요한 tool 권한만 사용한다.
- [ ] secret/credential을 repository file에 남기지 않는다.
- [ ] equivalent bypass path도 policy에 포함된다.

## Failure

- [ ] 실패 시 state가 잘못 성공으로 남지 않는다.
- [ ] interrupted execution의 cleanup 방법이 있다.
- [ ] 비용/resource leak 가능성이 문서화돼 있다.

## Evidence

- [ ] mutation 결과를 확인할 identifier/status/output이 있다.
- [ ] 완료 상태는 실행 결과와 연결된다.

---

# 7. Validation / Test Skill

- [ ] test가 실제로 read-only인지 확인했다.
- [ ] 실제 infrastructure, 외부 API, 비용, credential을 사용할 수 있는지 확인했다.
- [ ] 가장 좁은 충분한 test부터 실행한다.
- [ ] focused test와 full regression을 구분한다.
- [ ] explicit timeout이 필요한지 검토했다.
- [ ] flaky/cache false positive를 구분한다.
- [ ] suspiciously passing test는 failure sensitivity를 확인할 수 있다.
- [ ] test failure evidence가 다음 단계로 전달된다.

---

# 8. Fast-moving framework / CLI / API Skill

- [ ] 현재 정보의 source of truth가 무엇인지 정의했다.
- [ ] installed version과 latest version을 구분한다.
- [ ] existing project review와 new project recommendation의 기준을 구분한다.
- [ ] complete CLI option table을 static Skill에 복제하지 않는다.
- [ ] `--help`, generated schema, installed-version docs, live official docs 중 적절한 source를 사용한다.
- [ ] live source 실패 시 fallback policy가 있다.
- [ ] newer version을 추측하지 않는다.
- [ ] user-specified target을 무시하고 latest를 강제하지 않는다.

---

# 9. Hook / deterministic enforcement

- [ ] Hook이 필요한 실제 failure mode가 있다.
- [ ] prose-only rule을 왜 Hook으로 올렸는지 설명할 수 있다.
- [ ] matcher가 실제 위험 surface만 잡는다.
- [ ] blocking Hook에 positive deny test가 있다.
- [ ] legitimate near-match allow test가 있다.
- [ ] target tool의 실제 argument semantics를 정확히 모델링한다.
- [ ] equivalent bypass command를 함께 검토했다.
- [ ] Hook side effect는 idempotent하거나 안전하게 반복 가능하다.
- [ ] repository trust/workspace boundary를 고려했다.

---

# 10. Structural validator PR checklist

- [ ] YAML/frontmatter parse
- [ ] required fields
- [ ] local references
- [ ] script paths
- [ ] manifest coverage
- [ ] duplicate registration
- [ ] provider metadata syntax
- [ ] allowed-tools syntax
- [ ] Hook event/matcher schema
- [ ] blocking Hook test presence
- [ ] declared snapshot freshness metadata
- [ ] machine-readable state owner collision

다음은 validator hard fail로 만들지 않는다.

- [ ] prose가 충분히 좋은가
- [ ] description이 실제로 정확히 trigger되는가
- [ ] Skill이 output quality를 높이는가
- [ ] 500줄을 넘는가
- [ ] MUST가 많은가
- [ ] negative wording이 있는가

이것들은 eval/human review로 보낸다.

---

# 11. Instruction change PR template

## Why

이 지침을 왜 바꾸는가?

실패 사례, 사용자 correction, model/host 변화, product 변화 중 무엇이 원인인가?

## Scope

어떤 파일/task/path에만 적용되어야 하는가?

## Canonical source

이 지침이 의존하는 source of truth는 무엇인가?

## Behavior change

agent behavior가 전/후 어떻게 달라져야 하는가?

## Structural verification

어떤 validator/check가 통과해야 하는가?

## Semantic eval

positive / negative / routing / output case 중 무엇을 실행해야 하는가?

## Risk

permission, side effect, secret, operational cost가 바뀌는가?

## Portability

Claude/Codex/Cursor/Gemini/Copilot 등 provider-specific 의미가 있는가?

## Removal condition

언제 이 지침을 줄이거나 삭제할 수 있는가?

---

# 12. 최종 리뷰 질문

리뷰 마지막에는 10개만 다시 묻는다.

1. 언제 활성화되는가?
2. 언제 활성화되면 안 되는가?
3. 시작 전에 무엇이 참이어야 하는가?
4. state와 authority owner는 누구인가?
5. 실제로 어떤 절차가 필요한가?
6. 어떤 side effect와 권한이 있는가?
7. 무엇으로 완료를 증명하는가?
8. 어디서 멈추고 넘기는가?
9. 바뀌는 사실은 어디서 다시 읽는가?
10. 어떤 failure/eval이 이 지침을 수정하거나 삭제하게 하는가?

이 10개에 답할 수 없다고 무조건 나쁜 파일은 아니다.

하지만 해당 failure mode와 관련된 질문에 답이 없으면 그 지점이 리뷰 대상이다.
