# Exporter et vérifier

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/exports/

Remettez des fichiers que le destinataire peut vérifier lui-même face à votre espace.

Conserver une référenceExporter un fichier ZIP signéLe destinataire vérifie

Nouveau avec les signatures et points de contrôle ? [Modifiez un enregistrement d’exemple](https://phishdestroy.github.io/TgWitness/fr/docs/concepts/#chain) et voyez quelles vérifications le repèrent.

Vous souhaitez conserver une copie hors de portée du collecteur ? Rendez-vous dans [la configuration S3](https://phishdestroy.github.io/TgWitness/fr/docs/exports/#s3), la fonction « [Object Lock »](https://phishdestroy.github.io/TgWitness/fr/docs/exports/#s3-retention) ou [la récupération vérifiée](https://phishdestroy.github.io/TgWitness/fr/docs/exports/#s3-restore).

## Conservez une référence fiable

Notez l’empreinte de clé de l’espace ailleurs que sur le collecteur. Pendant la collecte, conservez aussi des points de contrôle signés ailleurs ou utilisez un [témoin indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/witness/). C’est avec cela que le destinataire vérifie la clé et un état antérieur du journal.

## Télécharger le fichier ZIP signé

**Exports** → ZIP de preuves signé. Il contient tout le journal et un manifeste de fichiers signé. Mettez en forme le rapport lisible dans [Report studio](https://phishdestroy.github.io/TgWitness/fr/docs/reports/), ou n’envoyez que des données choisies sous forme d’[extrait de transmission](https://phishdestroy.github.io/TgWitness/fr/docs/handover/).

Les rapports HTML, PDF et JSON portent leurs propres sceaux. Le CSV n’est qu’une copie de travail ; pour l’intégrité, prenez le CSV du ZIP vérifié.

## Vérifiez à l'aide d'une copie fiable de TgWitness

Dans l’environnement du projet, avec votre propre empreinte et vos chemins :

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

En cas de succès, vous voyez `key_pinned: true` et `checkpoint_checked: true`. Gardez cette sortie à côté de l’archive. Le point de contrôle doit se trouver à la fin de l’export ou avant.

## Utiliser le résultat de la vérification

- **Fichiers :** le manifeste lie leurs hachages, les signatures lient le journal. Tout changement se voit.
- **Identité :** l’empreinte que vous avez gardée prouve que c’est la clé attendue.
- **État antérieur :** un point de contrôle compare l’export avec un début de journal enregistré avant la transmission.
- **Couverture :** les lacunes, les résultats d’acquisition et un test envoyer → modifier → supprimer montrent ce que cette configuration a vraiment capté.

Détails : [ce que la vérification prouve et ce qu’elle ne prouve pas](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#verification-scope).

## Configurer la copie hors site sur S3

**Exports → Copie externe** dans votre espace. Fonctionne avec AWS S3 et tout service compatible S3. Copie les segments du journal, les fichiers enregistrés, les points de contrôle avec leurs horodatages et les exports de chats terminés, chacun chiffré en `AES-256-GCM` avant de quitter le collecteur.

La démo en ligne montre ces réglages avec l’envoi désactivé. Ne saisissez de vrais identifiants que dans votre propre installation.

[![Panneau complet de configuration hors site : point de terminaison, région, compartiment de stockage, clés d’accès, planification, verrouillage d’objets et contrôles des clés de récupération](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Le panneau complet avec les options avancées est déployé. Aucune information d'identification de stockage n'est affichée.

| Domaine | Que saisir ? |
| --- | --- |
| Point d'extrémité | URL du stockage, sans chemin de bucket ni identifiants. Exemple : `https://s3.example.invalid`. |
| Région | Ce que demande votre fournisseur. Par défaut `us-east-1`. |
| Compartiment | Un bucket existant où vous pouvez écrire. Exemple : `example-case-backup`. |
| Dossier dans le compartiment | Préfixe, par défaut `tgwitness`. Un préfixe par espace s’y ajoute. |
| Identifiant de la clé d'accès / Clé d'accès secrète | Les deux ensemble, stockées dans le coffre. Laissez-les vides plus tard pour les conserver. |
| Adresses au format « path » | Activé : `endpoint/bucket`. Désactivé : `bucket.endpoint`. Selon le fournisseur. |
| Intervalle de copie | De 1 à 1 440 minutes, 5 par défaut. Seulement pendant que l’application tourne. |
| Conservation des données par Object Lock | Jours et mode, si le bucket prend en charge Object Lock. Zéro garde la valeur par défaut du bucket. |

1. Créez le bucket, remplissez destination et identifiants avec **Conserver une copie externe** décoché, puis cliquez sur **Enregistrer la copie externe**.
2. **Tester la connexion** envoie un objet de test chiffré.
3. **Télécharger la clé de chiffrement** et gardez-la loin du collecteur. Pas de clé, pas de récupération.
4. Cochez **Conserver une copie externe**, enregistrez, puis **Copier maintenant** ou laissez la planification tourner.

## Vérifier la conservation et suivre la progression de la copie

Dans **Plus d’options**, choisissez les jours de rétention et `GOVERNANCE` ou `COMPLIANCE`. TgWitness relit la rétention sur un objet envoyé et vous indique : confirmée, absente ou échec de vérification.

Le panneau affiche le dernier passage, le nombre d’objets, les octets, la limite du journal copié et les erreurs. Un fichier local manquant est signalé et retenté au passage suivant ; le reste continue d’être copié.

Les envois passent en direct, par SOCKS5 ou par HTTP. Avec un itinéraire uniquement MTProxy, la copie attend avec une erreur.

## Conservez la clé de récupération à part

Le JSON de clé contient la clé de déchiffrement, la destination, le préfixe et l’empreinte de clé. Pour récupérer, il vous faut ce fichier plus des identifiants de stockage avec droit de lecture.

Endpoint, bucket ou préfixe changé ? Retéléchargez la clé. Une nouvelle copie démarre à la nouvelle destination ; les anciens exports restent où ils étaient.

## Restauration et vérification sur un autre ordinateur

Il vous faut une installation de TgWitness de confiance, le JSON de clé, des identifiants en lecture seule et un dossier vide :

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

Tout est d’abord vérifié dans un dossier temporaire privé : le journal entier, les points de contrôle, les hachages et tailles des fichiers. Chemins dangereux, segments contradictoires ou journal plus court que son point de contrôle échouent, et alors rien n’est écrit.

En cas de succès, vous obtenez `events.jsonl`, `media/`, `checkpoints/` et `exports/`. Gardez avec eux la sortie JSON de la commande et comparez avec les points de contrôle ou entrées du témoin que vous conservez vous-même.
