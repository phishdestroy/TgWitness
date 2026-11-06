# Découvrez comment fonctionne la conservation des preuves

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/concepts/

Les messages changent. Votre trace de ce que vous avez vu ne devrait pas changer, et tout le monde devrait pouvoir le vérifier.

Deux petites expériences ci-dessous. Messages fictifs, tout tourne dans votre navigateur, rien ne part vers Telegram.

## D’une exportation de discussion à un enregistrement vérifiable

Un [export Telegram Desktop](https://telegram.org/blog/export-and-more) enregistre l’historique visible à l’instant en HTML ou JSON. TgWitness y ajoute un journal continu des changements, des signatures sur chaque entrée et des points de contrôle auxquels d’autres peuvent se comparer.

| Mission | Exportation depuis Telegram Desktop | TgWitness |
| --- | --- | --- |
| Lire les conversations enregistrées | HTML ou JSON avec les médias sélectionnés | Conversations enregistrées, journal consultable et rapports hors ligne |
| Suivre une évolution dans le temps | L'historique disponible lors de l'exportation | Anciennes versions, modifications ultérieures et suppressions, tout est gardé |
| Vérifier les fichiers après le transfert | Les fichiers d'exportation HTML/JSON standard ne sont pas signés. | Manifeste signé, entrées signées et rapports scellés, vérifiés avec une clé de confiance |
| Comparer avec un état antérieur conservé | Conserver une copie de référence distincte ou un hachage | Points de contrôle signés, témoin distinct et horodatages externes facultatifs |

La comparaison s’appuie sur le [code d’export de Telegram Desktop](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output) au 2 novembre 2026.

## Un message, trois observations

Un nouveau message, une modification et une suppression deviennent trois entrées distinctes. La modification n’écrase pas la première et la suppression ne l’efface pas.

01 / PARCOURS DU MESSAGESéquence illustrative

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Collecteur · Journal · mise à jour → · ajouter →

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

Telegram ne dit pas qui a supprimé un message ni quand exactement. TgWitness laisse ces champs vides au lieu de deviner.

## Modifier un enregistrement. Suivre le hachage.

Chaque entrée contient le hachage de la précédente. Un point de contrôle conservé ailleurs fixe la longueur du journal et le dernier hachage.

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

**C** désigne les neuf champs de l’événement en JSON UTF-8 : clés triées, pas d’espaces superflus, pas d’échappement ASCII, pas de NaN/infini. `previous_hash` vaut hi−1, h0 correspond à 64 zéros et les signatures couvrent les 32 octets bruts du condensé.

Les champs : `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. Spécification complète : [encodage des événements](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#event-canonicalization).

POINT DE CONTRÔLE CONSERVÉ

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Vérifiez la signature du point de contrôle avec la clé épinglée, puis comparez-le au journal. Un export ultérieur peut être plus long, mais il doit concorder au point de contrôle.

## Trois questions, trois vérifications différentes

[01 / INTÉGRITÉ**Cet enregistrement a-t-il été modifié ?** Hachages et signatures face à une clé de confiance.](https://phishdestroy.github.io/TgWitness/fr/docs/exports/)[02 / CONTINUITÉ**Qu’est-ce qui a été conservé précédemment ?** Comparez l’export aux points de contrôle conservés par un témoin.](https://phishdestroy.github.io/TgWitness/fr/docs/witness/)[03 / LIVRAISON**Ces événements de test sont-ils bien arrivés ?** Envoyez, modifiez et supprimez des messages de test, puis regardez ce que chaque compte a capté.](https://phishdestroy.github.io/TgWitness/fr/docs/cases/)

Les signatures répondent à « a-t-on modifié ? », les points de contrôle à « est-ce conforme à ce qui existait avant ? » et les messages de test à « a-t-on tout capté ? ». [Ce que la vérification prouve et ce qu’elle ne prouve pas.](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#verification-scope)

Ensuite : une [enquête sur un compte entier](https://phishdestroy.github.io/TgWitness/fr/docs/cases/), du début jusqu’au dossier final.

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
