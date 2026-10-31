# Configurer un bot TgWitness

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/witness/

Laissez un processus distinct vérifier le journal et publier des points de contrôle signés sur votre chaîne.

## Deux serveurs, deux clés de signature

HÉBERGER UN / COLLECTEUR**Compte + journal**

Clé de signature du collecteur de sessions Telegram

Point de contrôle en lecture seule

← Demander une réponse signée →

HOST B / WITNESS**Vérifier + conserver**

Empreinte digitale du collecteur épinglée Clé de signature distincte du témoin

Journal personnel + jeton de bot

Witness → API du bot Telegram →**Votre chaîne · publications TGW1 signées**

Le « witness » effectue lui-même les vérifications. L’accès du collecteur est en lecture seule. La publication par le bot utilise la connexion et le jeton du « witness » ; aucune session de compte n’est attribuée au « witness ».

03 / DÉCISIONS RELATIVES AUX POINTS DE CONTRÔLEExemples de réponses

DERNIÈRE VERSION ACCEPTÉE**120 entrées**`head 9c7d…`

RÉPONSE SUIVANTE**128 entrées**`head a4f2…`

Accepté : le décompte augmente, la signature est vérifiée et la clé correspond. Le témoin conserve cette nouvelle limite.

Tous les exemples de réponse partent du principe qu’une signature valide et la clé épinglée sont disponibles. Les hachages présentés ici sont des illustrations abrégées. Un nombre plus élevé ne suffit pas à lui seul à prouver que l’intégralité de l’ancien préfixe est inchangée ; comparez une exportation avec les points de contrôle conservés.

## Préparez un bot et une chaîne

Créez un bot à l’aide de BotFather et autorisez-le à publier dans un canal que vous contrôlez. Choisissez un ordinateur ou un serveur pour le « witness ». Un hébergeur et un opérateur distincts garantissent une plus grande indépendance qu’un deuxième processus sur le serveur du collecteur.

## Trois étapes dans la rubrique « Extras »

1. **Accès en lecture seule.** Ouvrez « **Extras » → Un bot dans votre chaîne**, créez un jeton de témoin et enregistrez le fichier d’accès. Cela permet de consulter les points de contrôle et l’état de santé du système, mais pas les conversations ni les commandes du collecteur.
2. **Canal et intervalle.** Saisissez le canal et une adresse de collecteur accessible depuis le témoin. Enregistrez le fichier de paramètres.
3. **Lancement.** Placez ensemble les fichiers `witness.json`, `witness-token.txt` et `bot-token.txt` créés sur l’hôte « witness ». Exécutez les commandes ci-dessous dans l’environnement du projet installé.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Le téléchargement des fichiers ne lance pas le « witness ». Vérifiez que le premier message signé apparaît bien dans la chaîne, puis conservez séparément l’empreinte de la clé publique du « witness ».

## Choisissez la fréquence de publication

La publication de chaque vérification crée un enregistrement externe régulier. À raison d’intervalles de cinq minutes, cela représente environ 288 publications par espace de travail et par jour. Les paramètres avancés permettent également de publier les modifications ou les problèmes, d’utiliser un proxy et de définir une adresse API de bot personnalisée.

**Que certifie réellement ce bot ?**

Le témoin demande au collecteur un point de contrôle signé, le vérifie par rapport à la clé attendue et tient un journal signé distinct. Il enregistre les réponses manquantes et les réponses rejetées, ainsi que les vérifications réussies. La publication dépend toujours du fonctionnement du témoin et de sa capacité à accéder à l’API Bot de Telegram.

Il vérifie l’état du journal tel que signalé par le collecteur. Il n’observe pas de manière indépendante chaque message Telegram. Pour cela, veuillez ajouter le test de livraison contrôlée.

## Vérifiez les preuves ultérieurement

Conservez le journal des témoins, les publications des chaînes et les empreintes enregistrées de manière indépendante. La [procédure de vérification complète](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/#verify) les compare à l’exportation signée par l’utilisateur.
