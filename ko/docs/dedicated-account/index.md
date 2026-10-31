# 별도의 계정을 사용하십시오. 절대 주 계정을 사용하지 마십시오.

Canonical page: https://phishdestroy.github.io/TgWitness/ko/docs/dedicated-account/

계정을 연결하기 전에 반드시 읽어보세요

주 계정을 사용하지 말라는 저희의 조언은 농담이 아닙니다. 이는 현실입니다.

주 계정

- 사용자 앱 해시: 99% 로그아웃됨
- 신뢰도가 낮다는 이유만으로 차단되는 경우가 빈번합니다
- 이것을 사용하는 것은 정말 어리석은 생각입니다

공개 키 쌍에 대한 추가 계정

- 이 두 가지를 통해 100만 개 이상의 계정이 등록되었습니다.
- 이 쌍은 5년 이상 운영되어 왔습니다.
- 누구도 이를 통해 귀하의 정보를 볼 수 없습니다

01

## 왜 메인 계정을 사용하지 않는가

이 정보는 정확합니다. 우리는 이러한 문제들의 함정이 정확히 어디에 있는지 정확히 알고 있습니다.

1. ### 사용자 앱 해시: 99% 로그아웃됨

   접근 권한이 없는 계정으로 my.telegram.org에 로그인하여 앱 해시를 얻은 후, 해당 앱 해시를 통해 요청을 보내면 해당 계정이 로그아웃될 확률이 99%입니다. 직접 확인해 보실 수 있습니다.
2. ### 신뢰도가 낮다는 이유만으로 차단되는 경우가 빈번합니다

   계정이 차단되는 이유는 단순히 텔레그램이 해당 계정을 신뢰하지 않기 때문이며, 이러한 차단은 빈번하게 발생합니다. 이 점도 직접 확인해 볼 수 있습니다. 자신의 계정을 사용하는 것은 정말 어리석은 생각입니다.
