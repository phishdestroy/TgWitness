# Format des preuves

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/

Contenu du fichier ZIP signé, types d’enregistrements, accusés de réception, profils des utilisateurs, copies hors site et vérification hors ligne.

Une observation n’est pas une conclusion. Un identifiant d’expéditeur n’est pas une identité dans le monde réel. La mise à jour du service visible sur le compte constitue la source ; Telegram ne signe pas cryptographiquement ces enregistrements sauvegardés à l’intention d’un enquêteur tiers.

## Qu'est-ce qui est signé ?

| Contenu | Protection | Éléments à conserver |
| --- | --- | --- |
| Chaque observation du journal, y compris les événements opérationnels | Chaîne SHA-256 et signature Ed25519 par événement | `events.jsonl` d'origine, l'empreinte de la clé de confiance, et un point de contrôle conservé |
| Contenu du fichier ZIP de preuves | `manifest.sig` signe le manifeste canonique, qui répertorie les hachages des fichiers de contenu | Le fichier ZIP complet, comprenant son manifeste et sa signature |
| Pièces jointes conservées | SHA-256 et nombre d’octets dans un événement `media.saved` signé ; hachage du fichier dans le manifeste ZIP signé | Les octets d'origine contenus dans le fichier ZIP vérifié |
| Checkpoint | Signature Ed25519 portant sur la longueur du journal, le hachage d'en-tête, la clé publique et l'heure de création | Une copie indépendante conservée avant une modification contestée |
| Reçu de transaction | Mesures du collecteur signées séparément ; également incluses dans un événement signé « `process.started` » | Le relevé et le journal associé ; les mesures sont déclarées par les utilisateurs eux-mêmes. |
| Fichier CSV ou HTML autonome | Pas de signature cryptographique autonome ; les hachages d’événements seuls ne suffisent pas | Utilisez le fichier exact contenu dans l'archive ZIP vérifiée pour contrôler l'intégrité. |
| Captures d’écran, impressions ou fichiers PDF générés par un navigateur | Aucune signature TgWitness sur le document dérivé | Conservez le paquet original vérifié et documentez la manière dont le dérivé a été créé. |

Le collecteur vérifie les signatures du journal avant de générer chaque format d’exportation. Cette vérification à la source ne crée pas de signature sur un fichier CSV ou HTML téléchargé séparément. De même, une signature d’événement JSONL valide ne fournit pas les octets de la pièce jointe ni ne prouve de manière indépendante que l’intégralité du journal observé a été fournie.

## Transfert de l'enquête

