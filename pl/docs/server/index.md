# Telegram · Prosimy o dalsze prowadzenie tej strony

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/server/

Utrzymuj kolektor w działaniu, a dane bezpieczne przy restartach.

## Proszę wybrać metodę uruchomienia

Natywnie: [launcher](https://phishdestroy.github.io/TgWitness/pl/docs/start/) plus szablony usług w [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, z folderu projektu:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Panel nasłuchuje na localhost:8787. Otwieraj lokalnie albo przez tunel SSH, z tokenem z drugiego polecenia.

## Należy zachować cały katalog danych

Natywnie: `data/live`. Docker: wolumen `tgwitness-data`. Dzienniki, sesje i klucze trzymaj razem. Podpisany eksport to dowód, a nie kopia zapasowa.

1. Najpierw zatrzymaj zbieranie.
2. Skopiuj cały katalog danych w bezpieczne miejsce poza hostem.
3. Spróbuj przywrócić go na osobnej instalacji, zanim mu zaufasz.

## Proszę sprawdzić po ponownym uruchomieniu

Sprawdź przestrzeń i klucz, połączenie, źródła i to, czy przychodzą nowe wiadomości. TgWitness nadrabia to, co Telegram jeszcze ma, a nie wszystko, co działo się podczas przestoju.

„Zdrowy” kontener znaczy, że serwer WWW odpowiada. Czy zbieranie działa, pokażą wiadomość testowa i świadek.

## Proszę publikować wyłącznie to, co zamierzają Państwo opublikować

HTTPS, wolumeny, aktualizacje i przywracanie są w dokumentacji wdrożenia. Co naprawdę przetestowano: [rejestr weryfikacji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/).
