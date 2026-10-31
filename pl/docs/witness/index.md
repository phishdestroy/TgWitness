# Skonfiguruj bota Witness

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/witness/

Proszę zlecić oddzielnemu procesowi sprawdzenie dziennika i opublikowanie podpisanych punktów kontrolnych na Państwa kanale.

## Dwa serwery, dwa klucze podpisujące

HOST A / COLLECTOR**Konto + dziennik**

Klucz podpisujący narzędzie Telegram Session Collector

Punkt końcowy punktu kontrolnego tylko do odczytu

← proszę o podpisaną odpowiedź →

HOST B / WITNESS**Weryfikacja + archiwizacja**

Zaznaczony odcisk palca kolektora; oddzielny klucz podpisujący świadka

Własny dziennik + token bota

Witness → Telegram Bot API →**Pański kanał · podpisane posty TGW1**

Narzędzie Witness samodzielnie przeprowadza weryfikację. Dostęp kolektora ma charakter wyłącznie do odczytu. Publikacja przez bota odbywa się przy użyciu połączenia i tokenu narzędzia Witness; narzędziu Witness nie jest przyznawana żadna sesja konta.

03 / DECYZJE DOTYCZĄCE PUNKTÓW KONTROLNYCHPrzykładowe odpowiedzi

OSTATNIO PRZYJĘTE**120 wpisów**`head 9c7d…`

KOLEJNA ODPOWIEDŹ**128 wpisów**`head a4f2…`

Zatwierdzono: liczba wzrasta, podpis został zweryfikowany, a klucz jest zgodny. Świadek zachowuje tę nową granicę.

Wszystkie przykładowe odpowiedzi zakładają ważny podpis oraz przypięty klucz. Przedstawione tutaj skróty skrótów są jedynie ilustracjami. Sama większa liczba nie może stanowić dowodu na to, że cały stary prefiks pozostał niezmieniony; proszę porównać eksport z zachowanymi punktami kontrolnymi.

## Przygotowanie bota i kanału

Proszę utworzyć bota za pomocą BotFather i zezwolić mu na publikowanie postów w kanale, którym Pan/Pani zarządza. Proszę wybrać komputer lub serwer, na którym będzie działać narzędzie. Oddzielny serwer i operator zapewniają większą niezależność niż uruchomienie drugiego procesu na serwerze osoby gromadzącej dane.

## Trzy kroki w sekcji „Dodatki”

1. **Dostęp tylko do odczytu.** Otwórz **sekcję „Dodatki” → Bot na Państwa kanale**, utwórz token świadka i zapisz plik dostępu. Umożliwia to odczytanie punktów kontrolnych i stanu systemu, ale nie pozwala na przeglądanie rozmów ani sterowanie kolektorem.
2. **Kanał i interwał.** Proszę wprowadzić nazwę kanału oraz adres kolektora dostępny dla świadka. Proszę zapisać plik ustawień.
3. **Uruchomienie.** Umieść razem pliki `witness.json`, `witness-token.txt` oraz `bot-token.txt` utworzone na serwerze Witness. Proszę uruchomić poniższe polecenia w zainstalowanym środowisku projektowym.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Pobranie plików nie uruchamia narzędzia TgWitness. Proszę sprawdzić, czy w kanale pojawił się pierwszy podpisany wpis, a następnie oddzielnie zachować odcisk klucza publicznego narzędzia TgWitness.

## Proszę wybrać częstotliwość publikacji

Publikowanie każdego sprawdzenia tworzy regularny zewnętrzny zapis. W odstępach pięciominutowych oznacza to około 288 wpisów dziennie na każdy obszar roboczy. Ustawienia zaawansowane umożliwiają również publikowanie informacji o zmianach lub problemach, korzystanie z serwera proxy oraz podanie niestandardowego adresu API bota.

**Co właściwie poświadcza ten bot?**

Świadek zwraca się do podmiotu gromadzącego dane o podpisany punkt kontrolny, weryfikuje go przy użyciu oczekiwanego klucza i prowadzi oddzielny, podpisany dziennik. Rejestruje on zarówno brakujące odpowiedzi i odrzucone odpowiedzi, jak i pomyślnie przeprowadzone weryfikacje. Publikacja nadal zależy od tego, czy świadek działa i ma dostęp do interfejsu API botów serwisu Telegram.

Narzędzie to weryfikuje stan dziennika zgłoszony przez moduł zbierający dane. Nie monitoruje ono samodzielnie każdej wiadomości w Telegramie. W tym celu należy zastosować test kontrolowanego dostarczania.

## Proszę sprawdzić dowody później

Należy zachować dziennik świadków, posty z kanałów oraz niezależnie zapisane odciski palców. [Pełna procedura weryfikacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/#verify) polega na porównaniu ich z podpisanym eksportem pochodzącym od osoby gromadzącej dane.
