# Charger l'historique des sources

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/history/

Charger les messages antérieurs provenant des sources activées, mettre en pause et reprendre l'opération, puis vérifier un rapport d'avancement signé.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Collection](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Pause, redémarrage et résultats partiels

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- L’observation du message, la tâche de pièce jointe et la validation du curseur sont regroupées en une seule transaction. Une exécution reprise ne répète pas les observations déjà validées. Une capture en direct ou une exécution distincte, lancée explicitement, peut observer indépendamment le même message.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Les sources inaccessibles et celles désactivées lors de l'acquisition restent visibles comme « échouées » ou « ignorées ». Les autres sources continuent ; le résultat global est incomplet.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

La « finalisation de l’historique » ne concerne que la lecture de l’historique. Les pièces jointes peuvent rester en attente, échouer ou être exclues par la politique configurée. Vérifiez les accusés de réception multimédia dans le journal et la file d’attente des pièces jointes ; seul un accusé de réception finalisé avec des octets préservés constitue une pièce jointe enregistrée. L’opération d’historique est une demande explicite d’instantané et est distincte des commutateurs qui sélectionnent des catégories d’événements en direct futurs.

## Transférer et vérifier

Enregistrez le **rapport d'avancement signé**, puis utilisez **« Exporter les preuves »** pour télécharger le journal et les pièces jointes enregistrées. Une exportation ultérieure des preuves peut inclure des enregistrements supplémentaires ; le rapport lie ses compteurs au préfixe du journal au moment de sa création. Exécutez le vérificateur à partir d'une version fiable de cette version :

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

Le curseur d’acquisition correspond à l’état local de l’espace de travail. La restauration d’un fichier ZIP de preuves ne restaure pas à elle seule une tâche d’acquisition en attente ou une session Telegram. Conservez la sauvegarde de l’espace de travail si la poursuite de la tâche d’origine est nécessaire.
