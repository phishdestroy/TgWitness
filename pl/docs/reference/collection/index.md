# Jak przebiega gromadzenie danych

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/

Zakres obserwacji, aktualizacje na żywo, ponowne weryfikacje, załączniki, własne działania oraz znaczenie luk w danych – wszystko to w ujęciu poszczególnych wpisów.

TgWitness rejestruje to, co obserwuje podłączone konto w aplikacji Telegram. Dziennik zachowuje te obserwacje, ich kolejność oraz towarzyszący im kontekst. Nie wyciąga wniosków dotyczących niewidocznych działań na podstawie brakującej wiadomości lub faktu, że konto jest podłączone.

## Od logowania do dziennika

Schemat blokowy · Autoryzacja konta użytkownika → Wybierz dostępne grupy i kanały; Wybierz dostępne grupy i kanały → Zapisz ustawienia zdarzeń i załączników; Zapisz ustawienia zdarzeń i załączników → Rozpocznij obserwację; Rozpocznij obserwację → Otrzymuj aktualizacje od aktywnego klienta; Otrzymuj aktualizacje od aktywnego klienta → Należy stosować zasady dotyczące źródeł i zdarzeń; Należy stosować zasady dotyczące źródeł i zdarzeń → Dodaj podpisane zgłoszenie; Dodaj podpisane zgłoszenie → Przeglądaj lub eksportuj dziennik; Dodaj podpisane zgłoszenie → Przetwarzanie wszelkich załączników znajdujących się w kolejce; Przetwarzanie wszelkich załączników znajdujących się w kolejce → Proszę dołączyć wynik pobierania · Autoryzacja kontaużytkownika · Wybierz dostępne grupyi kanały · Zapisz ustawieniazdarzeń i załączników · Rozpocznij obserwację · Otrzymuj aktualizacjeod aktywnego klienta · Należy stosować zasadydotyczące źródeł izdarzeń · Dodaj podpisanezgłoszenie · Przeglądaj lubeksportuj dziennik · Przetwarzaniewszelkich załącznikówznajdujących się wkolejce · Proszę dołączyć wynikpobierania

**Schemat w formie tekstowej**

1. Autoryzacja konta użytkownika → Wybierz dostępne grupy i kanały
2. Wybierz dostępne grupy i kanały → Zapisz ustawienia zdarzeń i załączników
3. Zapisz ustawienia zdarzeń i załączników → Rozpocznij obserwację
4. Rozpocznij obserwację → Otrzymuj aktualizacje od aktywnego klienta
5. Otrzymuj aktualizacje od aktywnego klienta → Należy stosować zasady dotyczące źródeł i zdarzeń
6. Należy stosować zasady dotyczące źródeł i zdarzeń → Dodaj podpisane zgłoszenie
7. Dodaj podpisane zgłoszenie → Przeglądaj lub eksportuj dziennik
8. Dodaj podpisane zgłoszenie → Przetwarzanie wszelkich załączników znajdujących się w kolejce
9. Przetwarzanie wszelkich załączników znajdujących się w kolejce → Proszę dołączyć wynik pobierania

Autoryzacja, dostęp do źródła, działający moduł zbierający dane oraz pełna dostawa to odrębne kwestie. Pomyślne zalogowanie się nie gwarantuje dostępu do wszystkich grup. Połączenie transportowe nie oznacza, że dotarły wszystkie istotne aktualizacje.

## Zakres monitorowania: wybrane czaty, folder lub całe konto

Źródła → **Zakres obserwacji** decyduje o tym, które czaty są rejestrowane w danym obszarze roboczym.

