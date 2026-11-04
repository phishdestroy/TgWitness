# 아카이브 활용하기

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/archive/

메시지를 찾아보세요. 출처를 확인하세요. 증거를 구축하세요.

01**이력을 불러오기**

활성화된 소스의 지난 메시지를 작업 공간으로 가져옵니다.

02**출처를 확인하세요**

검색한 다음, 각 결과 뒤에 있는 저장된 메시지를 엽니다.

03**인계 과정을 명확히 하십시오**

분석은 파일 하나에, 서명된 증거는 그 옆에.

캡처된 기록, 인식된 텍스트 및 분석가의 결론은 명확히 구분됩니다.

## 이전 메시지 불러오기

1. **소스 → 범위 내 채팅**: 활성화된 채팅을 확인하고 관찰을 시작합니다.
2. **전체 기록 불러오기**. 지금 이 순간의 소스 목록을 그대로 사용합니다.
3. 언제든 **기록 일시 중지** / **기록 계속**. 재시작 후에는 직접 다시 시작하십시오.
4. 소스별 결과와 다운로드 대기열을 확인하고, 서명된 진행 보고서를 내보내기와 함께 보관합니다.

이것은 작업 공간을 채웁니다. 단일 채팅의 HTML/JSON 내보내기는 별개입니다. [자세히](https://phishdestroy.github.io/TgWitness/ko/docs/reference/history/).

## 먼저 검색한 후, AI 사용 여부를 결정하세요

1. **저널**은 로컬에서 검색하며, 소스와 시간으로 필터링합니다.
2. 구문이나 도메인을 검색하고, 기록과 그 버전을 엽니다.
3. AI를 쓰려면 관리자가 **연동 기능**에서 공급자를 설정합니다. 그런 다음 **아카이브에 문의하기**에서 채팅과 기간을 고르고, **모델로 전송된 데이터**를 살펴보고, 내보내면 안 되는 항목의 체크를 해제합니다.
4. 인용을 확인하고, 답변을 보고서로 저장하고, 메모를 추가합니다.

검색에는 AI가 필요 없습니다. 보고서는 서명된 저널과 별도로 출처와 수정본을 보관합니다. [공급자 설정](https://phishdestroy.github.io/TgWitness/ko/docs/reference/analysis/).

## 필요한 연결 방식을 선택하세요

| 과제 | 열기 | 설정 |
| --- | --- | --- |
| AI 클라이언트가 선택한 채팅을 읽게 하기 | **연동 기능 → MCP** | [MCP 설치, 범위 제한 토큰 생성, 연결](https://phishdestroy.github.io/TgWitness/ko/docs/reference/mcp/) |
| 저장된 미디어 내 텍스트 인식 | `media.saved` 기록 → **첨부 파일 인식** | [로컬 Docker 워커 설정](https://phishdestroy.github.io/TgWitness/ko/docs/reference/media-analysis/) |
| 이벤트를 n8n 또는 SIEM으로 전송 | **연동 → 발신 웹훅** | [수신자 추가, HMAC 확인, ID 중복 제거](https://phishdestroy.github.io/TgWitness/ko/docs/reference/webhooks/) |

**어떤 액세스 토큰을 어디에 입력해야 하나요?**

패널 액세스는 사람용입니다. MCP는 자체 읽기 전용 토큰을, 웹훅은 자체 HMAC 비밀 값을 씁니다. 어느 것도 텔레그램 세션이 필요 없습니다.

[패널 액세스 권한을 공유하거나](https://phishdestroy.github.io/TgWitness/ko/docs/access/) [MCP 클라이언트를 구성하세요](https://phishdestroy.github.io/TgWitness/ko/docs/reference/mcp/).

## 출처 및 결론 제시

보고서를 서명된 ZIP 옆에 두십시오. 보고서는 소스에 대한 귀하의 해석이고, 받는 사람이 검증하는 것은 ZIP입니다.

[내보내기 및 검증](https://phishdestroy.github.io/TgWitness/ko/docs/exports/) · [전체 조사 과정 진행](https://phishdestroy.github.io/TgWitness/ko/docs/cases/)
