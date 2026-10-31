# Fonctionnalités et limites

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/features/

Ce que TgWitness met en œuvre aujourd’hui, ce que la plateforme Telegram limite et ce qui reste à faire à l’avenir.

Référence de conception : 26 octobre 2026. Le principal cas d’utilisation concerne les groupes et canaux Telegram privés accessibles aux comptes connectés. Ce document distingue le comportement implémenté, les limites de la plateforme et les travaux futurs. Un élément de l’architecture cible ne signifie pas que la fonctionnalité existe déjà.

## Application autonome

TgWitness dispose de sa propre procédure d’installation, de son répertoire de données et de son cycle de vie des versions. L’interface web intégrée permet la configuration et la consultation ; les enregistrements exportés peuvent être utilisés de manière indépendante.

L’opérateur connecte ses comptes, choisit les sources visibles pour chacun d’entre eux et obtient un journal d’observation enregistré. Le tableau de bord présente le contenu, les modifications enregistrées, la provenance des observations et les lacunes connues. Un autre enquêteur peut vérifier les données exportées.

Quatre états distincts sont importants : l’autorisation du compte, l’accès à une source, un collecteur opérationnel et la mesure dans laquelle l’exhaustivité de la transmission est établie. Aucun des trois premiers ne prouve automatiquement le quatrième. Un groupe inactif n’est pas nécessairement synonyme de collecteur défaillant.

## Enquêtes collaboratives

Un administrateur peut émettre [des jetons d’accès](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) limités à des espaces de travail et à des discussions individuelles, avec sept niveaux d’autorisation, des restrictions d’adresse IP, une date d’expiration, des limites de connexion et un contrôle des sessions. Un réviseur en lecture seule peut examiner un dossier sans recevoir l’autorisation Telegram ni la clé du panneau principal. L’accès limité aux discussions reste distinct des paramètres applicables à l’ensemble du compte et des exportations complètes du journal.

