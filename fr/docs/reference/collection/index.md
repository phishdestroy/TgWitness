# Fonctionnement de la collecte

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/

Champ d’observation, mises à jour en temps réel, vérifications croisées, pièces jointes, actions effectuées et signification d’une lacune, message par message.

TgWitness enregistre ce qu’un compte Telegram connecté observe. Le journal conserve ces observations, leur séquence et le contexte qui les accompagne. Il ne déduit pas d’actions invisibles à partir d’un message manquant ou du fait qu’un compte soit connecté.

## De la connexion au journal

Organigramme · Autoriser un compte utilisateur → Sélectionnez les groupes et canaux accessibles; Sélectionnez les groupes et canaux accessibles → Enregistrer les paramètres relatifs aux événements et aux pièces jointes; Enregistrer les paramètres relatifs aux événements et aux pièces jointes → Commencer l'observation; Commencer l'observation → Recevez les mises à jour du client actif; Recevez les mises à jour du client actif → Appliquer la politique relative aux sources et aux événements; Appliquer la politique relative aux sources et aux événements → Ajouter une observation signée; Ajouter une observation signée → Consultez ou exportez le journal; Ajouter une observation signée → Traiter toute pièce jointe en attente; Traiter toute pièce jointe en attente → Ajoutez le résultat du téléchargement · Autoriser un compteutilisateur · Sélectionnez lesgroupes et canauxaccessibles · Enregistrer lesparamètres relatifsaux événements et auxpièces jointes · Commencerl'observation · Recevez les mises àjour du client actif · Appliquer la politiquerelative aux sourceset aux événements · Ajouter uneobservation signée · Consultez ou exportezle journal · Traiter toute piècejointe en attente · Ajoutez le résultat dutéléchargement

**Schéma sous forme de texte**

1. Autoriser un compte utilisateur → Sélectionnez les groupes et canaux accessibles
2. Sélectionnez les groupes et canaux accessibles → Enregistrer les paramètres relatifs aux événements et aux pièces jointes
3. Enregistrer les paramètres relatifs aux événements et aux pièces jointes → Commencer l'observation
4. Commencer l'observation → Recevez les mises à jour du client actif
5. Recevez les mises à jour du client actif → Appliquer la politique relative aux sources et aux événements
6. Appliquer la politique relative aux sources et aux événements → Ajouter une observation signée
7. Ajouter une observation signée → Consultez ou exportez le journal
8. Ajouter une observation signée → Traiter toute pièce jointe en attente
9. Traiter toute pièce jointe en attente → Ajoutez le résultat du téléchargement

L’autorisation, l’accès à une source, le bon fonctionnement d’un collecteur et la transmission complète sont des questions distinctes. Une connexion réussie ne garantit pas l’accès à tous les groupes. Un transport connecté ne prouve pas que toutes les mises à jour pertinentes sont bien parvenues.

## Périmètre d’observation : discussions sélectionnées, un dossier ou l’intégralité du compte

Sources → **Le périmètre d’observation** détermine les discussions qu’un espace de travail enregistre.

| Mode | Enregistre | Nouvelles conversations |
| --- | --- | --- |
| Discussions sélectionnées (par défaut) | Uniquement les discussions que vous ajoutez manuellement | Jamais ajouté automatiquement |
| Dossier Telegram | Conversations contenues dans l’un des dossiers du compte : conversations incluses par nom, auxquelles s’ajoutent les catégories du dossier (contacts, non-contacts, groupes, chaînes, bots), moins les conversations exclues et, si le dossier le précise, les conversations archivées | Les conversations correspondantes sont ajoutées dès qu’elles deviennent actives ; celles que vous ajoutez au dossier dans Telegram sont récupérées dans l’heure qui suit. |
| Compte complet | Toutes les conversations auxquelles le compte a accès | Chaque nouvelle conversation, groupe, conversation privée ou bot est ajouté dès la réception de sa première mise à jour. |

