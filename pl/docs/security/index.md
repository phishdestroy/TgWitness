# Dbaj o bezpieczeństwo

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/security/

Co opuszcza Twoją maszynę, co otwiera każdy sekret i co chronią zabezpieczenia, a co zostaje po Twojej stronie.

**127.0.0.1**domyślny adres panelu

**256-bitowy**losowy token panelu

**0**Sieci CDN, narzędzia analityczne lub czcionki zdalne

**Ed25519**podpis na każdym wpisie

## Miejsce, w którym wszystko się znajduje

Kolektor, panel i wszystkie wpisy zostają na Twojej maszynie. Domyślnie łączy się tylko z Telegramem, wszystko inne to osobny przełącznik.

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
| **Token panelu** | `panel-token.txt` w katalogu danych; przeglądarka trzyma go dla karty | Wszystko we wszystkich przestrzeniach | Zatrzymaj TgWitness, usuń `panel-token.txt`, uruchom ponownie — dostaniesz nowy |
| **Sesja w Telegramie** | Vault, zaszyfrowany (`credentials.enc`) | Samo konto w serwisie Telegram | Zakończ sesję w aplikacji Telegram, wybierając opcję *Ustawienia → Urządzenia* |
| **Klucz podpisujący** | Vault, zaszyfrowany (`signing.enc`) | Podpisywanie wpisów Twoim odciskiem | Punkty kontrolne przechowywane gdzie indziej, świadek i znaczniki czasu nadal pokazują, co istniało wcześniej |
| **Klucz do skarbca** | `vault.key` obok danych albo zewnętrzny klucz główny | Sejf | Załóż, że sesja i klucz podpisu też wyciekły |
| **Token Witness** | Na serwerze Witness | Tylko odczyt: punkty kontrolne i stan | Usuń go na stronie świadka i utwórz nowy |
| **Klucz treści poza witryną** | Vault; wystarczy pobrać go raz, aby móc odzyskać dane | Kopię zewnętrzną | Kto ma też bucket, może ją odszyfrować — traktuj kopię jako ujawnioną |

## Zakres ochrony

### – omówiono

- Zmieniony, usunięty lub przestawiony wpis: pęka łańcuch skrótów albo podpis.
- Dziennik przycięty lub odbudowany po tym, jak zapisałeś punkt kontrolny gdzie indziej: punkt przestaje się zgadzać.
- Zgadywanie tokenu: 256 losowych bitów, porównanie w stałym czasie; 15 błędów na minutę i adres zostaje zablokowany.
- Wroga treść czatów: tekst zostaje tekstem, nigdy HTML; załączniki pobierają się jako pliki; panel nie ładuje niczego z innych stron.
- Skradziony katalog danych przy zewnętrznym kluczu sejfu: sesje i klucze pozostają zaszyfrowane.

### Pozostawiamy to Państwu

- Główny token może wszystko. Innym dawaj ograniczony dostęp, a główny trzymaj dla siebie.
- Administrator maszyny może przeczytać wszystko i ponownie podpisać dziennik. Odcisk i punkty kontrolne trzymaj gdzie indziej.
- TgWitness nie szyfruje wiadomości i mediów. Szyfruj dysk i ogranicz uprawnienia.
- Zwykły HTTP poza localhost ujawnia token. Używaj HTTPS albo tunelu SSH.
- Podpisy nie powiedzą, co zostało pominięte. Sprawdzaj pokrycie i testuj dostarczanie na własnych kontach i źródłach.

[Udostępnij dostęp do sprawy](https://phishdestroy.github.io/TgWitness/pl/docs/access/) z uprawnieniami, terminem ważności i limitem sesji.

## Zabezpieczenie instalacji

Zrobiono 0 z 8

1. **Używaj osobnego konta Telegram**, nigdy głównego.
2. **Trzymaj panel na 127.0.0.1.** Zdalnie tylko przez HTTPS (dołączony Caddy) albo tunel SSH.
3. **Zaszyfruj dysk** z katalogiem danych — wiadomości i media są zapisywane tak, jak przyszły.
4. **Ogranicz katalog danych** do konta usługi (0700 w Unix, uprawnienia folderu w Windows).
5. **Trzymaj klucz sejfu osobno** na serwerach: ustaw `TGWITNESS_VAULT_KEY_FILE` przed pierwszym uruchomieniem.
6. **Zapisuj odcisk i punkty kontrolne** w innym systemie, uruchom świadka na innym hoście.
7. **Nigdy nie należy przesyłać** kluczy typu „`data/`”, kluczy sesji, kluczy typu „`panel-token.txt`” ani kluczy do skarbca na GitHub ani w czacie.
8. **Proszę nie rejestrować** nagłówków `Authorization` ani treści żądań na serwerze proxy odwrotnym.

**Czy mogę zmienić token panelu bez utraty danych?**

Tak, on tylko otwiera panel. Zatrzymaj TgWitness, usuń `panel-token.txt`, uruchom ponownie. Dziennik, sesje i klucze zostają. Jeśli ustawiono `TGWITNESS_TOKEN`, ta wartość ma pierwszeństwo przed plikiem.

**Dlaczego wiadomości nie są szyfrowane w stanie spoczynku?**

Kolektor musi je czytać, żeby wyszukiwać, porównywać i eksportować. Klucz na tej samej maszynie nie zatrzyma kogoś, kto i tak może czytać tę maszynę. Szyfrowanie dysku chroni skradziony dysk, uprawnienia — działający.

## Zgłoś lukę w zabezpieczeniach

**Security → Report a vulnerability** na GitHubie. Wersja, skutki i minimalny przykład na fikcyjnych danych. Nigdy nie wysyłaj danych logowania, folderów kont ani prawdziwych dowodów. Jeśli prywatne zgłoszenia są wyłączone, otwórz issue z prośbą o prywatny kanał, bez szczegółów exploita.
