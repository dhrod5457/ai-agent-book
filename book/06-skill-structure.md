# 6장. Skill의 구조와 공개 표준

Skill은 단순한 긴 프롬프트 파일이 아니다. 특정 종류의 작업이 들어왔을 때만 발견되고, 선택되고, 필요한 절차와 자료를 로드하는 **업무 단위**다.

이 구조를 이해하지 못하면 SKILL.md를 작은 매뉴얼처럼 작성하게 된다. 그러면 discovery와 execution이 섞이고, description은 길어지고, 본문에는 모든 예외와 자료가 한꺼번에 들어간다.

## 6.1 Skill은 두 단계로 읽힌다

대부분의 Agent Skills 구현에서 핵심 개념은 progressive disclosure다.

첫 단계에서는 Skill의 이름과 description 같은 metadata만 보인다. 모델은 이 정보로 해당 Skill을 사용할지 판단한다.

두 번째 단계에서 Skill이 선택되면 본문과 필요한 resource가 로드된다.

따라서 Skill에는 서로 다른 두 품질이 존재한다.

- Routing quality: 필요한 요청에서 선택되고, 불필요한 요청에서는 선택되지 않는가.
- Execution quality: 선택된 뒤 올바른 절차를 수행하는가.

본문이 아무리 좋아도 routing이 실패하면 Skill은 존재하지 않는 것과 같다. 반대로 routing만 잘 되고 본문이 부실하면 잘못된 절차를 매우 안정적으로 실행하게 된다.

## 6.2 Portable core

공개 Agent Skills 계열에서 공통으로 볼 수 있는 핵심 구조는 단순하다.

- Skill directory
- SKILL.md
- name
- description
- Markdown body
- 선택적인 references
- 선택적인 scripts
- 선택적인 assets

이 정도를 portable core로 보면 이해가 쉽다.

도구별 추가 metadata는 별개다. 어떤 제품은 허용 도구, 호출 방식, 모델, 실행 권한 같은 확장을 제공한다. 이런 필드를 공개 표준의 일부처럼 설명하면 portability가 깨진다.

## 6.3 Skill directory는 작은 패키지다

좋은 Skill은 하나의 Markdown 파일보다 작은 패키지처럼 생각하는 편이 낫다.

본문은 진입점과 절차를 담당한다.

references는 필요할 때 읽는 상세 근거를 담당한다.

scripts는 반복 가능하고 결정론적인 작업을 담당한다.

assets는 템플릿이나 산출물 재료를 담당한다.

모든 것을 SKILL.md 하나에 넣지 않는 이유는 단순히 줄 수를 줄이기 위해서가 아니다. **언제 무엇을 읽을지 제어하기 위해서**다.

## 6.4 name은 사용자가 기대하는 기능을 표현한다

좋은 이름은 기능과 책임이 드러난다.

review-db-migration, triage-ci-failure, write-release-notes처럼 작업 의도가 보이면 인접 Skill과 구분하기 쉽다.

helper, common, developer, backend처럼 조직이나 범위를 나타내는 이름은 실제 호출 조건을 설명하지 못한다.

Skill library가 커질수록 이름은 문서용 label이 아니라 routing surface의 일부가 된다.

## 6.5 Router와 leaf Skill

모든 Skill이 같은 크기일 필요는 없다.

### Leaf Skill

하나의 좁은 책임을 가진다.

장점은 의미가 선명하고, 수정 영향 범위가 작고, 다른 workflow가 재사용하기 쉽다는 점이다.

### Router Skill

여러 capability 중 어떤 절차로 갈지 선택한다.

장점은 진입점을 줄일 수 있다는 것이다.

하지만 router가 커지면 모든 절차의 세부사항을 품기 시작하고, metadata도 넓어지고, trigger 간 충돌이 증가한다.

좋은 router는 “무엇을 선택할지”를 담당하고, 선택된 작업의 full manual은 leaf Skill이나 reference에 둔다.

## 6.6 Skill은 문서가 아니라 계약이다

Skill의 핵심은 설명량이 아니라 다음 계약에 있다.

- 언제 시작하는가.
- 시작 전에 무엇이 필요하다.
- 어떤 순서가 중요한가.
- 무엇을 하면 안 되는가.
- 어떤 상태를 소유하는가.
- 무엇으로 완료를 증명하는가.
- 실패하면 어디에서 멈추는가.

이 계약이 명확하면 본문은 짧아질 수도 있고 길어질 수도 있다.

중요한 것은 독자가 아니라 모델이 실행 가능한 형태로 이해할 수 있는가다.

## 6.7 Progressive disclosure의 실전 기준

세부 자료를 reference로 분리할 때는 “자세한 내용은 참고”라고만 쓰지 않는다.

언제 읽어야 하는지 명시한다.

예를 들어 schema 변경인 경우에만 migration reference를 읽고, 공개 API 호환성 변경인 경우에만 compatibility reference를 읽는 식이다.

이렇게 해야 reference 분리가 실제 context 절감으로 이어진다.

## 6.8 좋은 Skill 구조를 판단하는 질문

Skill을 만들기 전에 다음을 묻는다.

1. 독립적인 반복 업무인가.
2. 항상 필요한 절차가 아니라 특정 요청에서만 필요한가.
3. 이 업무를 description 하나로 인접 업무와 구분할 수 있는가.
4. 본문에 둘 내용과 reference로 분리할 내용이 구분되는가.
5. 반복되는 기계 작업은 script로 옮길 수 있는가.
6. 완료 상태를 관측 가능한 증거로 정의할 수 있는가.

이 질문에 답하기 어렵다면 Skill을 만들기 전에 책임 자체를 더 좁혀야 한다.
