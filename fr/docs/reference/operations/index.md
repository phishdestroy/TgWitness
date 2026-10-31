# Workflows et opérations

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/operations/

Fonctionnement quotidien du panneau : modes, catégories de surveillance, paramètres, notifications, exportations, sauvegarde et capacité.

Pour votre première connexion, utilisez [les comptes et les formats de session](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/). Pour obtenir des explications sur les versions enregistrées, les règles relatives aux événements et les lacunes, consultez la section « [Comment fonctionne la collecte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/) ». Ce guide traite du fonctionnement quotidien et de la restauration des données.

## Processus de travail de l'opérateur

Organigramme · Choisissez le mode de stockage et la protection des clés → Ouvrez le panneau à l'aide de son jeton; Ouvrez le panneau à l'aide de son jeton → Sélectionnez un espace de travail; Sélectionnez un espace de travail → Configurer un acheminement direct ou via un proxy; Configurer un acheminement direct ou via un proxy → Saisissez un numéro de téléphone ou sélectionnez des fichiers / QR; Saisissez un numéro de téléphone ou sélectionnez des fichiers / QR → Vérifiez l’identité du compte et sélectionnez les groupes accessibles; Vérifiez l’identité du compte et sélectionnez les groupes accessibles → Enregistrez les règles relatives aux événements et aux pièces jointes, puis lancez la surveillance; Enregistrez les règles relatives aux événements et aux pièces jointes, puis lancez la surveillance → Surveillez les erreurs, les accès, les files d'attente et l'espace disque; Surveillez les erreurs, les accès, les files d'attente et l'espace disque → Conserver des points de contrôle indépendants; Conserver des points de contrôle indépendants → Exporter et vérifier les données · Choisissez le mode destockage et laprotection des clés · Ouvrez le panneau àl'aide de son jeton · Sélectionnez un espacede travail · Configurer unacheminement direct ouvia un proxy · Saisissez un numéro detéléphone ousélectionnez desfichiers / QR · Vérifiez l’identité ducompte et sélectionnezles groupesaccessibles · Enregistrez les règlesrelatives auxévénements et auxpièces jointes, puislancez la surveillance · Surveillez leserreurs, les accès,les files d'attente etl'espace disque · Conserver des pointsde contrôleindépendants · Exporter et vérifierles données

**Schéma sous forme de texte**

1. Choisissez le mode de stockage et la protection des clés → Ouvrez le panneau à l'aide de son jeton
2. Ouvrez le panneau à l'aide de son jeton → Sélectionnez un espace de travail
3. Sélectionnez un espace de travail → Configurer un acheminement direct ou via un proxy
4. Configurer un acheminement direct ou via un proxy → Saisissez un numéro de téléphone ou sélectionnez des fichiers / QR
5. Saisissez un numéro de téléphone ou sélectionnez des fichiers / QR → Vérifiez l’identité du compte et sélectionnez les groupes accessibles
6. Vérifiez l’identité du compte et sélectionnez les groupes accessibles → Enregistrez les règles relatives aux événements et aux pièces jointes, puis lancez la surveillance
7. Enregistrez les règles relatives aux événements et aux pièces jointes, puis lancez la surveillance → Surveillez les erreurs, les accès, les files d'attente et l'espace disque
8. Surveillez les erreurs, les accès, les files d'attente et l'espace disque → Conserver des points de contrôle indépendants
9. Conserver des points de contrôle indépendants → Exporter et vérifier les données

L’autorisation, la connectivité de transport, l’accès à un groupe et l’intégralité de la transmission sont des propriétés distinctes. Un statut de connexion vert n’implique pas que tous les événements aient été capturés.

## Partager votre travail sans divulguer la clé principale

**Accès** ouvert permettant d’attribuer un jeton à un réviseur ou à un analyste. Choisissez les comptes et les discussions qu’ils peuvent ouvrir, puis autorisez la consultation, l’exportation ou les actions opérationnelles. Un opérateur qui lance ou arrête la collecte a besoin d’un accès à l’ensemble de l’espace de travail ; un examinateur peut être limité à une seule conversation. Les limites de session, la durée de validité et les règles relatives aux adresses IP sont distinctes de l’autorisation du compte Telegram. Voir « [Accès et autorisations](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) ».

