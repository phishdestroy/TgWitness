# Konfiguracja i weryfikacja raportów

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-reports/

Filtry raportów, osiem szablonów, gotowe ustawienia treści, zapisana historia zmian oraz ocena zawarta w podpisanych plikach eksportowych.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Investigation](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

Przekształć wybrane obserwacje w czytelny opis sprawy: jej przedmiot, zakres, zapisane zmiany, wykresy, ustalenia i odniesienia do źródeł. Każdy raport daje odbiorcy możliwość sprawdzenia dostarczonego materiału i zweryfikowania zakresu zgromadzonych danych.

Sekcja **„Podstawa zaufania i ograniczenia”** pojawia się w raportach dziennika, przekazania, czatu, konta oraz udostępniania. Pliki PDF dziennika i przekazania wykorzystują tę samą ocenę, co ich podpisany plik `report.json`. Manifesty ZIP zawierają element `case_assessment` w podpisanym manifeście. Ocena ta jest przekazywana wraz z wyeksportowanym materiałem. Oryginalne obserwacje zachowują swoje istniejące podpisy.

## Formaty dokumentów i kolejność czytania

### Studio raportów

Otwórz **menu Eksportuj → Skonfiguruj i wyświetl podgląd**. Przejdź przez **sekcję Dane → Projekt i zawartość → Podgląd**:

1. Wykorzystaj cały obszar roboczy lub wybierz czaty, autorów, w tym daty obserwacji w strefie czasowej UTC oraz typy zdarzeń. Załaduj katalog, aby przeszukiwać czaty i autorów, lub wprowadź ich identyfikatory Telegramu. Filtry autorów dopasowują zarejestrowane identyfikatory nadawców; powiadomienie o usunięciu bez nadawcy nie pasuje do filtra autora.
2. Wybierz układ strony, a następnie wybierz wykresy, etykiety uczestników, transkrypcję oraz swoje pisemne ustalenia. Zmiana układu powoduje zachowanie tych wyborów.
3. Utwórz podgląd. Pokazuje on rzeczywiste liczby, aktywność, uczestników, przykładowe rekordy, zapisane zmiany oraz brakujące zakresy numerów wiadomości. Zmiana wyboru sprawia, że podgląd staje się nieaktualny. Zapisz przed pobraniem pliku HTML, podpisanego pliku PDF, podpisanego pliku JSON lub pliku ZIP z dowodami.

Podgląd danych uwzględnia kompletny, stabilny prefiks dziennika, a nie początkową próbkę. Ograniczone są wyłącznie wyświetlane przykładowe wiersze i długie listy; ich pominięte liczby są wyświetlane. Późniejszy eksport tworzy nową, stabilną migawkę, więc trwające gromadzenie danych może zwiększyć te liczby. Zakres, liczby i tożsamość źródła są zawarte w podpisanym raporcie. Otwarcie lub podgląd formularza nie powoduje jego zapisania.

**Jurisdiction guidance.** Under Document details, open **Jurisdiction guidance · optional** to choose a jurisdiction and civil/commercial or criminal procedure. The appendix carries the legal basis, source links, preparation notes and research status. Local-language summaries and explanations of collection safeguards are optional. No jurisdiction is selected by default. These choices belong to the workspace, and are excluded from saved layout configurations and implicit sharing-copy defaults. See [defaults, supported reports and research limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/JURISDICTION_GUIDANCE.md).

**Należy wybrać wersję przeznaczoną dla odbiorcy.** Wykresy i transkrypcja opierają się na wybranych zapisach. Integralność, nadzór i zakres opisują pełny dziennik źródłowy. Plik ZIP z dowodami zawiera oryginalne zapisy i załączniki. Należy zastosować [zminimalizowane przekazanie,](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#handover-extract) gdy odbiorca ma otrzymać wyłącznie wybrane, dozwolone dane.

### Odczytuj zmiany, usunięcia i brakujące identyfikatory

Edycja pokazuje zapisany tekst **„przed”** i **„po”** oraz zaznacza zmienione słowa. Usunięcie pokazuje ostatnią wersję zapisaną przed zgłoszeniem. Jeśli żadna wcześniejsza treść nie została zarejestrowana, raport zawiera odpowiednią informację. Po wybraniu wyłącznie edycji lub usunięć, poprzednie wersje pozostają dostępne jako wyraźnie oznaczony kontekst poza filtrami. Komunikaty niezwiązane z tematem nie są dodawane do tych historii.

**Niezauważone identyfikatory wiadomości** to luki między znanymi numerami w wybranych czatach a zakresem identyfikatorów wyznaczonym na podstawie daty. Każdy znany rekord źródłowy jest sprawdzany przed uznaniem numeru za niezauważony: odfiltrowanie innego autora, typu zdarzenia lub daty nie może powodować powstania fałszywej luki. Sąsiednie zapisane wiadomości są oznaczane jako kontekst. Brakujący numer nie potwierdza, że wiadomość istniała lub została usunięta; powiadomienia o usunięciu i nieudane ponowne sprawdzenia pozostają odrębnymi typami zdarzeń.

### Wybierz projekt

Dostępnych jest osiem szablonów stron dla raportów w formacie HTML (dziennik i pojedyncza rozmowa) oraz podpisanych plików PDF. Wykorzystują one te same dane i obliczenia, różniąc się jedynie okładkami, typografią, nagłówkami rozdziałów, tabelami i odstępami.

| Projekt | Styl pisania |
| --- | --- |
| Klasyczny | Tradycyjna teczka z ciemną okładką i ponumerowanymi sekcjami. |
| Redakcja | Strona tytułowa w ramce z czcionką szeryfową, szerokie marginesy i wąska listwa rozdziałów. |
| Informacje ogólne | Zwięzła okładka z granatowym grzbietem, krótkimi nagłówkami i ściśle rozmieszczonymi tabelami. |
| Analizy | Okładka w stylu ankiety, modułowe tabele i rysunki o stałej szerokości znaków. |
| Techniczne | Rejestr z liniami, ponumerowana skala odniesienia oraz precyzyjne tabele porównawcze. |
| Przegląd | Panoramiczna okładka, duże odstępy i wyraźnie widoczne dane podsumowujące. |
| Seria artykułów | Spis treści oraz pogrupowane rozdziały dotyczące ustaleń, zakresu, zmian i dziennika obserwacji. |
| Księga i depozyt zabezpieczający | Numerowane rozdziały z szerokimi marginesami, precyzyjne wykresy i tabele oraz oddzielna transkrypcja wiadomości. |

Projekt jest zapisywany dla każdego obszaru roboczego i rejestrowany w podpisanym manifeście eksportu. HTML działa w trybie offline, obsługuje jasne i ciemne motywy oraz dostosowuje się do wąskich ekranów i języków pisanych od prawej do lewej. Natywne pliki PDF wykorzystują dołączone czcionki; projekt redakcyjny obejmuje czcionkę Noto Serif na licencji SIL Open Font License. Seria „Reading” oraz „Ledger & margin” mają również zastosowanie do przeglądów kont, czatów na kontach i udostępniania kopii.

Pliki PDF w językach chińskim, japońskim i koreańskim wymagają dodatkowo odpowiedniej czcionki na serwerze, takiej jak Noto Sans CJK, zainstalowanej w całym systemie lub umieszczonej w katalogu `TGWITNESS_FONT_DIR`. W przypadku jej braku plik ZIP zachowuje raporty w formatach HTML i JSON.

Te dwa projekty obejmują czytelny dziennik bez wykorzystania JavaScript. W przypadku dużych eksportów ten widok zawiera do 500 pełnych rekordów w ramach limitu wejściowego wynoszącego 8 MiB; raport wskazuje ten limit oraz zawiera linki do pełnej przeglądarki i rekordów źródłowych. Katalog kont i indeks relacji opisują tę samą próbkę odczytu, a nie wszystkich uczestników. Wykresy pełnego dziennika zachowują swój oddzielnie określony zakres.

### Wybierz treść

| Wstępnie ustalona zawartość | Domyślnie zawarte |
| --- | --- |
| Dokumentacja sprawy | Działania, czasy obserwacji, uczestnicy, czaty oraz transkrypcja zapisu. |
| Informacje ogólne | Przegląd działań bez rankingów uczestników ani transkrypcji. |
| Przegląd działań | Działania, czasy obserwacji, uczestnicy, czaty i ich skład, wraz z odniesieniami do źródeł i dokładnymi danymi liczbowymi. |
| Raport niestandardowy | Własna kombinacja wykresów, transkrypcji i podglądów. |

Zmiana ustawień domyślnych pozwala zachować projekt, szczegóły sprawy i sporządzoną analizę. Kontrole integralności, zakres, ograniczenia i instrukcje weryfikacji pozostają w każdym projekcie. Rekordy źródłowe w pliku ZIP pozostają niezmienione, gdy wykres lub transkrypcja są ukryte.

Opcjonalne **„Notatki z badania**” zawierają pytanie, metodę, ustalenia i wnioski sporządzone przez autora raportu. W ustaleniach należy podać numer pliku źródłowego i numer rejestru. Podpis zabezpiecza te autorowskie oświadczenia wraz z raportem; obserwacje źródłowe i interpretacja autora pozostają możliwe do zidentyfikowania. W przypadku zminimalizowanych przekazów pomija się te prywatne notatki oraz pełne wykresy z dziennika. Wybory dotyczące wykresów i badań mają zastosowanie do raportów z dziennika.

Wybierz aktywność w czasie, mapę cieplną dni tygodnia i godzin w strefie UTC, rankingi uczestników, rankingi czatów oraz skład zapisów. Wybierz 5–30 grup według rankingu oraz neutralne aliasy uczestników lub identyfikatory kont. Nieznani nadawcy i pozostali uczestnicy znajdują się w oddzielnych wierszach. Aliasy mają wpływ wyłącznie na wykresy; zapisy źródłowe nadal zawierają ich tożsamości.

Podgląd projektu aktualizuje się na podstawie niezapisanego szkicu, wykorzystując okładkę produkcyjną, elementy analizy i wykresów, ograniczając się do wyników pasujących w pierwszych 50 000 rekordów źródłowych. Poniższy podgląd danych oblicza kompletny wybór. Jest on wyraźnie niepodpisany i nie zachowuje wprowadzonych zmian. Przyciski „Okładka” i „Wykresy” przełączają sekcje podglądu. Nie jest to pełny podgląd pliku PDF. **Opcja „Zapisz ustawienia raportu”** stosuje wybrane opcje do przyszłych eksportów; istniejące podpisane pliki są niezmienne. Plik PDF wykorzystuje wybraną okładkę, typografię, układ rozdziałów oraz te same wybrane agregaty, co HTML i podpisany plik JSON.

Ocena wiarygodności, ograniczenia zakresu oraz instrukcje weryfikacji pozostają aktualne. Ukrycie wykresów lub czytelnej transkrypcji nie powoduje usunięcia wierszy zawierających wiarygodne źródła z pliku ZIP. Wyłączone serie wykresów są pomijane w analitycznym pliku JSON; należy skorzystać z eksportu w trybie zminimalizowanym, aby ograniczyć ujawnianie rekordów źródłowych.

Filtry wyboru danych mają zastosowanie do raportów dziennika; eksporty kont i udostępnionych treści zachowują własny zakres pozyskiwania i ujawniania danych.

Wspólne preferencje dotyczące projektu/wykresów są utrwalane w nowych eksportach czatów/kont oraz w podglądach udostępniania kont. Ustawienia językowe i prywatności konta oraz udostępniania pozostają niezależne; prywatne notatki dotyczące spraw i analiz nie są kopiowane do tych eksportów. Raporty dotyczące kont i udostępniania pozostają w formacie HTML chronionym przez podpisany manifest archiwum. Dziennik, zminimalizowane przekazywanie dziennika oraz zestawy do pojedynczych czatów również zapewniają podpisane pliki PDF.

### Co pokazują wykresy

Aktywność dziennika i mapy aktywności uwzględniają **obserwacje** nowych, historycznych, odzyskanych, edytowanych, usuniętych oraz brakujących przy ponownej weryfikacji, według czasu obserwacji kolektora w strefie czasowej UTC. Sygnały kontrolne i potwierdzenia odbioru załączników są wykluczone. W rankingach uczestników uwzględniane są wyłącznie nowe, historyczne i odzyskane obserwacje wiadomości: nadawca nie jest uznawany za osobę edytującą ani usuwającą. Powtarzające się obserwacje mogą odnosić się do tej samej wiadomości w Telegramie.

Analizy dziennika zachowują liczby według rodzaju, odniesienia do pierwszego/ostatniego zapisu oraz źródłowy plik ` `events.jsonl`` z skrótem SHA-256. Dane liczbowe zawierają dokładne wartości w formatach HTML i PDF. Codzienne przedziały czasowe przechodzą na przedziały miesięczne po przekroczeniu 366 zarejestrowanych dni; wykresy łączą je w maksymalnie 36 przedziałów o równej szerokości. Ponad 100 000 unikalnych identyfikatorów lub 1 200 miesięcy powoduje, że dany wykres staje się niedostępny, podczas gdy dokładne łączne liczby pozostają dostępne.

Wykresy migawek i udostępniania kont uwzględniają wyłącznie wiersze zawierające wiadomości niezwiązane z usługą, na podstawie zarejestrowanego czasu wysłania wiadomości. Agregaty dotyczące udostępniania są obliczane po redakcji i filtrowaniu. Wykresy te wykorzystują maksymalnie 90 przedziałów czasowych o równej szerokości w formacie UTC i zachowują do 10 000 wartości grupujących; nadwyżki są wyraźnie zgłaszane i uzgadniane. Ostatni przedział może być krótszy. Nieznane lub nieprecyzyjne daty nie są uwzględniane na wykresach czasowych.

Pusty przedział oznacza brak uwzględnionych obserwacji; w przypadku luk należy sprawdzić zakres pokrycia. Te wykresy opisują zapisane działania. Nieznani nadawcy pozostają w oddzielnej kategorii, a każda kontrola jest raportowana indywidualnie.

W przypadku dołączenia plik `analytics.json` jest chroniony przez podpisane skróty plików archiwum. `report.json` dziennika zawiera tę samą wybraną sumę zbiorczą. Weryfikacja podpisu wykrywa zmienione bajty. Aby sprawdzić dane liczbowe, należy ponownie obliczyć sumy zbiorcze dziennika za pomocą `report_analytics.Analytics` i `selected` lub sumy zbiorcze migawki za pomocą `snapshot_analytics.collect` i `project`.

### Anomaly indicators

**Preview.** Evidence reports add an **Anomaly indicators** section computed by registered processors (`tgwitness/metrics/`, one file per metric). The report names every processor that ran with its version, and prints its method under its table, so the computation can be repeated from `events.jsonl` with `tgwitness.metrics.run`.

| Processor | Co pokazuje |
| --- | --- |
| `first_time_posters_over_time` v1 | First-time posters and messages per UTC day. A flag requires at least five first-time posters and three times their median, with message volume at most 1.5 times its median. The baseline uses at least seven observed days within the previous 14 calendar days, after seven days of warm-up. |
| `service_vs_message_ratio` v1 | Distinct saved message numbers per chat and the share used by service messages. It describes a numbering; it does not explain a particular missing number. |
| `join_leave_per_month` v1 | Joins, departures and removals or bans per month, one per person, chat, change and day. |
| `pinned_per_month` v1 | Pin service messages, unpin notices, and pinned messages added or removed between chat-state snapshots, per month. |

**Parameters → Report metrics** selects processors and the number of displayed rows, including in filtered reports. Daily and monthly tables show recent rows, service-share tables rank chats by saved message count. Totals cover every row.

Na podstawie pobranego kodu źródłowego należy stworzyć wszystkie osiem wymienionych powyżej projektów na podstawie tego samego fikcyjnego dziennika:

```
python tools/build_report_styles.py --output test-results/report-styles
```

Otwórz plik `index.html`, aby porównać kompletne raporty HTML, podpisane pliki PDF oraz archiwa ZIP. Każdy projekt wykorzystuje ten sam dziennik źródłowy. Używaj nowego katalogu wyjściowego dla każdego uruchomienia, aby zachować poprzednio podpisane przykłady.

![Fikcyjna dokumentacja HTML](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

Plik HTML otwiera się stroną tytułową sprawy i kluczowymi danymi. Numerowana mapa dowodów zawiera linki do każdego ustalenia, faktów je potwierdzających, ograniczeń oraz niezależnej weryfikacji. Możliwość wyszukiwania rekordów oraz stałe odniesienia do rekordów pozostają dostępne w przeglądarce offline. Projekt dostosowuje się do wąskich ekranów, zarówno motywów, jak i przeglądarek bez obsługi JavaScript.

Podpisany plik PDF zawiera dedykowaną okładkę formatu A4, numer referencyjny raportu i kod QR, streszczenie wykonawcze, mapę dowodów, ponumerowane ustalenia oraz zakładki dokumentów. Nagłówki i stopki stron identyfikują raport. Kod QR identyfikuje materiał; nie jest to niezależny wynik weryfikacji. Wydruki z przeglądarki są oddzielone od tego podpisanego kryptograficznie pliku PDF.

Oś czasu obserwacji umieszcza zarejestrowane okresy obserwacji i przerwy na tej samej osi czasu UTC. Puste miejsca nie oznaczają domniemanego zasięgu; szczegółowe tabele zachowują dokładne przedziały czasowe. Plik ZIP zawiera czytelne raporty, podpisane pliki JSON, rekordy źródłowe oraz instrukcje weryfikacji.

Należy stworzyć nową, fikcyjną dokumentację w języku angielskim/rosyjskim/niemieckim z zainstalowanym środowiskiem programistycznym:

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Każdy katalog językowy zawiera pliki `report.html`, `report.pdf`, `report.json` oraz `dossier.zip`. Istniejące katalogi przykładowe nigdy nie są nadpisywane. Do utworzenia dokumentacji nie jest wykorzystywane żadne konto Telegram, zewnętrzna usługa znaczników czasu ani połączenie sieciowe.

![Pierwsze trzy strony fikcyjnego, podpisanego pliku PDF](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Analiza konkretnej sprawy

W przypadku dziennika zawierającego 1 200 wpisów, którego wpis nr 1 000 posiada zweryfikowany znacznik czasu, raport identyfikuje 200 późniejszych wpisów wykraczających poza granice tego znacznika czasu. Jest to górna granica istnienia punktu kontrolnego, a nie dowód czasu wysłania każdej wiadomości . Jeśli trzy inne pliki znaczników czasu nie przejdą walidacji lub nie można ich zweryfikować, są one liczone oddzielnie i nie mogą dostarczyć jednoznacznego wniosku.

Ważny znacznik czasu musi spełniać wszystkie poniższe warunki: jego odcisk musi odpowiadać punktowi kontrolnemu, jego podpis musi być powiązany z zaufanym korzeniem TSA w momencie nadania znacznika, a podpis, klucz, liczba i nagłówek punktu kontrolnego muszą dokładnie odpowiadać prefiksowi dziennika. Samo przeanalizowanie sygnatury czasowej lub posiadanie potwierdzenia OTS jest niewystarczające. Odbiorca musi samodzielnie wybrać zaufany korzeń TSA i powtórzyć weryfikację. OTS wymaga własnej kontroli potwierdzenia Bitcoin.

| Status raportu | Znaczenie |
| --- | --- |
| Sprawdzono podczas eksportu | Eksporter przeprowadził określoną kontrolę; nadal konieczne jest niezależne powtórzenie tej czynności. |
| Zapisano; wymagana weryfikacja | Rejestrowana jest podstawowa obserwacja lub oświadczenie operatora; nie stanowi to niezależnego potwierdzenia. |
| Nie obejmuje niniejszego tekstu | W tekście nie ma żadnych dowodów potwierdzających to twierdzenie. Nie stwierdza się jednak, że nigdzie indziej nie istnieją. |
| Nie zostało to niezależnie zweryfikowane | Raport nie zawiera wyników niezależnej weryfikacji. |
| Niekompletne lub niedostępne | Brakuje materiału lub wymaganej weryfikacji, są one niekompletne lub zakończyły się niepowodzeniem. |

Należy sprawdzić każdy punkt osobno, biorąc pod uwagę zakres zgromadzonych danych.

## Co musi zachować konfiguracja o wysokim poziomie bezpieczeństwa

1. Przed rozpoczęciem gromadzenia danych należy zachować odcisk klucza kolektora za pośrednictwem oddzielnego, zaufanego kanału. Należy porównać ten odcisk z kluczem podpisującym eksport.
2. Należy zachować niezależne punkty kontrolne z sygnaturami czasowymi oraz, w przypadku ich stosowania, dziennik świadków poza kontrolą administracyjną kolektora. Należy porównać je z wyeksportowanym dziennikiem, aby sprawdzić jego wcześniejsze granice.
3. Należy uwzględnić zakres pozyskiwania danych, luki, filtry, ograniczenia oraz zmiany w procesie gromadzenia danych. Należy wyjaśnić brakujące okresy istotne dla konkretnego zgłoszenia, wyraźnie odróżniając niezauważone identyfikatory wiadomości, powiadomienia o usunięciu oraz nieudane ponowne sprawdzenia.
4. Należy zachować oryginalne pliki ZIP i ich skróty. Należy odnotować każdego posiadacza, transfer, datę i cel. Należy zachować przypisane oświadczenia operatorów i notatki dotyczące sprawy wraz z nimi.
5. W przypadku poufnych komunikatów głosowych należy zachować i niezależnie zweryfikować cytat, wyzwanie, łańcuch certyfikatów Intel, pomiary, dokładne źródło oraz warunki obsługi kluczy. Wynik weryfikacji poświadczenia należy zachować wraz ze zweryfikowanymi artefaktami.

See [verification scope](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#verification-scope) for the checks of acquisition, archive integrity, time and collection coverage in each mode.

## Weryfikacja przez odbiorcę

Należy korzystać ze sprawdzonej instalacji programu TgWitness oraz niezależnie uzyskanego odcisku palca:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

Plik ZIP z danymi świadka musi pochodzić z niezależnego, zaufanego źródła; należy zachować również jego klucz i pochodzenie. Należy zachować polecenia, wersję narzędzia, wyniki, sprawdzone skróty danych wejściowych oraz nierozstrzygnięte pytania. Weryfikacja sygnału nawigacyjnego to oddzielna kontrola online; moduł renderujący raport nigdy nie łączy się z usługą wyłącznie w celu wyświetlenia raportu.

W przypadku sporu dotyczącego konkretnej wiadomości należy podać odniesienie do archiwum, autorytatywny plik oraz odniesienie do zapisu, a następnie opisać odpowiedni przedział czasowy, luki w pokryciu, wybór oraz materiały potwierdzające. W przypadku kopii udostępnianej należy również sprawdzić zarejestrowaną transformację i jej odniesienia do archiwum źródłowego. Filtry prywatności i mapowania tożsamości pozostają poza zakresem publicznej oceny.

Weryfikacja podpisanego pliku PDF wykrywa zmiany w objętych nią bajtach. Należy zachować oryginalny plik cyfrowy i wynik weryfikacji wraz z wszelkimi zrzutami ekranu lub wydrukowanymi kopiami do wglądu.
