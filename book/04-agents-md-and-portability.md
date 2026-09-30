# 4장. AGENTS.md와 다중 도구 호환성

여러 AI 코딩 도구를 함께 사용하는 팀이라면 특정 제품 전용 파일만으로 규칙을 관리하기 어렵다. 이때 AGENTS.md는 공통 저장소 지침의 중심 후보가 된다.

하지만 “AGENTS.md 하나면 모든 제품이 똑같이 동작한다”는 기대는 위험하다.

## 4.1 공통 포맷과 공통 의미는 다르다

여러 도구가 같은 파일명을 읽더라도 파일 탐색 순서, root와 nested 파일 우선순위, 하위 파일 로드 시점, 사용자 지침과 프로젝트 지침의 결합 방식, path rule 지원 방식은 다를 수 있다.

따라서 portability를 두 층으로 나눠야 한다.

### Portable principle

도구에 상관없이 유지되는 원칙이다. 전역 지침을 작게 유지하고, path-local 규칙은 해당 scope로 내리고, 반복 절차는 Skill로 분리하고, canonical source를 복제하지 않는 것이 여기에 속한다.

### Vendor syntax

특정 도구에서만 의미가 있는 문법이다. Claude Rule의 path 설정, Cursor Rule의 globs, Copilot의 applyTo, 제품별 Skill metadata 등이 여기에 속한다.

## 4.2 공통 AGENTS.md에는 무엇을 둘 것인가

여러 도구가 공유해야 하는 저장소 사실을 둔다.

프로젝트 구조, 공통 개발 명령, repository-wide invariant, 생성 파일이나 보안 경로 같은 공통 주의사항, 세부 문서로 가는 포인터가 좋은 후보다.

제품별 기능 사용법은 전용 파일로 분리하는 편이 낫다.

## 4.3 Vendor 파일은 adapter처럼 쓴다

이상적인 구조는 하나의 거대한 공통 파일이 아니다.

AGENTS.md는 도구 독립적 사실을 소유하고, CLAUDE.md나 Cursor Rules, Copilot path instruction은 제품별 wiring과 scope를 담당한다. Skill은 task-specific workflow를 맡는다.

공통 규칙의 원문은 한 곳에 두고 vendor 파일에는 필요한 연결만 남긴다.

## 4.4 중복의 위험

같은 규칙을 여러 파일에 복사하면 처음에는 호환성이 좋아 보인다. 하지만 시간이 지나면 한 파일만 수정되고, 명령이 서로 달라지고, path 이름 변경이 일부에만 반영된다.

결국 어느 파일이 진짜인지 알기 어렵다.

따라서 공통 사실은 canonical source 하나를 정하고 필요한 곳에서는 참조한다.

## 4.5 파일 수보다 소유권이 중요하다

다중 도구 팀에서 목표는 파일 수 최소화가 아니다.

> 같은 사실은 한 번만 소유하고, 각 도구에는 필요한 형태로 최소한만 연결한다.

이 기준을 지키면 도구가 늘어나도 지침 시스템이 폭발적으로 복잡해지지 않는다.
