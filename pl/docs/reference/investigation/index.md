# Tryb dochodzeniowy

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/

Kompleksowe dochodzenia dotyczące całych kont, obejmujące kanały, grupy, czaty prywatne i boty – od określenia zakresu po przygotowanie zweryfikowanej dokumentacji sprawy.

Śledź przebieg sprawy w różnych kanałach, grupach, czatach prywatnych i botach, od momentu pozyskania danych po sporządzenie osi czasu z odniesieniami oraz weryfikowalne przekazanie materiałów. Interaktywna wersja strony internetowej znajduje się pod adresem `/docs/cases/`; [instrukcje dotyczące podglądu](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

## Przykładowa sprawa: zmiana miejsca docelowego w czterech rozmowach

W ogłoszeniu pojawia się odniesienie do bota. Grupa operacyjna omawia nowy adres docelowy płatności, klawiatura bota wyświetla go, a w prywatnej wiadomości uzupełniającej informacja ta zostaje powtórzona. Następnie ogłoszenie zostaje edytowane, a wiadomość grupowa znika.

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

1. Należy podłączyć konto służące do gromadzenia danych w oddzielnym obszarze roboczym. W zewnętrznych notatkach dotyczących sprawy należy odnotować numer referencyjny sprawy, identyfikator konta, obszar roboczy, datę rozpoczęcia obserwacji oraz zaufany odcisk klucza podpisu.
2. **Źródła** otwarte **→ Zakres obserwacji → Tryb dochodzeniowy**. Ustawienie domyślne obejmuje **całe konto**, kanały/grupy/prywatne czaty/boty, własne działania, profile źródeł oraz 200 najnowszych widocznych wiadomości dla nowo wykrytych źródeł. Proszę zapoznać się z tymi ustawieniami, nacisnąć **przycisk „Zapisz zakres**” i potwierdzić wybrany zakres.
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

- **Funkcja „Załaduj pełną historię** ze **źródeł**” (obecnie `main`) ładuje dostępne przeszłe wiadomości z włączonych źródeł do dziennika obszaru roboczego. Obsługuje ona wstrzymywanie/wznawianie oraz podpisany raport o postępach. Zobacz sekcję [„Pozyskiwanie historii](https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/)”.
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

Proszę porównać skróty załączników oraz powiązane z nimi odniesienia do wiadomości. Identyczne pliki nie pozwalają ustalić twórcy, osoby przekazującej ani wspólnego operatora. Same identyczne nazwy i podobne awatary nie pozwalają połączyć dwóch identyfikatorów Telegramu w jedną osobę.

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

Korelacja między przestrzeniami roboczymi odbywa się w zewnętrznych notatkach dotyczących spraw lub narzędziach analitycznych. TgWitness nie posiada obecnie funkcji globalnego wyszukiwania między przestrzeniami roboczymi, scalonej osi czasu, wykresu śledczego ani połączonego archiwum spraw. Eksport danych z wielu kont z **jednego** kanału lub supergrupy stanowi odrębną operację, a nie połączenie dzienników tych kont.

W przypadku dłuższych projektów należy zachować niezależność w stosunku do [niezależnego świadka](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/). Należy stosować kontrolowane weryfikacje dostarczenia w celu potwierdzenia ścieżki przechwytywania i widoczności każdego konta.

## 7. Przygotowanie i weryfikacja przekazania sprawy

Proszę zgromadzić te materiały w katalogu sprawy przygotowanym przez analityka:

| Materiały | Cel |
| --- | --- |
| Notatki dotyczące spraw i rejestr źródeł | Pytania, polityka gromadzenia danych, dostęp/role, ustalenia, alternatywne wyjaśnienia oraz luki |
| Oś czasu | Dla każdego wpisu podano zarówno datę i godzinę, jak i odniesienia do obszaru roboczego, czatu, wiadomości oraz sekwencji |
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
```

Należy zachować rzeczywiste wyniki weryfikacji oraz oryginalne artefakty. Katalog najwyższego poziomu sprawy, rejestr źródeł oraz wnioski analityków są przechowywane zewnętrznie; każdy artefakt TgWitness posiada własny podpis oraz procedurę weryfikacji.

## Dostosowanie dochodzenia

| Przykład | Śledzenie | Dostarczyć |
| --- | --- | --- |
| Spór dotyczący zamówienia/płatności obsługiwany przez bota | Ogłoszenie o dodaniu wpisu → podgląd zapisanego linku → parametr uruchamiania bota → wersje wiadomości i klawiatury → potwierdzenia wywołania panelu → dalsze działania dotyczące wiadomości prywatnych/grupowych | Uwzględniono chronologię ofert i odpowiedzi oraz zweryfikowane źródła; sam link do płatności nie stanowi dowodu dokonania płatności |
| Wiadomości usunięte po zdarzeniu | Wszystkie czaty, których to dotyczy → zapisane oryginały/zmiany → wyniki dotyczące usunięcia lub braku wiadomości przy ponownej weryfikacji → zachowane pliki multimedialne → zakres monitorowania oraz inne perspektywy związane z kontem | Zachowane wersje oraz wyraźnie zaznaczone nieznane przedziały czasowe; brak fikcyjnych podmiotów odpowiedzialnych za usunięcie wiadomości |
| Uczestnik zmienia imiona w różnych czatach | Numeryczny identyfikator nadawcy → historia nazwisk/nazw użytkowników → odpowiedzi → inne zaobserwowane rozmowy → cytowane miejsca docelowe/pliki | Cytowana oś czasu aktywności konta w Telegramie, z oddzielnym przedstawieniem hipotez dotyczących tożsamości w świecie rzeczywistym oraz powiązań |

[Odniesienie do zbioru](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/) · [Weryfikacja profili osób](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#people-profiles) · [Przekazywanie dowodów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#investigation-handoff) · [Weryfikacja zakończona](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/)
