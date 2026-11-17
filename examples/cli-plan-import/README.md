# 실제 적용 사례: VAD CLI의 안전한 계획 가져오기

이 사례는 가상의 앱이 아니라 `ai-vad-methodology` 저장소의 실제 CLI 변경이다.
도구의 개선 효과가 일반적으로 입증되었다는 의미는 아니다. 요구사항과 관찰된 실행
결과, 아직 받지 않은 사람의 승인을 구분한다.

## 요구사항과 영향 분석

실사용을 시작하자 `init`이 만든 JSON의 `plan`을 직접 편집해야 했다. 같은 파일에
검증 결과와 승인 기록이 있어 계획 편집 중 다른 기록을 손상시킬 여지가 있었다.
이를 줄이기 위해 **계획만 내보내고 검증해 가져오는 `plan` 명령**을 추가했다.

위험은 Medium으로 분류했다. 네트워크·업무 API·인증 권한은 바뀌지 않지만 기존 기록에
쓰는 명령을 추가하므로 데이터 보존과 잘못된 승인 재사용을 확인해야 한다.

실행 경로는 `parser → execute → paths/load/plan_errors → locked/save`다.
기존 저장·잠금·검증 함수를 재사용한다. 스키마 마이그레이션이나 새 의존성은 없다.
공통 명령 분기와 저장 경로에 연결되므로 신규 검증 뒤 기존 CLI 테스트 모음도 실행한다.

| 수용 기준 | 검증 |
| --- | --- |
| 미완성 초안도 계획만 JSON으로 내보내며 원본을 쓰지 않는다 | 초안 export 전후 바이트 비교 |
| 유효한 계획만 가져오고 결과·승인 이력을 보존한다 | 초안 완성, 기존 기록 교체, 이력 비교 |
| 잘못된 입력·누락 파일·잠금·심볼릭 링크는 원본을 보존하며 거절한다 | 명령 수준 실패 경로 검증 |
| 달라진 계획은 증거·승인을 무효화하고 동일한 계획은 유효성을 유지한다 | 문맥 및 상태 비교, 재검증·재승인 테스트 |
| 기존 명령이 유지되고 실제 사례에 사람의 승인을 꾸며 넣지 않는다 | 회귀 테스트와 실제 상태 확인 |

상세 요구사항·환경·검증 선택은
[실제 변경 기록](../../.vad/changes/cli-plan-import.json)의 `plan`에 있다.
소유자는 저장소 관리자로 두고 사람의 검토는 미완료로 표시했다.

## 변경 전 기준과 실패 재현

구현 전 관련 기존 검증 5개를 실행해 통과를 확인했다. 초안·입력 형식·계획 변경 시
유효성·검증/승인 흐름·저장 경로와 잠금 처리가 기준이었다.
[변경 전 테스트 로그](../../.vad/evidence/cli-plan-import/baseline-tests.txt)를 보존했다.

`python3 tools/vad.py plan cli-plan-import`는 기존 CLI에서 `invalid choice`와
종료 코드 2로 실패했다. 이 결과를 숨기지 않고 `plan-import: Fail`로 기록했다.
[실패 재현 로그](../../.vad/evidence/cli-plan-import/baseline-plan-command.txt)와 이후
결과는 같은 변경 기록에 누적된다. 새 내보내기 테스트도 구현 전 실패를 확인했다.

처음에는 가져오기 명령이 없어서 이 사례의 계획을 기존 방식으로 직접 작성했다.
이 초기 수작업이 이번 개선의 출발점이다. 구현 후에는 새 명령으로 같은 실제 계획을
내보내고 다시 가져와서 이력이 유지되는지 확인한다.

## 변경과 사용 방법

```sh
python3 tools/vad.py init my-change --title "Actual change" --owner "Developer"
python3 tools/vad.py plan my-change > .vad/my-change-plan.json
# 파일에 실제 목적, 영향, 수용 기준, 검증, 환경, 복구 방법을 작성한다.
python3 tools/vad.py plan my-change --file .vad/my-change-plan.json
python3 tools/vad.py status my-change
```

가져오기는 완성된 계획만 허용한다. 전체 변경 기록을 입력하거나 필수 항목을 비우면
거절하며 기존 파일을 덮어쓰지 않는다. 기존 기록의 `schema_version`, `results`,
`approvals`는 그대로 유지한다. 달라진 계획은 이전 증거를 새 결과로 바꾸지 않는다.

| 파일 | 변경 |
| --- | --- |
| `tools/vad.py` | `plan ID` 내보내기와 `plan ID --file FILE` 검증 후 가져오기 |
| `tests/test_vad.py` | 공개 명령을 실행하는 새 시나리오 5개 |
| `tools/README.md` | 변경 기록 직접 편집 대신 계획 파일 편집·가져오기 안내 |
| `docs/vad-cli-plan.md` | 실행 흐름·명령 목록과 실제 적용 결과 연결 |
| 이 사례 및 `.vad/` | 계약, 변경 전 실패, 실행 근거, 누적 결과와 보고서 보존 |

## 검증 결과와 남은 승인

실행 근거는 다음 파일에서 확인한다. 로그는 직접 실행한 출력이며 가상 성공 예제가 아니다.

* [최종 CLI 테스트 로그](../../.vad/evidence/cli-plan-import/final-tests.txt)
* [문서·구문·공백 검증 로그](../../.vad/evidence/cli-plan-import/docs-checks.txt)
* [이 저장소에서의 실제 가져오기·입력 거절·이력 보존 확인](../../.vad/evidence/cli-plan-import/actual-workflow.json)
* [CLI가 생성한 최종 보고서](../../.vad/evidence/cli-plan-import/report.md)

변경 전 Pass/Fail도 남겨 두고 최종 결과를 추가한다. 검증이 통과하더라도 실제 변경의
`approvals`는 비워 둔다. 따라서 최종 판단은 **Not ready — 사람의 검토 대기**다.
테스트 안의 임시 승인자는 동작 검증용 데이터이며 실제 저장소 관리자의 승인이 아니다.
커밋·푸시 허용과 소프트웨어 변경의 검토 승인은 구분한다.

## 복구와 한계

`plan` 명령 추가를 되돌려도 기존 스키마와 기록을 읽을 수 있다. 계획 복구가 필요하면
Git의 이전 기록을 확인해 계획을 다시 가져온다. 원본 JSON이 손상되었으면 Git에서
복원한 뒤 사용한다. 자동 배포나 업무 데이터 변경은 없다.

검증은 이 작업의 macOS/Python 환경에서 수행한다. Python 3.9는 구문 호환성만 확인하며
런타임·Windows·다른 실제 서비스는 검증하지 않는다. 기록과 승인자는 편집 가능한
자기 신고 자료이며 신원 인증이나 변조 방지를 제공하지 않는다.
