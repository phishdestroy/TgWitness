# Telegram · 프록시 선택

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/proxies/

계정을 온라인 상태로 유지하고, 서버의 IP를 보여 줘도 되는지는 직접 결정합니다.

## 먼저 IP 모드를 선택하세요

01**주소 숨기기**

프록시만 사용. 작동하는 것이 없으면 기다립니다.

02**최후의 수단으로서 직접 전송**

일정 시간 후 직접 연결하고, 작동하는 프록시가 생기면 다시 프록시로 돌아갑니다.

03**터널 또는 VPN 뒤에 위치한 서버**

직접 연결도 괜찮습니다. VPN을 대신 설정하거나 확인하지는 않습니다.

경로에 따라 연결 방식이 결정됩니다. IP 모드는 직접 연결이 허용되는지 여부를 결정합니다.

## 풀이 경로를 유지하도록 하십시오

1. **계정 → 설정 → 연결 설정**.
2. IP 모드와 **자동 MTProxy** 또는 고정 경로를 고릅니다.
3. 저장하고 **Telegram 연결 테스트**(로그인 전에도 작동).
4. 수집을 시작하고 자신에게 테스트 메시지를 보냅니다.

새 작업 공간은 자동 MTProxy와 **주소 숨기기**로 시작합니다. 풀은 네 개의 공개 목록을 가져와 서버를 확인하고, 좋은 것은 남기고 죽은 것은 교체합니다.

## 자신의 프록시를 사용하세요

SOCKS5, HTTP CONNECT, 텔레그램 프록시 링크 또는 운영자 카탈로그. 전환하기 전에 관찰을 일시 중지하십시오. Fake TLS 비밀 값(`ee`…)은 작동하지 않습니다.

**회전, 공유 및 재시도 설정**

**매개변수 → 자동 MTProxy**: 실패 임계값, 대기 시간, 순환, 프록시당 계정 수. 한도 1은 계정이 공유하지 않고 기다린다는 뜻입니다. 서로 다른 프록시도 출구 IP는 같을 수 있습니다.

## 텔레그램과 외부 요청을 분리

MTProxy는 텔레그램만 전달합니다. 타임스탬프, 알림, 사본, 코드 검사는 별도의 SOCKS5/HTTP 프록시, 계정의 SOCKS5/HTTP 경로, 또는 모드가 허용하면 직접 연결로 나갑니다. 아예 끌 수도 있습니다.

`TGWITNESS_PROXY_FEED_PROXY`는 목록 다운로드 경로를 정합니다. [증인](https://phishdestroy.github.io/TgWitness/ko/docs/witness/)은 자체 설정이 있습니다. 이 중 어느 것도 브라우저나 시스템 네트워크를 건드리지 않습니다.

더 보기: [모드와 기본값](https://phishdestroy.github.io/TgWitness/ko/docs/reference/connection/#ip-modes), [경로를 바꿀 수 있는 사람](https://phishdestroy.github.io/TgWitness/ko/docs/access/).
