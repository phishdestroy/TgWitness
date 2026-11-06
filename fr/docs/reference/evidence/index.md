# Format des preuves

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/

Contenu du fichier ZIP signé, types d’enregistrements, accusés de réception, profils des utilisateurs, copies hors site et vérification hors ligne.

TgWitness conserve les observations Telegram visibles sur le compte dans un journal signé. Les destinataires peuvent vérifier les enregistrements, les pièces jointes et les rapports sauvegardés à l’aide d’une clé de collecte fiable, puis comparer le journal avec un point de contrôle conservé de manière indépendante. Cette page décrit les formats, les vérifications et les éléments à conserver en vue de la remise.

Recipients can start with **VERIFY.cmd** on Windows: it asks for the original ZIP and independently obtained key fingerprint, displays an explained result, and saves a separate verification transcript. See [verification launchers and the portable runtime](https://github.com/phishdestroy/TgWitness/blob/main/docs/VERIFICATION_LAUNCHER.md) for setup and trust limits.

## Qu'est-ce qui est signé ?

| Contenu | Protection | Éléments à conserver |
| --- | --- | --- |
| Chaque observation du journal, y compris les événements opérationnels | Chaîne SHA-256 et signature Ed25519 par événement | `events.jsonl` d'origine, l'empreinte de la clé de confiance, et un point de contrôle conservé |
| Contenu du fichier ZIP de preuves | `manifest.sig` signe le manifeste canonique, qui répertorie les hachages des fichiers de contenu | Le fichier ZIP complet, comprenant son manifeste et sa signature |
| Pièces jointes conservées | SHA-256 et nombre d’octets dans un événement `media.saved` signé ; hachage du fichier dans le manifeste ZIP signé | Les octets d'origine contenus dans le fichier ZIP vérifié |
| Checkpoint | Signature Ed25519 portant sur la longueur du journal, le hachage d'en-tête, la clé publique et l'heure de création | Une copie indépendante conservée avant une modification contestée |
| Reçu de transaction | Signed record of the collector version, source-file hashes and start settings, also included in `process.started` | The receipt, associated journal and the environment evidence for the selected verification mode |
| Rapports lisibles : `report.html` et ses parties, `report.json`, `report.pdf`, `chat.pdf` | Un sceau Ed25519 par fichier sur son contenu ; le PDF comporte également une signature standard PDF (voir [Rapports lisibles](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#readable-reports)) | Le fichier tel qu'il a été reçu et l'empreinte digitale de la clé de confiance ; l'archive ZIP qu'il décrit |
| CSV autonome | Pas de signature cryptographique autonome ; les hachages d’événements seuls ne suffisent pas | Utilisez le fichier exact contenu dans l'archive ZIP vérifiée pour contrôler l'intégrité. |
| Captures d’écran, impressions ou fichiers PDF générés par un navigateur | Aucune signature TgWitness sur le document dérivé | Conservez le paquet original vérifié et documentez la manière dont le dérivé a été créé. |

Le collecteur vérifie les signatures du journal avant de générer chaque format d’exportation. Les rapports HTML et PDF lisibles comportent leurs propres sceaux ; le fichier CSV autonome est vérifié dans le cadre d’un fichier ZIP signé. Conservez le fichier ZIP afin de préserver les octets de la pièce jointe et le manifeste, ainsi qu’un point de contrôle distinct pour comparer le journal à une limite antérieure.

## Comparing chat exports

Verify and compare two signed chat-export ZIPs with independently retained signer fingerprints:

```
python -m tgwitness.verify first.zip --compare second.zip \
  --fingerprint FIRST_TRUSTED_KEY_SHA256 --compare-fingerprint SECOND_TRUSTED_KEY_SHA256
```

When both archives record the same numeric account and chat IDs, records are paired by message ID. **Unchanged** means equality of the complete saved JSON record: full text, author, dates, reply target, nested metadata and unknown fields are all included. JSON object key order does not matter; absent fields, nulls, value types and array order do. The 300-character preview is only for display. Changed entries name the differing top-level `changed_fields`, including changes invisible in that preview. Duplicate message IDs are rejected instead of overwriting one another during matching.

A difference can be a changed display name, view count, collection annotation or other observation metadata. It does not by itself establish a Telegram edit, identify who made a change, or prove which contradictory archive is accurate. Unparsed records remain in the comparison; equality of their saved representation does not mean their Telegram payload was decoded.

For different or missing account/chat identities, the tool only finds possible correspondences using sender, complete text, file hash, media type and a five-second time tolerance. It reports **Matched**, not **Unchanged**. These candidates do not establish message identity or equality of all metadata. Unparsed records remain unmatched. Differences in paired records remain listed in `changed`, including in content mode; these differences do not prove edits of the same message. With `--json`, `matched` counts pairs and `unchanged` counts pairs whose complete saved records are equal. Neither count proves message identity in content mode. The existing `changed_fields` and integer `unchanged` output remain compatible with earlier comparison results. Archive format and signature verification are unchanged.

## Transfert de l'enquête

1. Consignez la référence du dossier, le nom de l’opérateur, l’identifiant numérique du compte Telegram, les sources sélectionnées, la politique de collecte et la période de collecte dans vos notes de dossier. TgWitness conserve les observations et prend en charge les notes et les collectes liées aux sources dans [le « Case Board](https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-board/) ». Conservez les registres de transfert et de conservation avec vos documents de dossier. Vérifiez la configuration de collecte prévue à l’aide de la [procédure d’acceptation en direct](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
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

Une vérification réussie établit l’intégrité par rapport à la clé de collecte de confiance et aux limites définies. Consultez [la portée de la vérification](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#verification-scope) pour connaître les hypothèses de confiance et [les résultats](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/) [de validation](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/) des contrôles effectués.

## Extrait de la passation de pouvoir

Un fichier ZIP signé contient l'intégralité du journal de l'espace de travail. Lorsqu'un tribunal, un avocat ou un service de lutte contre les abus n'a besoin que de certaines conversations, d'une période donnée ou de certaines personnes, la fonction « **Exportations → Extrait de transfert »** prépare une copie allégée (« `tgwitness-handover-v1` ») conformément aux règles de divulgation sélectionnées. L’opérateur précise l’objectif et choisit les conversations, une période facultative (UTC), les personnes concernées par l’ extrait, le sort réservé à toutes les autres personnes (affichées, remplacées par des pseudonymes P01, P02… ou omises ), quels textes de messages sont conservés, quelles pièces jointes et photos de profil sont incluses, et si les numéros de téléphone et adresses e-mail présents dans les textes sont masqués. L’objectif et ces règles figurent dans le manifeste signé et dans le rapport ; le journal enregistre « `handover.exported` » avec l’accès qui l’a préparé et la valeur SHA-256 du fichier, et non son contenu.

Le script `verify.py` vérifie un extrait de deux manières. Un enregistrement indiqué comme inchangé est vérifié dans son intégralité : son contenu est comparé à son hachage, à sa signature Ed25519 et à son lien vers un prédécesseur inclus. Un enregistrement « minimisé » conserve la somme de contrôle et la signature d’origine ; la signature reste donc valide, mais les champs omis ne peuvent pas être recalculés à partir de celles-ci ; l’enregistrement précise ce qui a été omis et le rapport le signale. Le manifeste indique la longueur du journal et son en-tête, avec la signature du collecteur sur cet en-tête, et dénombre les enregistrements omis ; le fichier « `coverage.json` » décrit les conversations sélectionnées. Les noms figurant dans les noms de fichiers ne sont pas détectés. Vérifiez les fichiers finaux avant de les partager : le texte libre, les noms de fichiers et les pièces jointes sélectionnées peuvent toujours permettre d’identifier des personnes. Conservez l’archive ZIP complète et signée : l’extrait constitue une divulgation, et non un substitut.

## Rapports lisibles

Les preuves signées, les transferts et les fichiers ZIP de discussions contiennent des rapports lisibles au format HTML et JSON, ainsi que des PDF lorsque les polices requises sont disponibles, dans la langue sélectionnée pour le rapport. Chaque rapport est scellé à l’aide de la clé Ed25519 de l’espace de travail et peut être vérifié séparément : ` `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]``.

- `report.html` / `chat.html` : l'instruction de scellage (`tgwitness-report-seal-v1`) ferme le fichier et signe le SHA-256 de chaque octet qui le précède. Les journaux et les discussions volumineux sont divisés en parties d'une taille configurable (paramètres du rapport, de 500 à 100 000 enregistrements ; 5 000 par défaut) : `records/records-0001.html` ou `messages/messages-0001.html`, chacune scellée avec son numéro, sa plage et le total, et répertoriée avec son SHA-256 dans le manifeste signé. Les séries de signaux de présence du collecteur sont affichées sur une seule ligne, sauf si les paramètres du rapport prévoient de les lister une par une.
- `report.json` (`tgwitness-report-json-v1`, clés `format`, `report`, `seal`) : le sceau signe le SHA-256 du JSON canonique du `report`, ce qui permet aux systèmes de gestion des dossiers et aux scripts de lire les faits et d’effectuer une sélection à des fins de protection des données tout en préservant l’intégrité du fichier signé.
- `report.pdf` / `chat.pdf` : document officiel destiné à l’impression et à l’archivage, signé deux fois sur les mêmes octets, l’ensemble du fichier à l’exception de la valeur de signature (`/ByteRange`). La signature standard PDF (`adbe.pkcs7.detached`, CMS avec SHA-256 et ECDSA P-256) utilise un certificat de signature de document auto-émis conservé dans le coffre-fort de l’espace de travail ; son numéro de série de sujet correspond à l’empreinte de clé Ed25519 . Le sceau Ed25519 est intégré au CMS sous la forme de l’attribut non signé `2.25.240684792623320047764573196045913242332` et désigne le certificat SHA-256 par `"content": "pdf-byte-range"`, de sorte que la clé Ed25519 se porte garante du certificat. Un lecteur PDF indique si le fichier a été modifié après la signature et considère le signataire comme inconnu tant que le certificat n’est pas considéré comme fiable ; comparez plutôt l’empreinte Ed25519. Les fichiers PDF en chinois, japonais et coréen nécessitent une police sur le serveur (ou dans `TGWITNESS_FONT_DIR`) ; en l’absence de celle-ci, l’archive ZIP ne contient que les rapports HTML et JSON .

Dans un canal ou un supergroupe, Telegram numérote les messages 1, 2, 3… dans l’ordre. Une exportation de discussion répertorie le premier et le dernier numéro, le nombre de messages présents ainsi que chaque série de numéros manquants dans `message-ids.json` , le manifeste et l’en-tête `chat.json` , et signale chaque lacune à l’endroit où elle se trouve dans la transcription. `verify.py` les recompte à partir de `chat.json` . Un numéro manquant correspond à un message que Telegram n’a pas renvoyé (supprimé avant l’exportation ou non visible pour le compte) ; dans les discussions privées et les groupes de base, les numéros sont partagés entre toutes les discussions du compte et les lacunes ne sont pas comptabilisées.

After reading the history, the export asks Telegram for every absent number again, by number (`channels.getMessages`, up to 10,000 numbers). The result is in `message-ids.json` and the report. An empty answer records that the number is unavailable to this account at recheck time; it leaves the cause unspecified. A message returned on recheck is added to the export and marked `found_on_recheck`.

Chaque rapport commence par **. En bref** : un paragraphe, puis ce que le contenu montre et ce qu’il ne montre pas (qui se cache derrière un compte, l’exhaustivité de la transmission, les suppressions avant l’observation, l’heure sans horodatage). Le cachet de la page passe à l’ambre lorsque le navigateur a vérifié la signature du cachet, et non celle de la page : un navigateur ne fournit pas ses propres octets à une page. Il ne devient vert que lorsque le lecteur glisse le fichier dans la zone de vérification en bas de la page et que chaque octet correspond, et uniquement si la page affichée correspond bien à ce fichier ; sinon, il devient rouge.

Chaque rapport nomme le programme avec exactitude : le commit Git au moment où le collecteur s'exécute à partir d'un checkout ou lorsque le programme d'installation définit `TGWITNESS_COMMIT`, ainsi que le SHA-256 de ses fichiers source (`source_tree_sha256`, le JSON canonique du chemin → SHA-256 de chaque fichier `.py`, `.js`, `.css`, `.html` et `.svg` du paquet), que reproduit un checkout de ce commit à moins que les fichiers n'aient été modifiés. Le client Telegram est nommé d’après sa bibliothèque, sa couche API et son centre de données. Lorsque l’observation commence et lorsqu’une exportation de chat débute et se termine, le collecteur demande à Telegram son heure (`updates.getState`, en secondes entières) et enregistre l’heure de Telegram moins l’heure du collecteur, en tenant compte de l’incertitude liée au temps de transit ; les rapports indiquent ces mesures sous la rubrique « Chaîne de traçabilité ». Une exportation de discussion enregistre également le moment où l'historique a été lu, en plus des dates des messages.

### Guide d'utilisation de la visionneuse de rapports hors ligne et de l'archive

Décompressez l'archive ZIP complète avant d'ouvrir `chat.html` ou `report.html`. La visionneuse offre des fonctionnalités de recherche, de filtrage, d'affichage des participants, des indicateurs, des détails des enregistrements et des sélections JSON/CSV sans serveur. Conservez `viewer/` et `media/` à côté du rapport. Les sélections sont des dérivés : utilisez `verify.py SELECTION.json
--evidence ARCHIVE.zip` pour les comparer avec l'archive signée. Le vérificateur contrôle l’ID du rapport, la clé de signature, la limite de l’archive et chaque élément sélectionné ; les éléments modifiés, manquants ou en double sont rejetés. Les notes de sélection et l’heure de création restent des métadonnées non signées.

Les écarts entre les numéros de messages ne s'affichent que pour un flux de discussion complet, non filtré et classé par ordre croissant. Le fait de masquer une catégorie ou de ne pas parvenir à charger un bloc de données ne doit pas transformer une ligne omise en preuve de l'absence d'un message. Les surlignages de recherche s'appliquent au texte brut avant l'échappement « HTML », en conservant le balisage littéral.

Le navigateur vérifie les signatures du manifeste, l'ID et la clé du rapport, ainsi que tous les hachages de fichiers répertoriés. Il rejette les structures ZIP ambiguës ou mal formées, les noms en double et les chemins d'accès non sécurisés, et limite la taille des fichiers à 256 Mio et le volume total déclaré du contenu à 4 Gio. Utilisez le vérificateur autonome pour les archives plus volumineuses. Cette vérification par le navigateur complète les contrôles effectués par le vérificateur sur les chaînes de journaux et la sémantique des données.

Le fichier `README.txt` contient un guide de démarrage, un inventaire des fichiers alignés, des instructions de vérification et des remarques sur le format des données dans la langue du rapport, suivis d’un guide complet en anglais. `SHA256SUMS` couvre les fichiers qui y sont répertoriés, à l’exception de lui-même, de `manifest.json` et de `manifest.sig` ; le manifeste signé couvre également `SHA256SUMS`. Ne modifiez pas le fichier ZIP d’origine et enregistrez les fichiers de travail en dehors du dossier extrait. Les rapports PDF comprennent des signets de section et l’identification du dossier/rapport sur les pages suivantes.

### La conversation au moment de l'exportation

Une exportation de discussion enregistre ce que Telegram indiquait à propos de la discussion au moment où l'exportation a commencé : les propres étiquettes de Telegram (`scam`, `fake`, `restricted` avec leurs justifications, `verified`), les noms d'utilisateur, la description, le nombre de membres et d'administrateurs, la discussion associée, la protection du contenu, si les nouveaux membres peuvent voir les messages antérieurs et à partir de quel message ce compte a accès à l'historique (`available_min_id`), la date du message n° 1 lorsqu'il s'agit de la création du chat, et le SHA-256 de la photo du chat (enregistrée dans `media/`). Il enregistre la place du compte exportateur dans le chat : rôle, date d'inscription, nom de la personne qui l'a invité et, pour un administrateur, ses droits. Une demande refusée par Telegram est mentionnée à la place.

Lorsque le compte effectuant l'exportation est un administrateur, l'exportation lit le journal d'administration de la conversation (Telegram, conservé environ 48 heures) dans `admin-log.json` : suppressions et modifications avec le contenu et le compte à l'origine de l'action. C' est le seul enregistrement d'une suppression qui indique qui a supprimé le message.

### Indicateurs

La liste des rapports et l'archive contiennent les références `indicators.csv` , `indicators.stix.json` (STIX 2.1 ) et `indicators.misp.json` (événement MISP ), sur lesquelles un service de signalement des abus peut agir dans les messages enregistrés : liens et domaines (y compris ceux cachés derrière du texte, dans des boutons et dans les aperçus de liens), adresses de cryptomonnaies, noms d’utilisateur et liens d’invitation Telegram , numéros de téléphone, adresses e-mail et images enregistrées. Les adresses Bitcoin, Litecoin, Dogecoin et TRON ne sont répertoriées que si leur somme de contrôle base58 est valide, les adresses SegWit si leur somme de contrôle bech32 ou bech32m est valide et les adresses TON si leur CRC est valide ; les adresses EVM et Solana sont marquées comme non vérifiées. Les images comportent un SHA-256 et un hachage perceptuel (dHash, 64 bits) que les copies recompressées ou redimensionnées conservent pratiquement inchangés. Les rapports enregistrent des indicateurs afin qu’ils ne s’ouvrent pas par accident (`hxxps[://]example[.]com` ) ; les fichiers conservent les valeurs telles qu’elles étaient. Chaque indicateur est marqué comme inconnu et non destiné à la détection automatique (STIX , `indicator_types: unknown` , MISP , `to_ids: false` , distribution à la propre organisation) : le fait qu’il soit répertorié indique qu’un message le contenait, et non qu’il est malveillant. Un lien dont le texte affiche une adresse différente de celle vers laquelle il redirige est signalé dans le rapport.

Les rapports PDF se terminent par une déclaration de l'examinateur à signer à la main, une liste de contrôle destinée à un notaire ou à un expert judiciaire, ainsi qu'un code QR (également présent sur la première page) contenant l'identifiant du rapport, l'empreinte de la clé et le SHA-256 des données faisant autorité, de sorte qu'une impression permette de remonter jusqu'à son archive.

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

An unscoped notice does not establish that a message was never saved: a matching chat may be outside the current observation scope, or a unique match may be unavailable. Recheck absence remains a separate observation from a deletion notification in report counts, filters and labels. A later recovery clears the current missing state while preserving the earlier unsuccessful check in the signed history; neither observation establishes a deletion notice.

Multiple IDs resolved to the same chat from one notification are grouped as `deletion.batch`, regardless of their count. The notification does not establish that the entire history was cleared, who performed the deletion, or whether it applied to all participants. Saved outgoing messages do not change these limits. Older journals may contain `history.cleared` events inferred from batches of ten or more IDs, with explanatory text attributing the deletion to the other participant. Those inferences are not supported by the update. Preserve those original signed records, but treat them as grouped deletion notifications; the current interface labels them accordingly.

## Portée : continuité, lacunes et identifiants non observés

Chaque fichier ZIP signé porte la référence « `coverage.json` » ; le rapport HTML s'ouvre sur ce même résumé, et « `verify.py` » le recalcule à partir de « `events.jsonl` » au lieu de se fier au fichier :

- **Observation continue de X à Y.** Une période commence par `observation.started` et se termine par une pause, un arrêt, une perte de connexion Telegram, une déconnexion, un démarrage de processus sans arrêt ordonné, ou plus de trois minutes sans aucun enregistrement pendant l’observation (des signaux de présence sont enregistrés toutes les minutes ; par conséquent, le silence signifie que le processus s’est arrêté, s’est figé ou que l’ ordinateur est passé en veille). Lorsque l’intervalle entre les signaux de présence est modifié dans **les paramètres**, chaque signal enregistre ce changement et le silence autorisé passe à trois intervalles, sans jamais être inférieur à trois minutes.
- **Les lacunes** indiquent le délai entre deux périodes, accompagné de la raison. Une lacune toujours présente lors du dernier enregistrement est signalée par le code « `not_resumed_by_last_record` ».
- **Les identifiants de messages non observés.** Pour les chaînes et les supergroupes, qui numérotent les messages par discussion, les identifiants manquants entre ceux qui ont été observés sont répertoriés sous forme de plages. Ils sont signalés comme « non*observés* » — supprimés, jamais remis ou hors de l'historique enregistré — jamais comme « supprimés ». Les discussions privées et les groupes ordinaires partagent une séquence valable pour l'ensemble du compte ; ainsi, les lacunes au sein d'une telle discussion n'ont aucune signification et n'y sont pas répertoriées.
- Les notifications de lacunes au niveau des conversations (par exemple, lorsque Telegram demande la récupération des différences dans un canal) sont comptabilisées comme des notes ; elles n’interrompent pas la couverture globale.

### Numéros de messages manquants (`gap_summary`)

**Aperçu.** `coverage.json` → `gap_summary` mesure les numéros attribués par Telegram et que ce collecteur n’a jamais détectés. Telegram numérote les messages une fois par chaîne ou supergroupe, et une fois par compte pour l’ensemble des discussions privées, des bots et des groupes ordinaires. Un numéro situé entre deux messages observés est soit observé, soit manquant ; une plage contiguë indique de manière certaine que tous les messages qui y sont numérotés ont été observés. Une lacune ne désigne ni acteur ni raison.

| Domaine | Signification |
| --- | --- |
| `status` | `on`, ou `off` lorsqu’il est désactivé dans **Paramètres → Analyse des écarts** |
| `parameters` | Les paramètres ayant permis d'obtenir ce résultat, afin de pouvoir le reproduire |
| `chats[]` | Une entrée par canal ou supergroupe, chacune étant numérotée individuellement |
| `account` | La séquence, à l'échelle du compte, des discussions privées, des bots et des groupes classiques |
| `status` (par séquence) | `applicable`, ou `not_applicable` avec `reason` |
| `observed_from`, `observed_to`, `span` | Numéro observé en premier et en dernier, ainsi que la taille de la plage |
| `observed`, `observed_without_content` | Numéros observés ; ceux qui ne sont connus qu’à partir d’un enregistrement de suppression ou de nouvelle vérification |
| `missing`, `density`, `gap_ranges`, `largest_gap` | Nombres jamais observés, leur part dans l'intervalle, nombre d'itérations, itération la plus longue |
| `clusters[]` | Listes des lacunes : `low`, `high`, `missing`, ainsi que les numéros observés adjacents `after` / `before` avec leurs heures d'observation |
| `service_estimate` | Uniquement lorsque cette option est activée : nombre de numéros manquants qui correspondraient à des messages de service, compte tenu de leur part observée. Jamais soustrait de `missing` |

La validité est dérivée du journal, elle n'est jamais présumée :

- **Les canaux et les supergroupes** sont mesurés par discussion, y compris lors de l'exportation des discussions sélectionnées. Les enregistrements sélectionnés par l'expéditeur constituent la base de la mesure `not_applicable`.
- **La séquence à l'échelle du compte** est mesurée uniquement du premier au dernier message reçu alors que la collecte de l'intégralité du compte était activée et inclut les discussions privées, les bots, les groupes ordinaires et les messages propres au compte, sans exclure aucune de ces discussions (`scope.changed`). Les numéros désignés par `deletion.unscoped` sont considérés comme observés sans leur contenu. Une exportation ou un transfert de discussions sélectionnées ne permet pas de la mesurer. Si la collecte de l’ensemble du compte a été désactivée puis réactivée, une note indique que les numéros utilisés entre-temps apparaissent sous forme de lacunes.
- Les messages de service sont des entrées de journal dotées de leurs propres numéros ; ils comblent donc eux-mêmes leurs lacunes ; l'estimation facultative ne sert qu'à fournir du contexte.

`verify.py` recalcule `gap_summary` à partir de `events.jsonl` à partir des paramètres du `coverage.json` (valeurs par défaut pour les archives plus anciennes) et affiche la ligne relative à l’ensemble du compte dans son résumé de couverture. Le `get_capture_status`(MCP et ligne de commande) renvoie la même mesure pour les discussions qu’un accès peut lire ; la séquence à l’échelle du compte ne s’applique qu’aux accès couvrant l’ensemble de l’espace de travail.

Repeated observations of one service message count once, and the account service estimate uses only numbers inside the measured range. An applied scope must explicitly preserve the account's own messages before account-wide measurement is enabled; older records without that information cannot establish this condition. Stopped observation does not extend the measured range, and resuming it is noted. The live archive query has a time budget, including its database scan, and marks an unfinished measurement as partial.

Telegram documents the [separate message ID sequences](https://core.telegram.org/api/updates#message-id-sequences). These numbers describe observations; they do not identify a deletion actor or establish why a number is absent.

Lorsque Telegram cesse d’accepter le compte, l’enregistrement `coverage.gap` qui met fin à la surveillance contient `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` ou `not_authorized`) et l’erreur Telegram ; `verify.py` indique la cause de la fin de la période.

Coverage combines recorded observation periods, interruptions and message outcomes. Assess it together with the selected chats, period and attachment policy; continuous operation alone does not establish complete delivery of Telegram updates.

## Producteur

Le manifeste signé des fichiers ZIP de preuves, des exportations de discussions, des journaux de témoins et de la déclaration des fichiers de profil des personnes contient `producer` : logiciel, version, projet (PhishDestroy), page d’accueil et référentiel source. Le rapport HTML affiche la même ligne, et `verify.py` l’affiche dans le cadre de ce qu’il a vérifié. Les archives créées avant l’existence de ce champ sont validées comme auparavant et sont signalées comme ne mentionnant pas de producteur.

Chaque enregistrement `observation.started` mentionne également le client Telegram qui a effectué l’observation : son `api_id` (jamais le hachage), qu’il s’agisse d’une paire publique intégrée ou de l’application propre à l’opérateur, la description du client envoyée dans la demande de connexion Telegram, ainsi que le type de route de connexion avec le mode IP (sans adresse proxy ni secret). Le rapport et le fichier « `custody.json` » répertorient chaque client et chaque itinéraire distincts avec leur date d’enregistrement, ainsi que les moments où aucun proxy répertorié n’a répondu et où le fichier « Telegram » a détecté l’adresse du serveur. Les journaux enregistrés avant celui-ci le mentionnent.

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

Run verification from your installed TgWitness version or a reviewed checkout. The copy included in an archive supports portable use; check that copy against your trusted installation before executing it.

A checkpoint signs a statement containing the public key, journal length, head hash, and creation time. The verifier can check that a later archive contains the same prefix. Retain the checkpoint outside the collector, so later verification compares the archive with a reference held separately from it.

## Périmètre de vérification

Verification checks the archive and the collection mode used to produce it. Choose the mode whose trust boundary matches the case, then retain its verification inputs.

| Mode de collecte | Ce que vérifie le vérificateur | Données de vérification et périmètre de confiance |
| --- | --- | --- |
| Espace de travail local | Record signatures, hash chain, manifest and attachment bytes | Independently retained collector fingerprint; the host administrator controls the local signing key |
| Espace de travail local avec un témoin indépendant | Vérification des archives et cohérence avec un préfixe de journal antérieur conservé par le témoin | Separately trusted witness key and records; the checkpoint binds the prefix already observed |
| [Capture GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) | GitHub attestation of the archive digest, approved workflow and collector commits, hosted runner, fresh session/key origin and internal archive integrity | Trusted verifier policy, caller repository and GitHub attestation bundle; collection runs under the pinned workflow |
| [Déploiement dans le cloud](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/) | Provider lifecycle and access records, firewall and Cloudflare state, plus the collector's signed run record | Read-only queries to the provider and Cloudflare; availability of individual checks depends on the provider |
| [Machine virtuelle confidentielle Intel TDX](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx) | Quote signature and platform status, binding to the collector statement, compose and OS measurements | Intel trust chain and expected deployment measurements; retain the results of every required TDX check |

In sealed acquisition, the approved collector receives data through an authenticated Telegram connection inside the verified environment. Attestation binds the archive to that execution, so verification covers acquisition as well as later file integrity. This relies on the approved code and the platform trust chain listed above. GitHub capture verification requires a session created inside the run and rejects imported-session captures.

The run receipt records the collector version, file hashes and startup settings. GitHub provenance and TDX measurements provide the environment checks; the [validation record](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/) identifies tested configurations.

TgWitness signs the observations it collects; Telegram and message authors do not issue these signatures. In a local workspace, material created before the first independent checkpoint still depends on the collector and its key holder. Coverage records describe the selected scope and collection outcomes, while verified external timestamps anchor the committed archive or journal boundary in time.

## Pièces jointes

Les fichiers sont identifiés par leur hachage SHA-256 dans le répertoire « media/ ». Un événement « media.saved » associe un hachage et une longueur en octets à un événement de message spécifique. Les noms de fichiers bruts constituent des métadonnées, et ne correspondent jamais à des chemins d’accès locaux. Les octets multimédias sont téléchargés de manière asynchrone ; une suppression immédiate peut donc empêcher leur capture. La collecte désactivée, les fichiers trop volumineux ou de taille inconnue, les échecs de téléchargement et les téléchargements interrompus apparaissent comme des résultats. Un plantage du processus peut laisser des fichiers partiels non référencés ; ceux-ci ne sont pas inclus dans les exportations.

L'exportateur ZIP vérifie la correspondance entre les fichiers multimédias stockés et leurs noms. Les exportations au format JSONL, CSV et HTML vérifient les signatures des événements mais ne contiennent pas les données multimédias. Les rapports dérivés sont fournis à titre pratique ; le fichier events.jsonl constitue la représentation officielle des événements.

Une exportation complète d'une conversation enregistre les pièces jointes, conformément aux paramètres de l'espace de travail, dans le répertoire media/, sous le nom SHA-256. Chaque enregistrement de message dans chat.json indique le nom de son fichier (`file`, `file_sha256`) ou la raison de son absence (`file_status`), ainsi que ce que le lecteur a vu autour du texte : liens derrière le texte, origine du transfert, boutons de bot, signature, vues et le compte à rebours de suppression automatique. `verify.py` vérifie que chaque fichier nommé figure dans le manifeste signé sous ce hachage.

## Collecte et traitement durables des justificatifs (0,2)

Une tâche multimédia et la validation de l’événement de message s’effectuent en une seule transaction. La tâche stocke le descripteur du message TL d’origine ; l’observation signée associe son SHA-256, son compte et sa politique de taille. La récupération vérifie cette association avant le téléchargement. Elle ne récupère jamais le message actuel et ne le remplace pas silencieusement par une pièce jointe plus récente. Les tâches interrompues sont relancées, tandis qu’un échec permanent reste un résultat explicite.

Each workspace has its own journal and signing identity. A process.started event includes a run ID, local clocks, dependency versions, source-file hashes, initial account/scope, and capture settings. Heartbeats include the run ID, monotonic time, and queue state. The run receipt can also be downloaded as a separately signed statement. For verification of the execution environment, pair it with the GitHub attestation or TDX checks described in [Verification scope](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#verification-scope).

Automatic checkpoints are retained locally on startup, every five minutes while observing (**Parameters → Signed checkpoint every**), and on orderly stop. Startup verification and export compare the journal against the latest retained local checkpoint. This can detect a database rollback when the checkpoint survives. Independent retention keeps that reference available outside the workspace; a verified external timestamp additionally anchors it in time.

Après un redémarrage, la position de mise à jour enregistrée de Telegram est reprise (`catch_up_from` dans `observation.started`) et les mises à jour manquantes sont demandées. Une nouvelle vérification périodique enregistre `message.recovered` pour les messages manquants et `message.missing_on_recheck` lorsque Telegram ne renvoie plus de message enregistré ; ce dernier n’est pas un avis de suppression et ne mentionne ni l’auteur de la suppression ni l’heure.

### Sauvegarde et restauration hors site (S3)

La copie hors site (Exportations, désactivée par défaut) transfère les segments de journal, les fichiers conservés, les points de contrôle avec leurs horodatages ainsi que les exportations de discussions terminées vers un stockage compatible S3, chiffrés avec AES-256-GCM avant leur transfert, à l’aide d’une clé conservée dans le coffre-fort de l’espace de travail ; la conservation par « Object Lock » s’applique lorsque le compartiment le prend en charge. Sans la clé téléchargée, la copie ne peut pas être lue. Restaurez et vérifiez à l’aide de `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

La restauration nécessite un répertoire ordinaire vide. Les téléchargements et les objets déchiffrés restent dans un espace de stockage temporaire privé jusqu’à ce que l’intégralité du journal et chaque point de contrôle conservé soient vérifiés. Les chemins d’accès aux objets non sécurisés, les plages de segments incohérentes et les journaux plus courts qu’un point de contrôle sont rejetés ; en cas d’échec de la vérification, aucun fichier restauré n’est publié. Les contrôles de conservation comparent le mode « Object Lock » et la date renvoyés avec le délai envoyé lors du téléchargement (tolérance d’arrondi d’une seconde). Un délai expiré, non valide ou raccourci n’est pas considéré comme vérifié. Le statut indique l’objet échantillonné dont la conservation a été relue pour ce cycle de téléchargement.

Les fichiers locaux manquants ou corrompus sont signalés comme une erreur du cycle et le curseur de fichier reste positionné avant ceux-ci, de sorte que le fichier soit réessayé lors du cycle suivant ; les fichiers, points de contrôle et exportations qui suivent sont tout de même copiés. La restauration vérifie toutes les références aux fichiers conservés par rapport aux hachages déchiffrés et aux tailles enregistrées. Les segments de journal identiques qui se chevauchent provenant de téléchargements interrompus sont dédupliqués ; les chevauchements conflictuels sont rejetés. Les points de contrôle créés au cours d’un téléchargement sont reportés jusqu’à ce que les enregistrements du journal qu’ils couvrent aient été copiés, de sorte qu’un passage terminé ne publie pas de point de contrôle avant son journal.

### Exportation en continu d’instantanés

Les exportations en continu utilisent un instantané de lecture SQLite stable. Son début peut être antérieur au journal en ligne actuel une fois le téléchargement terminé. Un point de contrôle créé après cet instantané peut indiquer à juste titre que l’archive est plus courte ; comparez-le à un point de contrôle situé au niveau ou avant le préfixe exporté, et non à un point de contrôle ultérieur choisi arbitrairement.

## Préparation de la norme RFC 3161 et vérification des réponses (0.2)

Le mode « Evidence » (désactivé par défaut) envoie uniquement la valeur SHA-256 de chaque point de contrôle signé aux autorités RFC 3161 et aux calendriers OpenTimestamps répertoriés, via la route de l’espace de travail et jamais via MTProxy. Les réponses sont conservées dans `checkpoints/anchors/`, exportées et vérifiées par `verify.py` (`--tsa-ca` vérifie la signature TSA ; confirmez les preuves OpenTimestamps avec `ots upgrade` et `ots verify`).

Le module prépare une archive de requête contenant les octets canoniques du fichier checkpoint.json, une empreinte SHA-256 du message et un nonce aléatoire dans le fichier timestamp.tsq, ainsi que des sommes de contrôle et des instructions. Aucune requête réseau n’est effectuée. Cette préparation ne constitue pas un horodatage fiable.

`python -m tgwitness.anchor verify` appelle OpenSSL deux fois : une fois sur les octets de point de contrôle et une fois sur la requête d’origine. Un fichier CA de confiance est explicitement requis ; les certificats inclus ne sont pas automatiquement considérés comme fiables. La vérification de la requête est facultative via l’interface en ligne de commande ; veillez donc à conserver et à fournir l’option --request pour vérifier le nonce. Le résultat indique si la vérification a été effectuée. La signature du point de contrôle du collecteur et le journal doivent tout de même être vérifiés séparément à l’aide de l’empreinte digitale de confiance du collecteur.

La vérification contrôle la signature de la réponse, les octets de point de contrôle et, le cas échéant, la requête d’origine dans le cadre de la chaîne de confiance de l’autorité de certification spécifiée. Les contrôles de révocation et la validation de l’archivage à long terme après l’expiration du certificat ne relèvent pas du vérificateur actuel. Consultez la [procédure](https://phishdestroy.github.io/TgWitness/fr/docs/reference/timestamp/) et [les résultats de validation](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/).

## Enregistrements facultatifs en mode « preuves » : appareils drand et Telegram

Deux enregistrements supplémentaires peuvent s'exécuter lors des mêmes passes que les horodatages. Tous deux sont désactivés par défaut et ne prennent effet que lorsque le mode « Preuves » est activé : Extras → Preuves et sauvegardes → **Témoins supplémentaires · facultatif**, ou `"drand": true` et `"devices": true` dans `POST /api/evidence`. Une défaillance n’empêche pas le fonctionnement de l’autre ni celui des horodatages ; le panneau affiche le dernier résultat de chacun sous le formulaire.

**drand** (`beacon.drand` ). À chaque passage, le collecteur enregistre la dernière série de drand quicknet, le générateur aléatoire public de la League of Entropy (une série toutes les 3 secondes), dans le journal : `chain` , `round` , `randomness` , `signature` , `round_time` et le `relay` qui a répondu. Une série vérifiée et imprévisible fournit une référence temporelle inférieure pour les données liées par hachage qui suivent. Un horodatage vérifié sur un point de contrôle ultérieur fournit une référence temporelle supérieure. Ces vérifications délimitent le contenu lié ; la couverture de la collecte est évaluée séparément. Le collecteur interroge d’abord `drand.cloudflare.com` , puis les relais de Protocol Labs, via la route de l’espace de travail, à raison d’une requête par passage.

`verify.py` vérifie que chaque valeur aléatoire correspond au SHA-256 de sa signature et que le temps de cycle est correct, puis signale les cycles, la plus longue période sans cycle et le retard de l’horloge du collecteur par rapport à drand. Il ne vérifie pas la signature BLS. `--check-drand` compare les cycles avec un relais Cloudflare et un relais Protocol Labs, soit tous, soit un échantillon aléatoire de 100 dans un journal complet ; un cycle qui diffère échoue à la vérification.

Appareils **, Telegram,**, `account.devices`. À chaque passage, le système lit les sessions du compte avec `account.getAuthorizations` ; la liste Telegram s'affiche dans Paramètres → Appareils, et l'enregistre : dans son intégralité lorsqu’elle a changé depuis le passage précédent, avec les hachages de session `added` et `removed`, sinon uniquement son nombre et SHA-256. Le modèle de l’appareil, la plateforme, l’application et sa version, la date de création et la dernière activité, le pays et la région sont conservés ; les adresses IP ne le sont pas, car les exportations de preuves échappent à votre contrôle. La session du collecteur lui-même est active en permanence, de sorte que seule l’activité des autres sessions est considérée comme un changement. Le `verify.py` indique la fréquence à laquelle la liste a été enregistrée, ainsi que chaque nouvelle session et chaque session terminée. Il ne lit la liste que pendant que l’observation est en cours.

Ce qu’ils ne montrent pas : drand ne prouve rien de plus que l’ordre des enregistrements par rapport à l’heure publique, et la liste des appareils correspond à la déclaration de Telegram transmise par le collecteur, signée par ce dernier comme tous les autres enregistrements.

**Journal de Cloudflare Gateway** (`cloudflare.gateway_dns`). Pour un serveur dont la résolution s'effectue via Cloudflare Gateway ([Gateway DNS](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)), chaque pass copie ce que Gateway a enregistré depuis la copie précédente : un enregistrement par fenêtre de trois heures au maximum avec `from`, `until`, `location_id`, le `address` du serveur lorsqu'il est défini, et le `queries` en tant que `[at, name, type, rcode, decision, colo]`, même en l'absence d'enregistrements. Configurez-le sous **Journal de la passerelle Cloudflare** : compte, emplacement, adresse facultative et un jeton en lecture seule (lecture des données analytiques du compte Analytics en lecture ; Zero Trust PII en lecture pour conserver une adresse d’un emplacement partagé). Le panneau les vérifie à l’aide d’une seule requête avant l’enregistrement ; le jeton reste chiffré et n’apparaît jamais dans le journal. `verify.py` répertorie les fenêtres, les noms les plus recherchés et les moments non couverts par une copie ; un enregistrement dont le nombre ne correspond pas à ses requêtes échoue. Une fenêtre contenant plus d’une page de requêtes en une seule seconde conserve cette page et indique que le reste est manquant. La copie est la réponse de Cloudflare transmise par le collecteur, signée par ce dernier ; dans les 24 heures, toute personne disposant d’ un jeton en lecture seule peut la comparer avec celle de Cloudflare.
