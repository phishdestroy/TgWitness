# Déploiement

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/deployment/

Exécutez TgWitness en tant que service sous Windows, Linux, macOS ou Docker, via HTTPS, avec des sauvegardes et des mises à jour.

**Anglais** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [Ukrainien](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [Portugais (Brésil)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [Urdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [हिन्दी](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [Bahasa Indonesia](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [Chinois simplifié](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## Choisissez une installation

Pour le package portable, extrayez le fichier « `TgWitness-<version>-windows-amd64-portable.zip` » depuis GitHub Releases. Pour les autres méthodes, téléchargez et extrayez le fichier ZIP source ou clonez le dépôt, puis exécutez la commande suivante depuis le répertoire du projet :

| Installation | Début | Fonctionne-t-il en arrière-plan ? |
| --- | --- | --- |
| Pack portable pour Windows | `TgWitness.cmd` | Non ; veuillez laisser la fenêtre ouverte. |
| Natif Windows | `Start.cmd` | Non ; utilisez la tâche de connexion facultative pour une exécution en arrière-plan. |
| Natif sous Linux/macOS | `sh start.sh` | Non ; utilisez systemd/launchd pour une exécution en arrière-plan. |
| Docker sur n'importe quel hôte pris en charge | `docker compose up -d --build --wait` | Oui, tant que le démon Docker est en cours d'exécution. |
| Aide à l'utilisation de Docker sous Windows | `scripts\Docker.cmd` | Oui ; l’assistant attend que le serveur web soit opérationnel. |
| Aide à l'utilisation de Docker sous Linux/macOS | `sh scripts/docker-start.sh` | Oui ; l’assistant attend que le serveur web soit opérationnel. |

Pour un serveur cloud pouvant être vérifié par un tiers — créé via l’ API du fournisseur, sans SSH, accessible uniquement via un tunnel Cloudflare —, veuillez consulter la section « [Déploiement à haute sécurité](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md) ».

Le démarrage natif crée un fichier « `.venv` » privé et installe les dépendances épinglées. Docker les compile au sein de l’image, sans nécessiter Python sur l’hôte. La première configuration nécessite un accès à Internet. Si aucune version de Python 3.11 ou supérieure n’est détectée, `Start.cmd` vous demande votre accord avant d’installer Python 3.12 pour l’utilisateur Windows actuel (via winget, ou bien via le programme d’installation de python.org après vérification de la signature de la Python Software Foundation) ; il ne demande jamais de droits d’administrateur. Docker et les services du système d’exploitation restent des prérequis.

Les installations natives et portables utilisent « `data/live` » dans leur dossier. Docker utilise le volume nommé « `tgwitness-data` » à l’emplacement « `/data` ». Il s’agit d’installations distinctes jusqu’à ce que vous migriez délibérément l’ intégralité du répertoire de données. Ne vous attendez pas à ce qu’un nouveau conteneur Docker détecte automatiquement les comptes natifs.

## Configuration requise

L'installation native nécessite Python 3.11 ou une version ultérieure avec `venv` et `ensurepip`, un accès à Internet pour l'installation de la première dépendance, ainsi qu'un répertoire de projet accessible en écriture pour `.venv`. Le panneau fourni ne nécessite ni Node.js ni compilation front-end. Lancez le programme de démarrage depuis votre compte habituel sur le système d'exploitation ; TgWitness ne requiert pas de droits d'administrateur ou de root.

- **Windows :** `Start.cmd` vérifie `py -3`, puis `python`, puis les dossiers d’installation par défaut par utilisateur et « Program Files », et nécessite la version 3.11 ou une version ultérieure. Si aucune de ces options ne fonctionne, il propose l’installation automatique par utilisateur décrite ci-dessus. `py -3 start.py` fonctionne également. Le package portable ne nécessite pas du tout Python.
- **Linux :** `start.sh` tente `python3.13`, `python3.12`, `python3.11`, `python3` et `python`, puis affiche la commande d'installation pour apt, dnf, pacman, zypper, apk ou Homebrew lorsqu'aucune ne correspond. Les installations Debian/Ubuntu peuvent nécessiter le paquet `python3-venv` correspondant à l'interpréteur sélectionné. L'ancienne version par défaut de Python d'une distribution doit être remplacée ou complétée par Python 3.11 ou une version ultérieure.
- **macOS :** installez une distribution Python 3.11+ à jour ; ne partez pas du principe qu’un interpréteur fourni par le système d’exploitation répond aux exigences. Utilisez `python3 start.py` depuis le répertoire du projet.
- **Docker :** utilisez Docker Engine/Desktop avec Compose v2.20 ou une version plus récente. Docker Desktop doit utiliser des conteneurs Linux sous Windows. Le conteneur installe ses propres dépendances Python ; l'hôte n'a pas besoin d'une installation Python distincte.

Utilisez un stockage local persistant pour le répertoire de données. Prévoyez la capacité nécessaire en fonction du nombre de messages, des fichiers multimédias, de la croissance du WAL, des exportations et des sauvegardes ; il n’existe pas de spécification minimale universelle, fondée sur des preuves, en matière de disque dur ou de mémoire vive pour chaque charge de travail. Les architectures CPU et les versions de Python ne disposant pas de roues de dépendances compatibles peuvent nécessiter des outils de compilation supplémentaires ainsi que leur propre qualification. Le terme « portable » ne signifie pas une prise en charge universelle de tous les systèmes d’exploitation ou de tout le matériel.

La compatibilité avec Windows 11/Python 3.12 a été vérifiée localement. Les définitions pour Linux/macOS/conteneurs ainsi que l’environnement de CI sont fournies, mais n’ont pas été exécutées sur cet hôte de développement. Veuillez consulter [le fichier VERIFICATION.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/) pour connaître la portée exacte.

## Ordinateur local

Utilisez `Start.cmd` sous Windows ou `sh start.sh` sous Linux/macOS. `scripts\Setup.cmd` ou `sh start.sh --setup-only` permet de préparer l’environnement. Le lanceur installe les dépendances lors de la première utilisation ; les lancements suivants réutilisent l’environnement. Un accès à Internet est nécessaire pour la configuration et la collecte des données Telegram, mais la consultation des enregistrements existants et la création d’exportations fonctionnent hors ligne.

Exécutez la commande « `python start.py --check` » après l’installation pour vérifier les dépendances locales, Ed25519, le stockage, la configuration des clés et l’adresse d’écoute sans démarrer de collecteur. Utilisez `--json` pour obtenir une sortie structurée. Transmettez les commandes `--data-dir`, `--host` et `--port` prévues. Cette vérification n’installe pas de paquets, ne crée pas de journal et ne se connecte pas à Telegram ; il ne s’agit pas d’une qualification d’intégrité ou de couverture. Le démarrage vérifie séparément les journaux existants. `python start.py --help` évite également toute installation.

Options :

Après avoir exécuté start.py, lancez les commandes auxiliaires avec `.venv\Scripts\python.exe` sous Windows ou `.venv/bin/python` sous Linux/macOS, ou activez d'abord cet environnement. Les exemples `python -m ...` ci-dessous partent du principe que l'environnement est actif.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

Variables d’environnement : TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE permet de sélectionner le mode « clé externe » pour une nouvelle installation ; voir ci-dessous. TGWITNESS_TOKEN, s’il est fourni, doit contenir au moins 24 caractères ; utilisez une valeur aléatoire cryptographique. En son absence, l’application génère un jeton aléatoire de 256 bits dans le fichier panel-token.txt. La redéfinition via les variables d’environnement ne réécrit pas ce fichier. Redémarrez pour renouveler les identifiants.

Un seul processus à la fois peut être propriétaire d’un répertoire de données. Un verrouillage de fichier multiplateforme au niveau du système d’exploitation empêche les écritures simultanées accidentelles. Utilisez un seul worker Uvicorn. Le panneau de configuration permet de gérer un nombre illimité d’ espaces de travail, avec des répertoires d’espaces de travail supplémentaires sous profiles/<id>/. Pour des instances de service distinctes, utilisez des répertoires et des ports distincts. Les fichiers WAL de SQLite doivent être stockés sur un support de stockage local persistant , et non sur un système de fichiers réseau. Ne partagez pas un même volume entre les répliques.

## Pack portable pour Windows

Chaque version GitHub comprend `TgWitness-<version>-windows-amd64-portable.zip` et son `.sha256`. Elle contient le runtime Python 3.12 officiel intégrable provenant de python.org (somme de contrôle fixée dans `tools/build_portable.py`), TgWitness et ses dépendances fixées, ainsi que trois lanceurs :

| Fichier | Objectif |
| --- | --- |
| `TgWitness.cmd` | Lancez le panneau ; les options supplémentaires sont transmises, par exemple `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Lancez la démo synthétique à l'adresse `data\demo` |
| `TgWitness-Check.cmd` | Lancez le contrôle de préparation sans démarrer |

Décompressez l'intégralité de l'archive dans un dossier accessible en écriture, tel que « `Documents\TgWitness` » ; ne l'exécutez pas à partir du fichier ZIP ni du dossier « Program Files ». L'environnement d'exécution utilise un chemin d'accès isolé aux modules, de sorte que les autres installations Python et le dossier « `PYTHONPATH` » n'ont aucune incidence sur son fonctionnement. Les données sont conservées dans le dossier « `data` » du package. Pour effectuer une mise à jour, arrêtez TgWitness, extrayez la nouvelle version dans un nouveau dossier, puis copiez-y le dossier « `data` ».

Compilez-le vous-même sous Windows 64 bits avec Python 3.12 :

```
python tools/build_portable.py
```

Le générateur vérifie la somme de contrôle d'exécution, installe les dépendances restreintes dans le paquet, effectue le contrôle de préparation à l'aide de l'interpréteur intégré, puis enregistre le fichier ZIP et la somme de contrôle dans `dist/`.

## Conteneur

```
docker compose up -d --build --wait
```

Cela crée un volume persistant nommé pour /data. Le port web est mappé sur 127.0.0.1:8787. Le processus s’exécute sous l’UID 10001 avec des capacités restreintes, un système de fichiers racine en lecture seule, et des répertoires /data et /tmp accessibles en écriture. `--wait` vérifie l’état de santé du serveur web avant de renvoyer une réponse ; il n’établit pas d’ autorisation ni de livraison Telegram. Les utilitaires fournis utilisent un délai d’attente de disponibilité de 180 secondes après la compilation. Le téléchargement initial des dépendances peut prendre plus de temps.

Les deux fichiers Compose de base utilisent le nom de projet « `tgwitness` » ; par conséquent, l’extraction d’une nouvelle version dans un autre répertoire ne sélectionne pas automatiquement un nouveau volume de données. Ne conservez qu’un seul déploiement actif pour ce projet. Pour les installations indépendantes, utilisez un « `docker compose -p NAME ...` » unique et un port hôte différent, et conservez les deux lors des mises à jour. Pour un déploiement plus ancien utilisant un nom de projet différent, continuez à utiliser son nom d’origine avec « `-p` » ; « `docker compose ls` » répertorie les projets existants.

Copiez `deploy/env.example` vers `.env` et modifiez `TGWITNESS_PORT` pour utiliser un autre port de bouclage. Par exemple, `TGWITNESS_PORT=8788` expose le panneau à l'adresse `http://127.0.0.1:8788` ; le conteneur reste à l'écoute sur le port 8787. `.env` est ignoré par Git.

Récupérer le jeton initial :

```
docker compose exec tgwitness cat /data/panel-token.txt
```

Commandes utiles :

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` redémarre le collecteur après un plantage ou un redémarrage du démon Docker . Sur un serveur Linux, activez Docker au démarrage à l’aide du gestionnaire de services de votre distribution , généralement `sudo systemctl enable --now docker`. Sous Windows/macOS, activez le paramètre « Démarrer à la connexion » de Docker Desktop. La déconnexion du bureau, la mise en veille ou l’arrêt du peuvent interrompre la collecte. Un conteneur explicitement arrêté reste arrêté jusqu’à ce que vous le redémarriez.

Dans la configuration d’exemple, le volume /tmp est limité à 512 Mio. La construction de l’exportation utilise plutôt le répertoire `temporary-exports/` de chaque espace de travail sur le répertoire persistant /data. Réservez de l’espace à cet endroit pour les exportations simultanées, la croissance du journal/WAL, les fichiers multimédias et les sauvegardes. Le lanceur utilise le fichier deploy/constraints.txt pour fixer les versions des dépendances d’exécution requises. Les serveurs Docker et à haute sécurité s’installent à partir des fichiers deploy/requirements.lock et deploy/build.lock avec pip --require-hashes : chaque fichier de paquet doit correspondre à une valeur SHA-256 enregistrée dans le commit, de sorte qu’un fichier remplacé sur PyPI ou un miroir est refusé. L’image de base Python et les paquets du système d’exploitation nécessitent toujours une qualification de version indépendante.

N’utilisez pas la commande « docker compose down -v » sauf si vous avez l’intention de détruire le journal et les clés. Le rapport d’état du conteneur indique la disponibilité du serveur web, et non la réussite de la capture des messages Telegram. Vérifiez l’état du collecteur, le signal de vie, les erreurs et les événements de couverture dans le panneau de contrôle.

### Profil d’un témoin indépendant

Le service optionnel « `witness` » exécute un [témoin indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/) dans son propre conteneur, avec sa propre clé et son propre journal dans le volume « `witness-data` », et uniquement un jeton de témoin en lecture seule pour le collecteur. Créez le jeton sur la page **« Witness »** du panneau de configuration, ajoutez-le avec un jeton de bot et un canal à « `.env` », puis lancez le profil :

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

Le service accède au collecteur au sein du réseau Compose à l’adresse `http://tgwitness:8787` (`TGWITNESS_WITNESS_COLLECTOR` le remplace, par exemple `/profiles/<workspace ID>` pour un autre espace de travail). Pour un témoin hébergé sur un serveur distinct, géré par un tiers, utilisez `deploy/compose/compose.witness.yaml` et définissez `TGWITNESS_WITNESS_COLLECTOR` sur l’adresse HTTPS du collecteur ; ce fichier ne contient que le témoin.

## Installez une image publiée

Ce site devient accessible une fois le [workflow de publication](https://phishdestroy.github.io/TgWitness/fr/docs/reference/deployment/#automated-github-releases) validé et la configuration publique du package GHCR effectuée. Le nom du propriétaire du dépôt n’est pas codé en dur dans cet arborescence source. Veuillez vous référer à l’image figurant dans le résumé du workflow de cette version.

Copiez `deploy/env.example` vers `.env`. Définissez `TGWITNESS_IMAGE` sur la version publiée, en utilisant le chemin d'accès au dépôt **en minuscules**, par exemple :

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.0
TGWITNESS_PORT=8787
```

Exécutez ce fichier seul, à la place de `compose.yaml` :

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

Aucune compilation à partir du code source, ni Python, ni compilateur n’est nécessaire sur l’hôte. Le workflow de publication cible les conteneurs Linux AMD64 et ARM64, y compris la machine virtuelle Linux de Docker Desktop. Utilisez une balise de version ou « `ghcr.io/owner/repository@sha256:...` » issue du résumé du workflow. Aucune configuration de balise « `latest` » mobile ni de mise à niveau automatique de l’application n’est prévue. L’ image et les variantes de source utilisent le même volume de données lorsque leur nom de projet correspond.

## HTTPS automatique sur un serveur

Utilisez un serveur équipé de Docker, un nom de domaine que vous contrôlez et un stockage local persistant. Orientez les enregistrements A/AAAA du domaine vers le serveur ; ne publiez l’enregistrement AAAA que si l’IPv6 y accède. Autorisez le trafic entrant sur les ports TCP 80 et 443, ainsi que le trafic sortant DNS/HTTPS pour l’émission de certificats. Ces ports ne doivent pas être déjà utilisés par d’autres services.

Copiez `deploy/env.example` vers `.env` et définissez un nom d'hôte, sans schéma ni chemin d'accès :

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

Lancez la compilation du code source avec la superposition HTTPS :

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

Pour une image publiée, utilisez plutôt `deploy/compose/compose.image.yaml` comme premier fichier. Conservez les deux arguments `-f` pour les commandes ultérieures de statut, de journalisation, de mise à jour et d’arrêt.

Caddy obtient et renouvelle un certificat, redirige le trafic HTTP vers HTTPS et transmet les requêtes au collecteur sur le réseau privé Compose. L’état du certificat dispose de son propre volume persistant. Le port hôte direct du collecteur reste réservé au loopback. La configuration Caddy fournie n’active pas la journalisation des accès.

Ouvrez `https://watch.your-domain.org` et saisissez le jeton du panneau. La vérification de l’état de préparation ne confirme ni la délivrance d’un certificat ni l’accessibilité externe. Si le protocole HTTPS n’est pas prêt, vérifiez le DNS, les règles du pare-feu, ainsi que :

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

L'image Caddy fournie porte le tag « `2-alpine` ». La commande « pull » actualise cette image ; épinglez un résumé testé dans votre déploiement si vous avez besoin de versions fixes de l'infrastructure.

## Mises à jour et sauvegardes

Conservez le nom du projet « Compose » et le volume de données lors des mises à jour. Arrêtez d’abord le collecteur et effectuez une sauvegarde complète. Pour le déploiement par défaut à partir du code source :

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Utilisez à chaque fois une nouvelle destination de sauvegarde, en dehors du référentiel, et protégez-la comme du matériel d’accès au compte. Le chemin d’accès indiqué à titre d’exemple est donné à titre indicatif ; utilisez votre propre emplacement de sauvegarde privé. Copiez l’intégralité du répertoire, y compris les fichiers cachés, tous les espaces de travail, les clés, les journaux et les fichiers multimédias. Sauvegardez séparément la clé principale du coffre-fort externe si celle-ci est configurée. Un fichier ZIP de preuves n’est pas une sauvegarde d’application restaurable. Pour le protocole HTTPS, conservez également les volumes Caddy si vous devez préserver l’état de son certificat ou de son compte.

Pour un déploiement à partir du code source, procurez-vous les fichiers de la nouvelle version et exécutez la commande suivante :

```
docker compose up -d --build --wait
```

Pour le déploiement d’une image, remplacez `TGWITNESS_IMAGE` par la version souhaitée, puis exécutez :

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Utilisez également le ou les fichiers Compose de votre installation pour les commandes « stop » et « copy » ci-dessus. Conservez `.env`, la configuration personnalisée et le même nom de projet. `down` conserve les volumes nommés ; **`down -v` les supprime**. Ne copiez pas `.venv` d’un système d’exploitation à l’autre ni d’une version de Python à l’autre. Pour les mises à jour natives, arrêtez TgWitness, sauvegardez l’intégralité de son répertoire de données, remplacez les fichiers source, puis exécutez `python start.py --setup-only` avant le redémarrage.

Vérifiez l’accès au panneau de configuration, l’identité du compte, l’état de l’observation et la couverture après une mise à jour. Le redémarrage ne permet pas de reconstituer les mises à jour Telegram manquées. Une restauration peut nécessiter la sauvegarde antérieure à la mise à jour si une version future modifie les formats de stockage.

## Publications automatisées sur GitHub

Le [workflow de publication](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml) est prêt à l’emploi dès que ce projet est poussé vers un dépôt GitHub sur lequel les Actions sont activées. Il s’exécute lorsqu’une version GitHub est **publiée**, y compris une préversion. Les brouillons et les poussées de balises ne suffisent pas à eux seuls à publier des paquets.

1. Définissez la version du paquet et le journal des modifications, puis publiez une version portant le tag « `v` » suivi de la version exacte « `pyproject.toml` », par exemple « `v0.7.0` ».
2. Le workflow valide le tag et exécute les vérifications communes à Windows/Linux/macOS concernant Python, general/account-import/QR browser, le paquet source et Docker. Une nouvelle installation native est également effectuée sur les trois systèmes d'exploitation à l'aide de Python 3.12.
3. Une fois ces vérifications réussies, il effectue des tests de fonctionnement sur une image ARM64 sous QEMU, publie les images AMD64/ARM64 sur `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>`, et joint le fichier ZIP source, la somme de contrôle et le fichier Python wheel à la version. Une tâche distincte sous Windows compile et joint le fichier ZIP portable ainsi que sa somme de contrôle.
4. Après la première publication, ouvrez les paramètres du paquet GHCR et définissez la visibilité sur **« Public »** si vous souhaitez permettre le téléchargement anonyme d’images. Un dépôt source public ne garantit pas à lui seul un paquet de conteneur public. Les politiques de l’organisation doivent autoriser la publication du paquet. Le workflow utilise `GITHUB_TOKEN` ; aucun mot de passe de registre ni aucun identifiant VPS ne doit figurer dans le dépôt.

Le bon fonctionnement à distance n’a pas été validé par cette préparation locale. L’émulation ARM64 constitue un test de fonctionnement de base, et non une qualification sur matériel natif ou en environnement Telegram réel. Cela automatise la création des paquets de version ; le démarrage d’un serveur nécessite toujours la commande « Compose » et ses prérequis en matière de domaine et d’hôte. Les serveurs existants ne sont pas mis à jour ni redémarrés en arrière-plan lorsqu’une nouvelle version est publiée.

## Serveur distant

Limitez le service au loopback et utilisez un tunnel SSH, ou terminez la connexion HTTPS au niveau d’un proxy inverse. Le fichier Compose de base est accessible uniquement en local ; la superposition optionnelle `deploy/compose/compose.https.yaml` fournit Caddy pour un domaine configuré. Veillez à ce que le jeton « bearer » n’apparaisse pas dans les URL ni dans les journaux du proxy. Un proxy inverse doit limiter la taille des requêtes et le débit des connexions. N’exposez pas le protocole HTTP en clair sur Internet.

Des exemples concernant systemd, une tâche de connexion Windows, un agent utilisateur macOS et Caddy sont fournis dans [le répertoire deploy/.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Vérifiez et adaptez leurs chemins d’accès avant l’installation. Il s’agit de modèles fournis, et non de configurations de plate-forme exécutées localement. Aucun service ou tâche en arrière-plan n’est enregistré par le lanceur standard.

Sous Windows, un lancement de `pythonw.exe` sans fenêtre stocke les diagnostics de démarrage et du serveur dans `logs/server.log`, sous le répertoire de données (5 Mio par fichier, deux sauvegardes en rotation). Les lancements en mode console conservent les journaux de la console. La journalisation des accès HTTP est désactivée dans les deux modes. Protégez les journaux avec le répertoire de données et examinez-les avant de les partager.

## Redémarrage et lacunes

Le dernier état d’observation demandé est conservé. Si l’observation était active, le démarrage tente de se reconnecter et de reprendre les sources sélectionnées. Une mise en pause manuelle annule cette intention. Un redémarrage ayant échoué est enregistré et affiché dans le panneau.

StringSession conserve l’autorisation, mais pas l’état durable des mises à jour/entités de Telethon. Les dialogues sont rechargés au démarrage. Telegram/Telethon peut récupérer certaines interruptions de transport pendant son exécution, mais TgWitness ne garantit pas une relecture durable après un redémarrage du processus. À chaque démarrage, le journal enregistre l’en-tête du journal précédent et la limite hors ligne. Le moniteur vérifie la connectivité toutes les 10 secondes et ajoute un signal de présence toutes les minutes (**Paramètres → Enregistrement de présence toutes les**). De brèves interruptions peuvent passer inaperçues ; un transport connecté ne garantit pas la transmission complète des mises à jour. Les instantanés sont des observations explicites de l’historique actuel, et ne servent en aucun cas à combler des lacunes.

La file d’attente des médias est stockée dans la base de données SQLite de chaque espace de travail. Un message et sa tâche sont validés de manière atomique. Les tâches en cours d’exécution qui ont été interrompues sont récupérées pour être relancées au démarrage. Chaque téléchargement dispose d’un délai d’expiration de base de 120 secondes, auquel s’ajoute un temps de téléchargement à 256 KiB/s en fonction de sa taille, ainsi qu’une limite comprise entre 1 et 2 000 MiB par type de pièce jointe ; le délai d’expiration, la vitesse et le nombre de tentatives sont configurables dans **les paramètres**. Le collecteur ignore les fichiers dont la taille est inconnue. La mise en pause conserve les tâches en file d’attente. La nouvelle tentative utilise le descripteur de fichier d’origine tel qu’il a été observé, et non la dernière version d’un message modifié par la suite. Les échecs temporaires font l’objet d’un nombre limité de nouvelles tentatives ; les mises en pause de FloodWait pour les médias sont conservées après un redémarrage. La récupération des médias est distincte de la récupération des mises à jour des télégrammes et ne permet pas de recréer les fichiers disparus.

## Sauvegarde, restauration et capacité

Arrêtez le processus avant de copier **l’intégralité** du **répertoire de données**, y compris les fichiers vault.key, signing.enc, credentials.enc, la base de données SQLite et les fichiers WAL, les médias, le jeton, les points de contrôle, ainsi que tous les profils et sous-répertoires. Restaurez la copie complète pendant que le service de destination est arrêté. L’absence de clés de coffre-fort ou une non-correspondance des clés de signature entraînent l’échec du démarrage ; ne régénérez pas les clés pour forcer l’accès.

Conservez les sauvegardes secrètes chiffrées et soumises à un contrôle d’accès. Les fichiers ZIP de preuves sont des artefacts d’analyse portables, et non des sauvegardes d’application ou de session Telegram. Il n’y a pas de suppression automatique après une certaine durée de conservation. Prévoyez suffisamment d’espace disque pour tous les messages, les métadonnées brutes, les fichiers multimédias, les exportations temporaires et les sauvegardes.

La vérification et l’exportation des enregistrements en continu permettent d’éviter de charger l’intégralité du journal. Une exportation fige un instantané lu tandis que les nouvelles écritures WAL peuvent se poursuivre ; les exportations de longue durée peuvent conserver des pages WAL, de sorte que la capacité du disque reste un facteur important. Les fichiers ZIP sont plafonnés à 4 Gio non compressés afin de correspondre à la valeur par défaut du vérificateur indépendant ; **Paramètres → « Plus grand fichier ZIP signé »** augmente cette limite, et ces archives sont vérifiées à l’aide de l’`verify.py --max-gib N`. Les autres formats ne sont soumis à aucune limite de nombre d’événements. Les navigateurs pris en charge transmettent les blocs de réponse en continu vers un fichier sélectionné par l’utilisateur. Les autres navigateurs mettent en mémoire tampon au maximum 128 MiB et redirigent les transferts plus volumineux vers l’interface CLI authentifiée :

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Utilisez `--profile ID` dans **Exports → Workspace ID** pour un autre espace de travail, `--format zip|jsonl|csv|html` ou `--url https://your-server` pour un serveur distant, ou `--max-mib` pour modifier la limite de transfert de 5 GiB. Le protocole HTTP simple n’est autorisé que pour le loopback. Les jetons transitent dans les en-têtes, les redirections sont refusées, les fichiers existants ne sont pas écrasés et les téléchargements incomplets ne sont pas publiés comme des fichiers terminés. Si TGWITNESS_TOKEN remplace le jeton généré, utilisez un fichier protégé séparément contenant cette valeur active : panel-token.txt n’est pas réécrit par la substitution. Le SHA-256 de la commande n’est qu’une somme de contrôle de transfert ; vérifiez indépendamment le fichier ZIP signé.

Les fichiers d’exportation du serveur restent dans le répertoire privé « `temporary-exports/` » de chaque espace de travail. Les exportations réussies effacent leurs fichiers. Les exportations interrompues sont supprimées au prochain démarrage de l’espace de travail, son verrou d’instance exclusif étant maintenu. Ce répertoire fait partie du modèle de menace/capacité de stockage ; utilisez un volume de données chiffré. Les transferts à l’échelle de production de plusieurs gigaoctets nécessitent toujours une validation sur votre système cible.

Le panneau affiche les médias en file d’attente ou ayant échoué, les médias en attente les plus anciens, l’espace disque disponible, les suspensions de requêtes Telegram, ainsi que les sources dont l’accès n’est pas confirmé. Ces diagnostics ne constituent pas un outil complet de surveillance de la transmission de bout en bout. Les espaces de travail partagent un même processus ; un compte générant beaucoup de trafic peut tout de même affecter les autres. Les processus de travail distincts, la conservation/rotation, la récupération durable des mises à jour et la qualification complète du déploiement restent d’actualité. L’accès limité au panneau est documenté dans la section [« Accès et autorisations](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) » ; les points de contrôle indépendants sont traités dans le [guide du témoin](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/).

## Options de connexion et de protection

Les itinéraires de connexion sont propres à chaque espace de travail et doivent être configurés avant l’autorisation. Les protocoles SOCKS5/HTTP CONNECT utilisent la dépendance « python-socks » épinglée. MTProxy utilise le transport intermédiaire aléatoire expérimental de Telethon ; les faux secrets TLS « ee » ne sont pas pris en charge. Le repli direct dépend du [mode IP](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/#ip-modes) sélectionné : le mode « Hide IP » le refuse ; le mode de repli explicite l’autorise après un délai. Le mode « Tunnel/VPN » autorise les routes directes mais ne crée pas de VPN. Il ne s’agit pas d’une politique réseau applicable à l’ensemble du système.

Pour les nouvelles installations, la variable TGWITNESS_VAULT_KEY_FILE pointe vers un fichier de clé principale aléatoire protégé séparément. Montez-le en lecture seule en dehors du répertoire /data dans un conteneur. Conservez séparément les métadonnées publiques « salt » du fichier vault.external.json pour chaque espace de travail, ainsi que la clé principale. Les coffres-forts locaux existants nécessitent une migration planifiée ; la définition de cette variable ne les convertit pas automatiquement. Le stockage et les exportations de messages/fichiers multimédias ne sont pas chiffrés par l’application. Utilisez des volumes chiffrés et un espace de stockage temporaire privé suffisant lorsque cela est nécessaire.

Procédures détaillées : [connexion/sécurité](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/) et [modes de fonctionnement](https://phishdestroy.github.io/TgWitness/fr/docs/reference/operations/).
