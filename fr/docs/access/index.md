# Partager un cas

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/access/

Partagez les informations dont quelqu’un a besoin. Gardez le contrôle sur le reste.

01**Choisissez les preuves**

Sélectionnez l’ensemble des espaces de travail d’un compte ou des discussions enregistrées individuellement.

02**Choisissez les actions**

Autorisez la consultation, l'exportation ou les autorisations opérationnelles spécifiques dont la personne a besoin.

03**Définir les limites**

Émettez un jeton personnel avec une date d’expiration, des limites de session et des restrictions d’adresse IP facultatives.

Le périmètre de collecte détermine ce qui est enregistré. Le périmètre d’accès détermine ce qu’une personne peut voir et faire.

## Accorder un accès à quelqu’un

1. Connectez-vous en tant qu’administrateur et ouvrez la rubrique « **Accès** ».
2. Indiquez le nom d’accès et sélectionnez les espaces de travail et les discussions.
3. Conservez **l’option « Afficher »** pour un réviseur. Ajoutez **l’option « Exporter »** s’il doit télécharger les enregistrements.
4. Définissez les limites, puis cliquez sur « **Créer un accès** ».
5. Copiez une seule fois le jeton affiché. Envoyez-le en privé avec l'adresse du panneau.
6. Vérifiez l’affichage autorisé dans une session de navigateur distincte avant de le transmettre.

## Commencez par la mission qu’ils doivent accomplir

| Personne | Accès | Résultat |
| --- | --- | --- |
| Réviseur | Discussions sélectionnées ; consultation uniquement | Lisez la conversation capturée sans modifier la collecte. |
| Analyste | Discussions sélectionnées ; consultation et exportation | Consultez et téléchargez les enregistrements nécessaires à l’affaire. |
| Opérateur | Espaces de travail complets sélectionnés ; sources et collecte | Gérez les données collectées et lancez ou arrêtez les collecteurs. |

Il s’agit de configurations que vous choisissez, et non de rôles fixes. Les paramètres applicables à l’ensemble du compte et les exportations complètes du journal restent inaccessibles aux utilisateurs dont l’accès est limité aux discussions, même lorsqu’une autre autorisation est activée. L’accès à l’ensemble de l’espace de travail inclut les futurs comptes.

## Vous pouvez changer d'avis à tout moment

Modifiez les droits d’accès pour définir les actions autorisées lors des requêtes suivantes. Mettez fin à une session ou révoquez l’ensemble des droits d’accès pour mettre fin à toutes les sessions. Les fichiers déjà téléchargés ne peuvent pas être récupérés. La fermeture d’une session du panneau n’interrompt pas la collecte.

**Limites de sessions et d'adresses IP**

Limitez le nombre de sessions parallèles et de connexions réussies, définissez une date de fin absolue, autorisez des adresses IP ou des sous-réseaux, ou liez l’accès à l’adresse utilisée lors de la première connexion. L’expiration de la session est déterminée par l’inactivité ; le rafraîchissement d’un panneau ouvert est considéré comme une activité. Vérifiez l’adresse du client affichée par l’application lorsqu’elle s’exécute derrière un proxy ou un tunnel.

**La clé principale et le journal d'activité**

L’administrateur conserve le jeton du panneau principal. Les utilisateurs disposant d’un accès ne peuvent pas gérer les accès d’autres personnes ni ouvrir la console d’administration. La console affiche l’activité des processus en cours dans tous les espaces de travail ; les enregistrements d’accès signés conservent les événements d’autorisation et de session sans jetons. Les espaces de travail partagent le processus hôte et n’isolent pas les données de l’administrateur du serveur.

Utilisez la [référence complète des autorisations](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) pour les sept autorisations, les règles de session et les limites de l'administrateur.
