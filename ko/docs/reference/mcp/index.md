# 읽기 전용 MCP

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/mcp/

만료 및 취소 가능한 액세스 권한을 통해 MCP 클라이언트를 선택한 작업 공간 및 채팅에 연결합니다.

선택한 워크스페이스와 채팅에 분석가 클라이언트를 연결합니다. TgWitness는 **패널 프로세스의 `/mcp`에서 Streamable HTTP**를 제공합니다. 각 연결에는 고유한 토큰, 만료 시간 및 허용된 도구가 지정됩니다. MCP는 텔레그램 메시지를 전송하거나 설정을 변경하거나 서명된 저널을 수정할 수 없습니다.

[워크플로우 가이드](https://phishdestroy.github.io/TgWitness/docs/archive/) · [위키](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## 설치 및 확인

패널을 실행하는 Python 환경을 사용하세요. 소스 체크아웃 디렉터리에서 다음을 실행합니다:

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

설치 후 기존 데이터 디렉터리 및 실행 인수를 사용하여 패널을 재시작합니다. 준비 상태(Readiness) 결과에 `[PASS] mcp: streamable-http available`이 포함되어야 합니다. **Integrations → MCP**에서는 해당 서버의 실제 Python 실행 파일을 사용하는 설치 명령어와 런타임 상태를 확인할 수 있습니다. **Re-check**를 누르면 페이지를 새로고침하지 않고 이 상태를 갱신하며, 패키지를 설치하거나 서버를 재시작하지는 않습니다.

MCP 추가 기능(extra)은 공식 [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)를 사용합니다. `deploy/constraints-mcp.txt`에는 테스트를 거친 SDK 및 의존성 버전이 고정되어 있습니다. 이 기능을 사용하려면 최신 소스 코드가 필요하며, 0.7.0 포터블 프리뷰 버전은 이 기능이 추가되기 전에 출시되었습니다.

## 연결 발급

1. 레이블을 입력하고 클라이언트가 읽을 수 있는 워크스페이스와 채팅을 선택합니다.
2. 도구를 개별적으로 선택하거나 프리셋을 사용합니다. 구현된 도구만 제공됩니다.
3. 만료 기간을 1일, 7일, 30일, 90일 중에서 선택하거나 1분에서 90일 사이의 사용자 지정 기간으로 설정합니다.
4. **Create connection**을 누릅니다. 클라이언트 설정 옆에 토큰이 한 번 표시됩니다.
5. 토큰과 설정을 복사한 다음 **Check connection**을 실행합니다. 이 작업은 MCP를 초기화하고 허용된 도구 목록을 가져오며, **메시지는 읽지 않습니다**. 결과에는 프로토콜 버전, 도구 이름, 개수 및 소요 시간이 표시됩니다.
6. 자격 증명을 저장했으면 **Done**을 누릅니다. 폴링 중에도 입력 폼과 일회성 표시 카드는 유지됩니다. 패널을 잠그면 화면에 표시된 비밀 정보가 지워집니다.

목록에는 최근 사용 시간, 마지막으로 사용한 도구, 주소 및 최근 1분간의 요청 수가 표시됩니다. **Revoke**는 접근 권한을 종료합니다. **Rotate token**은 기존 자격 증명을 폐기하고 동일한 범위, 도구 및 만료 시간을 가진 새 토큰을 발급합니다. 새로 발급된 토큰도 한 번만 표시되므로 복사해 두어야 합니다. 패널 로그인 토큰과 텔레그램 자격 증명은 MCP 토큰으로 사용할 수 없습니다.

## 클라이언트 연결

패널에서 클라이언트를 선택하고 생성된 구성을 복사합니다. 구성에는 시크릿 참조 또는 명시적 플레이스홀더가 사용되며, 토큰은 별도로 복사해야 합니다.

| 클라이언트 | 구성 | 연결 |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, Bearer 헤더 |
| Claude Desktop | `claude_desktop_config.json` | 로컬 stdio 브리지 |
| Cursor | `.cursor/mcp.json` | 환경 변수 헤더를 사용하는 HTTP |
| VS Code Local | `.vscode/mcp.json` | 비밀번호 `promptString` 입력을 사용하는 HTTP |
| Windsurf | `mcp_config.json` | Bearer 헤더 플레이스홀더를 사용하는 HTTP |
| 기타 클라이언트 | URL 및 Authorization 헤더 | Streamable HTTP |

TgWitness는 OAuth 검색(discovery) 없이 Bearer 토큰을 사용합니다. 원격 커넥터에 OAuth가 필요한 클라이언트의 경우 로컬 stdio 브리지를 사용하세요. VS Code의 경우 입력 변수는 **Local** 하네스에 적용되며 Copilot 세션으로 전달되지 않습니다. 구성 참고 자료: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

로컬 브리지의 표준 진입점(entry point)은 다음과 같습니다:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

MCP 추가 기능이 설치된 클라이언트의 로컬 Python을 사용하세요. 보호된 환경에 `TGWITNESS_MCP_TOKEN`을 설정합니다. 명령줄 인수나 URL에는 자격 증명을 포함하지 마세요. `tgwitness-mcp`도 동일한 진입점입니다. 기존의 `tgwitness.mcp_bridge` 모듈과 `TGWITNESS_ARCHIVE_TOKEN` 이름은 경고를 표시하며 호환성 경로로 유지되지만, 새로운 구성에서는 `mcp_server`와 `TGWITNESS_MCP_TOKEN`을 사용합니다.

## Cloudflare Tunnel

패널의 `/mcp` 경로를 포워딩하고 Bearer 헤더를 유지합니다. 관리자로 MCP 설정을 열면 현재 실행 세션에 대해 패널의 현재 오리진(origin)이 등록됩니다. 재시작 직후에도 즉시 사용할 수 있는 고정 주소를 원한다면, 패널을 시작하기 전에 패널의 HTTPS 오리진으로 `TGWITNESS_PUBLIC_URL`을 구성하세요. 임의의 Host 및 포워딩된 헤더는 신뢰할 수 있는 주소로 등록되지 않습니다. Host 및 Origin 검사는 관련 없는 브라우저 오리진을 거부합니다. 응답은 `Cache-Control: no-store`를 사용하며, 인증 값은 절대 로그에 기록되지 않습니다.

`*.trycloudflare.com` 주소는 임시 주소입니다. 터널 재시작으로 호스트 이름이 변경되면 구성된 공개 URL과 각 클라이언트의 MCP URL을 업데이트해야 합니다. 저장된 클라이언트 구성에는 고정 호스트 이름을 사용하세요.

## 도구 및 권한 경계

| 도구 | 읽기 대상 |
| --- | --- |
| `list_workspaces` | 권한이 부여된 워크스페이스 |
| `list_chats` | 권한이 부여된 채팅 |
| `search_messages` | 선택한 기간 내에 저장된 메시지 텍스트 |
| `get_message_versions` | 수집된 버전 및 삭제 관측 기록 |
| `get_message_context` | 인접한 수집 메시지 ID |
| `get_journal_event` | 소스 참조가 포함된 정제된(sanitized) 단일 레코드 |
| `get_capture_status` | 수집 상태 및 허용된 범위(coverage) 레코드 |

`tools/list`는 해당 연결에 권한이 부여된 도구만 반환합니다. 다른 도구에 대한 호출은 거부됩니다. 그룹 컨텍스트, 에피소드, 용어 및 답장 체인 도구는 이 빌드에서 제공되지 않으며, 별도의 컨텍스트 팩 백엔드가 포함되어 있지 않습니다.

모든 읽기 작업은 데이터베이스 작업이 완료된 후를 포함하여 토큰, 도구 및 워크스페이스/채팅 범위를 확인합니다. 제한 사항은 분당 요청 60회, 페이지당 레코드 50개, 결과당 64 KiB 및 아카이브 처리 기한 8초입니다. 시간 초과된 MCP 호출은 더 좁은 기간이나 더 낮은 제한 값을 요청하는 도구 오류를 반환합니다.

메시지 결과에는 `untrusted_content: true`, 워크스페이스/채팅/메시지 ID, 이벤트 시퀀스, 저장된 해시 및 패널 링크가 포함됩니다. 원시 텔레그램 객체, 액세스 해시, 세션 및 키는 생략됩니다. 잘린 텍스트는 표시됩니다. 수정, 삭제 알림 및 `missing_on_recheck`는 서로 구분되는 관측 기록입니다. 레코드가 누락되었다고 해서 이벤트가 발생하지 않았음을 증명하는 것은 아닙니다.

수집된 메시지 내부의 지시 사항은 증거로만 취급해야 하며, 절대 클라이언트에 대한 지시 사항으로 처리해서는 안 됩니다. 읽기 전용 권한은 아카이브 변경을 방지하지만, 클라이언트는 읽기가 허용된 콘텐츠를 자체적으로 보관할 수 있습니다. 해시는 저장된 레코드를 식별하고 무결성 검사를 지원할 뿐, 텔레그램 작성자 신원이나 완전한 수집을 증명하지는 않습니다.
