# Rozpocznij w ciągu kilku minut

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/start/

Najpierw zapoznaj się z działającym przykładem. Następnie podłącz swoje konto.

## Zapraszamy do zapoznania się z witryną bez konieczności zakładania konta

Proszę pobrać lub sklonować projekt, zainstalować **Python 3.11 lub nowszą wersję** oraz uruchomić wersję demonstracyjną. Program uruchamiający tworzy środowisko lokalne i instaluje przypisane zależności.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

W przeglądarce otwiera się obszar roboczy zawierający fikcyjne wiadomości. Proszę otworzyć rozmowę, porównać edycję oraz sprawdzić eksport. Tryb demonstracyjny nie łączy się z aplikacją Telegram.

![Widok rozmowy w TgWitness wraz z przykładowymi wiadomościami](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Przykładowy obszar roboczy. Państwa własny dziennik zostanie utworzony oddzielnie.

## Załóż własną przestrzeń roboczą

Zakończ proces demonstracyjny, a następnie skorzystaj ze standardowego programu uruchamiającego:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Proszę otworzyć lokalny adres wyświetlony przez program uruchamiający. Jeśli pojawi się prośba, proszę wprowadzić **token dostępu do panelu** z lokalnego pliku o nazwie podanej w terminalu. Spowoduje to odblokowanie TgWitness; proces ten jest niezależny od logowania do aplikacji Telegram.

## Zapisz swoją pierwszą wiadomość

1. [Proszę podłączyć dedykowane konto w serwisie Telegram.](https://phishdestroy.github.io/TgWitness/pl/docs/accounts/)
2. Proszę wybrać grupę lub kanał, do których konto ma dostęp, a następnie rozpocząć obserwację.
3. Wyślij nową wiadomość w grupie testowej, którą Pan/Pani kontroluje, i sprawdź, czy pojawi się ona w dzienniku.

W przypadku instalacji na serwerze proszę postępować zgodnie z instrukcją [„Keep it running](https://phishdestroy.github.io/TgWitness/pl/docs/server/)”.
