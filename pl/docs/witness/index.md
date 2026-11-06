# Skonfiguruj bota Witness

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/witness/

Osobny proces sprawdza Twój dziennik i publikuje podpisane punkty kontrolne na kanale.

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

Utwórz bota przez BotFather i pozwól mu publikować na Twoim kanale. Świadka uruchom gdzie indziej: inny host, najlepiej prowadzony przez kogoś innego, jest wart znacznie więcej niż drugi proces obok kolektora.

## Trzy kroki w sekcji „Dodatki”

1. **Dostęp tylko do odczytu.** **Dodatki → Niezależny świadek**, utwórz token i zapisz plik. Czyta punkty kontrolne i stan, nic więcej.
2. **Kanał i interwał.** Kanał Telegram albo webhook Discorda, plus adres kolektora dostępny dla świadka. Zapisz plik ustawień.
3. **Uruchomienie.** Połóż `witness.json`, `witness-token.txt` i `bot-token.txt` razem na hoście świadka i uruchom:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Poczekaj na pierwszy podpisany post na kanale, potem zapisz odcisk świadka w bezpiecznym miejscu.

Wolisz Discorda? Zapisz URL webhooka jako `discord-webhook.txt`. Jeden świadek publikuje w jednym miejscu; długie kontrole przychodzą na Discorda jako plik.

## Proszę wybrać częstotliwość publikacji

Publikowanie każdej kontroli daje regularny zewnętrzny zapis: co pięć minut to około 288 postów dziennie na przestrzeń. Ustawienia zaawansowane pozwalają publikować tylko przy zmianach lub problemach, używać proxy albo własnego Bot API.

**Co właściwie poświadcza ten bot?**

Prosi kolektor o podpisany punkt kontrolny, sprawdza go oczekiwanym kluczem i prowadzi własny podpisany dziennik, także z pominiętymi i odrzuconymi odpowiedziami.

Sprawdza stan dziennika, a nie śledzi Telegrama sam. Do tego przeprowadź kontrolowany test dostarczania.

## Proszę sprawdzić dowody później

Zachowaj dziennik świadka, posty i odciski. [Jak je sprawdzić](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/#verify) wobec eksportu kolektora.
