# Architecture

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/architecture/

Les composants du collecteur, du panneau de contrôle, du journal, des workers et de Witness, ainsi que la manière dont les données circulent entre eux.

Un processus Python héberge le panneau FastAPI et un nombre illimité d’espaces de travail isolés, chacun doté d’un client de compte utilisateur Telethon. SQLite contient un journal d’événements signé, accessible en écriture seule, ainsi que des paramètres opérationnels modifiables. Un coffre-fort chiffré contient les identifiants API, la StringSession et la clé de signature. L’interface utilisateur est constituée d’un simple ensemble de fichiers HTML/CSS/JavaScript : aucune compilation Node, aucun CDN ni aucun téléchargement d’environnement d’exécution de l’interface utilisateur n’est nécessaire.

| Module | Responsabilité |
| --- | --- |
| collector.py | Autorisation, sélection des dialogues, mises à jour, instantanés, file d'attente des médias, surveillance de la connexion |
| interactions.py / telegram_client.py | Actions explicites du panneau, reçus signés, identifiants de requête persistants et politique de relance des appels de retour/de rejoignement au niveau de la tâche |
| message_content.py | Comparaison des messages observables, à l'exclusion des métadonnées d'accès au réseau de transport |
| workers.py | Attendez que les processus d’exportation des fichiers soient terminés avant de procéder au nettoyage suite à l’annulation |
| store.py | Transactions WAL, chaîne d'événements ordonnée, filtres de requête, paramètres opérationnels |
| security.py | Création de fichiers privés, coffre-fort chiffré, signature Ed25519, verrouillage à processus unique |
| evidence.py | Exportation du journal complet, des dérivés, des points de contrôle, vérification des pièces jointes |
| verify.py | Vérificateur autonome en lecture seule (bibliothèque standard + cryptographie) : archives, couverture, journaux de témoins et publications sur les chaînes, fichiers de profil |
| app.py | API authentifiée, cycle de vie, validation des requêtes, panneau statique |
| profiles.py | Collecteurs de comptes multiples, contrôleur d’accès partagé, cycle de vie par espace de travail |
| access.py | Subventions ciblées, vérifications des autorisations, restrictions d'adresses IP, limites de session et console d'administration |
| proxy_catalog.py | Instantanés des flux publics, contrôles de transport, pool de proxys partagés et sélection basée sur l'état de santé |
| provenance.py | Mesures signées de l’identité, du code et des dépendances lors de l’acquisition et de l’exécution |
| network.py | Itinéraires validés par espace de travail ; statut et preuves expurgés ; options de transfert Telethon |
| sessions.py | Conversion hors ligne en mode lecture seule des schémas SQLite de Telethon ayant fait l'objet d'une révision |
| account_import.py | Détection et normalisation en mémoire des fichiers de compte pris en charge et des fichiers JSON |
| tdata.py | Lecteur ZIP TData moderne et limité, validation des sommes de contrôle et du déchiffrement, aucune extraction |
| doctor.py | Vérifications de l'état de préparation locales sans collecte de données, connexion ni installation de logiciel |
| download.py | Téléchargement d’exportation en flux authentifié avec lectures limitées et sans écrasement |
| monitoring.py | Politique d’événements validée par espace de travail et règles relatives aux pièces jointes par type, partagées par les gestionnaires, avec statut et accusés de réception signés |
| scope.py | Périmètre d’observation (discussions sélectionnées, dossier Telegram, compte entier), types de sources, exclusions, niveaux de vérification |
| dossier.py | Profils des utilisateurs par discussion, établis à partir des enregistrements conservés : faits accompagnés de références d’enregistrement, SHA-256/pHash des avatars, extraction des mentions |
| witness_api.py | Les jetons de témoin en lecture seule et l'en-tête signé du journal qu'ils permettent de récupérer |
| witness.py | Processus de témoignage indépendant : clé et journal propres, vérifications d'en-tête, publications signées sur le canal, exportation |
| alerts.py | Notifications Apprise et liste des notifications du panneau |
| logging_config.py | Journalisation en console et diagnostics de serveur à rotation pour les lancements sans fenêtre |
| static/ | Interface réactive, portail d'accès local, filtres, détails, exportations, configuration du compte |
| demo.py | Journal synthétique clairement identifié, distinct de la collecte réelle |