| Tryb | Rejestruje | Nowe rozmowy |
| --- | --- | --- |
| Wybrane czaty (ustawienie domyślne) | Tylko czaty dodane ręcznie | Nigdy nie dodawane automatycznie |
| Folder Telegram | Rozmowy w jednym z folderów konta: rozmowy uwzględnione według nazwy, wraz z kategoriami folderu (kontakty, osoby spoza kontaktów, grupy, kanały, boty), pomniejszone o rozmowy wykluczone oraz, o ile folder to przewiduje, rozmowy zarchiwizowane | Odpowiednie czaty są dodawane natychmiast po ich uruchomieniu; czaty dodane przez Państwa do folderu w aplikacji Telegram są pobierane w ciągu godziny |
| Całe konto | Każda rozmowa, którą obserwuje dane konto | Każda nowa rozmowa, grupa, rozmowa prywatna lub bot są dodawane w momencie pojawienia się ich pierwszej aktualizacji |

- **Rodzaje źródeł** (kanały, grupy, czaty prywatne, boty) zawężają zakres trybu folderowego oraz trybu całego konta. Wybrane czaty mogą być dowolnego typu, w tym czaty prywatne i boty.
- **Wykluczone czaty** nie są nigdy rejestrowane, niezależnie od trybu pracy. W trybie folderowym i trybie całego konta wybranie opcji *„Wyklucz”* lub *„Usuń”* dla danego źródła powoduje umieszczenie go na tej liście, dzięki czemu funkcja „Zakres” nie dodaje go ponownie. Ponowne ręczne wybranie czatu (w sekcji „Źródła” lub z listy „Czaty”) powoduje usunięcie go z listy. Lista może pomieścić do 5 000 czatów; po przekroczeniu tej liczby *opcja „Usuń”* nie zostanie zaakceptowana, a czat można zamiast tego wstrzymać.
- **Własne działania** (domyślnie włączone): wiadomości wysyłane przez to konto, wprowadzone przez nie zmiany oraz naciśnięcia przycisków klawiatury odpowiedzi. Po wyłączeniu tej opcji wiadomości wychodzące i zmiany są pomijane.
- Przejście do folderu lub całego konta wymaga potwierdzenia: tryby te rejestrują prywatne rozmowy oraz wiadomości osób trzecich i powinny być stosowane wyłącznie na dedykowanym koncie. Potwierdzenie oraz każda zmiana zakresu są podpisanymi zapisami `scope.changed`.
- Czat dodane przez filtr pojawiają się jako źródła oznaczone jako *„auto”*, rejestrowane jako `scope.applied` (na początku i co godzinę) lub `source.discovered` (nowy czat podczas obserwacji). Powrót do wybranych czatów wstrzymuje rejestrację wszystkich automatycznie dodanych źródeł.

Czego te tryby nie potrafią:

- **Prywatne czaty** są szyfrowane od końca do końca między dwoma urządzeniami i nigdy nie trafiają do TgWitness, niezależnie od trybu działania.
- **Nic nie jest rejestrowane, gdy aplikacja TgWitness nie jest uruchomiona.** Po ponownym uruchomieniu aplikacja zwraca się do serwisu Telegram z prośbą o brakujące aktualizacje i ponownie sprawdza czaty, jednak serwis Telegram nie zwraca wszystkich danych po długich przerwach w działaniu. Raporty oraz plik `verify.py` przedstawiają takie okresy jako luki (patrz: [zakres pokrycia](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)).
- Początkowo wyświetlanych jest tylko pierwszych 1000 dialogów (limit określono w **sekcji „Parametry”**); starsze czaty są dodawane, gdy ponownie staną się aktywne. Wcześniejsza historia dodanego czatu nie jest pobierana — w razie potrzeby należy wykonać migawkę historii lub pełny eksport czatu.
- Warunki dotyczące folderów, które ulegają ciągłym zmianom (wyciszone, przeczytane), nie mają zastosowania: takie czaty pozostają pod obserwacją.
- **Przyciski bota wbudowane (z funkcją wywołania zwrotnego),** naciśnięte w innej aplikacji, są niewidoczne dla drugiej sesji; odpowiedź lub edycja bota zostaje zarejestrowana. Naciśnięcia klawiszy odpowiedzi są traktowane jako wiadomości wychodzące i oznaczane jako `button_press`.
- Więcej rozmów oznacza więcej zapytań. Telegram nakłada ograniczenia na konta, których aktywność uzna za nadmierną, co stanowi kolejny powód, by korzystać z dedykowanych kont.

