# VAD CLI의 CI 연동

## 범위와 아키텍처

첫 CI 연동은 기존 상태 판단을 재사용하는 읽기 전용 `check` 명령과 GitHub Actions다.
외부 서비스·새 패키지·스키마 변경은 없다. 검증 결과나 승인을 자동 생성하지 않는다.

```text
PR / main push → CLI tests → Python 3.9, 3.13 회귀 검증
PR / 수동 실행 / 호출 워크플로 → 변경 ID → check → 성공 / 준비 미완료 / 실행 오류
                                        → report → 진단 아티팩트
```

변경 경로는 `parser → execute → load/context/status → assess`다. 상태 판단을 복제하지
않고 기존 `status`와 같은 JSON을 출력한다. 기존 `status`의 종료 코드와 다른 명령의
오류 처리 호환성을 유지하며, `main`은 새 명령의 종료 코드를 전달한다.
공통 명령 처리 경로가 바뀌므로 새 게이트 시나리오와 기존 CLI 모음을 함께 검증한다.

| 수용 기준 | 관련 검증 |
| --- | --- |
| 현재 증거와 승인 기록이 있으면 0, 준비 미완료는 1, 읽기/입력/실행 오류는 2 | 정상·승인 대기·누락·Fail/Blocked/Not run·오래된 증거·고위험·손상 기록 테스트 |
| 판단은 읽기 전용이며 기존 명령의 동작을 유지한다 | 원본 바이트·잠금 미생성·기존 `status` 종료 코드 및 전체 CLI 회귀 검증 |
| PR과 main push에서 설치 의존성 없이 테스트한다 | GitHub Actions Python 3.9/3.13 실행 |
| 변경 ID를 안전하게 전달하고 게이트 실패를 숨기지 않는다 | 환경 변수와 인자 구분자 사용, `bash`의 pipefail, 실제 실패 워크플로 확인 |
| 준비 미완료여도 보고서를 확인할 수 있다 | 실제 수동 실행의 실패 상태와 `vad-report` 아티팩트 확인 |

영향 파일은 `tools/vad.py`, `tests/test_vad.py`, 두 워크플로, 사용 안내와 이 문서다.
기존 기록은 마이그레이션하지 않는다. 과거 증거는 소스 변경에 따라 오래된 상태가
되는 것이 정상이다. 업무 화면·API·데이터·사용자 권한은 변경하지 않는다.
GitHub 토큰은 `contents: read`만 부여하고 checkout 자격 증명을 보존하지 않는다.
자동 게이트의 우회 위험이 있으므로 이 CLI를 인증된 승인 시스템으로 설명하지 않는다.

## 로컬·다른 CI에서 사용

```sh
python3 tools/vad.py check -- actual-change-id
```

| 종료 코드 | 의미 | 출력 |
| --- | --- | --- |
| 0 | 현재 소스·계획·결과에 대해 Ready | 상태 JSON |
| 1 | Not ready: 누락, 실패, 오래된 증거, 승인 대기 또는 지원하지 않는 위험 수준 | 상태 JSON |
| 2 | 잘못된 인자, 손상/누락 기록, Git/파일 접근 오류 | stderr 오류; JSON이 없을 수 있음 |

`gaps`는 검증·정책의 문제, `human_review_recorded`는 현재 문맥과 결과에 맞는 승인
기록 여부를 보여 준다. `gaps: []`여도 승인 기록이 없으면 1이다. `status`는 정보 조회
명령이므로 준비 미완료일 때도 0을 유지한다. 파서의 `--help`는 일반 CLI 도움말이므로
동적 ID 앞에는 반드시 `--`를 둔다. ID가 `--help`여도 검사를 우회하지 못한다.

명령은 테스트를 대신 실행하거나 Pass를 생성하지 않는다. 수동 입력한 결과·승인의
진실성과 신원은 인증하지 않는다. CI는 파일의 일관성과 준비 상태를 재검사할 뿐이다.

## 이 저장소의 GitHub Actions

### 자동 회귀 검증

