# Sécurité et traitement des données

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/security/

Modèle de menace, modèle d’accès, données confidentielles au repos, exposition du réseau, importation de sessions et procédure de signalement d’une vulnérabilité.

TgWitness s'exécute sur votre propre ordinateur ou serveur. Les connexions aux comptes, la mise à jour de la liste publique de proxys et les services externes optionnels sont soumis à des politiques de routage explicites. Les notifications, les horodatages, les copies hors site et le témoin sont configurés séparément. Cette page répertorie ce qui est protégé, comment, et ce qui relève de la responsabilité de l'opérateur.

| Domaine | En bref |
| --- | --- |
| Accès | Clé d'administrateur et accès limité aux comptes/discussions, sept niveaux d'autorisation et sessions révocables ; « localhost » par défaut |
| Secrets au repos | La session, la paire API, la clé de signature et les paramètres de proxy sont chiffrés à l'aide de Fernet |
| Messages et fichiers multimédias | Stockage en clair : utilisez le chiffrement du disque et des autorisations strictes |
| Intégrité | Chaîne de hachages SHA-256 et signature Ed25519 sur chaque enregistrement |
| Non couvert | Un administrateur système, un jeton de panneau divulgué, l'exhaustivité de la capture |

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

Les identifiants de l’API Telegram, StringSession et la clé privée Ed25519 sont chiffrés à l’aide de Fernet. Par défaut, cette clé est stockée dans le même répertoire de données protégé. Cela réduit le risque d’exposition accidentelle en clair ; cela ne constitue toutefois pas une protection contre un attaquant capable de lire l’intégralité du répertoire. Le contenu des messages et les fichiers multimédias **ne** sont **pas chiffrés** par TgWitness. Utilisez le chiffrement du disque et des autorisations restrictives au niveau du système d’exploitation. Les fichiers de clé privée Unix sont créés avec le mode 0600 ; les répertoires de données nouvellement créés utilisent le mode 0700. Les autorisations existantes des répertoires ne sont pas modifiées. Sous Windows, les listes de contrôle d’accès (ACL) des répertoires sont héritées : limitez-les au compte de service et aux administrateurs autorisés.

### Clé principale externe

Pour un nouveau répertoire de données, TGWITNESS_VAULT_KEY_FILE peut fournir une clé principale aléatoire externe. HKDF-SHA256 et un sel aléatoire distinct permettent de dériver une clé Fernet différente pour chaque espace de travail. Le fichier vault.external.json doit être conservé à des fins de restauration. L’absence ou l’erreur dans les clés principales entraîne un échec de la procédure. Les coffres-forts locaux existants ne sont pas migrés de manière silencieuse. Le processus en cours d’exécution peut accéder à la clé ; il ne s’agit pas d’une isolation HSM. Le panneau indique le mode sélectionné et précise explicitement que le stockage des messages et des médias n’est pas chiffré par l’application. Reportez-vous aux sections « [Connexion », « Proxys » et « Protection des données »](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/) pour consulter le modèle de menace complet.

## Proxys et chemins de réseau

