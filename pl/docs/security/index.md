# Dbaj o bezpieczeństwo

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/security/

Zapoznaj się z trasami komunikacji w Telegramie, publicznymi listami serwerów proxy oraz opcjonalnymi usługami zewnętrznymi. Dowiedz się, co odblokowuje każda opcja, jaki zakres ochrony zapewniają poszczególne zabezpieczenia oraz jakie kwestie pozostawiają one do Państwa decyzji.

**127.0.0.1**domyślny adres panelu

**256-bitowy**losowy token panelu

**0**Sieci CDN, narzędzia analityczne lub czcionki zdalne

**Ed25519**podpis na każdym wpisie

## Miejsce, w którym wszystko się znajduje

Narzędzie do gromadzenia danych, jego panel oraz wszystkie zapisane rekordy pozostają na komputerze lub serwerze, na którym jest ono uruchomione. Telegram jest domyślnym miejscem docelowym; każda inna opcja wymaga osobnego przełączenia.

06 / CO WYCHODZI Z URZĄDZENIAInstalacja

PAN/PANI KOMPUTER LUB SERWER

**Panel**127.0.0.1:8787 · token bearer

**Collector**Jeden klient Telegramu na obszar roboczy

KATALOG DANYCH

**Rejestr**SQLite · łańcuchowanie skrótów · podpisane

**Media**pliki nazwane na podstawie skrótu SHA-256

**Vault**Fernet · sesja, para API, klucz podpisujący, serwer proxy

- **Telegram**Zawsze · zgodnie z Państwa wytycznymi

  Połączenie konta z protokołem MTProto: bezpośrednie, SOCKS5, HTTP lub MTProxy. Tryb ukrywania adresu IP oczekuje na działający serwer proxy. Przełączenie na połączenie bezpośrednie wymaga trybu, który wyraźnie na to zezwala.
- **Tekst poza witryną**Opcjonalne · domyślnie wyłączone

  Dziennik, pliki i punkty kontrolne są szyfrowane algorytmem AES-GCM przed przesłaniem do magazynu danych zgodnego ze standardem S3. Klucz pozostaje w Państwa posiadaniu; załączniki są nazywane na podstawie haszów opartych na kluczu, a nie na podstawie hasha ich zawartości.
- **Powiadomienia**Opcjonalne · domyślnie wyłączone

  Wykaz problemów i liczba zmian wraz z tytułami czatów. Fragmenty wiadomości są wysyłane wyłącznie po włączeniu tej funkcji.
- **Autorytet w zakresie znaczników czasu**Opcjonalne · domyślnie wyłączone

  Wyłącznie skrót SHA-256 podpisanego punktu kontrolnego oraz losowy nonce. Brak wiadomości, brak nazw użytkowników czatu.
- **Witness**Opcjonalne · domyślnie wyłączone

  Narzędzie pobiera podpisane punkty kontrolne i liczniki przechwyceń za pomocą tokenu tylko do odczytu. Nie ma możliwości odczytu treści rozmów ani zmiany ustawień.

Ustawienie domyślne: z tego urządzenia wychodzi wyłącznie połączenie z serwisem Telegram.

Opcjonalne lokalizacje docelowe konfiguruje się dla poszczególnych obszarów roboczych. Tekst wiadomości i pliki multimedialne są przechowywane w postaci niezaszyfrowanej w katalogu danych: należy je zabezpieczyć za pomocą szyfrowania dysku oraz uprawnień do plików.

## Co kryje się za każdą tajemnicą

| Tajne | Gdzie jest przechowywany | Jakie możliwości to stwarza | W przypadku wycieku |
| --- | --- | --- | --- |
| **Token panelu** | Plik `panel-token.txt` w katalogu danych; przeglądarka przechowuje go wyłącznie dla danej karty | Wszystkie funkcje w każdym obszarze roboczym: przeglądanie i eksportowanie, zmiana zakresu, logowanie się na konta | Zatrzymaj TgWitness, usuń `panel-token.txt`, uruchom ponownie: zostanie utworzony nowy token |
| **Sesja w Telegramie** | Vault, zaszyfrowany (`credentials.enc`) | Samo konto w serwisie Telegram | Zakończ sesję w aplikacji Telegram, wybierając opcję *Ustawienia → Urządzenia* |
| **Klucz podpisujący** | Vault, zaszyfrowany (`signing.enc`) | Zapisy opatrzone podpisem, których autentyczność można zweryfikować na podstawie Państwa podpisu cyfrowego | Punkty kontrolne przechowywane w innym miejscu, świadek oraz znaczniki czasu wskazują, co istniało wcześniej |
| **Klucz do skarbca** | `vault.key` obok danych lub zewnętrzny klucz główny dla nowego katalogu danych | Odszyfrowanie skarbca | Należy traktować klucz sesji i klucz podpisujący jako również ujawnione |
| **Token Witness** | Na serwerze Witness | Tryb tylko do odczytu: podpisane punkty kontrolne i stan działania | Proszę usunąć tę stronę z sekcji „Witness” i utworzyć nową |
| **Klucz treści poza witryną** | Vault; wystarczy pobrać go raz, aby móc odzyskać dane | Odszyfrowywanie kopii przechowywanej poza serwerem | Każdy, kto posiada przechowywane obiekty, może je odszyfrować: proszę traktować tę kopię jako ujawnioną |

