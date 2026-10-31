# Effectuez des recherches dans toutes les discussions

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/cases/

Traitez une affaire dans son intégralité, qu’il s’agisse de canaux, de groupes, de discussions privées ou de bots : collectez, reliez, reconstituez et transmettez les preuves.

Ce guide pratique suit le déroulement d’un incident fictif tout au long d’un dossier complet. Il utilise les fonctionnalités réelles de collecte, de recherche, de profilage des personnes et d’exportation. La carte du dossier est un exemple de documentation ; vos conclusions et votre registre des dossiers sont gérés en dehors de l’application.

CAS TRAITÉ / MODIFICATION DE LA DESTINATION D'UN PAIEMENT

### Un incident. Quatre conversations. Une piste à reconstituer.

Une annonce sur une chaîne fait référence à un bot. Un groupe opérationnel discute d’un nouveau lien de paiement. Un message privé de suivi le répète. Plus tard, l’annonce est modifiée et un message de groupe disparaît.

Qui a publié chaque version ?Où ce lien est-il apparu ?Quel fichier a été conservé ?Quels changements ont eu lieu, et quand ?

Pour le chargement de l'historique, la vérification facultative des sources par IA, le MCP, l'OCR et les webhooks sortants, consultez la section « [Utiliser les archives](https://phishdestroy.github.io/TgWitness/fr/docs/archive/) ».

## 1. Assurer une couverture complète de l’ensemble du compte

1. [Connectez le compte de collecte](https://phishdestroy.github.io/TgWitness/fr/docs/accounts/) dans son propre espace de travail. Notez la référence du dossier, l’identifiant du compte, le nom de l’espace de travail et l’empreinte de la clé de signature dans vos notes de dossier.
2. Sources ouvertes → Portée d’observation → Mode d’enquête. Passez en revue l’ensemble du compte, les quatre types de sources et vos propres actions. Ce préréglage permet d’enregistrer le profil d’une nouvelle source ainsi que ses 200 derniers messages visibles. Cliquez sur « Enregistrer la portée » et validez la portée.
3. Cliquez sur « **Charger les discussions** ». Comparez les sources avec la liste des conversations du compte et vérifiez les exclusions. Sous « **Paramètres » → « Discussions lues à partir de la liste du compte** », ajustez la limite initiale de la liste si nécessaire : la valeur par défaut est de 1 000 conversations, configurable jusqu’à 20 000. Les conversations dépassant cette limite sont détectées dès qu’elles deviennent actives.
4. Dans **les paramètres d’enregistrement**, sélectionnez et enregistrez « **Toutes les activités visibles** ». Vérifiez les types de pièces jointes, les limites de taille et l’espace disque disponible. Lancez l’observation et validez un message, une modification et une suppression contrôlés avant de vous fier à la configuration.

ChaînesGroupesConversations privéesBots

UN COMPTE / UNE CLÉ DE SIGNATURE**Toutes les activités visibles sur le compte sélectionné → un seul journal**

Messages · modifications · notifications de suppression · réactions visibles · événements liés à l'adhésion · actions personnelles

Le terme « compte complet » désigne les discussions auxquelles ce compte a accès, avec les types de sources et les exclusions configurés. Les discussions secrètes ne sont pas disponibles. De nouvelles discussions sont ajoutées au fur et à mesure des mises à jour ; l’activation de ce mode n’entraîne pas le téléchargement automatique de l’historique complet de toutes les discussions existantes.

## 2. Récupérer l'historique et conserver les fichiers

Constituez un registre des sources pour l’ensemble de l’enquête. Attribuez à chaque conversation une ligne comprenant son identifiant numérique, son titre, le compte concerné, les droits d’accès/rôle, la date de début de la conversation en direct, la date d’acquisition de l’historique, les résultats multimédias et les lacunes connues. Ne marquez une source comme « acquise » qu’après avoir vérifié les résultats correspondants.

| Besoin | Action dans le panneau | Ce qu’il propose |
| --- | --- | --- |
| Historique des discussions activées | Sources → Charger l'historique complet | Fonctionnalité principale actuelle : les messages passés disponibles sont intégrés au journal de l'espace de travail, avec des options de pause/reprise et un rapport d'avancement signé. [Guide de l'historique](https://phishdestroy.github.io/TgWitness/fr/docs/reference/history/). |
| Contexte de conversation existant dans le journal | Sources → Paramètres d’enregistrement → Instantané de l’historique | Les messages récents visibles sont présentés sous forme d’observations signées. Limite maximale par défaut : 500 ; **Paramètres → « Largest history snapshot »** permet d’augmenter cette limite jusqu’à 10 000. |
| Historique complet, tel qu'il est actuellement visible, d'une conversation | Exportation de l'intégralité d'une conversation → Exporter l'intégralité d'une conversation, ou Conversations → Exporter une conversation | Un ensemble signé distinct contenant les clés « `chat.json` » et « `chat.html` ». Répétez l'opération pour chaque source ; conservez les résultats indiquant la réussite ou l'échec. |
| Contexte : lorsqu’une nouvelle conversation apparaît | Périmètre d’observation → Lorsqu’une nouvelle conversation ou un nouveau bot apparaît | Un profil de source et jusqu’à 1 000 messages récents visibles ; le mode « Enquête » en sélectionne 200. Les discussions existantes ne bénéficient pas de cette fonctionnalité de manière rétroactive. |
| Nombre d'octets de la pièce jointe | Téléchargement des pièces jointes visibles + limites par type | Vérifiez la présence de `media.saved`, sa valeur SHA-256 et le nombre d’octets. Un téléchargement mis en file d’attente, ignoré ou ayant échoué ne constitue pas un fichier conservé. |

L'exportation complète d'une conversation correspond à un instantané distinct ; elle n'importe pas l'intégralité de l'historique dans le journal ni dans les profils des utilisateurs. Utilisez l'option « **Charger l'historique complet** de toutes les sources activées » ou des instantanés de journal délimités pour les données historiques que vous devez rechercher dans TgWitness. Vérifiez la liste des sources avant de lancer l'opération.

Dans le cas étudié, récupérez le canal d’annonce, le groupe d’opérations, la conversation avec le bot et le suivi privé. Conservez les octets et le hachage de la pièce jointe de la facture. L’historique disponible à ce jour ne permet pas de reconstituer un message supprimé avant sa capture ni une modification intermédiaire que Telegram ne renvoie plus.

## 3. Suivez l’évolution de la conversation et vos propres actions

Maintenez la surveillance active à mesure que l’affaire évolue. Marquez d’une étoile les discussions en cours liées à l’affaire comme sources prioritaires ; configurez les vérifications prioritaires et celles provenant d’autres sources dans **les paramètres d’enregistrement → « Recheck** ». Vérifiez les résultats relatifs à « `recheck.completed` », au rattrapage continu, à « FloodWait » et aux médias au fur et à mesure de l’avancement des travaux.

Utilisez **« Chats » → « Profil » → « Enregistrer le profil maintenant »** pour conserver les descriptions de source actuelles, les commandes du bot et les autres métadonnées fournies par Telegram. Ce profil de source est distinct des profils de personnes créés à partir des messages du journal.

**Suivi d’un bot ou d’une invitation dans le cadre de l’affaire**

1. Dans **« Chats » → « Ouvrir le lien Telegram »**, enregistrez d’abord l’aperçu. Le lien d’origine et l’aperçu généré deviennent des enregistrements signés.
2. Si l’enquête l’exige, la commande « **Join / open » permet**d’accéder à la source et de lancer un bot à l’aide du paramètre de démarrage fourni. Une demande de connexion en attente reste en attente dans l’historique.
3. Pour toute action que vous souhaitez documenter, utilisez la réponse textuelle du panneau ou la commande **« Appuyer sur le bouton »** prise en charge. Le journal conserve les codes « `interaction.requested` » et « `interaction.result` », y compris le texte ou l’URL renvoyés par la fonction de rappel.

Ces commandes effectuent des actions réelles sur Telegram. Un rappel déclenché dans une autre application Telegram n’est pas visible par le collecteur ; le message ou la modification ultérieure du bot peut l’être. Les applications Web, les paiements et les demandes relatives au téléphone ou à la localisation ne relèvent pas du mini-client.

## 4. Suivez les personnes, les liens et les fichiers dans les discussions

1. Ouvrez **le journal**, laissez le filtre de sources sur « **Toutes les sources »** et recherchez une expression distinctive, un domaine, un nom d’utilisateur ou un identifiant enregistré. Ouvrez chaque enregistrement correspondant et notez le nom du chat, l’identifiant du message et le numéro de séquence du journal.
2. Pour consulter une conversation, ouvrez « **Conversations » → « Contacts » → « Afficher les profils »**, puis sélectionnez une personne. Consultez l’historique des noms/noms d’utilisateur, les relations de réponse, l’activité, ainsi que**les rubriques « Également dans… » :** autres conversations observées, liens extraits, portefeuilles ou numéros de téléphone. Ouvrez les entrées du journal citées.
3. Suivez le même identifiant numérique d’utilisateur Telegram dans d’autres discussions de cet espace de travail. Considérez un nom correspondant, une mention de portefeuille ou un avatar similaire comme une piste à vérifier. Une adresse mentionnée ne prouve pas la propriété ; un avatar similaire ne prouve pas qu’il s’agit de la même personne.
4. Comparez les valeurs SHA-256 des pièces jointes conservées d’un enregistrement à l’autre. La concordance des hachages garantit l’identité au niveau des octets des fichiers enregistrés. Examinez les enregistrements associés aux messages et aux expéditeurs avant de tirer une conclusion quant à l’identité de la personne qui les a partagés.

CARTE DU DOSSIER / SUIVRE LES RÉFÉRENCESCas fictif · ce graphique n'est pas en temps réel

CHAÎNE / ANNONCE**Texte d'origine → texte révisé**

Enregistrements n° 101, n° 188 Message n° 84 · expéditeur non identifié

GROUPE / OPÉRATIONS**L'utilisateur 71001 publie le nouveau lien**

Enregistrement n° 146 · message n° 309 · Accusé de réception du fichier enregistré n° 151

BOT / CONVERSATION DE COMMANDE**Un bouton renvoie vers cette page**

Enregistrement n° 173 · message n° 12 Métadonnées du bouton « Retour »

PRIVÉ / SUIVI**L'utilisateur 71001 répète la destination**

Enregistrement n° 205 · message n° 922 · Accusé de réception du fichier enregistré n° 209

Quatre discussions apportent des observations différentes. Suivez les enregistrements sources pour chaque connexion ; n’attribuez pas la publication de la chaîne à l’utilisateur 71001 en l’absence d’un expéditeur identifié.

Les identifiants numériques et les références d’enregistrements sont fictifs pour ce guide pratique. Ce schéma explique le flux de travail d’un analyste utilisant la recherche, les profils et l’examen des enregistrements ; l’application ne génère pas de graphe d’enquête global.

| Connexion | Remarque complémentaire | Conclusion à conserver |
| --- | --- | --- |
| Même compte Telegram | Identifiant utilisateur 71001 dans le groupe n° 146 et la discussion privée n° 205 | Le même identifiant d’expéditeur a été publié dans les deux discussions. La question de l’identité réelle reste distincte. |
| Destination répétée | `pay.example.invalid/new` dans le n° 146, métadonnées du bouton n° 173, message modifié n° 188 et n° 205 | La même destination apparaît dans quatre contextes observés. Cela ne suffit pas à déterminer qui la contrôle. |
| Même nombre d’octets dans le fichier | Valeurs SHA-256 identiques dans les reçus multimédias finalisés n° 151 et n° 209 | Les deux pièces jointes conservées sont identiques au niveau des octets. Les noms de fichiers ou les vignettes ne suffiraient pas à eux seuls à le prouver. |

Les profils des utilisateurs concernent les auteurs dont les messages ont été enregistrés dans cette discussion et les relient à d’autres discussions du *même journal d’espace de travail*. Il ne s’agit pas d’un annuaire complet des membres. Les hachages des avatars proviennent d’un cache local distinct ; les citations de profil sont soumises à une limite configurable sous **Paramètres → Enregistrements cités par fait**.

## 5. Reconstituez la séquence et signalez les lacunes

Dans **la rubrique « Chats »**, examinez les versions enregistrées et leurs liens **vers l’entrée n°… du journal**. Dans **la rubrique « Journal »**, utilisez les options **« Toutes les sources »** ainsi que **« Modifications »**, « **Suppressions** » et « **Couverture** ». Établissez une chronologie de l’affaire en tenant compte à la fois de la date fournie par Telegram et de l’heure d’observation indiquée par le collecteur.

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

L’ordre des entrées dans le journal suit l’ordre de réception, et non nécessairement celui des actions initiales sur Telegram. Un instantané plus ancien peut apparaître après un message en temps réel plus récent. Veillez à bien distinguer les observations en temps réel, les instantanés, les messages récupérés, les notifications de suppression et les éléments « manquants lors de la vérification ultérieure ». Ajoutez explicitement la mention « intervalle inconnu » chaque fois que la couverture présente une lacune ; un instantané ultérieur n’efface pas cette lacune.

## 6. Étendre le cas à d’autres comptes de collecte

Créez un espace de travail pour chaque compte distinct et répétez l’inventaire du champ d’application et de l’historique. Enregistrez l’appartenance/le rôle et l’empreinte de la clé de signature pour chacun d’entre eux. Veillez à ce que les identifiants soient qualifiés par espace de travail et par discussion : un même numéro de message ne constitue pas un identifiant global valable pour tous les comptes.

Comparez les observations pertinentes dans vos notes de dossier ou vos outils d’analyse, en conservant la référence du compte et du journal pour chaque ligne. TgWitness ne propose actuellement pas de recherche globale, de chronologie fusionnée, de graphe des personnes ni d’archive de dossiers couvrant l’ensemble des espaces de travail. L’exportation complète multi-comptes d’un canal ou d’un supergroupe est une fonctionnalité distincte ; il ne s’agit pas d’une fusion de tous les journaux des comptes.

Lors de travaux de longue durée, faites appel à un [témoin indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/witness/) afin de préserver les limites initialement fixées. Utilisez le projet pilote de transmission contrôlée pour valider les chemins de capture et la visibilité des comptes.

## 7. Fournir un dossier complet et vérifiable

Exportez un fichier ZIP contenant le journal signé depuis chaque espace de travail. Il contient l’intégralité du journal enregistré, indépendamment des filtres de recherche du panneau. Exportez séparément les profils des personnes concernées, conservez l’intégralité de chaque historique de discussion et préservez l’intégralité des pièces jointes à titre de preuve.

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

Conservez les empreintes de confiance via un canal distinct. À partir d’une installation de confiance, vérifiez chaque élément par rapport à l’identité de son propre espace de travail :

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Vérifiez les résultats réels du vérificateur, conservez les originaux et archivez le rapport de couverture, les échecs d’acquisition et le journal des transferts avec vos conclusions. Le dossier de dossier de premier niveau et les conclusions des analystes sont compilés en externe ; les artefacts TgWitness individuels portent leurs propres signatures.

## Utilisez la même méthode pour d’autres enquêtes

**Litige lié à une commande ou à un paiement géré par un bot**

**Question :** qu’a promis le bot, quelle destination était associée au bouton, et qu’est-ce qui a changé par la suite ?

**Traçage :** publication sur la chaîne → aperçu du lien du bot enregistré → paramètre de démarrage du bot → messages et versions saisies au clavier → tout accusé de réception de rappel émis par le panneau → suivi en groupe ou en privé. Associez chaque destination à son enregistrement source ; conservez les descriptions de profil et les médias complets.

**Fournir :** une chronologie de l’offre observée et des réponses, les références des sources et les exportations vérifiées. L’affichage d’un lien de paiement ne constitue pas une preuve qu’un paiement a bien eu lieu.

**Messages supprimés à la suite d’un incident impliquant plusieurs discussions**

**Question :** qu’avait-on déjà observé avant la disparition des messages concernés ?

**Traçabilité :** toutes les discussions concernées → messages d’origine → modifications transmises → notifications de suppression ou résultats ultérieurs indiquant une disparition lors d’une nouvelle vérification → pièces jointes conservées → couverture médiatique autour de l’incident. Comparez les observations issues de comptes indépendants avec leur niveau de visibilité indiqué.

**Présentez :** une séquence de versions conservées et des intervalles d’inconnues explicites. Ne présentez pas l’absence d’un message dans l’historique comme une preuve qu’une personne en particulier l’a supprimé.

**Un participant change de nom au cours de plusieurs discussions**

**Question :** quelle activité observée appartient au même compte Telegram malgré un changement de nom ?

**Piste :** identifiant numérique de l’expéditeur → historique des noms/noms d’utilisateur enregistrés → réponses → autres discussions dans l’espace de travail → destinataires mentionnés et fichiers enregistrés. Vérifiez les enregistrements sources pour chaque connexion signalée ; distinguez les comptes similaires.

**Fournir :** une chronologie citée de l’activité du compte et des hypothèses distinctes concernant les relations. La similitude des noms et le pHash de l’avatar constituent des pistes, et non des preuves d’identité.