- **Les types de sources** (chaînes, groupes, discussions privées, bots) permettent de restreindre les modes « dossier » et « compte entier ». Les discussions sélectionnées peuvent être de n’importe quel type, y compris les discussions privées et les bots.
- **Les discussions exclues** ne sont jamais enregistrées, quel que soit le mode utilisé. En mode « dossier » et en mode « compte entier », les actions *« Exclure »* et *« Supprimer »* sur une source l’ajoutent à cette liste, de sorte que le périmètre ne l’ajoute pas à nouveau. Si vous sélectionnez à nouveau la conversation manuellement (dans « Sources » ou à partir de « Conversations »), celle-ci est retirée de la liste. La liste peut contenir jusqu’à 5 000 conversations ; au-delà, *la commande « Supprimer »* est refusée et la conversation peut être mise en pause à la place.
- **Actions propres à l’outil** (activées par défaut) : les messages envoyés par ce compte, ses modifications et les appuis sur les touches du clavier de réponse. Lorsque cette fonction est désactivée, les messages sortants et les modifications sont ignorés.
- Le passage à un dossier ou à l’ensemble du compte nécessite une confirmation : ces modes enregistrent les discussions privées et les messages de tiers et ne doivent être utilisés que sur un compte dédié. La confirmation et chaque modification de périmètre font l’objet d’enregistrements signés au format `scope.changed`.
- Les discussions ajoutées par le filtre apparaissent comme des sources marquées *« auto »*, enregistrées sous la forme `scope.applied` (au démarrage et toutes les heures) ou `source.discovered` (une nouvelle discussion pendant la surveillance). Le retour aux discussions sélectionnées met en pause toutes les sources ajoutées automatiquement.

Ce que ces modes ne permettent pas de faire :

- **Les discussions secrètes** sont chiffrées de bout en bout entre deux appareils et ne parviennent jamais à TgWitness, quel que soit le mode utilisé.
- **Aucun enregistrement n’est effectué lorsque TgWitness n’est pas en cours d’exécution.** Après un redémarrage, il interroge Telegram pour récupérer les mises à jour manquées et vérifie à nouveau les discussions, mais Telegram ne restitue pas l’intégralité des données après de longues pannes. Les rapports et le fichier `verify.py` indiquent ces périodes sous forme de lacunes (voir [la section « Couverture »](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)).
- Seules les 1 000 premières conversations sont répertoriées au démarrage (la limite est définie dans **les paramètres**) ; les conversations plus anciennes sont ajoutées dès qu’elles redeviennent actives. L’historique antérieur d’une conversation ajoutée n’est pas récupéré — effectuez un instantané de l’historique ou une exportation complète de la conversation lorsque vous en avez besoin.
- Les conditions relatives aux dossiers qui changent constamment (silencieux, lu) ne sont pas prises en compte : ces discussions restent sous surveillance.
- **Les boutons du bot intégrés (callback)** sur lesquels on appuie dans une autre application sont invisibles pour une deuxième session ; la réponse ou la modification du bot est enregistrée. Les frappes sur le clavier de réponse sont transmises sous forme de messages sortants et sont identifiées par le code `button_press`.
- Plus il y a de discussions, plus il y a de demandes. Telegram restreint les comptes dont le volume est jugé excessif, ce qui constitue une raison supplémentaire d’utiliser des comptes dédiés.

## Portée et sélection des événements

Chaque espace de travail dispose de ses propres sources. TgWitness ne rejoint pas de groupes, n’accepte pas d’invitations et ne recense pas automatiquement tous les membres. Les sources doivent déjà être accessibles au compte. Au démarrage, le collecteur vérifie les sources sélectionnées par rapport aux conversations visibles du compte ; les 1 000 premières conversations sont inspectées, sauf indication contraire **dans Paramètres → Chats lus à partir de la liste du compte**. Une source absente est marquée comme **« accès non confirmé** » ; on ne suppose pas pour autant que vous ayez été supprimé.

