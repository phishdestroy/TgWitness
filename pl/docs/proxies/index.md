# Proszę wybrać serwer proxy

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/proxies/

Trzymaj konto online i sam zdecyduj, czy kiedykolwiek może pokazać IP Twojego serwera.

## Proszę najpierw wybrać tryb IP

01**Ukryj adres**

Tylko proxy. Jeśli żadne nie działa, czeka.

02**Direct jako ostateczność**

Po opóźnieniu łączy się bezpośrednio, a gdy proxy zadziała, wraca do niego.

03**Serwer za tunelem lub VPN**

Bezpośrednio można. Ten tryb nie konfiguruje ani nie sprawdza VPN.

Trasa wybiera połączenie. Tryb IP określa, czy dozwolone jest połączenie bezpośrednie.

## Niech grupa zadba o trasę

1. **Konto → Ustawienia → Ustawienia połączenia**.
2. Wybierz tryb IP i **Automatyczny MTProxy** albo stałą trasę.
3. Zapisz, potem **Testuj połączenie z Telegramem** (działa też przed zalogowaniem).
4. Uruchom zbieranie i wyślij sobie wiadomość testową.

Nowe przestrzenie startują na automatycznym MTProxy z trybem **Ukryj adres**. Pula korzysta z czterech publicznych list, sprawdza serwery, zostawia działające i wymienia martwe.

## Proszę skorzystać z własnego serwera proxy

SOCKS5, HTTP CONNECT, link do proxy Telegrama albo katalog operatora. Przed zmianą wstrzymaj obserwację. Sekrety Fake TLS (`ee`…) nie działają.

**Ustawienia rotacji, udostępniania i ponownych prób**

**Parametry → Automatyczny MTProxy**: progi błędów, przerwy, rotacja, kont na proxy. Limit 1 oznacza, że konto poczeka zamiast współdzielić. Różne proxy mogą mieć ten sam wyjściowy IP.

## Oddzielenie serwisu Telegram od zewnętrznych zapytań

MTProxy przenosi tylko Telegram. Znaczniki czasu, powiadomienia, kopie i sprawdzanie kodu idą przez osobne proxy SOCKS5/HTTP, trasę SOCKS5/HTTP konta albo bezpośrednio, jeśli tryb na to pozwala. Albo je wyłącz.

`TGWITNESS_PROXY_FEED_PROXY` ustawia trasę pobierania list. [Świadek](https://phishdestroy.github.io/TgWitness/pl/docs/witness/) ma własne ustawienia. Nic z tego nie dotyka przeglądarki ani sieci systemu.

Więcej: [tryby i wartości domyślne](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/#ip-modes), [kto może zmieniać trasy](https://phishdestroy.github.io/TgWitness/pl/docs/access/).