## Zakres i wybór zdarzeń

Każdy obszar roboczy posiada własne źródła. TgWitness nie dołącza do grup, nie przyjmuje zaproszeń ani nie sporządza automatycznie listy wszystkich członków. Źródła muszą być już dostępne dla danego konta. Podczas uruchamiania moduł zbierający porównuje wybrane źródła z widocznymi rozmowami na koncie; sprawdzanych jest pierwszych 1000 rozmów, o ile nie określono inaczej w sekcji **Parametry → Czaty odczytywane z listy konta**. Brakujące źródło jest oznaczane jako **„dostęp niepotwierdzony”**, a nie zakłada się, że użytkownik został z niego usunięty.

| Kontekst | Gromadzi | Skutki wyłączenia funkcji |
| --- | --- | --- |
| Nowe wiadomości | Zwykłe dostarczone wiadomości | W przypadku późniejszych edycji lub usunięć może brakować wcześniej zarejestrowanego tekstu, z którym można by je porównać. |
| Edycje | Dostarczono zredagowane wersje wiadomości | Zmiany pośrednie nie są później odtwarzane. |
| Usunięcia | Powiadomienia o usunięciu o określonym zakresie oraz powiadomienia na poziomie konta o nieokreślonym zakresie | Powiadomienia o usunięciu nie są dodawane do dziennika. |
| Reakcje | Dostarczone migawki reakcji | Nie dodaje się oddzielnych aktualizacji dotyczących reakcji. |
| Członkostwo | Przekazywano komunikaty dotyczące usług członkowskich oraz aktualizacje dla uczestników | Uwagi dotyczące członkostwa nie są uwzględniane. |

Ustawienia mają zastosowanie do wszystkich wybranych źródeł w obszarze roboczym. Proszę zapisać formularz, aby zastosować zmiany; zmiany są rejestrowane wraz z podpisanymi wartościami „przed” i „po”. Wyłączenie kategorii nie powoduje usunięcia wcześniejszych zapisów. Ponowne włączenie tej kategorii nie powoduje uzupełnienia pominiętych aktualizacji.

Zapisy operacyjne oraz inne zdarzenia związane z obsługą grup pozostają niezależne od tych ustawień. Komunikaty serwisowe dotyczące członkostwa mogą tworzyć zapisy wiadomości, gdy funkcja członkostwa jest włączona, nawet jeśli standardowe przechwytywanie nowych wiadomości jest wyłączone. Przechwycone obiekty z Telegrama zachowują osadzone metadane; ustawienie to nie jest regułą redagowania.

**Usunięcia w czatach prywatnych i zwykłych grupach** są rejestrowane jako identyfikatory wiadomości bez przypisania do konkretnego czatu. Czaty te korzystają z jednej sekwencji identyfikatorów wiadomości dla całego konta, więc jeśli wiadomość o danym identyfikatorze została wcześniej zapisana, znany jest czat, z którego pochodzi: usunięcie jest rejestrowane w tym czacie, a `chat_resolution` wyjaśnia, w jaki sposób. Identyfikatory, które nigdy nie zostały zapisane, pozostają **usunięciami o nieokreślonym zakresie** z wyraźnie nieznanym źródłem; moduł gromadzący danych nie podejmuje żadnych domysłów. Telegram nigdy nie podaje, kto usunął wiadomość; jeśli usunięta wiadomość została wysłana przez to konto, zapis to potwierdza (`deleted_message_was_outgoing`) bez podawania nazwiska osoby, która dokonała usunięcia.

## Własne działania