| Contexte | Collecte | Conséquences en cas de désactivation |
| --- | --- | --- |
| Nouveaux messages | Messages ordinaires remis | Les modifications ou suppressions ultérieures peuvent ne pas disposer de texte capturé antérieurement avec lequel effectuer une comparaison. |
| Modifications | Versions modifiées des messages fournies | Les modifications intermédiaires ne sont pas reconstituées par la suite. |
| Suppressions | Notifications de suppression ciblées et notifications non ciblées au niveau du compte | Les notifications de suppression ne sont pas ajoutées au journal. |
| Réactions | Instantanés des réactions fournis | Les mises à jour relatives aux réactions ne sont pas ajoutées séparément. |
| Adhésion | Envoi de messages relatifs au service d’adhésion et de mises à jour destinées aux participants | Ces observations relatives à l’adhésion ne sont pas incluses. |

Les paramètres s’appliquent à toutes les sources sélectionnées dans l’espace de travail. Enregistrez le formulaire pour appliquer les modifications ; celles-ci sont consignées avec des valeurs « avant » et « après » signées. La désactivation d’une catégorie ne supprime pas les enregistrements antérieurs. Sa réactivation ne permet pas de récupérer les mises à jour manquées.

Les enregistrements opérationnels et autres événements liés aux services de groupe restent distincts de ces paramètres. Les messages de service relatifs à l’adhésion peuvent générer des enregistrements de messages lorsque l’adhésion est activée, même si la capture standard des nouveaux messages est désactivée. Les objets Telegram capturés conservent leurs métadonnées intégrées ; un paramètre ne constitue pas une règle de caviardage.

**Les suppressions dans les discussions privées et les groupes ordinaires** apparaissent sous forme d’identifiants de message sans discussion associée. Ces discussions partagent une séquence d’identifiants de message valable pour l’ensemble du compte ; ainsi, lorsqu’un message portant cet identifiant a été enregistré auparavant, sa discussion est connue : la suppression est consignée dans cette discussion, comme l’explique `chat_resolution`. Les identifiants jamais enregistrés restent une **suppression sans contexte,** avec une source explicitement inconnue ; le collecteur ne fait aucune supposition. Telegram n’indique jamais qui a supprimé un message ; lorsque le message supprimé a été envoyé par ce compte, l’enregistrement l’indique (`deleted_message_was_outgoing`) sans nommer la personne à l’origine de la suppression.

## Actions propres

Les messages envoyés par le compte surveillé sont identifiés par la mention « `outgoing` ». La modification d’un message sortant précise que, dans les discussions privées et les groupes, seul son auteur peut le modifier, tandis que les publications sur les chaînes peuvent être modifiées par d’autres administrateurs. Lorsqu’un message sortant reprend le texte d’un bouton issu du dernier clavier de réponse enregistré dans cette conversation, il porte la mention « `button_press` » accompagnée d’un lien vers l’enregistrement correspondant du clavier.

L'exclusion de vos propres actions s'applique également aux vérifications en arrière-plan et à l'historique automatique des nouvelles conversations. Les messages sortants ignorés font avancer la position de vérification afin qu'ils ne puissent pas bloquer les messages entrants ultérieurs. Les actions explicites effectuées dans le panneau et les instantanés d'historique demandés manuellement restent enregistrés.

## Mode d’enquête : rejoindre des groupes et communiquer avec des bots

**Sources → Portée d’observation → Le mode d’enquête** configure la portée pour un compte dédié qui rejoint des discussions de groupe, lance des bots et leur envoie des messages : l’intégralité du compte, chaque type de source, vos propres actions, ainsi que, pour chaque discussion ou bot qui apparaît, son profil et ses 200 derniers messages visibles. Vérifiez le formulaire et cliquez sur **« Enregistrer le champ d’observation »** ; le passage à l’ensemble du compte nécessite la confirmation habituelle.

