# Mantenetelo attivo

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/server/

Assicurarsi che il collettore rimanga disponibile e che i suoi dati rimangano intatti anche dopo i riavvii.

## Scegliere un metodo di avvio

Per un’installazione nativa, si prega di utilizzare il [launcher](https://phishdestroy.github.io/TgWitness/it/docs/start/) e gli esempi di servizio presenti nella cartella [`deploy/`.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Per Docker, si prega di installare Docker con Compose ed eseguire il comando dalla directory del progetto:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Il pannello predefinito è in ascolto sull’indirizzo di loopback dell’host, porta 8787. Lo si può aprire localmente o tramite un tunnel SSH. Utilizzi il token fornito dal secondo comando per sbloccare il pannello.

## Conservare l’intera directory dei dati

Le installazioni native utilizzano `data/live`. Docker utilizza il volume persistente `tgwitness-data`. Conservare insieme i registri, le sessioni degli account, le chiavi e lo stato operativo. Un’esportazione firmata costituisce una prova utile, ma non rappresenta un backup completo dell’installazione.

1. Interrompa la raccolta prima di eseguire un backup completo.
2. Copiare l’intera directory dei dati privati in un archivio protetto esterno all’host.
3. Si raccomanda di testare il ripristino in un’installazione isolata prima di fare affidamento sul backup.

## Verificare dopo il riavvio

Verifichi l’area di lavoro prevista e la chiave, la connessione a Telegram, le fonti selezionate e l’acquisizione dei nuovi messaggi. Lo stato salvato di MTProto e la funzione di recupero consentono di recuperare gli aggiornamenti che Telegram conserva ancora. Non è possibile ricostruire ogni aggiornamento scaduto né una modifica cancellata prima dell’acquisizione.

Per «stato del container» si intende che il server web risponde. Si utilizzino un messaggio di prova e un controllo di verifica per valutare la raccolta e la pubblicazione esterna.

## Pubblicate solo ciò che intendete pubblicare

La guida all’implementazione include esempi HTTPS, comandi relativi ai volumi persistenti, aggiornamenti e procedure di ripristino. Per l’implementazione vengono forniti comandi Docker; il [registro di convalida](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/) attuale identifica gli ambienti effettivamente testati.
