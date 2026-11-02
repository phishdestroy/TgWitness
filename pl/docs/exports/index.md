# Eksportowanie i weryfikacja

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/exports/

Należy udostępnić odbiorcy pliki, które będzie mógł porównać z obszarem roboczym zbierania danych i jego zapisaną historią.

Zachować odniesienieEksportuj podpisany plik ZIPOdbiorca weryfikuje

Nie znają Państwo jeszcze podpisów i punktów kontrolnych? [Proszę zmienić przykładowy wpis](https://phishdestroy.github.io/TgWitness/pl/docs/concepts/#chain) i sprawdzić, które kontrole to wykryją.

Chcą Państwo przechowywać kopię poza serwerem dostawcy? Proszę przejść do [sekcji konfiguracji S3](https://phishdestroy.github.io/TgWitness/pl/docs/exports/#s3), funkcji [Object Lock](https://phishdestroy.github.io/TgWitness/pl/docs/exports/#s3-retention) lub opcji [zweryfikowanego odzyskiwania danych](https://phishdestroy.github.io/TgWitness/pl/docs/exports/#s3-restore).

## Zachowaj wiarygodne źródło informacji

Proszę zapisać odcisk klucza publicznego obszaru roboczego poza kolektorem. Podczas gromadzenia danych należy przechowywać podpisane punkty kontrolne w innym miejscu lub skorzystać z usług [niezależnego świadka](https://phishdestroy.github.io/TgWitness/pl/docs/witness/). Odniesienia te umożliwiają odbiorcy weryfikację klucza oraz granicy poprzedniego dziennika.

## Pobierz podpisany plik ZIP

Otwórz **opcję „Exports”** i utwórz podpisany plik ZIP z dowodami. Zawiera on pełny dziennik obszaru roboczego oraz podpisany manifest plików. Skorzystaj z [narzędzia](https://phishdestroy.github.io/TgWitness/pl/docs/reports/) [„Report Studio”](https://phishdestroy.github.io/TgWitness/pl/docs/reports/), aby stworzyć czytelny raport, lub z opcji [„Handover Extract”](https://phishdestroy.github.io/TgWitness/pl/docs/handover/), aby dostarczyć wyłącznie wybrane, zredukowane dane.

Raporty w formatach HTML, PDF i JSON posiadają własne podpisane pieczęcie i można je weryfikować oddzielnie. Plik CSV stanowi wygodną kopię do analizy; w celu sprawdzenia jego integralności należy użyć dokładnie tego samego pliku CSV, który znajduje się w zweryfikowanym pliku ZIP. Należy zachować podpisany plik ZIP, jeśli odbiorca potrzebuje również oryginalnych zapisów i załączników.

## Proszę zweryfikować to za pomocą zaufanej kopii TgWitness

W zainstalowanym środowisku projektowym proszę zastąpić przykładowy odcisk palca oraz ścieżki do plików:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Gdy oba odniesienia zostaną zatwierdzone, w raporcie wynikowym pojawią się wartości `key_pinned: true` i `checkpoint_checked: true`. Wynik weryfikacji należy zachować wraz z oryginalnym archiwum. Zachowany punkt kontrolny musi znajdować się na granicy eksportu lub przed nią.

## Wykorzystaj wynik weryfikacji

- **Należy sprawdzić dostarczone pliki:** manifest wiąże ich skróty, a podpisy rekordów wiążą zapisany dziennik. Wykrywane są zmienione pliki lub przerwane łańcuchy rekordów.
- **Sprawdź tożsamość obszaru roboczego:** niezależnie przechowywany odcisk palca identyfikuje klucz podpisujący, którego oczekiwałeś.
- **Porównaj wcześniejszy punkt graniczny:** zachowany punkt kontrolny weryfikuje eksport w oparciu o prefiks dziennika zapisany przed przekazaniem.
- **Należy sprawdzić zakres zebranych danych:** luki, wyniki pozyskania oraz kontrolowany test „wyślij → edytuj → usuń” opisują zdarzenia zarejestrowane w tej konfiguracji.

Wyniki te należy zachować wraz z kopią przeznaczoną dla odbiorcy. Należy sprawdzić, [co ustala weryfikacja](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#verification-scope) w zakresie kontroli oraz oddzielnej oceny twierdzeń źródłowych i zakresu gromadzenia danych.

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

1. Utwórz zasób w swoim serwisie, a następnie wprowadź jego lokalizację docelową i dane uwierzytelniające. Podczas przygotowywania pozostaw **opcję „Zachowaj kopię poza lokalizacją”** niezaznaczoną, a następnie wybierz opcję **„Zapisz kopię poza lokalizacją**”.
2. Proszę wybrać opcję **„Test połączenia**”. Spowoduje to przesłanie zaszyfrowanego obiektu testowego i sprawdzenie odpowiedzi serwera.
3. Proszę wybrać opcję **„Pobierz klucz szyfrujący**”. Proszę przechowywać ten plik oddzielnie od programu zbierającego dane; będzie on niezbędny do odzyskania danych.
4. Zaznacz pole wyboru **„Zachowaj kopię poza serwerem**” i zapisz ponownie. Wybierz opcję **„Kopiuj teraz”**, aby przeprowadzić operację ręcznie, lub pozostaw harmonogram w działaniu.

## Sprawdź stan przechowywania danych i postęp kopiowania

W sekcji **„More options”** (**Więcej opcji**) wybierz liczbę dni przechowywania oraz opcję „`GOVERNANCE`” (Zarządzanie) lub „`COMPLIANCE`” (Zgodność), jeśli Twój zasób danych obsługuje funkcję Object Lock. TgWitness odczytuje tryb przechowywania i termin wygaśnięcia przesłanego obiektu. Sprawdź oddzielny wynik przechowywania: potwierdzone, brak przechowywania lub niepowodzenie sprawdzania.

Panel wyświetla informacje o ostatnim przebiegu, liczbie obiektów, liczbie przesłanych bajtów, granicy skopiowanego dziennika oraz ewentualnych błędach. Brakujące lub zmienione nośniki lokalne są zgłaszane, a próba ich skopiowania jest powtarzana podczas następnego przebiegu. Pliki, punkty kontrolne oraz eksporty oczekujące w kolejce po tych nośnikach mogą nadal zostać skopiowane.

Przesyłanie danych odbywa się za pośrednictwem trasy Direct, SOCKS5 lub HTTP w obszarze roboczym. Należy wybrać jedną z tych tras do kopiowania do S3; trasa wykorzystująca wyłącznie MTProxy powoduje, że kopiowanie pozostaje w stanie oczekującym z komunikatem o błędzie.

## Klucz odtwarzający należy przechowywać oddzielnie

Pobrany plik JSON zawiera klucz deszyfrujący, ustawienia miejsca docelowego, prefiks obiektu obszaru roboczego oraz odcisk palca klucza podpisu. Odzyskiwanie wymaga zarówno tego pliku klucza, jak i oddzielnych poświadczeń dostępu do pamięci masowej z uprawnieniami do odczytu w zasobniku. Należy uwzględnić je w planie odzyskiwania danych.

W przypadku zmiany punktu końcowego, zasobnika lub prefiksu folderu należy ponownie pobrać plik klucza, aby ustawienia miejsca docelowego były zgodne. Aplikacja uruchamia nową kopię lokalnie przechowywanego dziennika, plików i punktów kontrolnych w nowym miejscu docelowym. Gotowe eksporty czatów, które zostały już usunięte z lokalnej kolejki przesyłania, pozostają w poprzednim miejscu docelowym.

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

Porównaj odzyskane materiały z niezależnie zachowanymi punktami kontrolnymi lub zapisami świadków, a następnie przejrzyj zakres zgromadzonych danych dla wybranego okresu.
