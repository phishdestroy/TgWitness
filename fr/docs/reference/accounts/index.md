# Formats des comptes et des sessions

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/

Connectez-vous par téléphone, via un code QR ou une clé d'authentification, importez des sessions Telethon, Pyrogram ou Telegram Desktop, et gérez plusieurs comptes.

TgWitness se connecte en tant que **compte utilisateur Telegram** (et non en tant que bot) via MTProto, à l’aide de Telethon. Chaque compte dispose de son propre **espace de travail** (appelé « *workspace* » dans l’ API et les outils en ligne de commande) avec sa propre session, ses propres sources, son propre journal et sa propre clé de signature.

Les fichiers de session, les chaînes de session et les clés d’authentification constituent **des autorisations de compte** : toute personne qui en détient une peut agir au nom de ce compte. Ils ne contiennent pas l’historique des messages.

> [!AVERTISSEMENT] **N’utilisez rien que vous ne puissiez vous permettre de perdre.** Nous vous déconseillons vivement de connecter des comptes personnels ou de toute autre nature présentant une valeur particulière, ainsi que de créer un identifiant API / un hachage API sur un compte auquel vous tenez. Il ne s’agit pas ici d’un manque de tests de TgWitness : Telegram restreint et suspend définitivement des comptes de manière imprévisible — pour des volumes de requêtes qu’il juge excessifs, quel que soit le client ou l’objectif, sans documentation adéquate. De nombreuses suspensions sont irréversibles. Utilisez des comptes dédiés. Le bon déroulement des tests dépend de Telegram, et non du logiciel, et ne garantit rien pour la suite.