Wiadomości wysyłane przez obserwowane konto są oznaczone jako `outgoing`. Informacja o edycji wiadomości wychodzącej wskazuje, że w czatach prywatnych i grupach tylko jej autor może ją edytować, natomiast posty na kanałach mogą być edytowane przez innych administratorów. Gdy wysyłana wiadomość powtarza tekst przycisku z najnowszej zapisanej klawiatury odpowiedzi w tej rozmowie, opatrzona jest oznaczeniem „`button_press`” wraz z linkiem do zapisu tej klawiatury.

Wyłączenie własnych działań dotyczy również ponownej weryfikacji w tle oraz automatycznej historii nowych czatów. Pominięte wiadomości wychodzące przesuwają pozycję ponownej weryfikacji do przodu, dzięki czemu nie mogą one blokować późniejszych wiadomości przychodzących. Wyraźnie wykonane działania w panelu oraz ręcznie zlecone migawki historii pozostają zarejestrowane.

## Tryb dochodzeniowy: dołączanie do zespołów i komunikacja z botami

**Źródła → Zakres obserwacji → Tryb dochodzeniowy** przygotowuje zakres dla dedykowanego konta, które dołącza do czatów zespołowych, uruchamia boty i wysyła do nich wiadomości: całe konto, każdy typ źródła, własne działania oraz dla każdego pojawiającego się czatu lub bota – jego profil i ostatnie 200 widocznych wiadomości. Proszę przejrzeć formularz i nacisnąć **„Zapisz zakres”**; przejście na całe konto wymaga standardowego potwierdzenia.

- **Przyciski.** Przyciski znajdujące się pod wiadomością są zachowywane wraz z nią i wyświetlane w **sekcji „Czat**”: linki, aplikacje internetowe, linki logowania, teksty do skopiowania, dane dotyczące oddzwaniania, zapytania wbudowane, prośby o podanie numeru telefonu lub lokalizacji. Linki są wyświetlane jako tekst i nigdy nie są otwierane przez panel. Gdy bot zmienia wyłącznie przyciski (np. nowy link do płatności), stanowi to nową wersję wiadomości, zarówno w przypadku aktualizacji na żywo, jak i ponownych sprawdzeń.
- **Nowe czaty i boty.** W trybie folderowym oraz trybie całego konta, **gdy pojawia się nowy czat lub bot**, zapisywane są one natychmiast po ich pojawieniu się:

  - jego profil jako rekord `source.profile`: opis bota i polecenia, tekst informacyjny dotyczący użytkownika, grupy lub kanału, członkowie, powiązany czat oraz link zaproszeniowy, o ile Telegram go udostępnia;
  - najnowsze widoczne wiadomości (do 1 000) w postaci migawki historii oznaczonej jako `new_chat`: wcześniejsze wiadomości z czatu zespołowego, do którego właśnie dołączył użytkownik, lub to, co powiedział bot, zanim obserwator zauważył czat. Wiadomości już zapisane na żywo nie są powtarzane.

  Czat, który znajdował się już na liście w momencie włączenia trybu, zostanie dodany bez zrzutów ekranu. Funkcja FloodWait wstrzymuje tę operację, a po jej zakończeniu wznawia ją; awarie są rejestrowane, a rejestrowanie czatu na żywo jest kontynuowane. - **Profile na żądanie. Czat → Profil → Zapisz profil** pozwala **teraz** zapisać bieżący profil dowolnego źródła; najnowszy profil jest wyświetlany nad wiadomościami. - **Niewidoczne.** Przyciski wbudowane (callback) naciśnięte w innej aplikacji Telegram, wyskakujące okienko lub link, którym bot odpowiada na takie naciśnięcie, a także linki zaproszeniowe używane w innej aplikacji nie docierają do TgWitness. To, co bot wysyła lub edytuje później, jest rejestrowane.

### Działanie z poziomu panelu

**W sekcji „Czat”** dodano teraz miniklient korzystający z konta Telegram wybranego obszaru roboczego:

