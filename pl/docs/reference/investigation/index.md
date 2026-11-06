# Tryb dochodzeniowy

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/

Kompleksowe dochodzenia dotyczące całych kont, obejmujące kanały, grupy, czaty prywatne i boty – od określenia zakresu po przygotowanie zweryfikowanej dokumentacji sprawy.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Dochodzenie](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

Śledź przebieg sprawy w różnych kanałach, grupach, czatach prywatnych i botach, od momentu pozyskania danych po sporządzenie osi czasu z odniesieniami oraz weryfikowalne przekazanie materiałów. Interaktywna wersja strony internetowej znajduje się pod adresem `/docs/cases/`; [instrukcje dotyczące podglądu](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

**Na tej stronie**

- [Przykład działający: miejsce docelowe zmienia się w czterech rozmowach](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/#worked-case-a-destination-changes-across-four-conversations)
- [1. Zdefiniuj przypadek i zebraj pełny opis](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/#1-define-the-case-and-collect-the-whole-account)
- [2. Sporządź spis wszystkich źródeł i zgromadź kontekst historyczny](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/#2-inventory-every-source-and-acquire-historical-context)
- [3. Zachować ewoluujący kontekst i celowe interakcje](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/#3-preserve-the-evolving-case-and-deliberate-interactions)
- [4. Łączenie obserwacji z różnych czatów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/#4-connect-observations-across-chats)
- [5. Stworzenie osi czasu obejmującej różne czaty](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/#5-build-the-cross-chat-timeline)
- [6. Dodaj perspektywy kont bez utraty ich pochodzenia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/#6-add-account-perspectives-without-losing-their-origin)
- [7. Zbierz i zweryfikuj przekazanie sprawy](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/#7-assemble-and-verify-the-case-handoff)
- [Dostosuj dochodzenie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/#adapt-the-investigation)

## Przykładowa sprawa: zmiana miejsca docelowego w czterech rozmowach

Ogłoszenie odsyła do bota. Grupa operacyjna omawia nowy adres docelowy płatności, a klawiatura bota wyświetla go. Ogłoszenie zostaje edytowane, w prywatnej wiadomości uzupełniającej powtórzono adres docelowy, a wiadomość grupowa znika.

Pytania brzmią: co zaobserwowano przed i po zmianie, które konta w Telegramie opublikowały poszczególne wpisy, gdzie pojawił się adresat, które bajty załącznika zostały zachowane oraz jakie przedziały czasowe pozostają nieznane?

Wszystkie nazwy, identyfikatory, daty i odniesienia do dziennika w niniejszym przykładzie są fikcyjne. Proces wykorzystuje aktualne funkcje; mapa sprawy ma charakter ilustracyjny i nie jest automatycznym wykresem wygenerowanym przez aplikację.

Schemat blokowy · Kanały → Dziennik obszaru roboczego; Grupy → Dziennik obszaru roboczego; Czat prywatny → Dziennik obszaru roboczego; Boty → Dziennik obszaru roboczego; Dziennik obszaru roboczego → Przeszukaj wszystkie źródła; Dziennik obszaru roboczego → Profile osób wraz z odniesieniami do zapisów; Dziennik obszaru roboczego → Zapisane wersje i potwierdzenia otrzymania załączników; Przeszukaj wszystkie źródła → Oś czasu analityka i rejestr źródeł; Profile osób wraz z odniesieniami do zapisów → Oś czasu analityka i rejestr źródeł; Zapisane wersje i potwierdzenia otrzymania załączników → Oś czasu analityka i rejestr źródeł; Dziennik obszaru roboczego → Podpisany plik ZIP z dowodami; Oś czasu analityka i rejestr źródeł → Przekazanie sprawy wraz z oddzielnie zweryfikowanymi dowodami; Podpisany plik ZIP z dowodami → Przekazanie sprawy wraz z oddzielnie zweryfikowanymi dowodami · Kanały · Grupy · Czat prywatny · Boty · Dziennik obszaru roboczego · Przeszukaj wszystkieźródła · Profile osób wraz zodniesieniami do zapisów · Zapisane wersje ipotwierdzenia otrzymaniazałączników · Podpisany plik ZIP zdowodami · Oś czasu analityka irejestr źródeł · Przekazanie sprawy wraz zoddzielnie zweryfikowanymidowodami

**Schemat w formie tekstowej**

1. Kanały → Dziennik obszaru roboczego
2. Grupy → Dziennik obszaru roboczego
3. Czat prywatny → Dziennik obszaru roboczego
4. Boty → Dziennik obszaru roboczego
5. Dziennik obszaru roboczego → Przeszukaj wszystkie źródła
6. Dziennik obszaru roboczego → Profile osób wraz z odniesieniami do zapisów
7. Dziennik obszaru roboczego → Zapisane wersje i potwierdzenia otrzymania załączników
8. Przeszukaj wszystkie źródła → Oś czasu analityka i rejestr źródeł
9. Profile osób wraz z odniesieniami do zapisów → Oś czasu analityka i rejestr źródeł
10. Zapisane wersje i potwierdzenia otrzymania załączników → Oś czasu analityka i rejestr źródeł
11. Dziennik obszaru roboczego → Podpisany plik ZIP z dowodami
12. Oś czasu analityka i rejestr źródeł → Przekazanie sprawy wraz z oddzielnie zweryfikowanymi dowodami
13. Podpisany plik ZIP z dowodami → Przekazanie sprawy wraz z oddzielnie zweryfikowanymi dowodami

## 1. Zdefiniowanie sprawy i zebranie pełnego opisu zdarzenia

1. Połącz konto zbierające w osobnym obszarze roboczym. W [Case Board](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-board/) lub w rejestrze spraw zapisz numer referencyjny sprawy, identyfikator konta, obszar roboczy oraz datę rozpoczęcia obserwacji. Oddzielnie zachowaj zaufany odcisk palca klucza podpisu.
2. Aby utworzyć dedykowane konto do gromadzenia danych, otwórz opcję **Źródła → Zakres obserwacji → Tryb dochodzeniowy**. Ustawienie domyślne wybiera opcję **Całe konto**, kanały/grupy/prywatne czaty/boty, własne działania, profile źródeł oraz 200 najnowszych widocznych wiadomości dla nowo wykrytych źródeł. Sprawdź ustawienia, naciśnij **„Zapisz zakres**” i potwierdź wybór zakresu. Konta główne korzystają z wybranych czatów lub folderu; gromadzenie danych z całego konta jest dostępne dla kont oznaczonych do dochodzenia.
3. **Proszę załadować czaty** i porównać źródła z listą rozmów na koncie. Sprawdź wykluczenia. **Parametr „Czatów odczytywanych z listy konta”** domyślnie wynosi 1 000 i pozwala na maksymalnie 20 000. Źródła wykraczające poza limit listy są dodawane, gdy stają się aktywne. Zapisz to, co faktycznie zostało zliczone.
4. W **ustawieniach rejestrowania** proszę wybrać opcję **„Wszystkie widoczne działania**” i zapisać ustawienia monitorowania. Proszę sprawdzić typy załączników i limity oraz ilość wolnego miejsca na dysku.
5. Rozpocznij obserwację. Zweryfikuj kontrolowaną nową wiadomość, edycję oraz usunięcie, a następnie zachowaj odniesienia testowe oraz wszelkie niepowodzenia.

Zakres obejmujący całe konto rejestruje aktywność widoczną na koncie zgodnie z zapisanymi ustawieniami. Narzędzie nie uzyskuje dostępu do tajnych czatów ani nie dołącza automatycznie do wszystkich powiązanych grup. Ponadto nie uzupełnia danych historycznych wszystkich istniejących rozmów. Proszę zapoznać się z [zakresem gromadzenia danych](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account).

## 2. Sporządzenie wykazu wszystkich źródeł i zebranie kontekstu historycznego

Proszę prowadzić rejestr źródeł, w którym każdy wiersz odpowiada jednej rozmowie:

| Dziedzina | Rejestruj |
| --- | --- |
| Tożsamość | Obszar roboczy, identyfikator konta, numeryczny identyfikator czatu, tytuł i typ |
| Widoczność | Przynależność/rola, potwierdzony lub niepotwierdzony dostęp, wyłączenia |
| Rejestracja na żywo | Data rozpoczęcia, wybrane typy zdarzeń oraz późniejsze zmiany w zasadach |
| Historia dziennika | Zgłoszone/wykonane zrzuty ekranu, limit, czas oraz odniesienia do zapisów |
| Pełna historia | Podpisana nazwa pliku eksportu dla poszczególnych czatów, granice oraz informacja o pomyślnym zakończeniu lub niepowodzeniu |
| Załączniki | Zawiera potwierdzenia odbioru plików multimedialnych, skróty, rozmiary oraz wyniki pominięć i niepowodzeń |
| Zakres | Przerwy w działaniu, niekompletne dane wejściowe, FloodWait, niedostępne wiadomości i inne luki |

Należy stosować odpowiednią metodę pozyskiwania danych dla każdego źródła:

- **Opcja „Załaduj pełną historię** ze **źródeł”** ładuje dostępne wcześniejsze wiadomości z włączonych źródeł do dziennika obszaru roboczego. Obsługuje ona funkcję wstrzymywania/wznawiania oraz podpisany raport z postępów. Zobacz sekcję [„Pozyskiwanie historii](https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/)”.
- **Zrzut historii** zapisuje ostatnie widoczne wiadomości w dzienniku obserwacji. Domyślna maksymalna liczba wynosi 500; w sekcji **Parametry → Największy zrzut historii** można zwiększyć tę liczbę do 10 000. Są to bieżące obserwacje historii, a nie zrekonstruowane zmiany.
- **Eksport całej rozmowy → opcja „Eksportuj całą rozmowę**” lub **„Rozmowy” → „Eksportuj rozmowę**” pobiera aktualnie widoczną historię jednej rozmowy do oddzielnego, podpisanego pakietu `chat.json` / `chat.html`. Proszę powtórzyć tę czynność dla wszystkich źródeł danej sprawy i zachować każdy wynik.
- **W przypadku pojawienia się nowego czatu lub bota** narzędzie może zapisać jego profil oraz do 1000 najnowszych wiadomości; tryb śledczy wybiera 200. Istniejące czaty nie są objęte tym funkcjonowaniem z mocą wsteczną po włączeniu trybu.
- **Pobieranie widocznych załączników** pozwala zachować liczbę bajtów zgodnie ze skonfigurowaną polityką. Wymagane jest wypełnione potwierdzenie `media.saved` z algorytmem SHA-256 i liczbą bajtów. Zadanie w kolejce, miniatura lub nazwa pliku nie stanowią zachowanego załącznika.

Eksport całej rozmowy **nie** uzupełnia dziennika ani profili użytkowników o wszystkie zawarte w niej wiadomości. Aby uzyskać historię, którą chcesz przeanalizować w TgWitness, użyj opcji **„Załaduj pełną historię”** lub „Ograniczone migawki dziennika”. Przed rozpoczęciem generowania historii sprawdź listę włączonych źródeł. Żadna z tych metod nie pozwala odzyskać treści, których Telegram już nie udostępnia.

## 3. Zachowanie przebiegu sprawy i celowych interakcji

Oznacz aktywne czaty dotyczące spraw jako źródła priorytetowe. Sprawdzaj częstotliwość ponownych kontroli, ciągłe uzupełnianie danych oraz wyniki analizy multimediów. Podczas korzystania z konta należy zapewnić ciągłą obserwację przez moduł gromadzący dane. Proszę skorzystać z **opcji Czaty → Profil → Zapisz profil teraz**, aby zachować metadane źródłowe, takie jak opisy i polecenia botów. Jest to odrębne od profili osób wygenerowanych na podstawie zapisanych wiadomości.

W przypadku gdy sprawa dotyczy śledzenia źródła lub interakcji z botem:

1. **Otwórz link w Telegramie → Zapisz podgląd – funkcja ta** rejestruje podany link oraz wyświetlony podgląd przed wykonaniem działania.
2. **Funkcja „Join / open and observe”** realizuje operację dołączenia/otwarcia oraz wysyła parametr startowy bota, jeśli został podany. Żądanie dołączenia oczekujące na zatwierdzenie jest rejestrowane jako oczekujące.
3. Odpowiedzi tekstowe wysyłane z panelu oraz obsługiwane naciśnięcia przycisków zachowują wartości `interaction.requested` i `interaction.result`. Potwierdzenia wywołania zwrotnego mogą zachowywać zwracany tekst wyskakującego okienka, stan alertu oraz adres URL.

Są to rzeczywiste działania na koncie. Naciśnięcia przycisku „Callback” w innej aplikacji Telegram nie są widoczne dla modułu gromadzącego dane, choć wynikające z nich wiadomości lub edycje mogą być widoczne. Mini-klient nie obsługuje procesów związanych z aplikacjami internetowymi, płatnościami, połączeniami telefonicznymi ani lokalizacją. Aby zapoznać się ze szczegółowym opisem działania, proszę przejść do sekcji [„Interakcje z panelem](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/#act-from-the-panel)”.

## 4. Łączenie spostrzeżeń z różnych czatów

W sekcji **„Dziennik**” należy wybrać opcję **„Wszystkie źródła**” i przeszukać zarejestrowane treści. Należy otworzyć pasujące wpisy i zapisać obszar roboczy, czat, identyfikator wiadomości, sekwencję oraz skrót zapisu.

W odpowiednim czacie proszę otworzyć **opcję „Osoby” → „Włącz profile”** i sprawdzić profil danej osoby:

- Nazwiska/nazwy użytkowników odnotowane na przestrzeni czasu oraz numeryczny identyfikator Telegramu.
- Odpowiedzi zawierające odniesienia do oryginalnych zapisów.
- **Również w…** innych czatach w tym dzienniku przestrzeni roboczej, w których pisał ten identyfikator.
- Aktywność, edycje/usunięcia oraz wymienione portfele, numery telefonów, nazwy użytkowników i linki.
- Zapisane metadane awatarów oraz podobne awatary z pamięci podręcznej wraz z informacją o ich odrębnym pochodzeniu.

Przed wykorzystaniem profilu wygenerowanego na podstawie tych danych w ustaleniach należy otworzyć cytowane zapisy. Profile obejmują osoby, których wiadomości zostały zapisane, a nie wszystkich członków grupy. **Parametry → Liczba cytowanych zapisów na fakt** ogranicza listę odniesień, a nie liczbę podstawowych zdarzeń. Wzmianki i podobieństwo awatarów stanowią wskazówki; nie potwierdzają one jednak przynależności ani tożsamości.

W przykładzie:

| Link | Rejestruje | Obserwacje poparte dowodami |
| --- | --- | --- |
| To samo konto nadawcy | Grupa nr 146 oraz prywatna kontynuacja nr 205 | Oba podają identyfikator nadawcy w Telegramie: 71001 |
| Ten sam adres docelowy | nr 146, klawiatura bota nr 173, edycja kanału nr 188, wiadomość prywatna nr 205 | Wszystkie zawierają kod `pay.example.invalid/new`; nie ustalono właściciela ani podmiotu sprawującego kontrolę |
| Ten sam zapisany plik | Zrealizowano potwierdzenia odbioru plików multimedialnych nr 151 i nr 209 | Pełne wartości SHA-256 są zgodne dla zachowanych bajtów |
| Źródło kanału | #101 i #188 | Nie należy przypisywać wpisu na kanale użytkownikowi 71001 bez podania nazwy nadawcy |

Porównaj skróty załączników i powiązane z nimi odniesienia do wiadomości oraz zachowaj osie czasu kont pogrupowane według identyfikatorów Telegramu podanych w tych rekordach.

Zachowaj notatki robocze zespołu w [Case Board](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-board/): dodaj do zakładek zapisy, na których się opierasz, takie jak #146, #188 i #205, zaznacz dokładny ciąg docelowy oraz zapisz fragment każdej zarejestrowanej czynności pomiędzy dwoma zapisami lub w danym przedziale czasowym. Notatki i statusy zachowują przegląd zespołu w osobnej, podpisanej historii, którą można odróżnić od obserwacji źródłowych.

## 5. Stworzenie osi czasu obejmującej różne czaty

Należy korzystać z linków do zapisanych wersji w **sekcji „Czat”** oraz do **wpisów w dzienniku o numerze #…** W **dzienniku** należy połączyć **wszystkie źródła** z **edycjami**, **usunięciami** i **zakresem**. Należy zachować zarówno `source_at` (o ile jest podany), jak i `observed_at`.

| Przykładowy czas obserwacji | Źródło | Uwaga |
| --- | --- | --- |
| 09:00 | Kanał nr 101 | Oryginalny adres docelowy został zarejestrowany |
| 09:12 | Grupa nr 146; media nr 151 | Opublikowano nową lokalizację; pobieranie pliku zakończono |
| 09:16 | Bot nr 173 | Klawisz kieruje do nowego miejsca docelowego |
| 09:20 | Kanał nr 188 | Ogłoszenie zostało zredagowane; zachowano obie zapisane wersje |
| 09:24 | Prywatne #205; media #209 | Ten sam identyfikator nadawcy powtarza się w polu odbiorcy; zachowano te same bajty pliku |
| 09:28 | Grupa nr 231 | Otrzymano powiadomienie o usunięciu; osoba, która dokonała usunięcia, oraz dokładny czas usunięcia nie są znane |

Pomiędzy podanymi przykładowymi odniesieniami występują inne zapisy. Numery sekwencyjne porządkują obserwacje; migawki historii mogą zawierać starsze daty źródłowe i pojawiać się później niż bieżące zdarzenia. Należy rozróżniać migawki, odzyskane wiadomości, powiadomienia o usunięciu oraz wyniki wskazujące na brak danych przy ponownej weryfikacji. Luki w zasięgu należy oznaczyć jako nieznane przedziały czasowe. Późniejsze pozyskanie danych historycznych nie zapewnia z mocą wsteczną nieprzerwanej obserwacji.

## 6. Dodawanie perspektyw kont bez utraty informacji o ich pochodzeniu

Należy korzystać z oddzielnego obszaru roboczego dla każdego odrębnego konta i powtarzać proces inwentaryzacji. Przy każdym porównaniu należy zachować identyfikator konta, rolę, odcisk klucza podpisu oraz odniesienia do źródeł. Numery wiadomości nie są globalnymi identyfikatorami obowiązującymi we wszystkich czatach i na wszystkich kontach.

Case Board przechowuje notatki powiązane ze źródłami oraz zbiory w obrębie każdego obszaru roboczego. Ekran grupowy umożliwia wspólny przegląd statusu kont i pozwala łączyć eksporty z poszczególnych obszarów roboczych. Można korelować te źródła w notatkach dotyczących sprawy lub narzędziach analitycznych; każdy dziennik zachowuje swoje pochodzenie i klucz podpisu. Nie jest generowane globalne wyszukiwanie ani scalona oś czasu obejmująca wszystkie obszary robocze. Eksport z wielu kont dla jednego kanału/supergrupy pobiera historię czatu przy użyciu kwalifikujących się kont.

W przypadku dłuższych projektów należy zachować niezależność w stosunku do [niezależnego świadka](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/). Należy stosować kontrolowane weryfikacje dostarczenia w celu potwierdzenia ścieżki przechwytywania i widoczności każdego konta.

## 7. Przygotowanie i weryfikacja przekazania sprawy

Proszę zgromadzić te materiały w katalogu sprawy przygotowanym przez analityka:

| Materiały | Cel |
| --- | --- |
| Notatki dotyczące spraw i rejestr źródeł | Pytania, polityka gromadzenia danych, dostęp/role, ustalenia, alternatywne wyjaśnienia oraz luki |
| Oś czasu | Dla każdego wpisu podano zarówno datę i godzinę, jak i odniesienia do obszaru roboczego, czatu, wiadomości oraz sekwencji |
| Case Board eksport i fragmenty, jeśli są używane | Zakładki powiązane ze źródłami, cytaty, notatki zespołu, kolekcje, historia zmian oraz wybrane zapisy sprawdzone pod kątem zgodności z plikiem ZIP zawierającym dowody |
| Podpisany plik ZIP z dowodami dla każdego obszaru roboczego | Kompletny zarejestrowany dziennik, spis treści oraz zawarte w nim zachowane pliki multimedialne; filtry panelowe nie ograniczają zakresu eksportowanego dziennika |
| Oddzielnie podpisane pliki zawierające profile osób | Wprowadzone odniesienia zostały zweryfikowane w oparciu o dowody z odpowiedniego obszaru roboczego |
| Podpisane eksporty pełnych rozmów | Bieżące gromadzenie widocznej historii, niezależne od dziennika obserwacji |
| Zweryfikowane odciski palców i wcześniejsze punkty kontrolne | Kluczowe elementy tożsamości oraz granice zachowanego dziennika |
| Elementy dowodowe z serwisu Witness, o ile zostały skonfigurowane | Oddzielny dziennik, podpisane wpisy oraz odcisk palca świadka |
| Wyniki weryfikacji oraz skróty dostarczonych plików | Co zostało sprawdzone, jakie bajty zostały przesłane i do kogo |

Z zaufanej instalacji, wraz z nazwami plików i rzeczywistymi odciskami palców poszczególnych obszarów roboczych:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Należy zachować rzeczywiste wyniki weryfikacji oraz oryginalne artefakty. Należy wyeksportować notatki z obszaru roboczego z Case Board wraz z cytowanymi materiałami źródłowymi. Należy zebrać ustalenia z różnych obszarów roboczych w katalogu sprawy najwyższego poziomu; każdy artefakt TgWitness posiada własny podpis i procedurę weryfikacji.

## Dostosowanie dochodzenia

| Przykład | Śledzenie | Dostarczyć |
| --- | --- | --- |
| Spór dotyczący zamówienia/płatności obsługiwany przez bota | Ogłoszenie o dodaniu wpisu → podgląd zapisanego linku → parametr uruchamiania bota → wersje wiadomości i klawiatury → potwierdzenia wywołania panelu → dalsze działania dotyczące wiadomości prywatnych/grupowych | Uwzględniono chronologię ofert i odpowiedzi oraz zweryfikowane źródła; sam link do płatności nie stanowi dowodu dokonania płatności |
| Wiadomości usunięte po zdarzeniu | Wszystkie czaty, których to dotyczy → zapisane oryginały/zmiany → wyniki dotyczące usunięcia lub braku wiadomości przy ponownej weryfikacji → zachowane pliki multimedialne → zakres monitorowania oraz inne perspektywy związane z kontem | Zachowane wersje oraz wyraźnie zaznaczone nieznane przedziały czasowe; brak fikcyjnych podmiotów odpowiedzialnych za usunięcie wiadomości |
| Uczestnik zmienia imiona w różnych czatach | Numeryczny identyfikator nadawcy → historia nazw/nazw użytkowników → odpowiedzi → inne obserwowane czaty → cytowane miejsca docelowe/pliki | Oś czasu aktywności konta w Telegramie wraz z linkami do źródłowych wpisów |

[Odniesienie do zbioru](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/) · [Weryfikacja profili osób](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#people-profiles) · [Przekazywanie dowodów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#investigation-handoff) · [Weryfikacja zakończona](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/)
