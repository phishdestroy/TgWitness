# Assurez son bon fonctionnement

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/server/

Veillez à ce que le collecteur reste disponible et que ses données restent intactes après chaque redémarrage.

## Choisissez une méthode de lancement

Pour une installation native, utilisez le [lanceur](https://phishdestroy.github.io/TgWitness/fr/docs/start/) et les exemples de service disponibles dans [le répertoire `deploy/`.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Pour Docker, installez Docker avec Compose et exécutez depuis le répertoire du projet :

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Le panneau par défaut écoute sur l'adresse de bouclage de l'hôte, au port 8787. Ouvrez-le localement ou via un tunnel SSH. Utilisez le jeton issu de la deuxième commande pour déverrouiller le panneau.

## Conservez l'intégralité du répertoire de données

Les installations natives utilisent `data/live`. Docker utilise le volume persistant `tgwitness-data`. Conservez ensemble les journaux, les sessions de compte, les clés et l’état opérationnel. Une exportation signée constitue une preuve utile, mais elle ne constitue pas une sauvegarde complète de l’installation.

1. Arrêtez la collecte avant d’effectuer une sauvegarde complète.
2. Copiez l'intégralité du répertoire des données privées vers un espace de stockage sécurisé situé en dehors de l'hôte.
3. Testez la restauration dans un environnement isolé avant de vous fier à la sauvegarde.

## Vérifiez après un redémarrage

Vérifiez l’espace de travail et la clé prévus, la connexion à Telegram, les sources sélectionnées et la capture des nouveaux messages. L’état MTProto enregistré et la fonction de rattrapage permettent de récupérer les mises à jour que Telegram conserve encore. Il n’est toutefois pas possible de reconstituer toutes les mises à jour expirées ni les modifications supprimées avant la capture.

La « santé du conteneur » signifie que le serveur web répond. Utilisez un message contrôlé et une vérification par témoin pour évaluer la collecte et la publication externe.

## Ne publiez que ce que vous souhaitez publier

Le guide de déploiement comprend des exemples HTTPS, des commandes relatives aux volumes persistants, ainsi que les étapes de mise à jour et de restauration. Des commandes Docker sont fournies pour le déploiement ; le [rapport de validation](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/) actuel répertorie les environnements effectivement testés.
