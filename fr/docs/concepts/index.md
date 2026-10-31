# Découvrez comment fonctionne la conservation des preuves

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/concepts/

Un message peut être modifié. L'enregistrement de ce que vous avez observé doit rester vérifiable.

Découvrez ci-dessous deux petites expériences. Elles utilisent des messages fictifs, s'exécutent directement dans votre navigateur et ne se connectent jamais à Telegram.

## Un message, trois observations

Lorsque Telegram transmet un nouveau message, une modification ou une notification de suppression, l’outil d’enregistrement ajoute trois observations distinctes. La modification ne remplace pas l’enregistrement initial. Une notification de suppression ne l’efface pas.

01 / PARCOURS DU MESSAGESéquence illustrative

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Collector · Journal · mise à jour → · ajouter →

AFFICHAGE ACTUEL DE LA CONVERSATION Message n° 42

Message supprimé

Le message a disparu de la vue de la conversation.

JOURNAL D'OBSERVATION 3 entrées

1. 01

   `message.new`

   Rendez-vous à 10 h

   ✓
2. 02

   `message.edited`

   Rendez-vous à 11 h

   ✓
3. 03

   `message.deleted`

   Avis de suppression n° 42

   ✓

Les trois observations reçues sont conservées dans le journal.

Parcours simplifié pour une source déjà sélectionnée. Les registres opérationnels partagent également le journal réel. La capture dépend de ce que le compte peut voir et de ce que Telegram transmet.

Une notification de suppression ne fournit ni l’heure exacte de la suppression, ni l’identité de la personne ayant supprimé le message. Le fait de ne pas divulguer ces informations permet de préserver la distinction entre une observation et une supposition.

## Modifier un enregistrement. Suivre le hachage.

Chaque enregistrement contient le hachage de l’enregistrement précédent. Son propre hachage couvre les champs d’événement, y compris ce lien. Un point de contrôle conservé en externe fixe une longueur spécifique du journal et le hachage de tête.

02 / HASH-CHAIN SANDBOXSHA-256 réel · exemples d'enregistrements

ENREGISTREMENT 01**Message reçu**`h₁ = SHA-256(e₁)`Liens vers 64 zéros

ENREGISTREMENT 02**Rendez-vous à 11 h**`h₂ = SHA-256(e₂)`Comprend h₁

ENREGISTREMENT 03**Suppression constatée**`h₃ = SHA-256(e₃)`Comprend h₂

CONSERVÉ AILLEURS**3 entrées · en-tête `h₃`**Comparez cette limite fixe avec le journal fourni.

La modification d’un événement modifie son hachage. La reconstruction de la chaîne modifie son début. La suppression de la fin rend la chaîne plus courte que le point de contrôle conservé.

**Consultez l'enregistrement n° 2 et l'ensemble des hachages**

Il s'agit ici du JSON UTF-8 exact soumis à un hachage dans cet exemple. Les valeurs sont fictives ; les neuf champs et la sérialisation correspondent au format du journal.

```

```

Hachage de l'enregistrement n° 2

``

Hash de l'enregistrement n° 2 recalculé

``

Ce bac à sable calcule des hachages, et non des signatures. Le véritable vérificateur contrôle également la signature Ed25519, la séquence et le lien de chaque événement. La reconstruction des hachages ne suffit pas à elle seule à créer des signatures valides sous la clé de confiance.

## Les règles proprement dites, en quelques lignes

HACH + SIGNATURE

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** sérialise les neuf champs d’événement au format JSON UTF-8 : clés triées, sans espaces supplémentaires, sans échappement ASCII et sans NaN/infini. La valeur `previous_hash` de l’événement est hi−1. La valeur h0 affichée correspond à 64 caractères nuls ; les signatures couvrent les 32 octets bruts du résumé.

Les neuf champs sont `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` et `previous_hash`. Il s’agit [du codage JSON documenté](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#event-canonicalization) de TgWitness ; le hachage et la signature eux-mêmes ne constituent pas des champs de saisie de hachage.

POINT DE CONTRÔLE CONSERVÉ

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Vérifiez la signature du point de contrôle sous la clé de collecte épinglée, puis comparez ses limites avec celles du journal vérifié. Une exportation ultérieure peut contenir davantage d’enregistrements ; elle doit néanmoins correspondre au point de contrôle précédent.

## Trois questions, trois vérifications différentes

[01 / INTÉGRITÉ**Cet enregistrement a-t-il été modifié ?** Vérifiez les hachages et les signatures à l’aide d’une clé de confiance distincte.](https://phishdestroy.github.io/TgWitness/fr/docs/exports/)[02 / CONTINUITÉ**Qu’est-ce qui a été conservé précédemment ?** Comparez une exportation signée avec des points de contrôle conservés par un témoin distinct.](https://phishdestroy.github.io/TgWitness/fr/docs/witness/)[03 / LIVRAISON**Ces événements de test sont-ils bien arrivés ?** Comparez les actions contrôlées d’envoi, de modification et de suppression avec le journal de chaque compte.](https://phishdestroy.github.io/TgWitness/fr/docs/cases/)

Une chaîne de hachages correspondante répond à une question d’intégrité. Elle ne prouve pas la livraison complète du message sur Telegram, la véracité d’un message ni l’heure d’observation de manière indépendante et fiable.

Suivez l'[enquête complète sur le compte,](https://phishdestroy.github.io/TgWitness/fr/docs/cases/) de l'acquisition jusqu'au dossier d'affaire.
