# Opracuj raport

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reports/

Prowadź czytelnika od pytania sprawy prosto do zapisanych wpisów.

Report studio łączy wybrane dane, historie zmian, wykresy i Twoje wnioski. Osiem projektów, HTML i natywny PDF. Każdy raport HTML, PDF i JSON jest pieczętowany Twoim kluczem.

## Sporządź raport w trzech krokach

1. **Eksporty → Konfiguruj i podgląd → Dane**: cała przestrzeń albo wybrane czaty, autorzy, daty (UTC, kiedy TgWitness zobaczył wpis) i typy wpisów.
2. **Projekt i zawartość**: wybierz projekt i co wejdzie do raportu — wykresy, uczestnicy, transkrypcja, zmiany, elementy Case Board, dane sprawy i notatki.
3. **Podgląd**: sprawdź liczby, aktywność, próbki i zakresy brakujących ID. Zapisz i pobierz potrzebny format.

### Uporządkuj te same zapisane materiały tak, aby były przystępne dla czytelnika

Przykład syntetyczny · schematyczny układ, a nie wygenerowany raport

1. **Wybierz.** Wybierz dwie rozmowy oraz okres obserwacji dla danej sprawy.
2. **Opracuj tekst.** Wybierz układ i sekcje, które odpowiadają na zadane pytanie.
3. **Podgląd.** Sprawdź liczbę zaznaczonych elementów oraz zapisany tekst „przed” i „po”.
4. **Zweryfikuj.** Wygeneruj plik końcowy i sprawdź jego podpis w oparciu o zaufany odcisk palca obszaru roboczego.

#### Wybrane uwagi

2 czaty · 1 dzień obserwacji

Wiadomości, edycje i powiadomienia o usunięciu

#### Struktura raportu

##### Zmieniono miejsce docelowe płatności

Pytanie dotyczące sprawy → zakres → ustalenia → odniesienia do zapisów

**Kontekst wiadomości**

Uwaga nr 142: „Skorzystaj z nowego linku do płatności”.

**Zapisane zmiany**

Przed: old.example.invalid → Po: new.example.invalid

#### Sprawdź wybór

18 uwag · 2 zapisane zmiany

Czas wysłania, edycji i przeglądu ma oddzielne oznaczenia.

#### Ostateczny wynik pracy

Podpisany plik PDF + podpisany plik JSON lub podpisany plik ZIP zawierający czytelny raport

Odbiorca sprawdza plik i zaufany odcisk cyfrowy.

## Wybierz styl czytania

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin**: te same wpisy, inny wygląd. Przy zmianie zostają wybór i notatki. Dowolny z 25 języków.

PDF-y powstają z dołączonymi czcionkami, bez przeglądarki. Chiński, japoński i koreański wymagają czcionki takiej jak Noto Sans CJK na serwerze (w systemie lub w `TGWITNESS_FONT_DIR`), inaczej dostaniesz tylko HTML i JSON.

## Zapoznaj się ze zmianą w jej kontekście

Edycje pokazują „przed” i „po”, usunięcia — ostatnią zapisaną wersję. Odpowiedzi, przekazania, reakcje, przyciski i załączniki zachowują swoje odwołania.

Podgląd projektu używa pierwszych 50 000 wpisów, podgląd danych liczy wszystko dokładnie. Ostateczny układ stron pokaże dopiero wygenerowany PDF.

## Starannie dobierz wersję przeznaczoną dla odbiorcy

Filtry kształtują tylko raport, ZIP z dowodami nadal zawiera cały dziennik i pliki. Jeśli odbiorca ma dostać mniej, użyj [ograniczonego przekazania](https://phishdestroy.github.io/TgWitness/pl/docs/handover/). Więcej: [zawartość raportu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-reports/), [weryfikacja eksportu](https://phishdestroy.github.io/TgWitness/pl/docs/exports/).
