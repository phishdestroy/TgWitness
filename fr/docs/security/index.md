# Assurez-en la sécurité

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/security/

Découvrez les itinéraires pour Telegram, les listes de proxys publics et les services externes optionnels. Sachez ce que chaque secret permet d’accéder, ce que les protections couvrent et ce qu’elles vous laissent à votre charge.

**127.0.0.1**Adresse du panneau par défaut

**256 bits**jeton de panel aléatoire

**0**CDN, outils d'analyse ou polices de caractères à distance

**Ed25519**signature sur chaque enregistrement

## C’est ici que tout se trouve

Le collecteur, son panneau de configuration et chaque enregistrement conservé restent sur l'ordinateur ou le serveur sur lequel vous l'exécutez. Telegram est la seule destination par défaut ; chaque autre destination fait l'objet d'un commutateur distinct.

06 / CE QUI SORT DE LA MACHINEVotre installation

VOTRE ORDINATEUR OU VOTRE SERVEUR

**Panneau**127.0.0.1:8787 · jeton « bearer »

**Collector**Un client Telegram par espace de travail

RÉPERTOIRE DE DONNÉES

**Journal**SQLite · chaînage de hachages · signé

**Médias**fichiers nommés selon la valeur SHA-256

**Vault**Fernet · session, paire API, clé de signature, proxy

- **Telegram**Toujours · via votre itinéraire

  Connexion MTProto du compte : directe, SOCKS5, HTTP ou MTProxy. Le mode « Masquer l'adresse IP » attend un proxy opérationnel. Le repli direct nécessite un mode qui l'autorise explicitement.
- **Contenu hors site**Facultatif · désactivé par défaut

  Le journal, les fichiers et les points de contrôle sont chiffrés à l’aide de l’algorithme AES-GCM avant d’être transférés vers un espace de stockage compatible S3. La clé reste en votre possession ; les pièces jointes sont identifiées par des hachages chiffrés, et non par le hachage de leur contenu.
- **Notifications**Facultatif · désactivé par défaut

  Problèmes et nombre de modifications avec les titres des discussions. Les extraits de messages ne sont envoyés que si vous activez cette fonctionnalité.
- **Autorité en matière d’horodatage**Facultatif · désactivé par défaut

  Uniquement la valeur SHA-256 d’un point de contrôle signé et d’un nonce aléatoire. Aucun message, aucun nom d’utilisateur.
- **Witness**Facultatif · désactivé par défaut

  Il extrait les points de contrôle signés et les compteurs de captures à l’aide d’un jeton en lecture seule. Il ne peut ni lire les conversations ni modifier les paramètres.

Par défaut : seule la connexion Telegram sort de cette machine.

Les destinations facultatives sont configurées par espace de travail. Le texte des messages et les fichiers multimédias sont stockés en clair dans le répertoire de données : protégez-le à l’aide d’un chiffrement de disque et de droits d’accès aux fichiers.

## Ce que chaque secret révèle

| Secret | Où est-il conservé ? | Ce que cela permet | En cas de fuite |
| --- | --- | --- | --- |
| **Jeton de panel** | `panel-token.txt` dans le répertoire de données ; le navigateur ne le conserve que pour l'onglet concerné | Toutes les fonctionnalités dans chaque espace de travail : lire et exporter, modifier la portée, se connecter à des comptes | Arrêtez TgWitness, supprimez `panel-token.txt`, relancez-le : un nouveau jeton est créé |
| **Session Telegram** | Vault, chiffré (`credentials.enc`) | Le compte Telegram lui-même | Mettez fin à la session dans Telegram via *Paramètres → Appareils* |
| **Clé de signature** | Vault, chiffré (`signing.enc`) | Signature des enregistrements vérifiables à l’aide de votre empreinte numérique | Des points de contrôle conservés séparément, un témoin et des horodatages indiquent ce qui existait auparavant |
| **Clé de coffre-fort** | `vault.key` à côté des données, ou une clé principale externe pour un nouveau répertoire de données | Décrypter le coffre-fort | Considérez que la clé de session et la clé de signature ont également fait l’objet d’une fuite |
| **Jeton Witness** | Sur l’hébergeur Witness | En lecture seule : points de contrôle signés et état de santé | Supprimez-le sur la page Witness ; créez-en un nouveau |
| **Texte à utiliser hors site** | Vault ; téléchargez-le une seule fois pour pouvoir le récupérer | Décryptage de la copie hors site | Toute personne détenant également les objets stockés peut les déchiffrer : considérez cette copie comme exposée |