[CLI tests](../.github/workflows/ci.yml)는 `main` push, PR, 수동 실행에 반응한다.
Python 3.9와 3.13에서 `python3 -m unittest discover -s tests -v`를 실행한다.
실행 환경은 `ubuntu-24.04`로 고정한다. 최초 원격 실행에서 `ubuntu-latest`의 Ubuntu
26.04에는 Python 3.9 배포본이 없음을 확인했으며, 공식 제공 목록에 있는 24.04를
선택했다. 이는 CLI 테스트 실패와 구분되는 runner 호환성 수정이다.
테스트가 만드는 임시 승인자는 검증용 데이터이며 실제 변경의 승인 기록이 아니다.

### VAD 준비 상태 게이트

[VAD readiness](../.github/workflows/vad-check.yml)는 `main` 대상 PR에서 자동 실행한다.
PR은 `.vad/ci-change-id`에 검사할 변경 ID 하나를 기록한다. 파일이 없거나 ID가 잘못되면
검사는 실패한다. 과거 변경 기록 전체를 매번 검사하지 않는다.

수동 실행에서는 변경 ID를 필수 입력으로 받는다. 재사용 호출에서는 입력한 ID를
우선 사용하고, 생략하면 같은 선택 파일을 읽는다. 선택 값은 기존 CLI의 ID 검사로
검증한 뒤 `GITHUB_OUTPUT`에 기록해 줄바꿈이나 workflow 명령 주입을 차단한다.

Actions의 **VAD readiness → Run workflow**에서 대상 브랜치와 `change_id`를 선택한다.
GitHub CLI로도 실행할 수 있다:

```sh
gh workflow run vad-check.yml --ref main -f change_id=actual-change-id
```

게이트가 실패해도 보고서 단계와 업로드 단계를 실행하며 `vad-report`를 7일 보존한다.
Actions 실행 요약에는 검증 사유, 현재 승인 여부, 다음 조치와 전체 기록을 표시한다.
요약의 **Verification**과 **Human review**를 따로 확인한다. 검증이 모두 통과해도
**Pending: no approval record**이면 승인 대기이므로 게이트는 실패한다.
아티팩트에는 `check.json`과 가능한 경우 `report.md`가 있다. 입력 자체가 손상되었으면
파일이 비어 있을 수 있으므로 작업 로그의 오류도 확인한다. 출력은 runner 임시 폴더에
저장해 소스 지문에 영향을 주지 않는다. 자동 승인·자동 커밋·자동 배포는 수행하지 않는다.

모든 Action은 확인한 공식 저장소의 커밋으로 고정했다. ID는 환경 변수로 전달하고
인용한 셸 인자로 사용한다. `pull_request_target`, `secrets: inherit`, 쓰기 토큰은 사용하지 않는다.

### PR에서 필수 검사로 적용

PR 브랜치에 `.vad/ci-change-id`를 추가하거나 갱신한다. 예를 들어 파일 내용이
`ci-pr-enforcement`이면 `.vad/changes/ci-pr-enforcement.json`을 검사한다.
이 파일은 변경 기록 선택용 메타데이터다. 실제 소스와 계획의 일치 여부는 선택한
기록의 검증 문맥으로 별도 검사하며, 파일만 바꿔 오래된 증거를 재사용할 수는 없다.

PR의 실제 변경 ID를 선택해야 한다. 기본 checkout은 이벤트의
커밋을 사용하므로 PR의 병합 결과와 로컬 소스가 다르면 증거가 오래된 것으로 판단될 수
있다. 검사 대상 트리에서 검증·검토한 증거를 기록한다. 다른 저장소에 도입할 때는
`tools/vad.py`와 워크플로를 함께 배치한다. 재사용 워크플로는 호출자 저장소를 checkout한다.

PR 게이트의 검사 이름은 **VAD PR gate**다. 수동 실행은 **VAD readiness**라는 별도
이름을 사용하므로 수동 실행의 성공이 PR 필수 검사를 대체하지 않는다.

