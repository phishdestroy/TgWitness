# Telegram · Configurer un bot TgWitness

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/witness/

Un processus séparé vérifie votre journal et publie des points de contrôle signés dans un canal.

## Deux serveurs, deux clés de signature

HÉBERGER UN / COLLECTEUR**Compte + journal**

Clé de signature du collecteur de sessions Telegram

Point de contrôle en lecture seule

← Demander une réponse signée →

HÔTE B / TÉMOIN**Vérifier + conserver**

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

Créez un bot avec BotFather et laissez-le publier dans votre canal. Faites tourner le témoin ailleurs : un autre hôte, idéalement géré par quelqu’un d’autre, vaut bien plus qu’un second processus à côté du collecteur.

## Trois étapes dans la rubrique « Extras »

1. **Accès en lecture seule.** **Extras → Témoin indépendant**, créez un jeton et enregistrez le fichier. Il lit les points de contrôle et l’état, rien d’autre.
2. **Canal et intervalle.** Canal Telegram ou webhook Discord, plus une adresse du collecteur joignable par le témoin. Enregistrez le fichier de réglages.
3. **Lancement.** Placez `witness.json`, `witness-token.txt` et `bot-token.txt` ensemble sur l’hôte du témoin et lancez :

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Attendez la première publication signée dans le canal, puis conservez l’empreinte du témoin en lieu sûr.

Plutôt Discord ? Enregistrez l’URL du webhook dans `discord-webhook.txt`. Un témoin publie à un seul endroit ; sur Discord, les longues vérifications arrivent sous forme de fichier.

## Choisissez la fréquence de publication

Publier chaque vérification crée une trace externe régulière : toutes les cinq minutes, cela fait environ 288 publications par jour et par espace. Les réglages avancés permettent de publier seulement en cas de changement ou de problème, d’utiliser un proxy ou une Bot API personnalisée.

**Que certifie réellement ce bot ?**

Il demande au collecteur un point de contrôle signé, le vérifie avec la clé attendue et tient son propre journal signé, y compris les réponses manquées et rejetées.

Il vérifie l’état du journal ; il n’observe pas Telegram lui-même. Pour cela, faites un test de livraison contrôlé.

## Vérifiez les preuves ultérieurement

Conservez le journal du témoin, les publications et les empreintes. [Comment les vérifier](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/#verify) face à l’export du collecteur.
