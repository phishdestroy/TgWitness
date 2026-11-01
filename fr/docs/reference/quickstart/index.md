# Mise en route rapide

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/quickstart/

Toutes les méthodes d'installation et de lancement de TgWitness : package Windows, Python, Docker et la démo synthétique, avec les premières vérifications.

**Anglais** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Ukrainien](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Portugais (Brésil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [हिन्दी](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [Chinois simplifié](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness est une application autonome permettant de surveiller les groupes et les chaînes Telegram auxquels vos comptes ont accès. Elle fonctionne en local avec son propre répertoire de données.

**C'est votre première visite ?** [Découvrez la démo](https://phishdestroy.github.io/TgWitness/fr/docs/reference/quickstart/#explore-the-interface) avant de connecter un compte. [Choisissez un guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) consacré aux proxys, aux témoins, aux exportations ou à la configuration du serveur.

## Installation et mise en route

[Collecte via GitHub Actions (version préliminaire)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Choisissez une méthode. Les versions téléchargeables sont disponibles dès la publication d’une version stable :

| Hébergeur | Aucune installation requise | Source : Python 3.11+ | Docker : Engine/Desktop avec Compose 2.20 ou version ultérieure |
| --- | --- | --- | --- |
| Windows | Extrayez « `TgWitness-<version>-windows-amd64-portable.zip` » des versions GitHub, puis double-cliquez sur « `TgWitness.cmd` » | Double-cliquez sur `Start.cmd` | Double-cliquez sur `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

Pour les méthodes depuis les sources, [téléchargez et extrayez la branche `main` actuelle](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) ou clonez le dépôt :

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

`Start.cmd` propose d'installer Python 3.12 pour votre utilisateur Windows si aucune version appropriée de Python n'est trouvée (via winget ou l'installateur signé de python.org). `start.sh` affiche la commande d'installation exacte pour votre distribution Linux ou macOS si Python est manquant. Le premier lancement depuis les sources crée `.venv` et installe les dépendances automatiquement.

Docker compile l’application et la lance en arrière-plan ; l’utilisation de Python sur l’hôte n’est pas nécessaire. Les commandes « `scripts\Docker.cmd` » et « `scripts/docker-start.sh` » affichent l’adresse du panneau et le jeton lorsque le conteneur fonctionne correctement. Les commandes Docker équivalentes sur chaque hôte pris en charge sont les suivantes :

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

**http://127.0.0.1:8787** ouverte. Utilisez le jeton généré par l’assistant Docker ou la deuxième commande Docker, ou consultez **le fichier data/live/panel-token.txt** pour une installation portable ou à partir du code source. Poursuivez à la section « **Connecter Telegram »** ci-dessous. Les installations natives et Docker utilisent des espaces de stockage distincts ; le démarrage de Docker n’importe pas un journal natif existant.

Pour un serveur, [le déploiement](https://phishdestroy.github.io/TgWitness/fr/docs/reference/deployment/) inclut la configuration automatique du protocole HTTPS, le redémarrage, la publication d’images, les mises à jour et les sauvegardes.

## Découvrez l'interface

1. Exécutez **TgWitness-Demo.cmd** dans le package portable, **scripts\Demo.cmd** dans un dossier source Windows ou `sh start.sh --demo` sous Linux/macOS. Un lancement depuis le dossier source crée d'abord `.venv` et installe les dépendances.
2. **http://127.0.0.1:8787** ouvert.
3. La démo locale ouvre automatiquement le journal d'exemple. Aucune copie du jeton n'est nécessaire pour un accès local direct.

Les messages de démonstration sont fictifs. Le mode démo ne permet pas de se connecter à un véritable compte Telegram.

## Se connecter à Telegram

> [!AVERTISSEMENT] **N’utilisez rien que vous ne puissiez vous permettre de perdre.** Nous vous déconseillons vivement de connecter des comptes personnels ou importants, ainsi que de créer un identifiant API / un hachage sur un compte auquel vous tenez. Telegram suspend les comptes de manière imprévisible et souvent définitive, quel que soit le client utilisé. Le bon déroulement d’un test dépend de Telegram, et non de TgWitness, et ne garantit rien pour la suite.

1. Si la démo native est en cours d'exécution, arrêtez-la et exécutez **Start.cmd** ou `sh start.sh`. Sinon, laissez l'installation en direct lancée ci-dessus en cours d'exécution.
2. Utilisez le jeton correspondant à votre méthode d’installation pour ouvrir le panneau de configuration.
3. Si vous avez besoin d’un proxy, enregistrez-le dans **Compte → Paramètres → Paramètres de connexion → Modifier l’itinéraire de connexion**.
4. Dans **la section « Compte »**, saisissez votre numéro de téléphone et cliquez sur **« Continuer »**, choisissez **« Code QR » → « Afficher le code QR** », ou sélectionnez des fichiers et cliquez sur « **Connecter le compte** ». **L’ID API + le hachage** sont facultatifs : l’espace de travail utilise la paire enregistrée ou importée, ou une paire valide issue du pool intégré. Pour utiliser votre propre application, collez une paire `API ID:API Hash` dans le champ « ID API ». Pour obtenir une clé d’autorisation complète, choisissez « **Clé d’authentification »**, collez l’intégralité des 512 caractères hexadécimaux et sélectionnez l’identifiant DC fourni. L’identifiant utilisateur est facultatif et est coché s’il est saisi.
5. Veuillez compléter la méthode de connexion que vous avez choisie : téléphone/code/authentification à deux facteurs (2FA), confirmation depuis une application Telegram connectée pour le code QR, ou importation d’une session autorisée prise en charge.
6. Vérifiez l'identifiant du compte affiché. **Sources** ouvertes : vos discussions se chargent automatiquement ; ajoutez vos groupes.
7. Sous « **Choisissez les modifications à conserver** », sélectionnez des catégories d’événements ou le préréglage « **Messages, modifications et suppressions** », puis enregistrez les paramètres de surveillance.
8. Sélectionnez séparément les paramètres des pièces jointes, puis cliquez sur « **Démarrer l'observation** ».

Les identifiants API permettent d’identifier votre application ; ils n’autorisent pas en soi l’accès à un compte. Les groupes privés ne nécessitent pas de nom d’utilisateur public, mais votre compte doit disposer d’un accès.

Pour les comptes existants, consultez [comptes et formats de session](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/) : le panneau accepte Telethon StringSession, SQLite Telethon/Pyrogram, les archives ZIP TData à compte unique et les fichiers JSON de compte pris en charge. Sélectionnez ensemble une session et son fichier JSON associé, puis appuyez sur **Connecter un compte**. La connexion par code QR est également disponible avec les mêmes paramètres d'API facultatifs. TDLib, les sessions de bots et les inventaires de comptes CSV/JSON ne sont pas pris en charge.

Pour plusieurs comptes, utilisez **Comptes → Importer des comptes** et sélectionnez leurs fichiers de session pris en charge. Les fichiers JSON associés sont appariés selon leur nom de base ; chaque compte importé obtient son propre espace de travail. Consultez [importation en masse et groupes de comptes](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#bulk-import-and-account-groups).

Pour ajouter un autre compte, appuyez sur **+** à côté du sélecteur de compte ou ouvrez **Compte → Paramètres → Paramètres de connexion → Espaces de travail**, ou utilisez **la rubrique Comptes**. Les espaces de travail disposent de sessions, de journaux, de clés, de sources et de files d’attente distincts. Le changement de vue ne modifie pas le fonctionnement des autres collecteurs. Un même compte Telegram ne peut pas être attribué à deux espaces de travail dans cette installation. Il n’y a pas de nombre fixe d’espaces de travail ; ceux-ci partagent un seul processus, leur capacité dépend donc de la machine.

Le jeton de panel en direct protège l’accès à vos autorisations Telegram et à vos données enregistrées ; il est distinct des identifiants de l’API Telegram. Seule une démo locale explicitement lancée et à laquelle on accède directement bénéficie d’une connexion automatique. Une démo à distance ou via un proxy utilise toujours `data/demo/panel-token.txt`.

## Vérification et exportation

- **Journal :** recherchez et filtrez les observations par source et par type d'événement.
- Sélectionnez un événement pour consulter son enregistrement d'origine, ses informations d'attribution et ses versions sauvegardées.
- Les détails de modification indiquent le contenu disponible avant et après la modification. Les détails de suppression indiquent le dernier contenu capturé, le cas échéant ; un acteur inconnu reste inconnu.
- **Formats d'exportation :** ZIP signé, JSONL, CSV et HTML hors ligne.
- **Exportation complète**d’une **conversation** (Sources → Exportation complète d’une conversation) : téléchargez l’intégralité de l’historique visible d’une conversation sous la forme d’un ensemble signé avec `chat.json` (au format Telegram-export) et d’un fichier lisible `chat.html`. Les conversations privées fonctionnent lorsque le compte est membre. Il s’agit d’un instantané actuel, et non d’une reconstitution des messages supprimés ou précédemment modifiés. Vérifiez une copie à l’aide d’`python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`.
- **Point de contrôle à retenir :** veillez à ce que les limites du journal signé ne soient pas incluses dans le collecteur.
- **Télécharger le reçu d'exécution signé :** conservez l'historique du programme et de la version du collecteur.
- **Préparer une demande d’horodatage :** préparez une demande hors ligne auprès d’une autorité d’horodatage ; suivez les instructions du fichier [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/timestamp/) pour obtenir et vérifier une réponse.
- **Vérification du journal :** vérifiez les signatures des événements et les liens de la chaîne. L'exportation au format ZIP permet également de vérifier les fichiers multimédias.

Les navigateurs pris en charge enregistrent les exportations volumineuses directement dans le fichier de votre choix. Les autres navigateurs mettent en mémoire tampon au maximum 128 MiB. Lorsque le serveur est en cours d’exécution, l’interface CLI de streaming prend en charge des téléchargements plus volumineux sans mettre en mémoire tampon l’intégralité de la réponse :

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Pour un autre espace de travail, ajoutez `--profile ID` via **Exportations → ID de l’espace de travail**. Pour un serveur distant, ajoutez `--url https://your-server`. La limite de transfert par défaut est de 5 GiB ; `--max-mib` permet de la modifier. Le contenu ZIP signé dispose d’une limite de vérification distincte de 4 GiB en format non compressé par défaut (**la commande « Paramètres »** permet de l’augmenter ; vérifiez ces archives à l’aide de `verify.py --max-gib N`). Vérifiez l’archive à l’aide d’une copie fiable du vérificateur et d’une empreinte de clé ou d’un point de contrôle conservé de manière indépendante.

## Consultez la procédure d'installation

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` vérifie les dépendances locales, la prise en charge de la signature, le stockage, la configuration des clés et l’adresse d’écoute. Il n’installe rien et ne se connecte pas à Telegram. Un port occupé peut signifier qu’une autre instance est en cours d’exécution. Utilisez un autre `--port` ou arrêtez-le d’abord.

Le programme de lancement s'installe dans `.venv`. Les commandes auxiliaires `python -m tgwitness...` doivent utiliser `.venv\Scripts\python.exe` sous Windows ou `.venv/bin/python` sous Linux/macOS, à moins que cet environnement ne soit déjà activé.

## Sessions, protection et fonctionnement

Un fichier Telethon SQLite `.session` fermé et cohérent peut être converti localement à l’aide de `python -m tgwitness.sessions account.session --out account.tgwitness-session`, puis chargé dans Account. L’importation directe de fichiers et la connexion par code QR sont également disponibles. Consultez [le fichier CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/) pour connaître les formats de connexion, SOCKS5, HTTP CONNECT, MTProxy et les clés principales externes.

**La mise en pause de la surveillance** interrompt la collecte. **Le verrouillage** ne fait que fermer l’accès au navigateur. La fermeture d’un onglet laisse le processus de collecte en cours d’exécution. L’arrêt du processus interrompt la collecte ; un instantané de l’historique ne permet pas de reconstituer toutes les modifications ou suppressions manquées. Découvrez [le fonctionnement de la collecte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/) en ce qui concerne les règles d’événements, les files d’attente de pièces jointes, l’isolation des comptes et le comportement en cas de redémarrage.

Les sessions et les secrets sont chiffrés. Le contenu des messages, les fichiers multimédias et les exportations nécessitent un disque ou un volume chiffré. Les signatures garantissent l’intégrité par rapport à une clé de confiance ; elles ne garantissent pas l’origine Telegram ni n’empêchent la falsification par un opérateur qui contrôle le collecteur et sa clé.

Consultez [le fichier OPERATIONS.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/operations/) pour la sauvegarde et la restauration, [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/deployment/) pour l’hébergement, et [la page deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) pour des exemples d’utilisation. Le panneau d’installation comprend également un guide de configuration hors ligne à l’adresse `/guide.html`.

Les vérifications effectuées et les limites restantes sont consignées dans [les fichiers VERIFICATION.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/) et [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md).
