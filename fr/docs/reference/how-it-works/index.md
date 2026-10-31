# Fonctionnement des preuves

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/how-it-works/

Explication de la chaîne de hachage, des signatures, des points de contrôle et des témoins à l’aide des formules exactes utilisées par le vérificateur.

TgWitness conserve ce qu’un compte de collecte a observé, relie ces observations dans un journal signé et permet à une autre personne de vérifier une exportation à l’aide d’une clé de confiance et d’un point de contrôle conservé antérieurement.

Le [site web de documentation local](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally) propose des exemples interactifs à l’adresse `/docs/concepts/`, ainsi qu’un explorateur de décisions « checkpoint » à l’adresse `/docs/witness/`. Tous les messages d’exemple, les nombres et les délais sont fictifs. Les hachages dans le bac à sable de la chaîne sont calculés à l’aide de l’algorithme SHA-256 dans le navigateur. Aucune donnée n’est envoyée à Telegram.

## Un message évolue ; les observations s’accumulent

Diagramme de séquence · Telegram → Collector: Nouveau message : Rendez-vous à 10 h; Collector → Registre signé: Ajouter message.new; Telegram → Collector: Modification : rendez-vous à 11 h; Collector → Registre signé: Ajouter « message.edited »; Telegram → Collector: Avis de suppression; Collector → Registre signé: Ajouter message.deleted; Remarque concernant Registre signé: Les observations relatives aux messages originaux, modifiés et supprimés sont conservées. · Telegram · Collector · Registre signé · Nouveau message : Rendez-vous à 10 h · Ajouter message.new · Modification : rendez-vous à 11 h · Ajouter « message.edited » · Avis de suppression · Ajouter message.deleted · Les observations relatives aux messages originaux,modifiés et supprimés sont conservées.

**Schéma sous forme de texte**

1. Telegram → Collector: Nouveau message : Rendez-vous à 10 h
2. Collector → Registre signé: Ajouter message.new
3. Telegram → Collector: Modification : rendez-vous à 11 h
4. Collector → Registre signé: Ajouter « message.edited »
5. Telegram → Collector: Avis de suppression
6. Collector → Registre signé: Ajouter message.deleted
7. Remarque concernant Registre signé: Les observations relatives aux messages originaux, modifiés et supprimés sont conservées.

Cette séquence simplifiée part du principe que Telegram a bien transmis chaque mise à jour et que le compte sélectionné a pu la consulter. Les événements opérationnels sont également consignés dans le journal. Une notification de suppression n’indique ni l’auteur de la suppression ni l’heure exacte de celle-ci. Les transmissions répétées constituent des observations distinctes ; il n’y a pas de suppression des doublons à l’échelle du journal.

## Ce que couvre un hachage