MTProxy, qui fonctionne automatiquement, maintient des routes Telegram opérationnelles à partir de quatre sources publiques ou d’un catalogue d’opérateurs. [Les modes IP](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/#ip-modes) déterminent si, en cas de défaillance, il faut attendre un autre proxy ou s’il est possible d’utiliser une route directe explicitement autorisée. Les requêtes HTTP externes disposent d’une route distincte et d’un bouton de désactivation.

## Outils d'archivage

La version actuelle `main` ajoute [la collecte de l'historique](https://phishdestroy.github.io/TgWitness/fr/docs/reference/history/), [la recherche et l'analyse dans les archives](https://phishdestroy.github.io/TgWitness/fr/docs/reference/analysis/), [un MCP en lecture seule](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/), [l'OCR/transcription locale](https://phishdestroy.github.io/TgWitness/fr/docs/reference/media-analysis/) et [les webhooks sortants](https://phishdestroy.github.io/TgWitness/fr/docs/reference/webhooks/). Il s'agit de fonctionnalités issues du code source, ajoutées après la préversion portable 0.7.0. Les rapports analytiques et le texte reconnu restent séparés des événements capturés.

## Options supplémentaires

La configuration quotidienne se fait dans l'ordre suivant : compte → sources → observation. **La section « Extras »** est une destination distincte comprenant un bot Telegram Witness et un aperçu des captures sur GitHub. Chacune indique sa disponibilité et ses exigences avant d'afficher les paramètres. Sélectionner une fiche ouvre les instructions ; cela n'entraîne ni inscription ni démarrage d'un service.

La configuration du bot se déroule en trois étapes : créer un accès en lecture seule, choisir les paramètres de publication et lancer le bot sur l’hôte « witness ». Les options de réseau et de publication, les connexions existantes et les commandes de vérification sont communiquées à la demande. La configuration téléchargée est distincte d’un Witness en cours d’exécution. La désactivation des options supplémentaires conserve le brouillon ; les modifications de compte et le verrouillage effacent le jeton temporaire et le formulaire. Le guide intégré comprend des instructions de lancement. [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) lance un collecteur épinglé à partir de votre fork, capture une conversation et génère un transfert chiffré avec la provenance du workflow.

## Protocole et sources privées

**MTProto est le protocole de Telegram ; Telethon est la bibliothèque Python utilisée par TgWitness pour communiquer via MTProto.** Il ne s’agit pas de méthodes de connexion alternatives. La collecte utilise MTProto ; le « witness » (facultatif) publie des vérifications signées via l’API Bot.

Chaque espace de travail dispose de son propre client autorisé et de son propre flux de mise à jour de compte. TgWitness sélectionne les observations à partir des sources configurées et effectue des requêtes explicites distinctes pour des fonctions telles que les instantanés de l'historique et les téléchargements de fichiers multimédias.

Une source privée n’a pas besoin de nom d’utilisateur public. Le type de pair Telegram et l’identifiant numérique constituent les identifiants ; les titres et les noms d’utilisateur peuvent changer. L’accès dépend de l’ adhésion et des autorisations existantes. TgWitness n’ajoute pas automatiquement de sources et ne contourne pas la procédure d’approbation d’adhésion. Un hachage d’accès provenant d’un autre compte ne constitue pas un jeton d’accès universel.

Le modèle de collecte doit prendre en compte l’historique masqué antérieur à l’adhésion, les rôles des participants et des administrateurs, la révocation de sessions, la suppression ou la modification des autorisations, la migration d’un groupe vers un supergroupe, les sujets et forums, les discussions liées, les identités des chaînes et les pièces jointes indisponibles. Toutes les combinaisons n’ont pas encore été validées en conditions réelles.

La visibilité de la source est vérifiée au démarrage du collecteur. L’absence d’une source dans le résultat de la conversation délimitée signifie que **l’accès n’est pas confirmé**, et non qu’elle a été supprimée. Une source indisponible n’empêche pas l’observation des autres sources accessibles. Ne placez jamais de liens d’invitation ni de sessions réelles dans des fichiers publics.

## Comptes multiples

Le panneau prend en charge un nombre illimité d’**espaces de travail**, chacun disposant de ses propres :

- Autorisation, coffre-fort chiffré et chemin de connexion.
- Journal SQLite et identité de signature Ed25519.
- Sources sélectionnées, file d’attente des médias et paramètres de capture.
- État de surveillance, erreurs, points de contrôle et exportations.

Le changement d’espace de travail affiché n’interrompt pas le fonctionnement d’un autre collecteur. L’autorisation d’un compte en double entre différents espaces de travail est refusée. Un journal déjà lié à un compte Telegram ne peut pas être réattribué à un autre ; la reconnexion du même compte est autorisée. Cela permet de préserver l’identité du compte et la portée des identifiants de message concernés.

Il n’y a pas de nombre fixe ni de garantie de débit mesuré. Les espaces de travail partagent un processus Python et une boucle d’événements. La mise en place de « workers » distincts par compte reste à développer. Pour assurer l’isolation des processus, utilisez des installations, des ports et des répertoires de données distincts.

Attribuez à chaque compte les sources auxquelles il peut accéder. Différents comptes peuvent observer le même groupe, mais leurs observations restent distinctes et conservent leur origine. Deux comptes sur une même machine contrôlée par un opérateur ne constituent pas deux témoins indépendants. Les exportations s’effectuent par espace de travail ; il n’existe pas de dossier de dossier fusionné ni de chronologie Telegram globale.

## Capture et attribution

La section « Sources » propose des options par compte pour les nouveaux messages, les modifications, les suppressions, les réactions et l’appartenance à un groupe. Les préréglages permettent de conserver soit toutes les catégories, soit les messages, les modifications ou les suppressions. Cette politique s’applique aux groupes sélectionnés de l’espace de travail, est conservée après un redémarrage et est signée avec les modifications avant et après. Par défaut, toutes les catégories sont conservées. La désactivation d’une catégorie ne supprime pas les anciens enregistrements ; sa réactivation ne reconstitue pas les événements manqués. Les enregistrements opérationnels, les autres événements liés aux services de groupe et les instantanés explicites de l’historique sont distincts. Les objets Telegram capturés peuvent conserver leurs métadonnées intégrées, indépendamment des paramètres de mise à jour séparée. Il n’existe pas encore de remplacement de catégorie par groupe.

| Contenu | Capturé maintenant | Limites |
| --- | --- | --- |
| Message | Texte, identifiants de pair/message, métadonnées de l'expéditeur, réponses et enveloppe de mise à jour d'origine | Aucune signature Telegram vérifiable publiquement pour ce message |
| Modifier | Nouvelle version observée et toutes les versions précédemment enregistrées | Les modifications intermédiaires effectuées pendant les périodes d’indisponibilité peuvent être perdues ; l’expéditeur n’est pas nécessairement l’auteur de la modification. |
| Suppression | Notification et contenu précédemment capturé, le cas échéant | En général, aucune mention de l'auteur de la suppression ni d'heure précise de l'action |
| Suppression hors champ | Notification originale au niveau du compte, sans supposition quant à l’interlocuteur | La corrélation stricte avec les identifiants déjà enregistrés au niveau du compte fait l’objet de travaux futurs. |
| Réaction | Compteurs fournis et identités récentes visibles | La liste complète des réacteurs disponibles nécessite des requêtes distinctes ; les canaux peuvent masquer les identités |
| Adhésion | Messages de service et mises à jour transmises aux participants | La visibilité dépend du rôle et du type de discussion ; l’absence d’événements ne prouve pas l’absence |
| Actions de l'administrateur | Uniquement les mises à jour pertinentes | L'interrogation séparée du journal d'administration n'est pas mise en œuvre |
| Pièce jointe | Descripteur de la version d’origine, nombre d’octets téléchargés/SHA-256 et résultats des tentatives | Un fichier supprimé peut être irrécupérable ; la dernière version n'est pas remplacée. |
| Historique | Instantané explicite des messages actuellement visibles | Ne reconstitue pas l’intégralité des modifications ni du contenu supprimé |
| Processus de collecte | Démarrage/arrêt, signal de présence, erreurs, paramètres, périmètre et réception des programmes | Auto-déclaration, et non attestation indépendante du processus |

Une action n’est attribuée à une personne que si la source identifie effectivement cet acteur. Dans le cas contraire, l’interface signale l’absence d’attribution. Les noms d’utilisateur et les noms propres sont des attributs observés, et non la preuve d’une identité dans le monde réel.

## Capacité et limites de Telegram

Il n’existe pas de nombre universel de discussions pouvant être surveillées avec une qualité garantie. La capacité dépend du nombre maximal d’événements par seconde, du volume et de la taille des pièces jointes, des RPC supplémentaires, du nombre de comptes actifs, de la latence du disque et de l’espace libre, des conditions du réseau, des limites de Telegram, du délai acceptable et de la profondeur de la file d’attente.

Telegram fait la distinction entre la transmission passive et l’interrogation active par intervalles courts. Sa documentation de mise à jour décrit des appels `updates.getChannelDifference` supplémentaires pour les canaux ou supergroupes ouverts et recommande de ne pas dépasser **dix sources interrogées simultanément par intervalles courts**. Il ne s’agit pas d’une limite à dix groupes sélectionnés ni d’une garantie d’exhaustivité.

| Mode | Objectif | Statut |
| --- | --- | --- |
| Remarque générale | Enregistrez les mises à jour provenant de sources sélectionnées | Mis en œuvre |
| Observation prioritaire | Vérifications supplémentaires des différences pour un ensemble de sources délimité | Non implémenté en mode utilisateur |

Un sondage arbitraire à haute fréquence, ignorant FloodWait ou supposant une capacité linéaire provenant de comptes supplémentaires, ne constitue pas un modèle de dimensionnement valable. Les limites par défaut sont les 1 000 premières conversations répertoriées, jusqu’à 500 messages par instantané d’historique, 1 à 2 000 MiB par fichier collecté selon le type, et 4 GiB de contenu ZIP signé non compressé ; chaque valeur est modifiable par espace de travail dans **les paramètres**. Les exportations ne sont soumises à aucune limite fixe de nombre d’événements. Le mode de secours via le navigateur est limité à 128 MiB par défaut ; l’interface CLI de streaming dispose d’une limite de transfert configurable, fixée à 5 GiB par défaut.

`tools/check_capacity.py` mesure l’ingestion et l’exportation de données synthétiques au niveau local. Ses résultats ne constituent pas des mesures de livraison de Telegram ni un décompte garanti des conversations réelles. Consultez [le fichier VERIFICATION.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/) pour connaître la version mesurée et la charge de travail.

## Fiabilité et récupération

Les fonctionnalités implémentées comprennent : WAL SQLite et transactions synchrones ; écritures atomiques des messages et des tâches multimédias ; tâches persistantes et délais de réessai ; descripteurs de version d’origine ; des tentatives de réessai limitées ; la persistance de FloodWait pour les médias ; les téléchargements de médias en dehors de l’ attente réseau de l’événement texte ; les exportations à préfixe stable pendant que les écritures ultérieures se poursuivent ; les paramètres et les enregistrements d’audit atomiques ; la préservation de l’autorisation de travail après un échec de connexion de remplacement ; l’isolation d’un espace de travail supplémentaire endommagé ; des tentatives de reconnexion explicites ; des rapports distincts sur la perte d’autorisation ; et la détection des changements de l’horloge réelle à l’aide d’une horloge monotone.

Les points pts/qts/seq des comptes et des chaînes sont enregistrés et rétablis après un redémarrage, et les discussions surveillées sont revérifiées périodiquement ; voir [le format des preuves](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#durable-collection-and-process-receipts-02). L'enregistrement périodique de la position ne constitue pas une confirmation atomique et sans perte de l'acceptation du journal.

Chaque démarrage du processus enregistre l’emplacement de tête précédent et la limite hors ligne. L’historique actuel n’est pas considéré comme une réparation des lacunes. La capacité de conservation des différences de Telegram est limitée ; `differenceTooLong` ne peut pas reconstituer l’intégralité du contenu disparu. Les lacunes irrécupérables doivent rester explicitement signalées, même si un instantané ultérieur de l’historique aboutit.

## Modèle de preuve

Chaque événement enregistre une séquence, l’heure d’observation locale (UTC), l’heure de la source lorsqu’elle est fournie, le type, la source, l’acteur lorsqu’il est fourni, la charge utile d’origine, le hachage précédent et la signature. Les observations de messages conservent également le compte du collecteur et le contexte d’exécution.

Le relevé de processus signé contient un identifiant d’exécution aléatoire ; les versions de TgWitness/Python/OS/dépendances ; les valeurs SHA-256 des fichiers source et l’empreinte agrégée ; le compte initial, la portée et les paramètres ; les relevés UTC/monotones ; ainsi que l’en-tête du journal précédent. Les modifications de paramètres, les démarrages/arrêts et les erreurs sont consignés dans ce même journal. Des points de contrôle sont conservés au démarrage, toutes les cinq minutes pendant l’observation (durée modifiable) et lors d’un arrêt ordonné. Un point de contrôle local conservé permet de détecter une restauration vers un préfixe de journal antérieur.

| Mécanisme | Ce qu’il établit |
| --- | --- |
| Hachage SHA-256 du fichier | Les octets correspondent à un résumé connu |
| Chaîne de hachages des événements | Classement et mise en relation des enregistrements par rapport à une limite connue |
| Ed25519 | Signature sous une clé spécifique |
| Point de contrôle conservé de manière indépendante | Les éléments suivants respectent les limites fixées. |
| Analyse de la taille du fichier exécutable | Rapport d’auto-évaluation du collecteur concernant les fichiers mesurés |
| Réponse indépendante et valide de la TSA | Existence d’octets particuliers à l’instant TSA sous des hypothèses de confiance explicites |

La préparation des requêtes selon la norme RFC 3161 et la vérification des réponses via OpenSSL sont implémentées. L'envoi automatique ne l'est pas. Une requête ou une signature locale portant l'heure de la machine ne constitue pas un horodatage indépendant. Voir [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/timestamp/).

Un opérateur contrôlant le collecteur et la clé de signature peut fabriquer de nouvelles observations signées. Les signatures n’établissent pas l’origine Telegram, la véracité ni l’ admissibilité juridique automatique. Une conservation plus rigoureuse nécessite un point de contrôle indépendant et un stockage chronologique, des contrôles d’accès aux clés, des registres de transfert et une vérification par un logiciel de confiance.

## Exportation, déploiement et transfert

Un fichier ZIP signé contient les fichiers JSONL, CSV et HTML d’origine, les pièces jointes conservées, les hachages, un manifeste signé et un vérificateur pratique. Il couvre un espace de travail et un préfixe fixe pour l’intégralité du journal. Les filtres de recherche du panneau ne suppriment pas les enregistrements de manière silencieuse. Les clés secrètes, les jetons et les sessions Telegram sont exclus ; les observations d’origine peuvent toutefois contenir des informations personnelles et des métadonnées Telegram.

Conservez séparément le résumé ZIP, l’empreinte de confiance, le point de contrôle, l’accusé de réception du processus et le transfert. Utilisez un vérificateur issu d’une installation de confiance, plutôt que de vous fier au code exécutable uniquement parce qu’il figure dans le fichier ZIP examiné.

L’interface navigateur s’installe localement sans Node.js, sans CDN ni polices externes. Un seul jeton d’opérateur permet de contrôler l’installation. L’accès à distance nécessite le protocole HTTPS ou un tunnel SSH. Des définitions natives en Python et pour les conteneurs sont fournies, avec des exemples de services dans le répertoire [« deploy/ »](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) ; les vérifications de plate-forme effectuées sont répertoriées séparément.

L'espace de travail par défaut utilise la racine de données ; les espaces de travail supplémentaires utilisent `profiles/<id>/`. La sauvegarde nécessite l'arrêt du processus et l'ensemble complet des données et des clés. Les fichiers ZIP de preuves ne constituent pas des sauvegardes de l'application. Les secrets peuvent utiliser une clé principale externe pour un nouveau répertoire de données ; le chiffrement du journal et des médias est assuré par le disque ou le volume de l'opérateur. Voir [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/) et [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/operations/).

## Critères de publication d’une version stable

Avant la sortie d’une version stable, veuillez préciser :

1. Véritables groupes privés, supergroupes, forums et canaux avec des rôles de membre/administrateur et un historique masqué/visible, y compris les identifiants de connexion/authentification à deux facteurs (2FA), les révocations et les pertes d'accès.
2. Contrôle des modifications, des suppressions, des réactions, des adhésions et des médias par rapport aux actions connues.
3. Pannes de processus ou de serveur, pannes de disque ou disque plein, références de fichiers périmées, FloodWait, perte de connexion réseau, fichiers corrompus et restauration de la base de données.
4. Utilisation prolongée de plusieurs comptes avec un temps de latence mesuré, des files d’attente, de la mémoire et de l’espace disque, y compris des sources silencieuses et bruyantes combinées.
5. Interruption entre le passage à l’état suivant dans MTProto et l’acceptation du journal.
6. Installation propre sur la matrice système d'exploitation/conteneur prévue et restauration de sauvegarde vérifiée.
7. Analyse indépendante des aspects liés à la sécurité, aux signatures et aux allégations d’attribution/de preuve.

L'interrogation des journaux d'administration, les listes de réacteurs supplémentaires, l'interrogation prioritaire, les workers distincts et le chiffrement à l'échelle de l'application restent des travaux à venir. L'accès aux panneaux avec périmètre défini est décrit dans [la section « Accès et autorisations](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) ». La version 0.6 prend en charge le TData à compte unique délimité et l'importation de fichiers de compte décrits dans [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/). Veuillez consulter les conditions d’utilisation de l’API Telegram avant publication. Les références de recherche et les conclusions relatives à la plateforme figurent dans [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md).
