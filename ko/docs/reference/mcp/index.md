# 읽기 전용 MCP

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/reference/mcp/

만료 및 취소 가능한 액세스 권한을 통해 MCP 클라이언트를 선택한 작업 공간 및 채팅에 연결합니다.

**현재 메인 버전:** 소스 체크아웃을 사용하십시오. 0.7.0 휴대용 미리보기 버전은 이 기능이 구현되기 전의 버전입니다.

[워크플로우 가이드](https://phishdestroy.github.io/TgWitness/docs/archive/) · [위키](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

TgWitness 프로젝트 디렉터리에서 선택적 서버를 설치하십시오:

```
python -m pip install '.[mcp]'
```

패널에서 **‘통합(Integrations)’ → ‘MCP’를** 엽니다. 연결 이름을 지정하고, 해당 워크스페이스 및 채팅을 선택한 다음, 만료 기간을 설정합니다. 아카이브 토큰은 한 번만 복사하십시오. 나중에 다시 불러올 수 없습니다. 분실한 토큰은 취소하고 새 토큰을 발급받으십시오. 패널 토큰과 텔레그램 인증 정보는 MCP 인증 정보와 다릅니다.

## 클라이언트 연결

이 패널은 [문서화된 구성](https://code.visualstudio.com/docs/agents/reference/mcp-configuration) 설정을 사용하여 **VS Code 로컬**하네스용 `.vscode/mcp.json`를 생성합니다. 다운로드한 파일을 해당 **위치에 저장하고, MCP: List Servers를 실행한 후** 다운로드한 파일을 해당 위치에 저장하고, **MCP: List Servers를** 실행한 후 TgWitness를 시작하십시오. VS Code는 비밀번호 입력 창을 통해 토큰 입력을 요청합니다. 다운로드한 JSON 파일에는 토큰이 아닌 프롬프트 참조 정보가 포함되어 있습니다. MCP 엑스트라가 설치된 환경에서 Python 실행 파일을 사용하십시오.

다른 stdio 클라이언트의 경우 다음 명령을 실행하십시오:

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

클라이언트의 보호된 환경에 `TGWITNESS_ARCHIVE_TOKEN`를 설정하십시오. 이를 명령어 인자나 URL에 포함하지 마십시오. 브리지는 패널의 인증된 아카이브 API를 통해 데이터를 읽으며, 데이터베이스에 직접 접근할 수 없습니다. 표준 출력(stdou)에는 MCP 메시지만 전송됩니다.

원격 클라이언트의 경우, 패널과 함께 서비스를 실행하십시오:

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

HTTPS 리버스 프록시를 통해 `/mcp`를 `127.0.0.1:8766/mcp`로 전달하되, `Authorization: Bearer …` 헤더는 유지합니다. 인증 헤더 및 요청/응답 본문의 로깅을 비활성화합니다. 필요한 경우에만 `--host` 및 `--public-url`를 사용하여 루프백 외부의 주소에 바인딩합니다. 이 엔드포인트는 공식 [MCP Python](https://github.com/modelcontextprotocol/python-sdk)SDK의 Streamable HTTP를 사용합니다. 이 엔드포인트는 OAuth 탐색이 아닌 명시적으로 구성된 베어러 자격 증명을 지원하며, OAuth만 요구하는 클라이언트는 지원되지 않습니다.

**프로토콜 확인 및 액세스** 단계에서는 실제 MCP 클라이언트를 초기화하고 도구를 나열합니다. 이 단계에서는 메시지를 가져오지 않습니다. 원격 확인의 경우, 선택된 MCP 서버가 아카이브 토큰을 수신합니다. 해당 권한 범위 내에서 본인이 운영하거나 신뢰하는 서버만 구성하십시오.

## 범위 및 결과

사용 가능한 도구: `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event` 및 `get_capture_status`. 텔레그램 내 작업, 설정 변경 또는 대량 내보내기 도구는 제공되지 않습니다. 읽기 작업 시마다 작업 공간/채팅 접근 권한을 재확인하며, 만료되거나 취소된 인증 정보는 더 이상 작동하지 않습니다. 제한 사항은 인증 정보당 분당 60회의 API 요청, 페이지당 50건의 기록, 64 KiB 응답 크기, 8초의 API 응답 시간입니다.

메시지 결과에는 작업 공간, 채팅/메시지 ID, 이벤트 순서, 저장된 해시, 및 패널 링크가 포함됩니다. 링크를 여는 뷰어는 자체적으로 인증된 패널 세션을 보유하고 있어야 합니다. 원시 텔레그램 객체, 액세스 해시, 파일 참조, 세션 자료, 및 키는 생략됩니다. 검색은 원시 필드가 아닌 메시지 텍스트를 대상으로 합니다. 텍스트는 범위가 제한되며, 잘린 부분은 표시됩니다. 수정 내역, 텔레그램 삭제 알림 및 `missing_on_recheck`는 별도의 관측 항목으로 처리됩니다. 채팅 범위 내 접근 권한으로는 워크스페이스 전체의 운영 이벤트를 볼 수 없으며, 캡처 상태가 이 제한을 명확히 표시합니다.

아카이브 텍스트는 신뢰할 수 없는 입력 데이터입니다. 메시지 내의 지침은 어떠한 추가적인 권한도 부여하지 않으며, 클라이언트의 지침으로 간주되어서는 안 됩니다. 외부 AI 모델은 MCP 클라이언트가 요청하는 모든 콘텐츠를 수신할 수 있습니다. 읽기 전용 액세스 권한은 아카이브의 변경을 방지할 뿐이며, 클라이언트가 읽은 데이터를 보유하는 것을 막지는 않습니다.

해시 값은 저장된 기록을 식별하고 무결성 검사를 지원합니다. 해시 값 자체만으로는 텔레그램의 작성자 신원을 입증하거나 모든 메시지가 캡처되었음을 입증할 수는 없습니다.
