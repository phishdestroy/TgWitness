# Configuration et vérification des rapports

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-reports/

Filtres de rapports, huit modèles, préréglages de contenu, historiques des modifications enregistrés et évaluation incluse dans les exportations signées.

Transformez les observations sélectionnées en un compte rendu lisible de l’affaire : son objet, sa portée, les modifications enregistrées, les graphiques, les conclusions et les références aux sources. Chaque rapport offre au destinataire un moyen de vérifier les éléments fournis et d’examiner l’étendue de la collecte .

La section « **Base de confiance et limitations** » apparaît dans les rapports de journal, de transfert, de discussion, de compte et de partage. Les fichiers PDF du journal et du transfert utilisent la même évaluation que leur fichier « `report.json` » signé. Les manifestes ZIP contiennent le fichier « `case_assessment` » dans le manifeste signé. Cette évaluation accompagne les données exportées. Les observations originales conservent leurs signatures existantes.

## Formats des documents et ordre de lecture

### Report Studio

Ouvrez « **Exports » → « Configure » et « Preview** ». Parcourez « **Data** » **→ « Design & contents » → « Preview** » :

1. Utilisez l’ensemble de l’espace de travail ou sélectionnez des discussions, des auteurs, des dates d’observation en UTC et des types d’événements. Chargez le catalogue pour rechercher des discussions et des auteurs, ou saisissez leurs identifiants Telegram. Les filtres d’auteur correspondent aux identifiants d’expéditeur enregistrés ; une notification de suppression sans expéditeur ne correspond pas à un filtre d’auteur.
2. Choisissez une mise en page, puis sélectionnez les graphiques, les libellés des participants, la transcription et vos conclusions écrites. La modification de la mise en page conserve ces choix.
3. Générez l’aperçu. Celui-ci affiche les chiffres réels, l’activité, les participants, des exemples d’ enregistrements, les modifications enregistrées et les plages de numéros de messages manquants. Toute modification d’un choix rend l’aperçu obsolète. Enregistrez avant de télécharger le fichier HTML, le PDF signé, le JSON signé ou l’archive ZIP contenant les preuves.

L’aperçu des données prend en compte l’intégralité du préfixe du journal stable, et non un échantillon initial. Seules les lignes d’échantillon affichées et les longues listes sont limitées ; leur nombre omis est indiqué. Une exportation ultérieure effectue un nouvel instantané stable, de sorte que la collecte en cours peut augmenter ces chiffres. La portée, les nombres et l’identité de la source sont inclus dans le rapport signé. L’ouverture ou la prévisualisation du formulaire ne l’enregistre pas.

**Jurisdiction guidance.** Under Document details, open **Jurisdiction guidance · optional** to choose a jurisdiction and civil/commercial or criminal procedure. The appendix carries the legal basis, source links, preparation notes and research status. Local-language summaries and explanations of collection safeguards are optional. No jurisdiction is selected by default. These choices belong to the workspace, and are excluded from saved layout configurations and implicit sharing-copy defaults. See [defaults, supported reports and research limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/JURISDICTION_GUIDANCE.md).