`main` 보호의 설정 목표는 다음과 같다. 실제 적용 여부와 검증 PR 결과는
`.vad/evidence/pr-gate/`의 저장된 API 응답과 GitHub PR 검사 결과로 확인한다.

| 보호 | 설정 |
| --- | --- |
| 필수 검사 | `VAD PR gate`, `tests (3.9)`, `tests (3.13)`; 실제 GitHub Actions App에 연결 |
| 최신 기본 브랜치 반영 | 필수 (`strict: true`) |
| PR을 통한 변경 | 필수 |
| 관리자 우회 | 불허 (`enforce_admins: true`) |
| 강제 push·브랜치 삭제 | 불허 |
| 미해결 대화 | 병합 전 해결 |
| 별도 GitHub 승인 리뷰 수 | 0명; 단독 관리자가 자신의 PR을 승인할 수 없는 잠금을 만들지 않음 |

VAD의 현재 문맥에 대한 사람의 승인 기록은 계속 필요하다. GitHub 추가 리뷰어 수를
0으로 두는 것은 VAD 승인 검사를 끄는 의미가 아니다. 편집 가능한 자체 신고 승인과
workflow 파일은 인증된 독립 보안 심사나 변조 방지를 제공하지 않는다. 팀이 생기면
별도 리뷰어·CODEOWNERS 정책을 추가해야 한다. 기존 비활성 ruleset은 변경하지 않는다.

새 PR의 소스·계획이 바뀌면 검증과 승인을 다시 받아야 한다. 기존에 열린 PR도 이
필수 검사와 선택 파일 준비가 필요하다. 테스트 중 실패한 PR을 강제로 병합하거나
검사 우회를 사용하지 않는다. 복구가 필요하면 관리자가 저장해 둔 이전 보호 설정을
기준으로 설정을 되돌릴 수 있다.

## 검증과 복구

구현 전 기존 상태·소스/계획 유효성·잘못된 계획·고위험 관련 테스트 4개가 통과했다.
새 게이트 검증은 준비 완료·실패·오류 코드 구분, 원본 보존, 승인 무효화, 안전한 ID
전달을 다룬다. 로컬 실행 로그는 `.vad/evidence/ci-integration/`에 저장한다.
실제 GitHub 실행 여부와 결론은 Actions 실행 기록을 확인한다. 로컬 성공만으로
원격 워크플로가 실행되었다고 주장하지 않는다.

### `VAD readiness #2` 실패에 대한 원인 조사

2026-11-18 조사에서 확인한 `#2`는 `cli-plan-import`의 차단 동작을 시험한 실행이었다.
기록된 검증 문맥이 이후 소스와 달랐고 실제 승인도 없어서 정상적으로 1을 반환했다.
설치 장애나 테스트 실행 실패가 아니며, 준비 미완료를 성공으로 바꿔서는 안 된다.
기존 화면은 일반적인 종료 코드 오류와 원인을 구분해 보여 주지 못했다.
수정은 읽기 쉬운 보고서와 Actions 요약 표시이며, 종료 코드 규칙은 유지한다.
자세한 근거와 재검증 절차는 [조사 보고서](./readiness-incident-2026-11-18.md)를 참고한다.

정상 차단을 확인하는 개발 테스트는 `CLI tests`의 `test_check_*` 시나리오에서 수행한다.
실제 `VAD readiness`에 미승인 변경을 넣으면 **정상적으로 빨간색 실패**가 표시된다.
이 실행을 도구 자체의 장애 진단이나 성공 데모로 사용하지 않는다.

도입을 되돌리려면 워크플로와 `check` 명령 추가를 되돌린다. 기존 기록과 CLI 명령의
형식은 유지되며 기록 삭제·배포 롤백은 필요 없다.

## 공식 동작 근거

* [재사용 워크플로](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
* [workflow_dispatch 및 이벤트](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
* [checkout](https://github.com/actions/checkout), [setup-python](https://github.com/actions/setup-python), [upload-artifact](https://github.com/actions/upload-artifact)
* [공식 Python 배포 환경 목록](https://github.com/actions/python-versions/blob/main/versions-manifest.json)