3. ### 복사된 세션 키는 취소될 수 있습니다.

   Telegram Desktop과 TgWitness에서 가져온 TData/세션 키를 동시에 실행하면 `AUTH_KEY_DUPLICATED` 오류가 발생할 수 있습니다. Telegram은 해당 인증을 무효화하므로, 두 복사본 모두 새로 로그인해야 합니다. 전용 계정을 사용하더라도 이를 방지할 수는 없습니다.

   원래 클라이언트를 완전히 종료하고, 가져온 세션을 사용하는 동안에는 클라이언트를 닫아 두십시오. 병행 사용을 위해서는 전화번호나 QR 코드를 통해 TgWitness에 로그인하여 별도의 인증을 생성하십시오. 별도로 인증된 다른 클라이언트는 로그인 상태를 유지할 수 있습니다.

   [세션 가져오기 경고 사항 읽기](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ko#session-warning)

텔레그램 문서

- [로그아웃 오류: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [자체 앱 해시 생성: api_id 획득](https://core.telegram.org/api/obtaining_api_id)

02

## TgWitness가 공개 앱 해시/앱 ID 쌍을 통해 작동하는 이유

이것이 바로 우리가 TgWitness를 공개 앱 해시/앱 ID 쌍을 기반으로 구축한 이유입니다. 우리의 논리에 따르면, 이를 사용하면 차단될 가능성이 더 낮습니다. 100만 개 이상의 텔레그램 계정이 이러한 쌍을 통해 등록되었으며, 다양한 프로그램이 이를 통해 작동하고 있습니다. 저희의 논리에 따르면, 이는 개인 앱 해시를 직접 사용하는 것보다 더 낫습니다. 이 쌍들은 확실히 5년 이상 유지되어 왔기 때문입니다.

### 자신만의 새로운 쌍

my.telegram.org에서 해당 계정을 통해 생성됨.

- 계정의 약 99%가 로그아웃됨
- 애플리케이션 하나당 계정 하나

### 풀의 공개 키 쌍

많은 프로그램에서 사용하는 것과 동일한 쌍입니다.

- 100만 개 이상의 계정이 등록되었습니다
- 다양한 프로그램들
- 5년 이상 근무

### 이 쌍을 통해 아무도 귀하의 정보를 볼 수 없는 이유

- #### 이 쌍은 이름이지 키가 아닙니다

  Telegram은 프로그램이 연결되거나 로그인 코드를 요청할 때 API ID와 API 해시를 요구합니다. 이는 애플리케이션을 식별할 뿐, 어떤 계정에 대한 접근 권한도 부여하지 않습니다. Telethon의 문서에 따르면, 한 쌍의 ID와 해시는 어떤 전화번호와도 호환된다고 명시되어 있습니다.
- #### 세션 키는 절대 서버를 벗어나지 않습니다.

  로그인 시 TgWitness와 텔레그램 간의 디피-헬만(Diffie–Hellman) 교환을 통해 인증 키가 생성되며, 키 자체는 절대 전송되지 않습니다. 텔레그램 문서에 따르면, 인증 후 키는 사용자와 연결되며, 이 키를 사용하는 모든 호출은 해당 사용자로 실행됩니다. 동일한 키 쌍을 사용하는 다른 프로그램들은 각자 고유한 키를 가지고 있으므로 사용자의 키를 사용할 수 없습니다.
- #### 트래픽은 사용자의 키로 암호화됩니다

  모든 요청과 응답은 API 해시가 아닌 세션의 인증 키로 암호화됩니다. API 해시를 안다고 해서 아무것도 복호화할 수 없습니다.
- #### 한 쌍의 소유자는 아무것도 볼 수 없습니다

  텔레그램에는 API ID별로 계정, 세션 또는 메시지를 나열하는 기능이 없습니다. 쌍의 소유자는 my.telegram.org에서 해당 앱 설정만 볼 수 있습니다.
- #### 어떤 앱인지 확인할 수 있는 것은 오직 귀하의 계정뿐입니다

  본인의 계정 설정 → 기기에서 각 세션의 앱 이름과 API ID, 기기, IP 주소 및 날짜가 나열됩니다. 이 목록은 다른 누구에게도 제공되지 않습니다.

텔레그램 문서

- [사용자 인증: 키가 사용자 역할을 합니다](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [인증 키 생성](https://core.telegram.org/mtproto/auth_key)
- [MTProto 암호화](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [세션 기록에 포함되는 내용](https://core.telegram.org/constructor/authorization)
- [api_id 획득](https://core.telegram.org/api/obtaining_api_id)
- [텔레그램 앱의 오픈 소스 코드](https://telegram.org/apps#source-code)

라이브러리 및 토론

- [텔레톤: 로그인](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: 공식 앱 API](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: api_hash는 비밀로 유지해야 할까요?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### 다른 프로그램에서 동일한 쌍7

다음과 같은 공식 텔레그램 앱 쌍은 공개되어 있으며, 많은 독립적인 프로그램과 라이브러리에 내장되어 있습니다:

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  계정 등록을 위해 게시된 공식 앱 쌍 목록 포럼

03

## 추가 계정 생성 방법

텔레그램 계정을 생성하려면 로그인 코드를 수신할 전화번호가 필요합니다. 계정의 유효 기간에 따라 전화번호를 선택하십시오.

- 최선의 선택

  ### 선불 SIM 또는 eSIM

  ********

  마지막

  잔액을 충분히 유지하기만 한다면

  주의 사항

  가장 신뢰할 수 있는 방법: 텔레그램은 실제 휴대폰 번호를 가장 잘 인식합니다. 통신사가 회수한 번호는 다른 사람에게 할당됩니다.
- ### 가상 번호 앱

  ********

  마지막

  앱은 숫자를 유지하지만

  주의 사항

  텔레그램은 가상 번호 사용을 거부하거나, 인증 코드를 전송하지 않거나, 신규 계정 사용을 즉시 제한할 수 있습니다. 일부 앱은 사용되지 않는 번호를 회수하기도 합니다.
- ### 번호 대여

  ********

  마지막

  대여 기간

  주의 사항

  이 번호가 소진되면 다음 고객에게 배정됩니다.
- ### 일회성 활성화

  ********

  마지막

  하나의 코드

  주의 사항

  번호는 즉시 풀로 반환되며, 대개 이전 소유자의 이력이 함께 제공됩니다. 무엇보다 먼저 클라우드 비밀번호를 설정하십시오.

나중에 해당 번호를 보유한 사람은 누구나 로그인 코드를 요청할 수 있습니다. 클라우드 비밀번호(2단계 인증)가 없으면 로그인할 수 없으며, 이 비밀번호가 없으면 계정은 해당 번호의 다음 소유자에게 귀속됩니다.

텔레그램 문서

- [스팸 FAQ: 가상 번호 및 이전 소유자](https://telegram.org/faq_spam)
- [2단계 인증](https://core.telegram.org/api/srp)

### 임대된 +888 번호 (Fragment)

일부 마켓플레이스 및 서비스에서는 Fragment를 통해 텔레그램의 공식 +888 번호를 일시적으로 대여해 줍니다.

대략적인 가격: 하루당 20달러.

- 텔레그램 웹(Telegram Web) 또는 텔레그램 데스크톱(Telegram Desktop)에서 직접 계정을 등록할 수 있습니다.
- 해당 번호로 된 계정을 삭제하고 새 계정을 생성할 수 있습니다.
- 이러한 계정은 일반적으로 사기 방지 심사를 덜 받지만, 면책 특권이나 특별한 혜택을 제공하는 것은 아닙니다.

이 번호는 귀하의 것이 아닙니다. 대여 기간이 종료되면 소유자가 이를 되찾을 수 있습니다. 즉시 클라우드 비밀번호를 설정하고, 이 계정을 장기적으로 사용할 수 있는 것으로 간주하지 마십시오.

+888 번호를 직접 소유하거나 본인이 관리하는 선불 SIM 카드를 사용하는 것이 여전히 더 안정적입니다.

### 마켓플레이스에서 판매되는 기성 계정

일부 마켓플레이스(예: G2G 또는 Z2U)에서는 신규, 사용 기간이 지난 계정 또는 세션 파일이 포함된 텔레그램 계정을 판매합니다.

- [G2G: 텔레그램 계정 목록](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: 텔레그램 계정 목록](https://www.z2u.com/telegram/accounts-5-15140)

절대 본 계정을 사용하지 마십시오! 이 방법으로 만든 전용 계정은 주 텔레그램 계정을 TgWitness에 등록하는 것보다 훨씬 안전합니다.

#### 구매 전 주의사항

- 이는 텔레그램의 서비스 약관을 위반하는 행위입니다.
- 많은 계정이 대량 등록(자동 등록)되었거나 이력이 불분명합니다.
- 일부 판매자는 여전히 복구 권한을 보유하고 있을 수 있습니다.
- 이러한 마켓에서 생성된 계정은 나중에 차단되거나 제한되는 경우가 빈번합니다.
- 스틸러, 피싱 도구 또는 명백히 도난당한 계정을 공개적으로 판매하는 마켓플레이스는 피하십시오.
- 피싱 도구, 정보 탈취 프로그램, 도난당한 세션 또는 계정을 공개적으로 판매하는 플랫폼에서 계정(자동 등록으로 광고되는 계정 포함)을 구매하는 행위는 텔레그램의 이용 약관뿐만 아니라 대부분의 국가 법률을 위반하는 것입니다. 이는 나중에 증거의 효력을 상실시킬 수 있습니다. 신중하게 선택하십시오.

#### 이 옵션을 사용하는 경우

1. 이 계정은 일회용으로 취급하십시오.
2. 다른 모든 세션을 종료하고, 클라우드 비밀번호를 설정하며, 복구 방법을 즉시 변경하십시오.
3. 서로 다른 제공업체의 계정이나 본인이 직접 등록한 계정 중 2~3개를 사용하십시오.

**프리미엄, 삭제 및 7일 유예 기간**

계정에 프리미엄(Premium)이 활성화되어 있는 경우, 해당 전화번호에 접근할 수 있는 사람이라도 계정을 즉시 삭제할 수는 없습니다. 사용자에게 알림이 전송되며, 계정이 삭제되기 전까지 7일의 유예 기간이 주어집니다.

이 점은 매우 중요합니다. 귀하의 조사는 해당 계정에 달려 있으므로, 대체 계정을 준비할 시간이 있습니다.

**신규 계정 및 API 인증 정보**

SMS 서비스에서 받은 번호를 사용하여 직접 등록한 새 계정에서 api_id/api_hash를 획득하여 사용하는 경우, 첫 번째 API 요청이나 세션 인증 시 계정이 로그아웃됩니다. 조사를 계획할 때 이 점을 유의하십시오.

04

## 계정 생성

숫자에서 첫 번째 기록된 채팅까지.

1. ### 번호를 확인하세요

   계정을 장기간 유지해야 할 경우에는 선불 SIM 또는 eSIM을, 단기 작업의 경우에는 대여형 또는 일회성 활성화 방식을 사용하십시오. 관련 서비스는 아래에 나열되어 있습니다.
2. ### 주 계정과 별도로 등록하십시오

   주 계정과 나란히 등록하지 말고, 별도의 기기, 에뮬레이터 또는 휴대폰 프로필에서 공식 텔레그램 앱에 등록하십시오.
3. ### 클라우드 비밀번호로 잠그세요

   즉시 다른 곳에서는 사용하지 않는 클라우드 비밀번호와 복구 이메일을 설정하십시오.
4. ### 개인정보 설정을 닫습니다

   전화번호: **‘아무도 없음**’, ‘내 번호로 찾기’, **‘내 연락처**’, ‘마지막 접속 시간’, ‘프로필 사진’ 및 ‘자기소개’: **‘아무도 없음’** 또는 **‘내 연락처**’로 표시하고, 연락처 동기화를 해제하십시오.
5. ### 자동 삭제되지 않도록 하십시오

   계정 자동 삭제 기간을 최장 기간으로 설정하여, TgWitness가 중지되더라도 계정을 잃지 않도록 하십시오.
6. ### 중립적인 프로필을 부여하십시오

   다른 계정의 이름, 사진, 사용자 이름, 소개글 및 개인 연락처는 포함하지 마십시오.
7. ### 잠시 예열 시간을 두세요

   처음에는 하루에 몇 개의 채팅방만 참여하세요. 서두르는 신규 계정은 우선적으로 제한을 받게 됩니다.
8. ### 봇과는 어떠한 정보도 공유하지 마십시오

   봇의 경우 절대 “전화번호 공유”나 “위치 공유”를 누르지 마십시오. 해당 기기에서 VPN이나 프록시를 통해 링크와 미니 앱을 열어주세요.
9. ### TgWitness에 연결하세요

   자신의 작업 공간에서 **‘계정 → QR 코드’**를 통해 연결한 다음, **‘소스 → 조사 모드’를** 누르십시오. 앱은 사용자가 작업을 수행하는 곳이며, TgWitness는 기록입니다.

텔레그램 문서

- [2단계 인증](https://core.telegram.org/api/srp)
- [개인정보 설정](https://core.telegram.org/api/privacy)
- [계정 자동 삭제](https://core.telegram.org/method/account.setAccountTTL)

05

## 서비스 번호

시작 시 고려해야 할 사항. 국가, 가격, 텔레그램에서 번호 변경을 허용하는지 여부는 자주 변경되므로 결제 전에 확인하십시오.

### 선불 SIM 및 eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - 선불

  PayGo 요금제, 매우 저렴함
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - 선불
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - 선불
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - 선불
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### 가상 번호 앱 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  미국 전용; 등록 시 미국 전화번호가 필요합니다.
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  번호는 사용하지 않으면 회수됩니다.
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - 기타 국가
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - 유료

  체험 기간 동안
- [Hushedhushed.com](https://hushed.com)

  - 많은 국가에서
  - 유료

  저렴한
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  앱 내의 유럽 휴대폰 번호
- [Sonetelsonetel.com](https://sonetel.com)

  - 많은 국가에서
  - 무료 번호
- [Zadarmazadarma.com](https://zadarma.com)

  - 많은 국가에서

  가상 번호

### 대여 및 활성화 횟수 12

임대 서비스는 몇 주 또는 몇 달 동안 번호를 유지합니다. 일회성 활성화 시 단일 코드가 제공되므로, 등록 직후 클라우드 비밀번호를 설정하십시오.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - 임대
  - 활성화
- [SMSPVAsmspva.com](https://smspva.com)

  - 임대
  - 활성화
- [5SIM5sim.net](https://5sim.net)

  - 임대
  - 활성화
- [SMSPoolsmspool.net](https://www.smspool.net)

  - 임대
  - 일회성
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - 임대
  - 활성화
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - 임대
  - 활성화
- [JuicySMSjuicysms.com](https://juicysms.com)

  - 임대
  - 활성화
- [365SMS365sms.org](https://365sms.org)

  - 임대
  - 활성화
- [SIMSMSsimsms.org](https://simsms.org)

  - 임대
  - 활성화
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - 일회성
- [SMS-MANsms-man.com](https://sms-man.com)

  - 일회성
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - 일회성