Utilisez « **Sessions ouvertes »** pour mettre fin à une connexion ou « Révoquer l’accès » pour mettre fin à toutes ses sessions. La console d’administration regroupe l’activité des processus en cours sur l’ensemble des espaces de travail. La fermeture d’une session ne met pas fin à la collecte.

## Modes d'exécution

| Mode | Action | Comportement |
| --- | --- | --- |
| Démonstration | scripts\Demo.cmd ou `--demo` | Données synthétiques ; connexions aux comptes réels désactivées |
| Remarque | Commencer l'observation | Enregistrez les mises à jour fournies pour les sources sélectionnées |
| Aperçu historique | Sources → instantané de l'historique | Jusqu’à 500 messages récents ; aucune reconstitution de l’ensemble des modifications passées |
| Pause | Observation en pause | Interrompre la collecte tout en conservant les données et les tâches en attente |
| Révision/transfert | Exportations | ZIP, JSONL/CSV/HTML, point de contrôle, accusé de réception du processus et demande d’horodatage |
| Comptes multiples | Espaces de travail ou bouton « **+** » situé en haut de la page | Un nombre illimité d’espaces de travail distincts au sein d’un même processus |

L'accès à la démo locale s'ouvre automatiquement sans saisie manuelle de jeton. Il utilise une capacité valable pendant la durée de vie du processus, réservée exclusivement à l'accès direct en boucle fermée à une démo synthétique isolée ; le jeton du panneau principal n'est pas divulgué. Les espaces de travail réels et l'accès à la démo à distance ou via un proxy nécessitent une authentification par jeton. L'accès à la démo ne confère aucune autorisation sur Telegram.

## Catégories de surveillance

