# Preuves et confiance

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence-trust/

Ce que les exportations, les vidéos, les archives Web et les enregistrements signés peuvent établir, et comment le dispositif de collecte influe sur leur fiabilité.

Une exportation, une capture d’écran ou un enregistrement peut constituer une preuve utile. Sa fiabilité dépend de la manière dont il a été collecté, conservé et corroboré. **Un hachage ou une signature valide vérifie le contenu enregistré ; il n’établit pas de manière indépendante que l’appareil de collecte a reçu un contenu source authentique.** Cette distinction s’applique également à TgWitness.

Ce guide distingue la vérification technique de l’évaluation juridique. La documentation du produit et les dispositions juridiques ci-dessous ont été révisées le 1er novembre 2026 ; la comparaison Hunchly décrit sa documentation publiée, et non un nouvel audit du produit.

## Quand la confiance entre en jeu dans la capture

Organigramme · Compte et service Telegram → Client, navigateur et système d’exploitation; Client, navigateur et système d’exploitation → Exportation, capture vidéo ou capture de page; Exportation, capture vidéo ou capture de page → Hachages et signatures des collecteurs; Hachages et signatures des collecteurs → Hachage conservé par une partie indépendante · Compte et serviceTelegram · Client, navigateur etsystème d’exploitation · Exportation, capturevidéo ou capture depage · Hachages et signaturesdes collecteurs · Hachage conservé parune partieindépendante

**Schéma sous forme de texte**

1. Compte et service Telegram → Client, navigateur et système d’exploitation
2. Client, navigateur et système d’exploitation → Exportation, capture vidéo ou capture de page
3. Exportation, capture vidéo ou capture de page → Hachages et signatures des collecteurs
4. Hachages et signatures des collecteurs → Hachage conservé par une partie indépendante

Le modèle de menace considéré ici part du principe qu’un attaquant ou un opérateur peut modifier l’environnement de collecte avant que les preuves ne soient validées. Il s’agit d’une analyse conditionnelle, et non d’une affirmation selon laquelle un appareil ou un produit particulier a été compromis.

Un client officiel et une connexion chiffrée contribuent à protéger une utilisation normale. Ils ne rendent pas pour autant le système d’exploitation, le navigateur ou l’affichage environnants fiables en eux-mêmes. Si le contenu est remplacé après le déchiffrement mais avant la capture, l’ exportateur peut l’enregistrer avec précision et le signataire peut le signer correctement. Aucune de ces opérations ne nécessite un algorithme de hachage défaillant ni une signature falsifiée.

Une vidéo réalisée sur le même appareil peut enregistrer la même présentation substituée. Une caméra distincte peut confirmer ce que l’écran affichait, mais l’écran à lui seul n’authentifie pas ce que Telegram a fourni. De même, le HTML, le JSON, les captures d’écran et les journaux de navigateur correspondants provenant d’un même environnement contrôlé peuvent présenter la même anomalie. Leur concordance constitue un contexte utile ; elle ne constitue pas automatiquement une corroboration indépendante.

## Ce qu’apporte chaque type de preuve

| Contenu | Contribution utile | Question restante |
| --- | --- | --- |
| Exportation depuis Telegram Desktop | Conversations lisibles ou lisibles par machine et médias sélectionnés | Qui contrôlait le client et les fichiers d’exportation, et quels éléments étaient disponibles ou exclus ? |
| Capture d’écran ou enregistrement d’écran | Contexte visible, séquence d’actions et présentation | La présentation reflète-t-elle fidèlement la source, et que s’est-il passé en dehors de l’enregistrement ? |
| Archive Web locale, y compris MHTML | Contenu de la page et ressources associées pour examen ultérieur | Quelles données le navigateur a-t-il fournies à l’archiveur, et qui contrôlait ce navigateur ? |
| Archive signée par le collecteur | Les modifications apportées aux octets signés peuvent être détectées par rapport à une clé de confiance et à une référence conservée. | Qui contrôlait la clé de signature et les données d’entrée avant la signature ? |
| Point de contrôle conservé de manière indépendante ou horodatage vérifié | Un hachage ou un point de contrôle conservé à des fins de comparaison avec une soumission ultérieure | Quels octets et quelles limites sont couverts, et que certifie réellement la partie indépendante ? |

