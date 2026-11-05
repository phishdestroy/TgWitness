# Les messages changent． Conservez ce que vous avez vu．

Canonical page: https://phishdestroy.github.io/TgWitness/fr/

[Open source ／ v0.9.1](https://phishdestroy.github.io/TgWitness/fr/docs/reference/changelog/)

Enregistrez les chats Telegram avec chaque modification et suppression， puis transmettez un enregistrement que tout le monde peut vérifier．

[Démonstration en ligne ：](https://phishdestroy.github.io/TgWitness/demo/?lang=fr)[Guide d＇installation](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=fr)

Données fictives， sans connexion à Telegram．

 [Collecte via GitHub Actions （version préliminaire）](https://phishdestroy.github.io/TgWitness/fr/docs/capture/) [Copie hors site sur S3 ： configuration et restauration](https://phishdestroy.github.io/TgWitness/fr/#s3)

UN MESSAGE À TRAVERS LE TEMPS ＃0042

Northstar · RechercheSource fictive ／ message 42

1. **Message observé ：**09：41：02

   Le briefing commence à 14：00．
2. **Modification conservée**09：43：18

   Le briefing commence à 15：00．

   Version précédente conservée
3. **Avis de suppression**10：06：45

   Le contenu capturé reste dans votre journal．

Trois observations． Une histoire． EXEMPLE

Le message disparaît． L＇historique enregistré demeure．

## Chaque modification enregistrée． Exactement là où vous en avez besoin．

La vraie interface， avec des données inventées．

TgWitness ／ Conversations enregistréesVOTRE ESPACE DE TRAVAIL D＇OBSERVATION

![Conversations Telegram enregistrées dans le thème sombre， avec les modifications et les messages supprimés conservés dans leur contexte](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ Chats enregistrés On dirait un chat normal， avec les modifications et suppressions juste à côté des messages．

TgWitness ／ JournalESPACE DE TRAVAIL LOCAL

![Journal contenant les messages observés， les modifications， les notifications de suppression et les événements couverts](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ Journal Tout ce que votre compte a vu， consultable， lacunes comprises．

TgWitness ／ Historique des modificationsESPACE DE TRAVAIL LOCAL

![Panneau de détails comparant les versions précédentes et modifiées d＇un message](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ Historique des modifications Ancienne et nouvelle version côte à côte， rien n＇est écrasé．

TgWitness ／ Exportations signéesESPACE DE TRAVAIL LOCAL

![Fonctionnalité d＇exportation de l＇espace de travail proposant un fichier ZIP signé， des fichiers JSONL et CSV， ainsi qu＇un rapport HTML hors ligne](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ Exports signés Emportez le journal， signé et avec son propre vérificateur．

Suivez le parcours d＇un enregistrement sauvegardé via [le « Case Board »](https://phishdestroy.github.io/TgWitness/fr/docs/case-board/)， [la conception du rapport](https://phishdestroy.github.io/TgWitness/fr/docs/reports/) et une [copie partagée](https://phishdestroy.github.io/TgWitness/fr/docs/handover/)． [Passez en revue les groupes de comptes](https://phishdestroy.github.io/TgWitness/fr/docs/groups/) ensemble．

01 ／ CAPTURE

### C＇est vous qui choisissez le champ d＇application．

Quelques chats， un dossier ou le compte entier． Chaque compte a son propre espace．

[Comparez les modes de collecte](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html#scope)

02 ／ PRESERVE

### Les modifications viennent enrichir le récit．

Versions， suppressions et lacunes restent toutes dans le journal．

[Consultez la matrice d＇événements](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html#events)

03 ／ TRANSMISSION

### Un registre qui voyage．

ZIP signé， fichiers et rapport hors ligne． Mot de passe facultatif．

[Exporter et vérifier](https://phishdestroy.github.io/TgWitness/fr/docs/exports/)

## Modifiez un seul octet．
La vérification vous le signalera．

Chaque événement est lié au hachage précédent et comporte une signature Ed25519．

![Les événements capturés renvoient vers des hachages antérieurs， comportent des signatures et sont transmis sous forme d＇exportation vérifiable．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![La modification d＇un enregistrement capturé modifie son hachage et rend impossible la vérification de l＇enregistrement associé．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Un point de contrôle conservé séparément permet au destinataire de comparer le journal exporté avec une observation antérieure．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Suivez les vérifications， du hachage d＇un fichier jusqu＇à un point de contrôle conservé séparément．

[Découvrez les huit niveaux de preuve](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html#levels)

## Prêt à être relu par une autre personne．

Messages， fichiers et rapport hors ligne dans un seul paquet signé．

[Consultez le modèle de preuve](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/)

tgwitness-evidence.zipENSEMBLE SIGNÉ

- 01

  Observations originalesFichiers JSONL ＋ tableau CSV
- 02

  Contexte lisibleRapport HTML hors ligne ＋ médias conservés
- 03

  Vérification indépendanteManifeste signé ＋ vérificateur autonome

Le destinataire vérifie tout avec votre clé， et un point de contrôle conservé ailleurs montre que rien n＇a été réécrit depuis． [Comment fonctionnent les vérifications．](https://phishdestroy.github.io/TgWitness/fr/docs/concepts/#layers)

## Copies sur S3． Contrôles externes．

Conservez des copies chiffrées et mettez en place des contrôles indépendants．

Désactivé par défaut

### Copiez l＇intégralité des données vers un espace de stockage compatible S3

Journal， fichiers， points de contrôle et exports de chats， chiffrés avant de partir vers S3．

**Paramètres de stockage et de restauration**

Chiffrement côté client

`AES-256-GCM` sur votre machine． Le fournisseur ne voit que du texte chiffré．

Copies programmées ou manuelles

Copiez maintenant ou toutes les 1 à 1 440 minutes， avec la progression dans le panneau．

Object Lock

Choisissez les jours et le mode de rétention ； le panneau vérifie que c＇est bien appliqué．

Récupération vérifiée

Gardez la clé à part． Restaurez où vous voulez ： les fichiers ne sortent qu＇après vérification．

![Panneau complet de configuration hors site ： point de terminaison， région， compartiment de stockage， clés d＇accès， planification， verrouillage d＇objets et contrôles des clés de récupération](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Le panneau complet avec les options avancées est déployé． Aucune information d＇identification de stockage n＇est affichée．

Journal et médias`AES-256-GCM`Stockage compatible S3

[Configurer S3 et restaurer une copie](https://phishdestroy.github.io/TgWitness/fr/docs/exports/#s3)[Consultez les détails de la vérification](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Clé de récupération** Gardez－la à part ： sans elle， la copie est illisible．

### Notifications · Apprise

Problèmes， changements dans les chats et résumé quotidien vers messageries， e－mail ou votre propre webhook．

**Choisissez ce qui est partagé** Pas de texte des messages tant que vous ne l＇activez pas．

 [Configurer les destinataires des notifications](https://phishdestroy.github.io/TgWitness/fr/docs/reference/operations/#notifications)

### Horodatages externes

Hachage des horodatages à l＇aide des normes RFC 3161 et OpenTimestamps．

**Suivez le résultat** Vérifiez la réponse de la TSA ou mettez à niveau le reçu OpenTimestamps en preuve Bitcoin．

 [Vérifiez les preuves horodatées](https://phishdestroy.github.io/TgWitness/fr/docs/reference/timestamp/)

### Témoin indépendant

Un serveur distinct conserve les observations signées et peut publier des points de contrôle «`TGW1`»．

**Séparez la référence** Faites－le tourner sur un autre hôte， avec sa propre clé et son propre journal．

 [Configurer un Witness](https://phishdestroy.github.io/TgWitness/fr/docs/witness/)

### Récupération et lacunes visibles

Reprise après redémarrage． Les vérifications supplémentaires et `coverage.json` indiquent les messages récupérés et les lacunes．

**Examinez l＇intervalle** Messages récupérés et lacunes enregistrées côte à côte．

 [Vérifier la continuité et les lacunes](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html#continuity)

## Votre premier espace de travail commence ici．

Essayez d＇abord la démo， puis connectez un compte de rechange quand vous êtes prêt．
Windows， Linux， macOS ou Docker．

[Consultez le guide d＇installation](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=fr)

**Une session importée， un client en cours d＇exécution．**

N＇utilisez pas une TData ou une session importée dans Telegram Desktop et TgWitness en même temps ： Telegram peut invalider les deux （AUTH_KEY_DUPLICATED）． Besoin des deux ？ Connectez－vous à TgWitness séparément， par téléphone ou QR．

[Veuillez lire l＇avertissement concernant l＇importation de sessions](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=fr#session-warning)

**Consultez－le avant de vous connecter．**

Essayez l＇espace de travail fictif sans compte Telegram．

[Accéder à la démo en ligne →](https://phishdestroy.github.io/TgWitness/demo/?lang=fr)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**Commandes d＇installation locale**

ÉTAPE 01

### Téléchargez le code source．

[Téléchargez le fichier ZIP source](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) et décompressez－le， ou clonez le dépôt ：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Nécessite Python 3.11+． Sous Windows， le lanceur propose de l＇installer．

[Parcourir les versions](https://github.com/phishdestroy/TgWitness/releases)

ÉTAPE 02

### Choisissez votre mode d＇exécution．

Double－cliquez sur `Start.cmd` ou exécutez la commande suivante dans PowerShell ：

```
.\Start.cmd
```

Vous souhaitez simplement découvrir l＇outil ？ Double－cliquez sur `scripts\Demo.cmd` pour accéder à une démo isolée． Aucune connexion à Telegram n＇est nécessaire．

Avec Python 3.11+ et `venv`， vous disposez des fonctionnalités suivantes ：

```
sh start.sh
```

Pour ouvrir le journal fictif à la place， exécutez la commande `sh start.sh --demo`．

Avec Docker en cours d＇exécution et Compose 2.20+ installé ：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

La deuxième commande affiche votre jeton de panneau privé． Conservez－le sur votre ordinateur．

Ouvrez le port [127.0.0.1:8787](http://127.0.0.1:8787) après le lancement．

Pour une installation depuis les sources， le jeton se trouve dans `data/live/panel-token.txt`． Votre propre paire d＇API de [my.telegram.org](https://my.telegram.org) est facultative． [Guide complet ↗](https://phishdestroy.github.io/TgWitness/fr/docs/reference/quickstart/)

**TgWitness 0.9.1** [Quoi de neuf →](https://phishdestroy.github.io/TgWitness/fr/docs/reference/changelog/) · [Fonctionnalités et limites connues →](https://phishdestroy.github.io/TgWitness/fr/docs/reference/features/)

## Des instructions claires． Une prochaine étape utile．

[Découvrez les guides ↗](https://phishdestroy.github.io/TgWitness/fr/docs/)

[### Modes， scénarios et niveaux de preuve Quatre modes de collecte． Huit niveaux de vérification． Trouvez le flux de travail adapté à votre dossier．](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html)

[01 ### Connecter un compte Importation par numéro de téléphone， code QR et sessions prises en charge．](https://phishdestroy.github.io/TgWitness/fr/docs/accounts/)[02 ### Choisissez un proxy Listes publiques de MTProxy ou votre propre route．](https://phishdestroy.github.io/TgWitness/fr/docs/proxies/)[03 ### Configurer un bot TgWitness Des points de contrôle signés sur votre chaîne Telegram．](https://phishdestroy.github.io/TgWitness/fr/docs/witness/)[04 ### Exporter et vérifier Partagez l＇historique capturé et vérifiez son intégrité．](https://phishdestroy.github.io/TgWitness/fr/docs/exports/)

## Exploiter les archives．

Historique， IA avec sources， MCP， OCR et webhooks signés．

[Découvrez le flux de travail](https://phishdestroy.github.io/TgWitness/fr/docs/archive/)

## Avant de commencer．

**Cette page renvoie－t－elle vers Telegram ？**

Non． C＇est une page statique avec des exemples fictifs． L＇application tourne sur votre machine et c＇est là que vous vous connectez．

**Permet－il de récupérer les messages supprimés avant leur capture ？**

Non． Elle conserve ce que votre compte a vu pendant qu＇elle tournait． Un instantané ultérieur ne peut pas reconstruire des modifications manquées ni des messages supprimés．

**L＇intégralité de mon journal est－elle chiffrée ？**

Les sessions et les clés， oui． Les messages et fichiers， non ： utilisez le chiffrement du disque． Les exports peuvent avoir un mot de passe AES－256．

**Ce site est－il affilié à Telegram ？**

Non． C＇est un projet indépendant sous licence MIT， basé sur Telethon． Vous vous connectez avec vos propres comptes．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Commencez par découvrir l＇outil． Configurez－le lorsque vous êtes prêt．

[Démonstration en ligne ：](https://phishdestroy.github.io/TgWitness/demo/?lang=fr)[Guide d＇installation](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=fr)
