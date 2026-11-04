# Podłącz konto

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/accounts/

Jedna przestrzeń = jedno konto, jego dziennik i jego klucz.

## Wybierz sposób logowania

**Konta** → dodaj przestrzeń → ustawienia połączenia. Użyj do tego osobnego konta.

- **Kod QR:** zeskanuj go z ekranu Urządzenia w Telegramie i potwierdź.
- **Numer telefonu:** numer, kod, a potem hasło 2FA, jeśli je masz.
- **Import sesji:** własny plik sesji albo dane Telegram Desktop.

Użyj wbudowanego profilu API albo własnych API ID i hash. To tylko identyfikuje aplikację — nie loguje i niczego nie ukrywa.

**Czy potrzebują Państwo najpierw serwera proxy?**

Przed zalogowaniem się mogą Państwo [wybrać i przetestować trasę połączenia](https://phishdestroy.github.io/TgWitness/pl/docs/proxies/). Każde konto ma swoją własną trasę.

## Wybierz, co chcesz monitorować

1. Wybierz potrzebne czaty, grupy lub kanały.
2. Sprawdź ustawienia zbierania, w tym media.
3. Uruchom i sprawdź połączenie oraz ostatnią aktywność.

Konto musi mieć dostęp. Administratorzy i członkowie widzą co innego, dziennik pokazuje to, co dostało to konto.

Całe konto? **Źródła → Zakres obserwacji → Tryb dochodzenia**, sprawdź i kliknij **Zapisz zakres**. Pełny przewodnik: [dochodzenie na całym koncie](https://phishdestroy.github.io/TgWitness/pl/docs/cases/).

## Proszę sprawdzić całą ścieżkę

W grupie testowej wyślij wiadomość z innego konta, zedytuj ją i usuń. Wszystkie trzy zdarzenia powinny pojawić się w dzienniku. Potem [wyeksportuj i zweryfikuj](https://phishdestroy.github.io/TgWitness/pl/docs/exports/).

„Połączono” znaczy, że łącze działa. Przechwycona wiadomość testowa znaczy, że zdarzenia naprawdę docierają.

## Dodaj kolejne konto

Nowa przestrzeń w **Kontach**, te same kroki. Zapisz odcisk klucza każdego konta, żeby później odróżniać eksporty.