- **Boutons.** Les boutons situés sous un message sont conservés avec celui-ci et s’affichent dans **les discussions** : liens, applications web, liens de connexion, textes à copier, données de rappel, requêtes intégrées, demandes de numéro de téléphone ou de localisation. Les liens s’affichent sous forme de texte et ne sont jamais ouverts par le panneau. Lorsqu’un bot modifie uniquement les boutons (un nouveau lien de paiement), il s’agit d’une nouvelle version du message, tant lors des mises à jour en temps réel que lors des vérifications ultérieures.
- **Nouvelles conversations et nouveaux bots.** En mode « dossier » et en mode « compte entier », **lorsqu’une nouvelle conversation ou un nouveau bot apparaît**, l’enregistrement s’effectue immédiatement après son apparition :

  - son profil sous forme d’enregistrement `source.profile` : description du bot et commandes, texte de présentation d’un utilisateur, d’un groupe ou d’une chaîne, membres, discussion associée et lien d’invitation lorsque Telegram en fournit un ;
  - ses derniers messages visibles (jusqu’à 1 000) sous la forme d’un instantané de l’historique marqué `new_chat` : les messages antérieurs d’une discussion de groupe à laquelle vous venez de rejoindre, ou ce qu’un bot a dit avant que l’observation ne détecte la discussion. Les messages déjà enregistrés en temps réel ne sont pas répétés.

  Les discussions déjà présentes dans la liste au moment de l’activation du mode sont ajoutées sans capture d’écran. Un FloodWait suspend cette opération, qui reprend ensuite ; les échecs sont consignés et l’ enregistrement en temps réel de la discussion se poursuit. - **Profils sur demande. Conversations → Profil → Enregistrer le profil**permet **désormais** d’enregistrer le profil actuel de n’importe quelle source ; le plus récent s’affiche au-dessus des messages. - **Non visible.** Les boutons intégrés (callback) sur lesquels on appuie dans une autre application Telegram, la fenêtre contextuelle ou le lien par lequel un bot répond à une telle pression, ainsi que les liens d’invitation utilisés dans une autre application n’atteignent pas TgWitness. Ce que le bot envoie ou modifie par la suite est enregistré.

### Intervention lors de la table ronde

**La rubrique « Chats »** comprend désormais un mini-client utilisant le compte Telegram de l'espace de travail sélectionné :

- Rédigez un message en texte brut ou sélectionnez **« Répondre »** sous un message enregistré. Le message sortant ainsi généré est enregistré même lorsque la configuration exclut les mises à jour sortantes.
- Appuyez sur**le bouton « Appuyer »** situé sous un bouton de rappel ou de texte actif. Le serveur récupère à nouveau le message et refuse l’action si le clavier diffère de la version enregistrée. Les accusés de réception des rappels conservent le texte de la fenêtre contextuelle de Telegram, le drapeau d’alerte et l’URL ; la réponse s’affiche également sous la conversation. Les URL restent du texte sélectionnable et ne s’ouvrent pas automatiquement.
- Développez **le lien « Ouvrir Telegram** », saisissez `@username`, un lien public `https://t.me/name`, `https://t.me/+invite` / `joinchat/invite`, ou un lien de bot avec `?start=parameter`, puis cliquez sur « **Enregistrer l’aperçu** ». Le lien d’origine et l’aperçu Telegram sont signés avant l’adhésion. **Rejoindre / ouvrir et observer** : le système rejoint alors le groupe/la chaîne ou ouvre l’utilisateur/le bot, ajoute la conversation en tant que source activée et envoie « `/start` » à un bot, en incluant son paramètre de démarrage. Une demande d’adhésion en attente de validation par l’administrateur est enregistrée comme « en attente », et non comme une adhésion effective.

