# VAD readiness #2 원인 조사 및 수정

조사일: 2026-11-18 (Asia/Seoul).
대상: [실행 #2 / 44041006661](https://github.com/Richard-JHLee/ai-vad-methodology/actions/runs/44041006661),
소스 `3041c2ed9f05005a97c01ecb8f07f987f818e37d`, 변경 ID `cli-plan-import`.

## 확인된 원인

| 확인 항목 | 실제 결과 |
| --- | --- |
| checkout 및 Python 설치 | 성공 |
| `check` | `Not ready`, 종료 코드 1 |
| 검증 사유 | `regression`, `plan-import`, `docs`가 모두 `stale evidence` |
| 승인 | `human_review_recorded: false`, 실제 기록의 `approvals`가 비어 있음 |
| 보고서·진단 업로드 | 성공; `check.json`과 `report.md` 보존 |

코드는 원래부터 현재 소스·계획에 맞는 증거와 사람이 남긴 승인 기록을 요구한다.
이 사례의 검증은 CLI 계획 가져오기를 구현하던 소스에 연결되어 있었다. 이후 CI
구현과 runner 수정으로 소스가 바뀌었으므로 옛 결과를 재사용할 수 없다.
당시 실제 사람의 승인은 일부러 비워 두었다. 따라서 차단 자체는 요구한 동작이다.

이 실행은 이전 CI 개발 중 차단 동작과 보고서 보존을 확인하려고 실행한 음성 테스트였다.
일반 준비 상태 검사와 구분되는 설명 없이 실패 실행이 남아 도구 장애로 보이게 했다.
보고서도 전체 JSON에 치우쳐 있어 사용자가 해결 순서를 바로 확인하기 어려웠다.
이번에 고치는 결함은 **실패 원인과 다음 조치의 전달 부족**이다.

## 영향과 수정

* `tools/vad.py`의 `report`만 검증·승인·다음 조치·전체 기록으로 나눈다.
* `.github/workflows/vad-check.yml`은 같은 보고서를 아티팩트와 Actions 요약에 저장한다.
* 준비 상태 판단과 `check`의 0/1/2 종료 코드, 읽기 전용 정책은 유지한다.
* 검증 사유는 들여쓴 JSON으로 표시한다. 보고서 본문은 workflow 로그 대신 파일과
  요약에 써서, 본문을 workflow 명령으로 해석하거나 HTML로 렌더링하지 않게 한다.
* 기존 테스트에 승인 대기/승인 완료/오래된 증거/미완성 계획의 보고서 검증을 추가한다.

영향 경로는 `execute(report) → status → assess`와 Actions의 보고서 출력이다.
상태 판단은 바꾸지 않으며 실제 승인자를 자동 생성하지 않는다. 업무 데이터·권한·
배포 설정은 변경하지 않는다. 기존 검증 6개를 수정 전에 실행해 모두 통과했다.

## 해당 변경 건의 처리

현 소스에서 관련 테스트, 문서 검증, 실제 계획 내보내기·가져오기를 다시 실행한다.
통과한 결과만 `cli-plan-import` 기록에 추가한다. 옛 결과와 실패 기록은 삭제하지 않는다.
갱신한 계획·검증 기록·보고서는 사람의 검토 대상이며 승인을 대신하지 않는다.

자료는 `.vad/evidence/readiness-diagnostics/`에 보존한다. 갱신 후 상태는 다음 명령으로 확인한다:

```sh
python3 tools/vad.py status cli-plan-import
python3 tools/vad.py report cli-plan-import
```

검증 사유가 없어져도 현재 승인 기록이 없으면 `Not ready`다. 관리자가 변경·영향·
복구 계획과 실제 검증 자료를 검토한 후에만 본인 이름으로 승인할 수 있다:

```sh
python3 tools/vad.py approve cli-plan-import --reviewer "검토한 사람의 이름" --attest-human-review
python3 tools/vad.py check -- cli-plan-import
```

승인 기록을 GitHub에 저장하고 해당 소스를 대상으로 다시 실행해야 한다. 검증·승인
이후 소스·계획·결과가 바뀌면 필요한 검증과 승인을 다시 받는다. GitHub의 과거 #2
실행 결과는 역사적 실패 기록이며 이번 수정으로 소급해서 성공으로 바뀌지 않는다.

## 범위 밖

실제 사람의 검토·승인, 신원 인증, 브랜치 보호 변경은 수행하지 않는다.
실제 게이트에 `continue-on-error`를 넣거나 강제로 종료 코드 0을 반환하지 않는다.
Windows와 운영 배포 검증은 이번 변경의 영향 밖이다.
