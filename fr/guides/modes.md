# Un journal. Quatre modes de collecte. Huit niveaux de vérification.

Canonical page: https://phishdestroy.github.io/TgWitness/fr/guides/modes.html

Modes, scénarios et niveaux de preuve

TgWitness Enregistre ce que le compte connecté observe. Un tiers peut vérifier l’intégrité de l’enregistrement par rapport à une clé de confiance indépendante.

[Modes de collecte](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html#scope)[Scénarios](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html#scenarios)[Niveaux de preuve](https://phishdestroy.github.io/TgWitness/fr/guides/modes.html#levels)

Présentation de 3 à 5 minutes · exemples fictifs · implémentation actuelle

1. **Telegram**

   Mises à jour visibles sur le compte
2. **Collecteur**

   Enregistrements liés, chacun signé
3. **Vérificateur**

   Clé de confiance + limite conservée

`h₁ → h₂ → h₃ · Ed25519`L’intégrité est vérifiée. L’origine du message sur Telegram et la véracité de celui-ci restent deux questions distinctes.

## Choisissez le champ d’observation

Trois champs d’application et un préréglage d’enquête. Les exclusions et les types de sources activés s’appliquent toujours.

Par défaut**Discussions sélectionnées**

Enregistrements

Uniquement des sources sélectionnées manuellement.

Nouvelles discussions

Non ajouté automatiquement.

Choisissez

Un ensemble connu de canaux ou de groupes. Aucune capacité de discussion fixe n’a été spécifiée.

**Ne fait pas** Il ne détecte pas d’autres discussions et ne reconstitue pas l’historique antérieur.

Dossier « Account »**Dossier Telegram**

Enregistrements

Inclusions de dossiers et catégories, moins les exclusions et les discussions archivées lorsqu’elles sont configurées.

Nouvelles discussions

Correspondance des discussions actives ; modifications des dossiers dans l’heure qui suit.

Choisissez

Un analyste gère déjà un dossier de suivi. Vérifiez que la collecte s’effectue sur un compte dédié.

**Ne fait pas** Elle ne tient pas compte des conditions changeantes muted/read du dossier.

Confirmez le champ d’application**Compte complet**

Enregistrements

Les discussions visibles par le compte, y compris les conversations privées et les bots, au sein des types sélectionnés.

Nouvelles discussions

Ajouté dès la première mise à jour.

Choisissez

Un compte dédié à l’observation, y compris un compte participant à une affaire.

**Ne fait pas** Il ne rejoint pas automatiquement les discussions et ne contourne pas l’accès à la source.

Préréglage pour l'ensemble du compte**Mode d’enquête**

Enregistrements

Tous les types de sources, les actions propres, les profils de sources et les 200 derniers messages visibles des sources nouvellement découvertes.

Nouvelles discussions

Une nouvelle conversation ou un nouveau bot se voit attribuer un profil et un instantané de son historique.

Choisissez

Rejoignez une équipe ou interagissez avec un bot via le panneau. Vérifiez et enregistrez le préréglage.

**Ne fait pas** Elle ne capture pas chaque discussion existante et n’observe pas les rappels déclenchés dans un autre client.

Ces cartes constituent une comparaison locale et ne sont pas des commandes de collecte en temps réel. Elles ne modifient pas un compte.

**Ne fait pas** Aucun mode ne lit les discussions secrètes, n’enregistre lorsque le processus est arrêté, ne rejoint des sources de son propre chef ni ne récupère l’historique antérieur au-delà de ce qui a été demandé snapshot/export.

[Lire les détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/)

## Collecte via GitHub Actions (version préliminaire)

Une nouvelle connexion Telegram, une discussion, une archive chiffrée et une attestation de provenance GitHub.

[Ouvrir l’assistant de collecte](https://phishdestroy.github.io/TgWitness/fr/docs/capture/)

## Ce qui est enregistré

Seules les observations transmises ou explicitement demandées sont consignées. Une attribution inconnue reste inconnue.

 Capture des commutateurs · illustration localeNouveaux messagesModificationsSuppressionsRéactionsAdhésion

Le panneau applique ces commutateurs par espace de travail. La désactivation d’un commutateur conserve les enregistrements existants ; sa réactivation ne reconstitue pas les événements manqués.

**Matrice des événements : données enregistrées et inconnues restantes**

| Catégorie | Enregistré | Reste inconnu |
| --- | --- | --- |
| Message | Texte, identifiants, métadonnées de l’expéditeur, contexte de réponse et enveloppe de mise à jour d’origine. | Pas de signature Telegram vérifiable par un tiers. |
| Modifier | Chaque version observée, sans écraser les précédentes. | Les modifications intermédiaires peuvent passer inaperçues ; l’expéditeur n’est pas nécessairement l’éditeur. |
| Suppression | Veuillez noter également le texte précédemment enregistré, le cas échéant. | Le programme de suppression et l’heure exacte de l’action ne sont pas fournis. |
| Suppression sans portée | Avis au niveau du compte ; le pair inconnu reste explicitement identifié. | Pas de conversation devinée. La corrélation utilise, dans la mesure du possible, les identifiants au niveau du compte précédemment enregistrés. |
| Réaction | Compteurs fournis et identités récentes visibles. | Tous les réacteurs ne sont pas visibles ; une liste complète des réacteurs disponibles nécessite des requêtes distinctes. |
| Adhésion | Messages de service transmis et mises à jour des participants. | Le rôle et le type de discussion limitent la visibilité ; le silence n’implique pas l’absence. |
| Pièce jointe | Descripteur de la version originale, octets enregistrés, SHA-256 et résultats des tentatives. | Un fichier disparu peut ne plus être disponible ; une version plus récente ne le remplace pas. |
| Instantané de l'historique | Messages actuellement visibles, marqués comme des observations de l'historique. | Les modifications antérieures et le contenu disparu ne sont pas reconstitués. |
| Vos propres actions | Sortant messages/edits et les métadonnées correspondantes du clavier de réponse button_press . | Les rappels déclenchés dans un autre client Telegram ne sont pas visibles. |
| Boutons du bot | Les métadonnées relatives au callback, à l’URL, à l’application web et à la requête sont conservées avec le message. | Les URL et les phone/location les requêtes sont du texte ; elles ne sont ni ouvertes ni exécutées automatiquement. |

### Limites par défaut pour les pièces jointes

Photos

20 MiB

Vidéo

100 MiB

Fichiers

50 MiB

Animations

20 MiB

Notes vidéo

50 MiB

Voix

20 MiB

Audio

50 MiB

Autocollants

5 MiB

**Ne fait pas** Un commutateur ne masque pas les métadonnées intégrées ni ne désactive les enregistrements opérationnels. La capture n’identifie pas un acteur que Telegram n’a pas fourni.

[Lire les détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/)

## Utilisez les autorisations dont vous disposez

Chaque compte dispose de son propre espace de travail, journal, clé de signature, route et file d’attente.

### Téléphone + code

Entrez 2FA lorsqu’elle est activée.

### QR code

Effectuez le scan à partir d’un appareil autorisé ; 2FA cela peut encore être nécessaire.

### Telethon .session

Importez le fichier de session du compte.

### Pyrogram .session

Importez le Pyrogram format de session pris en charge.

### TData ZIP

Un seul compte Desktop pris en charge ; code d'accès local s'il est défini.

### StringSession texte

Collez un Telethon StringSession.

### .session + .json

Sélectionnez la session et les métadonnées associées correspondantes.

### Clé d'authentification HEX + DC ID

Importez l’autorisation du compte avec son identifiant de centre de données.

**API paire**

Votre propre API paire est facultative. En l’absence de paire, TgWitness utilise un pool de paires publiques, y compris des paires provenant du client officiel Telegram Desktop.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy est expérimental ; des listes publiques intégrées MTProxy sont disponibles. Un itinéraire de proxy défaillant ne bascule pas vers une connexion directe.

Deux espaces de travail sur une même machine ne constituent pas deux témoins indépendants.

**Ne fait pas** L’importation ne contourne pas l’autorisation Telegram, 2FA ni les formats de session non pris en charge. Les comptes continuent de partager le processus d’application.

[Formats des comptes](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/)

## Agissez depuis le panneau

Envoyez ou répondez, appuyez sur un bouton du bot actuel, enregistrez un aperçu de lien, puis rejoignez explicitement une conversation ou lancez un bot avec son paramètre de démarrage.

`interaction.preview``interaction.requested``interaction.result`

Les accusés de réception d’aperçu, de requête et de résultat sont signés. Avant qu’un bouton ne soit enfoncé, le serveur récupère à nouveau le message et rejette toute modification apportée au clavier. Le texte et les URL des rappels renvoyés restent enregistrés dans le contexte.

**Ne fait pas** Pas d’applications web, de paiements, de phone/location ni de partage, ni de requêtes intégrées. L’affichage d’une URL n’entraîne pas son ouverture.

[Lire les détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/)

## Récupération et continuité

Les lacunes sont mises en évidence, et non dissimulées.

### Reprenez la position enregistrée

Après un redémarrage, Telegram vous demande les mises à jour manquées. Une durée de conservation limitée et les différences périmées peuvent entraîner des lacunes.

### Vérifiez à nouveau les messages visibles

Valeurs par défaut : sources prioritaires toutes les 15 minutes, autres toutes les 6 heures. Les résultats comprennent message.recovered et message.missing_on_recheck.

### Lire coverage.json

Les périodes d’observation, les lacunes accompagnées de leurs motifs et les identifiants non observés accompagnent l’exportation signée. Un enregistrement « manquant lors de la vérification » ne constitue pas un avis de suppression.

**Ne fait pas** Un instantané ultérieur de l’historique n’efface pas une interruption de service et ne permet pas de récupérer toutes les versions disparues. Le curseur enregistré ne constitue pas une confirmation sans perte de l’acceptation du journal.

[Lire les détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/)

## Sept niveaux. Des questions différentes.

Chaque mécanisme répond à une question bien délimitée. Configurez les services externes séparément et conservez leurs ancrages de confiance en dehors du collecteur.

1. ### Enregistrer

   SHA-256 chaîne + Ed25519 par événement ; le premier previous_hash est constitué de 64 zéros.

   **Vérifications par des tiers** Ordre et signatures sous la clé de collecte épinglée.

   **Ne fait pas** Cela ne prouve ni l’origine Telegram ni l’exhaustivité.

   **Commande de vérification**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Conteneur

   manifest.json répertorie les hachages de fichiers ; manifest.sig le signe. media.saved associe les octets de la pièce jointe à un événement.

   **Vérifications par des tiers** Les fichiers fournis correspondent au manifeste signé et aux reçus multimédias.

   **Ne fait pas** Elle ne signe pas un fichier téléchargé séparément CSV, HTML ou d’une capture d’écran.

   **Commande de vérification**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Limite conservée

   Point de contrôle au démarrage, toutes les 5 minutes par défaut, et arrêt ordonné. Conservez une copie ailleurs.

   **Vérifications par des tiers** L’exportation ultérieure correspond à une longueur et à un en-tête conservés antérieurement ; une annulation peut être détectée.

   **Ne fait pas** Elle ne détecte pas le remplacement à la fois du journal et de tous les points de contrôle conservés.

   **Commande de vérification**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### Heure externe

   Le mode « Evidence » envoie un point de contrôle SHA-256 aux RFC 3161 autorités (FreeTSA, DigiCert) et OpenTimestamps aux calendriers.

   **Vérifications par des tiers** Une réponse TSA vérifiée date ces octets ; une OpenTimestamps les ancre à Bitcoin.

   **Ne fait pas** Elle ne considère pas une requête préparée ou un accusé de réception en attente comme un horodatage confirmé.

   **Commande de vérification**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Témoin indépendant

   Hôte distinct, point de terminaison en lecture seule à portée limitée, défi nouveau, et sa propre key/journal et TGW1 publications sur le canal.

   **Vérifications par des tiers** Têtes précédemment acceptées ; statuts « ok », key_changed, « rollback », « fork », « invalid » et no_response.

   **Ne fait pas** Cela ne transforme pas deux espaces de travail sur un même hôte collecteur en témoins indépendants.

   **Commande de vérification**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Réplique hors site

   S3- Copie compatible chiffrée avec AES-256-GCM; Object Lock lorsque le compartiment le prend en charge.

   **Vérifications par des tiers** La fonction « Restore » ne publie les fichiers qu’après vérification réussie du journal, du point de contrôle et des médias conservés.

   **Ne fait pas** Elle ne permet pas la restauration sans la clé exportée ni ne présume de la conservation sans vérifier la réponse de stockage.

   **Commande de vérification**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Exécuter la provenance

   Accusé de réception d’exécution signé : hachages de la source, versions des dépendances et contexte du processus. Déclaré par l’utilisateur lui-même.

   **Vérifications par des tiers** Ce que le collecteur de signatures a rapporté concernant sa propre exécution.

   **Ne fait pas** Elle ne fournit pas d’attestation indépendante du processus et n’exclut pas la possibilité d’une compromission avant l’enregistrement.

   **Commande de vérification**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### Ce qu’aucun niveau ne prouve

La transmission de chaque mise à jour de Telegram ; la véracité du texte ; le fait qu’un identifiant d’expéditeur identifie une personne réelle ; l’absence de compromission du collecteur avant l’enregistrement ; l’admissibilité en justice.

[Témoin indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/)

Expérience SHA-256 Expérience

### Essayez de modifier l'enregistrement 2

L'enregistrement suivant conserve le lien précédemment enregistré. La modification du texte modifie le hachage calculé de l'enregistrement 2.

Texte de l'enregistrement n° 2

Enregistrement n° 1`h1`Commence par 64 zéros

Enregistrement n° 2`h2`Comprend les fichiers enregistrés h1

Enregistrement n° 3`h3`Comprend les fichiers enregistrés h2

Exemple statique : h2 couvre « Rendez-vous à 11 h ». La modification de ce texte modifie h2; l’enregistrement n° 3 fait toujours référence à la valeur enregistrée h2.

**Vérifiez l’intégralité des résumés**

Hachage de l'enregistrement 2 sauvegardé

`SHA-256(e₂)`

Hash recalculé de l'enregistrement n° 2

`SHA-256(e₂)`

Cet exemple calcule des hachages, et non des signatures. Le véritable vérificateur compare chaque signature et chaque lien à la clé de confiance.

 [Lire les détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/how-it-works/)

## Choisissez un parcours à travers les preuves

Situations fictives. Commencez la collecte avant l’événement concerné ; conservez les limites et les lacunes parallèlement au contenu.

### Un canal modifie ses informations de paiement

Mode → événements

Discussions sélectionnées → messages, modifications, suppressions.

Sortie

Versions des publications et pièces jointes observées par hachage.

Vérification

Signé ZIP + point de contrôle conservé + réponse TSA vérifiée.

**Ne fait pas** Elle ne permet pas de récupérer un original qui n’a jamais été capturé.

### Les messages disparaissent après un incident

Mode → événements

Dossier ou compte entier → toutes les catégories d’événements.

Sortie

Originaux sauvegardés, avis de suppression et couverture présentant des lacunes.

Vérification

Journal de témoin ZIP + journal de témoin indépendant.

**Ne fait pas** Elle ne permet pas d’identifier l’auteur de la suppression à partir d’une notification qui ne mentionne aucun acteur.

### Étudiez un bot de boutique

Mode → événements

Préréglage « Investigation » → boutons, aperçus des liens et lancement explicite du bot.

Sortie

Reçus d’interaction signés, callbacks renvoyés et profils enregistrés.

Vérification

Une fois signé ZIP; vérifiez tout dossier par rapport au ZIP.

**Ne fait pas** Elle n’ouvre pas d’application web de bot, n’effectue pas de paiement et n’enregistre pas les rappels d’un autre client.

### Un participant change de nom d’un chat à l’autre

Mode → événements

Toute portée → métadonnées observées sender/profile métadonnées.

Sortie

Historique des noms/noms d’utilisateur par identifiant numérique, liens « également présent sur » et pistes extraites.

Vérification

Dossier JSON vérifié par rapport au document signé ZIP.

**Ne fait pas** Elle ne transforme pas un portefeuille, une chaîne de caractères de type « numéro de téléphone » ou un nom d’utilisateur en identité vérifiée.

### Observation à long terme avec une copie hors site

Mode → événements

Tout champ d’application → Mode « Evidence » et une S3 réplique avec prise en charge Object Lock.

Sortie

Copie chiffrée, points de contrôle conservés et réponses horodatées.

Vérification

Effectuez la restauration à l’aide de la clé exportée, puis procédez à la vérification sans le serveur d’origine.

**Ne fait pas** Elle ne remplace pas un témoin indépendant ni une clé de déchiffrement conservée séparément.

[Lire les détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/investigation/)

## Remettez un paquet vérifiable

Fournissez l’original signé, une empreinte de clé conservée de manière indépendante, le point de contrôle pertinent et le résultat de la vérification.

- Signé ZIP
- JSONL
- CSV
- HTML
- Point de contrôle
- Accusé de réception
- Exportation des discussions : chat.json / chat.html
- Dossier JSON
- Protégé par mot de passe AES-256 ZIP
- Exportations distinctes pour plusieurs comptes
- CLI de streaming : 5 GiB limite par défaut

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Obtenez le vérificateur à partir d’une copie de confiance, et non à partir de l’archive en cours de vérification.

**Ne fait pas** Autonome CSV et HTML ne sont pas des conteneurs signés. Un mot de passe protège la confidentialité du transfert, et non son authenticité. Les exportations multiples ne fusionnent pas les journaux de compte.

[Lire les détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/)

## Comparez l’artefact fourni

Artefacts de base sans signature, horodatage ni systèmes de témoins ajoutés. Les scripts et les outils de journalisation varient selon l’implémentation ; « partiel » signifie limité aux données capturées ou visibles.

| Approche | Modifications / suppressions | Enregistrer la signature | Heure externe | Témoin indépendant | Couverture / lacunes | Vérification sans auteur |
| --- | --- | --- | --- | --- | --- | --- |
| Exportation depuis Telegram Desktop | Partiel | Non | Non | Non | Non | Non |
| Telethon script de capture d'écran | Partiel | Non | Non | Non | Non | Non |
| Enregistreur de suppressions : journal textuel | Partiel | Non | Non | Non | Non | Non |
| Captures d'écran / captures Web | Partiel | Non | Non | Non | Non | Non |
| TgWitness avec des options supplémentaires configurées | Partiel | Oui | Oui | Oui | Partiel | Oui |

**Ne fait pas** Le tableau n’évalue pas chaque script ou produit de journalisation. Les vérifications facultatives de l’heure et des témoins nécessitent leurs propres services et ancrages de confiance ; aucun d’entre eux n’établit la vérité de la source.

[Lire les détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/)

## Respectez les limites en vous appuyant sur les preuves

La vérification est utile lorsque son champ d’application reste explicite.

- Les discussions secrètes ne sont pas disponibles.
- Rien n’est enregistré lorsque le processus est arrêté ; la récupération est limitée.
- Un enregistrement vérifié ne constitue pas une preuve de la véracité de son contenu.
- Un opérateur disposant de la clé peut signer n’importe quel contenu. Les témoins indépendants et les horodatages empêchent toute substitution ultérieure, mais pas une capture initiale malhonnête.
- Utilisez un compte dédié, et non votre compte principal.
- Telegram peut restreindre l’accès à certains comptes en raison du volume de requêtes.

**Ne fait pas** Aucun mode ni niveau de preuve ne garantit la recevabilité juridique, la livraison complète sur Telegram ou l’identité dans le monde réel.

[Guide d’installation](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=fr)[Compte dédié](https://phishdestroy.github.io/TgWitness/fr/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/fr/docs/reference/investigation/)
