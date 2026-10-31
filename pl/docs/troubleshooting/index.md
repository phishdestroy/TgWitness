# Dowiedz się, co poszło nie tak

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/troubleshooting/

Zacznij od objawu. Sprawdzaj po jednej warstwie na raz.

## Panel prosi o token

Proszę użyć tokenu panelu z pliku lokalnego wyświetlonego przez program uruchamiający. W przypadku Docker należy uruchomić `docker compose exec tgwitness cat /data/panel-token.txt`. Kod logowania do Telegrama, token BotFather oraz token obserwacyjny tylko do odczytu służą różnym celom.

## Telegram nie nawiązuje połączenia

Proszę otworzyć ustawienia połączenia i przeprowadzić test połączenia. W przypadku korzystania z publicznego serwera proxy proszę wypróbować inny wpis i wyraźnie zapisać trasę. Proszę sprawdzić typ serwera proxy oraz obsługiwany format klucza. Odświeżenie publicznej listy nie powoduje zmiany trasy konta.

## Połączenie nawiązane, ale brak nowych wiadomości

1. Proszę sprawdzić, czy obserwacja przebiega we właściwym obszarze roboczym.
2. Proszę upewnić się, że źródło zostało wybrane i jest widoczne dla tego konta.
3. Proszę wysłać nową, unikalną wiadomość w kontrolowanej grupie i wyszukać dokładnie ten tekst.
4. Proszę przejrzeć dziennik operacyjny pod kątem przerw w działaniu, opóźnień w pracy lub błędów serwisu Telegram.

Zrzuty historyczne i zdarzenia związane z nowymi wiadomościami to dwie różne kwestie. Źródło w trybie cichym można podłączyć bez generowania nowych wiadomości. W sytuacjach, gdy istotna jest kompletność danych, należy przeprowadzić test kontrolowanego dostarczania.

## FloodWait lub przerwa po ponownym uruchomieniu

Funkcja FloodWait oznacza, że aplikacja Telegram wymaga przerwy. Proszę odczekać wskazany czas i sprawdzić obciążenie związane z gromadzeniem danych; wielokrotne ponowne łączenie się nie znosi tego ograniczenia. Zapisany stan aktualizacji pomaga nadrobić zaległości po ponownym uruchomieniu, jednak wygasłe aktualizacje i niektóre okresy przerw pozostają ograniczeniami. Należy odnotować lukę w danych, zamiast traktować dziennik jako kompletny.

## Bot został skonfigurowany, ale nie publikuje żadnych wpisów

Należy upewnić się, że proces Witness faktycznie działa, bot może publikować posty na kanale, a Witness ma dostęp do kolektora oraz interfejsu API bota. Należy sprawdzić dziennik pod kątem nieudanych publikacji. Samo pomyślne odpytanie kolektora nie potwierdza opublikowania postu na kanale.

## Gdzie znajduje się integracja z tokenem GitHub?

**W planach.** Sekcja „Dodatkowe informacje” opisuje proponowany proces tworzenia rozgałęzień oraz weryfikacji kompilacji. Obecnie nie ma formularza tokenu GitHub ani automatycznego potwierdzenia, że uruchomiona instalacja jest zgodna z repozytorium. Proszę zapoznać się z [aktualnym statusem funkcji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/features/).

Zgłaszając problem, prosimy o podanie wersji oprogramowania, systemu operacyjnego, opis kroków prowadzących do błędu oraz zredagowanego komunikatu o błędzie. Prosimy nie ujawniać w publicznych zgłoszeniach informacji dotyczących sesji, tokenów, prywatnych wiadomości ani katalogu danych.
