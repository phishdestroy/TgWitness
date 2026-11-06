# 명령줄

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/cli/

스크립트 및 에이전트를 통해 메시지를 검색하고, 문맥을 확인하며, 활동 횟수를 집계하고, 저장된 메시지를 내보낼 수 있으며, --json 출력, 안정적인 종료 코드 및 범위 지정된 읽기 전용 토큰을 지원합니다.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [문서](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![아카이브 연동](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

[읽기 전용 MCP](https://phishdestroy.github.io/TgWitness/ko/docs/reference/mcp/) · [전체 텍스트 검색](https://phishdestroy.github.io/TgWitness/ko/docs/reference/search/) · [위키](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**미리 보기.** `tgwitness search`, `context`, `messages`, `stats` 그리고 `export` 스크립트 및 AI 에이전트를 위해 저장된 관측 내용을 읽을 수 있습니다. 이 도구들은 텔레그램으로 아무것도 전송하거나, 설정을 변경하거나, 서명된 일지를 수정할 수 없습니다.

이 경우 `--json`, stdout에는 정확히 하나의 JSON 문서가 출력됩니다(`export` JSON Lines 형식으로 출력). 진행 상황, 힌트 및 오류는 stderr로 출력됩니다. 종료 코드는 안정적입니다:

| 코드 | 의미 |
| --- | --- |
| `0` | 성공(결과가 비어 있는 경우 포함) |
| `1` | 오류: 패널에 접근 불가, 데이터 판독 불가, 내보내기 중단 |
| `2` | 사용법 오류 또는 유효하지 않은 요청: 잘못된 날짜, 알 수 없는 옵션, 검색 인덱스 비활성화 |
| `3` | 현재 사용할 수 없음: 작업 공간이 실행 중인 패널에 열려 있거나, 패널에서 나중에 다시 시도하라는 메시지가 표시됩니다(속도 제한, 시간 초과). |
| `4` | 접근 거부: 토큰이 없거나, 만료되었거나, 취소된 경우, 허용 범위를 벗어난 채팅, 허용되지 않는 도구 |

## 읽는 두 가지 방법

**패널(`--url`)을 통해** 사용합니다**.** 이 명령어는 MCP와 동일한 범위 지정 아카이브 API를 사용합니다. **'통합(Integrations)' →**'MCP**'에서** 연결을 생성하세요: 워크스페이스와 채팅, 도구 및 만료 기간을 선택한 후 토큰을 한 번 복사하세요. 이 연결은 읽기 전용이며, 선택한 채팅으로만 제한되고, 분당 60회 요청으로 속도 제한이 적용되며, 언제든지 취소하거나 갱신할 수 있습니다. 패널 로그인 토큰과 텔레그램 인증 정보는 여기에서 작동하지 않습니다.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

원격 패널에는 HTTPS가 필요합니다. 일반 HTTP는 다음의 경우에만 허용됩니다 `127.0.0.1`, `localhost` 및 `::1`에 대해서만 허용됩니다. 프록시 환경 변수는 무시되며 리디렉션은 허용되지 않으므로, 토큰은 사용자가 지정한 주소로만 전달됩니다.

**중지된 워크스페이스(`--data-dir`)에서 직접** 실행합니다**.** 토큰 없이 로컬에 대한 전체 액세스 권한으로 데이터 디렉터리를 읽습니다. 데이터 디렉터리의 복사본에서 사용하거나 데이터 수집이 중지된 상태에서 사용하십시오. 서명된 레코드는 절대 변경되지 않습니다. 패널과 마찬가지로, 워크스페이스를 열면 파생된 인덱스가 최신 상태로 업데이트될 수 있습니다. 패널에서 워크스페이스가 열려 있는 경우, 이 명령어는 코드 `3`로 종료됩니다; 대신 패널을 통해 읽어보십시오. `--data-dir`, `TGWITNESS_DATA`, `./data/live` 이 옵션이 없으면 명령을 실행하는 설치 환경의 데이터 디렉터리가 사용됩니다.

`--workspace ID` 워크스페이스를 선택합니다(기본값 `default`). `tgwitness messages
--workspaces` 읽을 수 있는 워크스페이스 목록을 표시합니다.

## 명령어

| 명령어 | 결과 |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | 가장 일치도가 높은 결과부터 우선 표시하며, 단어 형태, 따옴표로 묶인 정확한 구문, 도메인 및 `@username` ([구문](https://phishdestroy.github.io/TgWitness/ko/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | 정확한 텍스트, 최신 내용부터 순서대로, 색인 제외 |
| `tgwitness context CHAT_ID MESSAGE_ID` | 양쪽 방향으로 메시지 ID 기준 10개 범위 내의 저장된 메시지 |
| `tgwitness messages` | 읽을 수 있는 채팅 |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | 채팅에서 저장된 메시지, 최신순으로 표시 |
| `tgwitness messages CHAT_ID --message ID` | 단일 메시지의 모든 저장된 버전 및 삭제 기록 |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | 활동 통계는 아래와 같습니다. |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | 관측 기록은 저널 순서대로 JSON Lines 형식으로 저장됨 |

날짜는 `2026-10-01` (UTC 자정) 또는 시간대가 명시된 ISO 형식입니다. `2026-10-01T09:00+03:00`. `search`, `messages` 및 `export` 의 경우 관찰 시간을 선택합니다. 각 페이지에는 최대 50개의 기록이 표시되며, 순위 기반 검색을 위해서는 `next_offset` (`--offset`)를 따라 순위별 검색을 수행하고 `next_before` (`--before`)는 다른 곳에서 참조하십시오.

순위별 검색은 1,000개의 결과에서 중단됩니다. 마지막 페이지의 결과 수는 `--limit`보다 적을 수 있습니다. 일치하는 관측 결과가 더 많은 경우, 검색어, 채팅 또는 기간을 좁혀 주세요.

모든 메시지 결과에는 `untrusted_content: true`, 워크스페이스, 채팅 및 메시지 ID, 저널 순서, 저장된 기록 해시, 패널 링크를 포함합니다. 수정, 삭제 알림 및 `missing_on_recheck` 는 별도의 기록으로 처리됩니다. 기록이 없다고 해서 해당 사건이 발생하지 않았음을 증명하는 것은 아닙니다.

### 활동 통계

`stats` 지정된 범위 내의 특정 채팅, 특정 발신자 또는 모든 채팅에 대한 저장된 관측 기록 수를 집계합니다:

- UTC 시간대별 및 요일별(월요일부터 시작) 메시지, 가장 이용이 많은 시간대와 요일;
- 수정, 삭제 및 `missing_on_recheck` 공유;
- 메시지 수와 첫 번째 및 마지막 메시지 시간을 포함한 발신자;
- 가장 빈도가 높은 도메인과 `@handles`, 저장된 모든 버전을 통틀어 메시지당 한 번씩 집계된 도메인;
- 다루는 내용: `coverage.gap` 기록 및 전체 작업 공간에 대한 접근을 위해, 연결된 수집기의 하트비트가 없는 기간 (`collector_liveness`).

이 기간은 **텔레그램에서 보고한 메시지 시간을** 기준으로 합니다. 시간 및 요일 횟수는 발신자의 시간대를 추정하는 데 도움이 될 수 있으나, 이를 확정하는 것은 아닙니다. 수치는 저널에서 요청 시 계산되며 저장되지는 않습니다. 각 결과는 액세스 범위가 워크스페이스를 넘어갈 경우 해당 범위를 포함하는 저널 헤드의 이름을 표시합니다. 패널을 통해 5초가 지나거나 로컬에서 `--timeout` 로컬에서 5초(기본값 30초)가 지나면 중단됩니다. 그 후 `complete` 는 false이며 `partial` 읽지 않은 첫 번째 레코드의 이름을 반환합니다. 이 경우 가장 최근의 레코드만 계산됩니다.

### 내보내기

`export` 저장된 관측 항목(새 메시지, 스냅샷, 수정 내역, 복구된 메시지, 삭제 알림, `missing_on_recheck` 저장된 미디어 기록)에 대해 저널 순서대로 하나의 JSON 객체를 작성합니다. 각 행은 다른 결과와 동일한 필드를 가지며, 전체 텍스트가 포함됩니다. `--output`, 파일은 `.partial` 이름으로 저장되며, 패널의 완료 기록이 생성된 후에만 이름이 변경됩니다. 내보내기가 중단된 경우 파일은 생성되지 않으며, 종료 코드는 `1`. `--output` 기존 파일을 절대 덮어쓰지 않습니다. `--output` 및 `--json`를 함께 사용할 경우, stdout을 통해 요약 정보(레코드 수, 마지막 저널 시퀀스, 전체 작업 공간에 대한 액세스 시 저널 헤더)가 출력됩니다.

패널을 통한 내보내기를 수행하려면 **메시지 내보내기가** 허용되는 연결이 필요합니다 **(명령줄 전용)**; 이 기능은 기본적으로 선택되어 있지 않습니다. 이 파일은 작업용 사본일 뿐 증거 자료가 아닙니다. 검증 가능한 인계를 위해서는 **‘내보내기’** 메뉴에서 서명된 내보내기 파일을 사용하십시오. 이 파일은 `python -m tgwitness.verify`검증 과정을 거칩니다.

패널은 완료 레코드를 포함하여 각 레코드를 출력하기 전에 액세스 권한을 재확인합니다. 취소되거나 만료된 액세스 권한은 불완전한 내보내기 결과를 초래합니다. 지연 페이지 읽기는 다른 쿼리와 아카이브 작업자 한도를 공유하며 대기 시간이 제한되어 있습니다.

## 에이전트 스킬

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) 에는 에이전트가 이러한 명령어를 사용하는 방법, 기록을 인용하는 방법, 그리고 캡처된 텍스트를 처리하는 방법이 설명되어 있습니다. 다음을 수행하는 에이전트 `.agents/skills` 리포지토리 체크아웃에서 이를 불러옵니다. Claude Code의 경우, `tgwitness-cli` 폴더를 `.claude/skills/` 내 프로젝트 폴더로 복사하거나 `~/.claude/skills/`.

## MCP 및 명령줄

두 도구 모두 동일한 연결, 범위 확인 및 제한 사항을 사용합니다. MCP 결과는 64 KiB 페이지 1개로 제한되므로 MCP는 대량 내보내기 기능을 제공하지 않으며, 명령줄을 통해 스트리밍됩니다. `get_activity_stats` 두 도구 모두에서 사용할 수 있습니다.
