# Exporter et vérifier

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/exports/

Fournissez au destinataire des fichiers qu’il pourra comparer à l’espace de travail de collecte et à son historique enregistré.

Conserver une référenceExporter un fichier ZIP signéLe destinataire vérifie

Vous découvrez les signatures et les points de contrôle ? [Modifiez un exemple d’enregistrement](https://phishdestroy.github.io/TgWitness/fr/docs/concepts/#chain) et voyez quelles vérifications le détectent.

Vous souhaitez conserver une copie hors de portée du collecteur ? Rendez-vous dans [la configuration S3](https://phishdestroy.github.io/TgWitness/fr/docs/exports/#s3), la fonction « [Object Lock »](https://phishdestroy.github.io/TgWitness/fr/docs/exports/#s3-retention) ou [la récupération vérifiée](https://phishdestroy.github.io/TgWitness/fr/docs/exports/#s3-restore).

## Conservez une référence fiable

Enregistrez l’empreinte de la clé publique de l’espace de travail en dehors du collecteur. Lors de la collecte, conservez les points de contrôle signés ailleurs ou faites appel à un [témoin indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/witness/). Ces références permettent au destinataire de vérifier la clé et la limite d’un journal antérieur.

## Télécharger le fichier ZIP signé

Ouvrez **« Exports »** et créez un fichier ZIP de preuves signé. Celui-ci comprend l’historique complet de l’espace de travail et un manifeste de fichiers signé. Utilisez [« Report Studio »](https://phishdestroy.github.io/TgWitness/fr/docs/reports/) pour générer un rapport lisible, ou un [extrait de transfert](https://phishdestroy.github.io/TgWitness/fr/docs/handover/) afin de ne fournir que les données sélectionnées et réduites au minimum.

Les rapports au format HTML, PDF et JSON comportent leurs propres cachets signés et peuvent être vérifiés séparément. Le fichier CSV constitue une copie pratique pour l’analyse ; utilisez le fichier CSV exact contenu dans l’archive ZIP vérifiée pour en vérifier l’intégrité. Conservez l’archive ZIP signée lorsque le destinataire a également besoin des enregistrements sources et des pièces jointes.

## Vérifiez à l'aide d'une copie fiable de TgWitness

Dans l’environnement de projet installé, remplacez l’empreinte digitale et les chemins d’accès aux fichiers indiqués dans l’exemple :

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Lorsque les deux références sont validées, le résultat indique « `key_pinned: true` » et « `checkpoint_checked: true` ». Conservez le résultat de la vérification avec l’archive d’origine. Le point de contrôle conservé doit se situer au plus tard à la limite de l’exportation.

## Utiliser le résultat de la vérification

- **Vérifiez les fichiers fournis :** le manifeste lie leurs hachages, et les signatures des enregistrements lient le journal sauvegardé. Tout fichier modifié ou toute chaîne d’enregistrements brisée est détecté.
- **Vérifiez l’identité de l’espace de travail :** l’empreinte conservée de manière indépendante identifie la clé de signature attendue.
- **Comparez avec une limite antérieure :** un point de contrôle conservé vérifie la conformité de l’exportation par rapport à un préfixe de journal enregistré avant le transfert.
- **Vérifier l’étendue de la collecte :** les lacunes, les résultats de l’acquisition et un test contrôlé d’envoi → modification → suppression décrivent les événements capturés par cette configuration.

Conservez ces résultats avec la copie destinée au destinataire. Vérifiez [ce que la vérification établit](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#verification-scope) concernant la portée des contrôles et l’évaluation distincte des allégations des sources et de la couverture de la collecte.

## Configurer la copie hors site sur S3

Dans votre espace de travail en cours d’exécution, ouvrez **Exports → Copie hors site**. Cette fonctionnalité optionnelle fonctionne avec AWS S3 et d’autres services compatibles S3. Elle copie les segments de journal, les photos et fichiers conservés, les points de contrôle avec leurs réponses horodatées, ainsi que les exportations de discussions terminées. Chaque objet est chiffré sur le collecteur à l’aide de l’algorithme `AES-256-GCM` avant son téléchargement.

La démo en ligne présente les mêmes commandes, mais les téléchargements sont désactivés. Ne saisissez vos identifiants de stockage que dans votre propre espace de travail en cours d'exécution.

[![Panneau complet de configuration hors site : point de terminaison, région, compartiment de stockage, clés d’accès, planification, verrouillage d’objets et contrôles des clés de récupération](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Le panneau complet avec les options avancées est déployé. Aucune information d'identification de stockage n'est affichée.

| Domaine | Que saisir ? |
| --- | --- |
| Point d'extrémité | L'URL du service de stockage, sans chemin d'accès au compartiment ni identifiants. Exemple fictif : `https://s3.example.invalid`. |
| Région | La région requise par votre fournisseur d'accès. La valeur par défaut de l'application est `us-east-1`. |
| Bucket | Un « bucket » existant auquel vous pouvez accéder. Exemple fictif : `example-case-backup`. |
| Dossier dans le compartiment | Le préfixe de l’objet ; valeur par défaut : `tgwitness`. L’application ajoute un préfixe dérivé de l’empreinte de la clé de signature de cet espace de travail. |
| Identifiant de la clé d'accès / Clé d'accès secrète | Saisissez les deux identifiants de stockage simultanément. Ils sont enregistrés dans le coffre-fort de l’espace de travail. Laissez les deux champs vides lors des sauvegardes ultérieures afin de conserver la paire enregistrée. |
| Adresses au format « path » | Utilisez « `endpoint/bucket` » lorsque la fonctionnalité est activée, ou « `bucket.endpoint` » lorsqu’elle est désactivée, selon le fournisseur. |
| Intervalle de copie | De 1 à 1 440 minutes ; valeur par défaut : 5 minutes. L'application doit être en cours d'exécution pour que les sauvegardes programmées puissent s'effectuer. |
| Conservation des données par Object Lock | Durée et mode de conservation pour un compartiment prenant en charge Object Lock. La valeur « zéro jour » maintient la durée de conservation par défaut du compartiment. |

1. Créez le « bucket » auprès de votre fournisseur, puis indiquez sa destination et vos identifiants. Laissez la case « **Conserver une copie hors site »** décochée pendant la préparation, puis sélectionnez « **Enregistrer une copie hors site** ».
2. Sélectionnez « **Tester la connexion** ». Cela permet de télécharger un objet de test chiffré et de vérifier la réponse du stockage.
3. Sélectionnez « **Télécharger la clé de chiffrement** ». Conservez ce fichier séparément du collecteur ; il est nécessaire à la restauration.
4. Cochez la case « **Conserver une copie hors site »** et enregistrez à nouveau. Sélectionnez « **Copier maintenant »** pour une opération manuelle, ou laissez la planification s'exécuter.

## Vérifier la conservation et suivre la progression de la copie

Sous **«** **More options** », choisissez la durée de conservation et sélectionnez « `GOVERNANCE` » ou « `COMPLIANCE` » lorsque votre compartiment prend en charge la fonction « Object Lock ». TgWitness récupère le mode de conservation et la date limite d’un objet téléchargé. Vérifiez le résultat de conservation indiqué séparément : confirmé, conservation manquante ou échec de la vérification.

Le panneau indique le dernier passage, le nombre d’objets, le nombre d’octets transférés, la limite du journal copié et toute erreur éventuelle. Les supports locaux manquants ou modifiés sont signalés et une nouvelle tentative est effectuée lors du passage suivant. Les fichiers, les points de contrôle et les exportations en file d’attente situés après ce support peuvent toujours être copiés.

Les téléchargements utilisent la route Direct, SOCKS5 ou HTTP de l’espace de travail. Choisissez l’une de ces routes pour la copie vers S3 ; une route utilisant uniquement MTProxy laisse la copie en attente et génère une erreur.

## Conservez la clé de récupération à part

Le fichier JSON téléchargé contient la clé de déchiffrement, les paramètres de destination, le préfixe de l’objet de l’espace de travail et l’empreinte digitale de la clé de signature. La restauration nécessite à la fois ce fichier de clé et des identifiants de stockage distincts disposant d’un accès en lecture au compartiment. Conservez-les dans votre plan de restauration.

Si vous modifiez le point de terminaison, le compartiment ou le préfixe du dossier, téléchargez à nouveau le fichier de clé afin que ses paramètres de destination correspondent. L’application lance une nouvelle copie du journal, des fichiers et des points de contrôle conservés localement vers la nouvelle destination. Les exportations de discussions terminées déjà supprimées de la file d’attente de téléchargement locale restent à leur destination précédente.

## Restauration et vérification sur un autre ordinateur

Utilisez une installation fiable de TgWitness, le fichier JSON de clé téléchargé, des identifiants de stockage avec accès en lecture et un répertoire de sortie vide. Remplacez les identifiants fictifs ci-dessous.

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

Les fichiers téléchargés et les objets déchiffrés sont conservés dans un espace de stockage temporaire privé le temps que l’intégralité du journal, les points de contrôle conservés ainsi que les hachages et tailles des médias préservés soient vérifiés. Les chemins d’accès non sécurisés, les segments de journal en conflit et les journaux plus courts que leur point de contrôle sont rejetés. En cas d’échec de la vérification, aucun fichier restauré n’est publié.

Une récupération réussie génère les codes `events.jsonl`, `media/`, `checkpoints/` et `exports/` pour les éléments disponibles dans la copie. Conservez le résultat JSON de la commande avec les éléments récupérés.

Comparez les données récupérées avec vos points de contrôle ou vos enregistrements témoins conservés de manière indépendante, puis examinez la couverture de la collecte enregistrée pour la période qui vous intéresse.
