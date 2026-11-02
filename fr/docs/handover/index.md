# Préparez une copie à partager

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/handover/

Partagez les observations pertinentes tout en conservant l'espace de travail d'origine intact.

Un transfert correspond à un extrait distinct et signé. Choisissez les discussions et les personnes concernées, masquez les identités ou le texte, et déterminez quels fichiers et notes d’équipe doivent figurer dans la copie du destinataire. Son manifeste répertorie la sélection ainsi que le nombre d’enregistrements inchangés, réduits et omis.

## Préparez l'extrait destiné au destinataire

1. Ouvrez **Exports → Handover extract**. Indiquez son objectif, choisissez les discussions et, si vous le souhaitez, la période UTC, puis sélectionnez « **Charger les participants » des discussions choisies** si vous avez besoin des noms des personnes concernées.
2. Choisissez comment traiter les autres intervenants : utilisez des pseudonymes, omettez leurs messages ou affichez-les tels qu’ils ont été enregistrés. Définissez le texte des messages et les pièces jointes séparément ; vous pouvez également masquer les numéros de téléphone et les adresses e-mail.
3. Choisissez d'inclure les signets et les extraits de « Case Board », ou les fiches avec commentaires. Les pseudonymes des enquêteurs peuvent remplacer les noms d'équipe dans ce texte.
4. Sélectionnez « **Télécharger l'extrait de transfert** ». Ouvrez localement le rapport généré et les enregistrements sélectionnés, vérifiez l'archive et inspectez la copie avant de l'envoyer.

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
| Personnes | Veillez à ce que les personnes concernées restent identifiables ; pseudonymisez ou omettez les autres participants selon les instructions. |
| Texte | Inclure l'intégralité du texte, uniquement le texte des personnes sélectionnées et du compte d'observation, ou omettre le texte des messages et ses champs de détails contenant du texte. |
| Fichiers | Choisissez les fichiers des personnes sélectionnées et du compte surveillé, tous les fichiers des messages affichés, ou aucun fichier. |
| Case Board | Ne pas inclure de contenu de tableau, de signets ni de « slices », ni de fiches avec des discussions d’équipe. |

Vérifiez le contenu des textes libres et des fichiers, ainsi que les identités : un pseudonyme ne supprime pas automatiquement tous les noms figurant dans un message ou une pièce jointe. Si un fichier préservé sélectionné n’est pas disponible, restaurez-le ou omettez explicitement les pièces jointes avant de générer l’extrait.

## Veillez à ce que le texte puisse être vérifié de manière indépendante.

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Conservez séparément l’archive originale des preuves signées et les points de contrôle. Le transfert enregistre sa propre projection, ce qui permet au destinataire de vérifier la copie transmise sans recevoir l’intégralité de l’espace de travail. [Report Studio](https://phishdestroy.github.io/TgWitness/fr/docs/reports/) fournit sa mise en page de lecture ; [la vérification de l’exportation](https://phishdestroy.github.io/TgWitness/fr/docs/exports/) explique les références fiables.
