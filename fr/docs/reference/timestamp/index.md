# Horodatages

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/timestamp/

Horodatages RFC 3161 pour les points de contrôle signés : ce qui est envoyé à l’autorité et comment la réponse est vérifiée.

TgWitness prépare des requêtes RFC 3161 et vérifie les réponses de l’autorité d’horodatage (TSA). Cette procédure manuelle ne sélectionne pas de TSA et n’envoie pas de données ; le mode « preuves » effectue ces deux opérations selon un calendrier défini ([format de preuve](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)). Une requête préparée **ne** constitue **pas encore une preuve d’horodatage**.

## Ce que la preuve établit

Organigramme · Observations relatives aux comptes → Chaîne SHA-256 et signatures Ed25519; Chaîne SHA-256 et signatures Ed25519 → Point de contrôle signé; Point de contrôle signé → Hachage au byte près et nonce aléatoire; Hachage au byte près et nonce aléatoire → Requête RFC 3161; Requête RFC 3161 → TSA indépendante; TSA indépendante → Réponse signée de la TSA; Point de contrôle signé → Vérification des données, du nonce et de la confiance explicite envers l'autorité de certification (CA); Réponse signée de la TSA → Vérification des données, du nonce et de la confiance explicite envers l'autorité de certification (CA) · Observations relativesaux comptes · Chaîne SHA-256 etsignatures Ed25519 · Point de contrôlesigné · Hachage au byte prèset nonce aléatoire · Requête RFC 3161 · TSA indépendante · Réponse signée de laTSA · Vérification desdonnées, du nonce etde la confianceexplicite enversl'autorité decertification (CA)

**Schéma sous forme de texte**

1. Observations relatives aux comptes → Chaîne SHA-256 et signatures Ed25519
2. Chaîne SHA-256 et signatures Ed25519 → Point de contrôle signé
3. Point de contrôle signé → Hachage au byte près et nonce aléatoire
4. Hachage au byte près et nonce aléatoire → Requête RFC 3161
5. Requête RFC 3161 → TSA indépendante
6. TSA indépendante → Réponse signée de la TSA
7. Point de contrôle signé → Vérification des données, du nonce et de la confiance explicite envers l'autorité de certification (CA)
8. Réponse signée de la TSA → Vérification des données, du nonce et de la confiance explicite envers l'autorité de certification (CA)

La signature du collecteur lie les enregistrements à sa clé. Une réponse fiable de la TSA permet d’établir qu’un point de contrôle particulier existait à l’heure indiquée par la TSA. Le point de contrôle peut alors lier le préfixe du journal. Cela ne permet pas d’établir l’heure de chaque action sur Telegram ni la véracité du contenu capturé.

## Procédure

1. Conservez l’empreinte digitale de la clé du collecteur via un canal de confiance distinct. Une clé fournie uniquement par le fichier ZIP examiné ne suffit pas à identifier le collecteur.
2. Dans **Exportations → Préparer la demande d’horodatage**, téléchargez le fichier ZIP de la demande correspondant à l’espace de travail sélectionné. Extrayez les fichiers `checkpoint.json`, `timestamp.tsq`, `SHA256SUMS` et `README.txt`. Ne modifiez pas les octets de contrôle.
3. Choisissez un TSA adapté à l’enquête. Envoyez `timestamp.tsq` en suivant la méthode documentée, avec `application/timestamp-query` pour un service HTTP. Enregistrez la réponse binaire d’origine sous le nom `timestamp.tsr`, ainsi que le point de terminaison, l’heure de récupération et le résultat de la requête. La requête contient un hachage et un nonce plutôt que des messages ; les métadonnées du réseau permettent néanmoins d’identifier la requête.
4. Obtenez le certificat racine de confiance indépendamment de la réponse, ainsi que tous les certificats intermédiaires requis. Un certificat figurant dans la réponse ne devient pas pour autant de confiance simplement parce qu’il y est inclus.
5. À partir d’une installation fiable de TgWitness, vérifiez :

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

Ajoutez `--intermediates tsa-intermediates.pem` ou `--openssl /path/to/openssl` si nécessaire. OpenSSL doit prendre en charge `ts`. Sous Windows, le vérificateur recherche également l’installation standard de Git. OpenSSL 3.5.9 a été testé localement avec une CA/TSA synthétique.

1. Exportez un fichier ZIP contenant le journal signé après le point de contrôle afin qu’il inclue ce préfixe. Vérifiez à l’aide de l’empreinte digitale connue de manière indépendante :

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. Conservez le fichier ZIP, le point de contrôle, la requête, la réponse, la chaîne de certificats, les résultats de vérification et l’historique de transfert en dehors du collecteur. Répétez la vérification à la réception.

Pour préparer une requête à partir d’un point de contrôle enregistré :

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

La préparation normalise le format JSON et inclut le point de contrôle correspondant dans l’archive. Utilisez les **octets du point de contrôle issus de cette archive** pour la vérification TSA, même si le fichier d’entrée comportait des espaces différents.

## Limites de la vérification

| Vérifier | Comportement actuel |
| --- | --- |
| Données | La valeur SHA-256 des octets exacts du point de contrôle doit correspondre à la réponse |
| Demande | Avec `--request`, la requête d'origine et le nonce sont vérifiés |
| Signature TSA | OpenSSL vérifie la signature et la chaîne de certificats jusqu’à l’autorité de certification (CA) explicitement désignée. |
| Signature du collecteur | Vérifié séparément par le vérificateur du journal à l’aide d’une clé épinglée |
| Révocation | Pas de récupération automatique des fichiers OCSP/CRL |
| Validité à long terme | Aucune validation des archives après l'expiration du certificat |
| Soumission programmée | Mode « Evidence », désactivé par défaut |

`--request` est techniquement facultatif, mais son omission empêche la vérification du nonce d’origine. Pour que cette procédure soit complète, le résultat `request_checked` doit être vrai. La vérification des certificats suit les règles et les délais de vérification d’OpenSSL tel qu’il est installé. La conservation à long terme nécessite une politique distincte en matière de certificats et de preuves de révocation.

Une signature cryptographique valide ne constitue pas automatiquement un horodatage qualifié ni une détermination de la recevabilité juridique. Si un opérateur a falsifié des observations avant l’horodatage, le TSA ancre ces octets ; il n’établit pas leur véracité.

## Compte rendu de transfert

Enregistrez l’identifiant du dossier, l’expéditeur et le destinataire, l’heure de transfert (UTC) et sa source, l’objet, les noms de fichiers/valeurs SHA-256, l’empreinte du collecteur, la plage de séquences, les lacunes connues, la version du vérificateur et le résultat de la vérification. Signez et conservez ce document de manière indépendante conformément aux procédures de votre organisation. TgWitness ne dispose pas d’un système de conservation des documents multi-utilisateurs.

Aucune autorité de certification (TSA) indépendante n’a été contactée pendant le développement. Des tests locaux créent une autorité de certification (CA) ou une TSA synthétique afin de vérifier la compatibilité et le rejet des données modifiées, des nonces ou des CA.