Telegram documente son exportation via Telegram Desktop comme une copie HTML/JSON hors ligne et son API Takeout comme un moyen de récupérer des données de compte sélectionnées. Ces descriptions ne fournissent pas de signature Telegram sur l’archive finale exportée permettant à un destinataire de la vérifier. Notre conclusion se limite à ces mécanismes d’exportation documentés ; il ne s’agit pas d’une affirmation selon laquelle les preuves issues de Telegram n’ont aucune valeur juridique.[Exportation via Telegram Desktop](https://telegram.org/blog/export-and-more),[API Takeout](https://core.telegram.org/api/takeout).

La même distinction s’applique aux requêtes en arrière-plan, aux entrées de cache et aux journaux réseau. Ceux-ci peuvent révéler des incohérences et aider à corroborer une collecte. Leur complexité ne suffit pas à elle seule à établir qui les a produits. Une archive gérée de manière indépendante ou un enregistrement de service obtenu séparément introduit une source différente à comparer, sous réserve de ses propres limitations en matière de collecte et de conservation.

## Hunchly illustre la même limite

La documentation de Hunchly décrit le hachage SHA-256 des captures MHTML, des photos et des pièces jointes, avec une vérification indépendante du hachage. Elle explique également pourquoi un fichier modifié accompagné d’un hachage nouvellement calculé peut passer cette comparaison, et renvoie aux signatures et à la corroboration de la source comme contrôles supplémentaires.[Hunchly : hachage du contenu, des photos et des pièces jointes](https://support.maltego.com/support/solutions/articles/15000061289-content-photo-and-attachment-hashing).

Son *« Evidence Guide »* publié, révision 1.0 du 17 octobre 2018, décrit les clés GPG et les signatures générées localement pour les captures MHTML. Il identifie explicitement l’accès à la clé privée locale comme un moyen de signer à nouveau des éléments modifiés. Il s’agit d’une limitation de confiance documentée, et non d’une preuve d’une faille actuelle non divulguée. Le guide précise également que c’est Chrome qui effectue la capture MHTML. Décrire Hunchly comme reposant uniquement sur la réputation d’un enquêteur reviendrait à omettre ces contrôles techniques.[Guide des preuves Hunchly, sections 2 à 4](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf).

La question de savoir si les éléments recueillis à l’aide d’un produit particulier ont été admis dans une affaire dépend de la décision et des circonstances pertinentes. Nous ne nous prononçons pas ici sur la fréquence à laquelle les tribunaux acceptent Hunchly ou TgWitness, ni sur le fait que l’un ou l’autre de ces produits bénéficie d’une approbation générale des tribunaux.

## Ce qu’apporte TgWitness, et jusqu’où s’étend sa protection

TgWitness consigne les observations dans un journal signé et lié, et fournit des exportations que le destinataire peut vérifier. Les points de contrôle conservés, les horodatages et un témoin distinct fournissent aux examinateurs des références allant au-delà des fichiers actuels du collecteur. Ils permettent de mettre en évidence les modifications apportées aux enregistrements précédemment validés. Les enregistrements de couverture et les résultats explicites de la collecte aident à expliquer ce qui a été capturé et ce qui ne l’a pas été.[Format et transfert des preuves](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/), [portée de la collecte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/collection/).

Le moment d’une éventuelle substitution a son importance :

1. **Après la signature, sans accès à la clé de signature :** la modification d’un enregistrement signé ou d’un fichier lié au manifeste entraîne l’échec de la vérification par un vérificateur et une clé de confiance.
2. **Avec la clé du collecteur, après la conservation d’un point de contrôle indépendant :** un journal de remplacement peut comporter de nouvelles signatures valides, mais un préfixe modifié échoue à la comparaison avec ce point de contrôle antérieur. Un point de contrôle conservé uniquement sur le même appareil contrôlé peut être remplacé en même temps que le journal. Les enregistrements situés au-delà de la limite de conservation nécessitent leur propre couverture.
3. **Avant qu’un point de contrôle couvrant une observation ne soit conservé de manière indépendante :**des données erronées peuvent être signées et ancrées avec succès, y compris de nouveaux enregistrements ajoutés après un point de contrôle antérieur. Le point de contrôle ou l’horodatage résultant couvre toujours ces enregistrements erronés ; il n’établit pas leur véracité.

Un témoin TgWitness reçoit les points de contrôle signés par le collecteur ; il ne lit pas de manière indépendante la conversation Telegram sous-jacente. Sa clé et ses enregistrements conservés doivent être considérés comme fiables séparément. Lorsque l’intégralité du journal soumis doit être certifiée, utilisez la[procédure de transfert exigeant la limite d’exportation finale](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/#require-a-witnessed-export-boundary). Un contrôle d’intégrité ordinaire peut tout de même signaler une partie finale non certifiée.

Une réponse RFC 3161 vérifiée peut attester qu’un point de contrôle existait à l’heure indiquée par l’autorité. Elle ne permet pas de déterminer quand un message Telegram a été envoyé ni si son contenu était véridique. Une requête préparée ou un fichier de réponse inclus ne suffit pas à lui seul. Lors de la vérification d’une exportation avec `tgwitness.verify`, la vérification des signatures TSA incluses nécessite une autorité de certification (CA) explicitement approuvée via `--tsa-ca`. Les reçus OpenTimestamps nécessitent une vérification indépendante `ots verify`, avec des mises à niveau des preuves si nécessaire. [Procédure d’horodatage](https://phishdestroy.github.io/TgWitness/fr/docs/reference/timestamp/), [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html).

Dans [la capture GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md), un runner hébergé temporairement collecte les messages. L’attestation lie l’archive à un workflow approuvé. Ce mode fait toujours confiance à GitHub, au logiciel approuvé et à ses dépendances, à l’assistant/navigateur et au tunnel. Il ne s’agit pas d’un matériel confidentiel, d’une signature Telegram, ni d’une preuve que personne n’a accédé à l’hôte. Un reçu d’exécution signé localement est également une mesure autodéclarée, et non une attestation matérielle.

## La valeur juridique dépend du fondement

Quatre questions doivent rester distinctes : si l’élément est bien ce qu’il prétend être, si les octets soumis correspondent à l’enregistrement conservé, si le contenu corrobore les faits allégués, et si les règles applicables autorisent son utilisation. Un contrôle cryptographique ne couvre qu’une partie de ce fondement.

Dans les procédures fédérales américaines, la règle 901 prévoit des moyens d’authentifier les éléments de preuve, notamment par le témoignage d’un témoin compétent et des preuves relatives à un processus ou à un système. Les règles 902(13) et 902(14) prévoient des voies de certification pour certains documents et copies électroniques, assorties d’exigences procédurales. Leurs notes de commission distinguent l’authentification de questions telles que le ouï-dire, la pertinence et l’attribution. Une signature logicielle ne constitue pas à elle seule la certification par une personne qualifiée décrite dans ces règles.[Règle fédérale de preuve 901](https://www.law.cornell.edu/rules/fre/rule_901),[Règle fédérale de preuve 902](https://www.law.cornell.edu/rules/fre/rule_902).

Lorsque la Loi sur la preuve du Canada s’applique, l’article 31.1 traite de l’authentification des documents électroniques. L’article 31.2 lie la règle de la meilleure preuve à l’intégrité du système ou à une présomption applicable ; l’article 31.3 précise les circonstances dans lesquelles s’applique une présomption d’intégrité. Il s’agit de conditions de preuve définies, et non d’une présomption générale selon laquelle tout enquêteur agréé ou produit commercial serait infaillible. [Loi sur la preuve du Canada, articles 31.1](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.1.html),[31.2](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.2.html),[31.3](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.3.html).

Ces exemples ne préjugent pas de l’admissibilité dans une autre juridiction ou dans une affaire particulière. Les vérifications techniques doivent être appliquées de manière cohérente aux éléments venant étayer ou contester une allégation. Le présent guide ne prétend pas que les éléments de preuve de l’accusation sont généralement plus faciles à admettre que ceux de la défense.

## Préparez un document pouvant être évalué par une autre personne

- Décrivez le compte, le dispositif de collecte, l’opérateur, la version du logiciel, les droits d’accès, la portée sélectionnée et la période de collecte. Consignez les interruptions et les éventuelles compromissions au lieu de considérer une vérification de signature réussie comme un test de bon fonctionnement du dispositif.
- Conservez les paquets d’origine et enregistrez les transferts, les hachages et la source temporelle. Conservez l’empreinte de la clé et les points de contrôle via un canal de confiance distinct. Vérifiez la couverture effective des témoins ou des horodatages avant de la décrire dans un rapport.
- Recherchez une corroboration indépendante adaptée à l’allégation : les registres d’un autre participant, une capture indépendante ou des registres de service obtenus légalement. Expliquez leur indépendance et leurs limites ; la concordance entre les copies ne suffit pas en soi.
- Conservez le contexte pertinent. Identifiez les fichiers omis, l’historique indisponible et les expurgations. Préparez une [divulgation simplifiée distincte](https://github.com/phishdestroy/TgWitness/blob/main/docs/ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient)si nécessaire, et décrivez ses transformations sans la présenter comme l’original complet.
- Fournissez au destinataire les instructions de vérification ainsi que les éléments nécessaires à ces contrôles. Veillez à ce que les observations, les constatations techniques et les conclusions de l’analyste restent clairement distinctes.

Pour un transfert particulier, indiquez le hachage de l’archive, la clé de confiance, le résultat de la vérification et la limite exacte couverte en externe. Décrivez séparément l’authenticité de la source, l’attribution du compte, l’exhaustivité et les conclusions juridiques. Cela fournit au prochain réviseur des allégations spécifiques à examiner.
