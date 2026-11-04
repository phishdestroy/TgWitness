# Assurez-en la sécurité

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/security/

Ce qui quitte votre machine, ce que chaque secret ouvre, et ce que couvrent les protections par rapport à ce qui vous incombe.

**127.0.0.1**Adresse du panneau par défaut

**256 bits**jeton de panel aléatoire

**0**CDN, outils d'analyse ou polices de caractères à distance

**Ed25519**signature sur chaque enregistrement

## C’est ici que tout se trouve

Le collecteur, le panneau et chaque entrée restent sur votre machine. Par défaut, seul Telegram est contacté ; tout le reste est un interrupteur à part.

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
| **Jeton de panel** | `panel-token.txt` dans le dossier de données ; le navigateur le garde par onglet | Tout, dans chaque espace | Arrêtez TgWitness, supprimez `panel-token.txt`, redémarrez : vous en obtenez un nouveau |
| **Session Telegram** | Vault, chiffré (`credentials.enc`) | Le compte Telegram lui-même | Mettez fin à la session dans Telegram via *Paramètres → Appareils* |
| **Clé de signature** | Vault, chiffré (`signing.enc`) | Signer des entrées sous votre empreinte | Les points de contrôle conservés ailleurs, un témoin et les horodatages montrent toujours ce qui existait avant |
| **Clé de coffre-fort** | `vault.key` à côté des données, ou une clé maîtresse externe | Le coffre | Considérez que la session et la clé de signature ont aussi fuité |
| **Jeton Witness** | Sur l’hébergeur Witness | Lecture seule : points de contrôle et état | Supprimez-le sur la page du témoin et créez-en un nouveau |
| **Texte à utiliser hors site** | Vault ; téléchargez-le une seule fois pour pouvoir le récupérer | La copie externe | Quiconque a aussi le bucket peut la déchiffrer : considérez la copie comme exposée |

## Ce que couvrent les mesures de protection

### Couverts

- Une entrée modifiée, supprimée ou réordonnée : la chaîne de hachages ou une signature se rompt.
- Un journal raccourci ou reconstruit après que vous avez conservé un point de contrôle ailleurs : le point de contrôle ne correspond plus.
- Deviner le jeton : 256 bits aléatoires, comparaison en temps constant ; 15 échecs par minute et l’adresse est bloquée.
- Contenu hostile dans les chats : le texte reste du texte, jamais du HTML ; les pièces jointes se téléchargent comme fichiers ; le panneau ne charge rien depuis d’autres sites.
- Un dossier de données volé avec une clé de coffre externe : sessions et clés restent chiffrées.

### À vous de jouer

- Le jeton principal peut tout faire. Donnez aux autres un accès limité et gardez le principal pour vous.
- Qui est administrateur de la machine peut tout lire et re-signer le journal. Conservez l’empreinte et les points de contrôle ailleurs.
- TgWitness ne chiffre ni les messages ni les médias. Chiffrez le disque et restreignez les droits.
- Le HTTP simple hors de localhost fait fuiter le jeton. Utilisez HTTPS ou un tunnel SSH.
- Les signatures ne vous disent pas ce qui a été manqué. Vérifiez la couverture et testez la livraison sur vos propres comptes et sources.

[Partagez l’accès à une affaire](https://phishdestroy.github.io/TgWitness/fr/docs/access/) avec des droits, une expiration et des limites de session.

## Renforcer la sécurité d’une installation

0 sur 8 terminé

1. **Utilisez un compte Telegram dédié**, jamais le principal.
2. **Laissez le panneau sur 127.0.0.1.** Accès distant uniquement via HTTPS (Caddy fourni) ou un tunnel SSH.
3. **Chiffrez le disque** qui contient le dossier de données : messages et médias sont stockés tels quels.
4. **Restreignez le dossier de données** au compte de service (0700 sous Unix, droits du dossier sous Windows).
5. **Gardez la clé du coffre ailleurs** sur les serveurs : définissez `TGWITNESS_VAULT_KEY_FILE` avant le premier démarrage.
6. **Conservez l’empreinte et les points de contrôle** sur un autre système, faites tourner un témoin sur un autre hôte.
7. **Ne téléversez jamais** les clés « `data/` », de session, « `panel-token.txt` » ou de coffre-fort sur GitHub ou dans une conversation.
8. **Ne consignez pas** les en-têtes « `Authorization` » ni le corps des requêtes au niveau d’un proxy inverse.

**Puis-je modifier le jeton du panneau sans perdre de données ?**

Oui, il ouvre seulement le panneau. Arrêtez TgWitness, supprimez `panel-token.txt`, redémarrez. Journal, sessions et clés restent. Si `TGWITNESS_TOKEN` est défini, cette valeur prime sur le fichier.

**Pourquoi les messages ne sont-ils pas chiffrés au repos ?**

Le collecteur doit les lire pour chercher, comparer et exporter. Une clé sur la même machine n’arrêterait pas quelqu’un qui peut déjà lire cette machine. Le chiffrement du disque couvre un disque volé, les droits couvrent un système en marche.

## Signaler une vulnérabilité

**Security → Report a vulnerability** sur GitHub. Version, impact et une reproduction minimale avec des données fictives. N’envoyez jamais d’identifiants, de dossiers de compte ni de vraies preuves. Si le signalement privé est désactivé, ouvrez une issue pour demander un canal privé, sans détails d’exploit.
