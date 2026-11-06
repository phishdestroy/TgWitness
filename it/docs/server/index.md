# Telegram · Mantenetelo attivo

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/server/

Tenga il collector attivo e i dati al sicuro tra un riavvio e l’altro.

## Scegliere un metodo di avvio

Nativo: il [launcher](https://phishdestroy.github.io/TgWitness/it/docs/start/) più i modelli di servizio in [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, dalla cartella del progetto:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Il pannello ascolta su localhost:8787. Lo apra in locale o tramite un tunnel SSH, con il token del secondo comando.

## Conservare l’intera directory dei dati

Nativo: `data/live`. Docker: il volume `tgwitness-data`. Diari, sessioni e chiavi stanno insieme. Un’esportazione firmata è una prova, non un backup.

1. Prima fermi la raccolta.
2. Copi l’intera cartella dati in un posto sicuro, fuori dall’host.
3. Provi a ripristinarla su un’installazione separata prima di fidarsi.

## Verificare dopo il riavvio

Controlli spazio e chiave, connessione, fonti e che arrivino messaggi nuovi. TgWitness recupera ciò che Telegram ha ancora, non tutto ciò che è successo mentre era spento.

Un container «sano» significa che il server web risponde. Se la raccolta funziona lo diranno un messaggio di prova e il testimone.

## Pubblicate solo ciò che intendete pubblicare

HTTPS, volumi, aggiornamenti e ripristino sono nel riferimento di deployment. Cosa è stato davvero testato: [registro di convalida](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/).
