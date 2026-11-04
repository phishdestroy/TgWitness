# Effectuez des recherches dans toutes les discussions

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/cases/

Une affaire complète à travers canaux, groupes, chats privés et bots : collecter, relier les éléments, reconstituer la chronologie, transmettre.

Un incident inventé, du début à la fin. La collecte, la recherche et les profils de personnes trouvent les entrées, [Case Board](https://phishdestroy.github.io/TgWitness/fr/docs/case-board/) les organise, [Report studio](https://phishdestroy.github.io/TgWitness/fr/docs/reports/) les présente.

CAS TRAITÉ / MODIFICATION DE LA DESTINATION D'UN PAIEMENT

### Un incident. Quatre conversations. Une piste à reconstituer.

Une publication de canal renvoie vers un bot. Un groupe parle d’un nouveau lien de paiement et le bot l’affiche. La publication est modifiée, un chat privé répète le lien, un message du groupe disparaît.

Qui a publié chaque version ?Où ce lien est-il apparu ?Quel fichier a été conservé ?Quels changements ont eu lieu, et quand ?

Chargement de l’historique, IA, MCP, OCR et webhooks : [Travailler l’archive](https://phishdestroy.github.io/TgWitness/fr/docs/archive/).

## 1. Assurer une couverture complète de l’ensemble du compte

Périmètre « compte entier » uniquement sur un compte dédié. Un compte principal se limite à des chats choisis ou à un dossier.

1. [Connectez le compte](https://phishdestroy.github.io/TgWitness/fr/docs/accounts/) dans son propre espace. Notez la référence de l’affaire, l’ID du compte, l’espace et l’empreinte de clé.
2. **Sources → Périmètre d’observation → Mode enquête** : **Compte entier**, les quatre types de sources, **Actions propres**. Chaque nouveau chat voit son profil et ses **200 derniers messages visibles** enregistrés. **Enregistrer le périmètre** et confirmez.
3. **Charger les chats** et comparez avec la liste des chats du compte. La limite est de 1 000 dialogues (jusqu’à 20 000 dans **Paramètres → Chats lus depuis la liste du compte**) ; ceux au-delà apparaissent dès qu’ils deviennent actifs.
4. **Paramètres d’enregistrement** → **Toute l’activité visible**, vérifiez les limites de pièces jointes et l’espace disque. Démarrez, puis testez avec un message, une modification et une suppression.

ChaînesGroupesConversations privéesBots

UN COMPTE / UNE CLÉ DE SIGNATURE**Toutes les activités visibles sur le compte sélectionné → un seul journal**

Messages · modifications · notifications de suppression · réactions visibles · événements liés à l'adhésion · actions personnelles

« Compte entier » signifie tous les chats que ce compte peut ouvrir, moins les exclusions. Pas de chats secrets. Les nouveaux chats s’ajoutent à mesure qu’ils apparaissent ; l’ancien historique n’est pas téléchargé automatiquement.

## 2. Récupérer l'historique et conserver les fichiers

Créez une collection Case Board et marquez ce qui compte. Tenez un registre des sources : ID du chat, titre, compte, rôle, début de la capture en direct, résultat de l’historique, résultat des médias, lacunes.

| Besoin | Action dans le panneau | Ce qu’il propose |
| --- | --- | --- |
| Historique des discussions activées | Sources → Charger l'historique complet | Les messages antérieurs disponibles sont enregistrés dans le journal de l’espace de travail, avec des fonctions de pause/reprise et un rapport d’avancement signé. [Guide de l’historique](https://phishdestroy.github.io/TgWitness/fr/docs/reference/history/). |
| Contexte de conversation existant dans le journal | Sources → Paramètres d’enregistrement → Instantané de l’historique | Messages récents sous forme d’entrées signées. 500 par défaut, jusqu’à 10 000 dans **Paramètres → Plus grand instantané d’historique**. |
| Historique complet, tel qu'il est actuellement visible, d'une conversation | Exportation de l'intégralité d'une conversation → Exporter l'intégralité d'une conversation, ou Conversations → Exporter une conversation | Un paquet signé séparé avec `chat.json` et `chat.html`, un par chat. |
| Contexte : lorsqu’une nouvelle conversation apparaît | Périmètre d’observation → Lorsqu’une nouvelle conversation ou un nouveau bot apparaît | Son profil et jusqu’à 1 000 messages récents (200 en mode enquête). Ne s’applique pas aux chats existants. |
| Nombre d'octets de la pièce jointe | Téléchargement des pièces jointes visibles + limites par type | Cherchez `media.saved` avec SHA-256 et taille. En file d’attente, ignoré ou en échec signifie non enregistré. |

Un export de chat n’entre ni dans le journal ni dans les profils de personnes. Pour chercher dans l’ancien historique à l’intérieur de TgWitness, utilisez **Charger tout l’historique** ou des instantanés.

Ici : le canal, le groupe, le chat avec le bot et le chat privé, plus le fichier de la facture et son hachage. Ce qui a été supprimé avant la capture est perdu.

## 3. Suivez l’évolution de la conversation et vos propres actions

Laissez tourner. Marquez d’une étoile les chats chauds comme prioritaires, réglez les revérifications dans **Paramètres d’enregistrement → Revérification** et surveillez `recheck.completed`, FloodWait et les résultats des médias.

**Chats → Profil → Enregistrer le profil maintenant** enregistre la description du chat, les commandes du bot et d’autres métadonnées.

**Suivi d’un bot ou d’une invitation dans le cadre de l’affaire**

1. **Chats → Ouvrir un lien Telegram**, enregistrez d’abord l’aperçu. Le lien et l’aperçu deviennent des entrées signées.
2. Si besoin, **Rejoindre / ouvrir et observer** rejoint le chat ou démarre le bot avec son paramètre de démarrage.
3. Pour documenter une action, répondez ou utilisez **Appuyer sur le bouton** depuis le panneau. Vous obtenez `interaction.requested` et `interaction.result` avec la réponse du bot.

Ce sont de vraies actions. Les boutons pressés dans une autre application ne sont pas visibles, seulement la réponse du bot. Pas d’applications web, de paiements ni de téléphone/localisation.

## 4. Suivez les personnes, les liens et les fichiers dans les discussions

1. **Journal**, **Toutes les sources**, cherchez une phrase, un domaine ou un nom d’utilisateur. Ouvrez les résultats et envoyez-les **Vers le tableau**.
2. **Chats → Personnes → Activer les profils**, choisissez une personne : historique des noms, réponses, activité, **Aussi dans…**, liens, portefeuilles, téléphones. Ouvrez les entrées citées.
3. Suivez le même ID numérique d’utilisateur dans d’autres chats. Un nom, un portefeuille ou un avatar identique est une piste, pas une preuve.
4. Comparez les hachages de fichiers. Même SHA-256 = mêmes octets. Qui les a partagés est une autre question.

CARTE DU DOSSIER / SUIVRE LES RÉFÉRENCESCas fictif · ce graphique n'est pas en temps réel

CHAÎNE / ANNONCE**Texte d'origine → texte révisé**

Enregistrements n° 101, n° 188 Message n° 84 · expéditeur non identifié

GROUPE / OPÉRATIONS**L'utilisateur 71001 publie le nouveau lien**

Enregistrement n° 146 · message n° 309 · Accusé de réception du fichier enregistré n° 151

BOT / CONVERSATION DE COMMANDE**Un bouton renvoie vers cette page**

Enregistrement n° 173 · message n° 12 Métadonnées du bouton « Retour »

PRIVÉ / SUIVI**L'utilisateur 71001 répète la destination**

Enregistrement n° 205 · message n° 922 · Accusé de réception du fichier enregistré n° 209

Quatre discussions apportent des observations différentes. Suivez les enregistrements sources pour chaque connexion ; la publication sur le canal n'a pas d'expéditeur attribué.

Les identifiants numériques et les références d’enregistrements ont été inventés pour ce guide pratique. Ce schéma explicatif montre comment relier les résultats de recherche, les profils et les enregistrements examinés ; « Case Board » stocke les fiches correspondantes et les références des sources.

| Connexion | Remarque complémentaire | Conclusion à conserver |
| --- | --- | --- |
| Même compte Telegram | Identifiant utilisateur 71001 dans le groupe n° 146 et la discussion privée n° 205 | Le même ID d’expéditeur dans les deux chats. Qui c’est dans la vraie vie est une autre question. |
| Destination répétée | `pay.example.invalid/new` dans le n° 146, métadonnées du bouton n° 173, message modifié n° 188 et n° 205 | Le même lien à quatre endroits. Qui le contrôle nécessite d’autres sources. |
| Même nombre d’octets dans le fichier | Valeurs SHA-256 identiques dans les reçus multimédias finalisés n° 151 et n° 209 | Les deux fichiers sont identiques à l’octet près. |

Les profils ne couvrent que les personnes qui ont écrit quelque chose dans *cet espace*, ce n’est pas une liste de membres. Citations par fait : **Paramètres → Entrées citées par fait**.

## 5. Reconstituez la séquence et signalez les lacunes

Versions dans **Chats**, puis **Journal** avec **Toutes les sources** + **Modifications**, **Suppressions**, **Couverture**. Mettez les deux heures dans la chronologie : la date Telegram et le moment de l’observation.

1. 09:00 · #101**Message de la chaîne capturé**

   La destination d'origine est conservée.
2. 09:12 · #146 / #151**Le groupe propose un lien différent**

   L'utilisateur 71001 publie ce message ; le téléchargement d'une pièce jointe est terminé.
3. 09:16 · #173**Le bot affiche la même destination**

   Les métadonnées de clavier enregistrées contiennent le lien.
4. 09:20 · #188**Modifications apportées aux annonces de la chaîne**

   Les observations originales et modifiées sont toutes deux conservées.
5. 09:24 · #205 / #209**Un suivi privé le répète**

   La pièce jointe enregistrée présente le même SHA-256 complet que le n° 151.
6. 09:28 · #231**Une notification de suppression de groupe est reçue**

   L'observation précédente reste valable : ni l'auteur de la suppression ni l'heure exacte de la suppression ne sont indiqués.

Exemples de durées d’observation et de références. D’autres entrées du journal s’intercalent entre celles-ci.

L’ordre du journal est l’ordre d’arrivée, pas forcément l’ordre des événements. Gardez séparés les entrées en direct, instantanés, messages récupérés, suppressions et « introuvable à la revérification », et marquez chaque lacune comme inconnue.

## 6. Étendre le cas à d’autres comptes de collecte

Un espace par compte, mêmes étapes. Notez le rôle et l’empreinte de chacun. Les numéros de message sont propres à chaque compte, alors indiquez toujours l’espace et le chat.

Un [groupe de comptes](https://phishdestroy.github.io/TgWitness/fr/docs/groups/) affiche l’état, partage les paramètres et exporte tout le monde ensemble, chacun avec son journal et sa clé. La chronologie entre comptes, c’est vous qui la construisez dans vos notes.

Affaire longue ? Ajoutez un [témoin indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/witness/) et testez ce que chaque compte capte vraiment.

## 7. Fournir un dossier d’affaire vérifiable

Un ZIP signé de chaque espace (toujours le journal entier, les filtres n’y changent rien), plus les profils de personnes, les exports de chats et les fichiers.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Envoyez les empreintes séparément. Vérifiez chaque élément face à son propre espace :

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Gardez la sortie du vérificateur, les originaux, la couverture et la trace de transmission avec vos conclusions. Rédigez le tout dans Report studio. Si le destinataire a besoin de moins, préparez une [transmission minimisée](https://phishdestroy.github.io/TgWitness/fr/docs/handover/).
