# Dowiedz się, co poszło nie tak

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/troubleshooting/

Zacznij od objawu i sprawdzaj po jednej rzeczy.

## Panel prosi o token

Chodzi o token panelu z pliku, który wskazał launcher. Docker: `docker compose exec tgwitness cat /data/panel-token.txt`. To nie kod z Telegrama, nie token bota i nie token świadka.

## Telegram nie nawiązuje połączenia

Uruchom test połączenia. Przy publicznym proxy wybierz inne i zapisz. Sprawdź typ proxy i format sekretu. Odświeżenie list samo nie zmienia trasy.

## Połączenie nawiązane, ale brak nowych wiadomości

1. Czy obserwacja działa, i to we właściwej przestrzeni?
2. Czy źródło jest wybrane i widoczne dla tego konta?
3. Wyślij unikalną wiadomość w grupie testowej i wyszukaj ją.
4. Poszukaj w dzienniku przerw lub błędów Telegrama.

W cichym czacie po prostu nie ma nic nowego. Jeśli liczy się kompletność, przeprowadź kontrolowany test dostarczania.

## FloodWait lub przerwa po ponownym uruchomieniu

FloodWait to Telegram mówiący „zwolnij”. Przeczekaj i zmniejsz obciążenie, ponowne łączenie nie pomoże. Po restarcie TgWitness nadrabia to, co Telegram jeszcze ma; reszta to luka, więc ją zapisz.

## Bot został skonfigurowany, ale nie publikuje żadnych wpisów

Czy świadek działa, czy bot może publikować na kanale, czy dociera do kolektora i Bot API? Poszukaj w jego dzienniku nieudanych publikacji. Odpytanie po stronie kolektora nie znaczy, że post wyszedł.

## Gdzie znajduje się integracja z tokenem GitHub?

**W planach.** Sekcja „Dodatkowe informacje” opisuje proponowany proces tworzenia rozgałęzień oraz weryfikacji kompilacji. Obecnie nie ma formularza tokenu GitHub ani automatycznego potwierdzenia, że uruchomiona instalacja jest zgodna z repozytorium. Proszę zapoznać się z [aktualnym statusem funkcji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/features/).

Zgłaszasz błąd? Wersja, system, kroki i błąd bez danych osobowych. Nigdy nie wrzucaj sesji, tokenów, prywatnych wiadomości ani katalogu danych do publicznego issue.
