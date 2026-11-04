# Préparez une copie à partager

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/handover/

Ne partagez que le nécessaire, l’original reste intact.

Une transmission est un extrait signé séparé : choisissez chats et personnes, masquez identités ou texte, décidez quels fichiers et notes d’équipe y vont. Le manifeste consigne ce qui a été gardé, réduit et écarté.

## Préparez l'extrait destiné au destinataire

1. **Exports → Extrait de transmission** : indiquez l’objectif, choisissez chats et période, puis **Charger les personnes des chats choisis** si vous avez besoin de personnes nommées.
2. Les autres : pseudonymes, écartés ou tels qu’enregistrés. Texte et fichiers sont des interrupteurs séparés ; téléphones et e-mails peuvent être masqués.
3. Case Board : rien, signets et extraits, ou cartes avec commentaires. Les noms de l’équipe peuvent être remplacés par des alias.
4. **Télécharger l’extrait de transmission**, ouvrez-le, vérifiez-le, relisez-le avant de l’envoyer.

### Un original, une copie destinée au partage

Exemple de synthèse · à titre d’illustration uniquement

1. **Sélectionner.** Inclure la conversation relative à l’affaire et identifier la personne concernée par l’extrait.
2. **Réduire.** Choisissez la manière dont un autre participant apparaît dans la copie partagée.
3. **Vérifiez.** Ouvrez le rapport et les enregistrements de l'archive générée avant de l'envoyer.
4. **Partage.** Fournissez la copie vérifiée et communiquez séparément son empreinte numérique certifiée.

#### Observation originale

Nora · utilisateur 71002

« J’ai bien reçu le lien mis à jour. »

Le journal source conserve cette observation enregistrée.

#### Copie destinée au destinataire

Afficher tel qu’enregistré : Nora · utilisateur 71002 · « J’ai reçu le lien mis à jour. »

Pseudonyme : P01 · « J’ai bien reçu le lien mis à jour. »

À omettre : le message de ce participant n'est pas repris dans le texte.

#### Examinez les fichiers réels

Lire les fichiers report.html et records.jsonl.

Vérifiez les identités, le texte, les pièces jointes et les commentaires facultatifs de l'équipe.

#### Extrait signé

Sélection + hachages de fichiers + manifeste signé

Un dossier distinct lié aux limites du journal source

## Utilisez ces éléments de manière combinée

| Contrôle | Impact sur le texte |
| --- | --- |
| Personnes | Les personnes choisies restent nommées ; les autres reçoivent un pseudonyme ou sont écartées. |
| Texte | Tout le texte, seulement celui des personnes choisies et de votre compte, ou aucun. |
| Fichiers | Fichiers des personnes choisies et de votre compte, tous les fichiers affichés, ou aucun. |
| Case Board | Rien, signets et extraits, ou cartes avec discussion. |

Lisez aussi le texte et les fichiers : un pseudonyme n’efface pas les noms écrits dans un message ou une pièce jointe. S’il manque un fichier choisi, restaurez-le ou écartez les pièces jointes.

## Veillez à ce que le texte puisse être vérifié de manière indépendante.

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Gardez vous-même l’archive originale et les points de contrôle. Le destinataire peut vérifier sa copie sans recevoir tout l’espace. Mise en forme : [Report studio](https://phishdestroy.github.io/TgWitness/fr/docs/reports/). Références de confiance : [vérification de l’export](https://phishdestroy.github.io/TgWitness/fr/docs/exports/).
