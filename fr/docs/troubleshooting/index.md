# Découvrez ce qui n’a pas fonctionné

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/troubleshooting/

Commencez par le symptôme. Vérifiez une couche à la fois.

## Le panel demande un jeton

Utilisez le jeton du panneau figurant dans le fichier local affiché par le lanceur. Pour Docker, exécutez « `docker compose exec tgwitness cat /data/panel-token.txt` ». Un code de connexion Telegram, un jeton BotFather et un jeton « witness » en lecture seule ont des finalités différentes.

## Telegram ne se connecte pas

Ouvrez les paramètres de connexion et lancez le test de connexion. Si vous utilisez un proxy public, essayez une autre entrée et enregistrez explicitement le chemin d’accès. Vérifiez le type de proxy et le format de clé pris en charge. L’actualisation d’une liste publique ne modifie pas le chemin d’accès du compte.

## Connecté, mais aucun nouveau message

1. Vérifiez que l’observation s’exécute dans l’espace de travail approprié.
2. Vérifiez que la source est sélectionnée et visible pour ce compte.
3. Envoyez un nouveau message unique dans un groupe contrôlé et recherchez ce texte exact.
4. Consultez le journal opérationnel pour identifier les interruptions, les retards de traitement ou les erreurs de Telegram.

Les instantanés historiques et les événements liés à l’arrivée de nouveaux messages sont deux choses distinctes. Une source silencieuse peut être connectée sans générer de nouveaux messages. Recourez à un test de livraison contrôlée lorsque l’exhaustivité est primordiale.

## FloodWait ou un délai après un redémarrage

« FloodWait » signifie que Telegram nécessite une pause. Attendez la durée indiquée et vérifiez la charge de travail liée à la collecte ; les reconnexions répétées ne suppriment pas la limite. L’état des mises à jour enregistrées permet de rattraper le retard après un redémarrage, mais les mises à jour périmées et certaines fenêtres d’interruption restent des contraintes. Enregistrez l’intervalle manquant plutôt que de considérer le journal comme complet.

## Le bot est configuré mais ne publie rien

Assurez-vous que le processus « witness » est bien en cours d’exécution, que le bot peut publier dans le canal et que le « witness » peut accéder au collecteur et à l’API du bot. Vérifiez son journal pour détecter d’éventuelles publications ayant échoué. Une interrogation réussie du collecteur ne suffit pas à elle seule à confirmer la publication d’un message dans le canal.

## Où se trouve l'intégration du jeton GitHub ?

**En projet.** La section « Extras » décrit le workflow proposé pour la vérification des forks et des builds. Il n’existe actuellement ni formulaire de jeton GitHub ni attestation automatisée garantissant qu’une installation en cours de fonctionnement correspond bien à un dépôt. Consultez l’[état actuel des fonctionnalités](https://phishdestroy.github.io/TgWitness/fr/docs/reference/features/).

Lorsque vous signalez un problème, veuillez indiquer la version, le système d'exploitation, la marche à suivre et une description expurgée de l'erreur. Ne mentionnez pas les sessions, les jetons, les messages privés ni le répertoire de données dans les tickets publics.
