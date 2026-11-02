# Concevoir un rapport

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reports/

Indiquez clairement au lecteur le chemin à suivre depuis la question relative à l’affaire jusqu’aux enregistrements sauvegardés.

Report Studio combine une sélection de données, des historiques de modifications lisibles, des graphiques et vos conclusions écrites. Huit modèles intégrés s’appliquent aux formats de sortie pris en charge : HTML et PDF natif. Les rapports HTML, PDF et JSON comportent leurs propres sceaux signés ; le manifeste ZIP regroupe également les fichiers dans l’archive. Les fichiers HTML et PDF sont scellés une fois leur mise en page finale terminée.

## Créer un rapport en trois étapes

1. Ouvrez **Exports → Configurer et prévisualiser → Données**. Utilisez l’ensemble de l’espace de travail ou sélectionnez des discussions, des auteurs, des dates d’observation UTC inclusives et des types d’enregistrements. Les dates indiquent quand TgWitness a observé l’enregistrement.
2. Dans « **Design & contents** », choisissez un modèle de mise en page et de contenu. Sélectionnez les graphiques d’activité, les étiquettes des participants, la transcription, les modifications enregistrées et les éléments facultatifs du « Case Board ». Ajoutez les détails de votre dossier et vos notes d’examen.
3. Ouvrez **« Aperçu »** pour vérifier les nombres, l’activité, les participants, les enregistrements échantillonnés et les plages d’identifiants manquantes. Enregistrez les paramètres, puis téléchargez le format dont vous avez besoin.

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

**Les rubriques « Classique », « Éditorial », « Briefing », « Analytique », « Technique », « Aperçu », « Série de lectures » et « Grand livre et marge** **»** présentent les mêmes enregistrements sous-jacents selon différentes mises en page. La modification de la mise en page conserve la sélection des données et les notes écrites. La langue du rapport peut être choisie parmi les 25 langues prises en charge.

La « Reading series » regroupe le dossier, le périmètre, les conclusions et les modifications autour d’une colonne de section. « Ledger & margin » utilise des chapitres numérotés et une large marge. Les deux formats prennent également en charge les aperçus HTML des comptes et le partage de copies. Les PDF natifs sont générés avec les polices intégrées ; l’ordinateur de l’utilisateur ne nécessite aucune installation de navigateur ou de Node pour la création de PDF. Les PDF en chinois, japonais et coréen nécessitent en outre une police adaptée sur le serveur, telle que Noto Sans CJK, installée à l’échelle du système ou placée dans `TGWITNESS_FONT_DIR`. En son absence, l’archive ZIP conserve les rapports HTML et JSON.

## Lire une modification en tenant compte de son contexte

Les modifications enregistrées s’affichent « avant » et « après ». Une notification de suppression peut être accompagnée de la dernière version capturée. Les réponses, citations, partages, réactions, boutons et métadonnées des pièces jointes conservent leurs références disponibles. Les hachages SHA-256 des fichiers et des enregistrements du journal sont indiqués séparément.

L’aperçu de la mise en page présente la couverture, l’analyse et les graphiques à partir d’enregistrements correspondants parmi les 50 000 premiers enregistrements sources. L’aperçu séparé des données analyse l’intégralité de l’instantané stable du journal pour obtenir le nombre exact d’éléments sélectionnés, avec indication des limites d’échantillonnage affichées. Générez un PDF pour vérifier la pagination finale. L’exportation complète du compte comporte un aperçu au format HTML ; ses fichiers PDF individuels de discussion utilisent la mise en page choisie.

## Choisissez soigneusement la version destinée au destinataire

Les filtres de rapport permettent de structurer un rapport lisible. Le fichier ZIP complet des preuves conserve le journal d’origine et les pièces jointes. Utilisez un [transfert allégé](https://phishdestroy.github.io/TgWitness/fr/docs/handover/) lorsque le destinataire ne doit recevoir que des données sélectionnées. Consultez [le contenu du rapport et procédez à sa vérification,](https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-reports/) ou [vérifiez l’exportation terminée](https://phishdestroy.github.io/TgWitness/fr/docs/exports/).