- Proszę wpisać wiadomość w postaci zwykłego tekstu lub wybrać **opcję „Odpowiedz”** pod zapisaną wiadomością. Wysyłana wiadomość jest rejestrowana nawet wtedy, gdy zakres rejestracji nie obejmuje wysyłanych aktualizacji.
- Naciśnij **przycisk „Press”** znajdujący się pod bieżącym przyciskiem zwrotnym lub tekstowym. Serwer ponownie pobiera wiadomość i odrzuca działanie, jeśli treść wprowadzona z klawiatury różni się od zapisanej wersji. Potwierdzenia zwrotne zachowują tekst wyskakującego okienka Telegrama, flagę powiadomienia oraz adres URL; odpowiedź jest również wyświetlana pod rozmową. Adresy URL pozostają tekstem, który można zaznaczyć, i nie są otwierane automatycznie.
- Rozwiń **link „Otwórz w Telegramie**”, wprowadź `@username`, publiczny link `https://t.me/name`, `https://t.me/+invite` / `joinchat/invite` lub link do bota z `?start=parameter`, a następnie naciśnij **„Zapisz podgląd**”. Oryginalny link oraz podgląd w Telegramie są podpisywane przed dołączeniem. **Dołącz / otwórz i obserwuj**, a następnie dołącz do grupy/kanału lub otwórz użytkownika/bota, dodaj czat jako włączone źródło i wyślij `/start` do bota, podając parametr startowy. Prośba o dołączenie oczekująca na zatwierdzenie przez administratora jest rejestrowana jako oczekująca, a nie jako członkostwo.

Proszę włączyć opcję **„Rozpocznij obserwację”**, aby rejestrować przychodzące odpowiedzi na żywo. Działania w panelu działają, gdy obserwacja jest wstrzymana, jednak wówczas gwarantowane jest zapisanie wyłącznie bezpośrednich odpowiedzi. Nowo dodane źródła korzystają ze skonfigurowanego profilu/historii podczas trwania obserwacji. Gdy źródło jest wstrzymane, należy je włączyć w **sekcji „Źródła”** przed wysłaniem wiadomości lub naciśnięciem przycisków.

`interaction.preview`, `interaction.requested` i `interaction.result` to standardowe, podpisane zdarzenia dziennika uwzględniane w eksportach dowodów. Żądania identyfikują konto, wiadomość/przycisk lub rekord podglądu oraz wskazują, czy obserwacja była uruchomiona. Potwierdzenia rozróżniają wynik pomyślny, odrzucenie, zatwierdzenie w toku oraz wynik nieznany. Przerwane żądanie mogło dotrzeć do Telegramu: proszę sprawdzić czat przed rozpoczęciem nowej czynności. Ponowne użycie identyfikatora żądania powoduje pobranie zapisanego potwierdzenia bez powtarzania akcji, również po ponownym uruchomieniu. Panel zachowuje ten identyfikator po otrzymaniu niejednoznacznej odpowiedzi dotyczącej tej samej akcji w trakcie bieżącej sesji na stronie. Zachowuje go również, gdy odświeżenie widoku nie powiedzie się po pomyślnym wykonaniu akcji: potwierdzenie pozostaje widoczne, a ponowne kliknięcie powoduje jego pobranie. Wywołania zwrotne i RPC typu „join” mają jedną próbę wykonania; operacje odczytu z możliwością ponownej próby zachowują skonfigurowaną politykę ponownych prób. Natychmiastowe przełączenie czatów powoduje wyczyszczenie wersji roboczej i adresata odpowiedzi oraz wyłącza wysyłanie do momentu załadowania nowej rozmowy.

Ten miniklient obsługuje przyciski tekstowe i przyciski wywołania zwrotnego. Aplikacje internetowe, żądania logowania/numeru telefonu/lokalizacji, płatności, zapytania wbudowane oraz załączniki nadal wymagają klienta Telegram; zapisane metadane przycisków pozostają widoczne. Nowe elementy sterujące wykorzystują tekst w języku angielskim.

## Poziomy weryfikacji

