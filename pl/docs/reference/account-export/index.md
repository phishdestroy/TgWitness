# Telegram · Eksport konta

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/account-export/

Eksportuj to, co konto może obecnie odczytać: zakres, zadania z możliwością wznowienia, podpisane archiwum oraz zminimalizowane kopie udostępniane.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Dowody i weryfikacja](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)

![Dowody i weryfikacja](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

Eksport konta rezerwuje je na wyłączność. Przed startem lub wznowieniem jawnie wstrzymaj monitoring albo inne pozyskiwanie danych; aplikacja nigdy nie zatrzymuje ich automatycznie.

Jako administrator instalacji wybierz **Zacznij tutaj → Eksportuj moje konto** lub **Eksporty → Konto Telegram → Skonfiguruj eksport konta**. W razie potrzeby zaloguj się, sprawdź zakres i wyraźnie uruchom eksport. Ciągła obserwacja nie jest wymagana. **Zapisane obserwacje** to oddzielny eksport istniejącego dziennika; jego ZIP obejmuje wszystkie źródła niezależnie od filtrów dziennika. Każdy obszar roboczy ma własne zadania, tożsamość podpisującą i pamięć masową. Przyznany dostęp do panelu, w tym nieograniczone uprawnienie do zwykłego eksportu, nie pozwala na otwarcie tych ścieżek obejmujących całe konto.

Filtry nadawców i tekstu rozwijają się w sekcji **„Filtruj według nadawcy lub treści wiadomości**”. **Sekcja „Dane konta i metoda połączenia**” zawiera opcjonalne kategorie kont oraz wybór między trybem Takeout a zwykłą sesją; jej podsumowanie pokazuje aktywne opcje nawet po zamknięciu. Zamknięcie tych sekcji powoduje zachowanie ich ustawień. Szablony eksportu i raportów pozostają w bieżącej sesji panelu podczas zmiany widoków; nie są one zapisywane po ponownym załadowaniu przeglądarki. Dostęp do istniejących zadań jest możliwy z obu opcji eksportu.

Ten przepływ pracy eksportuje dane, do których obecnie ma dostęp podłączone konto. Domyślnie wykorzystywana jest [funkcja Telegram Takeout](https://core.telegram.org/api/takeout); nie jest to kopia zapasowa niedostępnych lub usuniętych danych z Telegrama. Tajne czaty, niedostępna historia i wcześniejsze edycje nie są odzyskiwane. Telegram może nałożyć okres oczekiwania przed uruchomieniem funkcji Takeout. Panel wyświetla ten czas oczekiwania; nie przełącza transportu w tle. Opcja „explicit regular-API” ma inny zakres i rejestruje kategorie, które nie są obsługiwane.

Takeout to oficjalny interfejs API eksportu, z którego korzysta również aplikacja Telegram Desktop. TgWitness może zapisywać plik JSON zgodny z Desktopem bezpośrednio na podstawie własnych danych; importowanie cudzego archiwum nie jest wymagane. Identyfikatory czatów i wiadomości są dostępne w obu kanałach transmisji. Czat publiczny lub uprawnienie do przekazywania wiadomości nie gwarantują szybszego eksportu ani nie eliminują opóźnienia związanego z zatwierdzeniem przez Takeout. Przed porównaniem szybkości należy ustawić ten sam zakres i te same ustawienia multimediów.

W przypadku maksymalnie 20 wyraźnie wybranych identyfikatorów czatów eksport za pomocą standardowego API rozpoznaje te węzły bezpośrednio przed uwzględnieniem pełnego wykazu dialogów konta. Czytelny kanał publiczny można zatem wyeksportować bez dołączania do niego, nawet jeśli nie ma go na liście dialogów. Użytkownicy niebędący w pamięci podręcznej są traktowani zgodnie ze zwykłą listą. Filtr archiwum pozostaje aktywny: jeśli Telegram nie zwraca dialogu, a zarchiwizowane czaty są wykluczone, nieznany status archiwum jest rejestrowany jako pominięcie. Takeout zachowuje procedurę podziału zakresu listy. Żadna z ścieżek nie dołącza do czatów ani nie zmienia uprawnień do przekazywania wiadomości. W formacie JSON zgodnym z wersją na komputery stacjonarne kanały oznaczone przez Telegram jako `left` pojawiają się pod `left_chats`, w tym publiczne kanały z prawem do odczytu, do których konto nie dołączyło.

Zarówno żądania wstrzymania typu `FLOOD_WAIT`, jak i `FLOOD_PREMIUM_WAIT` trwają przez cały okres żądany przez serwer. Termin ważności konta jest zachowywany po ponownym połączeniu i ponownym uruchomieniu; krótszy późniejszy czas oczekiwania nie może go skrócić. Liczba ponownych prób jest ograniczona, anulowanie zachowuje zapieczętowane strony, a poświadczenia API nie są rotowane w celu ominięcia limitu częstotliwości. Nie dokonuje się zakupu usługi Premium.

## Wybierz, co ma być gromadzone

| Kontekst | Znaczenie |
| --- | --- |
| Cel | Zapisz, dlaczego ta akwizycja jest konieczna. Nie umieszczaj tutaj zbędnych nazwisk ani poufnych szczegółów dotyczących sprawy. |
| Język raportu | Wybierz język etykiet w czytelnym raporcie. Oryginalny tekst wiadomości pozostaje niezmieniony; nieprzetłumaczone etykiety szablonów są w języku angielskim. Język jest ustalany na stałe w opcjach podpisanego zadania. |
| Rodzaje czatów / identyfikatory czatów | Wszystkie wybrane typy lub tylko wymienione czaty; „Zapisane wiadomości” dotyczą czatów prywatnych. Zarchiwizowane czaty można wybierać osobno. |
| Daty | UTC. Uwzględniono zarówno datę początkową, jak i końcową z kalendarza panelu. API stosuje daty włącznie `from_utc` i wykluczające `to_utc`; panel wysyła początek dnia następującego po dacie „Do”. Pusty przedział pozostawia tę stronę nieograniczoną. |
| Identyfikatory nadawców | Tylko wiadomości od wymienionych nadawców; pusta lista obejmuje wszystkich nadawców. |
| Tekst zawiera | Frazy dosłowne, w których nie rozróżnia się wielkości liter, są dopasowywane za pomocą operatora OR. Warunki dotyczące nadawcy, daty i własnej wiadomości łączą się za pomocą operatora AND. |
| Własne wiadomości | Zachowuj wyłącznie wiadomości wychodzące. |
| Typy multimediów | Wybierz kategorie załączników lub wyczyść wszystkie, aby uniknąć pobierania plików z wiadomości. |
| Limity plików / łączna pojemność multimediów | MiB na plik oraz GiB wszystkich pobranych multimediów. Tekst, potwierdzenia, czytelne raporty oraz dane dodatkowe ZIP wymagają dodatkowej przestrzeni dyskowej. |
| Kategorie kont | Profil, kontakty, zdjęcia profilowe, relacje, metadane sesji i inne dane z funkcji Takeout mają oddzielne opcje sterowania. |

Ustawienie domyślne **kolekcji „Minimize”** wyłącza pliki i metadane kont. Filtry nadawców i treści są stosowane przed zachowaniem stron wiadomości i pobraniem multimediów. Telegram nadal przesyła strony historii API zawierające wiadomości potrzebne do oceny tych filtrów: filtrowanie nie gwarantuje, że niewybrane wiadomości nigdy nie trafią do pamięci procesora. Inne bieżące obserwacje w obszarze roboczym mają własny zakres i ustawienia przechowywania.

Historia zdjęć profilowych i relacje nie są domyślnie zaznaczone. Jeśli w sprawie potrzebne są wyłącznie wiadomości, należy również wyłączyć profil i kontakty. Jeśli załączniki lub metadane nie są potrzebne, wykluczenie ich podczas pozyskiwania danych pozwala uniknąć zachowania kolejnej prywatnej kopii w tym eksporcie.

Dane zdjęć wykorzystują wariant obrazu statycznego zidentyfikowany w ich metadanych i manifestach skrótów, w tym zdjęcia z animowanym wariantem awatara. Animacja ta nie zastępuje wybranego obrazu statycznego. Dane o mniejszym lub większym rozmiarze niż zaobserwowany są rejestrowane jako nieudany załącznik, a zmieniona reprezentacja podczas odnawiania odwołania do pliku jest odrzucana. Te błędy powodują, że archiwum pozostaje niekompletne, przy czym zachowane są zapisy wiadomości. Niezależna weryfikacja odrzuca również zapisane załączniki, których długość podpisu jest sprzeczna z ich zaobserwowanym rozmiarem lub reprezentacją, w tym w starszych archiwach.

## Podsumowanie, zakres i weryfikacja

Każde zadanie zamraża swoje opcje i tożsamość konta. Spis zasobów i przechwycone strony są podpisane; potwierdzenia stron rejestrują skróty, pozycje kursora, czasy, wyniki załączników oraz poprzedzające je potwierdzenia. Tylko zatwierdzone strony zwiększają postęp zadania. Funkcja restartu/wznowienia sprawdza te zapisy przed kontynuowaniem. Zmienione konto, zmieniona podpisana strona lub niespójny łańcuch potwierdzeń są odrzucane. Opcji nie można edytować w trakcie pozyskiwania danych: należy uruchomić kolejne zadanie dla innego zakresu.

Funkcja „Pause” wstrzymuje bieżącą operację na koncie. Ponowne uruchomienie aplikacji pozostawia niedokończoną pracę dostępną do wyraźnego wznowienia. Wygasła sesja „Takeout” wymaga wyraźnego wznowienia; zmiana zakresów podziału w Telegramie może wymagać nowego pobrania danych. Funkcja „Resume” zachowuje poprzednie obserwacje, więc długotrwały eksport nie stanowi jednej atomowej migawki. Inne operacje związane ze zmianą konta oraz konfliktowe eksporty są blokowane podczas pobierania danych. Przed usunięciem obszaru roboczego należy poczekać na zakończenie pakowania.

Funkcja „Wznów” weryfikuje już zgromadzone treści przed kontynuowaniem. Duże archiwa przechowywane na wolnych nośnikach mogą przekroczyć skonfigurowany limit **czasu działania panelu w sekcji Parametry →** (domyślnie 120 sekund). Przed ponowną próbą należy zwiększyć to ustawienie; anulowanie lub przerwanie przechowywania powoduje wstrzymanie zadania, a nieudane kontrole integralności powodują niepowodzenie zadania wraz z wyjaśnieniem. Weryfikacja musi zostać zakończona lub bezpiecznie zatrzymana, zanim pliki będą mogły zostać zamknięte. Żadne twierdzenia dotyczące przepustowości dużych kont nie zostały potwierdzone przez testy syntetyczne.

Panel rozróżnia ukończony, wybrany zakres od częściowego archiwum oraz rejestruje pominięcia i nieudane odczyty. Pliki celowo wykluczone różnią się od plików, których odczyt nie powiódł się lub które są niedostępne. Należy sprawdzić zakres pokrycia nawet wtedy, gdy weryfikacja integralności zakończyła się powodzeniem. Żaden lokalny czytnik nie jest w stanie udowodnić, że Telegram zwrócił każdą wiadomość, jaka kiedykolwiek istniała.

Gotowe pliki ZIP pozostają dostępne do wielokrotnego pobierania oraz pobierania w zakresie HTTP. Archiwum konta zawiera `manifest.json`, `manifest.sig`, podpisane `job.json`, `inventory.json`, `receipts/`, autorytatywne `data/*.jsonl`, wybrany `media/`, czytelny kod HTML oraz weryfikator. Przypnij odcisk palca kolektora za pośrednictwem niezależnego kanału, a następnie zweryfikuj go przy użyciu zaufanej instalacji:

```
python -m tgwitness.verify account-export.zip --fingerprint TRUSTED_SHA256
```

W przypadku archiwów, których rozwinięta zawartość przekracza 4 GiB, należy jawnie ustawić odpowiedni `--max-gib`. Panel weryfikuje uwierzytelnione, kompletne archiwa lokalne na podstawie zadeklarowanego rozmiaru po rozpakowaniu oraz opublikowanego skrótu ZIP; zewnętrzny interfejs CLI zachowuje niezależny limit rozmiaru. Należy przeprowadzić weryfikację przed otwarciem pliku HTML do odczytu. Dołączony do archiwum weryfikator jest wygodny, ale weryfikator pozyskany niezależnie pozwala uniknąć konieczności ufania kodowi wykonywalnemu dostarczonemu wraz z dowodem.

Podpis Ed25519 oraz skróty SHA-256 wykrywają zmiany po zapisaniu odpowiednich bajtów przez kolektor. **Nie** dowodzą one jednak, że Telegram podpisał te wiadomości, że operator kolektora działał uczciwie, że historia konta jest kompletna ani że sąd uzna te materiały za dowód. Czas przechwycenia jest mierzony według zegara kolektora. Niezależne znaczniki czasu oraz niezależne pochodzenie danych należy oceniać oddzielnie.

## Przygotuj ujawnienie informacji dla prawnika lub innego odbiorcy

Po pobraniu gotowego eksportu należy zachować oryginalny plik ZIP i otworzyć `index.html` z wyodrębnionej kopii. Raport wyjaśnia jego zakres, dostępny zasięg i ograniczenia. Odniesienia do zapisów łączą odniesienie do archiwum, ścieżkę dokumentu oraz numer zapisu, dzięki czemu odbiorca może zlokalizować ten sam wpis w kodzie HTML lub na wydruku. Przykład praktyczny: [otwórz fikcyjny raport](https://phishdestroy.github.io/TgWitness/demo/report/).

Po zakończeniu eksportu konta wybierz opcję **„Przygotuj kopię do udostępnienia**”. Spowoduje to utworzenie oddzielnej, podpisanej kopii pochodnej. Źródło ZIP pozostaje niezmienione i prywatne; nie wysyłaj go razem ze zminimalizowaną kopią pochodną, chyba że odbiorca jest upoważniony do otrzymania pełnej zawartości. Wybierz język raportu osobno. Zmiana języka lub dowolnego ustawienia wyboru wymaga kolejnego podglądu przed utworzeniem.

1. Wprowadź cel ujawnienia i wybierz kryteria dotyczące dat, identyfikatorów nadawców oraz dosłownego tekstu.
2. Można wybrać, czy zachować tożsamości, ujawniać tylko wymienionych uczestników, czy też pseudonimizować wszystkich. W trybie pseudonimizacji identyfikatory/tytuły czatów oraz identyfikatory wiadomości również są zastępowane. Pseudonimy są stałe w ramach jednego ujawnienia i zmieniają się między niezależnie przygotowanymi ujawnieniami.
3. Zachowaj tekst wiadomości, pomiń go całkowicie lub dodaj dosłowne nazwy/frazy do zamaskowania. W trybach prywatnych narzędzie maskuje również znane ukryte nazwy nadawców i alternatywne nazwy użytkowników, identyfikatory nadawców w postaci całych tokenów, nazwy w czatach bezpośrednich, linki, adresy e-mail oraz ciągi znaków przypominające numery telefonów. Dopasowywanie znanych nazw uwzględnia zamianę wielkości liter w Unicode, w tym `Straße`/`STRASSE`. Ogólne nazwy grup/kanałów nie są automatycznie usuwane z treści wiadomości. Jeśli limit maskowania znanych tożsamości zostanie przekroczony, należy zawęzić zakres eksportu źródłowego lub pominąć tekst; narzędzie nie pomija w milczeniu kolejnych nazw. Są to zasady oparte na zasadzie „najlepszego wysiłku”, a nie ogólnej anonimizacji.
4. Pliki należy pominąć, chyba że odbiorca ich potrzebuje. Dołączone oryginały zachowują swoją rozdzielczość, dźwięk, tekst i metadane. Narzędzie **nie** anonimizuje ich.
5. Wyświetl podgląd liczb, ostrzeżeń i przykładowych przekształconych wiadomości, a następnie wyraźnie potwierdź utworzenie. Przykłady są ograniczone do 12 wiadomości, z których każda może zawierać maksymalnie 2 000 znaków tekstowych. Jest to przykład, a nie pełny przegląd wyniku. Zmiana ustawień wymaga wyświetlenia kolejnego podglądu. Podgląd wygasa po 15 minutach i jest powiązany z daną sesją administratora oraz konkretnym oryginalnym elementem ZIP; nie można go ponownie wykorzystać po utworzeniu. Wyświetlenie nowego podglądu unieważnia poprzedni dla tego samego zadania i sesji.
6. Zapoznaj się z pełnym wynikiem `index.html` i `messages.jsonl` lokalnie przed przekazaniem. Jeśli zawiera on niepotrzebne informacje, utwórz nowe ujawnienie z bardziej rygorystycznymi wykluczeniami. Nie edytuj na miejscu podpisanego elementu ZIP.

### Wiadomości pominięte podczas selekcji

**Podgląd.** Ujawnienie nie wygląda na kompletne, gdy takie nie jest. W każdej rozmowie zawierającej co najmniej jedną ujawnioną wiadomość wiadomości pominięte w zaznaczeniu pojawiają się jako znaczniki, `[withheld by selection — rule: sender]` (lub `text`, `period`). Wybierz **opcję** **„Wiadomości pominięte przez zaznaczenie**”: jeden znacznik dla każdego ciągu kolejnych pominiętych wiadomości (ustawienie domyślne) lub jeden dla każdej wiadomości. Znaczniki zawierają wyłącznie regułę i liczbę, nigdy tekst, nadawcę, datę ani pliki. Czaty, w których nie ujawniono żadnych wiadomości, są całkowicie pomijane, więc pakiet nie ujawnia ich istnienia.

Ujawnione odpowiedzi wskazują, na co odpowiadają: na wiadomość zawartą w tej kopii, na wiadomość pominiętą w wyniku selekcji lub na wiadomość, której nie ma w eksporcie źródłowym (usuniętą przed eksportem lub nigdy nieeksportowaną; eksport nie pozwala ustalić, która z tych opcji ma miejsce). Wiadomość pominięta, na którą odpowiada ujawniona odpowiedź, zawsze otrzymuje własny znacznik, dzięki czemu odpowiedź wskazuje na wpis wyjaśniający, dlaczego jest pusta. Te trzy stany różnią się od usunięć i luk w zbiorze, które należą do eksportu źródłowego.

W `messages.jsonl` (format `tgwitness-account-disclosure-v2`) każda wiadomość zawiera `state`: `disclosed`lub `withheld` z `rules` i `count`. Ujawniona odpowiedź zawiera `reply_to` z adresatem `id` i `state` (`disclosed`, `withheld`, `not_in_source`). Manifest zlicza ujawnione wiadomości, czaty, multimedia oraz `withheld` wiadomości. `verify.py` Odrzuca znacznik zawierający treść oraz odpowiedź wskazującą na rekord brakujący w pakiecie; pakiety w wersji 1 są weryfikowane tak jak dotychczas.

W formacie zredukowanym pominięto ustrukturyzowane profile kont, kontakty, awatary, sesje, relacje, surowe obiekty Telegramu, nagłówki przekazywanych wiadomości, cytaty z odpowiedzi, karty kontaktów oraz metadane lokalizacji. Nie zawiera on oryginalnych plików JSONL, prywatnych ustawień filtrów, klucza pseudonimu ani mapy tożsamości. Zaznaczony tekst, wyraźnie zachowane tożsamości oraz dołączone pliki mogą nadal zawierać te same nazwy, identyfikatory lub frazy, które zostały użyte w tych filtrach; wymagają one oddzielnej weryfikacji. Polityka prywatności i klucz pseudonimów są przechowywane w zaszyfrowanej postaci w lokalnym sejfie zadania; usunięcie zadania powoduje wyczyszczenie powiązanych z nim prywatnych rekordów ujawnienia. Publiczne rekordy polityki filtrują liczbę, a nie wartości filtrów. Podany cel jest publiczny w manifeście i kodzie HTML: jawne kryteria prywatności oraz, w trybach pseudonimizacji, znane ukryte tożsamości są tam również maskowane, nawet gdy pominięto tekst wiadomości. Cel powinien być wolny od zbędnych danych osobowych; nieznany kontekst identyfikacyjny może pozostać.

Jego manifest łączy pliki pochodne, politykę publiczną oraz skrót oryginalnego elementu ZIP. Weryfikacja pozwala ustalić integralność oraz, jeśli źródło jest dostarczane lokalnie, zgodność powiązania źródłowego:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Powiązanie ze źródłem nie stanowi samodzielnego dowodu na to, że podczas przetwarzania wybrano wszystkie wymagane elementy lub usunięto wszystkie szczegóły umożliwiające identyfikację. Oryginalny tekst jawny nie został dołączony jako dowód. Do wydania takiej oceny konieczna jest nowa weryfikacja.

## Udostępnianie i przechowywanie zrzutów

Należy wybrać wiadomości i pliki potrzebne odbiorcy, przejrzeć kompletną kopię udostępnioną oraz zachować osobno kopię źródłową. Należy zapisać skrót pliku ZIP, który został dostarczony, aby odbiorca mógł zidentyfikować i zweryfikować tę konkretną kopię. Wybrane identyfikatory są zastępowane w ramach pseudonimizacji; zawarty tekst i oryginalne pliki pozostają częścią przeglądu.

GitHub Actions obsługuje eksport całego konta oraz wybranych czatów za pośrednictwem Takeout lub standardowego API, a także dziennik zdarzeń z jednego czatu. Przewodnik po przechwytywaniu hostowanym  wyjaśnia weryfikację ustawień oraz limit 120 minut. Aby zweryfikować kopię udostępnioną pochodzącą z przechwytywania hostowanego, należy porównać jej skrót źródłowy z oryginalnym archiwum oraz zweryfikować poświadczenie tego archiwum za pomocą kontroli specyficznych dla trybu .

[Format dowodów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/) · [Raporty dotyczące spraw](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-reports/)
