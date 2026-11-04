# Concevoir un rapport

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reports/

Menez le lecteur de la question de l’affaire directement aux entrées enregistrées.

Report studio rassemble les données choisies, les historiques de modifications, les graphiques et vos conclusions. Huit modèles, HTML et PDF natif. Chaque rapport HTML, PDF et JSON est scellé avec votre clé.

## Créer un rapport en trois étapes

1. **Exports → Configurer et prévisualiser → Données** : l’espace entier, ou les chats, auteurs, dates (UTC, quand TgWitness a vu l’entrée) et types d’entrées que vous choisissez.
2. **Modèle et contenu** : choisissez un modèle et ce qui y figure : graphiques, participants, transcription, modifications, éléments Case Board, détails de l’affaire et notes.
3. **Aperçu** : vérifiez les décomptes, l’activité, les échantillons et les plages d’ID manquantes. Enregistrez, puis téléchargez le format voulu.

### Organisez les éléments enregistrés de manière cohérente pour le lecteur

Exemple synthétique · mise en page schématique, il ne s'agit pas d'un rapport généré

1. **Sélectionnez.** Choisissez deux discussions et la période d’observation pour le dossier.
2. **Rédigez le texte.** Choisissez une mise en page et les sections qui répondent à la question.
3. **Aperçu.** Vérifiez le nombre de occurrences sélectionnées et le texte « avant » et « après » enregistré.
4. **Vérifier.** Générer le fichier final et vérifier sa signature par rapport à l'empreinte digitale de l'espace de travail de confiance.

#### Observations sélectionnées

2 discussions · 1 journée d’observation

Messages, modifications et notifications de suppression

#### Structure du rapport

##### Modification du destinataire du paiement

Question relative à l’affaire → périmètre → conclusions → références des enregistrements

**Contexte du message**

Remarque n° 142 : « Utilisez le nouveau lien de paiement. »

**Modifications enregistrées**

Avant : old.example.invalid → Après : new.example.invalid

#### Vérifier la sélection

18 observations · 2 modifications enregistrées

Les heures d’envoi, de modification et d’observation sont indiquées par des libellés distincts.

#### Livrable final

PDF signé + JSON signé, ou un fichier ZIP signé contenant son rapport lisible

Le destinataire vérifie le fichier et l’empreinte numérique certifiée.

## Choisissez un style de lecture

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin** : les mêmes entrées, un autre rendu. Changer de modèle garde la sélection et les notes. N’importe laquelle des 25 langues.

Les PDF sont produits avec des polices fournies, sans navigateur. Le chinois, le japonais et le coréen nécessitent une police comme Noto Sans CJK sur le serveur (dans le système ou dans `TGWITNESS_FONT_DIR`) ; sinon vous n’obtenez que HTML et JSON.

## Lire une modification en tenant compte de son contexte

Les modifications montrent avant et après, les suppressions la dernière version enregistrée. Réponses, transferts, réactions, boutons et pièces jointes gardent leurs références.

L’aperçu du modèle utilise les 50 000 premières entrées, l’aperçu des données compte tout exactement. Pour la mise en page finale, générez le PDF.

## Choisissez soigneusement la version destinée au destinataire

Les filtres ne façonnent que le rapport ; le ZIP de preuves contient toujours le journal et les fichiers complets. Si le destinataire doit recevoir moins, utilisez une [transmission minimisée](https://phishdestroy.github.io/TgWitness/fr/docs/handover/). Plus : [contenu du rapport](https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-reports/), [vérifier l’export](https://phishdestroy.github.io/TgWitness/fr/docs/exports/).