Ponowne sprawdzanie polega na ponownym zwróceniu się do serwisu Telegram z prośbą o przesłanie pominiętych wiadomości, zmian oraz wiadomości, których serwis już nie udostępnia. Źródła oznaczone gwiazdką są źródłami **priorytetowymi** i domyślnie są ponownie sprawdzane co 15 minut; wszystkie pozostałe źródła – co 6 godzin. Wybrane czaty są domyślnie traktowane jako źródła priorytetowe, natomiast czaty dodane poprzez folder lub całe konto – jako źródła standardowe. W każdym cyklu ponownej weryfikacji sprawdzanych jest maksymalnie 30 źródeł, a pozostałe czekają do następnej minuty; po ponownym nawiązaniu połączenia źródła priorytetowe są sprawdzane w pierwszej kolejności. Oba interwały ustawia się w sekcji Źródła → Ustawienia rejestrowania → Ponowna weryfikacja (wartość 0 wyłącza dany poziom) i są one rejestrowane jako `recheck.changed`.

Brakujące wiadomości są pobierane od miejsca, w którym zakończyło się poprzednie przejście, przy czym maksymalna liczba **nowych wiadomości**na jedno przejście jest określona w sekcji **Parametry → liczba nowych wiadomości na ponowne sprawdzenie** (domyślnie 1 000). Po dłuższej przerwie ponowne sprawdzanie wypełnia zatem całą lukę, nawet jeśli najpierw zapisano wiadomości na żywo nowsze niż ta luka. Czat, który wciąż nadrabia zaległości, jest ponownie sprawdzany w następnej minucie zamiast czekać na swój interwał poziomu; `recheck.completed` wyświetla `continues_after`, dopóki proces nie zostanie zakończony.

Porównania obejmują treść wiadomości, podmioty, klawiatury (w tym usunięcia) oraz treść i tożsamość załączników. Sama zmiana skrótów dostępu do plików lub odwołań do plików nie stanowi edycji, podobnie jak elementy uzupełniane automatycznie przez Telegram: ładowanie podglądu linku, wyświetlenia relacji, płatne materiały multimedialne odblokowane przez to konto oraz potwierdzenie otrzymania faktury. Każda zapisana wersja w sekcji „Czat” zawiera link do pełnego wpisu w dzienniku, w tym metadanych multimediów.

## Historia wiadomości i przypisanie autorstwa

Załóżmy, że narzędzie rejestrujące odnotowuje komunikat „Spotkanie o godz. 10:00”, następnie widzi komunikat „Spotkanie o godz. 11:00”, a potem otrzymuje powiadomienie o usunięciu. Dodaje ono trzy odrębne zapisy. Oryginalny tekst pozostaje, edycja stanowi oddzielną wersję, a powiadomienie odnotowuje, że zaobserwowano usunięcie.

Jeśli gromadzenie danych rozpoczęło się po zniknięciu pierwszej wersji, tekst ten jest niedostępny. Jeśli podczas przerwy w działaniu serwisu nastąpiło kilka zmian, zapisane mogą zostać jedynie wersje zaobserwowane później. Powiadomienie o usunięciu nie pozwala na odzyskanie treści, które nigdy nie zostały zarejestrowane.

Nadawca wiadomości niekoniecznie jest jej edytorem. Aplikacja Telegram zazwyczaj nie podaje tożsamości osoby, która usunęła wiadomość, ani dokładnego czasu usunięcia. Nieznani uczestnicy pozostają nieznani. Migawki reakcji i aktualizacje dotyczące uczestników zawierają wyłącznie liczby oraz tożsamości, które aplikacja Telegram udostępnia danemu kontu.

Numery sekwencyjne odzwierciedlają kolejność obserwacji. Sygnatura czasowa UTC narzędzia zbierającego danych odpowiada jego zegarowi lokalnemu; sygnatura czasowa źródła z aplikacji Telegram jest przechowywana oddzielnie, o ile została dostarczona. Żadna z nich nie stanowi niezależnej, wiarygodnej sygnatury czasowej.

## Migawki historyczne

