# Installation, vérification et mise à jour

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/installation/

Installez-le en une seule commande, vérifiez les signatures et les hachages, mettez à jour et désinstallez l&#x27;application.

[Projet](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Mise en route rapide](https://phishdestroy.github.io/TgWitness/fr/docs/reference/quickstart/) · [Déploiement](https://phishdestroy.github.io/TgWitness/fr/docs/reference/deployment/)

## Installation en une seule commande

Le programme d'installation guidé inclut un environnement d'exécution Python privé. Utilisez la même adresse pour les futures installations : chaque publication met à jour le programme d'installation, les hachages, les signatures et les informations de compilation.

**Linux / macOS (Bash) :**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Sur un serveur Ubuntu, exécutez la commande en tant qu'administrateur pour installer un service en arrière-plan. Sur un ordinateur de bureau, exécutez la commande en tant qu'utilisateur normal.

**Windows (PowerShell ou Invite de commandes) :**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Aucun administrateur n’est nécessaire sous Windows. Le processus enfant PowerShell laisse votre terminal ouvert avec le résultat. Python et ses dépendances restent dans le répertoire d’installation.

Sous Ubuntu, choisissez « **Cet ordinateur** », « **Lien HTTPS temporaire »** ou « **Propre domaine** ». Le programme d'installation affiche l'adresse du panneau et la clé d'accès. Pour obtenir un lien temporaire, ouvrez cette adresse HTTPS dans votre navigateur et saisissez la clé. En cas d'accès local sur un serveur distant , utilisez un transfert SSH depuis votre ordinateur (`ssh -L 8787:127.0.0.1:8787 user@server`) et ouvrez `http://127.0.0.1:8787`. Sous macOS et Windows, le panneau local s’ouvre dans votre navigateur ; laissez son terminal en cours d’exécution.

Connectez-vous à Telegram dans le panneau et choisissez les éléments à collecter. L'installation seule ne lance pas la collecte sur Telegram.

## Là où tout fonctionne

`get.destroy.tools` Il s'agit d'un **Cloudflare Worker servant des téléchargements statiques**. Il ne contient ni panneau TgWitness, ni session Telegram, ni base de données de preuves utilisateur. Il n'est pas redirigé vers un VPS de projet. L'application s'exécute sur la machine où vous lancez la commande.

| Installation | Programme | Données |
| --- | --- | --- |
| Ubuntu en tant qu'administrateur | `/opt/tgwitness` | Service système : `/var/lib/tgwitness-<installation ID>`; utilisez `tgwitness paths` pour le chemin d'accès exact. |
| Utilisateur Linux / macOS | `~/.local/share/tgwitness` | `data/live` dans le cadre de cette installation. |
| Utilisateur Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` dans le cadre de cette installation. |

Cliquez `TGWITNESS_INSTALL_DIR` pour choisir un autre dossier. Les versions installées et les données sont séparées. Le programme d’installation ne télécharge pas vos comptes, messages ou clés vers le site de téléchargement. Choisir un tunnel Cloudflare achemine le trafic du panneau via Cloudflare ; utiliser votre propre domaine redirige vers votre propre serveur.

Chaque installation comprend les fichiers **START-HERE.html** et **START-HERE.txt**, contenant les chemins d'accès locaux, les commandes et les liens vers le dépôt. Exécutez `tgwitness guide` pour ouvrir le guide. Sous Windows, utilisez `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` dans PowerShell.

## Paramètres de recherche en texte intégral

[La recherche en texte intégral](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/) (aperçu) ne nécessite aucune configuration. Son index est créé en arrière-plan après une mise à jour.

| Variable ou commande | Effet |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | Par défaut : l'index est conservé dans `search/fulltext.sqlite3` de chaque espace de travail |
| `TGWITNESS_FULLTEXT=memory` | Pas de fichier d'index ; l'index est reconstruit à chaque démarrage |
| `TGWITNESS_FULLTEXT=off` | Pas d'index ; recherche par texte exact uniquement |
| `tgwitness index status` | Répertorier l'état de chaque espace de travail |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | Reconstruire tous les index à partir du journal signé |

Le choix de l’administrateur dans **Journal → Filtres → Index de recherche** remplace la variable pour cet espace de travail. Les commandes recherchent le répertoire de données de l’installation qui les exécute ; ailleurs, ajoutez `--data-dir` le chemin d’accès à partir de `tgwitness paths`. Pour disposer d'un dictionnaire ukrainien complet (données sous licence GPL-3.0), installez `pymorphy3-dicts-uk` dans l’ environnement Python de l’installation.

## Accès en ligne de commande

[La ligne de](https://phishdestroy.github.io/TgWitness/fr/docs/reference/cli/) [commande](https://phishdestroy.github.io/TgWitness/fr/docs/reference/cli/) (aperçu) analyse l'archive à la recherche de scripts et d'agents.

| Variable | Effet |
| --- | --- |
| `TGWITNESS_URL` | Adresse de la session `tgwitness search`, `context`, `messages`, `stats` et `export`; valeur par défaut `http://127.0.0.1:8787` lorsqu’un jeton est défini |
| `TGWITNESS_MCP_TOKEN` | Archiver le jeton de connexion depuis **Intégrations → MCP**, partagé avec les clients MCP ; `--token-file` le lit plutôt à partir d’un fichier |
| `TGWITNESS_DATA` | Le répertoire de données est lu directement lorsqu’aucun `--data-dir`, d’URL ou de jeton n’est fourni |

## Vérifier avant l'exécution

La commande d'une ligne fait confiance au protocole HTTPS pour son script initial. Ce script vérifie SHA-256 ainsi que la signature RSA du projet sur l'application et les contraintes avant l'installation. Vous pouvez également télécharger et vérifier le script initial au préalable.

La clé publique de publication est [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). Son SHA-256 est :

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Conservez cette empreinte provenant d'une révision du dépôt à laquelle vous faites confiance. Une somme de contrôle provenant du même serveur de téléchargement détecte toute divergence ; la clé publique, dont la fiabilité est vérifiée de manière indépendante, permet d'authentifier la signature d'une version.

Utilisez un nouveau répertoire vide pour les téléchargements de vérification ci-dessous.

**Linux / macOS — à exécuter dans un nouveau répertoire de téléchargement vide** (nécessite curl et OpenSSL) :

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

La `&&` chaîne s'arrête avant l'exécution si un téléchargement, une vérification d'empreinte de clé ou de signature échoue. Si une publication a lieu entre le téléchargement du script et sa signature, téléchargez à nouveau les deux. Les anciens programmes d'installation conservent leurs URL de paquets immuables.

**Windows — vérifiez l'SHA-256 avant de lancer l'application :**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Comparez le hachage avec la `install.ps1` ligne. Pour une vérification indépendante de la signature, utilisez OpenSSL (par exemple, depuis Git Bash) et la même empreinte de clé publique que ci-dessus :

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

L'installation sous Windows vérifie elle-même les signatures des paquets à l'aide de .NET et ne nécessite pas OpenSSL. Il s'agit de signatures détachées RSA-3072 / SHA-256, et non d'Authenticode. Le [manifeste](https://get.destroy.tools/manifest.json) enregistre la version du logiciel, le commit Git exact, l'ID de version immuable et l'SHA-256 de chaque artefact. La page renvoie vers la source correspondante. Le manifeste et la liste des sommes de contrôle comportent également des signatures détachées (`manifest.json.sig` et `SHA256SUMS.txt.sig`).

## Mettre à jour une installation existante

**Une nouvelle publication met à jour le site de téléchargement ; les programmes installés se mettent à jour lorsque vous relancez le programme d’installation.** Il n’y a pas de programme de mise à jour en mode silencieux ni de redémarrage automatique d’une collection en cours d’exécution. Le canal d’installation actuel est **« preview »** ; il suit les versions publiées et vérifiées provenant de `main`, dont le commit peut être plus récent que la dernière version numérotée sur GitHub. La version de la page provient de `pyproject.toml`; son commit et son identifiant de build permettent de distinguer les mises à jour au sein d’une même version « preview ».

Utilisez le même dossier d’installation et le même utilisateur du système d’exploitation que précédemment. Sauvegardez l’intégralité du répertoire de données une fois la collecte arrêtée ; `tgwitness paths` qui l’identifie. Une exportation signée ne constitue pas une sauvegarde complète de l’installation.

**Installation en tant qu’administrateur sur Ubuntu à l’adresse `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Une fois l'installation réussie :

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Pour une installation sur Linux/macOS, utilisez son `TGWITNESS_INSTALL_DIR` ou les paramètres par défaut, puis relancez la première commande d’installation. Fermez un panneau au premier plan avant la mise à jour, puis relancez-le après celle-ci. Pour un service Linux déjà configuré, exécutez sa `tgwitness restart` commande.

**Windows :** fermez le panneau en cours d'exécution, relancez la commande d'installation Windows, puis ouvrez `bin\tgwitness.cmd` dans la même installation. Le programme d’installation conserve les données, les sessions, les paramètres d’accès et les clés de signature. Il ne remplace le lanceur qu’une fois que le nouvel environnement a passé ses vérifications ; en cas d’échec de l’installation, l’ancien lanceur reste en place. Conservez la sauvegarde pré-mise à niveau en cas de modification du format de stockage.

## Commandes courantes sous Ubuntu

| Commande | Résultat |
| --- | --- |
| `tgwitness open` | URL actuelle du panneau et clé d'accès. |
| `tgwitness paths` | Chemins d'accès précis aux programmes, aux données et aux guides. |
| `tgwitness guide --print` | Mode d’emploi hors ligne. |
| `tgwitness status` / `tgwitness logs` | Disponibilité / journaux de service. |
| `tgwitness stop` / `tgwitness start` | Arrêter / redémarrer le service ; conserver les données. |
| `tgwitness token rotate` | Remplacer la clé d'administrateur et mettre fin aux sessions de navigateur. |
| `tgwitness tunnel off` | Désactivez le tunnel rapide public ; conservez le panneau local. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Créer un lien de tunnel rapide / remplacer son adresse. |

Consultez la section « [Accès »](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) pour les jetons de collègues, les sessions et les restrictions d’adresse IP, ainsi que la section « [Publication de l’installateur »](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) pour le workflow de publication de GitHub vers Cloudflare.

## Supprimer TgWitness

Il n'y a pas de programme de désinstallation : il suffit d'arrêter le panneau et de supprimer ses dossiers. La suppression du dossier « data » détruit définitivement les journaux, les clés de signature, les sessions Telegram et les fichiers enregistrés. Avant cela :

1. Exportez ce dont vous avez besoin (**Exports → Télécharger ZIP signé**) et conservez l’empreinte digitale de la clé de signature ainsi que les points de contrôle hors de cette machine. Pour conserver l’espace de travail lui-même, copiez l’intégralité du dossier de données après avoir arrêté la collecte.
2. Supprimez les serveurs créés sous « **Extras → Server 24/7 »** dans « **Vos serveurs »** ou via `python -m tgwitness.cloud destroy`; le fournisseur les facture jusqu’à ce qu’ils soient supprimés.
3. Mettez fin à la session de chaque compte dans Telegram via **Paramètres → Appareils**. La suppression des fichiers ne déconnecte pas la session côté Telegram.

**Installation en tant qu’administrateur sous Ubuntu.** Notez l’emplacement du dossier de données, arrêtez le service, puis supprimez le service, les dossiers et le raccourci :

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Installation pour les utilisateurs de Linux ou macOS.** Fermez le panneau. Un service utilisateur Linux configuré est arrêté avec `systemctl --user disable --now tgwitness-<ID>`; son unité se trouve dans `~/.config/systemd/user/`. Supprimez ensuite `~/.local/share/tgwitness` (ou votre `TGWITNESS_INSTALL_DIR`) ainsi que le `~/.local/bin/tgwitness` raccourci.

**Windows.** Fermez le panneau et supprimez `%LOCALAPPDATA%\TgWitness` (ou votre `TGWITNESS_INSTALL_DIR`). Le programme d'installation n'ajoute ni service, ni tâche planifiée, ni raccourci.