![Observer, encoder, hacher et signer : chaque nouvel événement inclut le hachage précédent.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Lisez la formule de l’intérieur vers l’extérieur : **C** transforme les neuf champs en octets exacts ; **SHA-256** produit leur condensé ; **« hex »** correspond au format dans lequel ce condensé est stocké. Le hachage précédent se trouve déjà à l’intérieur de l’événement. **« unhex »** retransforme le hachage stocké en 32 octets que Ed25519 signe.

[Schéma statique de la chaîne](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

Soit C(ei) le JSON UTF-8 canonique des neuf champs d’événement. Le premier `previous_hash` est composé de 64 caractères nuls. Chaque enregistrement suivant inclut le hachage hexadécimal de l’ enregistrement précédent :

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

La signature couvre les 32 octets bruts du digest. L’entrée de hachage contient exactement `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` et `previous_hash`. Les clés d’objet sont triées ; les espaces et les échappements ASCII sont omis ; les valeurs NaN et l’infini sont rejetées. Consultez l’ [encodage exact](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#event-canonicalization).

Organigramme · 64 caractères zéro → Enregistrement 1 / hachage h1; Enregistrement 1 / hachage h1 → L'enregistrement n° 2 comprend un titre h1 et un titre h2; L'enregistrement n° 2 comprend un titre h1 et un titre h2 → L'enregistrement n° 3 comprend un h2 / un h3; L'enregistrement n° 3 comprend un h2 / un h3 → Point de contrôle signé : count 3, balise h3 (conserver ailleurs) · 64 caractères zéro · Enregistrement 1 /hachage h1 · L'enregistrement n° 2comprend un titre h1et un titre h2 · L'enregistrement n° 3comprend un h2 / un h3 · Point de contrôlesigné : count 3,balise h3 · conserver ailleurs

**Schéma sous forme de texte**

1. 64 caractères zéro → Enregistrement 1 / hachage h1
2. Enregistrement 1 / hachage h1 → L'enregistrement n° 2 comprend un titre h1 et un titre h2
3. L'enregistrement n° 2 comprend un titre h1 et un titre h2 → L'enregistrement n° 3 comprend un h2 / un h3
4. L'enregistrement n° 3 comprend un h2 / un h3 → Point de contrôle signé : count 3, balise h3 (conserver ailleurs)

| Modification apportée au journal fourni | Ce qui le caractérise |
| --- | --- |
| Modifier l'enregistrement n° 2 tout en conservant son hachage enregistré | Le hachage de l’événement recalculé diffère ; sa signature ne couvre plus l’événement modifié |
| Reconstituez l'enregistrement modifié ainsi que chaque hachage ultérieur | Les signatures d’origine sont invalides ; un point de contrôle conservé au niveau de la limite concernée présente également une divergence. |
| Supprimez la partie finale tout en conservant le préfixe restant intact | Un point de contrôle antérieur conservé, situé au-delà du préfixe fourni, révèle que l’exportation est trop courte |
| Resigner un journal de remplacement avec une autre clé | Une empreinte de clé fiable, distincte, rejette l’identité de remplacement |

![La modification d’un champ enregistré modifie son condensé ; le recalcul des hachages ne permet pas de restaurer les signatures d’origine.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**Testez ce principe sur l’enregistrement n° 2 :** remplacez « `Meet at 11:00` » par « `Meet at 12:00` » dans l’ événement enregistré. Son hachage recalculé ne correspond plus. Le recalcul de la chaîne ultérieure peut réparer ses liens, mais ne permet pas aux signatures d’origine de couvrir les nouveaux résumés. En revanche, une modification observée sur Telegram donne lieu à un nouvel enregistrement dans le journal.

[Diagramme des modifications statiques](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

Les liens de hachage ne suffisent pas à eux seuls à empêcher quiconque de recalculer une chaîne de remplacement. La confiance repose sur la vérification des signatures à l’aide d’une clé de confiance indépendante et sur la comparaison avec des références conservées en dehors du collecteur.

## Ce qu’ajoute un point de contrôle antérieur

![Conservez le compteur à 3 et la balise h3 ; une exportation ultérieure de 4 enregistrements est vérifiée à la position 3.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**La référence reste inchangée tandis que le journal s’enrichit.** Si le point de contrôle indique « 3 enregistrements, en-tête h3 », une exportation de quatre enregistrements peut être validée en faisant correspondre h3 à la position 3. Son en-tête le plus récent est h4, qui est censé être différent. Une exportation ne comportant que deux enregistrements échoue.

[Schéma statique des points de contrôle](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

Après avoir vérifié la signature du point de contrôle, exigez :

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

Une exportation peut s’étendre au-delà d’un point de contrôle. Elle doit correspondre à la limite conservée. Le vérificateur réel contrôle également la séquence de chaque événement, le lien précédent, le hachage et la signature. Se contenter de comparer uniquement l’en-tête finale stockée permettrait de passer à côté d’un enregistrement interne altéré dont le hachage enregistré n’aurait pas été mis à jour.

## La place d’un témoin

Organigramme · Collecteur / session de compte / clé A → Point de contrôle en lecture seule; Witness / clé de collecte épinglée / clé personnelle B → Journal de témoignage signé distinct; Witness / clé de collecte épinglée / clé personnelle B → Point de contrôle en lecture seule (Demander une vérification); Point de contrôle en lecture seule → Witness / clé de collecte épinglée / clé personnelle B (Réponse signée); Witness / clé de collecte épinglée / clé personnelle B → Chaîne contenant des publications TGW1 signées (API du bot / jeton personnel) · Hôte A · Hébergeur B · Collecteur / session decompte / clé A · Point de contrôle enlecture seule · Witness / clé de collecteépinglée / clé personnelleB · Journal de témoignagesigné distinct · Chaîne contenant despublications TGW1 signées · Demander une vérification · Réponse signée · API du bot / jeton personnel

**Schéma sous forme de texte**

1. Collecteur / session de compte / clé A → Point de contrôle en lecture seule
2. Witness / clé de collecte épinglée / clé personnelle B → Journal de témoignage signé distinct
3. Witness / clé de collecte épinglée / clé personnelle B → Point de contrôle en lecture seule (Demander une vérification)
4. Point de contrôle en lecture seule → Witness / clé de collecte épinglée / clé personnelle B (Réponse signée)
5. Witness / clé de collecte épinglée / clé personnelle B → Chaîne contenant des publications TGW1 signées (API du bot / jeton personnel)

Le témoin enregistre les annulations, les en-têtes différents pour un même compteur, les clés modifiées, les réponses non valides et les réponses manquantes. Un compteur plus élevé ne suffit pas à lui seul à établir que tous les enregistrements antérieurs sont restés inchangés ; comparez l’exportation avec les points de contrôle conservés. Un témoin hébergé sur un autre serveur évite de subir la panne du serveur du collecteur ; un opérateur distinct apporte une indépendance supplémentaire.

Le « witness » certifie l’état du journal tel que signalé par le collecteur. Il n’ observe pas de manière indépendante l’ensemble des messages Telegram. Voir [la configuration du « witness](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/) ».

## Test de mise en œuvre par rapport à des actions connues

Utilisez un groupe contrôlé, des comptes de collecte distincts et un marqueur vierge. Envoyez, modifiez et supprimez délibérément, en vérifiant la capture entre chaque étape. Définissez les actions attendues et une date limite avant d’examiner les résultats.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Seules les actions conformes aux attentes sont prises en compte ; les reçus en double n’augmentent pas le numérateur. Le dénominateur doit être différent de zéro. Un reçu manquant n’entraîne aucun retard mesuré. Indiquez l’incertitude relative à l’horodatage ; utilisez votre propre durée de suppression contrôlée, car Telegram ne fournit pas l’heure exacte de suppression. Un résultat tel que 5/6 (83,3 %) décrit les actions testées, et non l’exhaustivité de l’ensemble du trafic Telegram.

## Choisissez un flux de travail

[Le guide complet de l’enquête](https://phishdestroy.github.io/TgWitness/fr/docs/reference/investigation/) suit le déroulement d’un incident sur un canal, dans un groupe, via un bot et dans une conversation privée :

1. Activez le mode « Enquête sur l’ensemble du compte » et répertoriez toutes les discussions accessibles.
2. Récupérez des instantanés du journal, l'historique complet de chaque conversation et les pièces jointes conservées.
3. Conservez les modifications en temps réel ainsi que toutes les interactions délibérées avec les panneaux, accompagnées de leurs justificatifs.
4. Suivez les identifiants numériques des expéditeurs, les relations de réponse, les destinataires récurrents et les hachages de fichiers à travers les enregistrements cités et les profils des personnes.
5. Reconstituez une chronologie inter-discussions comprenant à la fois des horodatages et des lacunes explicites.
6. Comparez les espaces de travail d’autres comptes tout en conservant leurs origines et leurs clés distinctes.
7. Compilez et vérifiez les journaux signés, les profils et les exportations d’historique à l’aide des notes de dossier.

Le guide « `/docs/cases/` » du site web comprend une carte interactive des dossiers ainsi que des variantes pour les litiges impliquant des bots, les messages supprimés et les participants changeant de nom. Les notes de dossier et l’analyse inter-espaces de travail sont externes ; l’application ne génère pas automatiquement de graphe d’enquête global ni d’archive de dossiers fusionnés.

[Validation terminée et travaux restants](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/) · [Exporter et vérifier](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#investigation-handoff) · [Commencez par un seul compte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/quickstart/)