Funkcja „snapshot” pobiera najnowsze widoczne wiadomości z włączonego źródła, maksymalnie 500 na jedno żądanie. Wyniki są oznaczane jako obserwacje historyczne. Mogą one pokrywać się z danymi zbieranymi na bieżąco, a powtarzające się obserwacje są przechowywane jako oddzielne zapisy.

Zrzuty ekranu są zgodne z polityką dotyczącą załączników, ale pozostają oddzielone od przełączników zdarzeń na żywo. Nie odtwarzają one usuniętych wiadomości ani pominiętych wersji pośrednich. Można złożyć wniosek o ich utworzenie w trakcie wstrzymania; wszelkie załączniki umieszczone w kolejce pozostają w oczekiwaniu do momentu rozpoczęcia obserwacji i uruchomienia modułu pobierania.

## Obsługa załączników

Pobieranie załączników jest domyślnie włączone i zostaje wstrzymane, gdy wolne miejsce na dysku spadnie poniżej 1 GiB. Moduł zbierający rejestruje obserwację wiadomości i zadanie pobierania łącznie. Zadanie zachowuje oryginalny deskryptor multimediów oraz zasady dotyczące rozmiaru, dzięki czemu załącznik poddany późniejszej edycji nie zostanie zastąpiony bez powiadomienia.

Pobieranie rozpoczyna się po przechwyceniu wiadomości. Zakończone pobieranie tworzy rekord `media.saved` wraz z jego skrótem SHA-256 i liczbą bajtów. Operacje pominięte, nieudane, ponowione oraz przerwane mają odrębne wyniki. Zadanie umieszczone w kolejce nie stanowi dowodu, że plik został zachowany. Zakończony plik musi również odpowiadać liczbie bajtów podanej w oryginalnym deskryptorze załącznika . Krótka lub nieoczekiwanie długa odpowiedź nie jest rejestrowana jako zachowany plik multimedialny.

Limity są ustalane **dla poszczególnych typów**: zdjęcia, filmy, pliki GIF i animacje, okrągłe wiadomości wideo, wiadomości głosowe, muzyka i pliki audio, naklejki oraz pliki. Każdy typ można wyłączyć i ma on własny limit rozmiaru od 1 do 2 000 MiB; nowe obszary robocze rozpoczynają się od 20 MiB dla zdjęć, 100 MiB dla filmów, 50 MiB dla plików, plików audio i okrągłych filmów, 20 MiB dla wiadomości głosowych i plików GIF oraz 5 MiB na naklejki. W nowych obszarach roboczych pliki GIF i naklejki są domyślnie wyłączone do momentu ich włączenia. Obszary robocze z zasadami zapisanymi przed wprowadzeniem limitów dla poszczególnych typów zachowują wszystkie typy włączone i utrzymują jeden limit dla każdego typu. *Maksymalny rozmiar pliku* ustala się jednocześnie dla wszystkich typów. Wyłączenie danego typu powoduje utworzenie rekordu `media.skipped`; pliki o nieznanym rozmiarze lub przekraczające limit nie są pobierane. Duże pliki otrzymują dodatkowy czas pobierania w oparciu o ich rozmiar i prędkość bazową wynoszącą 256 KiB/s. Zadania pozostają aktywne po ponownym uruchomieniu, jednak wygasłe odwołania, utrata dostępu lub usunięte pliki mogą nadal uniemożliwić ich odzyskanie. Zadania oczekujące zachowują zapisany dla nich limit, więc podwyższony limit ma zastosowanie wyłącznie do nowych plików. Wyłączenie typu lub obniżenie jego limitu powoduje również pominięcie wykluczonych plików oczekujących, z których każdy posiada rekord typu „`media.skipped`”; wyłączenie pobierania wstrzymuje działanie kolejki do momentu ponownego włączenia tej funkcji.

## Wstrzymanie, zablokowanie, rozłączenie i ponowne uruchomienie

