# Exporter et vérifier

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/exports/

Partagez un enregistrement signé que quelqu’un d’autre pourra vérifier.

Conserver une référenceExporter un fichier ZIP signéLe destinataire vérifie

Vous découvrez les signatures et les points de contrôle ? [Modifiez un exemple d’enregistrement](https://phishdestroy.github.io/TgWitness/fr/docs/concepts/#chain) et voyez quelles vérifications le détectent.

Vous souhaitez conserver une copie hors de portée du collecteur ? Rendez-vous dans [la configuration S3](https://phishdestroy.github.io/TgWitness/fr/docs/exports/#s3), la fonction « [Object Lock »](https://phishdestroy.github.io/TgWitness/fr/docs/exports/#s3-retention) ou [la récupération vérifiée](https://phishdestroy.github.io/TgWitness/fr/docs/exports/#s3-restore).

## Conservez une référence fiable

Enregistrez l’empreinte de la clé publique de l’espace de travail en dehors du collecteur. Lors de la collecte, conservez les points de contrôle signés ailleurs ou faites appel à un [témoin indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/witness/). Ces références permettent au destinataire de vérifier la clé et la limite d’un journal antérieur.

## Télécharger le fichier ZIP signé

Ouvrez « **Exports »** et créez un fichier ZIP de preuves signé. Celui-ci comprend le journal de l'espace de travail et un manifeste de fichiers signé. Les filtres du panneau ne limitent pas cette exportation du journal complet : veuillez examiner le contenu avant de le partager.

Les téléchargements HTML et CSV autonomes sont utiles pour la lecture et l’analyse. Conservez le fichier ZIP signé comme original vérifiable ; le fichier HTML ou CSV séparé ne comporte pas de signature autonome.

## Vérifiez à l'aide d'une copie fiable de TgWitness

Dans l’environnement de projet installé, remplacez l’empreinte digitale et les chemins d’accès aux fichiers indiqués dans l’exemple :

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Lorsque les deux références sont validées, le résultat indique « `key_pinned: true` » et « `checkpoint_checked: true` ». Conservez le résultat de la vérification avec l’archive d’origine. Le point de contrôle conservé doit se situer au plus tard à la limite de l’exportation.

## Comprendre le résultat

- **Intégrité :** l'historique enregistré et les fichiers exportés correspondent à leurs signatures.
- **Remarque préalable :** un point de contrôle externe vous permet de comparer l'exportation avec un préfixe de journal précédemment conservé.
- **Fonctionnement :** un test contrôlé « envoi → modification → suppression » vérifie la concordance entre des événements spécifiques et l'historique capturé.

Une signature valide ne prouve pas que chaque événement Telegram ait bien eu lieu, que la source ait dit la vérité ou que l’horloge du collecteur ait été exacte.

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

1. Saisissez la destination et vos identifiants. Laissez la case « **Conserver une copie hors site »** décochée pendant la préparation, puis sélectionnez « **Enregistrer une copie hors site** ».
2. Sélectionnez « **Tester la connexion** ». Cela permet de télécharger un objet de test chiffré et de vérifier la réponse du stockage.
3. Sélectionnez « **Télécharger la clé de chiffrement** ». Conservez ce fichier séparément du collecteur ; il est nécessaire à la restauration.
4. Cochez la case « **Conserver une copie hors site »** et enregistrez à nouveau. Sélectionnez « **Copier maintenant »** pour une opération manuelle, ou laissez la planification s'exécuter.

Ne crée pas de compartiment de stockage. Les téléchargements programmés s’arrêtent lorsque l’application cesse de fonctionner.

## Vérifier la conservation et suivre la progression de la copie

Dans **« Plus d’options** », choisissez la durée de conservation et « `GOVERNANCE` » ou « `COMPLIANCE` » si votre compartiment prend en charge la fonctionnalité Object Lock. TgWitness relit le mode de conservation et la date limite d’un objet téléchargé. Le statut indique une confirmation, une conservation manquante ou un échec de vérification ; un téléchargement réussi ne constitue pas à lui seul une confirmation de conservation.

Le panneau indique le dernier passage, le nombre d’objets, le nombre d’octets transférés, la limite du journal copié et toute erreur éventuelle. Les supports locaux manquants ou modifiés sont signalés et une nouvelle tentative est effectuée lors du passage suivant. Les fichiers, les points de contrôle et les exportations en file d’attente situés après ce support peuvent toujours être copiés.

Les téléchargements s'effectuent via les protocoles Direct, SOCKS5 ou HTTP de l'espace de travail. La copie vers S3 n'est pas disponible via MTProxy ; l'application ne bascule pas vers une connexion directe.

Cela n’oblige pas un fournisseur à appliquer la fonctionnalité « Object Lock » simplement parce que le téléchargement a été accepté.

## Conservez la clé de récupération à part

Le fichier JSON téléchargé contient la clé de déchiffrement, les paramètres de destination, le préfixe de l’objet de l’espace de travail et l’empreinte digitale de la clé de signature. Il ne contient pas les identifiants d’accès à S3 : la restauration nécessite des identifiants distincts disposant d’un accès en lecture au compartiment.

Si vous modifiez le point de terminaison, le compartiment ou le préfixe du dossier, téléchargez à nouveau le fichier de clé afin que ses paramètres de destination correspondent. L’application lance une nouvelle copie du journal, des fichiers et des points de contrôle conservés localement vers la nouvelle destination. Les exportations de discussions terminées déjà supprimées de la file d’attente de téléchargement locale restent à leur destination précédente.

**Ne fait pas :** il ne déchiffre pas la copie sans la clé exportée. Les identifiants d’accès au stockage ne peuvent pas remplacer cette clé.

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

**Ne fait pas :** il ne reconstitue pas les observations qui ne sont jamais parvenues au journal et ne remplace pas un point de contrôle ou un témoin conservé de manière indépendante.
