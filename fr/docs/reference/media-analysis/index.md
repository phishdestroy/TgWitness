# OCR et transcription en local

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/media-analysis/

Reconnaître les images et les fichiers audio capturés à l'aide d'un worker local ; conserver le texte extrait lié à son fichier source.

[Guide des procédures](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Ouvrez un enregistrement du journal `media.saved`, choisissez « **Reconnaître la pièce jointe** », puis sélectionnez « OCR » ou « transcription » sous « **Demander à l’archive** ». Le traitement est manuel et local. Il n’y a ni mode de stockage dans le cloud ni téléchargement automatique. Les octets de la pièce jointe d’origine et le fichier `media_sha256` restent inchangés ; le texte reconnu est explicitement marqué comme issu d’une reconnaissance automatique et stocké séparément avec le hachage source, la version du moteur/modèle, la langue, les paramètres et l’heure d’achèvement. Les transcriptions conservent les horodatages d’origine.

Effectuez une recherche parmi ces résultats à l'aide de **la fonction « Rechercher du texte reconnu »** et du filtre OCR/transcription. Il s'agit d'une recherche distincte sur des données dérivées ; elle ne convertit pas automatiquement la reconnaissance automatique en texte Telegram d'origine ni ne l'ajoute aux événements signés.

## Configurer le worker optionnel

La version 1 nécessite un hôte Linux équipé d’un démon Docker local. Les installations sous Windows peuvent exécuter TgWitness au sein d’un environnement Linux VM/WSL doté de son propre démon local. Le panneau ne décode jamais lui-même une pièce jointe non fiable.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Définissez ces variables dans l’environnement du service TgWitness, puis redémarrez-le. Le socket du démon est par défaut `/var/run/docker.sock` ; les déploiements sans droits root peuvent utiliser `TGWITNESS_DOCKER_SOCKET`. Le worker utilise explicitement ce socket Unix plutôt qu’un contexte Docker distant. N’exposez pas l’API Docker aux utilisateurs du panneau de configuration et ne montez pas son socket à l’intérieur du conteneur de reconnaissance.

Pour la transcription, installez séparément un modèle Whisper compatible avec CTranslate2, puis définissez `TGWITNESS_WHISPER_MODEL_DIR` sur son répertoire. Le worker le charge avec `local_files_only=True` ; le modèle sélectionné et les données d’entrée sont montés en lecture seule. Consultez la [documentation relative au chargement des modèles](https://github.com/SYSTRAN/faster-whisper) du moteur. L'image OCR fournie comprend des données d'entraînement en anglais et en russe. Intégrez une autre langue dans votre image si nécessaire ; les codes de langue suivent [la CLI de Tesseract](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

Aucun modèle n’est récupéré pendant le traitement. La compilation/le téléchargement du programme d’installation peut nécessiter une connexion réseau ; la connexion réseau est désactivée dans chaque conteneur de reconnaissance. Installez l’image avant de l’activer ; l’environnement d’exécution utilise `--pull=never`.

## Limites et récupération

Le conteneur s'exécute en tant qu'utilisateur sans privilèges, avec un compte root en lecture seule, des capacités réduites, le mode `no-new-privileges` , un cœur de processeur, 2 GiB de mémoire, une limite de PID et un système de fichiers temporaire délimité. Seules une copie vérifiée du fichier sélectionné et un répertoire de modèles facultatif sont montés. La base de données, le coffre-fort et la session du collecteur ne sont pas montés. Les [indicateurs du runtime Docker](https://docs.docker.com/reference/cli/docker/container/run/) imposent ces limites ; il s’agit d’une frontière de conteneur, et non d’une enclave matérielle.

La taille des fichiers est limitée à 50 MiB, celle des images à 20 millions de pixels, celle des fichiers audio à 30 minutes avec une durée connue, et la durée de traitement à cinq minutes. Un seul worker s'exécute à la fois, avec au maximum 20 tâches en file d'attente ou en cours d'exécution et 100 tâches conservées par espace de travail. La commande « Cancel » arrête le conteneur ; « Retry » crée une nouvelle tâche liée à la tentative précédente. Les tâches interrompues sont marquées après le redémarrage. Le traitement peut échouer lorsqu’un modèle ne respecte pas les limites configurées ; il ne s’exécute pas en silence sans isolation.
