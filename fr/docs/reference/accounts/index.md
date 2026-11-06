# Formats des comptes et des sessions

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/

Connectez-vous par téléphone, via un code QR ou une clé d'authentification, importez des sessions Telethon, Pyrogram ou Telegram Desktop, et gérez plusieurs comptes.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Pour commencer](https://phishdestroy.github.io/TgWitness/fr/docs/reference/quickstart/)

![Pour commencer](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

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

Vous pouvez vous connecter sans créer d’application API Telegram. Lorsqu’aucune paire n’est saisie, importée ou déjà enregistrée dans l’espace de travail, TgWitness choisit une paire dans son pool intégré de paires API publiques 50 (`tgwitness/api_pool.py`), en privilégiant Telegram Desktop pour une nouvelle connexion et en conservant en priorité une paire enregistrée ; les candidats restants sont mélangés. Si Telegram refuse une paire (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), la suivante est essayée, jusqu’à huit par connexion ; les paires refusées sont ignorées jusqu’au redémarrage. La paire ayant permis la connexion est enregistrée avec le compte et réutilisée pour celui-ci. Un identifiant **API** et un hachage **API** identifient l’application auprès de Telegram ; ils n’autorisent pas un compte à eux seuls.

Les champs de connexion manquants utilisent une paire appareil/système d'exploitation déterministe issue des catalogues [opentele2 2.0.0 fournis](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735) : `2040` (ordinateur de bureau), `6` (Android), `21724` (Android X), `10840` (iOS), `2834` (macOS) et `2496` (Web). L'identifiant de compilation source d'Android `4` utilise également le catalogue Android, tel qu'identifié dans [les variables de compilation (BuildVars) de Telegram pour Android](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). La valeur par défaut pour Web est A ; un suffixe de version d’application `K` ou un pack de langue `macos` importé sélectionne K, et la version `0.7.0` sélectionne Webogram. Les identifiants d’application inconnus conservent les valeurs par défaut de l’hôte de Telethon. Les champs importés prévalent toujours, y compris une version d’application plus ancienne et un pack de langue vide. Le catalogue ne modifie jamais l’identifiant API/hachage. Son instantané de version est vérifié explicitement, et non récupéré lors de la connexion. Un profil enregistré reste stable après les mises à jour.

`account.getAuthorizations` rend compte des métadonnées d’autorisation enregistrées par Telegram ; il ne s’agit pas d’un simple écho de chaque nouveau `initConnection`. Comparez-le avec le profil réellement envoyé. La connexion d’une autorisation existante ne valide pas le hachage API associé : `initConnection` envoie l’ID API, tandis que le hachage est utilisé par les demandes de connexion.

Après une nouvelle autorisation par téléphone ou QR code, TgWitness demande la configuration, le centre de données le plus proche, le statut en ligne, les langues (lorsque le pack de langues n’est pas vide), les mises à jour de l’application et les mises à jour des conditions d’utilisation, avec un intervalle de 0.3 à 1.5 secondes entre chaque requête. La mise à jour du statut marque brièvement le compte comme étant en ligne. Cette séquence s’exécute une seule fois à la fin de la connexion, et non lors d’importations, de reconnexions ou de redémarrages. L’autorisation est enregistrée en premier ; une requête ayant échoué interrompt la séquence sans nouvelle tentative ni annulation de la connexion. Les résultats sont enregistrés sous le nom `account.initialized`, avec les noms d’erreur plutôt que le corps des réponses. La séquence ne constitue pas une garantie contre les restrictions de compte.

Pour `tdesktop` , en l'absence de `tz_offset` , le décalage UTC local du serveur est utilisé, arrondi à 900 secondes à l'aide de l'algorithme [opentele2](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT ; licence en `tgwitness/client_profiles.LICENSE` ). Il est actualisé à chaque connexion afin de refléter les changements liés à l'heure d'été. Un `tz_offset` importé prévaut sur toutes les plateformes et est conservé tel quel, y compris s’il est égal à zéro. Les autres entrées `initConnection.params` sont conservées. Le formulaire de connexion HTTP accepte le fuseau horaire numérique renvoyé par l’importation de fichier ; les valeurs booléennes, les fractions et les décalages hors de la plage prise en charge sont rejetés.

Les routes directes, SOCKS5 et HTTP CONNECT utilisent le protocole `ConnectionTcpObfuscated` de Telethon (MTProto abrégé et obscurci). HTTPS CONNECT conserve le protocole TLS jusqu’au proxy et utilise le même transport obscurci à l’intérieur du tunnel. MTProxy conserve son transport intermédiaire aléatoire obligatoire et sa gestion des secrets. Les changements de route appliquent les mêmes choix. L’obscurcissement modifie le formatage des paquets ; il ne masque pas le compte ni ses métadonnées client vis-à-vis de Telegram et n’implique pas d’immunité face aux restrictions.

Après la connexion d’un client autorisé, TgWitnessvérifie la configuration, le centre de données le plus proche, l’autorisation actuelle, la base de référence de la couche révisée, les langues, les mises à jour de l’application et les mises à jour des conditions d’utilisation. Ces diagnostics s’exécutent une fois par instance de client, avant la collecte, et sont affichés dans les détails de la connexion avec leur heure. `account.connection_checked` enregistre le résultat sans hachages de session, adresses IP, jetons ni hachages d’API. Il n’accepte jamais les conditions générales ni n’installe de mises à jour. Un échec de requête ou un FloodWait interrompt les requêtes suivantes ; un résultat manquant reste inconnu. Les vérifications locales peuvent toujours signaler leurs résultats tandis que les vérifications réseau sont ignorées.

Les diagnostics FloodWait conservent la méthode TL ayant échoué, les éventuels wrappers Takeout/range, l'attente demandée par le serveur et le délai effectif dans `telegram.backoff`. Les détails de connexion indiquent la méthode et le délai lorsque les requêtes sont mises en pause. Le diagnostic inclut les compteurs d’appels client par méthode depuis la création de ce client ; ils comptabilisent séparément la résolution des pairs imbriqués, mais ne comptent pas les paquets ni les tentatives de réessai internes de Telethon. Les compteurs actuels sont également disponibles sous le nom d’ `collector.rpc_activity`dans l’API d’état. Aucun argument de requête, nom d’utilisateur, hachage d’accès ou texte d’exception n’est inclus. Le dernier diagnostic et le délai complet sont conservés après un redémarrage. Les attentes antérieures sans enregistrement de méthode ne peuvent pas être attribuées rétroactivement. Voir [: limites d’exportation](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) pour l’examen du code source et la distinction entre la découverte et l’acquisition de l’historique.

`official_app=True` ou `False` est l'indicateur d'autorisation actuelle de Telegram. Aucune de ces valeurs ne permet de déterminer si le compte est restreint, de confiance ou sous observation. Les instantanés `account.devices` existants en mode preuves conservent l'historique de tous les appareils connectés ; les diagnostics de connexion ne conservent que la description de l'appareil actuel.

Avant la connexion, des contrôles préventifs comparent la plateforme API, le pack linguistique, les formats de l'appareil/du système d'exploitation et de la version de l'application, les paramètres régionaux du système mobile, ainsi que la couche de schéma réelle de Telethon à la référence du catalogue vérifiée. Des avertissements apparaissent dans le journal du serveur et dans les métadonnées de l'état du compte ; ils ne remplacent jamais les valeurs importées ni ne modifient la couche de schéma. Une couche différente constitue un signal de vérification de compatibilité, et non la preuve d’un compte bloqué ou soumis à des restrictions. Ces vérifications et le code d’erreur `official_app` ne certifient pas que Telegram considère le compte comme à l’abri de toute restriction. Le statut de compte déconnecté utilise le profil enregistré au lieu de générer une nouvelle description de l’appareil.

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

Les formulaires **Fichiers**, **Clé d'authentification** et d'importation en masse affichent l'avertissement de session parallèle avant la connexion. Par défaut, les autorisations importées sont réutilisées. Gardez le client d'origine fermé tant que sa clé est utilisée ici. **Fichiers** et **Clé d'authentification** proposent également **Créer une autorisation indépendante**, décrite ci-dessous. L'importation en masse utilise toujours le mode direct. La connexion par téléphone et par QR code interactif crée des autorisations distinctes. L'en-tête d'avertissement reste visible dans le formulaire d'importation ; son explication complète s'ouvre automatiquement lorsque des fichiers ou une chaîne de clé/session sont fournis. Il peut être masqué après lecture, afin que le sélecteur de fichiers et les commandes de connexion restent utilisables sur un téléphone.

- Les fichiers sont convertis **en mémoire** sur votre serveur TgWitness. Les fichiers téléchargés ne sont pas stockés, les fichiers ZIP ne sont pas extraits sur le disque et aucun service externe n’est sollicité.
- La session ainsi obtenue est ensuite vérifiée auprès de Telegram. Si un fichier mentionne un identifiant d’utilisateur, celui-ci doit correspondre au compte indiqué par Telegram.
- Les fichiers décrivant différents comptes ou différents identifiants API sont rejetés au lieu d’en choisir un seul.
- Le champ **« Code d'accès ou texte de session »** contient le champ « TData local passcode », une zone permettant de coller une StringSession et **de lire des fichiers sans se connecter** (remplit le formulaire sans contacter Telegram).

### Créer une autorisation indépendante

Sélectionnez **Créer une autorisation indépendante** avant de connecter des fichiers importés ou une clé d’authentification. TgWitness connecte brièvement le donneur importé, l’utilise pour approuver le jeton de connexion QR du nouveau client, puis déconnecte le donneur immédiatement après l’approbation. Le nouveau client dispose de sa propre clé d’autorisation et d’un profil de bureau sélectionné séparément. Les identifiants API et le profil d’appareil fournis par le donneur ne sont utilisés que pour la connexion du donneur. Aucune autorisation existante n’est déconnectée ni révoquée.

**Gardez le client d'origine du donneur entièrement fermé pendant cette étape.** La connexion initiale utilise toujours sa clé copiée ; ce mode ne permet donc pas d’éliminer ce risque initial d’utilisation parallèle. Une fois la nouvelle autorisation connectée, le propriétaire peut rouvrir le client d’origine et utiliser les deux de manière indépendante. La connexion interactive **via un code QR** permet au client d’origine d’approuver la connexion sans copier ni connecter sa clé ici.

Si Telegram demande 2FA, ce mode utilise `twoFA` issu du fichier JSON sélectionné lorsqu’il est présent, ou demande le mot de passe. Un mot de passe importé rejeté renvoie à la fenêtre de saisie du mot de passe. Les mots de passe ne sont pas enregistrés. La clé candidate est enregistrée sous forme chiffrée dans le `independent_login.enc`, y compris les modifications effectuées lors de la migration du centre de données. Après une interruption, sélectionnez le même donneur et cette option pour reprendre la clé candidate enregistrée. L’espace de travail reste réservé à ce compte ; un échec de finalisation ne supprime pas le nouvel espace de travail. Conservez son répertoire de données et sa clé de coffre-fort. Les identifiants finaux et l’enregistrement du journal `account.authorized` incluent la méthode d’importation, les formats d’entrée et l’ID API du donneur, sans la clé ni le mot de passe du donneur.

Le 5 novembre 2026, un compte dédié a passé avec succès des tests en conditions réelles avec les donateurs Telethon, Pyrogram et TData : achèvement de l’authentification à 2 facteurs (2FA), nouvelles clés d’autorisation distinctes, accès simultané par le donateur et un nouveau client, et lecture d’un canal public. Le cas Téléthon a également permis de reprendre un candidat enregistré après une interruption à l’étape du mot de passe. Chaque nouvelle autorisation a permis de mener à bien les six requêtes d’initialisation post-connexion, et son journal signé a été vérifié. La session d’origine est restée utilisable dans les quatre formats fournis.

La base de données des erreurs [RPC de Telegram](https://core.telegram.org/api/errors.json) associe `FRESH_CHANGE_ADMINS_FORBIDDEN` au changement d’administrateur, `FRESH_CHANGE_PHONE_FORBIDDEN` au changement de numéro de téléphone et `FRESH_RESET_AUTHORISATION_FORBIDDEN` à la révocation d’autres sessions, à la modification de leur durée de vie ou à l’enregistrement d’une clé d’accès. `SESSION_TOO_FRESH_*` et `PASSWORD_TOO_FRESH_*` concernent les transferts de propriété et les retraits de revenus ou de cadeaux. Il ne s’agit pas d’opérations de collecte ; une nouvelle connexion n’ implique pas une interdiction générale de lecture de 24 heures. L’exportation peut renvoyer `TAKEOUT_INIT_DELAY_*` séparément. TgWitness conserve les pauses demandées par le serveur et ne tente pas automatiquement de faire accepter à nouveau le jeton ni de révoquer des sessions pour contourner les restrictions.

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
- Le profil de connexion utilise `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` et `tz_offset` (facultatif) (secondes par rapport à l'UTC, de -43200 à 50400). Les champs fournis ont priorité sur les valeurs par défaut générées et sur la langue du panneau/navigateur . Les alias en conflit sont rejetés. Le profil résolu est enregistré dans les identifiants chiffrés de l'espace de travail et réutilisé après le redémarrage, y compris sa version d'application.
- `phone`, les paramètres de proxy et les jetons d'appareil sont **ignorés**. `twoFA` est en lecture seule lorsque **Créer une autorisation indépendante** est sélectionné ; l'importation directe l'ignore.
- Un fichier JSON ne comportant pas de champ d’autorisation pris en charge ne contient que des métadonnées. Ajoutez son fichier de session ou poursuivez avec une connexion par téléphone ou via un code QR. Un fichier JSON contenant une session prise en charge ou une clé d’authentification (Auth Key) peut autoriser l’accès à lui seul ; voir [Account JSON](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData correspond au dossier « `tdata` » de l’application Telegram Desktop (l’application multiplateforme disponible sur desktop.telegram.org).

| Système | Emplacement par défaut : `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portable : à côté de `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Pour l'importer :

> **Avertissement concernant les sessions parallèles.** L'importation directe de TData réutilise la clé d'autorisation de Telegram Desktop. N'utilisez pas cette clé simultanément dans Desktop et TgWitness. Telegram peut invalider l'autorisation avec `AUTH_KEY_DUPLICATED`, rendant les deux copies inutilisables jusqu'à une nouvelle connexion.
>
>
>
> Fermez complètement Desktop, y compris son processus dans la barre d’état, et gardez cette instance fermée pendant que TgWitness utilise la session importée. **: Quittez, ne vous déconnectez pas et ne révoquez pas la session :** la révocation invalide également la copie importée. Si vous avez besoin que les deux clients fonctionnent, sélectionnez **Créer une autorisation indépendante** et gardez Desktop fermé jusqu’à ce que la nouvelle connexion aboutisse, ou connectez-vous à TgWitness par téléphone ou via un QR code. Un compte dédié est recommandé, mais cela ne garantit pas la sécurité de l’utilisation parallèle des clés clonées.
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
| `string_session` (`session_string`, `session_str` ; ancien `session`) | Texte « Telethon StringSession », et non un nom de fichier |
| `auth_key` (`auth_key_hex`) + `dc_id` | Clé d'authentification complète de 512 caractères et DC 1 à 5 |
| `user_id` (`id`) | Facultatif ; vérification effectuée par rapport à Telegram avant l'enregistrement de l'autorisation |
| `device_model` (`device`) | Description du dispositif de connexion |
| `system_version` (`sdk`) | Version du système d'exploitation de connexion |
| `app_version` | Version de l'application envoyée à Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Langue du client, langue du système et pack linguistique du client ; un champ `lang_pack` vide est autorisé |
| `tz_offset` | Décalage UTC facultatif en secondes, envoyé dans `initConnection.params` ; chaîne de caractères entière ou décimale |

Si un alias et le nom principal sont tous deux présents, ils doivent correspondre. Les champs de session Telethon explicites ont priorité sur un blob `session` générique dans un autre format. Si les deux contiennent des sessions Telethon reconnaissables, elles doivent décrire la même autorisation. En l'absence de champ explicite, `session` doit être une StringSession Telethon valide. Exemples :

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

Utilisez **Comptes → Importer des comptes** pour ajouter plusieurs comptes, associer des fichiers par nom de base et consulter le résultat de chaque connexion. Chaque compte dispose de son propre espace de travail.

Un groupe regroupe des comptes liés sans fusionner leurs sessions, leurs clés ou leurs preuves. **Ouvrir le groupe** sur **Comptes** mène à sa page à l'adresse `/groups/<id>`:

- **Comptes:** itinéraire de connexion, observation et dernier message de chaque membre, avec les boutons « **Tout** démarrer » et « **Tout mettre en pause** ».
- **Nécessite une attention:** les comptes dont la session a été déconnectée, qui sont indisponibles ou qui présentent un problème de connexion, d’acquisition, de source ou de média ; chaque nom renvoie vers sa fiche.
- **Les discussions impliquant plusieurs comptes permettent de visualiser :** les sources partagées, les comptes qui les surveillent et les interruptions dans la période d’observation de l’espace de travail disponible (jusqu’à sept jours). **L’exportation avec N comptes** répartit l’exportation d’un canal ou d’un supergroupe entre eux et signe une seule archive.
- **Exporter le groupe:** une image ZIP contenant l’exportation signée de chaque compte sous `accounts/` et `manifest.json` répertoriant leurs SHA-256 et leurs empreintes de clé, signées par l’ espace de travail principal dans `manifest.signature.json`. Vérifiez chaque archive de compte individuellement à l’aide de `python -m tgwitness.verify` et l’empreinte digitale de confiance de ce compte.

Les membres partagent les paramètres du groupe ; un compte peut conserver ses propres valeurs. Consultez la section sur [les paramètres partagés](https://phishdestroy.github.io/TgWitness/fr/docs/reference/settings/#account-groups), [le guide d'importation et des groupes](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) ainsi que [le tableau de bord du pool MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Se déconnecter

**Compte → Se déconnecter de Telegram** (avec la surveillance en pause) demande à Telegram de mettre fin à la session ; celle-ci disparaît donc également de la rubrique **Paramètres → Appareils** du compte, et la session est supprimée du coffre-fort de l’espace de travail. Le journal, les sources, les paramètres et la clé de signature sont conservés, et le journal enregistre la déconnexion. L’espace de travail appartient toujours à son compte : seul ce compte peut s’y reconnecter. Si Telegram ne répond pas, la session est tout de même supprimée ici et le panneau l’indique ; mettez-y fin dans Telegram sous **Paramètres → Appareils**.

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
| Échec de la connexion via le proxy | Vérifiez le mode de routage et le mode IP. Le mode «MTProxy» tente automatiquement une autre entrée valide. Le mode «Hide the address » attend ; le mode «Direct », en dernier recours, peut se connecter directement après le délai configuré. Voir [les modes de routage](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/#ip-modes). |

Voir également : [connexion et sécurité](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/) pour les proxys et le chiffrement, ainsi que [le fonctionnement de la collecte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/) des données enregistrées après connexion.
