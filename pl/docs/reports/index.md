# Opracuj raport

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reports/

Należy zapewnić czytelnikowi przejrzystą ścieżkę od pytania dotyczącego sprawy do zapisanych danych.

Studio raportów łączy w sobie funkcję wyboru danych, czytelne historie zmian, wykresy oraz sporządzone przez użytkownika wnioski. Osiem zintegrowanych szablonów ma zastosowanie do obsługiwanych formatów wyjściowych HTML i natywnego PDF. Raporty w formatach HTML, PDF i JSON posiadają własne podpisane pieczęcie; manifest plików ZIP dodatkowo wiąże pliki w pakiecie. Pliki HTML i PDF są pieczętowane po zakończeniu ich ostatecznego formatowania.

## Sporządź raport w trzech krokach

1. Otwórz **Eksport → Konfiguruj i podgląd → Dane**. Wykorzystaj cały obszar roboczy lub wybierz czaty, autorów, daty obserwacji w strefie czasowej UTC oraz typy rekordów. Daty określają, kiedy program TgWitness zarejestrował dany rekord.
2. W sekcji **„Projekt i treść**” wybierz gotowy szablon projektu i treści. Wybierz wykresy aktywności, etykiety uczestników, transkrypcję, zapisane zmiany oraz opcjonalne materiały z Case Board. Dodaj szczegóły sprawy i notatki z badania.
3. Otwórz **podgląd**, aby sprawdzić liczbę rekordów, aktywność, uczestników, rekordy z próby oraz brakujące zakresy identyfikatorów. Zapisz ustawienia, a następnie pobierz potrzebny format.

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

**Sekcje „Classic”, „Editorial”, „Briefing”, „Analytics”, „Technical”, „Overview”, „Reading series” oraz „Ledger & margin”** przedstawiają te same podstawowe zapisy w różnych układach. Zmiana układu nie wpływa na wybór danych ani na zapisane notatki. Język raportu można wybrać spośród 25 obsługiwanych języków.

Sekcja „Reading series” grupuje sprawę, zakres, ustalenia i zmiany wokół paska sekcji. Sekcja „Ledger & margin” wykorzystuje ponumerowane rozdziały i szerokie marginesy. Obie sekcje obsługują również przeglądy kont w formacie HTML oraz udostępnianie kopii. Natywne pliki PDF są generowane z dołączonymi czcionkami; komputer użytkownika nie wymaga instalacji przeglądarki ani środowiska Node do tworzenia plików PDF. Pliki PDF w językach chińskim, japońskim i koreańskim wymagają dodatkowo odpowiedniej czcionki na serwerze, takiej jak Noto Sans CJK, zainstalowanej w całym systemie lub umieszczonej w katalogu `TGWITNESS_FONT_DIR`. W przypadku jej braku plik ZIP zawiera raporty w formatach HTML i JSON.

## Zapoznaj się ze zmianą w jej kontekście

Zapisane zmiany są wyświetlane w wersji „przed” i „po”. Powiadomieniu o usunięciu może towarzyszyć ostatnia zarejestrowana wersja. Odpowiedzi, cytaty, przekazania, reakcje, przyciski i metadane załączników zachowują dostępne odniesienia. Skróty SHA-256 plików i dzienników są oznaczone oddzielnie.

Podgląd projektu pokazuje elementy okładki, analizy i wykresów przy użyciu dopasowanych rekordów spośród pierwszych 50 000 rekordów źródłowych. Oddzielny podgląd danych skanuje kompletną, stabilną migawkę dziennika w celu uzyskania dokładnych liczb wybranych elementów, z oznaczonymi limitami wyświetlanych próbek. Wygeneruj plik PDF, aby sprawdzić ostateczną paginację. Pełny eksport konta zawiera przegląd w formacie HTML; poszczególne pliki PDF z czatami wykorzystują wybrany układ.

## Starannie dobierz wersję przeznaczoną dla odbiorcy

Filtry raportów kształtują czytelny raport. Pełny plik ZIP z dowodami zachowuje oryginalny dziennik i załączniki. Należy stosować [zminimalizowane przekazywanie danych,](https://phishdestroy.github.io/TgWitness/pl/docs/handover/) gdy odbiorca ma otrzymać tylko wybrane dane. Należy sprawdzić [zawartość raportu i weryfikację](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-reports/) lub [zweryfikować gotowy eksport](https://phishdestroy.github.io/TgWitness/pl/docs/exports/).
