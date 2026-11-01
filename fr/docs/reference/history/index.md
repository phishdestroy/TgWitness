# Charger l'historique des sources

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/history/

Charger les messages antérieurs provenant des sources activées, mettre en pause et reprendre l'opération, puis vérifier un rapport d'avancement signé.

Dans **« Sources** », passez en revue les discussions activées, lancez l’observation, puis sélectionnez « **Charger l’historique complet**». L’exécution fixe cette liste de sources et importe leurs anciens messages disponibles dans « Discussions » et dans le journal d’observation signé. Les médias utilisent les paramètres de pièces jointes existants et la file d’attente de téléchargement permanente. Ceci est distinct de l’exportation JSON/HTML signée par discussion.

Pour une collecte à l'échelle du compte, sélectionnez « **Compte entier** », lancez l'observation pour charger sa liste de sources, puis vérifiez cette liste avant de démarrer l'historique. La limite du nombre de listes de dialogues s'applique toujours (1 000 par défaut, ajustable dans les paramètres). Une exécution réussie ne prouve pas que toutes les conversations du compte ont été répertoriées. Les discussions découvertes ou activées ultérieurement nécessitent une nouvelle exécution.

## Pause, redémarrage et résultats partiels

- **La mise en pause de l'historique** interrompt la lecture. **La poursuite de l'historique** reprend à partir du dernier message validé dans chaque source ; le redémarrage de l'application laisse également l'exécution en pause jusqu'à ce qu'elle soit reprise. Redémarrez d'abord l'observation. La reprise nécessite le même compte Telegram.
- L’observation du message, la tâche de pièce jointe et la validation du curseur sont regroupées en une seule transaction. Une exécution reprise ne répète pas les observations déjà validées. Une capture en direct ou une exécution distincte, lancée explicitement, peut observer indépendamment le même message.
- Chaque source fixe un identifiant de message maximal lors de sa première lecture. Les messages plus récents relèvent de l’ observation en temps réel, et non des pages historiques restantes de cette source.
- Les sources inaccessibles et celles désactivées lors de l'acquisition restent visibles comme « échouées » ou « ignorées ». Les autres sources continuent ; le résultat global est incomplet.
- Les délais d'attente FloodWait respectent le délai de réessai enregistré pour chaque compte. Les délais d'attente de transport et le manque d'espace disque suspendent l'exécution tout en conservant le curseur en place. Reprise après résolution du problème.
- **La fonction « Mettre fin à cette session d'historique »** conserve les observations enregistrées. Elle ne les supprime pas et n' annule pas les téléchargements de pièces jointes déjà mis en file d'attente. Une nouvelle session relit les sources activées.

La « finalisation de l’historique » ne concerne que la lecture de l’historique. Les pièces jointes peuvent rester en attente, échouer ou être exclues par la politique configurée. Vérifiez les accusés de réception multimédia dans le journal et la file d’attente des pièces jointes ; seul un accusé de réception finalisé avec des octets préservés constitue une pièce jointe enregistrée. L’opération d’historique est une demande explicite d’instantané et est distincte des commutateurs qui sélectionnent des catégories d’événements en direct futurs.

## Transférer et vérifier

Enregistrez le **rapport d'avancement signé**, puis utilisez **« Exporter les preuves »** pour télécharger le journal et les pièces jointes enregistrées. Une exportation ultérieure des preuves peut inclure des enregistrements supplémentaires ; le rapport lie ses compteurs au préfixe du journal au moment de sa création. Exécutez le vérificateur à partir d'une version fiable de cette version :

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Conservez séparément l’empreinte digitale attendue de la clé de signature. Le vérificateur contrôle la signature du rapport, l’archive des preuves, le point de contrôle du rapport, le plan source, le compte et le nombre de messages enregistrés/indisponibles. Sans `--evidence`, il ne vérifie que le rapport signé et sa cohérence interne. Les phases d’avancement, les titres, les curseurs et les résumés des pièces jointes sont des déclarations signées par le collecteur, et non reconstituées de manière indépendante par ce vérificateur de rapport. Le vérificateur de preuves contrôle néanmoins les octets des médias archivés.

Ni la signature ni la finalisation de l’historique disponible ne prouvent l’origine Telegram, un instantané atomique ou l’exhaustivité historique. Les messages peuvent changer pendant leur lecture ; les messages supprimés, les modifications intermédiaires non vues et les discussions secrètes ne sont pas récupérés. Un opérateur contrôlant la clé de signature peut fabriquer un journal avant l’existence d’engagements externes. Utilisez des points de contrôle conservés séparément ou un témoin indépendant pour garantir les propriétés de détection des altérations documentées.

Le curseur d’acquisition correspond à l’état local de l’espace de travail. La restauration d’un fichier ZIP de preuves ne restaure pas à elle seule une tâche d’acquisition en attente ou une session Telegram. Conservez la sauvegarde de l’espace de travail si la poursuite de la tâche d’origine est nécessaire.