## Zakres ochrony

### – omówiono

- Zmieniony, usunięty lub zmieniony w kolejności wpis w eksporcie: łańcuch skrótów lub podpis nie są już weryfikowalne.
- Dziennik, który został skrócony lub odtworzony po tym, jak punkt kontrolny został zapisany w innym miejscu: zachowany punkt kontrolny nie jest już zgodny.
- Odgadywanie tokenu panelu: 256 losowych bitów, porównywanych w stałym czasie; po 15 nieudanych próbach w ciągu minuty adres zostaje odrzucony.
- Treści o charakterze wrogim w czacie: tekst jest wstawiany jako zwykły tekst, nigdy jako kod HTML; załączniki są pobierane jako pliki; panel nie ładuje żadnych treści z innych stron.
- Skopiowany katalog danych z zewnętrznym kluczem do skarbca: sesje i klucze podpisujące pozostają zaszyfrowane bez klucza głównego.

### Pozostawiamy to Państwu

- Użytkownik posiadający token panelu głównego ma pełną kontrolę. Proszę przyznawać innym osobom ograniczony dostęp do kont, czatów i działań, których potrzebują; klucz główny należy zachować w tajemnicy.
- Administrator urządzenia może odczytać całą zawartość dziennika, a także go przeredagować i ponownie podpisać. Odciski palców i punkty kontrolne należy przechowywać na innym systemie.
- Treść wiadomości i pliki multimedialne nie są szyfrowane przez TgWitness. Należy stosować szyfrowanie dysku oraz rygorystyczne uprawnienia.
- Korzystanie z protokołu HTTP poza lokalnym hostem (localhost) powoduje ujawnienie tokenu w sieci. Prosimy o korzystanie z protokołu HTTPS lub tunelu SSH.
- Podpisy potwierdzają, że zarejestrowane dane nie zostały zmienione, a nie to, że każde zdarzenie w Telegramie zostało zarejestrowane.

[Udostępnianie dostępu do sprawy](https://phishdestroy.github.io/TgWitness/pl/docs/access/) z uwzględnieniem uprawnień, terminów ważności i limitów sesji. Token świadka pozostaje odrębnym poświadczeniem.

## Zabezpieczenie instalacji

Zrobiono 0 z 8

1. **Proszę korzystać z dedykowanego konta w Telegramie** — nigdy z konta głównego. Token panelu oraz sesja zapewniają pełną kontrolę nad nim.
2. **Proszę utrzymać panel pod adresem 127.0.0.1.** Dostęp zdalny powinien odbywać się wyłącznie za pośrednictwem protokołu HTTPS (wbudowana konfiguracja Caddy) lub tunelu SSH.
3. **Należy zaszyfrować dysk,** na którym znajduje się katalog danych: treści wiadomości i pliki multimedialne są przechowywane w postaci, w jakiej zostały otrzymane.
4. **Proszę ograniczyć dostęp do katalogu danych** wyłącznie do konta serwisowego. Nowe katalogi otrzymują uprawnienia 0700 w systemie Unix; w systemie Windows należy ustawić uprawnienia folderu.
5. **Klucz główny do skarbca należy przechowywać w innym miejscu** na serwerach: przed utworzeniem katalogu danych należy ustawić parametr `TGWITNESS_VAULT_KEY_FILE`.
6. **Proszę zapisać odcisk klucza podpisującego oraz punkty kontrolne** na innym systemie, a także dodać świadka na innym serwerze.
7. **Nigdy nie należy przesyłać** kluczy typu „`data/`”, kluczy sesji, kluczy typu „`panel-token.txt`” ani kluczy do skarbca na GitHub ani w czacie.
8. **Proszę nie rejestrować** nagłówków `Authorization` ani treści żądań na serwerze proxy odwrotnym.

**Czy mogę zmienić token panelu bez utraty danych?**

Tak. Token służy wyłącznie do otwarcia panelu. Proszę zatrzymać TgWitness, usunąć plik „`panel-token.txt`” z katalogu danych i uruchomić program ponownie; dziennik, sesje i klucze pozostaną nienaruszone. Po ustawieniu wartości „`TGWITNESS_TOKEN`” zamiast pliku wykorzystywana jest wartość środowiskowa.

**Dlaczego wiadomości nie są szyfrowane w stanie spoczynku?**

Osoba odpowiedzialna za gromadzenie danych musi je przeczytać, aby przeprowadzić wyszukiwanie, porównać wersje i wyeksportować dane. Szyfrowanie ich za pomocą klucza na tym samym urządzeniu nie zapewniłoby znaczącej ochrony przed osobą, która ma dostęp do tego urządzenia. Szyfrowanie dysku chroni dysk wyłączony lub skradziony; ścisłe uprawnienia chronią dysk, na którym toczy się praca.

## Zgłoś lukę w zabezpieczeniach

Prosimy skorzystać z opcji **„Security → Report a vulnerability”** w repozytorium GitHub. Należy podać wersję, skutki oraz minimalny syntetyczny przykład pozwalający na odtworzenie błędu. Prosimy nigdy nie przesyłać danych uwierzytelniających, katalogów kont ani archiwów zawierających rzeczywiste dowody. Jeśli zgłoszenie prywatne jest niedostępne, prosimy otworzyć zgłoszenie z prośbą o utworzenie prywatnego kanału, nie podając szczegółów dotyczących luki.
