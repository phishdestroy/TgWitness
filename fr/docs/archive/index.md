# Explorer les archives

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/archive/

Trouvez le message. Vérifiez la source. Construisez votre dossier.

01**Intégrer l'historique**

Ramenez dans l’espace les anciens messages de vos sources actives.

02**Suivre les sources**

Cherchez, puis ouvrez le message enregistré derrière chaque résultat.

03**Veillez à ce que le transfert soit clair**

Votre analyse dans un fichier, la preuve signée juste à côté.

Les enregistrements capturés, le texte reconnu et les conclusions des analystes restent clairement distingués.

## Charger les messages antérieurs

1. **Sources → Chats inclus** : vérifiez les chats actifs et lancez l’observation.
2. **Charger tout l’historique**. La liste des sources est prise telle qu’elle est à ce moment-là.
3. **Mettre l’historique en pause** / **Reprendre l’historique** à tout moment. Après un redémarrage, reprenez à la main.
4. Vérifiez le résultat par source et la file de téléchargement, et gardez le rapport de progression signé avec l’export.

Cela remplit l’espace. Exporter un seul chat en HTML/JSON, c’est autre chose. [Détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/history/).

## Commencez par effectuer une recherche, puis décidez de recourir ou non à l'IA

1. **Journal** cherche en local, avec des filtres par source et par date.
2. Cherchez une phrase ou un domaine, ouvrez l’entrée et ses versions.
3. Pour l’IA, l’administrateur configure un fournisseur dans **Intégrations**. Ensuite **Interroger l’archive** : choisissez des chats et une période, regardez **Données envoyées au modèle** et décochez ce qui ne doit pas partir.
4. Vérifiez les citations, enregistrez la réponse comme rapport et ajoutez vos notes.

La recherche n’a pas besoin d’IA. Les rapports gardent leurs sources et leurs révisions, à part du journal signé. [Configurer le fournisseur](https://phishdestroy.github.io/TgWitness/fr/docs/reference/analysis/).

## Choisissez la connexion qui vous convient

| Mission | Ouvrir | Configuration |
| --- | --- | --- |
| Laisser un client IA lire des chats choisis | **Intégrations → MCP** | [Installer MCP, créer un jeton limité, se connecter](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/) |
| Reconnaissance du texte dans les fichiers multimédias enregistrés | Un enregistrement `media.saved` → **Reconnaître la pièce jointe** | [Configurer le worker Docker local](https://phishdestroy.github.io/TgWitness/fr/docs/reference/media-analysis/) |
| Envoyer les événements vers n8n ou un SIEM | **Intégrations → Webhooks sortants** | [Ajouter un récepteur, vérifier le HMAC, dédoublonner les ID](https://phishdestroy.github.io/TgWitness/fr/docs/reference/webhooks/) |

**Quel jeton d'accès va où ?**

L’accès au panneau est pour les personnes. MCP a ses propres jetons en lecture seule, les webhooks leur propre secret HMAC. Aucun n’a besoin d’une session Telegram.

[Partager l'accès au panneau de configuration](https://phishdestroy.github.io/TgWitness/fr/docs/access/) ou [configurer un client MCP](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/).

## Présentation des sources et des conclusions

Mettez le rapport à côté du ZIP signé. Le rapport, c’est votre lecture des sources ; le ZIP, c’est ce que le destinataire vérifie.

[Exporter et vérifier](https://phishdestroy.github.io/TgWitness/fr/docs/exports/) · [Mener une enquête de A à Z](https://phishdestroy.github.io/TgWitness/fr/docs/cases/)