Activez « **Démarrer l’observation** » pour capturer les réponses entrantes en temps réel. Les actions du panneau fonctionnent lorsque l’observation est en pause, mais seules leurs réponses directes sont alors garanties d’être enregistrées. Les sources nouvellement ajoutées utilisent le profil configuré ou l’historique de collecte lorsque l’observation est en cours. Lorsqu’une source est en pause, activez-la dans **« Sources »** avant d’envoyer un message ou d’appuyer sur ses boutons.

`interaction.preview`, `interaction.requested` et `interaction.result` sont des événements courants du journal signés inclus dans les exportations de preuves. Les requêtes identifient le compte, le message/bouton ou l'aperçu concerné, et indiquent si l'observation était en cours. Les accusés de réception distinguent les cas de réussite, de rejet, d'approbation en attente et de résultat inconnu. Une requête interrompue peut avoir atteint Telegram : veuillez vérifier la conversation avant de lancer une nouvelle action. La réutilisation d’un identifiant de requête permet de récupérer son accusé de réception enregistré sans répéter l’action, y compris après un redémarrage. Le panneau conserve l’ identifiant après une réponse ambiguë pour la même action au cours de la session de page en cours. Il conserve également cet identifiant lorsque l’actualisation de la vue échoue après une action réussie : l’accusé de réception reste visible, et un nouveau clic permet de le récupérer. Les RPC de rappel et de participation ne disposent que d’une seule tentative ; les lectures réessayables conservent leur politique de réessai configurée. Le changement de discussion efface immédiatement le brouillon et la cible de réponse, et désactive l’envoi jusqu’à ce que la nouvelle conversation soit chargée.

Ce mini-client gère les boutons de texte et de rappel. Les applications web, les demandes d’identification, de numéro de téléphone ou de localisation, les paiements, les requêtes intégrées et les pièces jointes nécessitent toujours un client Telegram ; les métadonnées des boutons enregistrés restent visibles. Les nouvelles commandes utilisent du texte en anglais.

## Niveaux de vérification

Les vérifications de suivi demandent à nouveau à Telegram les messages manqués, les modifications et les messages qu’il ne renvoie plus. Les sources marquées d’une étoile sont des sources **prioritaires**, revérifiées toutes les 15 minutes par défaut ; toutes les autres sources toutes les 6 heures. Les discussions sélectionnées sont initialement considérées comme des sources prioritaires, tandis que celles ajoutées via un dossier ou l’ensemble du compte sont traitées comme des sources standard. Au maximum 30 sources sont revérifiées par cycle et les autres attendent la minute suivante ; après une reconnexion, les sources prioritaires sont traitées en premier. Ces deux intervalles sont définis sous Sources → Paramètres d’enregistrement → Revérification (la valeur 0 désactive un niveau) et sont enregistrés sous la forme `recheck.changed`.

Les messages manqués sont récupérés à partir du point où le cycle précédent s’est arrêté, dans la limite du nombre de **« nouveaux messages par nouvelle vérification »** (1 000 par défaut) défini dans **Paramètres**. Après une longue interruption, la nouvelle vérification comble donc l’intégralité du retard, même lorsque des messages en temps réel plus récents que le retard ont été enregistrés en premier. Une conversation qui est encore en cours de rattrapage est vérifiée à nouveau dès la minute suivante au lieu d’ attendre son intervalle de niveau ; `recheck.completed` affiche `continues_after` jusqu’à ce que l’opération soit terminée.

Les comparaisons portent sur le texte des messages, les entités, les claviers (y compris les suppressions) et le contenu/l’identité des pièces jointes. La modification des hachages d’accès aux fichiers ou des références de fichiers ne constitue pas à elle seule une modification, pas plus que ce que Telegram ajoute de lui-même : le chargement d’un aperçu de lien, les vues d’une story, les contenus multimédias payants débloqués par ce compte, la réception d’une facture. Chaque version enregistrée dans « Chats » renvoie vers son enregistrement complet dans le journal, y compris les métadonnées des médias.

