# Créer un « Case Board »

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/case-board/

Transformez les observations Telegram enregistrées en un dossier que votre équipe pourra examiner ensemble.

Case Board conserve les signets, les passages surlignés en texte exact, les extraits enregistrés et les discussions à côté de leurs références sources. Une collection donne à l’affaire une structure de travail ; les révisions signées permettent de retracer l’évolution du dossier au sein de l’équipe.

## D’un message à une fiche d’affaire

1. Ouvrez « **Investigation » → « Case Board »** en mode « Standard » ou « Expert ». Créez une collecte pour l'affaire et choisissez la portée de la discussion.
2. Dans **le Journal** ou une conversation enregistrée, choisissez **« Ajouter au tableau** » ou sélectionnez l’enregistrement puis appuyez sur **B**. La fiche est ajoutée à la Boîte de réception ; donnez-lui un titre pertinent et déplacez-la vers votre collection.
3. Sélectionnez un passage dans un message de discussion enregistré, puis choisissez **« Mettre en surbrillance » → « Tableau »** pour conserver la citation exacte et la version originale du message. Ajoutez une note expliquant en quoi cela est important.
4. Discutez de la fiche, attribuez-lui un statut de révision et revenez à son contexte d’origine chaque fois qu’une affirmation doit être vérifiée. Utilisez **la fonction « Présentation »** pour parcourir la collecte avec vos collègues.

### Suivre un lien de paiement modifié

Exemple synthétique · illustration locale

1. **Capture.** Ouvrez l’observation enregistrée n° 142 et sa version de message.
2. **Ajouter aux favoris.** Conservez la citation, la référence de la source et votre question sur une fiche.
3. **Révision.** Ajoutez un commentaire d'équipe et déplacez la fiche vers « Révision ».
4. **Présenter.** Parcourir la collecte et ouvrir le contexte de la source citée.

#### Observation enregistrée n° 142

« Utilisez le nouveau lien de paiement. »

Chat des opérations · message 38 · observé à 09h12 UTC

#### Fiche : destination modifiée

> Utilisez le nouveau lien de paiement.

Question : quelle destination figurait dans la version précédente ?

#### Révision par l'équipe

Analyste : à comparer avec l’observation n° 101.

Statut : Révision · version conservée

#### Contexte de la source

Fiche → version enregistrée → observation antérieure

Les annotations et l’observation des messages Telegram restent identifiables séparément.

## Enregistrer une plage utile une seule fois

Cliquez en maintenant la touche Maj enfoncée sur deux enregistrements dans une même conversation pour **effectuer** **une « Slice » entre eux**, choisissez **«** **Slice by time** » (Découper **par heure**) ou enregistrez les filtres actuels du Journal. Vérifiez le nombre d’enregistrements avant d’enregistrer. Rouvrez la « Slice » pour appliquer la requête enregistrée ; l’option **« Show records added since bookmark » (**Afficher les enregistrements **ajoutés depuis le signet)** permet de visualiser les ajouts ultérieurs.

Une tranche temporelle suit l’heure d’observation du collecteur. Une tranche d’identifiants de messages peut suivre les messages sélectionnés à mesure que des modifications ultérieures surviennent. La limite de création enregistrée permet à un destinataire de comparer la sélection d’origine avec son état ultérieur.

## Attribuez à chaque collègue le rôle qui lui correspond

**Le réviseur** consulte le tableau ; **l’analyste** ajoute des fiches et des commentaires ; **l’opérateur** gère également les collectes et les décisions de révision. Les autorisations d’accès à l’espace de travail et au chat s’appliquent aux fiches, au contexte des sources et aux discussions. Utilisez des autorisations d’accès nommées pour une attribution claire.

## Transposer ce travail en un livrable

Exportez une tranche au format JSON signé, ou utilisez le format CSV pour une feuille de calcul. Les paramètres du rapport peuvent inclure des signets et des tranches, ainsi que des commentaires de l’équipe si cette option est sélectionnée. Sélectionnez ces éléments dans [Report Studio](https://phishdestroy.github.io/TgWitness/fr/docs/reports/) ; une tranche enregistrée ne configure pas automatiquement un rapport. Pour un destinataire soumis à des restrictions d’accès, utilisez les [commandes de transfert](https://phishdestroy.github.io/TgWitness/fr/docs/handover/) dédiées.

Consultez la [référence relative au « Case Board »](https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-board/) pour les révisions signées, la correspondance exacte des citations, la vérification des sélections et les autorisations.
