# Przygotuj kopię do udostępnienia

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/handover/

Udostępniaj tylko to, co potrzebne — oryginał zostaje nietknięty.

Przekazanie to osobny podpisany wyciąg: wybierz czaty i osoby, ukryj tożsamości lub tekst, wybierz pliki i notatki zespołu. Manifest zapisuje, co zostawiono, skrócono i pominięto.

## Przygotuj fragment przeznaczony dla odbiorcy

1. **Eksporty → Wyciąg do przekazania**: wpisz cel, wybierz czaty i okres, a jeśli potrzebujesz konkretnych osób — **Wczytaj osoby z wybranych czatów**.
2. Wszyscy pozostali: pseudonimy, pominięci albo tak, jak zapisano. Tekst i pliki to osobne przełączniki; telefony i e-maile można zamaskować.
3. Case Board: nic, zakładki i wycinki albo karty z komentarzami. Nazwiska zespołu można zastąpić aliasami.
4. **Pobierz wyciąg do przekazania**, otwórz, zweryfikuj, przejrzyj przed wysłaniem.

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
| Osoby | Wybrane osoby pozostają z nazwiskiem, pozostałe dostają pseudonimy albo są pomijane. |
| Tekst | Cały tekst, tylko tekst wybranych osób i Twojego konta albo żaden. |
| Pliki | Pliki wybranych osób i Twojego konta, wszystkie pokazane pliki albo żadne. |
| Case Board | Nic, zakładki i wycinki albo karty z dyskusją. |

Przeczytaj też tekst i pliki: pseudonim nie usuwa nazwisk zapisanych w treści wiadomości czy załącznika. Jeśli brakuje wybranego pliku, przywróć go albo pomiń załączniki.

## Tekst powinien dać się niezależnie zweryfikować

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Oryginalne archiwum i punkty kontrolne zachowaj u siebie. Odbiorca może zweryfikować swoją kopię bez otrzymywania całej przestrzeni. Wygląd: [Report studio](https://phishdestroy.github.io/TgWitness/pl/docs/reports/). Zaufane odniesienia: [weryfikacja eksportu](https://phishdestroy.github.io/TgWitness/pl/docs/exports/).
