# Accès et autorisations

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/

Définissez les droits d’accès aux comptes et aux discussions, choisissez les autorisations, limitez les sessions et les adresses IP, et révoquez les accès.

Accordez à un réviseur l’accès à une conversation, à un analyste l’autorisation d’exporter un dossier, ou à un opérateur le contrôle de comptes sélectionnés. Chaque personne dispose de son propre jeton. Le jeton du panneau principal reste entre les mains de l’administrateur.

[Configuration du compte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/) · [Itinéraires de connexion](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/) · [Modèle de sécurité](https://phishdestroy.github.io/TgWitness/fr/docs/reference/security/)

## Deux domaines d’application, deux missions distinctes

**La portée de la collecte** détermine ce qu’un compte enregistre : des discussions sélectionnées, un dossier Telegram ou l’intégralité du compte. **La portée d’accès** détermine lesquels de ces comptes et discussions enregistrés une autre personne peut consulter et utiliser. Accorder l’accès ne revient pas à rejoindre une discussion Telegram, à lancer la collecte ni à octroyer des autorisations sur le compte Telegram.

Un accès peut permettre d’ouvrir des espaces de travail sélectionnés, des discussions sélectionnées au sein de ceux-ci, ou tous les espaces de travail. L’option « **Tous les espaces de travail », y compris ceux ajoutés ultérieurement,** couvre également les futurs comptes. Sélectionnez explicitement les espaces de travail lorsque vous souhaitez qu’une affaire se limite à ceux-ci.

## Accorder un accès à quelqu’un

1. Connectez-vous en tant qu’administrateur principal et ouvrez la rubrique « **Accès** ».
2. Sous « **Accorder l'accès à quelqu'un** », saisissez un nom que vous pourrez reconnaître dans le journal.
3. Sélectionnez les espaces de travail et, si nécessaire, les discussions individuelles.
4. Sélectionnez ce que cette personne est susceptible de faire. La mention « **Afficher »** est toujours incluse.
5. Définissez la durée de validité, les limites de connexion/de session et les adresses autorisées selon vos besoins.
6. Cliquez sur « **Créer un accès** ». Copiez le jeton dès maintenant : il ne s'affiche qu'une seule fois.
7. Envoyez l'adresse du panneau et le jeton en privé. Le destinataire saisit ce jeton sur la page de connexion habituelle ; il n'a pas besoin de votre jeton principal ni d'une session Telegram.

Ouvrez le panneau contenant le jeton généré dans une session de navigateur distincte et vérifiez les discussions visibles ainsi que les actions autorisées avant de le transmettre.

## Choisissez les autorisations

| Autorisation | Ce qu’il permet |
| --- | --- |
| `view` | Consultez les discussions autorisées, les messages capturés, les profils, les fichiers et les entrées filtrées du journal. Toujours inclus. |
| `export` | Exportation autorisée de l’historique des discussions et des dossiers. L’exportation des preuves de l’ensemble de l’espace de travail nécessite un accès à l’intégralité de celui-ci. |
| `sources` | Gérez les sources, les instantanés et la capture de profils. L’accès limité aux discussions ne peut s’appliquer qu’aux discussions autorisées ; la détection des sources à l’échelle du compte et les paramètres de portée restent désactivés. |
| `collect` | Démarrer ou arrêter un collecteur. Nécessite un accès à l'ensemble de l'espace de travail, car la collecte a une incidence sur le compte. |
| `interact` | Effectuez les interactions Telegram prises en charge dans les limites de votre périmètre d’accès. L’accès limité au chat ne permet pas d’utiliser les aperçus de liens à l’échelle du compte. |
| `settings` | Modifiez les paramètres de collecte, les horodatages, les notifications, les copies hors site et les paramètres. Nécessite un accès à l'ensemble de l'espace de travail. |
| `account` | Connectez-vous ou déconnectez-vous de Telegram et gérez les itinéraires de connexion. Nécessite un accès à l'ensemble de l'espace de travail. |

Les autorisations et leur portée sont vérifiées conjointement. Cocher une autorisation n’ouvre pas d’autres discussions ni ne débloque une opération à l’échelle de l’espace de travail pour un accès limité à une discussion. Pour une exportation parallèle, l’accès doit couvrir la conversation exportée dans chaque compte sélectionné. Un accès accordé ne permet pas de créer de nouveaux accès, de gérer les sessions d’autres personnes ni d’ouvrir la console d’administration.

### Trois configurations utiles

| Personne | Portée | Autorisations |
| --- | --- | --- |
| Réviseur | Conversations enregistrées dans le cadre d’une affaire | `view` |
| Analyste préparant un transfert de mission | Les conversations à examiner et à exporter | `view`, `export` ; n'ajoutez `interact` que s'ils doivent agir via Telegram |
| Opérateur de collecte | Espaces de travail complets sélectionnés | `view`, `sources`, `collect` ; n'ajoutez `settings` ou `account` qu'en cas de besoin |

Il s'agit d'exemples que vous configurez à l'aide des cases à cocher d'autorisation, et non de rôles fixes.

## Limites et sessions

| Contexte | Fonctionnement |
| --- | --- |
| Sessions parallèles | Limitez le nombre de sessions simultanées à 1–100. Lorsque cette limite est atteinte, refusez la connexion suivante ou mettez fin à la session la plus ancienne. |
| Connexions autorisées | Limitez le nombre d’utilisations réussies du jeton pour démarrer des sessions. Les sessions existantes ne sont pas interrompues simplement parce que la dernière connexion autorisée a été utilisée. |
| Valable jusqu’au | Expiration définitive de l’accès. Un accès expiré ne permet plus de se connecter ni de continuer à effectuer des requêtes. |
| Minutes sans activité | Délai d’inactivité de la session, de 5 minutes à 30 jours. Les requêtes abouties le prolongent ; un panneau ouvert peut rester actif grâce à un interrogateur. |
| Adresses autorisées | Acceptez des adresses IP spécifiques ou des sous-réseaux CIDR. Laissez ce champ vide pour autoriser toutes les adresses, sauf si la liaison à la première connexion est activée. |
| Se connecter lors de la première connexion | La première connexion réussie enregistre l’adresse autorisée pour cet accès. |

L'adresse IP correspond à l'adresse du client telle qu'elle est perçue par l'application. Si vous vous trouvez derrière un proxy inverse ou un tunnel, vérifiez l'adresse indiquée dans la section « **Sessions ouvertes »** avant de vous fier aux règles basées sur l'adresse IP : sinon, plusieurs utilisateurs pourraient sembler partager l'adresse du proxy.

## Modifier ou retirer l'accès

Modifiez une entrée sous **« Accès »** pour modifier sa portée, ses autorisations ou ses limites. Les modifications de portée et d’autorisations sont vérifiées lors des requêtes suivantes, y compris les requêtes provenant de sessions déjà ouvertes. La révocation d’un accès met fin à ses sessions et rend le jeton émis inutilisable. La gestion **des sessions ouvertes** permet également à l’administrateur de mettre fin à une session individuelle sans révoquer l’accès dans son intégralité.

La révocation ne permet pas de récupérer les fichiers qu’une personne a déjà téléchargés. Se déconnecter, verrouiller le panneau ou mettre fin à une session n’arrête pas un collecteur en cours d’exécution.

## Ce que l'administrateur peut voir

**Depuis son lancement, ce journal** combine les journaux de processus avec l’activité de chaque espace de travail : connexions, refus, changements d’itinéraire et actions de l’opérateur. Il s’agit d’une console en mémoire pour le processus en cours, et non d’une copie permanente de chaque message. Les événements fréquents liés aux messages sont conservés dans le journal plutôt que d’encombrer la console.

L'octroi, la modification et la révocation d'accès, ainsi que le démarrage ou la fin de sessions, génèrent également des enregistrements signés dans le journal `access.*`. Les jetons ne figurent pas dans ces enregistrements. Les jetons émis et les identifiants de session sont conservés sous forme de hachages dans le coffre-fort chiffré.

****Administrateur principal et périmètre de confiance**** Le jeton du panneau principal reste sans restriction. Les connexions via un navigateur à l’aide de ce jeton créent des sessions soumises aux limites de session configurées par l’administrateur. Les scripts envoyant le jeton principal directement conservent un accès complet et ne sont pas comptabilisés comme des sessions de navigateur. Il s’agit d’un contrôle d’accès au niveau de l’application au sein d’une même installation. Tous les espaces de travail partagent le processus serveur ; il ne s’agit pas d’une isolation vis-à-vis de l’administrateur de l’hôte. Veillez à préserver la confidentialité du jeton principal, des sessions Telegram, des clés de signature et du répertoire de données. Un jeton « witness » est un identifiant distinct de vérification de l’état de santé du système, et non un jeton d’accès au panneau de contrôle.