La configuration du proxy est chiffrée dans le coffre-fort. Les mots de passe et les secrets MTProxy ne sont ni renvoyés par l’API ni consignés dans les enregistrements de preuves. Chaque espace de travail choisit son itinéraire Telegram et un [mode IP](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/#ip-modes).

Le mode « Masquer l’IP » refuse la connexion de secours directe à Telegram et nécessite un proxy pour les requêtes HTTP externes. Le mode de secours explicitement sélectionné autorise l’accès direct à Telegram après un certain délai ; le mode tunnel/VPN autorise les routes directes. Le choix du mode « tunnel » n’entraîne ni l’installation ni la vérification d’un VPN. Ces paramètres ne contrôlent pas l’ensemble du trafic de la machine, ni les navigateurs, ni les gestionnaires de paquets, ni la résolution DNS de l’hôte proxy local.

MTProxy achemine uniquement le trafic Telegram. Les requêtes externes peuvent utiliser un proxy SOCKS5/HTTP distinct, la route SOCKS5/HTTP de l’espace de travail ou une route directe autorisée ; elles peuvent également être désactivées. Le témoin indépendant dispose de ses propres paramètres de transport. L’authentification SOCKS5/HTTP CONNECT standard n’est pas chiffrée par ces protocoles de proxy eux-mêmes. Les faux secrets TLS MTProxy ne sont toujours pas pris en charge.

## Connexion et importation de sessions

Les fichiers .tgwitness-session convertis contiennent un secret d’autorisation en texte clair jusqu’à ce qu’ils soient chargés et stockés dans le coffre-fort. L’interface en ligne de commande (CLI) hors ligne accepte les schémas Telethon validés. L’importation via le panneau accepte en outre Pyrogram SQLite, les fichiers ZIP TData modernes à compte unique, ainsi que les entrées JSON documentées. Elle est authentifiée, limitée à quatre fichiers / 8 MiB, et traite les téléchargements en mémoire sans extraction d’archive ni enregistrement des fichiers d’origine. Les identifiants normalisés ne sont renvoyés qu’au navigateur authentifié à l’origine de la requête ; ils sont enregistrés dans le coffre-fort chiffré une fois l’autorisation Telegram validée. Protégez les fichiers originaux et convertis, et évitez que des clients simultanés ne clonent une autorisation.

Le traitement des données vérifie les sommes de contrôle des conteneurs, les hachages de déchiffrement locaux et les longueurs de structure. Un code d'accès local fourni pour la version Desktop est utilisé de manière temporaire et n'est pas stocké. Cet analyseur syntaxique limité ne garantit pas la compatibilité de toutes les versions de Desktop. Les images QR sont générées localement, contiennent des jetons de connexion Telegram à durée de vie limitée et ne sont jamais envoyées à un service de rendu externe. Le verrouillage, le changement d’espace de travail, une nouvelle connexion et les changements d’itinéraire annulent les tentatives QR en attente. Le rechargement ou la fermeture d’un onglet peut laisser une tentative en attente jusqu’à son expiration. Une connexion QR réussie impose tout de même la liaison du compte. Les corps de requêtes API standard restent limités à 16 KiB ; la route d’importation authentifiée accepte jusqu’à 12 MiB de JSON encodé, en appliquant séparément la limite inférieure pour le fichier décodé.

Les codes de connexion et les mots de passe de vérification en deux étapes de Telegram ne sont pas conservés. L’état du numéro de téléphone et du hachage du code est conservé en mémoire pendant l’autorisation. Les sessions Telegram permettent d’accéder au compte ; ne téléchargez jamais de répertoire de données, de session, de jeton, de clé de coffre-fort ou de clé de signature privée sur GitHub.

## Journaux et transport

La réponse par défaut de validation de l’API est remplacée afin qu’elle ne renvoie pas les valeurs des identifiants. La journalisation des accès à l’application est désactivée. Ne configurez pas de proxy inverse pour enregistrer les en-têtes d’autorisation ou le corps des requêtes. Le protocole HTTP transmet les jetons et les identifiants de connexion en clair : utilisez HTTPS ou un tunnel SSH dès que vous quittez localhost.

## Limites d’intégrité

La chaîne de hachages, les déclencheurs de base de données et les signatures détectent certaines modifications ; ils n’empêchent toutefois pas un administrateur local de réécrire et de resigner le journal. Conservez les points de contrôle signés et l’empreinte de la clé publique sur un système distinct. Le mode « Evidence » et la copie hors site (tous deux désactivés par défaut) envoient les hachages des points de contrôle vers des services d’horodatage et des copies chiffrées vers un stockage compatible S3 ; veuillez consulter le [format des preuves](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/). Les journaux de transparence, la signature sécurisée par HSM et la certification formelle de la chaîne de conservation ne sont pas mis en œuvre.

## Si vous soupçonnez un problème

Conservez le répertoire de données d’origine et utilisez une copie distincte pour l’analyse. N’ incluez pas de données Telegram privées ni d’identifiants dans un ticket public. Aucune certification de sécurité indépendante n’est revendiquée.
