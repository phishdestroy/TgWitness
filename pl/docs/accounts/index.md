# Podłącz konto

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/accounts/

Jedno środowisko pracy obejmuje jedno konto, jego dziennik oraz klucz podpisujący.

## Wybierz sposób logowania

Proszę otworzyć **konta**, dodać obszar roboczy i otworzyć jego ustawienia połączenia. Do obserwacji należy używać dedykowanego konta.

- **Kod QR:** proszę zeskanować go w ustawieniach urządzenia w aplikacji Telegram i potwierdzić nowe logowanie.
- **Numer telefonu:** proszę wprowadzić numer, kod wysłany przez Telegram oraz hasło do weryfikacji dwuetapowej, jeśli jest ona włączona.
- **Import sesji:** proszę zaimportować obsługiwany plik sesji lub dane z aplikacji Telegram Desktop, które należą do Państwa.

Proszę wybrać wbudowany profil API lub wprowadzić własny identyfikator API oraz skrót. Profil API identyfikuje klienta; nie służy on do logowania się na konto ani do zapewnienia anonimowości połączenia.

**Czy potrzebują Państwo najpierw serwera proxy?**

Przed zalogowaniem się mogą Państwo [wybrać i przetestować trasę połączenia](https://phishdestroy.github.io/TgWitness/pl/docs/proxies/). Każde konto ma swoją własną trasę.

## Wybierz, co chcesz monitorować

1. Proszę otworzyć listę źródeł i wybrać potrzebne czaty, grupy lub kanały.
2. Przed rozpoczęciem obserwacji prosimy o zapoznanie się z ustawieniami gromadzenia danych, w tym plików multimedialnych.
3. Uruchom narzędzie do gromadzenia danych i sprawdź jego połączenie oraz ostatnią aktywność.

Konto musi mieć dostęp do źródła. Różne role mogą widzieć różne zdarzenia; dziennik odzwierciedla to, co otrzymało dane konto.

W przypadku sprawy obejmującej całe konto należy skorzystać z opcji **Źródła → Zakres obserwacji → Tryb dochodzeniowy**, sprawdzić ustawienia i nacisnąć **przycisk Zapisz zakres**. [Kompletny przewodnik po dochodzeniu](https://phishdestroy.github.io/TgWitness/pl/docs/cases/) obejmuje wszystkie widoczne typy czatów, starą historię, profile użytkowników, odniesienia między czatami oraz przekazywanie dowodów.

## Proszę sprawdzić całą ścieżkę

W grupie testowej, którą Pan/Pani kontroluje, proszę wysłać unikalną wiadomość z innego konta, edytować ją, a następnie usunąć. Proszę potwierdzić wszystkie trzy zdarzenia w dzienniku, a następnie [wyeksportować i zweryfikować](https://phishdestroy.github.io/TgWitness/pl/docs/exports/) zapis.

Status „połączono” potwierdza nawiązanie połączenia. Zarejestrowana wiadomość testowa potwierdza, że dane zdarzenie dotarło do tego obszaru roboczego.

## Dodaj kolejne konto

Proszę utworzyć kolejne środowisko pracy w **sekcji „Konta”** i powtórzyć proces konfiguracji. Proszę zachować odcisk klucza podpisu każdego konta, aby móc później zidentyfikować eksportowane dane.
