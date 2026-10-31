# Connexion, proxys et protection des données

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/

Authentification, pools de proxys automatiques, modes IP, politique de repli, requêtes externes et stockage des secrets.

Ce document décrit le fonctionnement de TgWitness 0.7.0 et ses limites. L’authentification, l’accès à la source, la connectivité réseau et l’exhaustivité de la capture constituent des états distincts. Pour connaître les étapes de connexion, les formats de fichiers et la gestion des comptes multiples, commencez par consulter la section « [Comptes et formats de session](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/) ». Pour les règles relatives aux événements et le comportement en cas de redémarrage, consultez [la section « Fonctionnement de la collecte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/) ».

## Méthodes d’authentification

**L’identifiant API et le hachage API identifient une application ; ils ne remplacent pas les identifiants de connexion au compte.** Ils sont facultatifs dans TgWitness. Ordre de priorité : une paire saisie dans le formulaire, puis une provenant d’un fichier JSON de compte importé, puis la paire enregistrée dans l’espace de travail, puis le pool intégré de 50 paires publiques, essayées dans un ordre aléatoire avec rotation automatique lorsque Telegram en refuse une. Seule la paire Telegram Desktop (2040) est envoyée avec une description correspondante du client Telegram Desktop. Votre propre paire, issue des outils de développement API sur [my.telegram.org,](https://my.telegram.org) peut être utilisée avec tous vos comptes ; chaque compte dispose toujours de sa propre autorisation.

| Méthode | Exigences | Assistance TgWitness |
| --- | --- | --- |
| Numéro de téléphone, code, authentification à deux facteurs (2FA) facultative | Accès au compte ; paire d’API facultative | Connexion au panneau d'administration |
| Clé d'authentification HEX + identifiant DC | Clé complète de 512 caractères et DC 1–5 | Onglet « **Clé d'authentification** directe » ; l'identifiant utilisateur facultatif est vérifié avant l'enregistrement de l'autorisation |
| Telethon StringSession | Une chaîne de session valide | Connexion au panneau d'administration |
| Telethon SQLite `.session` | Texte définitif et cohérent | Importation directe des schémas via l'interface graphique 7/8 ; interface en ligne de commande (CLI) hors ligne en option |
| Pyrogram SQLite `.session` | Session utilisateur de production fermée | Importation directe des schémas via le panneau 2/3 |
| Telegram Desktop TData ZIP | Un seul compte moderne ; code d'accès local si le compte est protégé | Conversion en mémoire avec vérification des sommes de contrôle et du déchiffrement |
| Fichier JSON du compte | Champs API/session/clé pris en charge | Les métadonnées suffisent à elles seules à remplir les identifiants de l'API ; une connexion par session/clé ou par numéro de téléphone/code QR reste toutefois nécessaire |
| Connexion par QR code | Confirmation provenant d’une application Telegram officielle | Génération locale de codes QR, expiration/nouvelle tentative, authentification à deux facteurs (2FA) en option |
| TDLib / Pyrogram StringSession | Autres formats spécifiques aux bibliothèques | Non pris en charge |
| Jeton du bot | Un bot doté de son propre modèle d’accès et de mise à jour | Non utilisé par ce collecteur |

Telegram privilégie la transmission par code ; la livraison par SMS n’est pas garantie. Un hachage d’API ne permet pas de rétablir une session révoquée ni de remplacer un mot de passe 2FA oublié. TgWitness ne conserve pas les codes de connexion ni le mot de passe 2FA de Telegram sur le disque dur.

Pour une source privée, le compte doit déjà disposer d’un accès. Il n’est pas nécessaire d’indiquer le nom d’utilisateur du groupe. L’utilisation d’un proxy ou l’importation d’une session ne confère ni le statut de membre ni de droits d’administrateur. Le fait d’être membre à l’heure actuelle ne garantit pas l’accès à l’historique antérieur à l’adhésion.

## Importer un fichier de session Telethon

Telethon SQLite, Pyrogram SQLite et Telegram Desktop TData utilisent des formats différents. Le panneau détecte et convertit les structures prises en charge ; le renommage d’un fichier ne constitue pas une conversion. Sélectionnez une session et son fichier JSON associé dans la rubrique « **Fichiers** », puis cliquez sur **« Connecter le compte** ». Jusqu’à quatre fichiers correspondants et 8 Mio au total sont acceptés. Consultez [les limites de format](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/) pour plus de détails sur TData/JSON. Il n’y a pas de récupération du code d’accès. La connexion par téléphone/authentification à deux facteurs (2FA) ou par code QR crée une autorisation distincte.

Le chemin d’accès en ligne de commande optionnel, réservé à Telethon, reste disponible :

1. Arrêtez le client en utilisant la session d’origine et créez une copie cohérente. Le convertisseur rejette les fichiers comportant un WAL/journal inachevé. Fermez le client d’origine correctement au lieu de supprimer ces fichiers pour contourner la vérification.
2. Depuis l'environnement TgWitness, exécutez :

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. Sous **« Ajouter un compte » → « Fichiers »**, chargez le résultat ou collez sa chaîne de caractères, puis continuez.
2. Vérifiez l'identifiant numérique du compte affiché, sélectionnez les sources et lancez la surveillance.

Le convertisseur ouvre SQLite en lecture seule, n’effectue aucune mise à jour de schéma ni aucune requête réseau, et n’affiche pas la session. Il vérifie la version du schéma, les types de tables, une seule ligne de session, l’adresse IP, le port, le centre de données et la longueur de la clé. La saisie via l’interface en ligne de commande est limitée à 64 Mio ; le texte de StringSession est limité à 4 Ko. La conversion via le panneau télécharge les fichiers vers le serveur TgWitness authentifié, les traite en mémoire et renvoie les identifiants normalisés à ce navigateur sans enregistrer les originaux téléchargés. Utilisez le protocole HTTPS pour un serveur distant.

**Le fichier converti contient un mot de passe d’accès au compte non chiffré.** Conservez-le dans un espace de stockage sécurisé et ne le commitez jamais ni ne l’envoyez à un service de conversion tiers. TgWitness enregistre la session autorisée dans son coffre-fort chiffré. La copie d’une session ne crée pas d’autorisation distincte : n’exécutez pas de clients simultanés avec des clés d’authentification clonées et ne supposez pas une mise à jour indépendante.

La conversion transfère l’autorisation, et non les messages originaux, le cache de l’entité ou un curseur de mise à jour persistant. Elle ne corrige pas la récupération des mises à jour lors des redémarrages du processus.

## MTProto, Telethon et les proxys

MTProto est le protocole de Telegram. Telethon est la bibliothèque cliente Python utilisée par TgWitness. MTProxy est un proxy de transport Telegram ; les protocoles SOCKS5 et HTTP CONNECT fournissent des tunnels généraux. Aucun d’entre eux ne remplace l’authentification du compte.

Enregistrez l’itinéraire pour chaque espace de travail dans **Compte → Paramètres → Paramètres de connexion → Modifier l’itinéraire de connexion** avant de vous connecter. Les nouveaux espaces de travail utilisent par défaut le mode «**MTProxy automatique » · listes publiques** avec le comportement « Masquer l’adresse IP ». Les espaces de travail existants qui utilisaient explicitement le mode « Direct » conservent un mode permettant cette option.

## Modes IP

C'est l'itinéraire qui détermine la connexion. Le mode IP détermine à quel moment l'adresse du serveur peut être exposée. Ces contrôles n'installent pas de VPN et ne redirigent pas l'ensemble du trafic de la machine.

| Mode | Telegram | Demandes externes |
| --- | --- | --- |
| Hide IP (`hide`) | Utilisez un proxy ; patientez si aucun ne fonctionne. Aucune solution de secours directe. | Nécessite SOCKS5/HTTP ; les requêtes sans proxy compatible sont refusées. |
| Autoriser la solution de secours (`fallback`) | MTProxy peut utiliser automatiquement la connexion directe après le délai configuré, puis revenir à un proxy opérationnel. | Privilégiez un proxy externe configuré ou la route SOCKS5/HTTP du compte ; à défaut, la connexion directe est autorisée. |
| Tunnel / VPN (`tunnel`) | Les routes directes et le basculement automatique immédiat vers le pool sont autorisés. | L'accès direct est autorisé lorsqu'aucun proxy applicable n'est configuré. |

Le mode « Tunnel/VPN » suppose que vous gérez ce réseau séparément. Sans un tunnel opérationnel, les destinataires peuvent voir l’adresse du serveur lui-même. Sélectionnez le mode en fonction de votre réseau réel, et non en fonction du nom de l’option.

### Choisissez un parcours

| Itinéraire | Paramètres | Limites |
| --- | --- | --- |
| MTProxy automatique | Listes intégrées ou catalogue d’opérateurs | Maintient une route Telegram opérationnelle ; la solution de secours directe dépend du mode IP |
| Direct | Mode tunnel/VPN | Telethon utilise l'itinéraire réseau de l'hôte |
| SOCKS5 | Hôte, port, nom d'utilisateur et mot de passe (facultatifs) | python-socks, DNS de destination distante activé |
| HTTP CONNECT | Hôte, port, nom d'utilisateur et mot de passe (facultatifs) | Connexion HTTP simple (CONNECT) ; le protocole TLS vers le proxy lui-même n’est pas implémenté |
| MTProxy | Hôte, port, clé secrète | Transport expérimental Telethon ; 32 chiffres hexadécimaux ou « `dd` » + 32 chiffres hexadécimaux |

Les faux secrets TLS « `ee` » sont rejetés. La normalisation de Telethon 1.45 peut supprimer un préfixe et un domaine, mais cela ne met pas en œuvre le « Fake TLS ». Collez « `tg://proxy?server=…&port=…&secret=…` » ou « `https://t.me/proxy?server=…&port=…&secret=…` » et sélectionnez « **Remplir les champs à partir du lien** ». Cela valide et remplit les champs sans connexion ni enregistrement ; vérifiez et enregistrez l’ itinéraire séparément. Les champs manuels restent disponibles. Voir [les liens proxy Telegram](https://core.telegram.org/api/links#proxy-links).

### Proxys publics fournis par votre installation

La liste intégrée regroupe quatre sources : [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) et [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). L'instantané fourni contient des informations sur les terminaux, l'attribution des sources et les dates de téléchargement. La présence d'un fournisseur dans la liste ne constitue pas une garantie que le proxy fonctionne ou qu'il transmet toutes les mises à jour de Telegram.

**MTProxy** vérifie **automatiquement** la connectivité du transport Telegram, maintient un proxy opérationnel et bascule vers un autre en cas de défaillance. Les espaces de travail privilégient différents proxys lorsqu’il y a suffisamment d’entrées opérationnelles disponibles ; une adresse de sortie unique n’est pas garantie. Les proxys défaillants restent inactifs avant une nouvelle tentative. Si aucun ne fonctionne, le mode IP détermine si la collecte doit attendre ou peut utiliser une connexion directe. Le changement de proxy ne modifie pas le compte ni n’efface son journal. Les choix et changements d’itinéraire sont consignés dans le journal signé.

Lorsque les itinéraires automatiques sont actifs, les listes sont actualisées toutes les heures et les vérifications de transport s’exécutent toutes les dix minutes par défaut. Ces intervalles sont configurables. **La mise à jour des listes publiques** déclenche une actualisation ; la simple consultation de la liste ne modifie pas un itinéraire manuel enregistré.

Chaque réponse de flux est limitée à 1 MiB, avec un délai d’expiration de la requête de huit secondes et un délai global de téléchargement de 20 secondes ; les redirections sont rejetées. Jusqu’à 64 entrées compatibles par source sont conservées et dédupliquées. L’analyseur accepte les clés secrètes hexadécimales et base64url prises en charge, ainsi que le flux JSON. Les faux certificats TLS « `ee` », les liens non valides, les littéraux IP privés/réservés et les noms d’hôtes locaux sont ignorés. Les noms d’hôtes sont résolus et vérifiés avant utilisation, et l’adresse IP choisie est verrouillée pour cette connexion. La réacquisition automatique résout à nouveau un nom d’hôte ; réappliquez une entrée manuelle pour le résoudre à nouveau.

Les réponses de flux ayant échoué, vides ou incompatibles conservent l’instantané de la source précédent. Les mises à jour sont atomiques, sérialisées et limitées à une tentative par minute et par espace de travail. Une sonde de transport réussie établit la connectivité, mais ne garantit ni l’anonymat ni l’exhaustivité de la capture.

**Le trafic Telegram et les requêtes HTTPS empruntent des chemins différents.** Les téléchargements de listes utilisent une connexion HTTPS distincte et le chemin de requête externe fourni. « `TGWITNESS_PROXY_FEED_PROXY` » remplace explicitement ce chemin par un proxy HTTP/SOCKS5 ; les deux variantes du collecteur « Compose » le transmettent. Le pool d’arrière-plan suit l’espace de travail principal. Aucune session Telegram, aucun identifiant API, aucun jeton de panneau ni aucun jeton de bot n’est transmis aux fournisseurs de flux. Les noms des fournisseurs, les dates des instantanés et l’itinéraire de téléchargement apparaissent sous « **D’où provient la liste** ».

Un MTProxy achemine uniquement le trafic Telegram. Les opérations HTTP de l’espace de travail, telles que les horodatages, les notifications, les copies hors site et les vérifications de source, utilisent un proxy SOCKS5/HTTP distinct lorsqu’il est configuré, puis la route SOCKS5/HTTP du compte. En l’absence de l’un ou de l’autre, Hide IP refuse la demande ; les autres modes autorisent le mode Direct. Les requêtes externes peuvent être désactivées. Un proxy de téléchargement de flux explicitement configuré reste une option de contournement distincte gérée par l’opérateur. Le service de témoin indépendant conserve sa propre route.

****Paramètres automatiques du pool**** Sous **Paramètres → MTProxy automatique**, configurez le seuil d’échec, le délai d’attente, la rotation planifiée, le partage de proxy et le délai de repli autorisé. | Commande | Valeur par défaut | | --- | --- | | Déconnexions avant remplacement | 3 en 10 minutes | | Nombre de proxys essayés par tentative de connexion | 3 | | Premier / temps de repos maximal après échec | 10 minutes / 6 heures | | Rotation planifiée | Désactivée ; basculement en cas d’échec | | Comptes par proxy | 0 : privilégiez des entrées distinctes, partagez si nécessaire. Définissez la valeur 1 pour attendre une entrée exclusive. | | Délai avant repli autorisé vers Direct | 10 minutes ; « Hide IP » refuse toujours Direct | | Actualisation du flux / vérifications de transport | 60 / 10 minutes ; les valeurs de l'espace de travail principal s'appliquent au pool partagé | Des proxys différents ne garantissent pas des adresses de sortie différentes. Ces paramètres ne remplacent pas les limites de Telegram et ne garantissent pas l'anonymat.

Pour remplacer la liste publique par votre propre catalogue d’opérateurs, configurez la surécriture ci-dessous. Cela désactive entièrement les abonnements externes, y compris lorsque son tableau « `proxies` » est vide.

Copiez [le catalogue vide](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) vers `proxy-config/proxies.json` et ajoutez vos points de terminaison publics déployés :

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

Les valeurs d’exemple doivent être remplacées. Jusqu’à 32 entrées distinctes sont acceptées. La liste authentifiée renvoie des étiquettes/hôtes/ports sans secrets partagés ; la sélection d’un élément enregistre ses identifiants dans le coffre-fort de l’espace de travail. La disponibilité n’est pas vérifiée tant qu’un test de transport explicite n’a pas été effectué. Un catalogue mal formé permet une configuration manuelle.

Lancement en mode natif : définissez `TGWITNESS_PROXY_CATALOG` comme chemin d'accès JSON local. Docker :

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

Le montage en superposition est en lecture seule (`proxy-config`) ; les fichiers doivent être lisibles par le conteneur UID 10001. Ce répertoire est exclu de Git, du contexte de compilation Docker et des archives sources. Ce catalogue configure les comptes de collecte ; [le bot témoin](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/) utilise sa propre route HTTP/SOCKS5, et non MTProxy.

La solution de secours directe est régie par le mode IP décrit ci-dessus. Suspendre la surveillance avant de modifier un itinéraire. L'enregistrement déconnecte les anciens clients et annule les connexions en cours ; un nouveau client utilise l'itinéraire enregistré. La liaison entre le journal et la session du compte est conservée. Les paramètres remplacent l'itinéraire précédent : veuillez saisir à nouveau les identifiants du proxy lors de sa modification.

Les identifiants sont chiffrés selon le standard `network.enc`. L’API ne renvoie ni le nom d’utilisateur, ni le mot de passe, ni la clé secrète. Les enregistrements signés contiennent le type de route et indiquent si des identifiants sont présents, sans mentionner le point de terminaison ni les clés secrètes. L’opérateur peut consulter le point de terminaison dans le panneau de contrôle. Les champs contenant les clés secrètes sont effacés après l’enregistrement, le verrouillage ou le changement d’espace de travail.

**La fonction « Tester la connexion Telegram** », également disponible avant la connexion, ouvre et ferme une connexion Telegram temporaire et non autorisée via le routeur. Elle ne contacte pas de site web de vérification d’adresse IP. En cas de succès, cela établit la connectivité de transport, mais ne garantit pas l’accès aux groupes, la livraison complète ni l’anonymat.

Le proxy s'applique aux connexions du client Telegram, y compris aux téléchargements de médias depuis les serveurs de distribution (DC) de Telegram. Le navigateur, pip, SSH et les outils TSA lancés manuellement empruntent des chemins distincts. Le nom d'hôte du proxy peut être résolu localement. `rdns` affecte les noms d'hôtes de destination ; Telegram fournit souvent des adresses IP numériques pour ses serveurs de distribution (DC).

Les protocoles SOCKS5 et HTTP CONNECT en clair ne chiffrent pas en eux-mêmes les identifiants du proxy ni le tunnel client-proxy. MTProto protège séparément le trafic Telegram. Utilisez un canal sécurisé approprié vers le proxy sur un réseau non fiable. Les groupes privés sont des discussions dans le cloud ; MTProto ne les transforme pas en discussions secrètes chiffrées de bout en bout.

## Chiffrement et signatures

| Niveau | Mis en œuvre | Responsabilité de l'opérateur |
| --- | --- | --- |
| Trafic Telegram | Telethon MTProto | Confiance, acheminement et disponibilité de la plateforme |
| Panneau web | Jeton porteur, configuration par défaut en boucle fermée, limites de requêtes | HTTPS ou tunnel SSH pour l'accès à distance |
| Secrets | Fernet pour les identifiants API, les sessions, les identifiants de proxy et la clé privée de signature | Protégez la clé de déchiffrement et l’hôte d’exécution |
| Clé de coffre-fort | Clé locale ou clé principale externe pour une nouvelle installation | Stockage sécurisé et sauvegarde des clés séparés |
| Messages et pièces jointes | Stockage des données de l’application en texte clair | Disque/volume chiffré |
| ZIP/JSONL/CSV/HTML | Contrôles d’intégrité, aucun chiffrement du contenu | Protégez les copies exportées et les transferts |
| Provenance et date | Journal signé, accusé de réception, outils conformes à la norme RFC 3161 | Clé de confiance, points de contrôle indépendants/TSA et procédure de conservation |

**La protection du stockage** dans « Compte » affiche ces états. Le jeton du panneau est un secret d’accès, et non un mot de passe de chiffrement. Il accorde un accès administrateur ; [les jetons émis](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) peuvent être limités à des comptes et à des discussions. Les espaces de travail partagent le processus hôte et ne constituent pas des locataires isolés.

Une démo synthétique isolée, lancée explicitement, peut s’ouvrir automatiquement via une connexion de bouclage direct. Cette fonctionnalité utilise un processus à durée de vie distincte ; elle ne révèle pas le jeton de panneau configuré et ne donne pas accès aux espaces de travail réels. Les requêtes à distance, par proxy ou inter-origines ne peuvent pas obtenir ni utiliser cette fonctionnalité d’accès automatique. Cette fonctionnalité pratique ne supprime pas la barrière d’authentification pour les données réelles des comptes.

BitLocker, LUKS, FileVault ou un volume chiffré géré peuvent protéger le stockage dans le cadre de leurs modèles de menaces respectifs. L’administrateur d’une machine déverrouillée et en cours d’exécution peut toujours lire les données. Tenez compte des fichiers WAL/SHM de SQLite, des fichiers multimédias, des exportations temporaires, de l’espace d’échange, des sauvegardes et des téléchargements du navigateur dans la planification du stockage. Un volume Docker n’est pas chiffré simplement parce qu’il s’agit d’un volume. TgWitness n’implémente ni SQLCipher ni le chiffrement d’objets.

## Clé principale externe

Pour une **nouvelle** installation, placez la clé principale en dehors du répertoire de données. Cela ne migre pas automatiquement un coffre-fort à clé locale existant. Préparez un répertoire de clés accessible uniquement à l’identité du service, puis exécutez :

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell, en utilisant l’environnement de projet installé :

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

Dans Docker, montez le fichier en lecture seule en dehors de `/data`, par exemple sur `/run/secrets/tgwitness-master.key`, et définissez la variable d’environnement sur ce chemin d’accès. L’UID du service doit pouvoir y accéder en lecture. Transmettez le chemin d’accès, et non les octets de clé, via les fichiers d’environnement/de configuration.

Chaque espace de travail reçoit un « salt » public aléatoire et sa propre clé Fernet dérivée via HKDF-SHA256. `vault.external.json` stocke les métadonnées de dérivation, et non la clé principale. Une clé manquante ou erronée empêche le démarrage sans la remplacer silencieusement. Conservez à la fois les métadonnées du « salt » et la clé principale à des fins de récupération.

Tous les espaces de travail dérivent de la même clé principale ; sa compromission affecte l’ensemble de l’ installation. Le processus en cours d’exécution peut déchiffrer les secrets. Il ne s’agit ni d’un HSM ni d’un KDF de mot de passe. Les mots de passe humains arbitraires ne sont pas acceptés à la place d’une clé aléatoire.

Conservez la clé existante pour les installations actuelles jusqu’à ce qu’une migration délibérée soit mise en œuvre et vérifiée. La suppression de « `vault.key` » ou le remplacement d’une clé principale peut empêcher l’accès aux sessions et aux clés de signature. Conservez les sauvegardes chiffrées et les clés séparément et testez la restauration dans une instance isolée.

## Sources et portée de la vérification

Révisé le 26 octobre 2026 :

- https://core.telegram.org/api/auth
- https://core.telegram.org/api/obtaining_api_id
- https://docs.telethon.dev/en/stable/basic/signing-in.html
- https://docs.telethon.dev/en/stable/concepts/sessions.html
- https://core.telegram.org/mtproto/mtproto-transports
- https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/storage/storage_account.cpp
- Telethon 1.45.0 : SQLiteSession, StringSession, `Connection._proxy_connect`, `TcpMTProxy.normalize_secret` et méthodes de téléchargement.

Les tests locaux portent sur les fixtures SOCKS5/HTTP CONNECT en boucle fermée, les sessions SQLite synthétiques, l’isolation des routes, l’exclusion des secrets et le refus en cas de clé manquante. Ils ne permettent pas d’établir une véritable interopérabilité entre Telegram et le proxy, ni de valider le comportement de MTProxy en conditions réelles. Voir [les fichiers VERIFICATION.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/) et [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