- [En bref](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#at-a-glance)
- [Avant de commencer : identifiant API et hachage API](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Numéro de téléphone](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#phone-number) · [Code QR](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#qr-code) · [Clé d'authentification + identifiant DC](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#auth-key--dc-id)
- [Fichiers de compte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#pyrogram-session) · [Paire session + JSON](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#telethon-stringsession) · [Fichier JSON du compte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#account-json)
- [Identifiez ce dont vous disposez](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#identify-what-you-have) · [Formats non pris en charge](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#unsupported-formats)
- [Comptes multiples](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#multiple-accounts) · [Assurer la sécurité des fichiers de compte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#keeping-account-files-safe) · [Dépannage](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#troubleshooting)

## En bref

| Ce dont vous disposez | Onglet « **Ajouter un compte »** | Vous aurez également besoin de |
| --- | --- | --- |
| Le numéro de téléphone et l'accès à ses codes de connexion | **Téléphone** | Mot de passe 2FA s'il est activé |
| Telegram ouvert sur un autre appareil | **Code QR** | Mot de passe 2FA s'il est activé |
| Un fichier `.session` (Telethon ou Pyrogram) | **Fichiers** | Fichier JSON complémentaire facultatif pour les paramètres de l’application |
| `.session` + `.json` portant le même nom | **Fichiers** (sélectionnez les deux) | Généralement, rien d’autre |
| Un dossier « `tdata` » dans Telegram Desktop | **Fichiers** (au format ZIP) | Le code d'accès local de l'application de bureau, s'il en a été défini un |
| Une session StringSession de Telethon (texte, `.txt`, `.tgwitness-session`) | **Fichiers** | Aucune paire d’API distincte n’est requise |
| Un `.json` avec une session ou une clé d'authentification | **Fichiers** | Aucune paire d’API distincte n’est requise |
| Une clé d'authentification (512 caractères hexadécimaux) et son numéro DC | **Clé d'authentification** | Identifiant utilisateur facultatif |

TgWitness identifie les fichiers en fonction de leur **contenu**, et non de leur nom. Le fait de renommer un fichier ne le convertit jamais.

## Avant de commencer : identifiant API et hachage API

Vous pouvez vous connecter sans créer d’application API Telegram. Lorsqu’aucune paire n’est saisie, importée ou déjà enregistrée dans l’espace de travail, TgWitness sélectionne une paire au hasard parmi son pool intégré de 50 paires API publiques (`tgwitness/api_pool.py`). Si Telegram refuse une paire (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), la suivante est essayée, jusqu’à huit par connexion ; les paires refusées sont ignorées jusqu’au redémarrage. La paire utilisée pour la connexion est enregistrée avec le compte et réutilisée pour celui-ci. Un **identifiant API** et **un hachage API** identifient l’application auprès de Telegram ; ils n’autorisent pas un compte à eux seuls.

Pour utiliser votre propre application à la place (c’est le compte qui l’enregistre qui est exposé à un risque ; voir « [Pourquoi un pool d’API intégré ?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account) ») :

1. Ouvrez [my.telegram.org](https://my.telegram.org) et connectez-vous avec n'importe quel numéro de téléphone dont vous disposez. Le code vous est envoyé dans l'application Telegram, et non par SMS.
2. Choisissez **des outils de développement d'API**.
3. Créer une application : titre et nom court au choix (5 à 32 lettres), plateforme « **Desktop** ». Les champs « URL » et « Description » peuvent rester vides.
4. Copiez **l’api_id de l’application** (un nombre) et **l’api_hash de l’application** (32 caractères hexadécimaux).

Dans le panneau, les champs **« API ID » et « Hash »** se trouvent sous le formulaire de connexion. Vous pouvez coller une seule paire `api_id:api_hash` dans le champ **« API ID »** : les deux champs seront alors automatiquement remplis. Une seule paire peut être utilisée pour tous vos comptes. Une fois la connexion établie, ces informations sont enregistrées, chiffrées, dans cet espace de travail uniquement et ne sont jamais renvoyées au navigateur.

Trois types d’informations d’identification sont concernés :

| Secret | Ouvrir | Où le trouver |
| --- | --- | --- |
| Jeton de panel | Le panneau web de TgWitness | `panel-token.txt` dans le répertoire de données, ou `TGWITNESS_TOKEN` |
| ID de l'API + hachage | Rien en soi ; identifie l’application | Appariement intégré, paramètres importés ou votre propre application sur my.telegram.org |
| Autorisation du compte | Le compte Telegram | Créé via une connexion par téléphone ou code QR, ou importé en tant que session |

Si l’accès à Telegram doit se faire via un proxy, configurez-le d’abord dans **Compte → Paramètres → Paramètres de connexion → Modifier l’itinéraire de connexion**.

## Numéro de téléphone

1. Ouvrez **un compte**, sélectionnez l'onglet « **Téléphone** », puis saisissez le numéro au format international, par exemple `+44 7700 900123`. Les espaces et les tirets sont supprimés automatiquement.
2. Cliquez sur « **Continuer** ». Les champs « API ID » et « Hash » peuvent rester vides.
3. Saisissez le code envoyé par Telegram (généralement dans l'application Telegram ; la réception par SMS n'est pas garantie).
4. Si le compte dispose d’une authentification en deux étapes, saisissez ce mot de passe. Il ne s’agit ni du jeton du panneau ni du code d’accès de l’appareil.
5. Vérifiez l'identifiant du compte affiché après la connexion, puis sélectionnez les sources.

Les identifiants de connexion et le mot de passe 2FA ne sont jamais enregistrés sur le disque.

## Code QR

Utilisez cette fonction lorsque le compte est déjà connecté sur un téléphone ou un autre ordinateur.

1. Onglet « **Code QR »** → **Afficher le code QR**. Les champs « ID API » et « Hachage » peuvent rester vides.
2. Sur l’appareil connecté : **Paramètres → Appareils → Associer un appareil de bureau**, scannez le code puis confirmez.
3. Saisissez le mot de passe 2FA dans TgWitness si Telegram vous le demande.

L'image QR est générée localement. Les codes ont une durée de validité limitée ; cliquez sur « **Générer un autre code QR »** pour réessayer. Le verrouillage du panneau, le changement d'espace de travail ou le lancement d'une nouvelle session annulent un code en attente.

## Clé d'authentification + identifiant DC

Une clé d'autorisation (Auth Key) est la clé d'autorisation brute de 256 octets qui sous-tend chaque session Telegram, représentée sous la forme de **512 caractères hexadécimaux**, accompagnée du numéro du centre de données **DC 1 à 5**.

1. Onglet « **Clé d'authentification** ». Collez la clé complète ; une clé raccourcie contenant « `…` » ne fonctionnera pas.
2. Sélectionnez l'identifiant DC fourni avec la clé.
3. Vous pouvez, si vous le souhaitez, saisir l’**identifiant utilisateur**. TgWitness refuse alors la connexion si Telegram signale un compte différent.
4. **Compte** Press **Connect**.

Une clé d'authentification (512 caractères) n'est pas un hachage API (32 caractères). La même clé peut également être importée au format JSON ; voir « [Account JSON](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#account-json) ».

## Fichiers de compte

Ouvrez **« Ajouter un compte » → « Fichiers »** et sélectionnez jusqu’à **quatre fichiers appartenant à un même compte**, pour un total de **8 Mio**, puis cliquez sur « **Connecter le compte** ».

- Les fichiers sont convertis **en mémoire** sur votre serveur TgWitness. Les fichiers téléchargés ne sont pas stockés, les fichiers ZIP ne sont pas extraits sur le disque et aucun service externe n’est sollicité.
- La session ainsi obtenue est ensuite vérifiée auprès de Telegram. Si un fichier mentionne un identifiant d’utilisateur, celui-ci doit correspondre au compte indiqué par Telegram.
- Les fichiers décrivant différents comptes ou différents identifiants API sont rejetés au lieu d’en choisir un seul.
- Le champ **« Code d'accès ou texte de session »** contient le champ « TData local passcode », une zone permettant de coller une StringSession et **de lire des fichiers sans se connecter** (remplit le formulaire sans contacter Telegram).

### Téléthon `.session`

|  |  |
| --- | --- |
| De quoi s’agit-il ? | La base de données SQLite créée par les outils basés sur Telethon, par exemple `my_account.session` |
| Reconnu par | Tableaux `sessions` (avec `dc_id`, `server_address`, `port`, `auth_key`) et `version` = 7 ou 8 |
| Exigences | Exactement une ligne de session autorisée ; une base de données fermée et complète |

Fermez d’abord le programme qui a créé le fichier. Si `my_account.session-journal` ou `my_account.session-wal` se trouve à côté, la base de données n’est pas finalisée : ouvrez puis fermez correctement le client d’origine. La suppression de ces fichiers « sidecar » peut laisser une copie corrompue.

### Pyrogram `.session`

|  |  |
| --- | --- |
| De quoi s’agit-il ? | La base de données SQLite que les outils basés sur Pyrogram créent |
| Reconnu par | Tableau `sessions` avec `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot` ; `version` = 2 ou 3 |
| Exigences | Une seule session **d'utilisateur** autorisée sur le réseau de production. Les sessions des bots et des centres de données de test sont rejetées. |

L'identifiant utilisateur enregistré est vérifié auprès de Telegram lors de la connexion.

### Paire session + JSON

Les comptes sont souvent distribués sous la forme de deux fichiers portant le même nom, par exemple `447700900123.session` et `447700900123.json`. Sélectionnez-les **tous les deux** en même temps.

- À partir du fichier JSON, TgWitness utilise `app_id`/`api_id` et `app_hash`/`api_hash` ; vous n’avez donc généralement pas besoin de saisir d’identifiants d’API.
- Les autres champs tels que `phone`, `device`, `sdk`, `app_version`, `lang_pack` ou un mot de passe `twoFA` enregistré sont **ignorés**. Si le compte dispose d’une authentification à deux facteurs (2FA), TgWitness vous la demande.
- Un fichier JSON en soi ne contient que des métadonnées. En l’absence de fichier de session, veuillez poursuivre la connexion via votre téléphone ou à l’aide d’un code QR.

### Telegram Desktop (TData)

TData correspond au dossier « `tdata` » de l’application Telegram Desktop (l’application multiplateforme disponible sur desktop.telegram.org).

| Système | Emplacement par défaut : `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portable : à côté de `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Pour l'importer :

> **Avertissement concernant les sessions parallèles.** L’importation de TData réutilise la clé d’autorisation de Telegram Desktop ; elle ne crée pas de connexion indépendante. N’utilisez pas cette clé simultanément dans Desktop et TgWitness. Telegram peut invalider l’autorisation avec `AUTH_KEY_DUPLICATED`, rendant les deux instances inutilisables jusqu’à une nouvelle connexion.
>
>
>
> Fermez complètement Desktop, y compris son processus dans la barre d’état, et veillez à ce que cette instance reste fermée pendant que TgWitness utilise la session importée. **Quittez l’application, ne vous déconnectez pas et ne révoquez pas la session :** la révocation invalide également la copie importée. Si vous avez besoin que les deux clients fonctionnent simultanément, connectez-vous à TgWitness via votre téléphone ou un code QR pour créer votre propre autorisation. Il est recommandé d’utiliser un compte dédié, mais cela ne garantit pas pour autant la sécurité de l’utilisation parallèle de clés clonées.
>
>
>
> Cela s'applique également aux fichiers `.session` importés, au texte StringSession et à la clé d'authentification au format HEX. Les autres clients disposant de leurs propres autorisations créées de manière indépendante peuvent rester connectés. Consultez [la documentation de Telegram relative à AUTH_KEY_DUPLICATED](https://core.telegram.org/api/errors#406-not-acceptable).

1. Quittez complètement Telegram Desktop.
2. Créez un fichier ZIP ne contenant **que** ces deux éléments provenant de `tdata` :

   - `key_datas`
   - le fichier de 16 caractères se terminant par « `s` » situé à côté, généralement « `D877F783D5D3EF8Cs` »

   La compression de l’intégralité du dossier avec son cache multimédia dépasse généralement les limites (512 entrées, 32 Mio décompressés). 3. Sélectionnez le fichier ZIP dans « **Fichiers** ». Si Telegram Desktop dispose d’un **code d’accès local**, saisissez-le d’abord dans le champ « **Code d’accès » ou « Texte de session** ». Il ne s’agit pas du mot de passe 2FA.

Prise en charge : un compte par archive, stockage moderne `key_datas`/`key_data0`/`key_data1`, code d'accès local. Non pris en charge : les dossiers contenant plusieurs comptes connectés, les anciennes versions de la version de bureau, les fichiers ZIP protégés par mot de passe et l'application native distincte pour macOS « Telegram for macOS ».

### Telethon StringSession

Une seule ligne de texte, commençant généralement par « `1` » et comptant environ 350 caractères. Importez-la sous forme de fichier « `.txt` » ou « `.tgwitness-session` » (4 Ko maximum), ou collez-la dans le champ « **Code d'accès » ou « Texte de session** ». Seules les chaînes Telethon sont acceptées ; les chaînes Pyrogram et TDLib utilisent des formats différents.

### Fichier JSON du compte

Un objet JSON, d'une taille maximale de **64 KiB**, dans un fichier se terminant par **`.json`**.

| Champ (alias) | Signification |
| --- | --- |
| `api_id` (`app_id`) | ID de l'application, un nombre positif |
| `api_hash` (`app_hash`) | Hachage de l'application, 32 caractères hexadécimaux |
| `string_session` (`session_string`, `session`) | Texte « Telethon StringSession », et non un nom de fichier |
| `auth_key` (`auth_key_hex`) + `dc_id` | Clé d'authentification complète de 512 caractères et DC 1 à 5 |
| `user_id` (`id`) | Facultatif ; vérification effectuée par rapport à Telegram avant l'enregistrement de l'autorisation |

Si un pseudonyme et le nom principal sont tous deux présents, ils doivent correspondre. Exemples :

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

Le premier exemple ne concerne que la saisie des identifiants API ; connectez-vous par téléphone ou via un code QR, ou ajoutez un fichier de session. Les listes groupées (un tableau JSON de comptes) ne sont pas acceptées.

## Identifiez ce dont vous disposez

| Vous voyez | Il s'agit de | Utilisation |
| --- | --- | --- |
| `*.session` ; lorsque vous l'ouvrez dans un éditeur de texte, « `SQLite format 3` » s'affiche en haut de la page | Telethon ou Pyrogram SQLite | **Fichiers** (détectés automatiquement) |
| Un dossier « `tdata` » contenant « `key_datas` » | Telegram Desktop TData | Compressez les deux fichiers au format ZIP, puis « **Fichiers »** |
| Une ligne de texte commençant par `1`, environ 350 caractères | Telethon StringSession | **Fichiers** |
| `*.json` avec `app_id`/`app_hash` | Métadonnées associées | **Fichiers**, ainsi que la session correspondante |
| `*.json` avec `auth_key` ou `string_session` | Fichier JSON du compte | **Fichiers** |
| 512 caractères `0-9a-f` | Clé d'authentification | **Clé d'authentification** |
| 32 caractères `0-9a-f` | Hachage de l'API | **ID API + hachage** |
| `td.binlog` ou `db.sqlite` provenant d’une application TDLib | Stockage TDLib | Non pris en charge |
| `123456789:AA…` | Jeton du bot | Non pris en charge |

## Formats non pris en charge

| Format | Alternative |
| --- | --- |
| Stockage TDLib (`td.binlog`) et exportations TDLib | Connectez-vous par téléphone ou via un code QR |
| **Chaînes** de session Pyrogram | Utilisez le fichier Pyrogram `.session`, ou le code QR/le numéro de téléphone |
| TData avec plusieurs comptes connectés | Déconnectez-vous des autres comptes dans Telegram Desktop, ou utilisez le fichier de session propre à chaque compte |
| Jetons de bot | Non pris en charge : TgWitness observe en tant que compte utilisateur |
| Listes au format CSV/JSON de nombreux comptes | Importez les fichiers de session pris en charge via **Comptes → Importer des comptes**, ou connectez-vous par téléphone/QR dans des espaces de travail distincts |
| Sessions de test sur DC ou via un bot | Utilisez un compte utilisateur de production |

## Comptes multiples

Appuyez sur **+** à côté du sélecteur de compte, ou ouvrez **Compte → Paramètres → Paramètres de connexion → Espaces de travail**, saisissez un libellé et connectez-vous.

- N’importe quel nombre d’espaces de travail, y compris l’espace principal. Chacun dispose de sa propre session, de son itinéraire de proxy, de ses sources, de sa politique de capture, de son journal, de sa clé de signature, de ses points de contrôle et de ses exportations.
- Le fait de changer d'espace de travail affiché ne met pas les autres en pause.
- Un journal reste lié au compte qui l’a créé. Se connecter avec un autre compte nécessite un autre espace de travail, et un même compte ne peut pas être attribué à deux espaces de travail.
- Le jeton du panneau principal contrôle l’ensemble des espaces de travail. [Les droits d’accès accordés](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) permettent de limiter l’accès d’autres personnes à certains comptes et discussions, avec des autorisations distinctes et des limites de session.
- **La fonction « Comptes »** permet de renommer un espace de travail et d’en supprimer un ajouté, avec sa session, son journal, ses sources et sa clé de signature. L’espace de travail principal ne peut pas être supprimé depuis le panneau.

### Importation par lots et groupes de comptes

Ouvrez **Comptes → Importer des comptes** pour ajouter plusieurs comptes, associer les fichiers par nom et voir le résultat de chaque connexion. Chaque compte dispose de son propre espace de travail. Les groupes peuvent copier certains réglages depuis un modèle sans fusionner les sessions, les clés ni les preuves. Consultez [le guide d’importation et des groupes](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) et [le tableau de bord du pool MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Se déconnecter

**Compte → Se déconnecter de Telegram** (avec la surveillance en pause) demande à Telegram de mettre fin à la session ; celle-ci disparaît donc également de la rubrique **Paramètres → Appareils** du compte, et la session est supprimée du coffre-fort de l’espace de travail. Le journal, les sources, les paramètres et la clé de signature sont conservés, et le journal enregistre la déconnexion. L’espace de travail appartient toujours à son compte : seul ce compte peut s’y reconnecter. Si Telegram ne répond pas, la session est tout de même supprimée ici et le panneau l’indique ; mettez-y fin dans Telegram sous **Paramètres → Appareils**.

## Convertir une session Telethon hors ligne

Le panneau importe directement les fichiers `.session`. Pour une conversion hors ligne vers un fichier StringSession, exécutez depuis le dossier du projet :

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

Le convertisseur lit uniquement les fichiers SQLite de Telethon (jusqu’à 64 Mio), ne modifie jamais les données d’entrée, n’effectue aucune requête réseau et refuse de remplacer un fichier de sortie existant.

## Assurer la sécurité des fichiers de compte

- Traitez chaque `.session`, fichier ZIP TData, StringSession, clé d’authentification et fichier JSON de compte comme un mot de passe. TgWitness conserve les informations d’autorisation importées dans son coffre-fort chiffré ; vous pouvez supprimer les fichiers d’origine par la suite.
- N’exécutez pas la même autorisation dans deux programmes à la fois. Telegram pourrait la révoquer (`AUTH_KEY_DUPLICATED`), et les deux instances cesseraient alors de fonctionner.
- Une session expirée ou révoquée ne peut pas être réactivée par conversion. Veuillez vous reconnecter.

## Dépannage

| Message ou symptôme | Que faire ? |
| --- | --- |
| *Impossible de lire cette session. Fermez son client d'origine…* | Le fichier SQLite est ouvert ou inachevé (fichier sidecar `-journal`/`-wal`). Fermez correctement le programme d'origine et recopiez le fichier. |
| *Schémas SQLite Telethon pris en charge : 7 et 8* / *Pyrogram… 2 et 3* | Ce fichier a été créé à l'aide d'une version très ancienne ou inconnue de la bibliothèque. Veuillez vous connecter par téléphone ou via un code QR à la place. |
| *Seules les sessions d'utilisateurs autorisées en production sont prises en charge* | Le fichier Pyrogram appartient à un bot ou au réseau de test. |
| *L'archive TData dépasse 512 entrées ou 32 Mio* | Seuls les fichiers ZIP « `key_datas` » et « `D877F783D5D3EF8Cs` » sont concernés, et non l'intégralité du dossier. |
| *Impossible de déchiffrer TData. Vérifiez le code d'accès local du bureau.* | Saisissez le code d'accès local de Telegram Desktop dans le champ « **Code d'accès » ou « Texte de session** ». |
| *Importez un compte TData à la fois* | Telegram Desktop disposait de plusieurs comptes ; voir la section « [Formats non pris en charge](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#unsupported-formats) ». |
| *Certains fichiers décrivent différents comptes ou identifiants API* | Sélectionnez les fichiers d’un seul compte. |
| *Le fichier JSON ne contient aucune information d'identification ou d'autorisation prise en charge par l'API.* | Vérifiez les noms des champs dans [le fichier JSON du compte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#account-json). |
| *Métadonnées de l'API uniquement* | Le fichier JSON ne contient pas de session. Ajoutez le fichier « `.session` » ou utilisez votre téléphone/le code QR. |
| *La clé d'authentification HEX doit contenir l'intégralité des 512 caractères hexadécimaux* | La clé est tronquée ou contient « `…` ». |
| L'identifiant du compte ne correspond pas à celui du compte importé | L'identifiant utilisateur du fichier diffère de celui indiqué par Telegram ; ce fichier concerne un autre compte. |
| Ce compte appartient déjà à un autre espace de travail | Ouvrez cet espace de travail au lieu d'ajouter le compte deux fois. |
| Connecté, mais il manque un groupe privé dans la liste des discussions sous « **Sources ».** | Vérifiez l’adhésion. Le sélecteur examine les 1 000 premières conversations ; augmentez cette limite dans la section « **Paramètres** ». |
| Échec de la connexion via le proxy | Vérifiez le mode de routage et le mode IP. Le mode MTProxy automatique tente une autre entrée valide. Le mode « Masquer l'IP » attend ; le mode de secours explicitement sélectionné peut se connecter directement après le délai configuré. Voir [les modes de routage](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/#ip-modes). |

Voir également : [connexion et sécurité](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/) pour les proxys et le chiffrement, ainsi que [le fonctionnement de la collecte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/) des données enregistrées après connexion.
