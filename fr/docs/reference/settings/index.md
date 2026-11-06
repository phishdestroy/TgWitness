# Telegram · Première configuration et paramètres

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/settings/

L&#x27;assistant de configuration, les objectifs, les niveaux d&#x27;interface, les chemins de connexion et les paramètres partagés par un groupe de comptes.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Pour commencer](https://phishdestroy.github.io/TgWitness/fr/docs/reference/quickstart/)

![Pour commencer](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Comptes](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/) · [Connexion](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/) · [Accès](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/)

Un nouvel espace de travail s'ouvre `/first-run`: langue et heure, niveau d’interface, objectif, connexion, Telegram et discussions. Chaque réponse est enregistrée sur le serveur dès qu’elle change, de sorte qu’un rafraîchissement reprend la même étape. Le dernier écran répertorie les réponses et vous permet de revenir à n’importe laquelle d’entre elles.

La langue, le fuseau horaire IANA, le thème et le niveau sont enregistrés par opérateur et par espace de travail. Les valeurs par défaut sont la langue du navigateur, le fuseau horaire de l’appareil, le thème du système et l’ interface simple. Le changement de langue ne modifie pas la session du panneau. Les heures indiquées dans le journal signé ne changent jamais.

`/settings` Il modifie les mêmes enregistrements que l’assistant. La recherche porte sur les champs principaux, les paramètres et les formulaires étendus ; un champ masqué peut être ouvert sans modifier le niveau. Les niveaux ne modifient que ce qui est affiché : le serveur vérifie lui-même les autorisations. Les paramètres de la collection et la première connexion relèvent de la responsabilité de l’administrateur de l’espace de travail.

| Niveau | Champs | Barre latérale |
| --- | --- | --- |
| Simple | L'essentiel, rien que l'essentiel | Accueil, Discussions, Modifications, Archives, Paramètres |
| Norme | Paramètres communs avec explications | Ajout de Case Board, Comptes et Accès |
| Expert | Tous les champs, limites et détails techniques | Ajoute les rubriques Sources, Extras, Demander à l'archive, Paramètres, Compte, Journal système et Intégrations |

[Le guide des panneaux](https://phishdestroy.github.io/TgWitness/fr/docs/reference/panel/) décrit chaque section.

## Objectifs

| Objectif | Collecte | Fichiers | Services externes | Adresse du serveur |
| --- | --- | --- | --- | --- |
| Copie d'archive | Désactivé ; « **Démarrer »** lance une exportation | Photos jusqu’à 20 Mo | Désactivé | Automatique |
| Suivre les discussions | En continu | Photos et vidéos d'une durée maximale de 60 secondes / 20 Mo | Horodatages et notifications de problèmes | Automatique |
| Preuves | En continu | Tous les fichiers jusqu’à 1 Go | Horodatages, drand, notifications | Non, le masquer |

La copie hors site, le bot « witness » et la vérification du code sont recommandés à des fins de preuve. Les adresses de stockage et de notification nécessitent d’abord une destination. Une fonctionnalité qui communique avec un service externe demande l’autorisation d’envoyer des requêtes en dehors de Telegram ; la désactiver entraîne la désactivation des horodatages, des notifications et de la copie hors site.

La modification de l’objectif affiche d’abord la différence, et les modifications manuelles peuvent être conservées. Un champ qui diffère de l’objectif est marqué « **Modifié par vous »** et peut être restauré. La révision des paramètres empêche qu’une différence révisée ne vienne remplacer une modification effectuée dans un autre onglet.

## Connexion

**Automatic** essaie d'abord les serveurs publics MTProxy, puis WARP, puis une connexion directe, cette dernière n'étant utilisée que lorsque l'adresse du serveur peut être affichée. Automatic et WARP peuvent installer des composants dont le hachage a été vérifié et enregistrer le serveur auprès de Cloudflare. WARP utilise le gestionnaire wgcf/wireproxy existant et un port SOCKS5 local ; la table de routage du système n'est pas modifiée. Lorsque des services externes sont nécessaires, Automatic privilégie WARP par rapport à MTProxy.

Votre propre proxy accepte `tg://proxy`, `socks5://`, `http://` et `https://`. Le certificat d’un proxy HTTPS est vérifié avant que les identifiants ne lui soient envoyés.

Une vérification de connexion est valable pendant cinq minutes et est liée à l’itinéraire, à la politique et aux réponses de l’assistant ; toute modification de l’un de ces éléments nécessite une nouvelle vérification. L’option **« Continuer sans vérification »** est disponible et ne remplace pas la connexion à Telegram. L’itinéraire choisi est revérifié en arrière-plan, et la fonction « Automatique » relance sa chaîne après une perte de connexion. Lorsqu’aucun proxy public ne répond, le compteur passe au rouge et déclenche des actions WARP et de revérification.

## Groupes de comptes

Les comptes d'un groupe partagent leurs paramètres. Ouvrez **Comptes → Groupes et paramètres partagés → Paramètres partagés**, ou **Paramètres du groupe** sur la page Paramètres d'un compte.

Le groupe partage l’objectif, les fichiers enregistrés, les horodatages, le drand, les notifications de problèmes, la copie hors site, les demandes en dehors de Telegram, le mode IP, les éléments à enregistrer, le calendrier de vérification, les règles de notification, les paramètres de rapport, les paramètres et l’itinéraire de connexion. Les destinataires des notifications, les identifiants du proxy et les informations de connexion restent propres à chaque compte, tout comme le démarrage et la mise en pause de la collecte.

- Chaque membre suit le groupe. Dans les paramètres, on peut attribuer une valeur 🔗 **à partir du groupe** ou ✏️ **une valeur personnalisée** ; l’option « **Revenir à la valeur du groupe »** rétablit la valeur par défaut.
- Une modification répertorie les comptes concernés (**s'applique à 2 comptes sur 3**) et demande confirmation pour chaque compte avant de remplacer une valeur. Les comptes non cochés conservent leur valeur d'origine.
- Un paramètre que le groupe ne partage pas reste sur « **Non partagé » : chaque compte conserve sa propre valeur** jusqu’à ce que vous cliquiez sur « **Partager cette valeur** ».
- **La copie des paramètres d'un compte** applique les valeurs du compte sélectionné à l'ensemble du groupe.
- Lorsqu’un compte est déplacé vers un groupe, on lui demande : « **Voulez-vous adopter les paramètres du groupe ? ».** Sinon, il conserve ses propres paramètres, signalés par ✏️. Les comptes ajoutés ultérieurement adoptent d’emblée les paramètres du groupe.
- Un compte d’observation conserve son mode IP jusqu’à ce qu’il soit mis en pause.

Chaque modification est consignée dans le journal signé de l'espace de travail principal et de chaque membre concerné. La suppression d'un groupe conserve ses comptes et leurs valeurs actuelles.

La page du groupe `/groups/<id>` affiche les membres, les éléments nécessitant une attention particulière et les discussions visibles par plusieurs comptes. Voir « [Groupes de comptes](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#bulk-import-and-account-groups) ».

## Espaces de travail existants

Un espace de travail comportant une session ou une configuration antérieure déjà terminée n’affiche pas l’assistant. Ses valeurs ne sont pas remplacées par un objectif lors du chargement de la page. Masquer un champ ne désactive pas la fonctionnalité ni ne supprime sa valeur.

L'estimation de la taille et de la durée porte sur un maximum de trois discussions sélectionnées et jusqu’à 20 messages par discussion. Il s’agit d’une estimation : elle ne tient pas compte des limites imposées par Telegram, de la vitesse d’un serveur donné ni des fichiers présents dans chaque discussion.