**Choisissez la version destinée au destinataire.** Les graphiques et la transcription utilisent les enregistrements sélectionnés. L’intégrité, la conservation et la couverture décrivent l’intégralité du journal source. Le fichier ZIP de preuves contient ses enregistrements originaux et ses pièces jointes. Optez pour [un transfert allégé](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#handover-extract) lorsque le destinataire ne doit recevoir que les données sélectionnées et autorisées.

### Lire les modifications, les suppressions et les identifiants manquants

Une modification affiche le texte enregistré **« avant »** et **« après »** et met en évidence les mots modifiés. Une suppression affiche la dernière version enregistrée avant la notification. Si aucun contenu antérieur n’a été capturé, le rapport l’indique. Lorsque vous sélectionnez uniquement les modifications ou les suppressions, les versions précédentes restent disponibles en tant que contexte explicitement identifié en dehors des filtres. Les messages sans rapport ne sont pas ajoutés à ces historiques.

**Les identifiants de messages non observés** correspondent à des lacunes entre des numéros connus dans les discussions sélectionnées et la plage d’identifiants dérivée de la date. Chaque enregistrement source connu est vérifié avant de déclarer un numéro comme non observé : le fait d’exclure un autre auteur, un type d’événement ou une date ne peut pas créer de fausse lacune. Les messages enregistrés adjacents sont étiquetés comme « contexte ». Un numéro manquant ne prouve pas qu’un message ait existé ou ait été supprimé ; les notifications de suppression et les vérifications infructueuses restent des types d’événements distincts.

### Choisissez un design

Huit mises en page sont disponibles pour les rapports HTML (journal et conversation unique) et les rapports PDF signés. Elles utilisent les mêmes données et calculs, mais présentent des couvertures, une typographie, des titres de chapitres, des tableaux et des espacements différents.

| Conception | Style de lecture |
| --- | --- |
| Classique | Un dossier traditionnel avec une couverture sombre et des sections numérotées. |
| Rédaction | Une page de titre encadrée avec des caractères à empattement, de larges marges et une barre de chapitres étroite. |
| Briefing | Une couverture compacte avec un dos bleu marine, des titres courts et des tableaux rapprochés. |
| Analyses | Une page de garde de type questionnaire, des tableaux modulaires et des figures en police à espacement fixe. |
| Technique | Un registre ligné, une barre de référence numérotée et des tableaux de comparaison précis. |
| Présentation générale | Une couverture panoramique, une mise en page aérée et des chiffres récapitulatifs bien mis en évidence. |
| Série de lecture | Une barre de navigation et des chapitres regroupés pour les conclusions, le périmètre, les modifications et le journal d’observation. |
| Ledger et marge | Chapitres numérotés avec une marge large, tableaux précis et transcription des messages sur une page séparée. |

La mise en page est enregistrée par espace de travail et consignée dans le manifeste d’exportation signé. Le format HTML fonctionne hors ligne, prend en charge les thèmes clair et foncé, et s’adapte aux écrans étroits ainsi qu’aux langues s’écrivant de droite à gauche. Les PDF natifs utilisent des polices intégrées ; la mise en page « Editorial » inclut la police Noto Serif sous sa licence SIL Open Font License intégrée. Les séries de lecture ainsi que les options « Ledger » et « marge » s’appliquent également aux aperçus de compte, aux discussions de compte et au partage de copies.

Les fichiers PDF en chinois, japonais et coréen nécessitent en outre une police adaptée sur le serveur, telle que Noto Sans CJK, installée à l'échelle du système ou placée dans le répertoire `TGWITNESS_FONT_DIR`. Si celle-ci n'est pas disponible, le fichier ZIP conserve les rapports au format HTML et JSON.

Ces deux modèles comprennent un journal lisible sans JavaScript. Pour les exportations volumineuses, cette vue contient jusqu’à 500 enregistrements complets dans une limite d’entrée de 8 Mio ; le rapport indique cette limite et propose des liens vers la visionneuse complète et les enregistrements sources. Le répertoire des comptes et l’index des relations décrivent ce même échantillon de lecture, et non l’ensemble des participants. Les graphiques du journal complet conservent leur champ d’application indiqué séparément.

### Choisissez le contenu

| Table des matières prédéfinie | Inclus par défaut |
| --- | --- |
| Dossier d'affaire | Activité, heures d’observation, participants, discussions et transcription de l’enregistrement. |
| Briefing | Un aperçu des activités sans classement des participants ni transcription. |
| Bilan des activités | Activités, heures d’observation, participants, discussions et composition, avec références aux sources et chiffres exacts. |
| Rapport personnalisé | Votre propre combinaison de graphiques, de transcriptions et d'aperçus. |

La modification d’un préréglage conserve votre mise en page, les détails de l’affaire et l’analyse écrite. Les contrôles d’intégrité, la couverture, les limitations et les instructions de vérification sont conservés dans chaque mise en page. Les enregistrements sources contenus dans le fichier ZIP restent inchangés lorsqu’un graphique ou une transcription est masqué.

Les **« Notes d’examen »** (en option) contiennent la question, la méthode, les constatations et la conclusion rédigées par l’auteur du rapport. Citer le fichier source et les numéros d’enregistrement dans les constatations. La signature préserve ces déclarations rédigées par l’auteur aux côtés du rapport ; les observations sources et l’interprétation de l’auteur restent identifiables. Les transferts simplifiés omettent ces notes privées et les dossiers complets du journal. Les choix relatifs aux dossiers et aux examens s’appliquent aux rapports du journal.

Sélectionnez l’activité au fil du temps, la carte thermique UTC par jour de la semaine et par heure, les classements des participants, les classements des discussions et la composition des enregistrements. Choisissez entre 5 et 30 groupes classés ainsi que des pseudonymes ou des identifiants de compte neutres pour les participants. Les expéditeurs inconnus et les autres participants apparaissent sur des lignes distinctes. Les pseudonymes n’affectent que les graphiques ; les enregistrements sources contiennent toujours leurs identités.

L’aperçu de la mise en page se met à jour à partir du brouillon non enregistré en utilisant la couverture de production, l’examen et les composants de graphiques, limités aux correspondances parmi les 50 000 premiers enregistrements sources. L’aperçu des données ci-dessous calcule la sélection complète. Il est explicitement non signé et ne conserve pas les modifications. Les boutons « Couverture » et « Graphiques » permettent de changer de section. Il ne s’agit pas d’un aperçu PDF complet. L’option « **Enregistrer les paramètres du rapport »** applique les choix aux futures exportations ; les fichiers signés existants sont immuables. Le PDF utilise la page de garde choisie, la typographie, la mise en page des chapitres et les mêmes agrégats sélectionnés que le HTML et le JSON signé.

L’évaluation de la fiabilité, les limites de couverture et les instructions de vérification restent présentes. Le fait de masquer des graphiques ou la transcription lisible ne supprime pas les lignes de source faisant autorité du fichier ZIP. Les séries de graphiques désactivées sont omises du fichier JSON analytique ; utilisez une exportation « minimisée » pour limiter la divulgation des enregistrements sources.

Les filtres de sélection des données s’appliquent aux rapports de journal ; les exportations de comptes et de partages conservent leur propre périmètre d’acquisition et de divulgation.

Les préférences de mise en page et de graphiques partagées sont conservées dans les nouvelles exportations de discussions et de comptes, ainsi que dans les aperçus de partage de compte. Les paramètres de langue et de confidentialité du compte et du partage restent indépendants ; les notes privées relatives aux dossiers et aux enquêtes ne sont pas copiées dans ces exportations. Les rapports de compte et de partage restent au format HTML, protégés par leur manifeste d’archive signé. Le journal, le transfert de journal réduit et les kits de discussion unique fournissent également des PDF signés.

### Ce que les graphiques indiquent

L'activité du journal et les cartes thermiques comptabilisent **les observations** nouvelles, historiques, récupérées, modifiées, supprimées et manquantes lors d'une nouvelle vérification, en fonction de l'heure d'observation du collecteur en UTC. Les signaux de présence et les accusés de réception des pièces jointes sont exclus. Les classements des participants ne comptabilisent que les observations de messages nouvelles, historiques et récupérées : un expéditeur n’est pas considéré comme l’auteur de la modification ou de la suppression. Des observations répétées peuvent correspondre au même message Telegram.

Les analyses de journal conservent les comptages par type, les références aux premier et dernier enregistrements ainsi que le SHA-256 de la source « `events.jsonl`». Les chiffres incluent des valeurs exactes au format HTML et PDF. Les tranches quotidiennes passent à des tranches mensuelles au-delà de 366 jours enregistrés ; les graphiques regroupent celles-ci en 36 intervalles de largeur égale au maximum. Plus de 100 000 identifiants distincts ou 1 200 mois rendent le graphique concerné indisponible, tandis que les totaux exacts restent disponibles.

Les graphiques de clichés et de partage de comptes ne comptabilisent que les lignes de messages non liés au service incluses, en utilisant l’heure d’envoi enregistrée de ces messages. Les agrégats de partage sont calculés après expurgation et filtrage. Ces graphiques utilisent au maximum 90 intervalles de date UTC de largeur égale et conservent jusqu’à 10 000 valeurs de regroupement ; les décomptes excédentaires sont explicitement déclarés et rapprochés. Le dernier intervalle peut être plus court. Les dates inconnues ou approximatives n’apparaissent pas dans les graphiques temporels.

Un intervalle vide signifie qu’aucune observation n’est incluse ; consultez la couverture pour identifier les lacunes. Ces graphiques décrivent l’activité enregistrée. Les expéditeurs inconnus constituent une catégorie distincte, et chaque vérification fait l’objet d’un rapport individuel.

Lorsqu’il est inclus, le fichier `analytics.json` est protégé par les hachages signés de l’archive. Le fichier journal `report.json` intègre le même agrégat sélectionné. La vérification de la signature détecte les octets modifiés. Pour vérifier les chiffres, recalculez les agrégats du journal à l’aide de `report_analytics.Analytics` et `selected`, ou les agrégats d’instantanés à l’aide de `snapshot_analytics.collect` et `project`.

### Anomaly indicators

**Preview.** Evidence reports add an **Anomaly indicators** section computed by registered processors (`tgwitness/metrics/`, one file per metric). The report names every processor that ran with its version, and prints its method under its table, so the computation can be repeated from `events.jsonl` with `tgwitness.metrics.run`.

| Processor | Ce qu’il présente |
| --- | --- |
| `first_time_posters_over_time` v1 | First-time posters and messages per UTC day. A flag requires at least five first-time posters and three times their median, with message volume at most 1.5 times its median. The baseline uses at least seven observed days within the previous 14 calendar days, after seven days of warm-up. |
| `service_vs_message_ratio` v1 | Distinct saved message numbers per chat and the share used by service messages. It describes a numbering; it does not explain a particular missing number. |
| `join_leave_per_month` v1 | Joins, departures and removals or bans per month, one per person, chat, change and day. |
| `pinned_per_month` v1 | Pin service messages, unpin notices, and pinned messages added or removed between chat-state snapshots, per month. |

**Parameters → Report metrics** selects processors and the number of displayed rows, including in filtered reports. Daily and monthly tables show recent rows, service-share tables rank chats by saved message count. Totals cover every row.

À partir d'un extrait du code source, créez les huit modèles énumérés ci-dessus à partir du même journal fictif :

```
python tools/build_report_styles.py --output test-results/report-styles
```

Ouvrez le fichier « `index.html` » obtenu pour comparer les rapports HTML complets, les PDF signés et les fichiers ZIP. Chaque modèle utilise le même journal source. Utilisez un nouveau répertoire de sortie pour chaque exécution afin de conserver les exemples signés précédemment.

![Dossier HTML fictif](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

Le code HTML s'ouvre sur une page de couverture du dossier et des chiffres clés. La carte des preuves numérotée renvoie à chaque conclusion, aux faits qui l'étayent, à ses limites et à l'examen indépendant. Les enregistrements consultables et les références d'enregistrements stables restent disponibles dans la visionneuse hors ligne. La mise en page s'adapte aux écrans étroits, ainsi qu'aux différents thèmes et navigateurs sans JavaScript.

Le PDF signé comporte une page de garde A4 dédiée, une référence de rapport et un code QR, un résumé, une carte des éléments de preuve, des conclusions numérotées et des signets de documents. Ses en-têtes et pieds de page identifient le rapport. Un code QR identifie le contenu ; il ne s’agit pas d’un résultat de vérification indépendant. Les impressions depuis le navigateur sont distinctes de ce PDF signé cryptographiquement.

La chronologie des observations place les périodes d’observation enregistrées et les interruptions sur le même axe UTC. Les espaces vides ne correspondent pas à une couverture implicite ; les tableaux détaillés conservent les intervalles exacts. L’archive ZIP contient les rapports lisibles, les fichiers JSON signés, les enregistrements sources et les instructions de vérification.

Créez un nouveau dossier fictif en anglais/russe/allemand avec l’environnement de développement installé :

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Chaque répertoire de langue contient les fichiers `report.html`, `report.pdf`, `report.json` et `dossier.zip`. Les répertoires d’exemples existants ne sont jamais écrasés. Aucun compte Telegram, aucun service externe d’horodatage ni aucune connexion réseau n’est utilisé pour le créer.

![Les trois premières pages du PDF fictif signé](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Étude d’un cas concret

Pour un journal comportant 1 200 entrées et dont l’horodatage est validé à l’entrée n° 1 000, le rapport identifie 200 entrées postérieures se situant en dehors de la plage de cet horodatage. Il s’agit d’une limite supérieure quant à l’existence d’un point de contrôle, et non d’une preuve de l’heure d’envoi de chaque message . Si trois autres fichiers d’horodatage échouent à la validation ou ne peuvent être validés, ils sont comptabilisés séparément et ne permettent pas de tirer une conclusion positive.

Un horodatage valide doit satisfaire à toutes ces vérifications : son empreinte correspond au point de contrôle, sa signature est chaînée à une racine TSA de confiance à l’heure indiquée, et la signature, la clé, le compteur et l’en-tête du point de contrôle correspondent exactement au préfixe du journal. Il ne suffit pas de simplement analyser un horodatage ou de disposer d’un reçu OTS. Le lecteur doit choisir de manière indépendante la racine TSA de confiance et répéter la vérification. OTS nécessite sa propre vérification de confirmation Bitcoin.

| Statut du rapport | Signification |
| --- | --- |
| Vérifié lors de l'exportation | L’exportateur a effectué la vérification indiquée ; une répétition indépendante reste toutefois nécessaire. |
| Enregistré ; révision requise | L’observation sous-jacente ou la déclaration de l’opérateur est enregistrée ; il ne s’agit pas d’une confirmation indépendante. |
| Non inclus dans ce texte | Le texte ne fournit aucun élément à l’appui de cette affirmation. Il n’indique pas non plus qu’il n’en existe nulle part ailleurs. |
| Non vérifié de manière indépendante | Le rapport ne fournit pas de résultat de vérification indépendant. |
| Incomplet ou indisponible | Un élément ou une vérification requise est manquant, incomplet ou a échoué. |

Vérifiez chaque point séparément, en vous référant à la couverture de collecte enregistrée.

## Ce qu’une configuration robuste doit préserver

1. Avant de procéder à la collecte, conservez l'empreinte digitale de la clé du collecteur via un canal de confiance distinct. Comparez cette référence avec la clé de signature de l'exportation.
2. Conservez les points de contrôle horodatés de manière indépendante et, le cas échéant, un journal de témoin hors du contrôle administratif du collecteur. Comparez-les au journal exporté pour vérifier ses limites antérieures.
3. Préciser la portée de l'acquisition des enregistrements, les lacunes, les filtres, les limites et les modifications apportées à la collecte. Expliquer les périodes manquantes pertinentes pour la plainte en question, en distinguant clairement les identifiants de messages non observés, les notifications de suppression et les vérifications infructueuses.
4. Conservez les fichiers ZIP d’origine et leurs hachages. Enregistrez chaque détenteur, transfert, date et objet. Conservez les déclarations attribuées aux opérateurs et les notes de dossier qui les accompagnent.
5. Pour les messages vocaux confidentiels, conservez et vérifiez de manière indépendante la citation, la contestation, la chaîne de certificats Intel, les mesures, la source exacte et les conditions de gestion des clés. Conservez le résultat de la vérification de l’attestation avec les artefacts examinés.

See [verification scope](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#verification-scope) for the checks of acquisition, archive integrity, time and collection coverage in each mode.

## Révision par le destinataire

Utilisez une installation fiable de TgWitness et une empreinte digitale obtenue de manière indépendante :

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

Le fichier ZIP « witness » doit provenir d’une source indépendante et fiable ; conservez également sa clé et sa provenance. Conservez les commandes, la version de l’outil, les résultats, les hachages des données d’entrée vérifiées et les questions non résolues. La vérification par balise est un contrôle en ligne distinct ; le générateur de rapports ne contacte jamais un service dans le seul but d’afficher un rapport.

En cas de litige concernant un message particulier, citez la référence d’archive, le fichier faisant autorité et la référence de l’enregistrement, puis décrivez la période concernée, les lacunes de couverture, la sélection et les éléments corroborants. Pour une copie partagée, examinez également la transformation enregistrée et ses références à l’archive source. Les filtres privés et les mappages d’identité ne font pas partie de l’évaluation publique.

La vérification du PDF signé détecte les modifications apportées aux octets concernés. Conservez le fichier numérique d’origine et le résultat de la vérification, ainsi que toutes les captures d’écran ou copies imprimées.