## Historique des messages et attribution

Supposons que le collecteur observe « Réunion à 10 h », puis constate « Réunion à 11 h », et reçoive ensuite une notification de suppression. Il ajoute alors trois observations distinctes. Le texte d’origine est conservé, la modification constitue une version distincte, et la notification indique qu’ une suppression a été constatée.

Si la collecte a commencé après la disparition de la première version, ce texte n’est pas disponible. Si plusieurs modifications ont eu lieu alors que le processus était hors ligne, seules les versions observées par la suite peuvent être enregistrées. Une notification de suppression ne permet pas de récupérer un contenu qui n’a jamais été capturé.

L’expéditeur d’un message n’est pas automatiquement la personne qui l’a modifié. Telegram ne fournit généralement pas l’identité de la personne ayant supprimé un message ni l’heure exacte de la suppression. Les acteurs inconnus restent inconnus. Les instantanés des réactions et les mises à jour des participants ne contiennent que les chiffres et les identités que Telegram rend visibles au titulaire du compte.

Les numéros de séquence indiquent l’ordre d’observation. L’horodatage UTC du collecteur correspond à son horloge locale ; l’horodatage source de Telegram est stocké séparément lorsqu’il est fourni. Aucun de ces deux horodatages n’est considéré comme un horodatage fiable et indépendant.

## Instantanés de l'historique

Une requête « snapshot » récupère les derniers messages visibles provenant d’une source activée, dans la limite de 500 par requête. Les résultats sont qualifiés d’« observations historiques ». Ils peuvent se chevaucher avec la capture en temps réel, et les observations répétées sont conservées sous forme d’enregistrements distincts.

Les instantanés respectent la politique relative aux pièces jointes, mais restent distincts des changements liés aux événements en temps réel. Ils ne reconstituent pas les messages supprimés ni les versions intermédiaires manquantes. Vous pouvez en demander un lorsque l’enregistrement est en pause ; les pièces jointes mises en file d’attente attendent que l’observation commence et que le processus de téléchargement s’exécute.

## Gestion des pièces jointes

Le téléchargement des pièces jointes est activé par défaut et est suspendu lorsque l'espace disque disponible est inférieur à 1 GiB. Le collecteur valide simultanément la surveillance des messages et la tâche de téléchargement. La tâche conserve le descripteur multimédia d’origine et la politique de taille, de sorte qu’une pièce jointe modifiée ultérieurement ne soit pas remplacée sans préavis.

Les téléchargements s’exécutent après la capture des messages. Un téléchargement abouti génère un enregistrement « `media.saved` » accompagné de son hachage SHA-256 et de son nombre d’octets. Les opérations ignorées, ayant échoué, ayant fait l’objet d’une nouvelle tentative ou ayant été interrompues génèrent des résultats distincts. Une tâche mise en file d’attente ne constitue pas une preuve que le fichier a été préservé. Le fichier final doit également correspondre au nombre d’octets indiqué dans le descripteur de pièce jointe d’origine observé. Une réponse trop courte ou inattendue n’est pas enregistrée comme média conservé.

Des limites sont définies **par type** : photos, vidéos, GIF et animations, messages vidéo circulaires, messages vocaux, musique et fichiers audio, autocollants et fichiers. Chaque type peut être désactivé et dispose de sa propre limite de taille comprise entre 1 et 2 000 Mio ; les nouveaux espaces de travail commencent avec 20 Mio pour les photos, 100 Mio pour les vidéos, 50 Mio pour les fichiers, les fichiers audio et les vidéos circulaires, 20 Mio pour les messages vocaux et les GIF, et 5 MiB pour les autocollants. *La taille maximale des fichiers* s’applique à tous les types simultanément. Les politiques enregistrées avant l’ instauration des limites par type conservent leur limite unique pour chaque type. Un type désactivé génère un enregistrement `media.skipped` ; les fichiers de taille inconnue ou trop volumineux ne sont pas téléchargés. Les fichiers volumineux bénéficient d’un débit de téléchargement d’au moins 256 KiB/s. Les tâches survivent à un redémarrage, mais les références expirées, la perte d’ accès ou la suppression de fichiers peuvent néanmoins empêcher leur récupération. Les tâches existantes conservent la politique enregistrée avec elles.

