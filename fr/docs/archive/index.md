# Explorer les archives

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/archive/

Trouvez le message. Vérifiez la source. Construisez votre dossier.

Ces outils sont disponibles dans la branche principale actuelle. La version préliminaire portable 0.7.0 est antérieure à celles-ci ; utilisez une extraction du code source pour ce workflow.

01**Intégrer l'historique**

Importez les messages antérieurs provenant de vos sources activées dans l'espace de travail.

02**Suivre les sources**

Effectuez une recherche dans les archives et ouvrez le message enregistré correspondant à chaque résultat.

03**Veillez à ce que le transfert soit clair**

Enregistrez votre analyse séparément et exportez les preuves signées à côté.

Les enregistrements capturés, le texte reconnu et les conclusions des analystes restent clairement distingués.

## Charger les messages antérieurs

1. **Sources** ouvertes : passez en revue les discussions activées et commencez l'observation.
2. Sélectionnez « **Charger l'historique complet** ». L'exécution utilise la liste de sources sélectionnée à ce moment-là.
3. Utilisez les options « **Pause de l'historique »** et « **Reprise de l'historique »** selon les besoins. Après un redémarrage, reprenez explicitement l'enregistrement.
4. Vérifiez les résultats par source et la file d'attente des pièces jointes. Enregistrez le rapport d'avancement signé avec l'exportation des preuves.

Cette opération remplit l'espace de travail avec les messages disponibles. L'exportation au format HTML/JSON par conversation est une opération distincte. [Historique et détails de la restauration](https://phishdestroy.github.io/TgWitness/fr/docs/reference/history/).

## Commencez par effectuer une recherche, puis décidez de recourir ou non à l'IA

1. Ouvrez « **Ask the archive** ». Choisissez un espace de travail, des discussions et une période d'observation.
2. Recherchez une expression, un domaine ou un identifiant de message. Ouvrez l'enregistrement correspondant et ses versions sauvegardées.
3. Pour l'analyse par IA, l'administrateur doit d'abord configurer un fournisseur. Il doit ensuite examiner **les données envoyées au modèle** et décocher les extraits indésirables avant d'approuver la demande.
4. Vérifiez les citations renvoyées. Enregistrez la réponse sous forme de rapport et ajoutez-y vos propres corrections ou remarques.

Les recherches s'effectuent localement, sans IA. Les rapports analytiques conservent les références des sources et l'historique des révisions ; ils sont distincts du journal signé. [Configuration du fournisseur et rapports](https://phishdestroy.github.io/TgWitness/fr/docs/reference/analysis/).

## Choisissez la connexion qui vous convient

| Mission | Ouvrir | Configuration |
| --- | --- | --- |
| Lire une sélection de discussions provenant d'un client IA | **Intégrations → MCP** | [Installez l'extension MCP, générez un jeton à portée limitée et connectez le client](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/) |
| Reconnaissance du texte dans les fichiers multimédias enregistrés | Un enregistrement `media.saved` → **Reconnaître la pièce jointe** | [Configurer le worker Docker local et les fichiers de langage/modèle requis](https://phishdestroy.github.io/TgWitness/fr/docs/reference/media-analysis/) |
| Envoyer les événements vers n8n ou un SIEM | **Intégrations → Webhooks sortants** | [Ajouter un destinataire, vérifier le HMAC et dédupliquer les identifiants d'événements](https://phishdestroy.github.io/TgWitness/fr/docs/reference/webhooks/) |

**Quel jeton d'accès va où ?**

L'accès au panneau est réservé aux personnes chargées d'examiner l'affaire. Les connexions MCP reçoivent des jetons d'archivage distincts en lecture seule. Un récepteur de webhook utilise son propre secret HMAC. Aucun d'entre eux n'a besoin d'un fichier de session Telegram.

[Partager l'accès au panneau de configuration](https://phishdestroy.github.io/TgWitness/fr/docs/access/) ou [configurer un client MCP](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/).

## Présentation des sources et des conclusions

Conservez le rapport d'analyse révisé avec le fichier ZIP de preuves signées. Le rapport explique votre interprétation des sources ; le fichier ZIP permet au destinataire de vérifier l'enregistrement sauvegardé par rapport à une empreinte et à un point de contrôle fiables et indépendants.

[Exporter et vérifier](https://phishdestroy.github.io/TgWitness/fr/docs/exports/) · [Mener une enquête de A à Z](https://phishdestroy.github.io/TgWitness/fr/docs/cases/)
