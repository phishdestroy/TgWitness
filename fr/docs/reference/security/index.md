# Sécurité et traitement des données

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/security/

Modèle de menace, modèle d’accès, données confidentielles au repos, exposition du réseau, importation de sessions et procédure de signalement d’une vulnérabilité.

This page describes access，storage and network protection in a local or server workspace． For collection on a GitHub runner or in an Intel TDX confidential VM，see the [verification modes](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#verification-scope)，which add checks of the collection environment． Account connections，notifications，timestamps，off-site copies and witnesses have their own routing settings．

| Domaine | En bref |
| --- | --- |
| Accès | Clé d'administrateur et accès limité aux comptes/discussions, sept niveaux d'autorisation et sessions révocables ; « localhost » par défaut |
| Secrets au repos | La session, la paire API, la clé de signature et les paramètres de proxy sont chiffrés à l'aide de Fernet |
| Messages et fichiers multimédias | Stockage en clair : utilisez le chiffrement du disque et des autorisations strictes |
| Intégrité | Chaîne de hachages SHA-256 et signature Ed25519 sur chaque enregistrement |
| Local trust boundary | The host administrator controls the workspace and its signing key；independent checkpoints retain an earlier journal boundary |

Pour les rapports de vulnérabilité, veuillez consulter la [politique de sécurité](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

## Modèle d'accès

Le jeton du panneau principal confère un contrôle total. D’autres personnes peuvent bénéficier d’un [accès limité](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) : espaces de travail et discussions sélectionnés, autorisations, durée de validité, restrictions d’adresse IP, limites de connexion et sessions révocables. Un accès limité à une discussion ne permet pas d’effectuer des opérations sur l’ensemble de l’espace de travail, même si l’autorisation correspondante est cochée. Les espaces de travail partagent un processus et n’isolent pas les données de l’administrateur hôte.

Par défaut, le panneau écoute sur localhost. La connexion via le navigateur échange un jeton d’accès contre des identifiants de session ; le navigateur l’envoie sous forme de jeton « bearer ». Celui-ci est conservé dans sessionStorage plutôt que dans un cookie d’authentification. Le verrouillage ou la déconnexion efface la session du navigateur. La fermeture du navigateur ou la fin d’une session n’interrompt pas la collecte.

Les jetons émis et les identifiants de session sont conservés sous forme de hachages dans le coffre-fort chiffré. La révocation met fin aux sessions associées ; les modifications d’autorisations s’appliquent aux demandes ultérieures. Les fichiers téléchargés ne peuvent pas être récupérés. L’administrateur peut également limiter ses propres sessions de navigateur, mais les scripts utilisant directement le jeton du panneau principal conservent un accès complet et contournent ces limites de session de navigateur.

Les échecs d’authentification sont limités en nombre par adresse client. Les restrictions IP s’appliquent à l’ adresse détectée par l’application ; veuillez vérifier le comportement du proxy inverse avant de vous y fier . Les identifiants de Witness restent des identifiants distincts, en lecture seule, destinés au contrôle de l’état de fonctionnement.

### Accès à la démo

`/api/demo-access` est un bootstrap délibérément non authentifié destiné à une démonstration synthétique isolée et explicitement lancée. Il émet une capacité distincte valable pendant la durée de vie du processus, jamais le véritable jeton de panneau ni une substitution de TGWITNESS_TOKEN. Son émission et son utilisation nécessitent un pair en boucle fermée et un hôte, sans en-têtes transférés ni requête inter-origines. Des espaces de travail supplémentaires ou une session autorisée désactivent ce chemin. Les espaces de travail actifs n’émettent jamais cette capacité. La démonstration ne permet pas de connecter des comptes ni de modifier les paramètres de collecte.

## Contenu des panneaux et exportations

Le site n’utilise aucune police externe, aucun outil d’analyse, aucune ressource CDN ni aucun média distant intégré. Le texte provenant de Telegram est inséré sous forme de texte brut, et non en HTML. Les pièces jointes téléchargées sont fournies sous forme de pièces jointes binaires. Les exportations au format JSONL conservent les chaînes de caractères d’origine ; le format HTML les échappe ; les cellules CSV susceptibles de contenir des formules sont préfixées d’une apostrophe.

Les exportations excluent les secrets d’authentification et de signature, mais contiennent délibérément les métadonnées sources collectées, les identifiants et, éventuellement, du contenu personnel ou sensible. Des hachages d’accès à Telegram et des références de fichiers peuvent apparaître dans les métadonnées sources brutes.

## Secrets au repos

Telegram API credentials，the session and signing key are encrypted with Fernet． For local messages and media，encryption is provided by the host's disk or volume； the workspace stores ordinary files．Exports can use a password-protected AES-256 ZIP， and off-site copies use AES-256-GCM．

The vault key defaults to the protected data directory．Use an external master-key file below to store it separately．On Unix，new private-key files use mode 0600 and new data directories use 0700；on Windows，set the directory ACL for the service account and authorized administrators．Existing directory permissions are retained．

### Clé principale externe

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode．Disk encryption protects the local message and media files in either mode；see [connection and data protection](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/) for setup details．

## Proxys et chemins de réseau

La configuration du proxy est chiffrée dans le coffre-fort. Les mots de passe et les secrets MTProxy ne sont ni renvoyés par l’API ni consignés dans les enregistrements de preuves. Chaque espace de travail choisit son itinéraire Telegram et un [mode IP](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/#ip-modes).

**L'option « Masquer l'adresse »** désactive le recours direct à Telegram et nécessite un proxy pour les requêtes HTTP externes. Le mode de secours explicitement sélectionné autorise l'accès direct à Telegram après un certain délai ; le mode tunnel/VPN autorise les routes directes. Le choix du mode tunnel n'entraîne ni l'installation ni la vérification d'un VPN. Ces paramètres ne contrôlent pas l'ensemble du trafic de la machine, ni les navigateurs, ni les gestionnaires de paquets, ni la résolution DNS de l'hôte proxy local.

MTProxy achemine uniquement le trafic Telegram. Les requêtes externes peuvent utiliser un proxy SOCKS5/HTTP distinct, la route SOCKS5/HTTP de l’espace de travail ou une route directe autorisée ; elles peuvent également être désactivées. Le témoin indépendant dispose de ses propres paramètres de transport. L’authentification SOCKS5/HTTP CONNECT standard n’est pas chiffrée par ces protocoles de proxy eux-mêmes. Les faux secrets TLS MTProxy ne sont toujours pas pris en charge.

## Connexion et importation de sessions

Les fichiers .tgwitness-session convertis contiennent un secret d’autorisation en texte clair jusqu’à ce qu’ils soient chargés et stockés dans le coffre-fort. L’interface en ligne de commande (CLI) hors ligne accepte les schémas Telethon validés. L’importation via le panneau accepte en outre Pyrogram SQLite, les fichiers ZIP TData modernes à compte unique, ainsi que les entrées JSON documentées. Elle est authentifiée, limitée à quatre fichiers / 8 MiB, et traite les téléchargements en mémoire sans extraction d’archive ni enregistrement des fichiers d’origine. Les identifiants normalisés ne sont renvoyés qu’au navigateur authentifié à l’origine de la requête ; ils sont enregistrés dans le coffre-fort chiffré une fois l’autorisation Telegram validée. Protégez les fichiers originaux et convertis, et évitez que des clients simultanés ne clonent une autorisation.

Le traitement des données vérifie les sommes de contrôle des conteneurs, les hachages de déchiffrement locaux et les longueurs de structure. Un code d'accès local fourni pour la version Desktop est utilisé de manière temporaire et n'est pas stocké. Cet analyseur syntaxique limité ne garantit pas la compatibilité de toutes les versions de Desktop. Les images QR sont générées localement, contiennent des jetons de connexion Telegram à durée de vie limitée et ne sont jamais envoyées à un service de rendu externe. Le verrouillage, le changement d’espace de travail, une nouvelle connexion et les changements d’itinéraire annulent les tentatives QR en attente. Le rechargement ou la fermeture d’un onglet peut laisser une tentative en attente jusqu’à son expiration. Une connexion QR réussie impose tout de même la liaison du compte. Les corps de requêtes API standard restent limités à 16 KiB ; la route d’importation authentifiée accepte jusqu’à 12 MiB de JSON encodé, en appliquant séparément la limite inférieure pour le fichier décodé.

Les codes de connexion et les mots de passe de vérification en deux étapes de Telegram ne sont pas conservés. L’état du numéro de téléphone et du hachage du code est conservé en mémoire pendant l’autorisation. Les sessions Telegram permettent d’accéder au compte ; ne téléchargez jamais de répertoire de données, de session, de jeton, de clé de coffre-fort ou de clé de signature privée sur GitHub.

## Journaux et transport

La réponse par défaut de validation de l’API est remplacée afin qu’elle ne renvoie pas les valeurs des identifiants. La journalisation des accès à l’application est désactivée. Ne configurez pas de proxy inverse pour enregistrer les en-têtes d’autorisation ou le corps des requêtes. Le protocole HTTP transmet les jetons et les identifiants de connexion en clair : utilisez HTTPS ou un tunnel SSH dès que vous quittez localhost.

## Limites d’intégrité

Local verification checks record signatures，the hash chain，attachments and the export manifest． The administrator holds the local signing key and can create another signed journal； an independently retained checkpoint detects replacement of the prefix it covers． Keep the key fingerprint and checkpoints with the recipient or an independent witness．

For independently checked collection，choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)． Their verifiers check workflow provenance or hardware measurements in addition to archive integrity． Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies； the [evidence format](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#verification-scope) describes the checks for each mode．

## Si vous soupçonnez un problème

Preserve the original data directory and use a separate copy for analysis． Report the affected version，operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)，keeping account data and credentials private．