![Paramètres de surveillance par compte avec des données sources synthétiques](https://phishdestroy.github.io/TgWitness/assets/sources.png)

Dans **Sources → Paramètres de capture → Choisir les modifications à conserver**, sélectionnez indépendamment les nouveaux messages, les modifications, les notifications de suppression, les mises à jour des réactions et les événements liés à l’adhésion. Le réglage par défaut conserve toutes les catégories. L’option « **Messages, modifications et suppressions »** conserve le contexte d’origine tout en désactivant les mises à jour distinctes concernant les réactions et les membres. L’option « **Toutes les activités visibles »** restaure les cinq catégories. Les préréglages modifient le format ; cliquez sur « **Enregistrer les paramètres de surveillance »** pour les appliquer.

La politique enregistrée s’applique à toutes les sources sélectionnées dans cet espace de travail. Les autres espaces de travail conservent leurs propres paramètres. Chaque modification effective enregistre les valeurs « avant » et « après » signées ; la politique en vigueur est également incluse dans les accusés de réception de processus et les enregistrements de début d’observation. La désactivation d’une catégorie ne supprime pas les observations antérieures. La réactivation ne permet pas de récupérer les modifications manquées. Il n’existe pas de dérogation par groupe de catégories dans cette version.

Veillez à ce que l’enregistrement des nouveaux messages reste activé lorsque le contenu antérieur est important : une notification de suppression ne permet pas de récupérer du texte qui n’a jamais été capturé. Les enregistrements opérationnels/de couverture et autres événements liés au service de groupe sont toujours conservés. Les instantanés explicites de l’historique sont distincts de la sélection de catégories en temps réel et peuvent inclure des messages de service. Ces options ne masquent pas les métadonnées relatives aux réactions ou aux membres intégrées dans un objet Telegram par ailleurs capturé.

Un instantané de l'historique peut mettre des pièces jointes en file d'attente lorsqu'il est en pause. Lancez l'observation pour les traiter. Le fait qu'elles soient en file d'attente ne signifie pas qu'elles ont été téléchargées. Un fichier original indisponible n'est pas remplacé par une version modifiée plus récente ; les résultats sont enregistrés séparément.

**La fonction « Verrouiller »** efface l’accès au navigateur et les champs secrets, mais laisse la collecte en cours. La fermeture d’un onglet laisse également le processus en cours d’exécution. L’arrêt du processus Python ou du service interrompt la collecte, quel que soit l’état du navigateur.

La suppression d’un espace de travail supplémentaire arrête son collecteur et supprime ses données locales. Si un fichier verrouillé ou une erreur du système de fichiers interrompt la suppression, le panneau signale l’échec et maintient l’espace de travail dans la liste des espaces indisponibles (`DeletionPending`). Fermez les programmes ouvrant ses fichiers et réessayez **la suppression**. Le redémarrage de TgWitness laisse cet espace de travail à l’arrêt et ne recrée pas son journal ou ses clés partiellement supprimés. Une suppression réussie n’est enregistrée qu’une fois le répertoire supprimé ; les copies exportées ou sauvegardées séparément restent soumises à leur propre politique de conservation.

## Notifications

**Sources** ouvertes **→ Notifications → Alertes et résumé quotidien**. TgWitness utilise Apprise pour envoyer des alertes vers Matrix, Telegram, Discord, Slack, ntfy, par e-mail et vers d’autres services pris en charge. Vous pouvez ajouter plusieurs destinations à un même espace de travail.

1. Saisissez une URL de destination Apprise par ligne. Utilisez le [catalogue de services et les formats d'URL](https://appriseit.com/services/) adaptés à votre service.
2. Activez l’option « **Envoyer des notifications** », puis sélectionnez les alertes de problèmes, les modifications dans les discussions surveillées et un résumé quotidien. L’heure indiquée dans le résumé correspond à l’heure du serveur.
3. Cochez la case « **Inclure de courts extraits »** si vous souhaitez que le texte des messages supprimés et modifiés soit conservé dans les alertes.
4. Cliquez sur « **Enregistrer les notifications »**, puis sur « **Envoyer un test »** pour vérifier la bonne réception.

Pour votre propre destinataire, utilisez [le webhook JSON](https://appriseit.com/services/json/) d’Apprise. Par exemple, `jsons://notify.example.org/tgwitness` envoie des données JSON via HTTPS vers ce point de terminaison. Il s’agit d’un exemple fictif ; remplacez-le par votre propre destination.

Les destinations et les paramètres relèvent de l'espace de travail sélectionné. Les notifications de modification couvrent les sources surveillées, y compris les discussions récemment ajoutées. La cloche située dans la barre supérieure répertorie également les problèmes récents et les modifications apportées aux discussions.

Dans la démo, les commandes de notification sont visibles mais l’envoi est désactivé. Configurez la transmission dans un espace de travail réel. Les notifications utilisent la route Direct, SOCKS5 ou HTTP de cet espace de travail ; MTProxy ne peut pas les acheminer. Les destinations non-HTTP telles que SMTP nécessitent une route directe.

## Mise en page des panneaux

![Espace de travail de connexion utilisant des données synthétiques](https://phishdestroy.github.io/TgWitness/assets/connection.png)

**Le journal** présente les observations, les recherches et les filtres. Une modification permet d’afficher les versions capturées ; une suppression permet d’afficher le contenu antérieur, s’il est disponible. Les sources inconnues restent explicitement indiquées. Les chiffres sont disponibles dans **la rubrique « Aperçu »** ; les détails relatifs à l’acquisition figurent dans le guide local.

Ouvrez un message modifié pour comparer ses versions avec **Différences dans le texte** ou **Côte à côte** ; **Données brutes** affiche les champs enregistrés. Les modifications apportées aux liens masqués et aux boutons de bot apparaissent séparément. Ouvrez l'aperçu d'une pièce jointe pour inspecter les images, l'audio ou la vidéo enregistrés ; le bouton de téléchargement permet de récupérer l'original préservé.

**Live** met à jour le journal et les discussions au fur et à mesure que les enregistrements arrivent. Mettez-le en pause pendant la vérification, ou utilisez le bouton des nouveaux événements lorsque vous êtes prêt ; la collecte continue de fonctionner. **Ctrl/Cmd+K** trouve les actions du panneau et effectue des recherches dans le journal.

**La section « Sources »** contient le périmètre d’observation (discussions sélectionnées, un dossier Telegram ou l’ensemble du compte), les discussions accessibles de tous types, les sources sélectionnées avec des étoiles de priorité, les paramètres relatifs aux pièces jointes et aux vérifications, ainsi que les instantanés de l’historique. Les sources privées sont sélectionnées par boîte de dialogue/identifiant sans lien public. Le statut d’accès décrit la dernière vérification effectuée, et non des autorisations permanentes.

Filtrez les sources, cochez leurs cases, puis activez-les, mettez-les en pause ou marquez-les comme prioritaires simultanément. Dans la liste des discussions disponibles, **Ajouter la sélection** utilise votre sélection ; **Ajouter tous les résultats** utilise la recherche et le filtre de type actuels.

**« Chats → Personnes »** répertorie toutes les personnes dont les messages ont été enregistrés ; lorsque les profils des participants sont activés pour la conversation, un clic ouvre le profil de cette personne avec des liens vers les entrées du journal.

**Witness** crée des jetons de témoin en lecture seule, indique la date de la dernière vérification de chaque témoin et fournit les commandes et options permettant d’exécuter un [témoin (indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/)).

**La section « Paramètres »** regroupe toutes les limites et tous les rythmes de l’espace de travail qui ne figurent pas sur une autre page : le nombre de dialogues lus, la fréquence de relecture de la liste des discussions, les intervalles entre les signaux de vie et les points de contrôle, la mémoire tampon de démarrage, la manière dont les vérifications répétées répartissent leurs requêtes (premier délai, nombre de discussions par passage, pause entre les discussions, messages récupérés et redemandés), l’espace disque réservé, les délais d’expiration et les nouvelles tentatives de téléchargement, les critères de recherche des profils d’utilisateurs (y compris vos propres expressions régulières), la taille et la fréquence des notifications, les limites relatives aux instantanés, aux fichiers ZIP et aux téléchargements via le navigateur, ainsi que les délais d’expiration et les nouvelles tentatives du client Telegram. Chaque champ affiche sa plage de valeurs et sa valeur par défaut ; les champs modifiés sont signalés et peuvent être restaurés un par un ou tous ensemble. Chaque modification est enregistrée sous la référence « `parameters.changed` » avec les valeurs avant et après, et les enregistrements de début d’observation indiquent les valeurs en vigueur. Les valeurs s’appliquent dès leur prochaine utilisation ; les délais d’expiration et les tentatives de réessai du client s’appliquent dès la prochaine connexion. Les intervalles de vérification, les types et tailles de pièces jointes, ainsi que les intervalles de sauvegarde et de copie hors site restent sur leurs propres pages et peuvent prendre n’importe quelle valeur comprise dans leur plage, et pas seulement les valeurs prédéfinies.

La cloche située dans la barre supérieure répertorie les problèmes et modifications récents dans les discussions surveillées ; les messages non lus sont comptabilisés jusqu’à ce qu’ils soient marqués comme lus. Les modifications sont regroupées par discussion et par heure (« 12 supprimés, 1 modifié, 0 introuvable »), et les problèmes tels qu’une déconnexion ou un disque plein restent dans la liste quelle que soit l’activité des discussions.

**La création du compte** commence par le champ « Numéro de téléphone ». **La suite** mène directement à la saisie du code, les identifiants API n’étant demandés que s’ils sont manquants. Le QR et l’importation de fichiers constituent des onglets alternatifs. Les identifiants API enregistrés ne sont réutilisés qu’au sein de leur propre espace de travail. L’écran de saisie ne comporte ni barre latérale, ni statistiques, ni paragraphes de configuration. L’icône **« Paramètres »** ouvre les contrôles relatifs à l’API, au proxy, au stockage et aux comptes supplémentaires. Les nouvelles installations commencent ici ; les comptes connectés sans source sélectionnée commencent par « **Choisir les discussions** ». La modification de la configuration nécessite une observation en pause et annule toute connexion inachevée. Un journal existant ne peut pas être réassocié en arrière-plan à un autre compte Telegram.

**L’exportation** vérifie l’intégrité du journal et génère des fichiers portables. L’identifiant de son espace de travail peut être transmis à l’interface de ligne de commande (CLI) de téléchargement. Chaque exportation attribue un préfixe au journal complet ; les événements ultérieurs sont intégrés à une exportation suivante. Les filtres de recherche ne modifient pas la portée du paquet. Vous trouverez des informations détaillées sur la signature et la couverture dans la section « **Vérification et limitations** ».

Le panneau indique l’état du collecteur, les médias en file d’attente ou ayant échoué, les médias en attente les plus anciens, l’espace disque disponible, les pauses de requêtes et les sources dont l’accès n’est pas confirmé sous **la rubrique « État du collecteur**». Ces détails sont initialement masqués et cachés sous l’onglet « Compte ». Une fiche de configuration présente l’étape suivante : connecter un compte, choisir des sources ou démarrer la surveillance. La liste des comptes correspond à un instantané au moment du chargement ; l’espace de travail sélectionné s’actualise périodiquement. Il ne s’agit pas d’un outil de surveillance SLA multiprocessus.

L’interface utilisateur utilise des ressources locales et un rendu de texte adapté au contenu source. Les mises en page pour ordinateur de bureau et les mises en page étroites basées sur Chromium ont été testées. Il ne s’agit pas d’une certification d’accessibilité complète ; l’évaluation de l’ergonomie par les lecteurs d’écran et par des utilisateurs humains reste un travail distinct.

## Environnements de déploiement

| Environnement | Installation | Statut de vérification |
| --- | --- | --- |
| PC/serveur Windows | Python 3.11+, scripts\Setup.cmd/Start.cmd, répertoire de données privées | Testé localement sous Windows/Python 3.12 |
| Serveur Linux/VPS | Environnement Python (venv), utilisateur dédié au service, HTTPS/SSH | Exemples de code, de CI et de systemd fournis ; non exécutés sur cet hôte |
| macOS | Environnement Python (venv), processus au premier plan ou agent utilisateur | Exemple « launchd » fourni ; vérification séparée de l'installation requise |
| Docker/Compose | Volume persistant, un seul nœud de travail | Définition et vérification de l'exécution de la CI fournies ; Docker indisponible localement |
| Navigateur mobile | Connectez-vous au panneau sécurisé sur un serveur en service | Mise en page Chromium étroite testée ; le collecteur ne fonctionne pas sous iOS/Android |

La portabilité signifie qu’aucun service cloud ni aucune interface utilisateur ne sont obligatoires. Chaque cible doit toutefois disposer des dépendances Python/crypto compatibles, ainsi que d’un accès au disque local et au réseau. Consultez [le fichier DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/deployment/) et [les modèles de service](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md).

Les espaces de travail partagent le processeur, la mémoire et une boucle d’événements. Pour isoler les processus, utilisez des instances, des ports, des répertoires de données et des autorisations de compte distincts. Il n’existe pas de panneau de contrôle unifié entre les différentes instances. Ne faites jamais accéder plusieurs workers à une même base de données.

## Vérifications et exportations au démarrage

Exécutez la commande `python start.py --check` avant de démarrer un environnement préparé. Ajoutez `--json` pour des vérifications lisibles par machine ou transmettez les paramètres `--data-dir`, `--host` et `--port` souhaités. Cette commande vérifie les prérequis sans connexion à Telegram ni création de journal. Elle ne vérifie pas le journal ni ne confirme que la capture est prête ; la vérification du journal s’effectue lors du démarrage de l’application. Un port occupé peut simplement correspondre à une instance existante.

Les navigateurs prenant en charge l’API d’accès au système de fichiers enregistrent les exportations via un flux inscriptible. Les autres navigateurs ne mettent en mémoire tampon que 128 MiB au maximum. Utilisez l’interface de ligne de commande (CLI) de streaming pour les exportations plus volumineuses ou les navigateurs ne prenant pas en charge le streaming de fichiers :

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Ajoutez « `--profile ID` » à partir de la section « Exports » pour un espace de travail enfant. Utilisez « `--url https://server` » pour l’accès à distance. Le protocole HTTP simple n’est accepté que pour les destinations en boucle locale. Le jeton est lu à partir d’un fichier et envoyé dans un en-tête ; il n’est ni affiché ni intégré à une URL. Les redirections sont refusées. Les destinations existantes ne sont pas écrasées. Les transferts ayant échoué suppriment leur fichier partiel temporaire. Le SHA-256 signalé est une somme de contrôle du transfert ; vérifiez le fichier ZIP signé séparément à l’aide d’une empreinte digitale ou d’un point de contrôle fiable.

## Sauvegarde, restauration et interruptions

1. Mettez l'observation en pause et arrêtez le processus de manière propre.
2. Copiez l'intégralité du répertoire de données : bases de données, fichiers WAL/SHM s'ils sont présents, fichiers multimédias, `credentials.enc`, `signing.enc`, `network.enc`, clés/métadonnées du coffre-fort, jeton, points de contrôle et tous les répertoires `profiles/`.
3. En mode « clé externe », conservez séparément la clé principale et conservez chaque `vault.external.json`. La génération d’une nouvelle clé ne permet pas de récupérer les anciens secrets.
4. Effectuez la restauration alors que la destination est à l'arrêt ; configurez la clé d'origine, restreignez l'accès et vérifiez l'intégrité avant de reprendre le processus.
5. Consignez les périodes d’indisponibilité et les résultats des vérifications. Un instantané de l’historique ne permet pas de prouver qu’ aucune suppression n’a eu lieu pendant l’interruption.

Les fichiers ZIP de preuves excluent les sessions et les clés privées et ne constituent pas des sauvegardes complètes du service. Quatre éléments sont protégés de manière différente :

| Qu'est-ce que | Protection |
| --- | --- |
| Exporter des fichiers sans mot de passe (par défaut) | Non chiffré. Signé, ce qui permet de détecter les modifications, mais toute personne en possession du fichier peut le lire. |
| Exporter des fichiers avec un mot de passe | Si vous définissez un mot de passe, le fichier exporté final est enregistré tel quel dans un fichier ZIP WinZip chiffré en AES-256, compatible avec 7-Zip et WinRAR ; le mot de passe n’est pas stocké ([traitement des preuves](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/)). |
| La base de données du journal et les pièces jointes enregistrées sur le disque | Non chiffré par TgWitness ; veuillez utiliser un disque ou un volume chiffré |
| Sessions Telegram et clés de signature | Chiffré dans le répertoire de données (`credentials.enc`, `signing.enc`, `network.enc`) |

Une sauvegarde complète correspond au répertoire de données figées décrit ci-dessus, et non à une exportation. Utilisez un stockage sécurisé et un mécanisme de transfert dédié pour les deux. Les exportations temporaires vers le serveur sont stockées dans le répertoire « `temporary-exports/` » de chaque espace de travail ; les réponses finalisées sont supprimées, et les fichiers d’exportation interrompus sont supprimés au prochain démarrage, tant que le verrouillage de l’instance de cet espace de travail est maintenu.

Le rétablissement d’une connexion ne garantit pas la récupération des modifications intermédiaires. Les tâches multimédias persistantes et la position de mise à jour de Telegram sont conservées après un redémarrage ; voir [le format des preuves](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#durable-collection-and-process-receipts-02).

## Capacité et durée de conservation

Limites par défaut, toutes modifiables sous **« Paramètres** » : les 1 000 premières conversations, 500 messages par instantané, 4 Gio de contenu ZIP signé non compressé (les archives plus volumineuses nécessitent `verify.py --max-gib N`) et une solution de secours de 128 Mio pour le navigateur. Les pièces jointes occupent entre 1 et 2 000 MiB par type sous **Sources → Pièces jointes**. L’interface de ligne de commande (CLI) de téléchargement est configurée par défaut pour un transfert de 5 GiB. L’espace disque disponible peut constituer une limite inférieure. Réservez de l’espace pour les journaux, les médias, le WAL, les exportations temporaires et les sauvegardes. Les exportations utilisent le volume de données plutôt que la valeur de 512 Mio « `/tmp` » de Compose.

Mesurez le nombre d’événements par seconde, l’ancienneté de la file d’attente, le nombre d’octets de médias et la latence du disque plutôt que de compter uniquement les groupes. Les benchmarks locaux synthétiques ne garantissent pas la livraison des messages Telegram. Il n’y a pas de suppression automatique des données conservées. La suppression de la fin d’un journal invalide son lien avec les points de contrôle conservés.

Des vérifications prioritaires existent déjà : les sources marquées d’une étoile sont revérifiées toutes les 15 minutes par défaut, les autres toutes les 6 heures (voir [les niveaux de vérification](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/#recheck-tiers)). Des exportations protégées par mot de passe sont disponibles comme décrit ci-dessus. L’acceptation en temps réel de Telegram/proxy, la relecture durable, le journal d’administration et l’interrogation des réactions, les workers isolés, le chiffrement du journal local et des médias par TgWitness lui-même, ainsi que l’examen indépendant, restent des travaux distincts. L’accès restreint est documenté dans [la section « Accès et autorisations](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) ». Voir [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md), [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) et [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/).
