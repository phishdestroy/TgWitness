# Témoin indépendant

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/

Exécutez un instance de TgWitness avec sa propre clé et son propre bot, publiez des points de contrôle signés sur un canal et vérifiez les exportations par rapport à ceux-ci.

[Configuration du bot et du proxy en russe](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

Un collecteur signe son propre journal ; ainsi, toute personne contrôlant le collecteur et sa clé pourrait, en principe, réécrire ou tronquer le journal, puis le signer à nouveau. Un « témoin » rend ce manipulateur détectable. Il s’agit d’un processus distinct — un autre conteneur, ou mieux encore, un serveur géré par une autre personne — qui, toutes les quelques minutes, récupère l’en-tête du journal signé du collecteur, signe ce qu’il a observé avec sa propre clé, le conserve dans son propre journal et le publie sur une chaîne Telegram.

Organigramme · Collector → Witness (point de contrôle signé : nombre d'enregistrements + hachage de tête); Witness → Journal de témoin, clé personnelle; Witness → Chaîne Telegram (Message signé via son propre bot); Fichier ZIP de preuves → verify.py; Journal de témoin, clé personnelle → verify.py; Chaîne Telegram → verify.py (Exportation depuis Telegram Desktop ou page «t.me/s») · Collector · Witness · Journal de témoin, clépersonnelle · Chaîne Telegram · Fichier ZIP de preuves · verify.py · point de contrôle signé : · nombre d'enregistrements + · hachage de tête · Message signé via son propre · bot · Exportation depuis Telegram · Desktop ou page «t.me/s»

**Schéma sous forme de texte**

1. Collector → Witness (point de contrôle signé : nombre d'enregistrements + hachage de tête)
2. Witness → Journal de témoin, clé personnelle
3. Witness → Chaîne Telegram (Message signé via son propre bot)
4. Fichier ZIP de preuves → verify.py
5. Journal de témoin, clé personnelle → verify.py
6. Chaîne Telegram → verify.py (Exportation depuis Telegram Desktop ou page «t.me/s»)

## Ce que TgWitness fournit, et ce qu’il ne fournit pas

| Le témoin a | Le témoin n’a jamais |
| --- | --- |
| Un **jeton « witness »** en lecture seule pour un espace de travail | La session Telegram ou les identifiants API de l’utilisateur |
| Sa propre clé Ed25519 et son propre journal | Le coffre-fort du collecteur, la clé de signature ou le jeton du panneau |
| Son propre jeton de bot Telegram | Contenu du message : l'en-tête comprend le nombre d'enregistrements et un hachage |

Le jeton est créé sur la page **« Witness »** du panneau, affiché une seule fois et stocké uniquement sous forme de SHA-256. Il ouvre exactement un point de terminaison, `GET /api/witness/head`, qui renvoie un point de contrôle fraîchement signé, ainsi que des compteurs de collecte sans contenu signés et des informations sur l’état de fonctionnement. Il ne peut pas ouvrir le panneau, lire le contenu des messages ni modifier les paramètres, et le jeton du panneau n’y est pas accepté. Vous pouvez révoquer un jeton sur cette même page. Le collecteur enregistre le moment où une nouvelle clé de témoin commence à effectuer une vérification (`witness.seen`) et affiche la dernière vérification par jeton ; un témoin qui n’a pas effectué de vérification depuis 2,5 intervalles est marqué comme en retard.

Les nouveaux témoins envoient un défi aléatoire à chaque sondage ; l’instruction de capture le reprend sous la signature du collecteur. Les compteurs sont liés au point de contrôle exact et sont inclus dans les messages signés des témoins. Les en-têtes hérités restent acceptés par le témoin autonome. La croissance du journal à elle seule n’est jamais comptabilisée comme un nouveau message.

## Ce qu’il vérifie et enregistre

À chaque intervalle (10 minutes par défaut), TgWitness :

1. récupère l'en-tête lui-même (le collecteur ne peut ni l'insérer ni le sauter) ;
2. vérifie la signature du collecteur, la clé de collecteur épinglée (`--collector-fingerprint`, ou la première clé rencontrée), un compteur non décroissant et un en-tête inchangé à un compteur inchangé ;
3. ajoute un enregistrement signé à son propre journal : `witness.anchor` avec les statuts `ok`, `key_changed`, `rollback` (moins d’enregistrements qu’auparavant), `fork` (même longueur, en-tête différent ) ou `invalid` (la réponse n’a pas passé la vérification), ou `witness.no_response` lorsque le collecteur n’a pas répondu ;
4. publie le résultat sur le canal, signé, y compris en cas de « pas de réponse » tant que TgWitness est en cours d’exécution et peut accéder à l’API du bot. L’identifiant de la publication est enregistré (`witness.posted`), tout comme une publication ayant échoué (`witness.post_failed`).

Une publication se présente comme suit ; la dernière ligne contient la déclaration signée :

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Lancer un témoin

Vous avez besoin d’un bot Telegram (créez-en un avec @BotFather), d’une chaîne dont ce bot est administrateur, ainsi que de l’adresse du collecteur accessible depuis le témoin — via HTTPS en dehors d’un réseau privé (voir le profil HTTPS dans la section « [Déploiement](https://phishdestroy.github.io/TgWitness/fr/docs/reference/deployment/) »).

Ouvrez **« Extras » → « Un bot dans votre chaîne » → « Configurer un bot »** dans le panneau. Trois étapes permettent de définir l’accès en lecture seule, votre chaîne et l’intervalle, puis de lancer le witness. La politique de publication, le proxy HTTP/SOCKS5 facultatif et l’adresse API personnalisée du bot se trouvent dans **les paramètres avancés** . Le formulaire télécharge le fichier `witness.json` avec la clé de collecte de cet espace de travail épinglée. Téléchargez le jeton en lecture seule nouvellement créé en **enregistrant le fichier d’accès** sous le nom `witness-token.txt` ; placez-le ainsi qu’un fichier `bot-token.txt` créé sur l’hôte du témoin à côté de ce fichier JSON. Le collecteur ne reçoit jamais le jeton du bot. Le téléchargement ne lance pas de service et ne publie pas de message. Aucun témoin de projet hébergé n’est implicitement enregistré.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

La première commande vérifie les fichiers de configuration et les fichiers secrets sans effectuer de requêtes réseau ni créer de clé. Les chemins d’accès indiqués au format JSON sont relatifs à ce fichier ; les chemins d’accès CLI/environnement sont relatifs au répertoire de travail. Conservez l’empreinte digitale du témoin en dehors de son hôte. L’indicateur de dernier sondage du collecteur ne fait que confirmer une requête ; la publication est signalée par Proof ou vérifiée dans le journal et le canal du témoin.

Si le panneau se trouve derrière un tunnel SSH, n’exposez que le point de terminaison « witness » restreint sur un nom d’hôte HTTPS distinct, comme dans [cet exemple Caddy](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). L’espace de travail par défaut utilise alors `https://witness.example.org`, les autres espaces de travail utilisent `https://witness.example.org/profiles/ID`. Des jetons sont toujours requis ; le panneau et ses autres routes API ne sont pas redirigés par cet hôte virtuel.

Choisissez `all` pour des points de contrôle publiés régulièrement. Un intervalle de cinq minutes correspond à environ 288 messages par espace de travail et par jour. `changes` et `problems` laissent délibérément certains points de contrôle non publiés. MTProxy est destiné au client Telegram du collecteur. L’interrogation HTTP de Witness et l’API Bot HTTPS de Telegram utilisent leur propre route directe/HTTP/SOCKS5 ([API Bot](https://core.telegram.org/bots/api)).

**À côté du collecteur, avec Docker** (même hôte — processus et clé indépendants, mais même opérateur) : saisissez les valeurs dans `.env` et lancez le profil.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

Pour toute utilisation d’une image publiée, veuillez indiquer la référence `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**Sur le serveur d’un tiers** (un véritable témoin indépendant) : copiez-y le dépôt, définissez `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` ainsi que les trois valeurs ci-dessus dans `.env`, puis

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

ou sans Docker :

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Options

| Option | Environnement | Par défaut | Signification |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Intervalle entre les vérifications : 1 à 1 440 |
| `--timeout` | `_TIMEOUT` | 30 | Temps d'attente en secondes pour le collecteur et l'API du bot : 5 à 600 |
| `--post` | `_POST` | `all` | `all` : tout est en ordre ; `changes` : un nouveau problème ; `problems` : que des problèmes et des réponses manquantes |
| `--title` | `_TITLE` | `TgWitness witness` | Premiers mots de chaque publication sur un canal |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Enregistrez la clé du collecteur au lieu de vous fier à la première réponse |
| `--proxy` | `_PROXY` | direct | `socks5://host:port` ou `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Adresse de l'API du bot, par exemple un serveur API de bot local |
| `--data-dir` | `_DATA` | `witness-data` | Clé de témoin et journal |
| `--config` | `_CONFIG` | – | Fichier JSON contenant l’une des options ci-dessus |

L’adresse du collecteur, les jetons et le canal proviennent de `--collector`, `--token` ou `--token-file`, `--bot-token` ou `--bot-token-file` et `--channel`, ou encore de `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE` et `_CHANNEL`, ce qui permet de préserver la confidentialité des informations hors de la liste des processus.

Un fichier de configuration utilise les noms d’options avec des traits de soulignement, ainsi que « `texts` », qui remplace les mots des publications de la chaîne :

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Clés `texts` : `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. La ligne de commande prime sur l’environnement, et l’environnement sur le fichier. Les options ou clés de texte inconnues interrompent le journal de preuve par un message au lieu d’être ignorées. La formulation n’affecte jamais la vérification : verify.py vérifie le jeton signé à la fin de chaque publication. Avec `--post changes` ou `problems`, les vérifications qui n’ont pas été publiées figurent toujours dans le journal des témoins et `verify.py` les répertorie comme n’ayant jamais été publiées ; l’enregistrement de début désigne la politique. Chaque vérification apparaît toujours dans le journal ; ainsi, moins de publications signifient moins de transmissions Telegram indépendantes, et non moins de vérifications.

Même en l'absence de chaîne, TgWitness conserve son journal. Conservez l'empreinte de la clé de TgWitness (`python -m tgwitness.witness fingerprint`) dans un autre emplacement.

## Vérifier

Du côté de l’utilisateur, exportez son journal :

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Ensuite, où que vous soyez, à l’aide du fichier ZIP signé du collecteur et du canal exporté depuis Telegram Desktop (*Exporter l’historique de la conversation* → JSON donne `result.json` ) ou de sa page publique `https://t.me/s/…` :

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` vérifie le journal de TgWitness (chaîne et signatures), puis s’assure que **chaque en-tête que le témoin a vu figure bien dans le journal exporté** : l’enregistrement correspondant à ce compteur doit posséder exactement cet hachage. Un en-tête qui ne correspond pas échoue à la vérification — le journal a été modifié après que le témoin l’ait vu. Il signale également les en-têtes consultés après l’exportation, les anomalies que le témoin a enregistrées, les réponses ayant échoué, les périodes dont les points de contrôle correspondants sont présents dans cette exportation (« Témoigné de X à Y ») et les lacunes. Les points de contrôle ultérieurs ne prolongent pas ces périodes. Le résultat inclut le dernier numéro d’enregistrement correspondant et le nombre d’enregistrements suivants sans point de contrôle correspondant. Seules les réponses signées par la clé de l’exportation elle-même sont prises en compte : une exportation signée par une clé que le témoin n’a jamais vue est signalée comme non attestée, et sans `--fingerprint`, son signataire reste non épinglé. Avec « `--channel` », chaque message signé doit correspondre au journal du témoin enregistrement par enregistrement : les messages modifiés échouent à la vérification, les messages manquants sont répertoriés. Une date figurant dans une exportation JSON fournie par Telegram est une métadonnée modifiable, hors du jeton de témoin signé. La correspondance avec le jeton n’authentifie pas la date de publication ; le résultat indique explicitement que la vérification de l’heure de publication n’a pas été effectuée.

### Exiger une limite d’exportation certifiée

Pour un transfert devant inclure un enregistrement final certifié, ajoutez `--require-witness` :

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Cela nécessite l’empreinte de témoin conservée de manière indépendante et un point de contrôle correspondant situé exactement à la fin de cette exportation. Un point de contrôle ne couvrant qu’un préfixe antérieur est insuffisant. Interrompez la collecte, laissez le témoin observer l’état final, puis effectuez l’exportation avant toute nouvelle écriture dans le journal ; si le journal change, conservez un autre point de contrôle et exportez cet état. Un point de contrôle ultérieur ne suffit pas à lui seul à vérifier le hachage final d’une exportation plus courte. Lorsque « `--channel` » est également fourni, des publications déclarées manquantes ou un ensemble de correspondances vide entraînent l’échec de ce contrôle strict. Sans cet indicateur, les contrôles d’intégrité ordinaires signalent toujours les enregistrements non certifiés sans pour autant rejeter une archive par ailleurs intacte.

Ce drapeau garantit la cohérence avec les enregistrements de témoin fournis et épinglés. L’opérateur doit néanmoins s’assurer de l’indépendance du témoin et conserver ses propres enregistrements séparément. Il ne garantit pas la véracité des messages, l’exhaustivité de la collecte ni une durée d’exécution mesurée de manière indépendante.

Un « witness » montre ce que le collecteur a rapporté à ces moments-là et que les exportations ultérieures concordent avec ces données. Il ne montre pas que le collecteur a enregistré tout ce que Telegram a transmis, ni que le contenu des messages est véridique. Un « witness » exécuté par le même opérateur sur la même machine est moins fiable que celui exécuté par une autre personne.

Une simple augmentation du nombre d’entrées ne suffit pas à établir la continuité « en ajout seul » en ligne : la comparaison hors ligne doit faire correspondre chaque hachage de préfixe conservé à l’exportation complète du collecteur. Les périodes d’indisponibilité de Witness et les échecs de publication laissent des intervalles sans repères externes. Les messages manquants peuvent être signalés par rapport à un journal Witness conservé ; ni une chaîne ni un serveur contrôlé par le même opérateur ne constituent une archive tierce immuable.
