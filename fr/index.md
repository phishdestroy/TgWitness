# Les messages changent. Conservez ce que vous avez vu.

Canonical page: https://phishdestroy.github.io/TgWitness/fr/

[Open source / v0.7.0](https://phishdestroy.github.io/TgWitness/fr/docs/reference/changelog/)

Capturez les messages Telegram, conservez leurs modifications et exportez un enregistrement signé.

[Démonstration en ligne :](https://phishdestroy.github.io/TgWitness/demo/?lang=fr)[Guide d'installation](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=fr)

La démo utilise des données fictives. Aucune connexion à Telegram n'est requise.

 [Collecte via GitHub Actions (version préliminaire)](https://phishdestroy.github.io/TgWitness/fr/docs/capture/) [Copie hors site sur S3 : configuration et restauration](https://phishdestroy.github.io/TgWitness/fr/#s3)

UN MESSAGE À TRAVERS LE TEMPS #0042

Northstar · RechercheSource fictive / message 42

1. **Message observé :**09:41:02

   Le briefing commence à 14:00.
2. **Modification conservée**09:43:18

   Le briefing commence à 15:00.

   Version précédente conservée
3. **Avis de suppression**10:06:45

   Le contenu capturé reste dans votre journal.

Trois observations. Une histoire. EXEMPLE

Le message disparaît. L'historique enregistré demeure.

## Chaque modification enregistrée. Exactement là où vous en avez besoin.

Parcourez l'interface à l'aide de données de démonstration fictives.

TgWitness / Conversations enregistréesVOTRE ESPACE DE TRAVAIL D'OBSERVATION

![Conversations Telegram enregistrées dans le thème sombre, avec les modifications et les messages supprimés conservés dans leur contexte](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Conversations enregistrées Une vue familière des conversations, avec les modifications capturées et les notifications de suppression affichées à côté des messages.

TgWitness / JournalESPACE DE TRAVAIL LOCAL

![Journal contenant les messages observés, les modifications, les notifications de suppression et les événements couverts](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Journal : une chronologie consultable de tout ce que votre compte a enregistré, y compris les interruptions.

TgWitness / Historique des modificationsESPACE DE TRAVAIL LOCAL

![Panneau de détails comparant les versions précédentes et modifiées d’un message](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Historique des modifications : comparez les versions capturées sans écraser l'observation précédente.

TgWitness / Exportations signéesESPACE DE TRAVAIL LOCAL

![Fonctionnalité d’exportation de l’espace de travail proposant un fichier ZIP signé, des fichiers JSONL et CSV, ainsi qu’un rapport HTML hors ligne](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Exportations signées : emportez le journal avec vous, accompagné d’un manifeste et d’un vérificateur indépendant.

01 / CAPTURE

### C'est vous qui choisissez le champ d'application.

Des discussions sélectionnées, un dossier Telegram ou l’intégralité du compte. Un espace de travail distinct pour chaque compte.

[Comparez les modes de collecte](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html#scope)

02 / PRESERVE

### Les modifications viennent enrichir le récit.

Les versions capturées, les notifications de suppression et les lacunes d’observation sont conservées dans le journal.

[Consultez la matrice d'événements](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html#events)

03 / TRANSMISSION

### Un registre qui voyage.

Fichier ZIP signé, fichiers conservés et rapport hors ligne. Protection par mot de passe en option.

[Exporter et vérifier](https://phishdestroy.github.io/TgWitness/fr/docs/exports/)

## Modifiez un octet. La chaîne vous le signale.

Chaque événement est lié au hachage précédent et comporte une signature Ed25519.

![Les événements capturés renvoient vers des hachages antérieurs, comportent des signatures et sont transmis sous forme d’exportation vérifiable.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![La modification d’un enregistrement capturé modifie son hachage et rend impossible la vérification de l’enregistrement associé.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Un point de contrôle conservé séparément permet au destinataire de comparer le journal exporté avec une observation antérieure.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Découvrez ce que chaque mécanisme de vérification permet d’établir et quelles sont ses limites.

[Découvrez les huit niveaux de preuve](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html#levels)

## Prêt à être relu par une autre personne.

Transmettez vos observations, vos fichiers et un rapport HTML hors ligne dans un seul ensemble signé.

[Consultez le modèle de preuve](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/)

tgwitness-evidence.zipENSEMBLE SIGNÉ

- 01

  Observations originalesFichiers JSONL + tableau CSV
- 02

  Contexte lisibleRapport HTML hors ligne + médias conservés
- 03

  Vérification indépendanteManifeste signé + vérificateur autonome

Les signatures détectent toute altération par rapport à une clé de confiance. Elles ne prouvent pas l’origine Telegram ni ne garantissent une capture complète. Le contenu du journal et les fichiers multimédias doivent être stockés de manière chiffrée, ce dont vous devez vous charger.

## Copies sur S3. Contrôles externes.

Conservez des copies chiffrées et mettez en place des contrôles indépendants.

Désactivé par défaut

### Copiez l'intégralité des données vers un espace de stockage compatible S3

Journal, fichiers, points de contrôle horodatés et exportations de discussions — cryptés avant leur transfert vers AWS S3 ou un stockage compatible.

**Paramètres de stockage et de restauration**

Chiffrement côté client

`AES-256-GCM` crypte les objets sur cette machine. Le fournisseur reçoit les objets cryptés.

Copies programmées ou manuelles

Lancez la sauvegarde dès maintenant ou choisissez un intervalle compris entre 1 et 1 440 minutes. Suivez la progression dans le panneau.

Object Lock

Choisissez la durée de conservation et un mode lorsque le compartiment le permet. Le panneau indique si la conservation a été confirmée pour un objet téléchargé.

Récupération vérifiée

Téléchargez la clé de chiffrement et conservez-la séparément. Restaurez-la sur un autre ordinateur ; les fichiers ne sont publiés qu’après vérification.

![Panneau complet de configuration hors site : point de terminaison, région, compartiment de stockage, clés d’accès, planification, verrouillage d’objets et contrôles des clés de récupération](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Le panneau complet avec les options avancées est déployé. Aucune information d'identification de stockage n'est affichée.

Journal et médias`AES-256-GCM`Stockage compatible S3

[Configurer S3 et restaurer une copie](https://phishdestroy.github.io/TgWitness/fr/docs/exports/#s3)[Consultez les détails de la vérification](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Ne permet pas**de restaurer les données sans la clé de déchiffrement exportée, ni de se substituer à un témoin indépendant.

### Notifications · Apprise

Alertes en cas de problème, modifications des discussions et résumés quotidiens via Apprise : messageries instantanées, e-mail ou votre propre webhook JSON.

Fonctionnalités : il n'envoie pas le texte des messages, sauf si vous activez l'option « extraits ».

 [Configurer les destinataires des notifications](https://phishdestroy.github.io/TgWitness/fr/docs/reference/operations/#notifications)

### Horodatages externes

Hachage des horodatages à l'aide des normes RFC 3161 et OpenTimestamps.

**Ne traite pas :** il ne considère pas une confirmation de réception en attente comme un horodatage Bitcoin confirmé.

 [Vérifiez les preuves horodatées](https://phishdestroy.github.io/TgWitness/fr/docs/reference/timestamp/)

### Témoin indépendant

Un serveur distinct conserve les observations signées et peut publier des points de contrôle «`TGW1`».

**Ne fait pas :** cela ne transforme pas deux espaces de travail sur un même hôte collecteur en témoins indépendants.

 [Configurer un Witness](https://phishdestroy.github.io/TgWitness/fr/docs/witness/)

### Récupération et lacunes visibles

Reprise après redémarrage. Les vérifications supplémentaires et `coverage.json` indiquent les messages récupérés et les lacunes.

Ce qu’il**ne fait pas :** il ne reconstitue pas chaque modification manquée ni chaque message disparu.

 [Vérifier la continuité et les lacunes](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html#continuity)

## Votre premier espace de travail commence ici.

Commencez par découvrir la démo. Connectez-vous à un compte dédié lorsque vous êtes prêt. Windows, Linux, macOS ou Docker.

[Consultez le guide d'installation](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=fr)

**Une session importée, un client en cours d'exécution.**

N’utilisez pas simultanément une clé TData/session importée dans Telegram Desktop et TgWitness. Telegram peut invalider l’autorisation partagée (AUTH_KEY_DUPLICATED). Pour une utilisation parallèle, créez un compte TgWitness distinct via votre téléphone ou un code QR.

[Veuillez lire l'avertissement concernant l'importation de sessions](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=fr#session-warning)

**Consultez-le avant de vous connecter.**

Essayez l'espace de travail fictif sans compte Telegram.

[Accéder à la démo en ligne →](https://phishdestroy.github.io/TgWitness/demo/?lang=fr)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Commandes d'installation locale**

ÉTAPE 01

### Téléchargez le code source.

[Téléchargez le fichier ZIP source](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) et décompressez-le, ou clonez le dépôt :

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Le lancement de la source nécessite Python 3.11 ou une version ultérieure. Le lanceur Windows propose une installation si Python n'est pas présent.

[Parcourir les versions](https://github.com/phishdestroy/TgWitness/releases)

Vous n'avez pas Python sous Windows ? [Téléchargez le package portable](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip), décompressez-le et double-cliquez sur « `TgWitness.cmd` ».

ÉTAPE 02

### Choisissez votre mode d'exécution.

Double-cliquez sur `Start.cmd` ou exécutez la commande suivante dans PowerShell :

```
.\Start.cmd
```

Vous souhaitez simplement découvrir l'outil ? Double-cliquez sur `scripts\Demo.cmd` pour accéder à une démo isolée. Aucune connexion à Telegram n'est nécessaire.

Avec Python 3.11+ et `venv`, vous disposez des fonctionnalités suivantes :

```
sh start.sh
```

Pour ouvrir le journal fictif à la place, exécutez la commande `sh start.sh --demo`.

Avec Docker en cours d'exécution et Compose 2.20+ installé :

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

La deuxième commande affiche votre jeton de panneau privé. Conservez-le sur votre ordinateur.

Ouvrez le port [127.0.0.1:8787](http://127.0.0.1:8787) après le lancement.

Pour les installations à partir des sources, le jeton est « `data/live/panel-token.txt` ». La connexion à Telegram peut s'effectuer via les paramètres API intégrés ou à l'aide de votre propre paire de clés obtenue sur [my.telegram.org](https://my.telegram.org). [Guide d'installation complet ↗](https://phishdestroy.github.io/TgWitness/fr/docs/reference/quickstart/)

**TgWitness 0.7.0** [Quoi de neuf →](https://phishdestroy.github.io/TgWitness/fr/docs/reference/changelog/) · [Fonctionnalités et limites connues →](https://phishdestroy.github.io/TgWitness/fr/docs/reference/features/)

## Des instructions claires. Une prochaine étape utile.

[Découvrez les guides ↗](https://phishdestroy.github.io/TgWitness/fr/docs/)

[### Modes, scénarios et niveaux de preuve Quatre modes de collecte. Huit niveaux de vérification. Trouvez le flux de travail adapté à votre dossier.](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html)

[01 ### Connecter un compte Importation par numéro de téléphone, code QR et sessions prises en charge.](https://phishdestroy.github.io/TgWitness/fr/docs/accounts/)[02 ### Choisissez un proxy Listes publiques de MTProxy ou votre propre route.](https://phishdestroy.github.io/TgWitness/fr/docs/proxies/)[03 ### Configurer un bot TgWitness Des points de contrôle signés sur votre chaîne Telegram.](https://phishdestroy.github.io/TgWitness/fr/docs/witness/)[04 ### Exporter et vérifier Partagez l'historique capturé et vérifiez son intégrité.](https://phishdestroy.github.io/TgWitness/fr/docs/exports/)

## Exploiter les archives.

Charger l'historique, examiner les sources IA, connecter un client MCP, reconnaître les médias enregistrés et envoyer des webhooks signés.

Disponible à partir de la source actuelle. La version préliminaire portable 0.7.0 est antérieure à ces outils.

[Découvrez le flux de travail](https://phishdestroy.github.io/TgWitness/fr/docs/archive/)

## Avant de commencer.

**Cette page renvoie-t-elle vers Telegram ?**

Non. Il s'agit d'une page de projet statique contenant des exemples fictifs et des captures d'écran. L'application proprement dite s'exécute sur votre ordinateur ou votre serveur ; c'est là que s'effectue la connexion.

**Permet-il de récupérer les messages supprimés avant leur capture ?**

Non. TgWitness conserve le contenu que votre compte a détecté pendant que la collecte était en cours. Un instantané ultérieur de l'historique ne permet pas de reconstituer les modifications manquées ni les messages supprimés.

**L'intégralité de mon journal est-elle chiffrée ?**

Les identifiants de compte et les secrets de signature sont stockés dans un coffre-fort chiffré. Les messages et pièces jointes locaux nécessitent un disque ou un volume chiffré. Les exportations peuvent, au choix, utiliser un fichier ZIP AES-256 protégé par mot de passe.

**Ce site est-il affilié à Telegram ?**

Non. TgWitness est un projet indépendant utilisant Telethon, distribué sous licence MIT. Vous autorisez vos propres comptes, soit via les paramètres API intégrés, soit à l’aide de votre propre paire d’API.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Commencez par découvrir l'outil. Configurez-le lorsque vous êtes prêt.

[Démonstration en ligne :](https://phishdestroy.github.io/TgWitness/demo/?lang=fr)[Guide d'installation](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=fr)
