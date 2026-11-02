# Przygotuj kopię do udostępnienia

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/handover/

Należy przekazać istotne spostrzeżenia, zachowując przy tym oryginalny układ obszaru roboczego.

Przekazanie to oddzielny, podpisany wyciąg. Należy wybrać czaty i osoby, ograniczyć tożsamości lub tekst oraz zdecydować, które pliki i notatki zespołu powinny znaleźć się w kopii odbiorcy. Manifest zawiera zapis wyboru oraz liczbę rekordów niezmienionych, zminimalizowanych i pominiętych.

## Przygotuj fragment przeznaczony dla odbiorcy

1. Otwórz **menu Eksportuj → Wyciąg do przekazania**. Opisz jego cel, wybierz czaty i opcjonalny okres w formacie UTC, a następnie zaznacz opcję **„Załaduj osoby z wybranych czatów”,** jeśli potrzebujesz nazwisk osób, których dotyczą dane.
2. Wybierz sposób postępowania z pozostałymi osobami: użyj pseudonimów, pomiń ich wiadomości lub wyświetl je zgodnie z zapisem. Tekst wiadomości i załączniki można ustawić niezależnie; opcjonalnie można zamaskować numery telefonów i adresy e-mail.
3. Należy zdecydować, czy uwzględnić zakładki i fragmenty z Case Board, czy też karty z komentarzami. W niniejszym tekście nazwy zespołów mogą zostać zastąpione pseudonimami śledczych.
4. Wybierz opcję **„Pobierz wyciąg z przekazania**”. Otwórz wygenerowany raport i wybrane zapisy lokalnie, zweryfikuj archiwum i sprawdź kopię przed wysłaniem.

### Jeden egzemplarz oryginalny, jedna kopia przeznaczona do udostępniania

Przykład syntetyczny · służy wyłącznie do zilustrowania treści

1. **Wybierz.** Dołącz czat dotyczący sprawy i określ, kogo dotyczy dany fragment.
2. **Zminimalizuj.** Wybierz, w jaki sposób inny uczestnik pojawi się w kopii udostępnianej.
3. **Sprawdź.** Przed wysłaniem otwórz wygenerowany raport i zapisy z archiwum.
4. **Udostępnij.** Przekaż sprawdzoną kopię i oddzielnie przekaż jej wiarygodny odcisk cyfrowy.

#### Pierwotna obserwacja

Nora · użytkownik 71002

„Otrzymałem poprawiony link.”

Dziennik źródłowy przechowuje tę zapisaną obserwację.

#### Kopia dla odbiorcy

Wyświetl zgodnie z zapisem: Nora · użytkownik 71002 · „Otrzymałam poprawiony link”.

Pseudonim: P01 · „Otrzymałem poprawiony link”.

Pominąć: wiadomość tego uczestnika nie została uwzględniona w tekście.

#### Zapoznaj się z rzeczywistymi plikami

Zapoznaj się z plikami report.html i records.jsonl.

Należy sprawdzić tożsamości, tekst, załączniki oraz opcjonalne komentarze zespołu.

#### Podpisany fragment

Wybór + skróty plików + podpisany manifest

Oddzielny pakiet powiązany z granicą źródłowego dziennika

## Należy stosować te elementy razem

| Kontrola | Wpływ na tekst |
| --- | --- |
| Osoby | Wybrane osoby powinny pozostać rozpoznawalne; pozostałych uczestników należy pseudonimizować lub pominąć zgodnie z wytycznymi. |
| Tekst | Należy uwzględnić cały tekst, tylko tekst wybranych osób i konta obserwującego lub pominąć treść wiadomości i pola szczegółowe zawierające tekst. |
| Pliki | Wybierz pliki wybranych osób i konta obserwowanego, wszystkie pliki wyświetlonych wiadomości lub żadne pliki. |
| Case Board | Nie należy wybierać materiałów z tablicy, zakładek i fragmentów ani kart z dyskusjami zespołu. |

Należy sprawdzić tekst swobodny i zawartość plików, a także tożsamości: pseudonim nie powoduje automatycznego usunięcia wszystkich nazwisk występujących w wiadomości lub załączniku. Jeśli wybrany plik podlegający archiwizacji jest niedostępny, należy go przywrócić lub wyraźnie pominąć załączniki przed wygenerowaniem wyciągu.

## Tekst powinien dać się niezależnie zweryfikować

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Oryginalne, podpisane archiwum dowodów oraz punkty kontrolne należy przechowywać oddzielnie. Proces przekazania rejestruje własną projekcję, dzięki czemu odbiorca może sprawdzić dostarczoną kopię bez konieczności otrzymywania całego obszaru roboczego. [Studio raportów](https://phishdestroy.github.io/TgWitness/pl/docs/reports/) zapewnia własny układ graficzny; [weryfikacja eksportu](https://phishdestroy.github.io/TgWitness/pl/docs/exports/) wyjaśnia zaufane odniesienia.
