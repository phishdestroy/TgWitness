# Dostęp i uprawnienia

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/

Proszę określić zakres dostępu do kont i czatów, wybrać uprawnienia, ograniczyć liczbę sesji i adresów IP oraz cofnąć dostęp.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/pl/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

Można przyznać recenzentowi dostęp do jednej rozmowy, analitykowi uprawnienie do eksportowania sprawy lub operatorowi kontrolę nad wybranymi kontami. Każda osoba otrzymuje własny token. Główny token panelu pozostaje w posiadaniu administratora.

[Konfiguracja konta](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/) · [Trasy połączeń](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/) · [Model bezpieczeństwa](https://phishdestroy.github.io/TgWitness/pl/docs/reference/security/)

## Dwa obszary zastosowań, dwa różne zadania

**Zakres gromadzenia danych** określa, co jest rejestrowane na danym koncie: wybrane czaty, folder w aplikacji Telegram lub całe konto. **Zakres dostępu** określa, które z tych zarejestrowanych kont i czatów mogą być przeglądane i wykorzystywane przez inną osobę. Przyznanie dostępu nie powoduje dołączenia do czatu w aplikacji Telegram, rozpoczęcia gromadzenia danych ani przyznania uprawnień do konta w aplikacji Telegram.

Uprawnienie dostępu może obejmować wybrane obszary robocze, wybrane czaty w ich obrębie, wszystkie obszary robocze lub wszystkie konta w [grupie kont](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#bulk-import-and-account-groups). Uprawnienie do **wszystkich obszarów roboczych, w tym tych dodanych później,** obejmuje również przyszłe konta. Uprawnienie do grupy obejmuje również konta dodane do tej grupy w późniejszym czasie. Należy wyraźnie wybrać obszary robocze, jeśli sprawa ma być ograniczona wyłącznie do nich.

## Przyznaj komuś dostęp

1. Zaloguj się jako główny administrator i otwórz sekcję **„Dostęp**”.
2. W sekcji **„Przyznaj komuś dostęp**” proszę wpisać imię i nazwisko, które będzie Pan/Pani w stanie rozpoznać w dzienniku.
3. Proszę wybrać przestrzenie robocze oraz, w razie potrzeby, poszczególne czaty.
4. Proszę wybrać, co dana osoba może zrobić. Zawsze należy uwzględnić opcję **„Wyświetl**”.
5. Proszę ustawić termin ważności, limity logowań/sesji oraz dozwolone adresy zgodnie z potrzebami.
6. Proszę kliknąć **„Utwórz dostęp**”. Proszę skopiować token teraz: zostanie on wyświetlony tylko raz.
7. Proszę przesłać adres panelu i token w wiadomości prywatnej. Odbiorca wprowadza ten token na standardowej stronie logowania; nie potrzebuje on Państwa głównego tokenu panelu ani sesji w Telegramie.

Proszę otworzyć panel z wygenerowanym tokenem w osobnej sesji przeglądarki i sprawdzić widoczne czaty oraz dozwolone działania przed przekazaniem go.

## Proszę wybrać uprawnienia

Aby przeprowadzić publiczną prezentację zawierającą wyłącznie tekst, należy skorzystać z **opcji** **„Publiczna prezentacja”** zamiast zwykłego dostępu recenzenta. Wyświetla ona wyraźnie wybrane kanały publiczne, zachowane edycje i usunięcia oraz podpisane statystyki, przy czym pola autora są zamazane, a pliki zamknięte na granicy API. [Utwórz i zweryfikuj prezentację](https://phishdestroy.github.io/TgWitness/pl/docs/reference/showcase/).

| Uprawnienia | Możliwości narzędzia |
| --- | --- |
| `view` | Dostęp do odczytanych rozmów, przechwyconych wiadomości, profili, plików oraz przefiltrowanych wpisów w dzienniku. Zawsze w zestawie. |
| `export` | Dopuszczalny jest eksport historii czatów i dossier. Eksport dowodów z całego obszaru roboczego wymaga dostępu do całego obszaru roboczego. |
| `sources` | Zarządzanie źródłami, migawkami i przechwytywaniem profili. Dostęp ograniczony do czatów pozwala na działanie wyłącznie w ramach dozwolonych czatów; funkcje wykrywania źródeł w całym koncie oraz ustawienia zakresu pozostają wyłączone. |
| `collect` | Uruchomienie lub zatrzymanie modułu zbierającego. Wymagany jest dostęp do całego obszaru roboczego, ponieważ proces gromadzenia danych ma wpływ na konto. |
| `interact` | Proszę wykonywać obsługiwane interakcje w aplikacji Telegram w ramach zakresu dostępu. Dostęp ograniczony do czatu nie pozwala na korzystanie z podglądu linków dla całego konta. |
| `settings` | Zmiana ustawień gromadzenia danych, znaczników czasu, powiadomień, kopii poza serwerem oraz parametrów. Wymagany jest dostęp do całego obszaru roboczego. |
| `account` | Zaloguj się lub wyloguj z serwisu Telegram oraz zarządzaj trasami połączeń. Wymagany jest dostęp do całego obszaru roboczego. |
| `board.read` | Notatki z tablicy spraw należy przeglądać wyłącznie w ramach dozwolonego obszaru roboczego i czatów. |
| `board.write` | Dodawaj zakładki, zaznaczenia, fragmenty, komentarze oraz statusy otwarcia/przeglądu. Wymagana jest również funkcja ``board.read``. |
| `board.manage` | Zarządzaj zbiorami, ostatecznymi statusami zespołu oraz kartami innych uczestników. Wymagane są również uprawnienia do odczytu i zapisu w tablicy. |

Uprawnienia i zakres są sprawdzane łącznie. Zaznaczenie uprawnienia nie powoduje otwarcia innych czatów ani odblokowania operacji obejmującej cały obszar roboczy w przypadku dostępu ograniczonego do konkretnego czatu. W przypadku eksportu równoległego uprawnienie musi obejmować eksportowany czat na każdym wybranym koncie. Przyznane uprawnienie nie pozwala na tworzenie nowych uprawnień, zarządzanie sesjami innych osób ani otwieranie konsoli administratora.

### Trzy przydatne konfiguracje

| Osoba | Zakres | Uprawnienia |
| --- | --- | --- |
| Recenzent | Zapisane rozmowy z jednej sprawy | `view` |
| Analityk przygotowujący przekazanie obowiązków | Czatów do zbadania i wyeksportowania | `view`, `export`; proszę dodać `interact` wyłącznie w przypadku, gdy działania mają być prowadzone za pośrednictwem Telegrama |
| Operator gromadzenia danych | Wybrane kompletne obszary robocze | `view`, `sources`, `collect`; proszę dodać `settings` lub `account` wyłącznie w razie potrzeby |

Ustawienia domyślne formularza dostępu obejmują również tablicę sprawy: recenzent ma uprawnienia do odczytu, analityk do odczytu i zapisu, a operator do zarządzania. Ustawienia domyślne można edytować, a istniejące uprawnienia nie są automatycznie rozszerzane. Zobacz [sekcję „Tablica sprawy”](https://phishdestroy.github.io/TgWitness/pl/docs/reference/case-board/), aby zapoznać się z dziedziczonymi zakresami czatów i ustawieniami prywatności eksportu.

## Ograniczenia i sesje

| Kontekst | Jak to działa |
| --- | --- |
| Sesje równoległe | Należy ograniczyć liczbę jednoczesnych sesji do 1–100. Po osiągnięciu limitu należy odmówić kolejnego logowania lub zakończyć najstarszą sesję. |
| Dopuszczalne logowanie | Należy ograniczyć liczbę pomyślnych użyć tokenu do rozpoczęcia sesji. Istniejące sesje nie są kończone tylko dlatego, że wykorzystano ostatnie dozwolone logowanie. |
| Ważne do | Bezwzględny termin wygaśnięcia dostępu. Użytkownik z wygasłym dostępem nie może się zalogować ani nadal wysyłać żądań. |
| Minuty bez aktywności | Limit czasu bezczynności sesji, od 5 minut do 30 dni. Pomyślne żądania przedłużają ten czas; otwarty panel może utrzymać swoją aktywność poprzez wysyłanie zapytań. |
| Dopuszczalne adresy | Proszę zaakceptować określone adresy IP lub podsieci CIDR. Proszę pozostawić pole puste, aby zezwolić na dowolny adres, o ile nie włączono powiązania z pierwszym logowaniem. |
| Powiązanie z pierwszym logowaniem | Pierwsze pomyślne zalogowanie się ustala adres dozwolony dla tego dostępu. |

Adres IP to adres klienta widoczny dla aplikacji. W przypadku korzystania z serwera proxy odwrotnego lub tunelu należy sprawdzić adres wyświetlany w sekcji **„Otwarte sesje”** przed zastosowaniem reguł opartych na adresach IP: w przeciwnym razie może się wydawać, że kilku użytkowników korzysta z tego samego adresu serwera proxy.

## Zmiana lub cofnięcie dostępu

Edytuj wpis w sekcji **„Przyznany dostęp”**, aby zmienić jego zakres, uprawnienia lub ograniczenia. Zmiany zakresu i uprawnień są sprawdzane przy kolejnych żądaniach, w tym przy żądaniach pochodzących z sesji, które są już otwarte. Cofnięcie dostępu kończy sesje i uniemożliwia korzystanie z wydanego tokenu. **Funkcja „Otwarte sesje”** pozwala również administratorowi zakończyć pojedynczą sesję bez cofania całego dostępu.

Zapisane kopie eksportu zachowują informacje o twórcy, obszarze roboczym, zakresie czatu oraz wymaganych uprawnieniach. Osoba, której przyznano dostęp, może wyświetlać lub pobierać własne kopie tylko tak długo, jak długo te uprawnienia są ważne; kopie zawierające Case Board wymagają również uprawnienia „`board.read`”. Administrator może pobrać wszystkie kopie. Starsze kopie bez tych metadanych oraz pakiety grupowe są dostępne wyłącznie dla administratora. Bilety pobierania i przygotowane odpowiedzi plikowe ponownie sprawdzają uprawnienia po przygotowaniu pliku, przed wysłaniem jego danych.

Cofnięcie uprawnień nie pozwala na odzyskanie plików, które ktoś już pobrał. Wylogowanie się, zablokowanie panelu lub zakończenie sesji nie zatrzymuje działającego kolektora.

## Co widzi administrator

Recenzenci i analitycy otrzymują informacje o postępach w gromadzeniu danych bez punktów końcowych proxy, diagnostyki puli, ścieżek serwerowych ani surowych błędów połączenia. Diagnostyka połączeń wymaga uprawnienia `account` w całym obszarze roboczym. Odczyt powiadomień, kopii poza lokalizacją oraz ustawień parametrów wymaga uprawnienia `settings`.

Pełne ciągi znaków User-Agent z przeglądarki nie są zachowywane w sesjach dostępu. Aktualizacja usuwają je również z modyfikowalnej pamięci podręcznej sesji. Dziennik procesu panelu maskuje literały adresów IP, poświadczenia URL oraz oznaczone tajemnice. Lokalne dzienniki usług oraz wcześniej podpisane zapisy dziennika nie są przepisywane. Reguły dostępu i podpisane zapisy logowania nadal wykorzystują adres klienta.

### Wymień klucz główny

Użyj **Access → Moje limity → Ponowne wydanie klucza administratora** lub uruchom `tgwitness token rotate` z zarządzanej instalacji podczas działania panelu. Wszystkie istniejące sesje przeglądarki zostaną zakończone, w tym sesje otwarte za pomocą tokenów współpracowników. Przeglądarka wysyłająca żądanie otrzyma nową sesję; zapisz nowy klucz administratora przed jego ukryciem. Wydane tokeny współpracowników pozostają ważne do momentu ich oddzielnego unieważnienia. W przypadku instalacji korzystającej z `TGWITNESS_TOKEN` należy zmienić to ustawienie środowiskowe i ponownie uruchomić system.

### Granice żądań i serwerów proxy

API dopuszcza do 600 żądań na minutę na adres IP klienta. Dziesięć odrzuconych autoryzacji w ciągu minuty uruchamia wykładniczy okres blokady, trwający od jednej sekundy do pięciu minut. Nieudana próba po upływie okresu blokady wydłuża go; dziesięć minut bez nieudanej próby resetuje eskalację. Odrzucenia zwracają kody HTTP 429 i `Retry-After`. Limity są przechowywane w pamięci i współdzielone między obszarami roboczymi w ramach jednego procesu panelu; ponowne uruchomienie je kasuje. Strumienie na żywo są ograniczone do czterech na token nośny i 32 dla procesu panelu. Otwarcie strumienia również zużywa limit żądań API.

Treści żądań mają 60-sekundowy limit czasu na odbiór (8 sekund dla MCP). Każda aplikacja ogranicza niedokończone treści do 32 żądań i 64 MiB zarezerwowanego limitu trasy. Treści przekraczające limit zwracają kod 413, treści, dla których upłynął limit czasu, zwracają kod 408, a wyczerpanie pojemności na treści zwraca kod 503 wraz z parametrem „`Retry-After`”.

Przekierowane nagłówki IP są ignorowane, chyba że rzeczywisty partner TCP należy do `TGWITNESS_TRUSTED_PROXIES` (adresy IP lub CIDR oddzielone przecinkami). Ustaw `TGWITNESS_PROXY_HEADER` na `x-forwarded-for` lub `cf-connecting-ip`. XFF jest przechodzony od najbliższego serwera proxy w kierunku pierwszego niezaufanego partnera. Nieprawidłowe lub zduplikowane metadane zaufanych adresów są odrzucane, więc nie mogą one odziedziczyć adresu proxy znajdującego się na liście dozwolonych. Zarządzany szybki tunel ufają lokalnemu łącznikowi Cloudflare; konfiguracja w domenie własnej ufa lokalnemu serwerowi Caddy. Wdrożenia bezpośrednie domyślnie nie ufają żadnemu serwerowi proxy. Jeśli samodzielnie uruchamiasz Uvicorn, wyłącz przetwarzanie nagłówków proxy, aby ta granica otrzymała rzeczywisty węzeł równorzędny.

`TGWITNESS_PANEL_ALLOWED_IPS` ogranicza dostęp do panelu, w tym dostęp administratora, do wymienionych adresów IP lub zakresów CIDR. Sonda tożsamości routingu instalatora pozostaje publiczna i nie zwraca żadnych danych konta. Przed włączeniem listy dozwolonych adresów należy uwzględnić wymaganą lokalną trasę administracyjną. Przewodnik **START-HERE** dotyczący instalacji zarządzanej zawiera instrukcje dotyczące konfiguracji usługi i przywracania.

Selektor zapytania API `ws` musi identyfikować obszar roboczy w ścieżce żądania; nieznane, niezgodne i zduplikowane selektory są odrzucane z kodem 404.

Skrypty i style paneli zawierają metadane integralności SHA-384. Mapa importu obejmuje również lokalnie importowane moduły JS w przeglądarkach obsługujących integralność mapy importu. Dynamicznie generowana odpowiedź językowa jest oddzielna. Kontrole te wykrywają podstawianie zasobów w stosunku do dostarczonej strony; nie budują zaufania do zainfekowanego serwera, który może zastąpić zarówno stronę, jak i jej skróty.

**Dziennik od momentu uruchomienia** łączy logi procesowe z aktywnością dziennika z każdego obszaru roboczego: logowania, odmowy, zmiany trasy oraz działania operatorów. Jest to konsola działająca w pamięci dla bieżącego procesu, a nie trwała kopia każdej wiadomości. Często powtarzające się zdarzenia związane z wiadomościami pozostają w dzienniku, zamiast zapełniać konsolę.

Przyznawanie, zmiana i cofanie uprawnień dostępu, a także rozpoczynanie lub kończenie sesji powodują również utworzenie podpisanych wpisów w dzienniku `access.*`. Tokeny nie są uwzględniane w tych wpisach. Przyznane tokeny i poświadczenia sesji są przechowywane w postaci skrótów w zaszyfrowanym sejfie.

****Główny administrator i granica zaufania****

The main panel token remains unrestricted. Browser sign-ins with it create sessions subject to the administrator's configured session limits. Scripts sending the main token directly retain full access and are not counted as browser sessions.

This is application-level access control in one installation. All workspaces share the server process; this is not isolation from the host administrator. Keep the main token, Telegram sessions, signing keys and data directory private. A witness token is a separate checkpoint/health credential, not a panel access token.
