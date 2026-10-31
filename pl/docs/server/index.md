# Prosimy o dalsze prowadzenie tej strony

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/server/

Należy zapewnić dostępność modułu zbierającego dane oraz zachowanie integralności danych po każdym ponownym uruchomieniu.

## Proszę wybrać metodę uruchomienia

W przypadku instalacji natywnej proszę skorzystać z programu [uruchamiającego](https://phishdestroy.github.io/TgWitness/pl/docs/start/) oraz przykładów usług znajdujących się w katalogu [`deploy/`](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). W przypadku Docker proszę zainstalować Docker z Compose i uruchomić z katalogu projektu:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Domyślny panel nasłuchuje na adresie pętli zwrotnej hosta, na porcie 8787. Proszę otworzyć go lokalnie lub poprzez tunel SSH. Aby odblokować panel, należy użyć tokenu z drugiego polecenia.

## Należy zachować cały katalog danych

W przypadku instalacji natywnych stosowany jest wolumin `data/live`. W środowisku Docker wykorzystywany jest trwały wolumin `tgwitness-data`. Należy przechowywać dzienniki, sesje kont, klucze oraz stan operacyjny w jednym miejscu. Podpisany eksport stanowi przydatny dowód, jednak nie jest to pełna kopia zapasowa instalacji.

1. Należy przerwać gromadzenie danych przed wykonaniem spójnej kopii zapasowej.
2. Proszę skopiować cały katalog danych prywatnych do zabezpieczonej pamięci poza serwerem.
3. Przed skorzystaniem z kopii zapasowej należy przetestować przywracanie danych w izolowanej instalacji.

## Proszę sprawdzić po ponownym uruchomieniu

Proszę potwierdzić oczekiwane środowisko pracy i klucz, połączenie z Telegramem, wybrane źródła oraz przechwytywanie nowych wiadomości. Zapisany stan MTProto oraz funkcja nadrabiania zaległości pomagają odzyskać aktualizacje, które Telegram nadal przechowuje. Nie jest możliwe odtworzenie wszystkich wygasłych aktualizacji ani edycji usuniętych przed ich przechwyceniem.

Prawidłowe działanie kontenera oznacza, że serwer internetowy odpowiada. Należy zastosować wiadomość testową oraz kontrolę weryfikacyjną w celu oceny procesu gromadzenia danych i ich publikacji zewnętrznej.

## Proszę publikować wyłącznie to, co zamierzają Państwo opublikować

Dokumentacja wdrożeniowa zawiera przykłady wykorzystania protokołu HTTPS, polecenia dotyczące woluminów trwałych, a także instrukcje dotyczące aktualizacji i przywracania danych. Do wdrożenia udostępniono polecenia Docker; aktualny [rejestr walidacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/) określa środowiska, w których przeprowadzono rzeczywiste testy.
