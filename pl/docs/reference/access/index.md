# Dostęp i uprawnienia

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/

Proszę określić zakres dostępu do kont i czatów, wybrać uprawnienia, ograniczyć liczbę sesji i adresów IP oraz cofnąć dostęp.

Można przyznać recenzentowi dostęp do jednej rozmowy, analitykowi uprawnienie do eksportowania sprawy lub operatorowi kontrolę nad wybranymi kontami. Każda osoba otrzymuje własny token. Główny token panelu pozostaje w posiadaniu administratora.

[Konfiguracja konta](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/) · [Trasy połączeń](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/) · [Model bezpieczeństwa](https://phishdestroy.github.io/TgWitness/pl/docs/reference/security/)

## Dwa obszary zastosowań, dwa różne zadania

**Zakres gromadzenia danych** określa, co jest rejestrowane na danym koncie: wybrane czaty, folder w aplikacji Telegram lub całe konto. **Zakres dostępu** określa, które z tych zarejestrowanych kont i czatów mogą być przeglądane i wykorzystywane przez inną osobę. Przyznanie dostępu nie powoduje dołączenia do czatu w aplikacji Telegram, rozpoczęcia gromadzenia danych ani przyznania uprawnień do konta w aplikacji Telegram.

Uprawnienie to umożliwia dostęp do wybranych obszarów roboczych, wybranych czatów w ich obrębie lub wszystkich obszarów roboczych. Dostęp **do wszystkich obszarów roboczych, w tym tych dodanych później,** obejmuje również przyszłe konta. Należy wyraźnie wybrać konkretne obszary robocze, jeśli sprawa ma ograniczać się wyłącznie do nich.

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

| Uprawnienia | Możliwości narzędzia |
| --- | --- |
| `view` | Dostęp do odczytanych rozmów, przechwyconych wiadomości, profili, plików oraz przefiltrowanych wpisów w dzienniku. Zawsze w zestawie. |
| `export` | Dopuszczalny jest eksport historii czatów i dossier. Eksport dowodów z całego obszaru roboczego wymaga dostępu do całego obszaru roboczego. |
| `sources` | Zarządzanie źródłami, migawkami i przechwytywaniem profili. Dostęp ograniczony do czatów pozwala na działanie wyłącznie w ramach dozwolonych czatów; funkcje wykrywania źródeł w całym koncie oraz ustawienia zakresu pozostają wyłączone. |
| `collect` | Uruchomienie lub zatrzymanie modułu zbierającego. Wymagany jest dostęp do całego obszaru roboczego, ponieważ proces gromadzenia danych ma wpływ na konto. |
| `interact` | Proszę wykonywać obsługiwane interakcje w aplikacji Telegram w ramach zakresu dostępu. Dostęp ograniczony do czatu nie pozwala na korzystanie z podglądu linków dla całego konta. |
| `settings` | Zmiana ustawień gromadzenia danych, znaczników czasu, powiadomień, kopii poza serwerem oraz parametrów. Wymagany jest dostęp do całego obszaru roboczego. |
| `account` | Zaloguj się lub wyloguj z serwisu Telegram oraz zarządzaj trasami połączeń. Wymagany jest dostęp do całego obszaru roboczego. |

Uprawnienia i zakres są sprawdzane łącznie. Zaznaczenie uprawnienia nie powoduje otwarcia innych czatów ani odblokowania operacji obejmującej cały obszar roboczy w przypadku dostępu ograniczonego do konkretnego czatu. W przypadku eksportu równoległego uprawnienie musi obejmować eksportowany czat na każdym wybranym koncie. Przyznane uprawnienie nie pozwala na tworzenie nowych uprawnień, zarządzanie sesjami innych osób ani otwieranie konsoli administratora.

### Trzy przydatne konfiguracje

| Osoba | Zakres | Uprawnienia |
| --- | --- | --- |
| Recenzent | Zapisane rozmowy z jednej sprawy | `view` |
| Analityk przygotowujący przekazanie obowiązków | Czatów do zbadania i wyeksportowania | `view`, `export`; proszę dodać `interact` wyłącznie w przypadku, gdy działania mają być prowadzone za pośrednictwem Telegrama |
| Operator gromadzenia danych | Wybrane kompletne obszary robocze | `view`, `sources`, `collect`; proszę dodać `settings` lub `account` wyłącznie w razie potrzeby |

Są to przykłady, które można skonfigurować za pomocą pól wyboru uprawnień, a nie stałe role.

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

Proszę edytować wpis w **sekcji „Dostępy”**, aby zmienić jego zakres, uprawnienia lub ograniczenia. Zmiany zakresu i uprawnień są sprawdzane przy kolejnych żądaniach, w tym przy żądaniach pochodzących z sesji, które są już otwarte. Cofnięcie dostępu powoduje zakończenie sesji i uniemożliwia korzystanie z wydanego tokenu. Funkcja **otwartych sesji** pozwala również administratorowi zakończyć pojedynczą sesję bez konieczności cofania całego dostępu.

Cofnięcie uprawnień nie pozwala na odzyskanie plików, które ktoś już pobrał. Wylogowanie się, zablokowanie panelu lub zakończenie sesji nie zatrzymuje działającego kolektora.

## Co widzi administrator

**Dziennik od momentu uruchomienia** łączy logi procesowe z aktywnością dziennika z każdego obszaru roboczego: logowania, odmowy, zmiany trasy oraz działania operatorów. Jest to konsola działająca w pamięci dla bieżącego procesu, a nie trwała kopia każdej wiadomości. Często powtarzające się zdarzenia związane z wiadomościami pozostają w dzienniku, zamiast zapełniać konsolę.

Przyznawanie, zmiana i cofanie uprawnień dostępu, a także rozpoczynanie lub kończenie sesji powodują również utworzenie podpisanych wpisów w dzienniku `access.*`. Tokeny nie są uwzględniane w tych wpisach. Przyznane tokeny i poświadczenia sesji są przechowywane w postaci skrótów w zaszyfrowanym sejfie.

****Główny administrator i granica zaufania**** Token panelu głównego pozostaje nieograniczony. Logowanie za jego pomocą w przeglądarce tworzy sesje podlegające limitom sesji skonfigurowanym przez administratora. Skrypty wysyłające bezpośrednio token główny zachowują pełny dostęp i nie są traktowane jako sesje przeglądarki. Jest to kontrola dostępu na poziomie aplikacji w ramach jednej instalacji. Wszystkie obszary robocze współdzielą proces serwera; nie oznacza to izolacji od administratora hosta. Należy zachować poufność głównego tokena, sesji Telegramu, kluczy podpisujących oraz katalogu danych. Token świadka stanowi oddzielny punkt kontrolny/poświadczenie stanu, a nie token dostępu do panelu.
