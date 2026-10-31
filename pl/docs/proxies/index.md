# Proszę wybrać serwer proxy

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/proxies/

Należy utrzymać połączenie z kontem. Należy wyraźnie określić, w jakich przypadkach trasa połączenia może korzystać z adresu serwera.

## Proszę najpierw wybrać tryb IP

01**Ukryj adres IP**

Proszę skorzystać z serwera proxy. Jeśli żaden z nich nie działa, proszę poczekać bez bezpośredniego połączenia z Telegramem.

02**Zezwól na rozwiązanie awaryjne**

Po upływie skonfigurowanego opóźnienia zezwól na bezpośrednie połączenie; w przypadku uzyskania odpowiedzi należy powrócić do działającego serwera proxy.

03**Tunel / VPN**

Zezwól na bezpośrednie połączenia przez sieć dostawcy usług. Ta opcja nie powoduje instalacji ani weryfikacji sieci VPN.

Trasa wybiera połączenie. Tryb IP określa, czy dozwolone jest połączenie bezpośrednie.

## Niech grupa zadba o trasę

1. Otwórz **konto → Ustawienia → Ustawienia połączenia**.
2. Proszę wybrać tryb IP i opcję **„Automatic MTProxy**” lub wprowadzić stałą trasę.
3. Zapisz i uruchom **test połączenia z Telegramem**. Działa to również przed zalogowaniem się.
4. Po rozpoczęciu gromadzenia danych proszę sprawdzić, czy kontrolowana wiadomość trafiła do dziennika.

Nowe środowiska robocze wykorzystują automatyczny serwer MTProxy z funkcją ukrywania adresu IP. Pula łączy cztery publiczne źródła, sprawdza połączenia, zachowuje działające trasy i zastępuje serwery proxy, które przestały działać. W przypadku nieudanych pobrań zachowywane są poprzednie migawki.

## Proszę skorzystać z własnego serwera proxy

Proszę wprowadzić dane SOCKS5 lub HTTP CONNECT, wkleić obsługiwany link do serwera proxy Telegramu lub podać katalog operatora. Przed zmianą aktywnej trasy należy wstrzymać monitorowanie. Fałszywe klucze tajne TLS MTProxy zaczynające się od `ee` nadal nie są obsługiwane.

**Ustawienia rotacji, udostępniania i ponownych prób**

W sekcji **Parametry → Automatyczny MTProxy** należy ustawić progi awarii, czasy oczekiwania, planowaną rotację oraz liczbę kont na jeden serwer proxy. Limit współdzielenia wynoszący jeden powoduje, że konto oczekuje, gdy nie jest dostępny żaden wyłączny dostęp. Interwały odświeżania listy i sondowania są zgodne z wartościami głównego obszaru roboczego. Oddzielne serwery proxy nie gwarantują oddzielnych adresów IP wyjściowych.

## Oddzielenie serwisu Telegram od zewnętrznych zapytań

MTProxy obsługuje wyłącznie ruch z aplikacji Telegram. Sygnatury czasowe, powiadomienia, kopie oraz weryfikacja źródeł wykorzystują oddzielny serwer proxy SOCKS5/HTTP, trasę SOCKS5/HTTP danego konta lub połączenie bezpośrednie (Direct), o ile pozwala na to tryb IP. Te zewnętrzne żądania można wyłączyć.

Wyraźna konfiguracja `TGWITNESS_PROXY_FEED_PROXY` określa trasę działania programu pobierającego kanały. [Niezależny moduł „witness”](https://phishdestroy.github.io/TgWitness/pl/docs/witness/) zachowuje własne ustawienia. Te opcje nie powodują instalacji systemowej sieci VPN ani przekierowywania ruchu przeglądarki.

Zapoznaj się ze [wszystkimi trybami działania, ustawieniami domyślnymi i listami źródeł](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/#ip-modes) lub [wybierz osoby uprawnione do zmiany trasy konta](https://phishdestroy.github.io/TgWitness/pl/docs/access/).