| Czynność lub stan | Efekt |
| --- | --- |
| Zmień obszar roboczy | Zmienia widok panelu; pozostałe narzędzia do gromadzenia danych zachowują swój stan. |
| Zablokuj panel lub zamknij kartę | Serwer i proces monitorowania pozostają uruchomione. |
| Wstrzymanie obserwacji | Zatrzymuje działanie tego modułu zbierającego i zachowuje zadania związane z załącznikami znajdujące się w kolejce. |
| Wyłącz źródło | Wyłącza przyszłe przechwytywanie w określonym zakresie; zadania związane z multimediami oczekujące w kolejce na tę funkcję są wstrzymywane na czas jej wyłączenia. |
| Usuń źródło | Narzędzie pomija tę platformę jako źródło i usuwa profile użytkowników; zapisane już dane pozostają w dzienniku, do którego można jedynie dodawać nowe wpisy. Załączniki, które wciąż oczekują na przetworzenie, są rejestrowane jako nieudane (`source_removed`). W trybie folderowym i trybie całego konta są one również pomijane. |
| Zmiana trasy połączenia | Wymaga wstrzymania działania, zamyka stare sesje klientów i anuluje niedokończone logowanie. |
| Zatrzymanie procesu w języku Python | Narzędzie zatrzymuje działanie wszystkich obszarów roboczych; w trybie offline nie są rejestrowane żadne obserwacje. |
| Ponowne uruchomienie po zakończeniu aktywnej obserwacji | Próba wznowienia zapisanego zakresu przy użyciu zapisanej sesji. Ręczne wstrzymanie usuwa ten zamiar. |

Moduł zbierający rejestruje wykryte rozłączenia, ponowne próby połączenia, błędy, uruchomienia/zatrzymania oraz sygnały kontrolne. Krótkie przerwy w połączeniu mogą zostać pominięte podczas okresowych kontroli łączności. Po ponownym uruchomieniu wysyłane są żądania dotyczące pominiętych aktualizacji, począwszy od zapisanej pozycji aktualizacji, a obserwowane czaty są okresowo ponownie sprawdzane; patrz [format dowodów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#durable-collection-and-process-receipts-02). Migawka dostarcza kontekstu; nie stanowi ona dowodu na to, że luka została uzupełniona.

## Izolacja i weryfikacja kont

Każdy obszar roboczy posiada własny dziennik, uprawnienia, klucz podpisujący, zasady oraz kolejkę. Tylko aktywny klient danego obszaru roboczego może wprowadzać obserwacje na bieżąco. Klienci, których wnioski zostały odrzucone, oczekują na rozpatrzenie, zostali zastąpieni lub przeprowadzają test połączenia, nie mogą wprowadzać aktualizacji na bieżąco do dziennika tego obszaru roboczego. Różne konta mogą obserwować tę samą grupę, jednak ich dzienniki pozostają oddzielne.

Każde zdarzenie zawiera poprzedni skrót oraz podpis Ed25519. Eksport obejmuje cały dziennik obszaru roboczego poprzez stały numer sekwencyjny. Filtry panelowe nie filtrują eksportu; gromadzenie danych może trwać poza jego granicami w trakcie przygotowywania eksportu.

**Dziennik weryfikacyjny** sprawdza ciąg zdarzeń i podpisy w ramach wyświetlanego zakresu. Jego wynik jest kasowany w momencie zmiany obszaru roboczego, a panel identyfikuje nowe rekordy dodane po przeprowadzeniu kontroli. Eksport do formatu ZIP pozwala również zweryfikować zebrane pliki multimedialne.

Ważny podpis potwierdza integralność w odniesieniu do zaufanego klucza, a nie do pochodzenia z serwisu Telegram ani prawdziwości treści. Należy niezależnie przechowywać odciski palców i punkty kontrolne. Proszę zapoznać się z [modelem dowodowym](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/), [codziennymi operacjami](https://phishdestroy.github.io/TgWitness/pl/docs/reference/operations/) oraz [procedurą akceptacji na żywo](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) w celu zapoznania się z wymaganiami dotyczącymi zaufania i dostarczania danych.
