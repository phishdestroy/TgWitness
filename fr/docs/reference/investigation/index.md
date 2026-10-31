# Mode enquête

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/investigation/

Enquêtes portant sur l’intégralité d’un compte, couvrant les chaînes, les groupes, les discussions privées et les bots, depuis la définition du périmètre jusqu’à la constitution d’un dossier de cas vérifié.

Suivez une affaire à travers les canaux, les groupes, les discussions privées et les bots, depuis l’acquisition initiale jusqu’à une chronologie référencée et un transfert vérifiable. La version interactive du site web est disponible à l’adresse `/docs/cases/` ; [instructions de prévisualisation](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

## Exemple concret : un changement de destination au cours de quatre conversations

Une annonce fait référence à un bot. Un groupe opérationnel discute d’une nouvelle destination de paiement, le clavier du bot l’affiche, puis un message privé de suivi la répète. L’annonce est ensuite modifiée et un message de groupe disparaît.

Les questions sont les suivantes : qu’a-t-on observé avant et après la modification, quels comptes Telegram ont publié chaque élément, où la destination est-elle apparue, quels octets de pièce jointe ont été conservés, et quels intervalles restent inconnus ?

Tous les noms, identifiants, dates et heures ainsi que les références du journal figurant dans cet exemple sont fictifs. Le processus utilise les fonctionnalités actuelles ; la carte de l’affaire est une illustration et non un graphique généré automatiquement par l’application.

Organigramme · Chaînes → Journal de l'espace de travail; Groupes → Journal de l'espace de travail; Conversations privées → Journal de l'espace de travail; Bots → Journal de l'espace de travail; Journal de l'espace de travail → Rechercher dans toutes les sources; Journal de l'espace de travail → Fiches de personnes avec références aux enregistrements; Journal de l'espace de travail → Versions enregistrées et accusés de réception des pièces jointes; Rechercher dans toutes les sources → Chronologie de l’analyste et registre des sources; Fiches de personnes avec références aux enregistrements → Chronologie de l’analyste et registre des sources; Versions enregistrées et accusés de réception des pièces jointes → Chronologie de l’analyste et registre des sources; Journal de l'espace de travail → Fichier ZIP contenant les preuves signées; Chronologie de l’analyste et registre des sources → Transfert de dossier avec des éléments de preuve vérifiés séparément; Fichier ZIP contenant les preuves signées → Transfert de dossier avec des éléments de preuve vérifiés séparément · Chaînes · Groupes · Conversations privées · Bots · Journal de l'espace detravail · Rechercher dans toutes lessources · Fiches de personnes avecréférences auxenregistrements · Versions enregistrées etaccusés de réception despièces jointes · Fichier ZIP contenant lespreuves signées · Chronologie de l’analysteet registre des sources · Transfert de dossier avecdes éléments de preuvevérifiés séparément

**Schéma sous forme de texte**

1. Chaînes → Journal de l'espace de travail
2. Groupes → Journal de l'espace de travail
3. Conversations privées → Journal de l'espace de travail
4. Bots → Journal de l'espace de travail
5. Journal de l'espace de travail → Rechercher dans toutes les sources
6. Journal de l'espace de travail → Fiches de personnes avec références aux enregistrements
7. Journal de l'espace de travail → Versions enregistrées et accusés de réception des pièces jointes
8. Rechercher dans toutes les sources → Chronologie de l’analyste et registre des sources
9. Fiches de personnes avec références aux enregistrements → Chronologie de l’analyste et registre des sources
10. Versions enregistrées et accusés de réception des pièces jointes → Chronologie de l’analyste et registre des sources
11. Journal de l'espace de travail → Fichier ZIP contenant les preuves signées
12. Chronologie de l’analyste et registre des sources → Transfert de dossier avec des éléments de preuve vérifiés séparément
13. Fichier ZIP contenant les preuves signées → Transfert de dossier avec des éléments de preuve vérifiés séparément

## 1. Définir le cas et recueillir l’intégralité des faits

1. Connectez le compte de collecte dans son propre espace de travail. Dans les notes externes relatives au dossier, consignez la référence du dossier, l’identifiant du compte, l’espace de travail, la date de début de l’observation et l’empreinte de la clé de signature de confiance.
2. **Sources** ouvertes **→ Portée d’observation → Mode d’enquête**. Le préréglage sélectionne « **Compte complet** », les chaînes/groupes/discussions privées/bots, vos propres actions, les profils des sources et les 200 derniers messages visibles pour les sources nouvellement découvertes. Vérifiez ces paramètres, cliquez sur **« Enregistrer la portée »**, puis confirmez la portée.
3. **Chargez les discussions** et comparez les sources avec la liste des conversations du compte. Vérifiez les exclusions. **Le paramètre « Nombre de discussions lues à partir de la liste du compte »** est défini par défaut sur 1 000 et peut aller jusqu’à 20 000. Les sources dépassant la limite de la liste sont ajoutées dès qu’ elles deviennent actives. Enregistrez ce qui a effectivement été recensé.
4. Dans **les paramètres d’enregistrement**, sélectionnez « **Toutes les activités visibles »** et enregistrez les paramètres de surveillance. Vérifiez les types et limites de pièces jointes ainsi que l’espace disque disponible.
5. Lancez l’observation. Validez un nouveau message contrôlé, une modification et une suppression, puis conservez les références du test ainsi que les éventuels échecs.

Le mode « Compte complet » enregistre l’activité visible sur le compte, conformément aux paramètres enregistrés. Il n’accède pas aux discussions secrètes et ne rejoint pas automatiquement tous les groupes associés. Il ne récupère pas non plus l’historique de toutes les conversations existantes. Voir [la portée de la collecte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account).

## 2. Répertorier toutes les sources et recueillir le contexte historique

Tenez un registre des sources avec une ligne par conversation :

| Domaine | Enregistrer |
| --- | --- |
| Identité | Espace de travail, identifiant de compte, identifiant numérique de la conversation, titre et type |
| Visibilité | Adhésion/rôle, accès confirmé ou non confirmé, exclusions |
| Capture en temps réel | Date de lancement, types d’événements sélectionnés et modifications ultérieures de la politique |
| Historique du journal | Capture d'écran demandée/réalisée, limite, heure et références d'enregistrement |
| Historique complet | Nom de fichier d’exportation signé par conversation, limites et statut (réussite/échec) |
| Pièces jointes | Reçus multimédias complets, hachages, tailles et résultats omis ou échoués |
| Champ d'application | Pannes, collecte incomplète, FloodWait, messages indisponibles et autres lacunes |

Utilisez la méthode d’acquisition adaptée à chaque source :

- **La fonction « Charger l'historique complet** dans **les sources** » (`main` actuellement) charge les anciens messages disponibles provenant des sources activées dans le journal de l'espace de travail. Elle prend en charge la mise en pause/reprise ainsi qu'un rapport de progression signé. Voir la section « [Acquisition de l'historique](https://phishdestroy.github.io/TgWitness/fr/docs/reference/history/) ».
- **L'instantané de l'historique** enregistre les messages visibles récents dans le journal d'observation. Sa limite maximale par défaut est de 500 ; sous **Paramètres → « Largest history snapshot »,** vous pouvez augmenter cette limite jusqu'à 10 000. Il s'agit d'observations de l'historique actuel, et non de modifications reconstituées.
- **Exportation complète de la conversation → « Exporter la conversation complète** », ou **« Conversations » → « Exporter la conversation** », permet de récupérer l’ historique actuellement visible d’une conversation dans un ensemble distinct signé `chat.json` / `chat.html`. Répétez l’opération pour les sources du dossier et conservez chaque résultat.
- **Lorsqu’un nouveau chat ou un nouveau bot apparaît,** il est possible d’en enregistrer le profil ainsi que jusqu’à 1 000 messages récents ; le mode « Enquête » en sélectionne 200. Les chats existants ne bénéficient pas de cette collecte rétroactive lorsque le mode est activé.
- **Le téléchargement des pièces jointes visibles** permet de conserver les octets conformément à la politique configurée. Exigez un reçu `media.saved` complet avec SHA-256 et le nombre d’octets. Une tâche en file d’attente, une vignette ou un nom de fichier ne constituent pas une pièce jointe conservée.

Une exportation complète d’une conversation **ne** remplit **pas** le journal ni les profils des personnes avec l’ensemble de ses messages. Utilisez **« Charger l’historique complet »** ou des « instantanés de journal délimités » pour l’historique que vous devez analyser dans TgWitness. Vérifiez la liste des sources activées avant de lancer une analyse de l’historique. Aucune de ces deux méthodes ne permet de récupérer les données que Telegram ne renvoie plus.

## 3. Conserver l’évolution du dossier et les interactions délibérées

Marquez les discussions relatives à des affaires en cours comme sources prioritaires. Vérifiez les intervalles de vérification, le rattrapage continu et les résultats relatifs aux médias. Veillez à ce que le collecteur continue d’observer pendant l’utilisation du compte. Utilisez **Discussions → Profil → Enregistrer le profil maintenant** pour conserver les métadonnées de la source, telles que les descriptions et les commandes du bot. Cela est distinct des profils de personnes dérivés des messages enregistrés.

Lorsque l’affaire implique de suivre une source ou d’interagir avec un bot :

1. **Ouvrir le lien Telegram → Enregistrer l’aperçu : cette fonction** enregistre le lien fourni et l’ aperçu affiché avant toute action.
2. **La commande « join / open and observe** » effectue l'opération « join/open » et envoie le paramètre de démarrage du bot lorsqu'il est fourni. Une demande d'adhésion en attente d'approbation est enregistrée comme « en attente ».
3. Les réponses textuelles émises par le panneau et les pressions sur les boutons prises en charge conservent les codes `interaction.requested` et `interaction.result`. Les accusés de réception de rappel peuvent conserver le texte de la fenêtre contextuelle renvoyée, l'état de l'alerte et l'URL.

Il s’agit là d’actions réelles sur les comptes. Les pressions sur les boutons de rappel dans une autre application Telegram ne sont pas visibles par le collecteur, bien que les messages ou modifications qui en résultent puissent l’être. Le mini-client n’effectue pas de workflows liés aux applications web, aux paiements, au téléphone ou à la localisation. Pour connaître le comportement exact, consultez la section « [Interactions avec les panneaux](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/#act-from-the-panel) ».

## 4. Relier les observations entre les différentes discussions

Dans **le Journal**, sélectionnez « **Toutes les sources »** et effectuez une recherche dans le contenu enregistré. Ouvrez les enregistrements correspondants et notez l’espace de travail, le chat, l’identifiant du message, la séquence et le hachage de l’enregistrement.

Dans une conversation concernée, ouvrez « **Personnes » → « Activer les profils »** et examinez le profil d’une personne :

- Noms/pseudonymes observés au fil du temps et identifiant numérique Telegram.
- Relations entre les réponses et les références aux enregistrements sources.
- **Également dans…** d’autres discussions de ce journal d’espace de travail où cet identifiant a écrit.
- Activité, modifications/suppressions et mentions de portefeuilles, de téléphones, de noms d'utilisateur et de liens.
- Métadonnées des avatars enregistrés et avatars similaires mis en cache, avec leur origine respective.

Ouvrez les enregistrements cités avant d’utiliser un profil dérivé dans une conclusion. Les profils concernent les personnes dont les messages ont été enregistrés, et non l’ensemble des membres du groupe. **Paramètres → Enregistrements cités par fait : cette option** limite la liste des références, et non le nombre d’activités sous-jacentes. Les mentions et la similitude des avatars constituent des pistes ; elles n’établissent ni la propriété ni l’identité.

Dans l’exemple ci-dessous :

| Lien | Enregistre | Observation étayée |
| --- | --- | --- |
| Même compte d'expéditeur | Groupe n° 146 et discussion privée de suivi n° 205 | Les deux fournissent l'identifiant d'expéditeur Telegram 71001 |
| Même destinataire | #146, clavier du bot #173, modification d'une chaîne #188, message privé #205 | Tous contiennent « `pay.example.invalid/new` » ; la propriété ou le contrôle n’est pas établi. |
| Même fichier enregistré | Réceptions multimédias n° 151 et n° 209 terminées | Les valeurs SHA-256 complètes concordent pour les octets conservés |
| Attribution de la chaîne | #101 et #188 | Ne pas attribuer une publication de chaîne à l’utilisateur 71001 sans mentionner l’expéditeur. |

Comparez les hachages des pièces jointes et les références de messages qui leur sont associées. Des fichiers identiques ne permettent pas d’établir l’identité d’un créateur, d’un expéditeur ou d’un opérateur commun. Des noms identiques et des avatars similaires ne suffisent pas à eux seuls à associer deux identifiants Telegram à une seule et même personne.

## 5. Créer la chronologie inter-discussions

Utilisez les versions enregistrées dans **les discussions** et leurs liens **vers le journal n°…** Dans **le journal**, regroupez **toutes les sources** avec **les modifications**, **les suppressions** et **la couverture**. Conservez à la fois `source_at`, lorsqu’il est fourni, et `observed_at`.

| Exemple de durée d’observation | Référence | Remarque |
| --- | --- | --- |
| 09:00 | Chaîne n° 101 | Destination d'origine enregistrée |
| 09:12 | Groupe n° 146 ; média n° 151 | Nouvelle destination publiée ; téléchargement du fichier terminé |
| 09:16 | Bot n° 173 | Le clavier pointe vers la nouvelle destination |
| 09:20 | Chaîne n° 188 | Annonce modifiée ; les deux versions enregistrées sont conservées |
| 09:24 | Vie privée #205 ; médias #209 | Le même identifiant d’expéditeur correspond à la même destination ; les mêmes octets de fichier sont conservés |
| 09:28 | Groupe n° 231 | Avis de suppression reçu ; auteur de la suppression et heure exacte de la suppression inconnus |

D’autres enregistrements peuvent se situer entre ces exemples de références. Les numéros de séquence classent les observations par ordre chronologique ; les instantanés d’historique peuvent contenir des dates de source plus anciennes et arriver après les événements en temps réel. Distinguez les instantanés, les messages récupérés, les notifications de suppression et les résultats « manquant lors de la vérification ultérieure ». Marquez les lacunes de couverture comme des intervalles inconnus. L’acquisition ultérieure de l’historique n’établit pas rétroactivement une observation ininterrompue.

## 6. Ajouter les points de vue des comptes sans perdre leur origine

Utilisez un espace de travail distinct pour chaque compte et répétez l’inventaire de celui-ci. Conservez l’identifiant du compte, le rôle, l’empreinte de la clé de signature et les références sources à chaque comparaison. Les numéros de message ne constituent pas des identifiants globaux valables pour l’ensemble des discussions et des comptes.

La corrélation entre espaces de travail s’effectue dans des notes de dossier externes ou des outils d’analyse. TgWitness ne dispose actuellement ni de recherche globale inter-espaces de travail, ni de chronologie fusionnée, ni de graphe d’enquête, ni d’archive de dossiers combinée. L’exportation multi-comptes d’**un** canal ou d’un supergroupe constitue une opération distincte, et non une fusion des journaux des comptes.

Pour les travaux de plus grande envergure, veillez à respecter les limites en faisant appel à un [témoin indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/). Utilisez des contrôles de livraison pour valider le chemin de capture et la visibilité de chaque compte.

## 7. Constituer et vérifier le dossier de transfert

Conservez ces éléments ensemble dans un dossier de dossier constitué par un analyste :

| Contenu | Objectif |
| --- | --- |
| Notes d’enquête et registre des sources | Question, politique de collecte, accès/rôle, conclusions, explications alternatives et lacunes |
| Chronologie | Mention des dates ainsi que des références à l’espace de travail, au chat, au message et à la séquence pour chaque entrée |
| Fichier ZIP de preuves signées par espace de travail | Journal complet des enregistrements, manifeste et médias conservés inclus ; les filtres du panneau ne restreignent pas l'exportation du journal |
| Fichiers de profil des personnes signés séparément | Références dérivées vérifiées par rapport aux preuves correspondantes de l’espace de travail |
| Exportations signées de l’intégralité des discussions | Acquisition de l'historique visible en temps réel, distincte du journal d'observation |
| Empreintes fiables et points de contrôle antérieurs | Identité clé et limites du journal conservé |
| Éléments de preuve, s’ils sont configurés | Journal distinct, messages signés et empreinte digitale du témoin |
| Résultats de vérification et hachages des fichiers fournis | Ce qui a été vérifié, quels octets ont été transférés et à qui |

À partir d’une installation de confiance, avec les noms de fichiers et l’empreinte digitale réelle de chaque espace de travail :

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Conservez les résultats de vérification réels et les artefacts d’origine. Le répertoire de cas de premier niveau, le registre des sources et les conclusions des analystes sont gérés en externe ; chaque artefact TgWitness dispose de sa propre signature et de sa propre procédure de vérification.

## Adapter l’enquête

| Cas | Trace | Livrer |
| --- | --- | --- |
| Litige relatif à une commande ou à un paiement géré par un bot | Annonce de l’entrée → aperçu du lien enregistré → paramètre de démarrage du bot → versions « message » et « clavier » → accusés de réception des rappels du panneau → suivi des conversations privées/de groupe | Chronologie des offres et des réponses observée et sources vérifiées ; un lien de paiement ne suffit pas à lui seul à prouver qu’un paiement a bien eu lieu |
| Messages supprimés à la suite d’un incident | Toutes les conversations concernées → originaux et modifications enregistrés → résultats des suppressions ou des éléments manquants lors d’une nouvelle vérification → médias conservés → couverture et autres points de vue des comptes | Versions conservées et intervalles d’inconnues explicites ; aucun acteur de suppression inventé |
| Un participant change de nom d’une conversation à l’autre | Identifiant numérique de l'expéditeur → historique des noms/noms d'utilisateur → réponses → autres conversations observées → destinations/fichiers cités | Une chronologie de l’activité d’un compte Telegram cité, dans laquelle les hypothèses concernant l’identité réelle et les relations sont présentées séparément |

[Référence de la collection](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/) · [Vérification des profils de personnes](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#people-profiles) · [Transfert des preuves](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#investigation-handoff) · [Validation terminée](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/)
