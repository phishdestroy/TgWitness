# Wiadomości ulegają zmianom． Zachowaj to， co widział Pan／Pani．

Canonical page: https://phishdestroy.github.io/TgWitness/pl/

[Oprogramowanie typu open source ／ v0.9.1](https://phishdestroy.github.io/TgWitness/pl/docs/reference/changelog/)

Zapisuj czaty Telegrama z każdą edycją i usunięciem， a potem przekaż zapis， który każdy może sprawdzić．

[Otwórz wersję demonstracyjną](https://phishdestroy.github.io/TgWitness/demo/?lang=pl)[Instrukcja konfiguracji](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pl)

Fikcyjne dane， bez logowania do Telegrama．

 [Zbieranie przez GitHub Actions （wersja wstępna）](https://phishdestroy.github.io/TgWitness/pl/docs/capture/) [Kopia zapasowa poza lokalizacją w usłudze S3： konfiguracja i odzyskiwanie](https://phishdestroy.github.io/TgWitness/pl/#s3)

WIADOMOŚĆ PRZEZ CZAS ＃0042

Northstar · BadaniaFikcyjne źródło ／ wiadomość nr 42

1. **Zaobserwowana wiadomość：**09：41：02

   Prezentacja rozpoczyna się od 14：00．
2. **Zachowano edycję**09：43：18

   Prezentacja rozpoczyna się od 15：00．

   Zachowano poprzednią wersję
3. **Powiadomienie o usunięciu**10：06：45

   Zarejestrowane treści pozostają w Państwa dzienniku．

Trzy obserwacje． Jedna historia． PRZYKŁAD

Wiadomość znika． Zachowana historia pozostaje．

## Każda zarejestrowana zmiana． Dokładnie tam， gdzie jest potrzebna．

Prawdziwy interfejs， ale z wymyślonymi danymi．

TgWitness ／ Zapisane rozmowyPANIE I PANI PRZESTRZEŃ ROBOCZA DO OBSERWACJI

![Zapisane rozmowy z Telegrama w ciemnym motywie， wraz z zarejestrowanymi zmianami i usuniętymi wiadomościami zachowanymi w kontekście](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ Zapisane czaty Wygląda jak zwykły czat， a edycje i usunięcia są tuż obok wiadomości．

TgWitness ／ DziennikLOKALNE ŚRODOWISKO PRACY

![Rejestr zawierający zaobserwowane wiadomości， zmiany， powiadomienia o usunięciu oraz zdarzenia objęte monitorowaniem](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ Dziennik Wszystko， co widziało konto， z wyszukiwaniem i zaznaczonymi lukami．

TgWitness ／ Historia zmianLOKALNE ŚRODOWISKO PRACY

![Okienko szczegółów porównujące przechwyconą poprzednią wersję wiadomości z jej edytowaną wersją](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ Historia edycji Stara i nowa wersja obok siebie， nic nie jest nadpisywane．

TgWitness ／ Podpisane eksportyLOKALNE ŚRODOWISKO PRACY

![Funkcja eksportu obszaru roboczego umożliwiająca uzyskanie podpisanego pliku ZIP， JSONL， CSV oraz raportu HTML w trybie offline](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ Podpisane eksporty Dziennik można zabrać ze sobą ， podpisany i z własnym weryfikatorem．

Śledź zapisany rekord za pomocą [Case Board](https://phishdestroy.github.io/TgWitness/pl/docs/case-board/)， [projektu raportu](https://phishdestroy.github.io/TgWitness/pl/docs/reports/) i [kopii](https://phishdestroy.github.io/TgWitness/pl/docs/handover/) [udostępnionej](https://phishdestroy.github.io/TgWitness/pl/docs/handover/)． [Przeglądaj grupy kont](https://phishdestroy.github.io/TgWitness/pl/docs/groups/) łącznie．

01 ／ PRZECHWYTYWANIE

### To Państwo wybierają zakres．

Kilka czatów， folder albo całe konto． Każde konto ma własną przestrzeń．

[Porównaj tryby gromadzenia danych](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html#scope)

02 ／ ZACHOWANIE

### Zmiany wzbogacają treść．

Wersje， usunięcia i luki zostają w dzienniku．

[Zobacz matrycę zdarzeń](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html#events)

03 ／ PRZEKAZANIE

### Rejestr， który podróżuje．

Podpisany ZIP， pliki i raport offline． Hasło opcjonalne．

[Eksportuj i zweryfikuj](https://phishdestroy.github.io/TgWitness/pl/docs/exports/)

## Zmień jeden bajt．
System weryfikacji to wykryje．

Każde zdarzenie zawiera odnośnik do poprzedniego skrótu oraz podpis Ed25519．

![Zarejestrowane zdarzenia zawierają odnośniki do poprzednich skrótów， są opatrzone podpisami i przekazywane w formie weryfikowalnego pliku eksportowego．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Zmiana zarejestrowanego wpisu powoduje zmianę jego skrótu i uniemożliwia weryfikację powiązanego wpisu．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Oddzielnie przechowywany punkt kontrolny umożliwia odbiorcy porównanie wyeksportowanego dziennika z wcześniejszymi obserwacjami．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Należy przestrzegać procedur weryfikacji， od skrótu pliku po oddzielnie zachowany punkt kontrolny．

[Zapoznaj się z ośmioma poziomami dowodów](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html#levels)

## Proszę o dodatkową weryfikację．

Wiadomości， pliki i raport offline w jednej podpisanej paczce．

[Zapoznaj się z modelem dowodowym](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)

tgwitness-evidence.zipPAKIET Z PODPISEM

- 01

  Oryginalne spostrzeżeniaPliki JSONL ＋ tabela CSV
- 02

  Przejrzysty kontekstRaport HTML w trybie offline ＋ zachowane pliki multimedialne
- 03

  Niezależna weryfikacjaPodpisany manifest ＋ samodzielny weryfikator

Odbiorca sprawdza wszystko Twoim kluczem， a punkt kontrolny przechowywany gdzie indziej pokazuje， że od tamtej pory nic nie przepisano． [Jak działają kontrole．](https://phishdestroy.github.io/TgWitness/pl/docs/concepts/#layers)

## Kopie w usłudze S3． Kontrole zewnętrzne．

Należy przechowywać zaszyfrowane kopie i wprowadzać niezależne mechanizmy weryfikacyjne．

Domyślnie wyłączone

### Skopiuj wszystko do pamięci masowej zgodnej ze standardem S3

Dziennik， pliki， punkty kontrolne i eksporty czatów są szyfrowane， zanim trafią do S3．

**Ustawienia przechowywania danych i odzyskiwanie**

Szyfrowanie po stronie klienta

`AES-256-GCM` na Twojej maszynie． Dostawca widzi tylko szyfrogram．

Kopie tworzone automatycznie lub ręcznie

Kopiowanie od razu albo co 1－1440 minut， postęp widać w panelu．

Object Lock

Wybierz liczbę dni i tryb przechowywania ， panel sprawdzi， czy naprawdę zadziałały．

Zweryfikowane odzyskiwanie danych

Klucz trzymaj osobno． Przywrócić można gdziekolwiek， pliki pojawiają się dopiero po weryfikacji．

![Pełny panel ustawień kopii poza lokalizacją： punkt końcowy， region， zasób， klucze dostępu， harmonogram， blokada obiektów oraz opcje związane z kluczem odtwarzania](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Pełny panel z rozwijanymi opcjami zaawansowanymi． Nie są wyświetlane żadne dane uwierzytelniające dotyczące pamięci masowej．

Dziennik i media`AES-256-GCM`Pamięć masowa zgodna ze standardem S3

[Skonfiguruj S3 i przywróć kopię](https://phishdestroy.github.io/TgWitness/pl/docs/exports/#s3)[Zapoznaj się ze szczegółami weryfikacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Klucz odzyskiwania** Trzymaj go osobno： bez niego kopii nie da się odczytać．

### Powiadomienia · Apprise

Problemy， zmiany w czatach i dzienne podsumowanie do komunikatorów， na e－mail albo do Twojego webhooka．

**Wybierz， co udostępniać** Bez treści wiadomości， dopóki sam jej nie włączysz．

 [Konfiguracja miejsc docelowych powiadomień](https://phishdestroy.github.io/TgWitness/pl/docs/reference/operations/#notifications)

### Zewnętrzne znaczniki czasu

Skróty punktów kontrolnych z sygnaturą czasową zgodne z RFC 3161 i OpenTimestamps．

**Śledź wynik** Sprawdź odpowiedź TSA albo zaktualizuj potwierdzenie OpenTimestamps do dowodu w Bitcoinie．

 [Proszę sprawdzić dowody z sygnaturami czasowymi：](https://phishdestroy.github.io/TgWitness/pl/docs/reference/timestamp/)

### Niezależny świadek

Oddzielny serwer przechowuje podpisane obserwacje i może publikować punkty kontrolne `TGW1`．

**Oddziel punkt odniesienia** Uruchom go na innym hoście， z własnym kluczem i dziennikiem．

 [Skonfiguruj Witness](https://phishdestroy.github.io/TgWitness/pl/docs/witness/)

### Odtworzenie danych i widoczne luki

Wznowienie po ponownym uruchomieniu． Funkcje ponownej weryfikacji oraz `coverage.json` pokazują odzyskane wiadomości i luki w danych．

**Przejrzyj przerwę** Odzyskane wiadomości i zapisane luki obok siebie．

 [Proszę sprawdzić ciągłość i ewentualne luki](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html#continuity)

## Państwa pierwsze środowisko pracy zaczyna się właśnie tutaj．

Najpierw wypróbuj demo， a gdy będziesz gotowy， podłącz zapasowe konto．
Windows， Linux， macOS lub Docker．

[Zapoznaj się z instrukcją konfiguracji](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pl)

**Jedna zaimportowana sesja， jeden uruchomiony klient．**

Nie używaj zaimportowanego TData ani sesji jednocześnie w Telegram Desktop i TgWitness： Telegram może unieważnić oba （AUTH_KEY_DUPLICATED）． Potrzebujesz obu？ Zaloguj się do TgWitness osobno， telefonem albo kodem QR．

[Proszę zapoznać się z ostrzeżeniem dotyczącym importowania sesji](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pl#session-warning)

**Proszę zapoznać się z nią przed nawiązaniem połączenia．**

Wypróbuj fikcyjne środowisko pracy bez konta w Telegramie．

[Otwórz wersję demonstracyjną online →](https://phishdestroy.github.io/TgWitness/demo/?lang=pl)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**Polecenia dotyczące instalacji lokalnej**

KROK 01

### Pobierz kod źródłowy．

[Proszę pobrać plik ZIP ze źródłami](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) i rozpakować go lub sklonować repozytorium：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Wymaga Pythona 3.11+． W Windows launcher sam zaproponuje instalację．

[Przeglądaj wersje](https://github.com/phishdestroy/TgWitness/releases)

KROK 02

### Wybierz sposób uruchomienia．

Proszę dwukrotnie kliknąć plik `Start.cmd` lub uruchomić go w PowerShell：

```
.\Start.cmd
```

Chce Pan／Pani tylko zapoznać się z serwisem？ Proszę dwukrotnie kliknąć `scripts\Demo.cmd`， aby uruchomić izolowaną wersję demonstracyjną． Nie jest wymagane logowanie do serwisu Telegram．

W przypadku dostępności języka Python 3.11+ oraz biblioteki `venv`：

```
sh start.sh
```

Aby zamiast tego otworzyć fikcyjny dziennik， proszę uruchomić polecenie `sh start.sh --demo`．

Przy uruchomionym Dockerze i zainstalowanym Compose w wersji 2.20 lub nowszej：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Drugie polecenie wyświetla token Państwa prywatnego panelu． Proszę zachować go na swoim komputerze．

Po uruchomieniu proszę otworzyć adres [127.0.0.1:8787](http://127.0.0.1:8787)．

Przy instalacji ze źródeł token jest w `data/live/panel-token.txt`． Własna para API z [my.telegram.org](https://my.telegram.org) jest opcjonalna． [Pełna instrukcja ↗](https://phishdestroy.github.io/TgWitness/pl/docs/reference/quickstart/)

**TgWitness 0.9.1** [Co nowego →](https://phishdestroy.github.io/TgWitness/pl/docs/reference/changelog/) · [Funkcje i znane ograniczenia →](https://phishdestroy.github.io/TgWitness/pl/docs/reference/features/)

## Jasne instrukcje． Przydatne wskazówki dotyczące dalszych działań．

[Zapoznaj się z przewodnikami ↗](https://phishdestroy.github.io/TgWitness/pl/docs/)

[### Tryby działania， scenariusze i poziomy wiarygodności dowodów Cztery tryby gromadzenia danych． Osiem poziomów weryfikacji． Znajdź schemat postępowania dostosowany do Państwa sprawy．](https://phishdestroy.github.io/TgWitness/pl/guides/modes.html)

[01 ### Podłącz konto Obsługa importu danych z telefonów， kodów QR oraz obsługiwanych sesji．](https://phishdestroy.github.io/TgWitness/pl/docs/accounts/)[02 ### Proszę wybrać serwer proxy Publiczne listy serwerów MTProxy lub Państwa własna trasa．](https://phishdestroy.github.io/TgWitness/pl/docs/proxies/)[03 ### Skonfiguruj bota Witness Podpisane punkty kontrolne na Państwa kanale w Telegramie．](https://phishdestroy.github.io/TgWitness/pl/docs/witness/)[04 ### Eksportowanie i weryfikacja Udostępnij zarchiwizowaną historię i sprawdź jej integralność．](https://phishdestroy.github.io/TgWitness/pl/docs/exports/)

## Przeglądaj archiwum．

Historia， AI ze źródłami， MCP， OCR i podpisane webhooki．

[Zapoznaj się z przebiegiem pracy](https://phishdestroy.github.io/TgWitness/pl/docs/archive/)

## Zanim zaczną Państwo．

**Czy ta strona jest powiązana z serwisem Telegram？**

Nie． To statyczna strona z fikcyjnymi przykładami． Aplikacja działa na Twojej maszynie i tam się logujesz．

**Czy narzędzie to pozwala odzyskać wiadomości usunięte przed ich przechwyceniem？**

Nie． Zapisuje to， co konto widziało， gdy program działał． Późniejszy zrzut nie odtworzy pominiętych edycji ani usuniętych wiadomości．

**Czy cały mój dziennik jest zaszyfrowany？**

Sesje i klucze tak． Wiadomości i pliki nie ， użyj szyfrowania dysku． Eksporty mogą mieć hasło AES－256．

**Czy serwis ten jest powiązany z Telegramem？**

Nie． To niezależny projekt na licencji MIT， oparty na Telethon． Logujesz się własnymi kontami．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Najpierw zapoznaj się z informacjami． Skonfiguruj narzędzie， gdy będzie Pan／Pani gotowy／gotowa．

[Otwórz wersję demonstracyjną](https://phishdestroy.github.io/TgWitness/demo/?lang=pl)[Instrukcja konfiguracji](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pl)
