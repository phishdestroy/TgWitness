# Telegram · Charger l'historique des sources

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/history/

Charger les messages antérieurs provenant des sources activées, mettre en pause et reprendre l'opération, puis vérifier un rapport d'avancement signé.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Collecte](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collecte](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

Dans **Sources**, passez en revue les discussions activées, mettez l’observation en pause, choisissez l’API standard ou l’exportation Takeout, puis sélectionnez **Charger l’historique complet**. L’exécution corrige cette liste de sources et lit leurs anciens messages disponibles dans les discussions et le journal d’observation signé. La fonctionnalité Médias utilise les paramètres de pièces jointes existants et la file d’attente de téléchargement permanente. Cela est distinct de l’exportation JSON/HTML signée par discussion.

Pour une collecte à l’échelle du compte, sélectionnez **Tout le compte**, lancez l’observation pour charger sa liste source, puis vérifiez cette liste avant de démarrer l’historique. La limite de la liste des boîtes de dialogue s’applique toujours (1,000 par défaut, ajustable dans les paramètres). Une exécution réussie ne prouve pas que toutes les boîtes de dialogue du compte ont été répertoriées. Les discussions découvertes ou activées ultérieurement nécessitent une nouvelle exécution. Mettez l’observation en pause avant de démarrer l’historique ; une acquisition ne peut porter que sur un seul compte à la fois.

Choisissez entre un et cinq attachment workers et indiquez si vous souhaitez conserver les Actions récentes disponibles et comparer les versions précédemment enregistrées. L’extraction peut nécessiter une validation dans Telegram et un délai d’attente spécifié par le serveur. Ces options restent inchangées à la reprise. Consultez [le comportement de backfill et le contrat de preuve](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) pour plus de détails sur le transport, les nouvelles tentatives et la confiance.

## Pause, redémarrage et résultats partiels

- **Historique des pauses** interrompt la lecture. **Historique des reprises** reprend à partir du dernier message validé dans chaque source ; le redémarrage de l'application laisse également l'exécution en pause jusqu'à sa reprise. La reprise nécessite le même compte Telegram inactif.
- L’observation du message, la tâche de pièce jointe et la validation du curseur sont regroupées en une seule transaction. Une exécution reprise ne répète pas les observations déjà validées. Une capture en direct ou une exécution distincte, lancée explicitement, peut observer indépendamment le même message.
- Chaque source (chaque plage de messages Telegram dans Takeout) fixe un ID de message maximal lors de sa première lecture. Les messages plus récents appartiennent à l’ observation en temps réel, et non aux pages historiques restantes de cette source.
- Les sources inaccessibles et celles désactivées lors de l'acquisition restent visibles comme « échouées » ou « ignorées ». Les autres sources continuent ; le résultat global est incomplet.
- Les délais FloodWait respectent le délai de réessai enregistré pour le compte. Les échecs temporaires donnent lieu à jusqu’à cinq tentatives ; en cas d’épuisement ou d’espace disque insuffisant, le processus est mis en pause tout en conservant la position du curseur.
- **Mettre fin à cette exécution de l'historique** conserve les observations enregistrées. Cela ne les supprime pas et n' annule pas les tâches de pièce jointe de l'API standard. Mettre fin à Takeout marque ses fichiers Takeout restants comme ignorés ; la mise en pause permet de les reprendre ultérieurement. Une nouvelle exécution relit les sources activées.

La « finalisation de l’historique » ne concerne que la lecture de l’historique. Les pièces jointes peuvent rester en attente, échouer ou être exclues par la politique configurée. Vérifiez les accusés de réception multimédia dans le journal et la file d’attente des pièces jointes ; seul un accusé de réception finalisé avec des octets préservés constitue une pièce jointe enregistrée. L’opération d’historique est une demande explicite d’instantané et est distincte des commutateurs qui sélectionnent des catégories d’événements en direct futurs.

## Transférer et vérifier

Enregistrez le **rapport d'avancement signé**, puis utilisez **« Exporter les preuves »** pour télécharger le journal et les pièces jointes enregistrées. Une exportation ultérieure des preuves peut inclure des enregistrements supplémentaires ; le rapport lie ses compteurs au préfixe du journal au moment de sa création. Exécutez le vérificateur à partir d'une version fiable de cette version :

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Conserver séparément l’empreinte digitale attendue de la clé de signature. Le vérificateur contrôle la signature du rapport, l’archive des preuves, le point de contrôle du rapport, le plan source, le compte et le nombre de messages enregistrés/indisponibles. Les nouvelles exécutions associent également la progression de la source et les options aux événements de curseur signés. Sans `--evidence`, il ne vérifie que le rapport signé et sa cohérence interne. Les champs de progression hérités et les résumés des pièces jointes restent des déclarations signées du collecteur. Le vérificateur de preuves vérifie les octets multimédias archivés.

Ni la signature ni la finalisation de l’historique disponible ne prouvent l’origine Telegram, un instantané atomique ou l’exhaustivité historique. Les messages peuvent changer pendant la lecture ; les messages supprimés et les modifications intermédiaires ne figurant pas dans les Actions récentes disponibles, ainsi que les Discussions secrètes, ne sont pas récupérés. Un opérateur contrôlant la clé de signature peut fabriquer un journal avant même que des engagements externes n’existent. Utilisez des points de contrôle conservés séparément ou un témoin indépendant pour les propriétés documentées de détection des altérations.

Le curseur d’acquisition correspond à l’état local de l’espace de travail. La restauration d’un fichier ZIP de preuves ne restaure pas à elle seule une tâche d’acquisition en attente ou une session Telegram. Conservez la sauvegarde de l’espace de travail si la poursuite de la tâche d’origine est nécessaire.
