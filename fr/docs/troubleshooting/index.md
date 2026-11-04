# Découvrez ce qui n’a pas fonctionné

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/troubleshooting/

Partez du symptôme, vérifiez une chose à la fois.

## Le panel demande un jeton

Il demande le jeton du panneau depuis le fichier indiqué par le lanceur. Docker : `docker compose exec tgwitness cat /data/panel-token.txt`. Ce n’est ni un code Telegram, ni un jeton de bot, ni celui du témoin.

## Telegram ne se connecte pas

Lancez la vérification de connexion. Avec un proxy public, choisissez-en un autre et enregistrez. Vérifiez le type de proxy et le format du secret. Actualiser les listes ne change pas l’itinéraire tout seul.

## Connecté, mais aucun nouveau message

1. L’observation tourne-t-elle, dans le bon espace ?
2. La source est-elle sélectionnée et visible pour ce compte ?
3. Envoyez un message unique dans votre groupe de test et cherchez-le.
4. Cherchez des interruptions ou des erreurs Telegram dans le journal.

Un chat calme n’a simplement rien de nouveau. Si l’exhaustivité compte, faites un test de livraison contrôlé.

## FloodWait ou un délai après un redémarrage

FloodWait, c’est Telegram qui dit « plus doucement ». Attendez que ça passe et allégez la charge, se reconnecter n’aide pas. Après un redémarrage, TgWitness rattrape ce que Telegram a encore ; le reste est une lacune, notez-la.

## Le bot est configuré mais ne publie rien

Le témoin tourne-t-il, le bot peut-il publier dans le canal, joint-il le collecteur et la Bot API ? Cherchez les publications échouées dans son journal. Une interrogation côté collecteur ne veut pas dire qu’une publication est partie.

## Où se trouve l'intégration du jeton GitHub ?

**En projet.** La section « Extras » décrit le workflow proposé pour la vérification des forks et des builds. Il n’existe actuellement ni formulaire de jeton GitHub ni attestation automatisée garantissant qu’une installation en cours de fonctionnement correspond bien à un dépôt. Consultez l’[état actuel des fonctionnalités](https://phishdestroy.github.io/TgWitness/fr/docs/reference/features/).

Vous signalez un bug ? Version, système, étapes et une erreur sans données personnelles. Ne mettez jamais de sessions, jetons, messages privés ni le dossier de données dans une issue publique.