## Mettre en pause, verrouiller, se déconnecter et redémarrer

| Action ou état | Effet |
| --- | --- |
| Changer d'espace de travail | Modifie l’affichage du panneau ; les autres collecteurs conservent leur état. |
| Verrouillez le panneau ou fermez l'onglet | Le serveur et le système d’observation continuent de fonctionner. |
| Observation en pause | Interrompt ce collecteur et conserve les pièces jointes en attente de traitement. |
| Désactiver une source | Interrompt toute capture ciblée future ; les tâches multimédias mises en file d’attente pour celle-ci sont mises en attente tant qu’elle est désactivée. |
| Supprimer une source | Il ignore cette source et supprime les profils des utilisateurs concernés ; les enregistrements déjà sauvegardés restent dans le journal à ajout seul. Les pièces jointes encore en attente sont enregistrées comme ayant échoué (`source_removed`). En modes « dossier » et « compte entier », elles sont également exclues. |
| Modifier l'itinéraire de connexion | Nécessite une pause, ferme les anciens clients et annule les connexions inachevées. |
| Arrêtez le processus Python | Interrompt tous les espaces de travail ; aucune observation n’est effectuée lorsque l’outil est hors ligne. |
| Redémarrage après une période d’observation active | Tente de reprendre la portée enregistrée à l'aide de la session sauvegardée. Une pause manuelle annule cette intention. |

Le collecteur enregistre les déconnexions détectées, les nouvelles tentatives, les erreurs, les démarrages/arrêts et les signaux de présence. Les courtes interruptions peuvent échapper aux contrôles de connectivité périodiques. Après un redémarrage, les mises à jour manquées sont demandées à partir de la position de mise à jour enregistrée et les discussions surveillées sont revérifiées périodiquement ; voir [le format des preuves](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#durable-collection-and-process-receipts-02). Un instantané fournit le contexte ; il ne prouve pas qu’une lacune a été comblée.

## Isolement et vérification des comptes

Chaque espace de travail dispose de son propre journal, de ses propres autorisations, de sa clé de signature, de sa politique et de sa file d’attente. Seul son client actif peut y ajouter des observations en temps réel. Les clients rejetés, en attente, remplacés ou effectuant un test de connexion ne peuvent pas enregistrer de mises à jour en temps réel dans ce journal. Différents comptes peuvent observer le même groupe, mais leurs journaux restent distincts.

Chaque événement comprend le hachage précédent et une signature Ed25519. Les exportations couvrent l’ intégralité du journal de l’espace de travail grâce à un numéro de séquence fixe. Les filtres du panneau ne filtrent pas l’exportation ; la collecte peut se poursuivre au-delà de ses limites pendant sa préparation.

**La vérification du journal** contrôle la chaîne d’événements et les signatures à travers la limite affichée. Son résultat est effacé lorsque l’espace de travail change, et le panneau identifie les nouveaux enregistrements ajoutés après la vérification. L’exportation au format ZIP permet également de vérifier les médias collectés.

Une signature valide garantit l’intégrité par rapport à la clé de confiance, et non par rapport à l’origine Telegram ou à la véracité du contenu. Conservez les empreintes et les points de contrôle de manière indépendante. Consultez le [modèle de preuve](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/), [les opérations quotidiennes](https://phishdestroy.github.io/TgWitness/fr/docs/reference/operations/) et [la procédure d’acceptation en temps réel](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) pour connaître les exigences en matière de confiance et de transmission.
