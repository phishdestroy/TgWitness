# Eksportowanie i weryfikacja

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/exports/

Przekaż pliki, które odbiorca sam porówna z Twoją przestrzenią.

Zachować odniesienieEksportuj podpisany plik ZIPOdbiorca weryfikuje

Podpisy i punkty kontrolne to nowość? [Zmień przykładowy wpis](https://phishdestroy.github.io/TgWitness/pl/docs/concepts/#chain) i zobacz, które kontrole to wychwycą.

Chcą Państwo przechowywać kopię poza serwerem dostawcy? Proszę przejść do [sekcji konfiguracji S3](https://phishdestroy.github.io/TgWitness/pl/docs/exports/#s3), funkcji [Object Lock](https://phishdestroy.github.io/TgWitness/pl/docs/exports/#s3-retention) lub opcji [zweryfikowanego odzyskiwania danych](https://phishdestroy.github.io/TgWitness/pl/docs/exports/#s3-restore).

## Zachowaj wiarygodne źródło informacji

Zapisz odcisk klucza przestrzeni gdzieś poza kolektorem. Podczas zbierania przechowuj też podpisane punkty kontrolne w innym miejscu albo uruchom [niezależnego świadka](https://phishdestroy.github.io/TgWitness/pl/docs/witness/). Właśnie z tym odbiorca porównuje klucz i wcześniejszy stan dziennika.

## Pobierz podpisany plik ZIP

**Eksporty** → podpisany ZIP z dowodami. Zawiera cały dziennik i podpisany manifest plików. Czytelny raport ułóż w [Report studio](https://phishdestroy.github.io/TgWitness/pl/docs/reports/), a jeśli trzeba oddać tylko wybrane dane — zrób [wyciąg do przekazania](https://phishdestroy.github.io/TgWitness/pl/docs/handover/).

Raporty HTML, PDF i JSON mają własne pieczęcie. CSV to tylko kopia robocza; do sprawdzania integralności bierz CSV ze zweryfikowanego ZIP.

## Proszę zweryfikować to za pomocą zaufanej kopii TgWitness

W środowisku projektu, z własnym odciskiem i ścieżkami:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Po pomyślnym sprawdzeniu zobaczysz `key_pinned: true` i `checkpoint_checked: true`. Zachowaj ten wynik obok archiwum. Punkt kontrolny musi być na końcu eksportu lub przed nim.

## Wykorzystaj wynik weryfikacji

- **Pliki:** manifest wiąże ich skróty, podpisy wiążą dziennik. Każda zmiana wyjdzie na jaw.
- **Tożsamość:** zachowany odcisk potwierdza, że to oczekiwany klucz.
- **Wcześniejszy stan:** punkt kontrolny porównuje eksport z początkiem dziennika zapisanym przed przekazaniem.
- **Pokrycie:** luki, wyniki pozyskania i test „wyślij → edytuj → usuń” pokazują, co ta konfiguracja naprawdę złapała.

Szczegóły: [co weryfikacja dowodzi, a czego nie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#verification-scope).

## Skonfiguruj kopię zapasową w usłudze S3 poza siedzibą firmy

**Eksporty → Kopia zewnętrzna** w Twojej przestrzeni. Działa z AWS S3 i każdym magazynem zgodnym z S3. Kopiuje segmenty dziennika, zapisane pliki, punkty kontrolne ze znacznikami czasu i gotowe eksporty czatów, każdy szyfrowany `AES-256-GCM` jeszcze na kolektorze.

Demo online pokazuje te ustawienia z wyłączonym wysyłaniem. Prawdziwe dane logowania wpisuj tylko we własnej instalacji.

[![Pełny panel ustawień kopii poza lokalizacją: punkt końcowy, region, zasób, klucze dostępu, harmonogram, blokada obiektów oraz opcje związane z kluczem odtwarzania](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Pełny panel z rozwijanymi opcjami zaawansowanymi. Nie są wyświetlane żadne dane uwierzytelniające dotyczące pamięci masowej.

| Dziedzina | Co należy wpisać |
| --- | --- |
| Punkt końcowy | URL magazynu, bez ścieżki bucketu i danych logowania. Przykład: `https://s3.example.invalid`. |
| Region | To, czego wymaga dostawca. Domyślnie `us-east-1`. |
| Bucket | Istniejący bucket z prawem zapisu. Przykład: `example-case-backup`. |
| Folder w zasobniku | Prefiks, domyślnie `tgwitness`. Dochodzi do niego prefiks przestrzeni. |
| Identyfikator klucza dostępu / Tajny klucz dostępu | Oba razem, przechowywane w sejfie. Później zostaw oba puste, żeby je zachować. |
| Adresy w formacie ścieżki | Wł.: `endpoint/bucket`. Wył.: `bucket.endpoint`. Zależy od dostawcy. |
| Interwał kopiowania | Od 1 do 1440 minut, domyślnie 5. Tylko gdy aplikacja działa. |
| Przechowywanie danych w Object Lock | Dni i tryb, jeśli bucket obsługuje Object Lock. Zero zostawia ustawienie domyślne bucketu. |

1. Utwórz bucket, wypełnij adres i dane logowania przy odznaczonym **Zachowuj kopię zewnętrzną** i kliknij **Zapisz kopię zewnętrzną**.
2. **Testuj połączenie** wysyła zaszyfrowany obiekt testowy.
3. **Pobierz klucz szyfrowania** i trzymaj go z dala od kolektora. Bez klucza nie ma odzyskiwania.
4. Zaznacz **Zachowuj kopię zewnętrzną**, zapisz, potem **Kopiuj teraz** albo zostaw harmonogram.

## Sprawdź stan przechowywania danych i postęp kopiowania

W **Więcej opcji** wybierz dni przechowywania oraz `GOVERNANCE` lub `COMPLIANCE`. TgWitness odczytuje przechowywanie z wysłanego obiektu i podaje: potwierdzone, brak albo błąd sprawdzenia.

Panel pokazuje ostatnie przejście, liczbę obiektów, bajty, skopiowaną granicę dziennika i błędy. Brakujący plik lokalny trafia do raportu i jest ponawiany przy następnym przejściu, reszta kopiuje się dalej.

Wysyłanie idzie bezpośrednio, przez SOCKS5 albo HTTP. Przy trasie tylko przez MTProxy kopia czeka z błędem.

## Klucz odtwarzający należy przechowywać oddzielnie

JSON klucza zawiera klucz deszyfrujący, adres, prefiks i odcisk klucza. Do odzyskania potrzebny jest on oraz dane logowania magazynu z prawem odczytu.

Zmieniony endpoint, bucket albo prefiks? Pobierz klucz ponownie. W nowym miejscu ruszy świeża kopia, stare eksporty czatów zostaną tam, gdzie były.

## Przywrócenie i weryfikacja na innym komputerze

Potrzebna jest zaufana instalacja TgWitness, JSON klucza, dane logowania tylko do odczytu i pusty folder:

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

Najpierw wszystko jest sprawdzane w prywatnym folderze tymczasowym: cały dziennik, punkty kontrolne, skróty i rozmiary plików. Niebezpieczne ścieżki, sprzeczne segmenty lub dziennik krótszy niż punkt kontrolny kończą się błędem i wtedy nic nie zostaje zapisane.

Po sukcesie dostajesz `events.jsonl`, `media/`, `checkpoints/` i `exports/`. Zachowaj obok wynik JSON polecenia i porównaj z punktami kontrolnymi lub wpisami świadka, które przechowujesz sam.