1. Consignez la référence du dossier, le nom de l’opérateur, l’identifiant numérique du compte Telegram, les sources sélectionnées, la politique de collecte et la période de collecte dans vos notes de dossier. TgWitness conserve les observations ; l’attribution des dossiers et les registres de conservation sont gérés en dehors de l’application. Validez la configuration de collecte prévue à l’aide de la [procédure d’acceptation en temps réel](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
2. Conservez l'empreinte de la clé publique de l'espace de travail de manière indépendante avant de vous fier à ses exportations. Enregistrez les points de contrôle signés en dehors du collecteur pendant la collecte. Consignez les interruptions et les limites de visibilité du compte.
3. Exportez un fichier **ZIP signé** et conservez le reçu d’exécution signé. Utilisez un point de contrôle situé au niveau ou avant la limite du journal exporté. Un point de contrôle situé plus loin dans le journal peut rejeter à juste titre une exportation antérieure en la jugeant trop courte. Les exportations incluent l’intégralité du journal de l’espace de travail, indépendamment des filtres des panneaux ; veuillez examiner le contenu avant de le partager.
4. Demandez au destinataire de vérifier le fichier ZIP à l’aide d’une copie fiable du vérificateur et de l’ empreinte numérique/point de contrôle fourni séparément. À partir d’un environnement de développement fiable avec son environnement Python actif :

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   La sortie renvoie les codes « `key_pinned: true` » et « `checkpoint_checked: true` » lorsque les deux entrées sont fournies et acceptées. Conservez le résultat de la vérification.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Enregistrez la valeur SHA-256 de l’archive, la limite d’exportation, la date de transfert, l’expéditeur et le destinataire dans votre registre de conservation. Conservez le paquet d’origine intact et travaillez à partir de copies. Partagez les fichiers de preuves plutôt que le répertoire de données privées de l’application, qui contient également les sessions de compte et les secrets de signature. Pour le transfert, une exportation peut être placée dans un fichier ZIP AES-256 protégé par mot de passe. Le mot de passe protège uniquement la confidentialité et n’est pas stocké ; le destinataire extrait l’archive et vérifie que l’exportation signée qu’elle contient est inchangée.
   2. Si un ancrage temporel indépendant est nécessaire, suivez la [procédure de la RFC 3161](https://phishdestroy.github.io/TgWitness/fr/docs/reference/timestamp/) et conservez la requête, le point de contrôle, les informations relatives à l’autorité de certification (CA) de confiance, ainsi que la réponse vérifiée de l’autorité. Le simple fait de préparer une requête ne permet pas d’obtenir un horodatage.

Une vérification réussie établit l’intégrité par rapport à la clé de collecte de confiance et aux limites définies. La véracité de la source, la transmission complète des messages Telegram, l’horodatage fiable et l’admissibilité juridique nécessitent des preuves distinctes. Cette version n’a pas encore fait l’objet d’une qualification en conditions réelles sur Telegram ni d’une évaluation indépendante en matière de criminalistique ou de sécurité.

Une clé de collecte copiée peut signer un journal de remplacement falsifié. La vérification par rapport à un point de contrôle ou un enregistrement témoin conservé de manière indépendante permet de détecter un préfixe antérieur modifié ; la vérification de la signature seule ne le permet pas. Un témoin valide ce que le collecteur a présenté ; il ne permet donc pas d’établir de manière indépendante la véracité des enregistrements fabriqués avant leur premier point de contrôle externe. Les rapports de déploiement sur le cloud vérifient la configuration et les mesures communiquées par le collecteur ; ils ne permettent pas d’établir qu’une clé privée n’a jamais été copiée lors de la phase de démarrage.

Les notifications envoyées via Apprise contiennent les noms et le nombre d’espaces de travail et de discussions ; de courts extraits des messages supprimés et modifiés ne sont ajoutés que lorsque l’opérateur active cette fonctionnalité (désactivée par défaut). Il s’agit d’un signal pratique, et non d’une preuve : la livraison n’est pas garantie, et seuls le journal et ses exportations signées consignent ce qui a été observé. Avec un proxy d’espace de travail, les notifications empruntent le même chemin ; les services qui ne peuvent pas l’utiliser, ainsi que les routes MTProxy, sont refusés.

## Canonisation des événements

L'entrée de hachage se compose exactement des champs suivants :

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Sérialisation au format JSON compatible Python avec UTF-8, clés d’objets triées, sans échappement ASCII, sans espaces insignifiants et sans NaN/infini :

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

Le SHA-256 de ces octets constitue le hachage de l’événement. La signature est générée à l’aide de l’algorithme Ed25519 sur les 32 octets bruts du hachage, puis encodée en base64. Le premier « previous_hash » est constitué de 64 zéros. Les numéros de séquence commencent à 1 et augmentent de 1. Tous les événements, y compris les événements opérationnels, partagent une seule chaîne. Il n’y a pas de suppression des doublons : les observations répétées constituent des reçus distincts, et non une affirmation d’actions distinctes sur Telegram.

Les dates brutes de Telegram sont des chaînes ISO ; les champs binaires deviennent des objets contenant des « bytes_base64 ». Le texte des messages, les entités, les descripteurs multimédias, les métadonnées de réponse, les réactions et les actions de service sont conservés dans les métadonnées brutes des messages lorsqu’ils sont fournis.

« observed_at » correspond à l’heure UTC du collecteur. « source_at » correspond à la date fournie par Telegram, lorsqu’elle est disponible. Les notifications de suppression ne fournissent pas d’heure exacte de suppression ; par conséquent, « source_at » reste nul. L’ordre de réception des données n’est pas nécessairement le même que l’ordre chronologique des événements à la source. Les instantanés de l’historique utilisent des dates de source plus anciennes, mais des heures d’observation actuelles.

## Sémantique des acteurs

message.new : actor_id correspond à l’expéditeur du message. message.edited ne comporte aucune inférence quant à l’auteur de la modification ; payload.sender_id enregistre l’expéditeur du message observé. Suppression L’`actor_id` reste nul. Les messages du service d’adhésion conservent l’expéditeur et le type d’action, sans considérer chaque suppression comme un départ volontaire. Les mises à jour brutes des participants conservent l’`actor_id` tel qu’il a été fourni. Les instantanés de réaction n’inventent pas d’acteur de modification.

Les notifications de suppression pour les discussions privées et les groupes ordinaires ne contiennent que les identifiants de message. Ces discussions partagent une séquence d’identifiants unique à l’échelle du compte ; ainsi, un identifiant identifie un message unique de ce compte. Lorsqu’un message portant cet identifiant a été enregistré précédemment dans ce journal, la suppression est consignée dans cette conversation sous la forme message.deleted, avec payload.chat_resolution comme nom de la méthode. Les identifiants qui n’ont jamais été enregistrés sont conservés sous la forme deletion.unscoped, sans chat_id ; aucune supposition n’est faite. Les canaux et les supergroupes numérotent les messages par discussion et ne sont jamais mis en correspondance de cette manière. Lorsque le message supprimé a été envoyé par le compte observé, payload.deleted_message_was_outgoing est vrai ; l’auteur de la suppression n’est toujours pas indiqué.

## Portée : continuité, lacunes et identifiants non observés

Chaque fichier ZIP signé porte la référence « `coverage.json` » ; le rapport HTML s'ouvre sur ce même résumé, et « `verify.py` » le recalcule à partir de « `events.jsonl` » au lieu de se fier au fichier :

- **Observation continue de X à Y.** Une période commence par `observation.started` et se termine par une pause, un arrêt, une perte de connexion Telegram, une déconnexion, un démarrage de processus sans arrêt ordonné, ou plus de trois minutes sans aucun enregistrement pendant l’observation (des signaux de présence sont enregistrés toutes les minutes ; par conséquent, le silence signifie que le processus s’est arrêté, s’est figé ou que l’ ordinateur est passé en veille). Lorsque l’intervalle entre les signaux de présence est modifié dans **les paramètres**, chaque signal enregistre ce changement et le silence autorisé passe à trois intervalles, sans jamais être inférieur à trois minutes.
- **Les lacunes** indiquent le délai entre deux périodes, accompagné de la raison. Une lacune toujours présente lors du dernier enregistrement est signalée par le code « `not_resumed_by_last_record` ».
- **Les identifiants de messages non observés ne sont pas pris en compte.** Pour les chaînes et les supergroupes, qui numérotent les messages par discussion, les identifiants manquants entre ceux qui ont été observés sont répertoriés sous forme de plages. Ils sont signalés comme « non*observés* » — supprimés, jamais remis ou hors de l’historique enregistré — et jamais comme « supprimés ». Les discussions privées et les groupes ordinaires partagent une séquence commune à l’ensemble du compte ; par conséquent, les lacunes observées à cet égard n’ont aucune signification et ne sont pas répertoriées.
- Les notifications de lacunes au niveau des conversations (par exemple, lorsque Telegram demande la récupération des différences dans un canal) sont comptabilisées comme des notes ; elles n’interrompent pas la couverture globale.

La couverture décrit ce que ce collecteur a enregistré. Elle ne constitue pas une preuve que Telegram a transmis toutes les mises à jour au cours d’une période continue.

## Producteur

Le manifeste signé des fichiers ZIP de preuves, des exportations de discussions, des journaux de témoins et de la déclaration des fichiers de profil des personnes contient `producer` : logiciel, version, projet (PhishDestroy), page d’accueil et référentiel source. Le rapport HTML affiche la même ligne, et `verify.py` l’affiche dans le cadre de ce qu’il a vérifié. Les archives créées avant l’existence de ce champ sont validées comme auparavant et sont signalées comme ne mentionnant pas de producteur.

## Profils de personnes

Un fichier de profil (`tgwitness-dossier-v1`, JSON) est généré sur demande à partir des enregistrements déjà présents dans le journal pour une conversation donnée ; aucune donnée n’est récupérée depuis Telegram et le contenu du profil n’est jamais enregistré dans le journal (l’activation et la désactivation des profils sont consignées sous la référence `dossier.changed`). Pour chaque personne dont un message a été enregistré, il répertorie l’historique des noms et des noms d’utilisateur, les indicateurs Telegram (bot, arnaque, faux, premium, vérifié, restreint, supprimé) tels qu’ils apparaissaient au moment de l’enregistrement, les identifiants de photo de profil, le hachage SHA-256 et le hachage perceptuel (pHash, compatible avec `imagehash.phash`) de l’ avatar issu du cache local d’avatars contenant des avatars similaires, l’activité (premier et dernier message, nombre de messages, partages modifiés et supprimés, messages par heure UTC), qui répond à qui, les autres discussions de ce journal dans lesquels la personne a écrit, ainsi que les portefeuilles mentionnés (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL ; les adresses Base58Check sont validées par somme de contrôle), les numéros de téléphone, les noms d’utilisateur et les liens, y compris les liens masqués derrière du texte.

Chaque fait indique les entrées du journal (`seq`) dont il est issu, et `record_hashes` contient le hachage de chaque entrée référencée. La déclaration est signée avec la clé de l'espace de travail :

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

Vérifie la signature, valide l’exportation des preuves elle-même (signature, chaîne de hachages et fichiers) et s’assure que chaque enregistrement référencé existe tel quel dans cette exportation du même espace de travail. Les hachages des avatars sont signalés comme provenant du cache local (et non des enregistrements du journal). Les mentions correspondent à des correspondances de motifs — il s’agit de pistes à vérifier, et non de faits avérés. Les profils sont activés pour chaque discussion, peuvent être exportés sous forme de fichier ZIP chiffré en AES-256 avec un mot de passe, et sont supprimés lorsqu’ils sont désactivés ou lorsque la discussion est supprimée des sources.

## Témoin indépendant

Un journal de témoin (`tgwitness-witness-v1`) et les publications de sa chaîne sont recoupés avec une exportation de preuves réalisée à l’aide de `verify.py --witness … --channel …` ; voir « [témoin indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/) ».

## Manifeste et points de contrôle

Le fichier `manifest.json` contient le format, l’heure d’exportation, la clé publique, l’empreinte digitale, la longueur du journal, le hachage d’en-tête, la portée, le producteur, les limitations et la valeur SHA-256 de chaque élément de contenu autre que `manifest.json` et `manifest.sig` eux-mêmes. Le fichier `manifest.sig` correspond à la signature Ed25519 en base64 du manifeste JSON canonique. Le vérificateur rejette les éléments inattendus ou manquants, les noms en double, les fichiers corrompus, les séquences ou chaînes brisées, les signatures non valides et les divergences par rapport à un point de contrôle fourni. Il n’extrait jamais les chemins d’accès aux archives. Il limite la taille totale déclarée non compressée à 4 GiB ; le `--max-gib N` permet des archives plus volumineuses créées avec une limite **de paramètres** augmentée.

Procurez-vous le code de vérification à partir d’un checkout fiable ou d’une copie indépendante validée. Un vérificateur contenu dans une archive non fiable est un élément exécutable fourni par l’auteur de cette archive ; sa présence constitue un avantage en termes de portabilité, et non un gage de confiance indépendant.

Un point de contrôle signe une déclaration contenant la clé publique, la longueur du journal, le hachage de tête et l’heure de création. Le vérificateur peut s’assurer qu’une archive ultérieure contient le même préfixe. Conservez un point de contrôle en dehors du collecteur avant toute modification contestée : un attaquant contrôlant à la fois l’archive et le point de contrôle peut remplacer les deux.

Une signature valide provenant d’une clé non épinglée établit uniquement la cohérence interne. Même une clé épinglée ne peut garantir l’authenticité du contenu source si le collecteur ou la clé a été compromis avant l’enregistrement. L’horodatage externe et la capture fiable constituent des exigences distinctes. TgWitness ne garantit ni l’admissibilité en justice ni la certification médico-légale.

## Pièces jointes

Les fichiers sont identifiés par leur hachage SHA-256 dans le répertoire « media/ ». Un événement « media.saved » associe un hachage et une longueur en octets à un événement de message spécifique. Les noms de fichiers bruts constituent des métadonnées, et ne correspondent jamais à des chemins d’accès locaux. Les octets multimédias sont téléchargés de manière asynchrone ; une suppression immédiate peut donc empêcher leur capture. La collecte désactivée, les fichiers trop volumineux ou de taille inconnue, les échecs de téléchargement et les téléchargements interrompus apparaissent comme des résultats. Un plantage du processus peut laisser des fichiers partiels non référencés ; ceux-ci ne sont pas inclus dans les exportations.

L'exportateur ZIP vérifie la correspondance entre les fichiers multimédias stockés et leurs noms. Les exportations au format JSONL, CSV et HTML vérifient les signatures des événements mais ne contiennent pas les données multimédias. Les rapports dérivés sont fournis à titre pratique ; le fichier events.jsonl constitue la représentation officielle des événements.

## Collecte et traitement durables des justificatifs (0,2)

Une tâche multimédia et la validation de l’événement de message s’effectuent en une seule transaction. La tâche stocke le descripteur du message TL d’origine ; l’observation signée associe son SHA-256, son compte et sa politique de taille. La récupération vérifie cette association avant le téléchargement. Elle ne récupère jamais le message actuel et ne le remplace pas silencieusement par une pièce jointe plus récente. Les tâches interrompues sont relancées, tandis qu’un échec permanent reste un résultat explicite.

Chaque espace de travail dispose de son propre journal et de sa propre identité de signature. Un événement « process.started » comprend un identifiant d’exécution, les heures locales, les versions des dépendances, les hachages des fichiers source, le compte/champ d’application initial, ainsi que les paramètres de capture. Les signaux de contrôle comprennent l’identifiant d’exécution, le temps monotone et l’état de la file d’attente. Le reçu de processus peut également être téléchargé sous la forme d’une déclaration signée séparément. Les mesures des fichiers sont autodéclarées et ne constituent pas une attestation matérielle fiable.

Des points de contrôle automatiques sont conservés localement au démarrage, toutes les cinq minutes pendant la surveillance (**Paramètres → Point de contrôle signé toutes les**), et lors d’un arrêt ordonné. La vérification au démarrage et l’exportation comparent le journal au dernier point de contrôle local conservé. Cela permet de détecter une restauration de la base de données lorsque le point de contrôle subsiste ; un opérateur contrôlant les deux éléments peut toutefois remplacer les deux. La conservation indépendante et les horodatages externes fiables restent des exigences distinctes.

Après un redémarrage, la position de mise à jour enregistrée de Telegram est reprise (`catch_up_from` dans `observation.started`) et les mises à jour manquantes sont demandées. Une nouvelle vérification périodique enregistre `message.recovered` pour les messages manquants et `message.missing_on_recheck` lorsque Telegram ne renvoie plus de message enregistré ; ce dernier n’est pas un avis de suppression et ne mentionne ni l’auteur de la suppression ni l’heure.

### Sauvegarde et restauration hors site (S3)

La copie hors site (Exportations, désactivée par défaut) transfère les segments de journal, les fichiers conservés, les points de contrôle avec leurs horodatages ainsi que les exportations de discussions terminées vers un stockage compatible S3, chiffrés avec AES-256-GCM avant leur transfert, à l’aide d’une clé conservée dans le coffre-fort de l’espace de travail ; la conservation par « Object Lock » s’applique lorsque le compartiment le prend en charge. Sans la clé téléchargée, la copie ne peut pas être lue. Restaurez et vérifiez à l’aide de `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

La restauration nécessite un répertoire ordinaire vide. Les téléchargements et les objets déchiffrés restent dans un espace de stockage temporaire privé jusqu’à ce que l’intégralité du journal et chaque point de contrôle conservé soient vérifiés. Les chemins d’accès aux objets non sécurisés, les plages de segments incohérentes et les journaux plus courts qu’un point de contrôle sont rejetés ; en cas d’échec de la vérification, aucun fichier restauré n’est publié. Les contrôles de conservation comparent le mode « Object Lock » et la date renvoyés avec le délai envoyé lors du téléchargement (tolérance d’arrondi d’une seconde). Un délai expiré, non valide ou raccourci n’est pas considéré comme vérifié. Le statut indique l’objet échantillonné dont la conservation a été relue pour ce cycle de téléchargement.

La progression de la copie est limitée à la destination et à la clé de chiffrement. La modification du point de terminaison, du compartiment ou du préfixe déclenche une copie complète du journal, des médias et des points de contrôle conservés localement vers cette destination. L’ancienne progression non limitée est conservée, mais n’est relancée qu’une seule fois après la mise à niveau. Les exportations historiques de discussions déjà supprimées de la boîte d’envoi locale restent à leur destination précédente.

Les fichiers locaux manquants ou corrompus sont signalés comme une erreur du cycle et le curseur de fichier reste positionné avant ceux-ci, de sorte que le fichier soit réessayé lors du cycle suivant ; les fichiers, points de contrôle et exportations qui suivent sont tout de même copiés. La restauration vérifie toutes les références aux fichiers conservés par rapport aux hachages déchiffrés et aux tailles enregistrées. Les segments de journal identiques qui se chevauchent provenant de téléchargements interrompus sont dédupliqués ; les chevauchements conflictuels sont rejetés. Les points de contrôle créés au cours d’un téléchargement sont reportés jusqu’à ce que les enregistrements du journal qu’ils couvrent aient été copiés, de sorte qu’un passage terminé ne publie pas de point de contrôle avant son journal.

### Exportation en continu d’instantanés

Les exportations en continu utilisent un instantané de lecture SQLite stable. Son début peut être antérieur au journal en ligne actuel une fois le téléchargement terminé. Un point de contrôle créé après cet instantané peut indiquer à juste titre que l’archive est plus courte ; comparez-le à un point de contrôle situé au niveau ou avant le préfixe exporté, et non à un point de contrôle ultérieur choisi arbitrairement.

## Préparation de la norme RFC 3161 et vérification des réponses (0.2)

Le mode « Evidence » (désactivé par défaut) envoie uniquement la valeur SHA-256 de chaque point de contrôle signé aux autorités RFC 3161 et aux calendriers OpenTimestamps répertoriés, via la route de l’espace de travail et jamais via MTProxy. Les réponses sont conservées dans `checkpoints/anchors/`, exportées et vérifiées par `verify.py` (`--tsa-ca` vérifie la signature TSA ; confirmez les preuves OpenTimestamps avec `ots upgrade` et `ots verify`).

Le module prépare une archive de requête contenant les octets canoniques du fichier checkpoint.json, une empreinte SHA-256 du message et un nonce aléatoire dans le fichier timestamp.tsq, ainsi que des sommes de contrôle et des instructions. Aucune requête réseau n’est effectuée. Cette préparation ne constitue pas un horodatage fiable.

`python -m tgwitness.anchor verify` appelle OpenSSL deux fois : une fois sur les octets de point de contrôle et une fois sur la requête d’origine. Un fichier CA de confiance est explicitement requis ; les certificats inclus ne sont pas automatiquement considérés comme fiables. La vérification de la requête est facultative via l’interface en ligne de commande ; veillez donc à conserver et à fournir l’option --request pour vérifier le nonce. Le résultat indique si la vérification a été effectuée. La signature du point de contrôle du collecteur et le journal doivent tout de même être vérifiés séparément à l’aide de l’empreinte digitale de confiance du collecteur.

Le vérificateur actuel ne récupère pas les informations de révocation et ne met pas en œuvre de validation d’archivage à long terme après l’expiration du certificat. Ne confondez pas la vérification réussie de la signature avec un horodatage qualifié ou une admissibilité juridique. Aucune autorité de signature de temps (TSA) véritablement indépendante n’a été contactée au cours du développement. Voir [la procédure](https://phishdestroy.github.io/TgWitness/fr/docs/reference/timestamp/).