## Ce que couvrent les mesures de protection

### Couverts

- Une entrée modifiée, supprimée ou réorganisée dans une exportation : la chaîne de hachage ou la signature n'est plus valide.
- Un journal raccourci ou reconstitué après qu’un point de contrôle a été conservé ailleurs : le point de contrôle conservé ne correspond plus.
- Deviner le jeton du panneau : 256 bits aléatoires, comparés en temps constant ; après 15 échecs par minute, l'adresse est refusée.
- Contenu de discussion hostile : le texte est inséré sous forme de texte, jamais en HTML ; les pièces jointes sont téléchargées sous forme de fichiers ; le panneau ne charge aucun élément provenant d’autres sites.
- Un répertoire de données copiées avec une clé de coffre-fort externe : les sessions et les clés de signature restent chiffrées sans la clé principale.

### À vous de jouer

- Le détenteur du jeton principal dispose d’un contrôle total. Accordez aux autres utilisateurs un accès limité aux comptes, discussions et actions dont ils ont besoin ; veillez à ce que la clé principale reste confidentielle.
- Un administrateur de la machine peut tout lire, réécrire et resigner le journal. Conservez l’empreinte numérique et les points de contrôle sur un autre système.
- Le texte des messages et les fichiers multimédias ne sont pas chiffrés par TgWitness. Veuillez utiliser un chiffrement de disque et définir des autorisations strictes.
- Une connexion HTTP standard en dehors de localhost expose le jeton sur le réseau. Utilisez le protocole HTTPS ou un tunnel SSH.
- Les signatures prouvent que ce qui a été enregistré n’a pas été modifié, et non que chaque événement sur Telegram a été enregistré.

[Partagez l’accès à un dossier](https://phishdestroy.github.io/TgWitness/fr/docs/access/) en définissant des autorisations, une date d’expiration et des limites de session. Un jeton « witness » reste un identifiant distinct.

## Renforcer la sécurité d’une installation

0 sur 8 terminé

1. **Utilisez un compte Telegram dédié** — jamais votre compte principal. Le jeton du panneau et la session vous permettent d’en avoir le contrôle total.
2. **Conservez le panneau sur 127.0.0.1.** Accédez-y à distance uniquement via HTTPS (la configuration Caddy fournie) ou un tunnel SSH.
3. **Chiffrez le disque** contenant le répertoire de données : le texte des messages et les fichiers multimédias sont stockés tels qu’ils ont été reçus.
4. **Limitez le répertoire de données** au compte de service. Sous Unix, les nouveaux répertoires se voient attribuer le mode 0700 ; sous Windows, définissez les droits d'accès du dossier.
5. **Conservez la clé principale du coffre-fort** sur un **autre** serveur : définissez « `TGWITNESS_VAULT_KEY_FILE` » avant de créer le répertoire de données.
6. **Enregistrez l’empreinte de la clé de signature et les points de contrôle** sur un autre système, puis ajoutez un témoin sur un autre serveur.
7. **Ne téléversez jamais** les clés « `data/` », de session, « `panel-token.txt` » ou de coffre-fort sur GitHub ou dans une conversation.
8. **Ne consignez pas** les en-têtes « `Authorization` » ni le corps des requêtes au niveau d’un proxy inverse.

**Puis-je modifier le jeton du panneau sans perdre de données ?**

Oui. Le jeton sert uniquement à ouvrir le panneau. Arrêtez TgWitness, supprimez `panel-token.txt` du répertoire de données, puis relancez-le ; le journal, les sessions et les clés restent intacts. Lorsque `TGWITNESS_TOKEN` est défini, la valeur d’environnement est utilisée à la place du fichier.

**Pourquoi les messages ne sont-ils pas chiffrés au repos ?**

L’utilisateur doit les lire pour effectuer des recherches, comparer les versions et exporter les données. Les chiffrer à l’aide d’une clé sur la même machine n’apporterait guère de protection face à une personne capable d’accéder à cette machine. Le chiffrement du disque protège un disque hors service ou volé ; des autorisations strictes protègent un disque en fonctionnement.

## Signaler une vulnérabilité

Utilisez **la rubrique « Sécurité → Signaler une vulnérabilité** » dans le dépôt GitHub. Indiquez la version, l’impact et un exemple minimal permettant de reproduire le problème. N’envoyez jamais d’identifiants, de répertoires de compte ni d’archives de preuves réelles. Si le signalement privé n’est pas disponible, ouvrez un ticket demandant la création d’un canal privé sans fournir de détails sur l’exploit.
