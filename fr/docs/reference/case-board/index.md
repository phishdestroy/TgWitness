# Référence « Case Board »

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-board/

Signets, surlignages précis, extraits d’actions, discussions, accès restreint et historique des annotations signées utilisés par Case Board.

Case Board offre à l’équipe d’enquête une vue de travail partagée sur les éléments enregistrés. Ajoutez une observation à vos favoris, surlignez un passage précis, enregistrez une série d’actions et discutez-en avec vos collègues. Les fiches conservent leurs références sources et l’historique des révisions signé. Les annotations de l’équipe restent dans l’ espace de travail, et peuvent être identifiées séparément des observations Telegram d’origine.

[Modèle de preuve](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/) · [Accès](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/) · [Rapports](https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-reports/) · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/CASE-BOARD.md)

![Flux d'enquête synthétique](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

## Travailler sur un dossier

Ouvrez « **Investigation » → « Case Board »** en mode Standard ou Expert. La langue s'adapte à celle du panneau. Utilisez **le** **bouton** **« Ajouter au tableau »** à côté d’une entrée de journal ou d’un message de chat enregistré, ou mettez-le en surbrillance et appuyez sur **B**. Le signet est ajouté à la Boîte de réception en un clic. Modifiez son titre, ses étiquettes et sa note, ou déplacez-le vers une collection. Une carte modifiée est accompagnée d’une révision signée ; sa suppression conserve l’historique.

Pour un premier cas, choisissez une collecte et ajoutez les enregistrements qui répondent à une question. Utilisez les commentaires pour vérifier l’interprétation, puis **l’option « Présentation »** pour parcourir les fiches et le contexte des sources. Sélectionnez séparément le contenu du « Case Board » dans [«](https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-reports/) [Report Studio »](https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-reports/) lors de la préparation du livrable. L’enregistrement d’une « tranche » ne configure pas automatiquement les filtres de données d’un rapport.

Sélectionnez du texte dans un message de discussion enregistré pour faire apparaître « **Mettre en évidence → tableau** ». Choisissez sa couleur et ajoutez une note. Le serveur vérifie la citation exacte et la version enregistrée, y compris les emojis, le texte RTL et les signes de combinaison. L'interface ne fait pas correspondre une sélection à du texte masqué ou transformé.

Cliquez en maintenant la touche Maj enfoncée sur deux enregistrements dans une même conversation pour **effectuer** **une « Slice » entre eux**, utilisez **la « Slice » par période**, ou enregistrez les filtres actuels du Journal concernant la conversation, la période et le type d’événement. Une « Slice » enregistrée dispose de son propre prédicat de référence : son ouverture dans le Journal applique également les filtres relatifs aux conversations multiples, aux limites de nombre de messages et aux acteurs . L’option « **Afficher les enregistrements ajoutés depuis le signet »** isole les ajouts ultérieurs. La modification des filtres de Journal entraîne la fermeture de la tranche. Dans « Personnes », l’option « **Tranche des actions de cette personne »** utilise l’identifiant d’acteur enregistré ; elle ne suppose pas que l’auteur du message ait modifié, supprimé ou réagi à un message.

La boîte de dialogue de sélection affiche un aperçu des comptes avant d’autoriser la création. « `all` » inclut tous les types d’éléments enregistrés, y compris les instantanés, les modifications, les suppressions, les réactions, les mises à jour d’adhésion/de service, les actions personnelles, les boutons, les résultats multimédias, les messages récupérés et les types d’événements futurs. La sélection décrit les observations enregistrées. Les notifications de suppression de discussions inconnues constituent un contexte distinct, accessible uniquement aux utilisateurs disposant d’un accès à l’ensemble de l’espace de travail, et ne sont jamais attribuées à l’une des discussions sélectionnées.

Les collections ont une portée de discussion définie. Une portée vide correspond à l’ensemble de l’espace de travail. Une collection ne peut pas contenir de fiches en dehors de sa portée ; un participant dont l’accès est limité à une discussion ne peut pas consulter une collection plus large. La boîte de réception est une collection virtuelle pour les fiches non attribuées. La recherche et les filtres ne concernent que les cartes visibles ; les fils de discussion et les mentions héritent des droits d’accès de la carte parente. Les commentaires supprimés sont signalés par une « pierre tombale » dans la discussion. Aucun historique de consultation n’est enregistré.

**Le mode « Présentation »** ouvre toutes les fiches de la collection sélectionnée, avec les vues « Fiche », « Contexte de la source » et « Commentaires de l’équipe », ainsi que les commandes « Précédent » et « Suivant » du clavier. Il ne propose aucune commande d’édition. Le flux standard est paginé ; le mode « Présentation » charge sa liste par pages et affiche les détails d’une seule fiche à la fois.

## Autorisations

Toutes les opérations nécessitent l’accès à « `view` », à l’espace de travail/la conversation et à « `board.read` ». « `board.write` » permet d’ajouter des fiches, des commentaires, de déplacer des éléments et de définir les statuts « ouvert » et « en cours de révision ». « `board.manage` » permet la gestion des collectes, les statuts « confirmé » et « rejeté », ainsi que la révision ou la suppression d’une fiche créée par un autre utilisateur. Un statut est une décision prise par l’équipe, et non le résultat d’une vérification cryptographique.

Accès aux préréglages des formulaires : Réviseur = lecture ; Analyste = lecture/écriture ; Opérateur = lecture/écriture/gestion, en plus de leurs autorisations existantes. Les autorisations existantes ne confèrent pas automatiquement de nouveaux droits. L’administrateur principal dispose de tous les droits et publie en tant qu’**administrateur** **principal**. Utilisez des autorisations nommées pour l’attribution. La liste des mentions n’indique que les accès actuels permettant de lire l’intégralité de la fiche parente.

Une autorisation pour la conversation A ne permet pas d’obtenir une carte ou une tranche pour A+B, même en devinant son identifiant ou en fournissant un faux `target.chat_id`. Les métadonnées de la cible sont déterminées à partir du hachage de l’événement signé sur le serveur. Les collectes, le nombre de discussions, les cartes associées et les notifications en temps réel sont filtrés avant la réponse. Les exportations nécessitent à la fois l’autorisation « `export` » et « `board.read` » ; un exportateur existant sans accès au tableau obtient les archives de preuves standard sans les notes de l’équipe. Le SSE vérifie à nouveau les autorisations en vigueur avant chaque lot.

## Contrats archivés

À l’instar des observations, les annotations sont écrites de manière transactionnelle dans une table SQLite en ajout seul (append-only) située dans l’espace de travail. Le fichier `annotations.jsonl` correspond à son exportation canonique exacte à partir du même instantané de lecture que `events.jsonl`. Il n’existe pas de deuxième stockage d’annotations concurrent ni d’événement de journal `board.activity`.

Chaque ligne doit comporter exactement :

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

L’exemple abrégé ci-dessus illustre l’enveloppe ; les charges utiles réelles incluent leurs valeurs par défaut et les champs cibles résolus par le serveur. Les schémas de requêtes API se trouvent dans [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json), générés à partir des modèles Pydantic d’exécution par l’outil `python tools/build_board_schemas.py`. Les champs de requête supplémentaires sont rejetés. Les identifiants sont générés côté serveur lorsqu’ils sont omis. L’auteur, l’heure, l’instantané et la signature ne peuvent pas être fournis par l’appelant. Les identifiants d’autorisation nommés respectent le format hexadécimal à 16 caractères existant d’Access ; les identifiants de carte sont au format hexadécimal à 32 caractères.

Le JSON canonique est au format UTF-8, avec des clés d'objets triées, aucun espace entre les tokens, du Unicode non échappé, et aucune valeur NaN ni infinité. Le hachage de l'annotation est un SHA-256 de l'objet canonique contenant le `format: "tgwitness-annotations-v1"`, ainsi que les sept champs d'enveloppe jusqu'à `previous_hash`. Cette balise de format sépare son domaine de hachage des observations. La signature est une signature Ed25519 sur les 32 octets bruts du hachage. La séquence commence à 1. Les révisions conservent l’ID de la carte et indiquent le hachage de l’annotation précédente dans le champ «`supersedes` » ; elles ne peuvent pas modifier la portée du chat. Les déplacements, les statuts et les suppressions constituent des enregistrements distincts. La table SQLite rejette les commandes UPDATE et DELETE.

`case-board.json` contient `{statement, signature}`. La déclaration canonique est signée par la clé de l'espace de travail et contient `format: "tgwitness-case-board-v1"`, `public_key`, `created_at`, `journal_head`, `meaning` et `state`. L'état est une relecture déterministe : `annotations_head`, un tableau ordonné d'`items` (collections, cartes, commentaires y compris les « tombstones »), et `status_history`. Les éléments conservent le hachage de leur dernière annotation, leur séquence, leur auteur et leur heure, ainsi que le créateur d’origine et l’heure de création à travers les révisions. La relecture vérifie les révisions, les éléments parents, les références de collection et les ID d’action en double. Le fichier « `manifest.json` » et les nouveaux points de contrôle lièrent également « `annotations_head` ». Conservez un point de contrôle de manière indépendante pour détecter toute troncature ou réécriture à l’aide d’une clé de signature copiée.

### Versions texte

`range.start` est un décalage de point de code Unicode à partir de zéro, `length` est un nombre positif de points de code, et `quote` doit correspondre exactement à la sous-chaîne de `payload.text` ou `payload.caption` à l’événement cible. Aucune normalisation NFC/NFKC, aucune conversion de casse ni normalisation des graphèmes n’est appliquée. Les tranches de chaînes Python et la méthode JavaScript ``Array.from(text)`` implémentent le même indexage. La combinaison de marques et d’émojis ZWJ peut occuper plusieurs points de code. ``range.version`` correspond au hachage de l’événement cible, et non à la version actuelle du message ni au décalage d’entité UTF-16 de Telegram. Les modifications ultérieures ne déplacent jamais automatiquement un surlignage.

### Identité et heure de la tranche

La `query` accepte exactement un `chat_id` ou des `chat_ids` non vides, une plage `from`/`to` inclusive facultative, des limites d’ID de message inclusives (un seul chat), des `kinds: "all"` « all » ou des types exacts/avec préfixe générique, des `actors` explicites, `search`, `hide_system` et `include_unscoped`. Les groupes de types de journal se développent en leurs prédicats exacts. La recherche utilise la recherche de charge utile NFC/sans distinction de majuscules-minuscules du journal sans modifier le texte source signé. Les dates nécessitent un fuseau horaire et sont normalisées en UTC. Les dates filtrent « **observed_at** ». Le « `source_at` » de Telegram est affiché séparément. Une suppression sans horodatage source n’a pas d’heure de suppression inventée. Un enregistrement tardif observé en dehors d’un intervalle de temps n’y entre pas ; une tranche d’identifiants de message peut inclure une suppression ultérieure pour ces identifiants de message.

Un « `snapshot` » fixe l’heure de création, la limite de séquence/hachage du journal, le nombre de correspondances, la première et la dernière séquence, ainsi que le « `result_hash` ». Ce dernier correspond au hachage SHA-256 du tableau JSON canonique en UTF-8 des hachages d’événements correspondants triés par ordre lexicographique, y compris `[]` pour une tranche vide. Il contient également le nombre exact de types et une miniature de l’heure d’observation à 24 bins. Une tranche stocke une requête, et non des enregistrements source dupliqués. Lors de l’exportation, le fichier « `board/slices/<id>.json` » répertorie les hachages actuels ainsi que les séquences ajoutées ou supprimées. Le vérificateur reconstitue le résultat d’origine à la limite de création, puis le résultat actuel. Les enregistrements ajoutés sont signalés comme un fait de modification. La suppression d’un événement d’origine rompt la chaîne de preuves immuable ; elle n’est pas acceptée tacitement comme une suppression ordinaire d’une tranche.

Les instantanés de réaction comportent des listes incomplètes d’acteurs récents. L’explorateur compare des instantanés adjacents d’une même conversation/d’un même message, y compris un prédécesseur situé en dehors de la tranche, et signale les écarts de comptage agrégés **entre les observations**. L’absence d’acteurs récents ne signifie pas que ceux-ci ont supprimé une réaction. Le premier instantané ne comporte aucun état antérieur déduit. Les observations des acteurs restent attribuées à l’ instantané dans lequel elles ont été fournies, et non à un moment d’action inventé.

## API et exportations

`GET /api/board` accepte les paramètres collection/chat/author/label/state/from/to/q/kind/comments, offset/limit et l'ordre « le plus récent » / « le plus ancien ». `GET /api/board/card/{id}` renvoie une carte, un aperçu de la source, le fil de discussion, l'historique des statuts et les cartes associées. La sous-route « participants » renvoie les mentions éligibles. `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}` ajoute un enregistrement. `POST /api/board/slice-preview` calcule une requête. Les enregistrements de segment sont paginés via `GET /api/board/slice/{id}/records` ; le recalcul utilise toujours l’instantané de lecture stable actuel. `/api/stream` en temps réel émet des notifications de `board` sans charge utile, indépendamment des curseurs de journal.

La requête `GET /api/board/export` renvoie un document signé. L’accès limité à une conversation donne lieu à une **divulgation** signée clairement identifiée, sans jamais inclure les annotations d’une autre conversation ni la chaîne complète. Les fichiers ZIP contenant l’intégralité des preuves comportent le fichier `annotations.jsonl`, le fichier `case-board.json` signé et des annexes JSON de segments. Les paramètres de rapport HTML/PDF/JSON permettent de choisir entre « aucun tableau », des signets/extraits sans discussion, ou des fiches avec commentaires. La section sépare explicitement les avis de l’équipe des observations. Les filtres de données du rapport restreignent également les notes lisibles ; les fichiers sources complets et signés dans le fichier ZIP de preuves restent intacts.

La requête `GET /api/board/slice/{id}/export` génère un extrait JSON signé « `tgwitness-board-selection-v1` » ; la requête `?format=csv` génère un tableau pratique sans signature indépendante. Conservez les formats JSON et ZIP :

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

Le contrôle de sélection authentifie la déclaration signée, l’exactitude des enregistrements sources et l’exhaustivité de sa requête à la limite spécifiée. Le fichier ZIP contenant les preuves peut être plus récent, mais doit contenir ce préfixe. Une cible non valide est signalée explicitement. Un instantané de tranche d’origine différent, une annotation modifiée, un état de relecture non concordant ou une source modifiée entraînent un échec. Les anciennes archives sans annotations conservent leur comportement de vérification existant.

Le transfert est par défaut réglé sur « **Ne pas inclure** ». L’inclusion explicite projette les fiches à travers les enregistrements déjà minimisés, omet les cibles inaccessibles ou omises, ne divulgue pas les passages mis en évidence dont le texte source a été minimisé, nettoie le texte de l’équipe selon les mêmes règles de mention et de contact, et remplace éventuellement les étiquettes des enquêteurs par R01, R02… dans les métadonnées et les occurrences connues dans les notes. Aucun fichier « `annotations.jsonl` » original n’est divulgué. Le fichier sidecar signé « `tgwitness-case-board-handover-v1` » et le rapport contiennent les mêmes éléments minimisés. Le nombre de tranches ne concerne que les documents divulgués, les détails originaux relatifs aux acteurs des instantanés/requêtes étant masqués. Les noms en texte libre inconnus du minimiseur doivent toujours faire l’objet d’un examen, comme c’est le cas lors des transferts habituels. Ce dérivé ne prétend pas préserver les signatures d’annotation d’origine après expurgation.

## Limites d'utilisation

Les paramètres incluent des limites souples de 10 000 cartes et 50 000 commentaires, une page d’extrait pouvant contenir jusqu’à 5 000 enregistrements, ainsi qu’un contrôle de l’aperçu des médias. Les limites souples déclenchent un avertissement sans supprimer l’historique. Les pages de flux contiennent au maximum 200 fiches. Les extraits JSON autonomes sont plafonnés à 64 Mio ; affinez la requête ou utilisez le fichier ZIP signé pour les volumes plus importants. Le vérificateur autonome limite la relecture des annotations à 256 Mio. Aucune notification de commentaire externe n’est activée ni mise en œuvre par Case Board.

L’acceptation automatisée de la fonctionnalité utilise des données fictives et un transfert Telegram simulé pour vérifier le stockage, l’accès, le rendu et les exportations. Consultez [la section « Portée de la vérification »](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#verification-scope) pour connaître l’étendue des contrôles des éléments de preuve.
