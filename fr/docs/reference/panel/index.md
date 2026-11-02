# Guide des panneaux

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/panel/

Tous les écrans du panneau : discussions, journal, sources, exportations, « Extras », modes de protection et vérification du code.

[Première configuration et paramètres](https://phishdestroy.github.io/TgWitness/fr/docs/reference/settings/) · [Comptes](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/) · [Exporter et vérifier](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/) · [Rapports de cas](https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-reports/)

Fonctionnalités de chaque écran, informations consignées dans le journal signé et emplacement du guide détaillé. Le panneau affiche un espace de travail à la fois : un compte Telegram avec ses propres sources, son journal et sa clé de signature. Le sélecteur situé en haut de la barre latérale permet de changer d’ espace de travail. L’adresse identifie l’espace de travail (`?ws=…`) ; tant que l’adresse, le sélecteur et le compte chargé ne correspondent pas, les actions restent bloquées.

## Repérez-vous

Les sections quotidiennes se trouvent en haut de la barre latérale, **la section « Comptes »** se trouve sous « **Espace de travail »** , et tout le reste se trouve sous « **Autres outils et paramètres** ». Le sélecteur **de niveau d’interface** dans la barre supérieure détermine le nombre de sections affichées :

| Niveau | Rubriques de la barre latérale |
| --- | --- |
| Simple | Accueil, Discussions, Modifications, Archives et Paramètres |
| Standard | Voir également Case Board, Comptes et accès |
| Expert | Également : Sources, Extras, Demander à l'archive, Paramètres, Compte, Journal système et Intégrations |

Appels simples : « Commencer ici », « Journal » et « Exportations » ; « **Accueil** », « **Modifications** » et « **Archives** ». Un niveau masque uniquement des sections. Une fonctionnalité masquée continue de fonctionner, et le serveur vérifie chaque autorisation de manière autonome. Le niveau, la langue, le thème et le fuseau horaire sont enregistrés par opérateur et par espace de travail ; voir [les paramètres](https://phishdestroy.github.io/TgWitness/fr/docs/reference/settings/).

La barre supérieure comporte également :

- **Accéder à une section** (Ctrl+K, ou ⌘K sur Mac) : rechercher une conversation, un paramètre ou une entrée de journal en `#number`. Les touches fléchées permettent de se déplacer, Entrée ouvre l'élément, Échap le ferme.
- **Notifications** : problèmes et modifications apportées aux discussions traités à partir du journal. L'option « **Marquer tout comme lu »** remet le compteur à zéro et « **Règles de notification »** ouvre la liste des règles. La transmission vers Telegram, Discord ou par e-mail se configure dans [Extras → Notifications](https://phishdestroy.github.io/TgWitness/fr/docs/reference/panel/#notifications).
- L'indicateur de connexion de cet espace de travail. **L'état du collecteur,** situé sous la barre supérieure, le divise en plusieurs éléments : la connexion Telegram, la réception des événements, les sources et la file d'attente des pièces jointes.
- **Verrouiller** : ferme le panneau dans ce navigateur. La collection continue de fonctionner sur le serveur.
- Le mode de protection situé à côté du numéro de version ; voir [les modes de protection](https://phishdestroy.github.io/TgWitness/fr/docs/reference/panel/#protection-modes).

L'espace de travail de démonstration contient des messages fictifs et ne se connecte jamais à Telegram. Les actions susceptibles de modifier un véritable espace de travail y sont refusées.

## Commencez ici

Choisissez une tâche. **L’option « Exporter mon compte »** télécharge tout ce que le compte peut lire actuellement. La fonction « **Suivre une enquête »** enregistre les nouveaux messages, les modifications observées et les notifications de suppression provenant des discussions que vous sélectionnez. La fiche de configuration présente les trois étapes : connecter le compte, choisir les sources, lancer la surveillance. La question d’objectif reste affichée sur cette page jusqu’à ce que vous y répondiez ou que vous la ignoriez. Un nouvel espace de travail ouvre directement la [première configuration](https://phishdestroy.github.io/TgWitness/fr/docs/reference/settings/).

## Discussions

Conversations enregistrées, en lecture seule par défaut.

- Effectuez une recherche dans la liste par nom ou par identifiant. **Choisissez** permet d’ajouter ou de supprimer des discussions suivies. **Ouvrir le lien Telegram** prend en charge un nom d’utilisateur ou un lien d’invitation et enregistre un aperçu dans le journal. **Rejoindre / ouvrir et observer** rejoint ensuite la discussion et l’ajoute à vos sources ; l’ouverture d’un bot l’envoie `/start`.
- L'en-tête de la conversation recense les messages **supprimés, le texte conservé**, **les messages supprimés avant la sauvegarde** et **ceux introuvables lors d'une nouvelle vérification**. La liste des conversations et les notifications utilisent les mêmes définitions. Un message supprimé apparaît en rouge et conserve son texte sauvegardé ; un message modifié conserve toutes ses versions sauvegardées. Chaque suppression indique ce que l'on sait : quand le message a été lu, que Telegram ne signale pas qui l'a supprimé, ou que seule la notification est parvenue.
- **L'historique de chargement** affiche les 100, 250 ou 500 derniers messages dans cette vue et dans le journal. Pour charger toutes les sources activées, utilisez [Sources → Historique complet](https://phishdestroy.github.io/TgWitness/fr/docs/reference/panel/#sources).
- **La fonction « Exporter la conversation » permet de** télécharger l’historique complet visible sous la forme d’un fichier signé `chat.json` et `chat.html`. Plusieurs comptes connectés peuvent se répartir la tâche : chacun télécharge sa propre plage de numéros de messages et signe sa partie, puis le compte qui a lancé l’ exportation signe l’archive. Voir « [Exporter une conversation](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) ».
- La liste **des participants** répertorie toutes les personnes dont les messages ont été enregistrés dans cette conversation. Les profils des participants sont désactivés par défaut, car il s’agit de données personnelles concernant des tiers. Lorsqu’ils sont activés pour une conversation, un profil affiche le nom et l’historique des noms d’utilisateur, les indicateurs Telegram, les hachages d’avatar, l’activité, qui répond à qui, les autres conversations observées, ainsi que les portefeuilles, téléphones, noms d’utilisateur et liens mentionnés. Chaque information renvoie à son enregistrement. **L’exportation des profils** enregistre un fichier signé, éventuellement dans un ZIP protégé par mot de passe ; la désactivation des profils supprime le fichier de profil. Voir [les profils des utilisateurs](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#people-profiles).
- **Enregistrer le profil maintenant** permet d'enregistrer un instantané de la discussion ou du profil d'un bot : description, membres, lien d'invitation, commandes du bot.

### Mode lecture seule, envoi et secrets

Deux boutons situés au-dessus des messages protègent le compte et le lecteur :

- **En lecture seule** est activé lorsqu'une conversation s'ouvre. Désactivez-le pour envoyer des messages ou appuyer sur les boutons du bot . Chaque action demande **Envoyer en tant que @compte ?** ou **Appuyez sur ce bouton du bot en tant que @compte ?**, vous indique que les participants à la conversation le voient et qu'il est ajouté au journal signé . **Ne posez plus cette question avant 10 minutes dans ce chat** ignore la question pendant un certain temps. L'envoi est désactivé pour l'objectif **Éléments de preuve à l'appui d'une affaire**, dans le panneau et dans l'API.
- **La fonction « Mask secrets »** masque ce qui ressemble à un mot de passe, un code de connexion, une clé API ou un hachage, un jeton de bot, une chaîne de session, une clé privée, un JWT ou un numéro de carte bancaire (les numéros de carte sont vérifiés à l’aide de la somme de Luhn). **La fonction « Show »** révèle une valeur ; cette révélation est enregistrée dans le journal. La désactivation du masquage pour ce navigateur est également enregistrée. Seul l’affichage change : les enregistrements d’origine et toutes les exportations conservent le texte intégral.

## Journal

Tous les enregistrements signés par l'espace de travail, classés par ordre chronologique décroissant.

- **La vue d’ensemble** recense les messages observés, les modifications enregistrées, les notifications de suppression et les sources sélectionnées.
- **Chronologie des événements** permet de filtrer par type d'événement (tout, modifications, suppressions, réactions, appartenance, couverture), par texte et par source. **Charger les événements précédents** permet de revenir en arrière.
- Ouvrez un enregistrement pour consulter ses détails, son hachage et sa charge utile. **Le lien vers cet enregistrement** est une adresse qui ouvre le même enregistrement. Les informations confidentielles éventuelles sont masquées dans cet aperçu ; les exportations conservent l'original.
- Le journal est en écriture seule : aucune action dans le panneau ne permet de modifier ou de supprimer un enregistrement. Vérifiez-le via **Exportations → Vérifier le journal** ou `python -m tgwitness.verify`; voir « [Exporter et vérifier](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/) ».

## Sources

Cet espace de travail enregistre certaines conversations et conserve certaines informations issues de celles-ci. Les modifications s'appliquent aux activités futures ; les enregistrements sauvegardés sont conservés.

**La fonction « Actualiser la liste des discussions »** lit les discussions et les dossiers du compte. Elle ne télécharge pas les messages.

### Portée

- **Ce que ce compte enregistre** : **Discussions sélectionnées** (uniquement les discussions que vous ajoutez), **Dossier Telegram** (l'un des dossiers du compte, y compris les discussions qui y sont ajoutées par la suite) ou **Compte complet** (toutes les discussions, ainsi que chaque nouvelle discussion, groupe, discussion privée ou bot dès son apparition). **Mode enquête** est destiné à un compte dédié : il enregistre tout ce que le compte voit, ses propres messages et les actions sur les boutons, et sauvegarde immédiatement le profil de chaque nouvelle discussion ainsi que les messages visibles antérieurs. L’ [Guide dédié aux comptes](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) explique pourquoi il ne faut jamais utiliser votre compte principal.
- **Les types de source** limitent les modes « dossier » et « compte entier » aux chaînes, groupes, discussions privées et bots. L’option « **Propres actions »** ajoute les messages, modifications et frappes sur le clavier de réponse propres au compte.
- **Lorsqu’une nouvelle discussion ou un nouveau bot apparaît** : enregistrez son profil et jusqu’au nombre choisi de ses derniers messages visibles.

Limites : les discussions secrètes n’apparaissent jamais dans TgWitness. Rien n’est enregistré lorsque TgWitness n’est pas en cours d’exécution ; après un redémarrage, il ne récupère que ce que Telegram renvoie encore, et le rapport indique le manque de données. Les discussions dépassant la limite de la liste des discussions (1 000 dialogues, sauf modification dans les paramètres) sont ajoutées dès qu’elles deviennent actives. Les boutons du bot intégrés cliqués dans une autre application sont invisibles ; la réponse du bot est enregistrée.

### Discussions concernées

Filtrez par statut (**Activé**, **En pause**, **Prioritaire**, **Exclu**, **Accès non confirmé**, **Ignoré**) et par type, puis effectuez une action sur une sélection : activer, mettre en pause, marquer ou supprimer la priorité, exclure du champ d’application ou supprimer. L’icône de statut indique uniquement l’état ; les actions se trouvent dans le menu de chaque ligne, accompagnées d’une description de leur fonction. La mise en pause et l’exclusion nécessitent une confirmation, y compris en masse. La suppression d’une source demande son nom et supprime les profils des personnes associées ; ses enregistrements sauvegardés restent dans le journal.

Une source que la liste des discussions du compte n'affiche pas est **réception des mises à jour, hors de la liste des discussions** tant que des enregistrements continuent d'arriver, sinon **Accès non confirmé**. **Discussions disponibles** ajoute des discussions avec **Ajouter la sélection** ou **Ajouter tous les résultats**.

### Historique complet

Charge l'historique disponible de chaque source activée dans les « Chats » et le journal. La progression est conservée après un redémarrage ; les pièces jointes respectent vos paramètres multimédia. Voir [l'historique des sources](https://phishdestroy.github.io/TgWitness/fr/docs/reference/history/).

### Enregistrement

- **Choisissez les modifications à conserver** : nouveaux messages, modifications, notifications de suppression, réactions visibles, arrivées et départs. Un préréglage modifie le formulaire ; l’option « **Enregistrer les paramètres d’enregistrement »** l’applique. Le fait de réactiver une catégorie ne permet pas de récupérer les événements manqués.
- **Conserver les médias lorsqu'ils sont disponibles** : télécharger les pièces jointes jusqu'à une taille maximale par fichier, définir par type une valeur comprise entre 1 et 2 000 MiB, et limiter la durée des vidéos en secondes (0 signifie aucune limite). Chaque tentative de téléchargement donne lieu à l'enregistrement d'un résultat.
- **Vérification** : les discussions prioritaires sont vérifiées toutes les quelques minutes, les autres rarement, afin que le compte reste en deçà des limites « FloodWait » de Telegram. La valeur 0 désactive un groupe. Marquez les discussions prioritaires avec l’étoile dans la liste ; le nombre de discussions par passage et la pause entre les discussions se trouvent dans les paramètres. Voir [la collection](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/).

## Exportations

**La section « Téléchargements »** prépare les fichiers ; la section « **Rapport de compilation »** permet de choisir la présentation des rapports.

| Qu'est-ce que | Utilisez-le pour | Guide |
| --- | --- | --- |
| Exportation de comptes | Un instantané récent de ce que le compte peut lire actuellement | [Exportation de comptes](https://phishdestroy.github.io/TgWitness/fr/docs/reference/account-export/) |
| Partage de la copie | Une version simplifiée d'une exportation de compte finalisée | [Mentions légales](https://phishdestroy.github.io/TgWitness/fr/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| Signé ZIP | Journal, rapport, pièces jointes et outils de vérification au sein d'une limite de journal fixe | [Exporter et vérifier](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/) |
| Rapport au format HTML, PDF, JSON | Un rapport scellé et lisible | [Rapports de cas](https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-reports/) |
| JSONL, CSV | Enregistrements originaux avec signatures ; une feuille de calcul sécurisée au niveau des formules | [Exporter et vérifier](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/) |
| Extrait de la passation de pouvoir | Uniquement les discussions, la période et les personnes dont le destinataire a besoin | [Preuves](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#investigation-handoff) |
| Exportation des discussions | Un chat signé `chat.json` et `chat.html` | [Exporter une conversation](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **Le chiffrement des téléchargements ci-dessus à l'aide d'un mot de passe** (12 caractères ou plus) permet d'enregistrer un fichier AES-256 ZIP, qui s'ouvre avec 7-Zip ou WinRAR. Le fichier signé qu'il contient reste inchangé. Le mot de passe n'est pas stocké.
- **Les exportations préparées** conservent jusqu’à 20 fichiers dans la limite de 2 Gio, plus le dernier en date, pour des téléchargements répétés, chacun comportant son SHA-256. La préparation d’un fichier ne garantit pas sa livraison.
- Lorsque le navigateur refuse d’afficher sa boîte de dialogue d’enregistrement, le panneau revient à un téléchargement classique.
- **Votre identité de signature** affiche l’empreinte de la clé. Les options « **Enregistrer un point de contrôle »** et « Télécharger **le reçu d’exécution signé »** vous permettent de conserver des enregistrements en dehors du collecteur. L’option « Préparer **une requête d’horodatage »** génère une requête RFC 3161 sans contacter aucun service.

## Paramètres, comptes et connexion

- **Paramètres** : objectif, connexion, éléments à enregistrer et interface. Consultez les sections « [Première configuration » et « Paramètres](https://phishdestroy.github.io/TgWitness/fr/docs/reference/settings/) ».
- **Comptes** : chaque espace de travail avec son état, ses sources, ses événements et sa file d'attente de pièces jointes. Filtrez par **Nécessite une attention**, **Collecte**, **Hors ligne ou en pause** ou **Non connecté**, mettez en pause ou reprenez une sélection, importez des fichiers de compte en masse et gérez les groupes. Voir [comptes](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/).
- **Compte** : connexion et itinéraire de connexion de ce compte. Direct, un profil WireGuard, votre propre proxy, le pool MTProto public ou WARP ; préparez et vérifiez un itinéraire, puis appliquez-le à ce compte, à un groupe ou à tous les comptes. Voir « [Connexion » et «](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/) [Proxys](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md) ».

## Extras

Facultatif : un compte et des sources suffisent pour commencer la collecte. Seule l’option que vous choisissez ouvre ses paramètres, et rien n’est connecté automatiquement. La carte « **Niveau de protection »** en haut de l’écran indique le [mode de protection](https://phishdestroy.github.io/TgWitness/fr/docs/reference/panel/#protection-modes).

| Fiche | Ce qu'il apporte | Guide |
| --- | --- | --- |
| Stockage et espace disque | Sauvegardes, transfert des anciens fichiers vers votre cloud, copie à valeur probatoire ne pouvant pas être supprimée | [Stockage](https://phishdestroy.github.io/TgWitness/fr/docs/reference/storage/) |
| Objectif et niveau de protection | Paramètres suggérés pour votre objectif et deux échelles | [ci-dessous](https://phishdestroy.github.io/TgWitness/fr/docs/reference/panel/#goal-and-protection-level) |
| Notifications | Problèmes, messages modifiés et résumé quotidien ; votre propre bot de contrôle | [ci-dessous](https://phishdestroy.github.io/TgWitness/fr/docs/reference/panel/#notifications) |
| Preuves et sauvegardes | Horodatages, témoins supplémentaires et copie chiffrée hors site | [ci-dessous](https://phishdestroy.github.io/TgWitness/fr/docs/reference/panel/#evidence-and-backups) |
| Serveur disponible 24 h/24, 7 j/7 | Un serveur cloud sans SSH, créé et supprimé depuis le panneau de configuration | [Haute fiabilité](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#from-the-panel) |
| Témoin indépendant | Des vérifications signées publiées sur votre chaîne Telegram ou Discord | [Witness](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/) |
| Vérification du code | Compare le programme en cours d'exécution à un commit GitHub public | [ci-dessous](https://phishdestroy.github.io/TgWitness/fr/docs/reference/panel/#code-check) |

### Objectif et niveau de protection

Quatre questions :

1. **À quoi cela sert-il ? À tenir** un journal personnel, à mener une enquête ou à constituer des preuves dans le cadre d’une affaire.
2. **Quel volume souhaitez-vous surveiller ?** Quelques discussions (jusqu’à environ 50), de nombreuses discussions (jusqu’à environ 500) ou des comptes entiers. Cela fixe la limite de la liste des discussions à 1 000, 3 000 ou 20 000.
3. **Photos et fichiers ?** Texte uniquement, photos et petits fichiers multimédias (photos de 20 Mo, vidéos de 100 Mo), ou tout (vidéos et documents jusqu’à 1 Go chacun). L’option « Tout » avec les comptes complets permet également de conserver 4 GiB d’espace libre sur le disque.
4. **Où cela fonctionnera-t-il ? Sur** cet ordinateur, ou sur un serveur qui reste allumé en permanence.

La suggestion répertorie les horodatages indépendants, le drand et la liste des appareils de Telegram, chacun accompagné d’une ligne décrivant ce qu’il apporte. Les horodatages sont générés toutes les 60, 30 ou 10 minutes pour un enregistrement personnel , une enquête ou une preuve ; le drand et la liste des appareils nécessitent des horodatages. **N’appliquez** les modifications qu’à ces éléments, à la politique relative aux pièces jointes et aux deux paramètres ci-dessus. Chaque modification correspond à une entrée de journal, ainsi qu’à `setup.applied`. Les notifications, une copie hors site, un serveur, le DNS de la passerelle, la vérification du code et un témoin sont proposés comme étapes suivantes, avec leurs propres formulaires.

Deux échelles sont calculées à partir des paramètres définis, et non à partir de l’objectif :

| Échelle | Points |
| --- | --- |
| Crédibilité | Journal signé 1, horodatages 3, drand 1, liste d'appareils 1, vérification de code correspondante 1, sondage des témoins 1, serveur certifié 2, journal DNS de la passerelle 1 |
| Fiabilité | Serveur toujours actif : 3, copies hors site : 3, Object Lock : 1, notifications de problèmes : 1 |

80 % ou plus pour le niveau « **maximum »**, 50 % **pour « élevé »**, 25 % **pour « modéré »**, et en dessous pour « **basique** ». La fiabilité prend actuellement en compte un serveur toujours actif, d’après la réponse à la question 4, avant toute vérification des serveurs.

### Notifications

Les notifications transitent par Apprise vers Telegram, Discord, Slack, ntfy, e-mail, Matrix et plus de 100 autres services. Choisissez un service, remplissez un ou deux champs et envoyez un test, ou collez directement les adresses Apprise.

- **Problèmes** : disque presque plein, déconnexion du compte, erreurs de collecte, de copie ou d’horodatage. Sur un serveur verrouillé, un port SSH ouvert ou une connexion constituent également un problème.
- **Modifications** : messages supprimés, modifiés ou manquants dans les discussions surveillées, regroupés en une seule notification par vérification (toutes les minutes, sauf modification dans les paramètres).
- **Tâches terminées** : historique, exportations et copies de sauvegarde.
- **Résumé quotidien** à l'heure choisie, heure du serveur.

Les notifications indiquent les noms des discussions et le nombre de messages. Les extraits de messages sont désactivés par défaut ; lorsqu’ ils sont activés, le texte des messages quitte cet ordinateur.

**Votre bot opérateur** est un bot que vous avez créé via @BotFather et qui répond `/status` et `/stats`, et éventuellement `/pause`, `/resume` et `/copy`. Seuls le chat indiqué et les identifiants d’utilisateur Telegram mentionnés peuvent l’utiliser ; le texte de la conversation reste dans l’espace de travail. Utilisez un bot distinct si une autre application reçoit déjà ses commandes. Voir [notifications](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md) et [bot opérateur](https://phishdestroy.github.io/TgWitness/fr/docs/reference/storage/#operator-bot-and-completion-notices).

### Preuves et sauvegardes

- **Horodatages indépendants** envoie uniquement l'SHA-256 de chaque point de contrôle signé aux autorités RFC 3161 et aux calendriers OpenTimestamps, toutes les 5 à 1 440 minutes. **Ancrer maintenant** exécute un cycle. Voir [horodatages](https://phishdestroy.github.io/TgWitness/fr/docs/reference/timestamp/).
- **D'autres témoins**, tous désactivés jusqu'à ce qu'ils soient sélectionnés : la dernière série « drand », la liste de Telegram des appareils connectés sans adresses IP, et le journal de Cloudflare Gateway concernant les requêtes DNS du serveur. Voir [les enregistrements facultatifs](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices).
- **La sauvegarde chiffrée** copie le journal, les fichiers, les points de contrôle et les exportations de discussions vers un stockage compatible S3 (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO). Tout est d’abord chiffré sur cette machine. **Téléchargez la clé de chiffrement** et conservez-la à l’écart : sans elle, la copie ne peut pas être lue. La fonction « Object Lock » en mode « Governance » ou « Compliance » empêche la suppression des objets pendant un nombre de jours défini. Voir « [Copie hors site](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md) ».

### Vérification du code

Vérifie si le programme installé correspond à une version publiée.

1. Saisissez un dépôt GitHub (celui officiel est déjà renseigné) ainsi qu'une balise, une branche ou un commit.
2. **Check now** interroge l’API de GitHub, via la route de cet espace de travail dédiée aux requêtes externes, pour obtenir la liste des fichiers de ce commit. Il compare l’ID de blob Git de chaque fichier de programme mesuré avec celui du commit. Une version Windows avec des fins de ligne converties correspond toujours.
3. Le résultat répertorie les fichiers modifiés, supplémentaires et manquants (jusqu’à 50 de chaque) et est enregistré sous la forme d’ un `source.checked` fiche de journal.

Le résultat n’est considéré comme à jour que tant que les fichiers du programme en cours d’exécution restent inchangés : vérifiez à nouveau après une mise à jour. Aucun jeton n’est nécessaire et seuls les dépôts publics fonctionnent ; les discussions et les identifiants ne sont pas téléchargés. Une correspondance identifie le code présent sur le disque. Il ne s’agit pas d’une attestation matérielle ; pour cela, consultez [Phala Cloud](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx).

## Modes de protection

Le sélecteur situé à côté du numéro de version indique le mode choisi et le nombre de couches de protection actives parmi les 18 disponibles, par exemple `🟠 Witnessed 9/18`. **Pour changer de mode**, sélectionnez « **Extras → Niveau de protection »** : le menu de sélection s’ouvre. Chaque mode décrit une cible et répertorie ce qui manque encore ; l’enregistrement, la signature et les paramètres enregistrés sont identiques dans tous les modes.

| Mode | Pour | Ajoute |
| --- | --- | --- |
| 🟢 Facile | Surveiller une conversation et en conserver une copie | Les discussions, le journal et les exportations de discussions ; la signature s'effectue en arrière-plan. |
| 🟡 Signé | Signale à une plateforme, à un hébergeur ou à un service de signalement des abus | Archive signée, vérification du journal, points de contrôle, extrait de transfert |
| 🟠 Certifié | Cas dans lesquels une personne pourrait prétendre que le record a été modifié | Un témoin indépendant publiant des en-têtes de journal signés |
| 🔴 Prêt à être utilisé devant les tribunaux | Éléments de preuve destinés à un avocat, à la police ou à un tribunal | Horodatages, copie cryptée hors site, détails des dossiers dans les rapports |
| 🟣 Vérifié par GitHub | Des enregistrements dont le logiciel doit pouvoir être vérifié par n'importe qui | Vérification du code et capture des GitHub Actions |
| ⚫ Mossad | Affaires à enjeux élevés contre un adversaire disposant de moyens financiers importants | Un serveur sécurisé disponible 24 h/24 et 7 j/7, une adresse IP masquée, les 18 couches |

Les couches : chaque enregistrement signé et chaîné ; un reçu d'exécution signé ; les pièces jointes enregistrées avec SHA-256 ; des points de contrôle signés ; des vérifications croisées ; des alertes de problème ; un accès témoin en lecture seule ; un témoin effectuant une vérification selon un calendrier ; des horodatages RFC 3161 ; des preuves OpenTimestamps ; un dernier horodatage vérifié ; une copie chiffrée hors site ; les détails du dossier dans les rapports ; une vérification de correspondance du code ; Telegram ne voit jamais l’adresse IP de cette machine ; les requêtes externes passent par un proxy ; un verrouillage d’objet sur la copie ; un serveur scellé contenant les enregistrements du fournisseur. Une couche désactivée dispose **d’une option « Configurer »**, qui ouvre son formulaire. Le choix d’un mode inférieur demande une confirmation et ne supprime rien.

## Plus d'outils

**Extras → Independent capture**: connect a separate browser or AyuGram recorder, pin its signing key, select capture options, start/pause, take snapshots and download verified signed archives. Each recorder has its own manual login, route, journal and key. Both connections start disabled. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md).

- **Consultez les archives** : recherchez les observations enregistrées, examinez les sources, puis décidez s'il convient de les envoyer à un modèle d'IA. Voir [analyse des archives](https://phishdestroy.github.io/TgWitness/fr/docs/reference/analysis/) et [OCR et transcription en local](https://phishdestroy.github.io/TgWitness/fr/docs/reference/media-analysis/).
- **Paramètres** : limites et cadence de collecte, vérifications, téléchargements, profils, notifications et exportations. Recherche par nom, affichage des « Valeurs **modifiées uniquement »** et préparation des paramètres par défaut sous forme de brouillon avec « **Restaurer les paramètres par défaut… »**. L’option « **Enregistrer les paramètres »** applique les valeurs dès leur prochaine utilisation, et chaque modification fait l’objet d’une entrée dans le journal.
- **Accès** : des jetons distincts pour les réviseurs, les analystes et les opérateurs, limités à certains espaces de travail, chats et droits. Voir [la section « Accès](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) ».
- **Journal système** : ce que ce processus a effectué depuis son démarrage (connexions, changements de proxy, connexions, refus, modifications de paramètres) avec les adresses IP masquées. L’option « **Suivre les nouvelles lignes »** permet de garder la ligne la plus récente à l’écran. Les messages ne figurent que dans le journal.
- **Intégrations** : le fournisseur d’IA, les connexions [MCP en lecture seule](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/) et [les webhooks signés](https://phishdestroy.github.io/TgWitness/fr/docs/reference/webhooks/).
- **Case Board** : notes privées de l'équipe, signets et extraits à côté des éléments de preuve. Voir [Case Board](https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-board/).
- **Capture GitHub Actions** dans « Exports » : une conversation capturée à partir de votre fork. Voir [capture scellée](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md).
