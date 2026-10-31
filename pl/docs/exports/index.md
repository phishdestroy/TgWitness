# Eksportowanie i weryfikacja

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/exports/

Udostępnij podpisany zapis, który może zweryfikować inna osoba.

Zachować odniesienieEksportuj podpisany plik ZIPOdbiorca weryfikuje

Nie znają Państwo jeszcze podpisów i punktów kontrolnych? [Proszę zmienić przykładowy wpis](https://phishdestroy.github.io/TgWitness/pl/docs/concepts/#chain) i sprawdzić, które kontrole to wykryją.

Chcą Państwo przechowywać kopię poza serwerem dostawcy? Proszę przejść do [sekcji konfiguracji S3](https://phishdestroy.github.io/TgWitness/pl/docs/exports/#s3), funkcji [Object Lock](https://phishdestroy.github.io/TgWitness/pl/docs/exports/#s3-retention) lub opcji [zweryfikowanego odzyskiwania danych](https://phishdestroy.github.io/TgWitness/pl/docs/exports/#s3-restore).

## Zachowaj wiarygodne źródło informacji

Proszę zapisać odcisk klucza publicznego obszaru roboczego poza kolektorem. Podczas gromadzenia danych należy przechowywać podpisane punkty kontrolne w innym miejscu lub skorzystać z usług [niezależnego świadka](https://phishdestroy.github.io/TgWitness/pl/docs/witness/). Odniesienia te umożliwiają odbiorcy weryfikację klucza oraz granicy poprzedniego dziennika.

## Pobierz podpisany plik ZIP

Proszę otworzyć **opcję „Eksportuj”** i utworzyć podpisany plik ZIP z dowodami. Zawiera on dziennik obszaru roboczego oraz podpisany manifest plików. Filtry panelowe nie ograniczają eksportu pełnego dziennika: proszę przejrzeć materiał przed jego udostępnieniem.

Pliki HTML i CSV do pobrania w postaci samodzielnych plików są przydatne do przeglądania i analizy. Proszę zachować podpisany plik ZIP jako weryfikowalny oryginał; oddzielny plik HTML lub CSV nie posiada samodzielnego podpisu.

## Proszę zweryfikować to za pomocą zaufanej kopii TgWitness

W zainstalowanym środowisku projektowym proszę zastąpić przykładowy odcisk palca oraz ścieżki do plików:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Gdy oba odniesienia zostaną zatwierdzone, w raporcie wynikowym pojawią się wartości `key_pinned: true` i `checkpoint_checked: true`. Wynik weryfikacji należy zachować wraz z oryginalnym archiwum. Zachowany punkt kontrolny musi znajdować się na granicy eksportu lub przed nią.

## Zrozumienie wyniku

- **Integralność:** zarejestrowana historia oraz wyeksportowane pliki są zgodne z ich podpisami.
- **Wcześniejsza uwaga:** zewnętrzny punkt kontrolny umożliwia porównanie wyeksportowanych danych z wcześniej zachowanym prefiksem dziennika.
- **Realizacja:** kontrolowany test wysyłania → edycji → usuwania pozwala zweryfikować konkretne zdarzenia w oparciu o zarejestrowane dane.

Ważny podpis nie stanowi dowodu na to, że każde zdarzenie w Telegramie miało miejsce, że źródło podało prawdziwe informacje ani że zegar osoby gromadzącej dane był prawidłowo ustawiony.

## Skonfiguruj kopię zapasową w usłudze S3 poza siedzibą firmy

W uruchomionym środowisku roboczym proszę otworzyć **opcję Eksporty → Kopia zewnętrzna**. Ta opcjonalna funkcja współpracuje z usługą AWS S3 oraz innymi usługami zgodnymi ze standardem S3. Kopiuje ona segmenty dziennika, zachowane zdjęcia i pliki, punkty kontrolne wraz z odpowiedziami zawierającymi sygnatury czasowe oraz gotowe eksporty czatów. Każdy obiekt jest szyfrowany na kolektorze za pomocą algorytmu `AES-256-GCM` przed przesłaniem.

Wersja demonstracyjna online przedstawia te same elementy sterujące, jednak z wyłączoną funkcją przesyłania danych. Dane uwierzytelniające do pamięci masowej należy wprowadzać wyłącznie we własnym, uruchomionym środowisku roboczym.

[![Pełny panel ustawień kopii poza lokalizacją: punkt końcowy, region, zasób, klucze dostępu, harmonogram, blokada obiektów oraz opcje związane z kluczem odtwarzania](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Pełny panel z rozwijanymi opcjami zaawansowanymi. Nie są wyświetlane żadne dane uwierzytelniające dotyczące pamięci masowej.

| Dziedzina | Co należy wpisać |
| --- | --- |
| Punkt końcowy | Adres URL usługi przechowywania danych, bez ścieżki do zasobnika ani danych uwierzytelniających. Fikcyjny przykład: `https://s3.example.invalid`. |
| Region | Region wymagany przez Państwa dostawcę. Domyślnym ustawieniem aplikacji jest `us-east-1`. |
| Bucket | Istniejący zasób, do którego mają Państwo dostęp. Fikcyjny przykład: `example-case-backup`. |
| Folder w zasobniku | Prefiks obiektu; domyślnie `tgwitness`. Aplikacja dodaje prefiks wygenerowany na podstawie odcisku palca klucza podpisu tego obszaru roboczego. |
| Identyfikator klucza dostępu / Tajny klucz dostępu | Proszę wprowadzić obie pary danych uwierzytelniających do pamięci masowej jednocześnie. Zostaną one zapisane w skarbcu obszaru roboczego. Aby zachować zapisaną parę, proszę pozostawić oba pola puste podczas kolejnych zapisów. |
| Adresy w formacie ścieżki | W zależności od dostawcy należy używać kodu `endpoint/bucket`, gdy funkcja jest włączona, lub `bucket.endpoint`, gdy jest wyłączona. |
| Interwał kopiowania | Od 1 do 1 440 minut; domyślnie 5 minut. Aby kopie były tworzone zgodnie z harmonogramem, aplikacja musi być uruchomiona. |
| Przechowywanie danych w Object Lock | Okres przechowywania i tryb dla zasobnika obsługującego funkcję Object Lock. Ustawienie „zero dni” powoduje, że obowiązuje domyślny okres przechowywania zasobnika. |

1. Wprowadź miejsce docelowe oraz dane uwierzytelniające. Podczas przygotowywania pozostaw **opcję „Zachowaj kopię poza lokalizacją”** niezaznaczoną, a następnie wybierz opcję **„Zapisz kopię poza lokalizacją**”.
2. Proszę wybrać opcję **„Test połączenia**”. Spowoduje to przesłanie zaszyfrowanego obiektu testowego i sprawdzenie odpowiedzi serwera.
3. Proszę wybrać opcję **„Pobierz klucz szyfrujący**”. Proszę przechowywać ten plik oddzielnie od programu zbierającego dane; będzie on niezbędny do odzyskania danych.
4. Zaznacz pole wyboru **„Zachowaj kopię poza serwerem**” i zapisz ponownie. Wybierz opcję **„Kopiuj teraz”**, aby przeprowadzić operację ręcznie, lub pozostaw harmonogram w działaniu.

**Nie** tworzy kontenera pamięci masowej. Zaplanowane przesyłanie danych zostaje wstrzymane wraz z zakończeniem działania aplikacji.

## Sprawdź stan przechowywania danych i postęp kopiowania

W sekcji **„Więcej opcji**” proszę wybrać liczbę dni przechowywania oraz opcję „`GOVERNANCE`” lub „`COMPLIANCE`”, jeśli Państwa zasób danych obsługuje funkcję Object Lock. TgWitness odczytuje tryb przechowywania oraz termin ważności przesłanego obiektu. Status informuje o potwierdzeniu, braku przechowywania lub niepowodzeniu weryfikacji; samo pomyślne przesłanie nie stanowi potwierdzenia przechowywania.

Panel wyświetla informacje o ostatnim przebiegu, liczbie obiektów, liczbie przesłanych bajtów, granicy skopiowanego dziennika oraz ewentualnych błędach. Brakujące lub zmienione nośniki lokalne są zgłaszane, a próba ich skopiowania jest powtarzana podczas następnego przebiegu. Pliki, punkty kontrolne oraz eksporty oczekujące w kolejce po tych nośnikach mogą nadal zostać skopiowane.

Przesyłanie danych odbywa się za pośrednictwem protokołów Direct, SOCKS5 lub HTTP w ramach obszaru roboczego. Kopiowanie do S3 nie jest dostępne za pośrednictwem MTProxy; aplikacja nie przechodzi w tryb połączenia bezpośredniego.

**Nie powoduje** to, że dostawca jest zobowiązany do egzekwowania funkcji Object Lock wyłącznie z powodu zaakceptowania przesłanego pliku.

## Klucz odtwarzający należy przechowywać oddzielnie

Pobrany plik JSON zawiera klucz deszyfrujący, ustawienia miejsca docelowego, prefiks obiektu obszaru roboczego oraz odcisk palca klucza podpisu. Nie zawiera on danych uwierzytelniających dostępu do S3: przywrócenie danych wymaga oddzielnych danych uwierzytelniających z uprawnieniami do odczytu w zasobniku.

W przypadku zmiany punktu końcowego, zasobnika lub prefiksu folderu należy ponownie pobrać plik klucza, aby ustawienia miejsca docelowego były zgodne. Aplikacja uruchamia nową kopię lokalnie przechowywanego dziennika, plików i punktów kontrolnych w nowym miejscu docelowym. Gotowe eksporty czatów, które zostały już usunięte z lokalnej kolejki przesyłania, pozostają w poprzednim miejscu docelowym.

**Nie** odszyfrowuje kopii bez wyeksportowanego klucza. Dane uwierzytelniające dostępu do pamięci masowej nie mogą zastąpić tego klucza.

## Przywrócenie i weryfikacja na innym komputerze

Należy skorzystać z zaufanej instalacji TgWitness, pobranego pliku JSON z kluczem, danych uwierzytelniających do pamięci masowej z uprawnieniami do odczytu oraz pustego katalogu wyjściowego. Proszę zastąpić poniższe fikcyjne symbole zastępcze danymi uwierzytelniającymi.

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

Pobrane i odszyfrowane obiekty pozostają w prywatnej pamięci tymczasowej na czas sprawdzania całego dziennika, zachowanych punktów kontrolnych oraz hashowych i rozmiarów zachowanych plików multimedialnych. Niebezpieczne ścieżki, sprzeczne segmenty dziennika oraz dziennik krótszy niż jego punkt kontrolny są odrzucane. W przypadku nieudanej weryfikacji przywrócone pliki nie są publikowane.

Pomyślne odzyskanie danych generuje wyniki `events.jsonl`, `media/`, `checkpoints/` oraz `exports/` dla materiałów dostępnych w kopii. Proszę zachować wynik polecenia w formacie JSON wraz z odzyskanymi materiałami.

**Nie odtwarza** obserwacji, które nigdy nie trafiły do dziennika, ani nie zastępuje niezależnie zachowanych punktów kontrolnych lub świadków.
