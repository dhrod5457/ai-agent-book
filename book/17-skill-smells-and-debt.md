# 17장. Skill Smell과 Instruction Debt

코드에는 smell이 있다. 지침 파일에도 반복적으로 나타나는 나쁜 징후가 있다.

Smell은 자동 실패 조건이 아니다. 문제가 있을 가능성이 높으니 검토해야 한다는 신호다.

이 구분이 중요하다. smell을 전부 lint hard fail로 바꾸면 지침 시스템이 또 다른 규칙 과잉 상태가 된다.

## 17.1 Weak Routing Metadata

description이 너무 넓거나 모호하다.

증상:

- unrelated task에서도 자주 호출된다.
- 인접 Skill과 구분되지 않는다.
- domain keyword만 나열되어 있다.

해결:

- what + when
- adjacent negative
- trigger eval

## 17.2 Bloated Body

SKILL.md가 매뉴얼 전체를 품는다.

증상:

- 모든 API와 edge case가 본문에 있다.
- 긴 예제가 반복된다.
- 작업과 무관한 자료도 항상 읽힌다.

해결:

- router 최소화
- conditional reference
- script 분리
- generic prose 삭제

## 17.3 Poor Resource Organization

reference가 깊게 연결되고 무엇을 언제 읽어야 하는지 알 수 없다.

해결:

- 진입점에서 직접 필요한 reference로 연결
- reference depth 축소
- 긴 문서는 자체 목차 제공

## 17.4 Duplicated Instruction

같은 규칙이 CLAUDE.md, Rule, Skill, README에 반복된다.

처음에는 강화처럼 보이지만 결국 drift를 만든다.

해결:

- canonical owner 하나
- 다른 파일은 pointer만 유지

## 17.5 Stale Reference

파일 경로, CLI 옵션, API 설명, 버전 정보가 낡는다.

해결:

- structural link validation
- installed-version source
- live official source
- dated fallback
- removal audit

## 17.6 Workflow Ownership Collision

여러 Skill이 같은 상태나 책임을 소유한다.

증상:

- validate가 deploy까지 한다.
- prepare가 approve를 암묵적으로 처리한다.
- deprecated Skill이 canonical logic을 복제한다.

해결:

- state owner 분리
- compatibility alias
- machine-readable transition 가능성 검토

## 17.7 Side-effect Intent Collapse

prepare, preview, publish, deploy가 같은 Skill에서 구분되지 않는다.

해결:

- intent threshold
- authority 분리
- approval/handoff
- permission/Hook 보강

## 17.8 Cached CLI Manual

CLI option table을 Skill에 복제한다.

결과:

- stale syntax
- 중복 source of truth
- body bloat

해결:

- help
- installed-version docs
- generated schema
- live docs

## 17.9 Host-Tolerated Invalidity

어떤 host가 잘못된 metadata를 우연히 허용해서 문제가 숨는다.

다른 host나 새 버전에서는 실패할 수 있다.

해결:

- spec 기반 structural validation
- provider별 smoke test
- “지금 동작한다”와 “유효하다”를 구분

## 17.10 Eval Skill Collision

candidate와 installed Skill이 동시에 보여 잘못된 Skill을 평가한다.

해결:

- inventory 고정
- duplicate 제거
- activation source 기록
- fresh session

## 17.11 Latest-Version Override

최신 문서가 기존 project target보다 우선한다.

해결:

- user target
- project target
- installed source
- current docs
- fallback 순서

## 17.12 Duplicated Domain Tokens

디자인 토큰, schema, type, threshold 같은 값을 Skill에 다시 쓴다.

해결:

- canonical machine-readable source를 읽는다.
- Skill에는 lookup rule만 둔다.

## 17.13 Generic Process in Domain Skill

domain Skill이 일반 계획, clean code, 테스트, 리뷰 절차를 반복한다.

해결:

- domain-specific surprise와 invariant만 남긴다.
- generic process는 공통 layer에 맡긴다.

## 17.14 Missing Completion Bound

작업 종료 조건이 없다.

해결:

- observable Done when
- artifact, status, test result로 완료 판정

## 17.15 Instruction Debt가 쌓이는 방식

Debt는 대부분 합리적인 이유로 시작한다.

실패가 발생한다.

사용자가 correction한다.

팀은 다시 발생하지 않게 문장을 하나 추가한다.

다음 실패에 또 문장을 추가한다.

이 과정이 반복되면 지침은 과거 사고 기록을 모두 품는다.

문제는 correction이 틀렸다는 것이 아니다. correction의 최종 형태가 항상 prose일 필요는 없다는 것이다.

## 17.16 Debt 처리 순서

반복 correction을 발견하면 다음을 묻는다.

1. 아직도 발생하는가.
2. 현재 모델에서도 필요한가.
3. 더 좁은 scope로 내릴 수 있는가.
4. canonical source로 대체할 수 있는가.
5. validator나 Hook으로 옮길 수 있는가.
6. eval case로 남길 수 있는가.
7. 삭제 조건이 있는가.

좋은 instruction maintenance는 추가 작업보다 **삭제와 소유권 정리**가 더 많아질 수 있다.

## 17.17 Smell은 점수표가 아니다

MUST가 많다고 자동으로 나쁜 Skill은 아니다.

500줄이 넘는다고 자동 실패도 아니다.

negative wording이 있다고 잘못된 것도 아니다.

고위험 업무에는 강한 표현이 필요할 수 있다.

Smell catalog의 목적은 기계 점수를 만드는 것이 아니라 **어디를 사람과 eval이 다시 봐야 하는지 알려주는 것**이다.
