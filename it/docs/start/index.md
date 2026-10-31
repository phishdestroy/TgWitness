# Iniziate in pochi minuti

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/start/

In primo luogo, esamini un esempio pratico. Successivamente, colleghi il proprio account.

## Date un’occhiata al sito senza creare un account

Scarichi o cloni il progetto, installi **Python 3.11 o versioni successive** ed esegua la demo. Il programma di avvio crea un ambiente locale e installa le dipendenze indicate.

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

Il browser apre un’area di lavoro con messaggi fittizi. È possibile aprire una conversazione, confrontare una modifica e esaminare un file esportato. La modalità demo non si connette a Telegram.

![Visualizzazione delle conversazioni in TgWitness con messaggi di esempio](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Un esempio di area di lavoro. Il Suo registro personale verrà avviato separatamente.

## Crea il vostro spazio di lavoro

Chiuda la procedura di dimostrazione, quindi utilizzi il normale programma di avvio:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Apra l’indirizzo locale indicato dal programma di avvio. Se richiesto, inserisca il **token di accesso al pannello** dal file locale indicato nel terminale. Ciò sblocca TgWitness; si tratta di una procedura distinta dall’accesso a Telegram.

## Acquisite il vostro primo messaggio

1. [Collegare un account Telegram dedicato.](https://phishdestroy.github.io/TgWitness/it/docs/accounts/)
2. Selezionare un gruppo o un canale a cui l’account ha accesso, quindi avviare il monitoraggio.
3. Invii un nuovo messaggio in un gruppo di prova da Lei controllato e verifichi che compaia nel registro.

Per l’installazione su server, segua le istruzioni riportate nella sezione [«Keep it running](https://phishdestroy.github.io/TgWitness/it/docs/server/)».