Les gestionnaires d’observation sont enregistrés avant la connexion. La collecte en temps réel est régulée par l’identité du client actif, son état d’exécution explicite, les sources activées ou le champ d’observation (les modes « dossier » ou « compte entier » ajoutent une nouvelle conversation en tant que source lors de sa première mise à jour), ainsi que par la politique relative aux événements. Les clients rejetés ou remplacés ne peuvent pas contribuer aux mises à jour en temps réel. Les réactions brutes et les mises à jour d’adhésion respectent les limites de visibilité. Le contenu des messages entrants et sa tâche de support durable sont validés ensemble. Les tâches conservent le descripteur TL d’origine et lient son hachage à l’observation du message signé. Les sémantiques « expéditeur », « éditeur » et « suppresseur » sont distinctes.

Chaque espace de travail accepte un seul compte et dispose de son propre répertoire ainsi que de sa propre identité de signature. L’espace de travail principal reste à la racine pour des raisons de compatibilité ; les espaces de travail supplémentaires se trouvent dans profiles/<id>/. Un seul jeton porteur contrôle l’ensemble de l’installation ; les espaces de travail ne constituent pas des entités d’autorisation distinctes. Des verrous de processus protègent les répertoires ; des verrous de base de données sérialisent l’insertion des événements. Chaque ajout est validé de manière synchrone dans le WAL de SQLite en mode synchrone FULL. Des déclencheurs de mise à jour/suppression d’événements empêchent les modifications ordinaires par l’application ; les administrateurs du système de fichiers restent à l’intérieur de la zone de confiance.

L’autorisation de l’API s’effectue via un jeton « bearer ». Les opérations de connexion sont sérialisées et limitées dans le temps. Les téléchargements de compte sont soumis à une limite dédiée de 12 MiB pour le corps encodé et de 8 MiB pour le fichier décodé ; les requêtes API normales conservent la limite de 16 KiB. La conversion s’exécute dans un thread de travail, conserve les téléchargements en mémoire et renvoie les données d’entrée normalisées au navigateur authentifié. La connexion par QR code comporte un candidat par espace de travail, un identifiant à durée de vie limitée, une tâche d’attente et une annulation explicite. Seule l’autorisation acceptée devient le client actif. Telegram FloodWait est renvoyé avec une valeur Retry-After ; les identifiants et les messages d’erreur RPC bruts ne sont pas exposés dans les erreurs de l’API. Les exportations s’exécutent en dehors de la boucle d’événements asynchrone et sont sérialisées par espace de travail. Elles diffusent un instantané de lecture stable et peuvent coexister avec des écritures WAL en cours. Les collecteurs d’espaces de travail partagent le processus et la boucle d’événements.

Les instantanés de l’historique actuel et les mises à jour en temps réel peuvent se chevaucher. Il s’agit de deux observations distinctes, identifiées par leur source ; les doublons ne sont pas masqués automatiquement. Aucune déduction n’est effectuée à partir d’ identifiants manquants, de textes supprimés inventés de toutes pièces, d’énumération forcée des membres ou d’adhésion automatique à un groupe .

Pour les explications destinées aux opérateurs, consultez [le fonctionnement de la collecte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/) ainsi que [les formats des comptes et des sessions](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/).

La configuration réseau est stockée dans le coffre-fort chiffré. L’application d’un itinéraire ferme les anciens clients et annule les connexions en cours ; les connexions ultérieures utilisent cet itinéraire sans repli direct. Une nouvelle installation avec clé externe dérive la clé Fernet de chaque espace de travail à l’aide de HKDF-SHA256 à partir d’un fichier de clé principale et d’un sel aléatoire stocké. Cela permet de protéger les secrets séparément du répertoire de données, et non le contenu en clair du journal ou des médias.

L'accès à la démo locale utilise une capacité de processus générée séparément, jamais le jeton de panneau configuré. L'émission et l'acceptation nécessitent le mode démo explicite, une racine synthétique sans espaces de travail supplémentaires ni session autorisée, un pair/hôte en boucle fermée, l'absence d'en-têtes de transfert par proxy et l'absence de requête de navigateur inter-origines. Les API en production conservent l’authentification par porteur et rejettent les modifications de collecte en mode démo.
