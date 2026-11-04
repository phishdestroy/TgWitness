# Assurez son bon fonctionnement

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/server/

Gardez le collecteur en marche et les données à l’abri au fil des redémarrages.

## Choisissez une méthode de lancement

Natif : le [lanceur](https://phishdestroy.github.io/TgWitness/fr/docs/start/) plus les modèles de service dans [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, depuis le dossier du projet :

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Le panneau écoute sur localhost:8787. Ouvrez-le en local ou via un tunnel SSH, avec le jeton de la deuxième commande.

## Conservez l'intégralité du répertoire de données

Natif : `data/live`. Docker : le volume `tgwitness-data`. Journaux, sessions et clés vont ensemble. Un export signé est une preuve, pas une sauvegarde.

1. Arrêtez d’abord la collecte.
2. Copiez tout le dossier de données en lieu sûr, hors de l’hôte.
3. Essayez de le restaurer sur une installation séparée avant de vous y fier.

## Vérifiez après un redémarrage

Vérifiez l’espace et la clé, la connexion, les sources et l’arrivée des nouveaux messages. TgWitness rattrape ce que Telegram garde encore, pas tout ce qui s’est passé pendant l’arrêt.

Un conteneur « sain » signifie que le serveur web répond. Si la collecte fonctionne, un message de test et le témoin vous le diront.

## Ne publiez que ce que vous souhaitez publier

HTTPS, volumes, mises à jour et restauration sont dans la référence de déploiement. Ce qui a vraiment été testé : [registre de validation](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/).
