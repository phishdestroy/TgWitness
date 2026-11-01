# Ce qui a été testé

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/

Le test Telegram en direct, les vérifications automatisées, les vérifications au niveau du navigateur et ce qui reste à vérifier.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Nombre |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| Vérifier | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Test Telegram en direct, compte complet · 29 octobre 2026

Le même compte a continué à fonctionner après le test ci-dessous. Le 29 octobre à 12 h 10 UTC, son champ d’application a été étendu à l’ensemble du compte (chaînes, groupes, discussions privées et bots) ; le panneau a demandé une confirmation et le journal signé a enregistré cette opération. À 17 h 59 UTC, le journal contenait :

| Enregistré du 27 octobre à 21 h 36 au 29 octobre à 17 h 59 (UTC) | Nombre |
| --- | --- |
| Enregistrements du journal | 9,968 |
| Nouveaux messages | 5,308 |
| parmi eux après le passage au compte complet | 3,878 |
| Suppressions | 784 |
| parmi lesquels certains ont été supprimés après que TgWitness eut enregistré le message | 596 |
| Modifications | 41 |
| Messages ajoutés à la suite de vérifications supplémentaires | 2,273 |
| Messages qu’une nouvelle vérification n’a plus pu retrouver | 18 |
| Messages enregistrés par des instantanés de l'historique | 242 |
| Pièces jointes enregistrées | 247 |
| Le collecteur démarre | 19 |
| Pause de Telegram FloodWait | 26 |

- Le contrôle **« Verify »** du comité a confirmé les signatures et la chaîne de hachages des 9 968 enregistrements.
- Les messages provenaient de 2 groupes ou canaux, ainsi que de 3 discussions privées et de bots. Un bouton de message a été actionné depuis **la section « Discussions »** ; la requête et la réponse de Telegram figurent dans le journal.
- De nouvelles conversations ont été ajoutées lorsque le collecteur a réanalysé le compte lors d’un redémarrage. L’enregistrement des messages antérieurs des nouvelles conversations était désactivé (`history = 0`) ; ce cas n’est donc pas abordé ici.

Ne sont pas pris en compte : les réactions, les changements d’adhésion, les profils des utilisateurs, l’envoi de messages, l’adhésion sur invitation, les proxys, les notifications, le bot « witness » et l’utilisation simultanée de plusieurs comptes. Les fichiers publics ne contiennent que des chiffres.

## Fichier d'exportation protégé par mot de passe, ouvert avec libarchive · 29 octobre 2026

Une archive créée à l’aide du code de chiffrement d’exportation (WinZip AES-256, format lu par 7-Zip et WinRAR ) a été ouverte sous Windows à l’aide de l’`tar` (bsdtar 3.6.2, libarchive). Avec le mot de passe correct, le fichier extrait correspondait au SHA-256 d’origine ; un mot de passe erroné a été refusé avec le message « Phrase de passe incorrecte ». Les logiciels 7-Zip et WinRAR n’ont pas été exécutés.

## Test en direct sur Telegram · Du 27 au 29 octobre 2026

Un compte Telegram réel, connecté via le pool de paires d’API intégré, a enregistré un supergroupe du **27 octobre à 21 h 36 UTC au 29 octobre à 05 h 15 UTC**. Le collecteur a été lancé 12 fois au cours de cette période.

| Enregistré | Nombre |
| --- | --- |
| Enregistrements du journal, y compris les « heartbeats » et les enregistrements de service | 2,385 |
| Nouveaux messages | 1,291 |
| Suppressions | 472 |
| parmi lesquels certains ont été supprimés après que TgWitness eut enregistré le texte | 347 |
| Modifications | 12 |
| Messages manqués pendant l’arrêt, ajoutés lors de la nouvelle vérification | 12 |
| Pièces jointes enregistrées | 17 |
| Pièces jointes non téléchargées (téléchargement désactivé ou aucun fichier à télécharger) | 14 |
| Telegram FloodWait effectue des pauses de 3 secondes chacune lors des vérifications | 8 |

- Les signatures et la chaîne de hachages des 2 385 enregistrements sont vérifiables à l'aide de la clé publique du journal.
- Après un redémarrage, le collecteur reprend à partir de l'état de mise à jour enregistré (`pts`) et Telethon rattrape son retard ; la nouvelle vérification ajoute ensuite les messages qui manquent encore.
- À chaque événement « FloodWait », le collecteur attendait la durée demandée avant de poursuivre.
- Le compte est resté connecté, et la même session s'est reconnectée le 29 octobre.

Ne sont pas couverts par ce test : la gestion simultanée de plusieurs comptes, les rôles d’administrateur, les proxys, les pannes d’une durée supérieure à quelques heures et la [procédure complète d’acceptation en direct](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Les fichiers publics ne contiennent que ces données : aucun identifiant de compte ou de discussion, aucun message ni aucune information d’identification.

Les entrées plus anciennes ci-dessous décrivent leurs propres exécutions ; la plupart d’entre elles ont utilisé des clients de test synthétiques. Les derniers résultats automatisés figurent ci-dessous.

## Listes MTProxy publiques intégrées · 29 octobre 2026

Il s'agit de l'historique des tests de la version originale à sélection manuelle. Pour les modes actuels de pool automatique et d'adresse IP, veuillez consulter [les paramètres de connexion](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/#ip-modes). Les chiffres et les fonctionnalités non prises en charge indiqués ci-dessous se rapportent à cette version testée.

Ajout d’un instantané public groupé et d’un rafraîchissement HTTPS explicite à partir de SoliSpirit/mtproto et zakky8/mtproto-proxy-pro. Sur cet hôte, le programme de téléchargement de l’application a récupéré les deux flux avec succès le 29 octobre 2026 à 12 h 58 UTC : **118 points de terminaison uniques compatibles** après filtrage, déduplication et application de la limite de 64 entrées par source. Cela permet de vérifier la récupération de la liste, et non la connectivité ou la transmission de messages via ces points de terminaison. Aucun compte réel n’a été connecté à un proxy répertorié au cours de ce travail. [Guide de l’opérateur et de l’utilisateur](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/PROXIES.md).

Les réponses de source échouées, vides ou incompatibles conservent les entrées et les dates précédentes. Les mises à jour ne modifient pas l’itinéraire sélectionné. Les adresses publiques sont validées et les adresses IP résolues sont enregistrées lors de la sélection ; les itinéraires définis par l’opérateur ou manuellement restent distincts. Le test de connexion est désormais disponible dans le panneau avant la connexion au compte. Les faux certificats TLS et la sélection automatique de proxy ne sont toujours pas pris en charge. Le catalogue de l’opérateur remplace entièrement les abonnements.

- Suite complète : **366 tests réussis, 3 ignorés**, 287,94 secondes. Les avertissements relatifs aux dépendances existantes et les ignorances liées à la plateforme persistent. Régression finale de la liste publique/localisation : **36 tests réussis**, y compris le rejet des ports de proxy de téléchargement non valides ; cela recoupe la suite complète.
- Test de compatibilité avec les navigateurs réussi en anglais/russe, modes clair/foncé à 390/1 440 pixels : options intégrées, aucune requête externe à l’ouverture des paramètres, actualisation explicite, conservation des chemins d’accès et du cache en cas de défaillance, test préalable à la connexion, isolation de l’espace de travail en cas de réponse tardive, détails de la source et mise en page/contraste. Aucune erreur JavaScript ni requête externe du navigateur.
- La couverture finale de la traduction statique a été validée pour les 13 langues ; le nouveau contenu a été traduit en russe, avec des versions de secours en anglais explicites ailleurs. Le guide intégré mis à jour a passé avec succès les contrôles de mise en page et de contraste dans les deux thèmes.
- Contrôles « Ruff » et de publication réussis (259 fichiers publics, 1 354 liens locaux) ; mise à jour du fichier « Compose » et analyse du fichier YAML de l’environnement de CI. Docker et l’environnement de CI à distance n’ont pas été exécutés ici.
- La roue reconstruite a passé avec succès les tests d’installation isolée, de chargement de la liste des paquets intégrés et de vérification de l’exportation signée. Les 69 ressources du paquet correspondaient toutes à l’espace de travail ; les hachages des sources ont été vérifiés.

Reçus : `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json` et `test-results/public-proxies-package.log`. Les paramètres de navigateur, de compte et de transport sont fictifs ; les deux téléchargements de flux ci-dessus correspondent à de véritables requêtes HTTPS.

## Présentation des options supplémentaires · 29 octobre 2026

L’ancienne page dédiée au bot Proof s’appelle désormais **« Extras »** : un bref aperçu suivi d’une page de configuration distincte pour l’option sélectionnée. Le formulaire « Witness » comporte trois étapes, les paramètres de connexion, les options réseau et les détails de déploiement étant masqués. L’utilisation de GitHub est explicitement prévue et ne nécessite aucun formulaire d’identifiants. [Présentation en russe](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/EXTRAS.md).

- 30 tests ciblés ont été validés concernant la localisation, la configuration de Witness et les vérifications de publication.
- Tests d’acceptation de la configuration Chromium réussis en anglais/russe, modes clair/foncé, à 390/1440 pixels : focalisation du clavier et touche Entrée, absence de connexions implicites lors de la sélection des options supplémentaires, conservation des brouillons, téléchargements des configurations et jetons épinglés, effacement des jetons au verrouillage, et bon fonctionnement des ancres du guide local. Contrôles de mise en page et de contraste du texte sur fond uni réussis.
- La prise en charge du changement d’espace de travail a été validée, y compris la réception d’une réponse de jeton différée après un changement. Une navigation rapide permet de trouver les fonctionnalités supplémentaires via les termes « bot », « proof » et « GitHub » ; les tests existants pour les résolutions 320/390/1440 pixels et les vérifications pour le russe et l’affichage de droite à gauche (RTL) ont également été validés.
- Aucune erreur JavaScript ni aucune requête externe du navigateur n’a été observée lors de l’exécution de la configuration. Il s’agit de vérifications synthétiques de l’interface utilisateur, et non de nouvelles preuves issues de publications en direct sur Telegram ou par des bots.
- Le chargement final des langues et la couverture du dictionnaire ont été validés pour les 13 langues prises en charge, en conservant des solutions de repli explicites en anglais pour toutes les langues autres que le russe. Le guide Proof enrichi a également passé avec succès les contrôles de mise en page et de contraste aux résolutions de 320/768/1 440 pixels dans les deux thèmes.
- La version remaniée a passé avec succès les tests d’installation isolée et de vérification de l’exportation signée. Les 67 ressources packagées correspondaient toutes à l’espace de travail ; l’archive source contient 253 fichiers publics . La vérification des sources et des liens a été validée pour 1 346 liens de documentation locaux.

Références : `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log` et `test-results/extras-artifacts.json`. Les captures d’écran proviennent d’espaces de travail synthétiques.

## Audit de la configuration du bot Witness et du proxy · 29 octobre 2026

La configuration de Witness (désormais **Extras → Un bot dans votre chaîne**) prépare un témoin déployé de manière indépendante : clé de collecte épinglée, téléchargement de jeton à portée limitée, chaîne dédiée, politique de publication, route HTTP/SOCKS5 et API Bot personnalisée. Le jeton du bot reste sur l’hôte du témoin. Son nouveau jeton « `--check-config` » valide la configuration et les fichiers sans établir de connexion réseau ni créer de clé. Les chemins d’accès aux fichiers JSON sont résolus parallèlement à la configuration. Toutes les variantes du témoin Compose transmettent désormais les paramètres du proxy HTTP et de l’API du bot.

Les paramètres du compte prennent en charge un catalogue MTProxy public géré par l’opérateur, un aperçu personnalisé des liens proxy Telegram ainsi que les champs manuels existants. Les réponses du catalogue omettent les informations confidentielles ; la sélection enregistre l’itinéraire dans le coffre-fort de l’espace de travail. En cas de catalogues manquants ou mal formés, les itinéraires manuels restent disponibles. Aucune adresse de proxy de projet ni aucun service témoin hébergé ne sont créés ou activés par défaut. Un exemple Caddy n’expose que le point de terminaison « head » limité lorsqu’un témoin externe doit accéder à un collecteur dont le panneau reste privé.

Validation :

- Suite complète : **348 tests réussis, 3 tests ignorés**, 195,81 secondes. Les limitations de Windows expliquent les tests ignorés ; les deux avertissements de dépréciation de dépendances existants persistent.
- Dernière série de tests de régression « witness/configuration/release » : **11 réussis, 1 ignoré**. Celle-ci recoupe l’ensemble complet des tests. Les tests incluent la résolution de chemin d’accès, la vérification préalable hors ligne, la signature/publication via un dispositif réel d’API HTTP Bot en boucle fermée, l’échec de la remise enregistrée, la vérification du jeton de canal et l’exclusion du secret de proxy.
- Test de configuration de Chromium réussi en anglais/russe à 390/1 440 pixels : configuration épinglée et téléchargements de jetons, effacement des jetons au verrouillage, sélection du catalogue, aperçu des liens personnalisés suivi d’une sauvegarde explicite, mise en page/contraste et absence d’erreurs JavaScript ou de requêtes externes au navigateur. Correction du débordement de l’en-tête du compte russe et de l’onglet de connexion en raison d’une largeur insuffisante.
- Vérifications Ruff, des sources et des liens, ainsi que l’analyse YAML de Compose et du workflow : validées.
- La version remaniée a passé avec succès les tests d’installation isolée, de vérification des panneaux/ressources statiques et d’authentification via l’API, ainsi qu’une vérification indépendante des exportations synthétiques de 32 événements, en direct et en flux continu.

Justificatifs : `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log` et `setup-package.log`. Ces vérifications utilisent des comptes synthétiques/proxys et une infrastructure locale d’API pour bot. Elles ne prétendent pas reproduire une publication réelle par un bot, un serveur MTProxy public opérationnel, l’exécution d’une infrastructure de test à distance ou un déploiement Docker. L’historique réel des observations Telegram conservé ci-dessus reste un élément de preuve distinct. [Instructions de configuration](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

## Révision de la présentation et de la documentation · 29 octobre 2026

La page du produit, l’écran d’accès, les fichiers README en anglais et en russe ainsi que les images de présentation adoptent désormais un style visuel harmonisé. Les captures d’écran publiques utilisent des données de démonstration fictives. Cette révision a également permis de corriger les descriptions obsolètes concernant la validation en temps réel et la récupération mentionnées ci-dessus.

- Tests de localisation, de site et de publication ciblés : **33 réussis, 1 ignoré**. Le test ignoré nécessite la création d’un lien symbolique, fonction non disponible sur cet hébergeur.
- La validation générale du panneau Chromium a été approuvée, y compris l’ensemble des catalogues de langues, la mise en page RTL, les thèmes clair/foncé, le contraste textuel optimal et le changement d’espace de travail. La vérification de la création de profil attend désormais la réponse HTTP effective avant de vérifier l’espace de travail sélectionné.
- Les écrans d’accès en anglais et en russe ont passé avec succès les contrôles de mise en page et de contraste dans les deux thèmes aux résolutions de 320, 390, 768, 850 et 1 440 pixels ; le bouton « Soumettre » reste visible dans la zone d’affichage initiale.
- La compatibilité avec les sites publics a été validée aux résolutions de 320, 390, 768, 1 024 et 1 440 pixels, y compris les , l’agrandissement des captures d’écran/la touche Échap/le retour au focus, les tabulations au clavier, le refus du presse-papiers, les sous-chemins du projet, la réduction des animations et la solution de secours sans JavaScript. Aucune requête de ressource infructueuse, aucune requête externe ni aucune erreur JavaScript n’ont été observées.
- La version remaniée a passé avec succès un test d’installation isolée : les ressources du panneau et les paramètres régionaux se chargent, l’accès à l’API nécessite une authentification, et les exportations directes/en continu vérifient indépendamment les 32 événements synthétiques. Les vérifications Ruff et des sources publiques/liens ont été validées.

Reçus locaux : `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log` et `design-package/install-receipt.json`. La suite complète du backend n’a pas été réexécutée pour cette modification de la présentation/documentation ; son résultat précédent figure toujours dans l’audit préalable à la publication.

## Version 0.6.1

La version 0.6.1 modifie la présentation du panneau de configuration, les lanceurs, l’emballage et la documentation ; le code relatif à la collecte, au stockage, à la signature et à l’exportation reste inchangé. Sous Windows 11 / Python 3.12.10 avec le runtime épinglé :

- La suite complète a réussi **137 tests,** avec **2 tests ignorés** et l’avertissement Starlette existant. Les nouveaux tests portent sur la gestion de la combinaison Ctrl+C par le lanceur (le serveur dispose de 30 secondes pour un arrêt ordonné) et sur les échecs exploitables lors des étapes de configuration.
- Chromium (shell sans interface graphique 156) a réussi les **45 scénarios généraux** et **les 35 scénarios d’importation de compte/QR/clé d’authentification**, y compris le contrôle du contraste du texte plein, l’absence de dépassement horizontal entre 320 et 1 440 px et la visibilité des champs de première connexion à 320/390 px. Aucune erreur JavaScript sur la page ni aucune requête externe n’ont été observées.
- `python start.py --setup-only` a réinstallé le paquet en version 0.6.1 et `python start.py --check` a signalé qu'il était prêt. Un véritable serveur `python -m tgwitness --demo` a renvoyé le panneau de configuration, la feuille de style, le script, le logo, le guide et la version `/api/status` 0.6.1 ; le serveur `workspace.css`, qui avait été supprimé, a renvoyé une erreur 404.
- `Start.cmd` a détecté une installation de Python en dehors du PATH. En l’absence de Python disponible, il a affiché l’offre d’installation ; après avoir refusé les instructions du manuel imprimé, il a quitté le programme 1. L’étape de téléchargement sur python.org a permis d’obtenir le programme d’installation de la version 3.12.10, qui a passé avec succès le contrôle Authenticode de la Python Software Foundation ; le programme d’installation lui-même n’a pas été exécuté sur cet hôte.
- `start.sh`, sans aucune instruction Python, a affiché l’astuce d’installation puis s’est arrêté. 1. `scripts\Docker.cmd` et `scripts/docker-start.sh` ont été testés sur de faux exécutables `docker` : séquence d’appel correcte, adresse du panneau et sortie du jeton correctes, et aucun message de réussite après un échec.
- `python tools/build_portable.py` a créé un package Windows de 18,8 MiB après avoir vérifié la somme de contrôle du runtime intégrable épinglé. Une fois extrait vers un chemin d'accès contenant des espaces et lancé avec uniquement les répertoires `C:\Windows` dans le PATH, son Python intégré a réussi le test `TgWitness-Check.cmd`, a mis à disposition la démo (32 événements) et un espace de travail en direct, et Chromium a affiché le journal et le volet de détails sans erreur JavaScript. Les données ont été écrites dans le dossier `data` du package.
- `python tools/build_preview.py` a généré une archive source de 110 fichiers. Un test de simulation de `git add` a répertorié ces mêmes 110 fichiers, sans aucun fichier de session, de clé, de base de données, de jeton, de journal ou d’exportation, sans aucun chemin d’accès absolu local et sans aucune chaîne de caractères pouvant constituer un secret.

Éléments non exécutés lors de cette série de tests du 27 octobre : l’installation automatique de Python elle-même, les vérifications de la compilation Docker et de Docker Compose, les exécutions sous Linux/macOS ou un nouvel exercice sur un compte actif . Des preuves réelles issues de Telegram sont consignées ci-dessus et dans les vérifications de compte précédentes ci-dessous. Les définitions CI ne suffisent pas à elles seules à valider l’exécution sur la plateforme.

## Version 0.6.0

La dernière suite complète « pinned-runtime » sous Windows 11 / Python 3.12.10 a réussi **135 tests**, avec **1 test ignoré**, en 26,53 secondes, tout en affichant l’avertissement Starlette existant. L'omission nécessite des autorisations POSIX. Après avoir ajouté le moteur de rendu QR aux vérifications de préparation et aux mesures de processus, 8 vérifications de préparation/espace de travail concernées ont également été réussies.

Les nouvelles fonctionnalités incluent les schémas Telethon 7/8, les schémas Pyrogram 2/3, les clés JSON complètes et les fichiers JSON contenant uniquement des métadonnées, les fichiers de comptes correspondants ou en conflit, les codes d’accès TData, la falsification des sommes de contrôle et les chemins d’accès non sécurisés, la conversion hors ligne ou authentifiée en mémoire, les vérifications d’identifiant de compte en ligne, la réussite des codes QR, l’authentification à deux facteurs (2FA) et l’expiration, l’annulation des codes périmés, ainsi que l’ isolation des comptes. Les fixtures TData utilisent une implémentation AES-IGE distincte pour le chiffrement.

Chromium a réussi **45 scénarios généraux** et **35 scénarios d’importation de compte/QR/clé d’authentification**, sans qu’aucune erreur JavaScript de page ni aucune requête externe n’ait été constatée. Les nouveaux tests de navigateur couvrent l’ensemble des quatre formats d’entrée, les données TData protégées, les métadonnées API, le rendu des codes QR, l’expiration et les tentatives de réessai, l’authentification à deux facteurs (2FA), le rejet en cas de compte erroné, le verrouillage et l’annulation de l’espace de travail, la mise en page adaptative, ainsi que les réponses de conversion tardives après la sélection d’un fichier plus récent.

Les deux suites de navigateurs ont de nouveau passé les tests avec succès après les modifications apportées à la page de connexion. La configuration en direct ouvre le formulaire de création de compte ; le mode démo ouvre son journal d’exemple. La page « Compte » de la démo affiche les instructions de démarrage en direct et masque les champs de saisie des identifiants. Des vérifications ciblées à 320, 390 et 1 440 pixels ont confirmé que le champ numérique et le bouton principal s’affichent sans défilement, que les champs API sont initialement masqués, et que le contraste du texte reste lisible. Les commandes de capture et de vérification restent masquées après l’ouverture de leurs nouvelles sections extensibles.

Le flux direct de la clé d’authentification a été testé à l’aide d’identifiants synthétiques via les véritables points de terminaison d’importation et d’autorisation. Les vérifications portent sur les clés incomplètes, l’absence de DC, les identifiants utilisateur imprécis, les identités de compte non concordantes, les identifiants API enregistrés, la visibilité de la progression de la requête, l’effacement des secrets et les réponses tardives après des modifications ou des changements de méthode. Les quatre méthodes de connexion ont été vérifiées à 320, 390 et 1 440 pixels. Le sélecteur de fichiers précède les consignes de format, et le bouton « Se connecter » s’adapte à la fenêtre d’affichage initiale de 844 pixels lorsque les paramètres de l’API sont masqués. Aucune autorisation réelle par clé d’authentification n’a été tentée lors de ce test d’acceptation de l’interface utilisateur.

L’actualisation du panneau a été vérifiée à nouveau avec les deux suites de navigateurs : aucune erreur JavaScript ni aucune requête externe n’a été observée. La suite de comptes couvre désormais le collage d’une paire ID API/hachage, le rejet des paires mal formées ou multiples sans remplacement des champs, les instructions relatives aux métadonnées uniquement, ainsi que l’ignorance des réponses d’importation obsolètes après un changement de méthode de connexion ou une modification manuelle des identifiants. Six contrôles ciblés supplémentaires ont été validés pour le guide de configuration, le démarrage/la mise en pause explicites, la récupération en cas de recherche vide, ainsi que la mise en page finale de la connexion et du guide local, et un contraste de texte satisfaisant à 320, 390 et 1 440 pixels. La mise à jour de la connexion directe ajoute une opération unique de demande de numéro de téléphone/code et réutilise la paire API enregistrée de l’espace de travail actuel pour la connexion par numéro de téléphone, code QR et session. La suite Python complète ci-dessus inclut de nouveaux tests de persistance, de rejet des identifiants partiels et d’isolation des espaces de travail. Les vérifications au niveau du navigateur portent sur la saisie directe du numéro de téléphone, la réutilisation des identifiants enregistrés, le routage basé uniquement sur les métadonnées, l’autorisation de fichiers en un seul clic et le rejet des comptes en double. Les formulaires simplifiés « jeton de panneau » et « numéro de téléphone » ont également été vérifiés sans défilement initial aux résolutions de 320, 390 et 1 440 pixels. Un contrôle de compatibilité a confirmé que le formulaire de saisie directe du numéro de téléphone peut utiliser les points de terminaison de configuration/code antérieurs alors qu’un processus plus ancien est encore en cours d’exécution.

Un compte fourni par un utilisateur a été vérifié séparément, en dehors des environnements de test publics. Ses données d’entrée Telethon, Pyrogram et TData ont abouti à la même autorisation ; le fichier JSON associé fournissait les identifiants de l’API. Les quatre fichiers ont été chargés via le panneau 0.6.0 et Telegram a confirmé l’identifiant numérique du compte attendu. Les fichiers sources sont restés inchangés. Aucune source n’a été sélectionnée et la fonction d’observation est restée désactivée. Cela constitue un exemple d’importation/de connexion, et non une collecte, une récupération ou une démonstration de capacité en temps réel.

Telegram a également émis un véritable jeton QR, qui a été annulé sans avoir été scanné. Les processus complets de confirmation par QR et d’authentification à deux facteurs (2FA) ont été testés avec des clients synthétiques ; la confirmation sur mobile via une véritable application Telegram reste une étape d’acceptation distincte. Aucun identifiant de compte réel, aucune information confidentielle ni aucune capture d’écran ne figure dans les fichiers publics.

La mise à jour du lanceur est terminée ; le code source, les métadonnées installées et l’indicateur de disponibilité indiquent la version 0.6.0, avec un code QR 8.2 et un code `pip check` valide. La roue installée a pris en charge le panneau et le guide, a rejeté les requêtes API non authentifiées et a vérifié de manière indépendante les exportations synthétiques directes et en flux de 32 événements. Le guide hors ligne mis à jour a été vérifié à 320, 390 et 1 440 pixels. Les captures d’écran publiques restent synthétiques.

La version source contient 107 fichiers figurant sur la liste blanche. Les liens vers la documentation locale sont fonctionnels. L'exécution via Docker/Caddy, la publication à distance via CI/package, l'environnement d'exécution ARM64, la collecte continue ainsi que la matrice complète d'acceptation de Telegram en temps réel ne font pas l'objet de précisions ici.

## Version 0.5.1

Sous Windows 11 / Python 3.12.10, l’ensemble complet de l’environnement du projet a été validé : **94 tests réussis, 2 ignorés**, en 31,21 secondes, avec l’avertissement Starlette existant. Les éléments ignorés nécessitent des droits POSIX et la création de liens symboliques, qui ne sont pas disponibles sur cet hôte. Le test HTTP de téléchargement a généré un diagnostic du thread de requête ; toutes les assertions ont été validées. Cette exécution ne permet pas d’exclure l’existence de problèmes de transport au niveau de l’hôte.

De nouveaux exercices de couverture de régression ont porté sur les sessions StringSession rejetées, les modifications du code et des comptes 2FA, l’annulation de la recherche d’identité, l’annulation de connexion en attente, ainsi que les mises à jour via des gestionnaires enregistrés sur les clients actifs, rejetés, remplacés et de test. Seul le collecteur actif contribue aux événements ; les identifiants enregistrés et l’historique signé restent intacts. D’autres nouveaux contrôles portent sur la recherche Unicode après la réouverture d’une base de données, l’inclusion des limites de la politique de surveillance dans Coverage, ainsi que les exclusions de paquets provenant de sources publiques.

Le projet `pythonw.exe` a lancé un panneau synthétique isolé, a renvoyé un code HTTP 200 et a conservé les diagnostics de démarrage dans `logs/server.log`. Le journal ne contenait ni le jeton de panneau généré ni les enregistrements d’accès HTTP. Le test n’a mis fin qu’à son propre processus synthétique. Aucune tâche n’a été enregistrée dans le Planificateur de tâches ; la connexion/déconnexion, la mise en veille et la reprise de service restent des critères distincts.

Les tests d’acceptation Chromium ont réussi **45 scénarios**, sans erreur JavaScript sur les pages et sans requête externe observée. De nouveaux contrôles portent sur les dates et heures de la chronologie en 601/768/850 pixels, les brouillons de pièces jointes lors de l’actualisation du statut, les modifications récentes effectuées lors de l’enregistrement, les résultats de vérification effacés lors du changement de compte, les réponses de vérification tardives après avoir quitté puis réintégré l’application, ainsi que les limites de vérification explicites à l’arrivée de nouveaux événements. L’espacement entre l’icône de recherche et le texte a également été corrigé et la suite de navigateurs a été relancée.

L'exécution dans le navigateur a utilisé le runtime épinglé dans `.venv` et la version existante fournie par le système de Playwright 1.62.0/Chromium, ajoutée après l'environnement du projet dans le chemin d'importation. Une installation facultative de dépendances de développement a été interrompue en raison d'un téléchargement lent de Playwright ; aucune nouvelle version de l'outil de navigateur n'a été validée. Un cycle normal « `python start.py --setup-only` » a permis de finaliser la mise à niveau de l’application. Le code source, les métadonnées installées et le marqueur du lanceur indiquent la version 0.5.1 ; « `pip check` » a été validé. Les contrôles de préparation ont été validés sur un chemin d’accès neuf et inutilisé, tout en conservant l’avertissement attendu concernant la clé du coffre-fort local.

Le paquet « wheel » de la version 0.5.1 a été installé séparément et soumis à des tests de fonctionnement : tous les éléments du panneau et du guide ont été fournis, l’accès non authentifié à l’API a été refusé, et les fichiers ZIP de preuves, tant directs que diffusés en continu, contenant 32 événements ont passé avec succès une vérification indépendante. Les fichiers de l’application contenus dans le paquet installé ont été comparés au code source. L’archive publique du code source utilise une liste blanche explicite des types de fichiers et refuse les fichiers source liés ; les éléments d’exécution placés à l’intérieur des répertoires source sont exclus des tests de régression.

Au cours de l’exécution de la correction du code, la sélection de sources publiques et l’ensemble de candidats Git contenaient 86 fichiers, sans inclure les répertoires de données d’exécution. Une analyse à la recherche de modèles reconnaissables de clés privées, de jetons GitHub, de jetons de bot Telegram et de StringSession n’a révélé aucune correspondance. Il s’agit d’une vérification de modèles limitée, et non d’un audit exhaustif des secrets. Les sondes de règles d’ignorance couvrent douze artefacts courants liés aux comptes, aux données et aux exportations. Les fichiers YAML relatifs au workflow, aux tickets et à Compose, ainsi que le script de tâche Windows, ont été analysés avec succès. Les liens vers la documentation locale sont fonctionnels.

Les sept constatations issues de l’examen du 27 octobre sont toutes prises en compte. L’exécution du workflow sur GitHub, le runtime sous Linux/macOS/Docker, l’utilisation de Telegram en conditions réelles, l’interopérabilité avec des proxys externes/TSA ainsi que la qualification en charge soutenue ne font pas partie de cette exécution locale. Aucune publication de dépôt, aucun enregistrement de service ni aucune collecte de comptes réels n’ont été effectués.

### Mise à jour de la documentation en anglais

Le fichier README, la référence relative aux comptes et aux sessions, le workflow de collecte et le guide fourni décrivent désormais les entrées prises en charge, le comportement de l’espace de travail, les politiques relatives aux événements et les formats d’exportation en anglais. Les trois captures d’écran publiques ont été mises à jour à l’aide de données synthétiques. À ce stade, la sélection des ressources publiques comprenait 88 fichiers, dont les deux nouveaux guides. Les 131 liens locaux répartis dans 23 documents Markdown sont tous fonctionnels.

Après les modifications apportées à l’interface et au guide, les tests d’acceptation Chromium ont de nouveau réussi les 45 scénarios, sans qu’aucune erreur JavaScript de page ni aucune requête externe n’ait été constatée. La suite complète de tests Python n’a pas été réexécutée pour cette mise à jour de la documentation et de la présentation ; le résultat de 94 tests réussis ci-dessus correspond à l’exécution précédente suite à la correction du code.

La roue reconstruite a été installée sur une nouvelle cible isolée. Ses composants de panneau et de guidage ont fonctionné correctement, les accès API non authentifiés ont été rejetés, et les exportations, tant directes qu’en continu, ont passé avec succès une vérification indépendante portant sur 32 événements synthétiques.

### Mise à jour concernant l'installation et le déploiement

Les vérifications ciblées de l’installateur, du packaging et de l’état de préparation ont réussi **14 tests**, avec un test ignoré en raison de l’impossibilité de créer un lien symbolique. Les vérifications du wrapper natif couvrent les chemins d’accès contenant des espaces, le transfert d’arguments, les modes de configuration/démonstration et la propagation d’un code de sortie différent de zéro. Les vérifications Git Bash testent l’assistant de shell Docker avec un démon simulé, notamment en cas d’absence de Docker, d’absence de Compose, d’échec de l’attente de santé et de réussite du démarrage sur un port alternatif. Ces vérifications simulées n’établissent pas la compatibilité d’exécution de Docker.

Une copie complète issue de sources publiques a été installée dans un nouveau répertoire Windows dont le chemin d’accès contient des espaces. `scripts\Setup.cmd` a créé un nouvel environnement et installé le runtime épinglé ; `Start.cmd --check --json` a signalé qu’il était prêt sans créer son répertoire de données cible. `pip check` a réussi le test. La version reconstruite a également réussi la vérification du paquet installé, y compris les exportations directes et en flux de 32 événements.

Syntaxe Shell et analyse de cinq fichiers YAML de workflow/Compose. Les configurations Compose du code source et des images concordent en ce qui concerne les paramètres de stockage et d’exécution. À ce stade, les 139 liens locaux répartis dans 23 documents Markdown ont été résolus. La sélection des sources publiques contient 99 fichiers.

Les définitions CI effectuent désormais une nouvelle configuration native sous Windows/Linux/macOS, ainsi que la gestion de l'intégrité, du contrôle d'accès et de la persistance de Compose lors de la recréation des conteneurs, et la configuration de Caddy. Le workflow de publication subordonne la mise en ligne à la réussite de ces vérifications et ajoute un test de fonctionnement sur ARM64 émulé. Docker n’est pas disponible sur cet hôte : l’exécution réelle de Compose/Caddy, la délivrance de certificats, l’exécution ARM64 et la publication à distance du workflow/paquet restent sans restriction en local. Le code de l’application et de l’interface utilisateur n’a pas été modifié par cette mise à jour ; les résultats complets antérieurs en Python et sur navigateur n’ont pas été réexécutés.

## Version 0.5.0

La suite complète de tests d’exécution épinglés a été réussie : **81 tests réussis, 1 test ignoré**, en 22,00 secondes, avec l’avertissement Starlette existant. La vérification des droits d’accès POSIX est ignorée sous Windows. Les nouveaux tests de gestionnaires envoient des messages, des modifications, des suppressions avec ou sans portée, des réactions, des mises à jour des participants et des messages du service d’adhésion selon différentes politiques. Les catégories désactivées ne génèrent aucune observation en temps réel correspondante ; les diagnostics de couverture et les instantanés explicites restent disponibles. Les tests vérifient la persistance de la politique, la séparation des espaces de travail, les enregistrements d’audit signés avant/après, le comportement en cas de politique inchangée, la validation stricte et l’inclusion dans la réception du processus suivant.

Les tests d’accès à la démo vérifient que ses capacités diffèrent de celles du jeton de panneau configuré : elle ne peut pas autoriser un espace de travail actif, ne peut pas modifier les paramètres de collecte et n’est pas émise ni acceptée pour les requêtes à distance, transférées, inter-origines ou dont l’hôte est invalide. L’ouverture d’une démo enregistrée sans l’indicateur de démo explicite n’active pas l’accès automatique.

Les tests d’acceptation Chromium ont réussi **39 scénarios**, notamment l’accès à la démo locale sans saisie de jeton, les préréglages de surveillance, la transition de la sélection de la source vers la politique, l’indépendance par compte, ainsi que les vérifications de mise en page (bureau/320/390 pixels) et de contraste du texte. Aucune erreur JavaScript n’a été détectée sur la page. Les requêtes injectées par AdGuard sur l’hôte restent présentes dans le journal. Le test HTTP de téléchargement a enregistré une réinitialisation de la connexion après la fermeture de la connexion par un client ; les assertions ont néanmoins été validées. Il ne s’agit pas d’un résultat issu d’un service en production.

Le lanceur standard a mis à jour l’environnement isolé vers la version 0.5.0 ; les versions source et installée correspondent et la vérification pip a réussi. Le chiffrement existant du coffre-fort de secrets, le refus en cas de clé erronée ou manquante ainsi que les contrôles de falsification des signatures et des médias ont été validés par la suite complète de tests. Aucun nouveau chiffrement au niveau de l’application du contenu des messages ou des pièces jointes n’est revendiqué.

La démo locale est redémarrée afin de rendre l’interface utilisateur mise à jour disponible. Les enregistrements synthétiques existants sont conservés ; l’arrêt de l’ancien processus de démo en arrière-plan crée une limite hors ligne lors du prochain démarrage. Aucune véritable session Telegram n’est utilisée pour ces vérifications.

Le panneau en cours d’exécution sur localhost:8787 affichait la version 0.5.0, un accès automatique à la démo, les cinq commandes de surveillance et 33 événements synthétiques conservés dans le journal. Le fichier « wheel » 0.5.0 installé séparément a fourni tous les ressources du panneau et du guide, a rejeté tout accès API non authentifié et a généré un fichier ZIP vérifié contenant 32 événements, à la fois directement et via l’assistant de téléchargement en continu . Les versions des paquets d’exécution restent fixées telles qu’enregistrées pour la version 0.4.

## Version 0.4.0

La suite complète de tests « pinned-runtime » a été validée : **78 tests réussis, 1 test ignoré**, en 19,77 secondes. Le test ignoré nécessite des droits d’accès POSIX ; l’avertissement de dépréciation du Starlette TestClient en amont demeure. De nouveaux tests couvrent le téléchargement en continu et le routage vers l’espace de travail, les en-têtes d’autorisation, le refus de réécriture, les redirections, les réponses tronquées, les limites de taille annoncées et réelles, les lectures bornées, le nettoyage, les systèmes de fichiers sans liens physiques, les échecs de préparation et les modes de lancement qui ne doivent pas installer de paquets. Les tests d’exportation confirment l’existence de fichiers temporaires locaux à l’espace de travail et le nettoyage sélectif des fichiers orphelins.

Les tests d'acceptation Chromium ont réussi les 36 scénarios répertoriés sans aucune erreur JavaScript sur la page. Il simule une connexion par téléphone/code/authentification à deux facteurs (2FA), des sessions converties, deux espaces de travail et des itinéraires/états distincts, des observations, des signatures, des points de contrôle et des demandes d'horodatage, ainsi que :

- Mises en page pour ordinateur de bureau et pour 320/390 pixels, pas de débordement horizontal, navigation visible, et le premier champ de connexion dans la zone d'affichage initiale de 844 pixels.
- Contraste du texte sur fond uni conforme aux seuils WCAG AA. Les contrôles désactivés, l’opacité et les arrière-plans composés d’images ou de dégradés sont exclus ; il ne s’agit pas d’un audit WCAG complet.
- Une véritable réponse d’exportation locale générée via un simulateur de sélecteur de fichiers OS/disque accessible en écriture, suivie d’une vérification indépendante du fichier ZIP ; l’annulation n’entraîne l’envoi d’aucune demande d’exportation.
- Un échec d’écriture interrompt l’opération vers la destination ; le mécanisme de secours de 128 Mio rejette une réponse annoncée trop volumineuse sans allouer de charge utile correspondante.
- Le guide local en anglais pour les ordinateurs de bureau et les deux formats d'écran étroits.

La boîte de dialogue d’enregistrement sur le système d’exploitation et les écritures réelles de plusieurs gigaoctets dans le navigateur n’ont pas été automatisées ni validées. Les tests de téléchargement en Python utilisent des blocs délimités et des dispositifs de bouclage. L’acceptation complète du déploiement avec une instance réelle de Telegram reste distincte.

Le programme d'installation standard a mis à jour `.venv` vers la version 0.4.0. Les métadonnées source et celles de l'installation concordent ; `pip check` a réussi le test. `python start.py --check --json` s'est déclaré prêt sur un nouveau chemin synthétique sans créer le répertoire de données. Son avertissement concernant le stockage des clés locales reste à juste titre affiché : les journaux et les médias ne sont pas chiffrés par l'application.

Le fichier « wheel » de la version 0.4.0 a été compilé et installé dans un répertoire distinct. Les 23 fichiers de l’application correspondent à l’octet près à la source. Le paquet installé a fourni le panneau de configuration et les guides/ressources en anglais, a rejeté tout accès non authentifié à l’API et a exporté un fichier ZIP synthétique contenant 32 événements qui a passé la vérification avec succès. Sa commande de téléchargement en continu a également récupéré un fichier ZIP vérifié de manière indépendante à partir de l’application installée et en cours d’exécution.

La documentation publique et le guide local sont en anglais ; les liens vers la documentation locale fonctionnent. PowerShell a analysé le modèle de tâche Windows et Python a analysé le fichier plist de macOS. Il s'agit de vérifications syntaxiques, et non de l'exécution d'un service. Aucune tâche/aucun service n'a été enregistré. La configuration CI inclut désormais des contrôles de disponibilité, mais la CI à distance ne s'est pas exécutée ici.

L'exécution 0.4 dans le navigateur a de nouveau détecté une injection par l'hôte AdGuard ainsi qu'une erreur OSError 10022 liée au nettoyage des sockets asyncio sous Windows. Les assertions du navigateur ont été validées ; ces observations environnementales sont conservées plutôt que considérées comme un comportement fixe de l'application. Les premières tentatives de sandbox OpenSSL/navigateur/pip ont échoué ; les exécutions de qualification réussies ont utilisé une exécution approuvée en dehors de la sandbox.

## Version 0.3.1 : corrections visant à améliorer la fiabilité

Les vérifications concernant le lanceur, le stockage des preuves et l’API ont été validées : **31 réussies, 1 ignorée**, un avertissement Starlette en amont. La vérification ignorée porte sur les droits d’accès POSIX aux répertoires et ne peut pas établir ces droits sur cet hôte Windows. Le test « old-Python » simule la limite entre les versions et les importations ; aucun interpréteur Python 3.10 n’était installé ni certifié. La suite de tests 0.3, qui avait précédemment réussi, est consignée ci-dessous ; la suite complète et les scénarios de navigateur n’ont pas été réexécutés pour ces modifications ciblées.

Le lanceur standard a mis à niveau l’environnement local vers la version 0.3.1 ; les métadonnées sources et celles de l’installation concordent, et la vérification pip a abouti. Une roue 0.3.1 installée séparément a fourni le panneau et les ressources, a rejeté tout accès non authentifié à l’API et a généré une exportation synthétique vérifiée de 32 événements. Le fichier YAML du workflow a été analysé, mais la nouvelle vérification du runtime du conteneur n’a pas été exécutée : aucun runtime local Docker/Podman/Linux utilisable n’était disponible.

Consultez [les conclusions relatives à l’état de préparation](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) pour connaître les lacunes restantes en matière d’ergonomie, de service en production et de plateforme. Ce correctif ne prend pas en charge de nouveaux systèmes d’exploitation.

## Version 0.3.0

La suite complète « pinned-runtime » a réussi : **61 tests**, avec un seul avertissement de dépréciation en amont concernant Starlette TestClient. Les métadonnées d’exécution indiquent TgWitness 0.3.0 et python-socks 2.8.2 ; la vérification pip a réussi. Le test d’acceptation du navigateur a réussi sans aucune erreur JavaScript sur la page.

La version 0.3.0 de wheel a été compilée et installée dans un répertoire de paquets distinct. Elle a fourni le panneau de contrôle et les ressources, a rejeté une requête API non authentifiée et a exporté un journal synthétique de 32 événements qui a passé avec succès une vérification indépendante. Les liens de la documentation locale sont opérationnels. Après la correction de normalisation de la clé brute par MTProxy, les neuf tests de connexion et de sécurité ont tous été réexécutés avec succès.

Les nouvelles fonctionnalités incluent :

- Identifiant/mot de passe SOCKS5 et HTTP CONNECT via de véritables serveurs de test en boucle fermée ; un proxy configuré mais hors service échoue plutôt que de se rabattre sur la destination.
- Validation des proxys, sélection du protocole de transport MTProxy, rejet des faux secrets TLS, persistance, isolation de l’espace de travail, rejet des modifications pendant l’observation et exclusion des secrets du statut de l’API et des événements signés.
- Conversion en lecture seule des schémas SQLite synthétiques 7 et 8 de Telethon ; hachage de la source inchangé ; rejet des autres formats, des vues SQL et d’un fichier WAL en attente. source hash; rejection of other formats, SQL views, and an outstanding WAL file.
- Clé principale externe du coffre-fort : différentes clés d’espace de travail dérivées, réouverture réussie, rejet en cas de clé erronée ou manquante, et aucune migration implicite des coffres-forts locaux existants.
- Paramètres de proxy du navigateur, effacement des identifiants, divulgation des mesures de protection du stockage, page de connexion mobile, autorisation des fichiers de session convertis, itinéraires distincts, et tous les scénarios de collecte/exportation précédemment abordés à l’aide d’un faux client Telegram.

Au cours du développement, un test de bouclage a attendu indéfiniment l’arrêt du pair ; un autre test a observé une réinitialisation de la connexion Windows après la poignée de main. Le dispositif limite désormais l’intégralité de l’échange et traite les événements EOF/réinitialisation survenant après une poignée de main achevée comme une fermeture de connexion. Les assertions relatives à la négociation de connexion et à l’authentification restent obligatoires. Cela n’exclut pas les véritables fournisseurs de proxy et n’implique pas non plus un défaut fixe du transport Telegram.

La remarque concernant l’observation de la requête AdGuard décrite ci-dessous reste valable. Aucun véritable compte Telegram, aucun proxy SOCKS/HTTP externe, ni aucun serveur MTProxy en production n’ont été utilisés. MTProxy est une solution expérimentale et seules ses options sélectionnées ainsi que la validation des secrets ont été vérifiées, et non son interopérabilité en conditions réelles. De nouvelles commandes de conversion de clés externes et de sessions ont été testées uniquement avec des secrets synthétiques. Linux/macOS/Docker ne font pas l’objet d’une validation dans le cadre de cette analyse.

La mesure de débit de la version 0.2 ci-dessous n’a pas été reproduite et ne doit pas être présentée comme une nouvelle référence en matière de gestion de comptes multiples et de proxys pour la version 0.3.

## Version de référence 0.2.0

Testé sous Windows avec Python 3.12.10. Aucun compte Telegram réel n’a été connecté.

| Vérifier | Résultat |
| --- | --- |
| Suite Python | 52 tests réussis dans l’environnement de développement et 52 réussis avec l’environnement d’exécution épinglé ; un avertissement de dépréciation de Starlette TestClient en amont lors de chaque exécution |
| Syntaxe JavaScript | Réalisé avec Node.js |
| Acceptation de Chromium | Validé ; aucune erreur JavaScript sur la page |
| Mise en page pour ordinateur de bureau et mobile | Vérifié aux résolutions 1 440 × 1 060 et 390 × 844 ; aucun débordement horizontal du document |
| Contenu des messages au format HTML | Affiché sous forme de texte ; le script injecté ne s'est pas exécuté |
| Exemple de flux de compte | Identifiants API → téléphone → code → authentification à deux facteurs (2FA) → sélectionner un groupe → démarrer → capture d'écran → mettre en pause → recharger |
| Preuves dans le navigateur | Comparaison des modifications, contenu antérieur après suppression, filtres, téléchargement au format ZIP, point de contrôle, accusé de réception signé du processus, téléchargement de la requête RFC 3161 et liaison au point de contrôle |
| Gestion de plusieurs comptes | Séparation des journaux, des clés, des sources et des états en temps réel ; le changement de navigateur laisse l’autre collecteur en fonctionnement ; les espaces de travail se rouvrent après un redémarrage ; les comptes en double et les réaffectations de compte sont rejetés |
| Défaillances cryptographiques | Changement de champs signés, ajout de champs non signés, clé incorrecte, élément d’archive corrompu, médias modifiés/manquants, troncature détectée par le point de contrôle et rejetée |
| Stockage | Les ajouts simultanés sont vérifiés ; les mises à jour ou suppressions déclenchent un rejet ; au démarrage, le système refuse un journal modifié sans ajout et libère son verrou. |
| Durabilité des supports | Écritures atomiques des messages/tâches ; récupération après redémarrage ; conservation des descripteurs de la version d’origine ; rejet de la substitution de file d’attente et de la corruption des fichiers existants ; persistance de FloodWait ; isolation des défaillances à la source |
| Diffusion en continu | Un préfixe stable est exporté à mesure que de nouveaux enregistrements s’ajoutent ; un point de contrôle conservé détecte tout journal tronqué ; l’exportation ne reflète pas l’intégralité du flux d’événements |
| RFC 3161 | OpenSSL 3.5.9 lit les requêtes générées ; les réponses CA/TSA synthétiques générées localement sont acceptées ; les données modifiées, les nonces et les CA erronées sont rejetées ; l’environnement CA ambiant ne remplace pas la confiance explicite. |
| Configuration locale | start.py --setup-only a mis à jour l'environnement .venv isolé vers la version 0.2.0 ; les métadonnées de la source et celles installées concordent ; la vérification pip a réussi |
| Wheel | Version 0.2.0 compilée et installée séparément dans le répertoire « test-results » ; mise à disposition des panneaux et des ressources, rejet des appels API non authentifiés, exportation et vérification d’une archive synthétique contenant 32 événements |

Les tests source ont utilisé FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1 et Playwright 1.62.0. L’environnement d’exécution verrouillé utilise FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0 et cryptography 50.0.2. Le fichier deploy/constraints.txt répertorie les versions fixes du runtime ; les fichiers deploy/requirements.lock et deploy/build.lock contiennent le SHA-256 de chaque fichier de paquet, et les serveurs Docker et à haute sécurité effectuent les installations uniquement à partir de ces fichiers (pip --require-hashes). Aucun de ces éléments ne constitue une preuve de compatibilité sur toutes les plateformes de CI configurées. La CI à distance n’a pas été exécutée.

## Mesure synthétique des capacités locales

Commande : `python tools/check_capacity.py --events 10000 --chats 100`

| Indicateurs | Constaté |
| --- | --- |
| Données d'entrée | 10 000 événements de messages synthétiques provenant de 100 sources synthétiques sélectionnées |
| Texte du message | 400 caractères ; pas de médias ni de réseau |
| Ingestion | 53,273 secondes ; 187,7 événements/seconde |
| Latence du gestionnaire | p50 4,162 ms ; p95 7,784 ms ; maximum 129,118 ms |
| Exportation au format ZIP | 19,868 secondes avec tracemalloc activé |
| Pics d'allocations d'exportation Python tracées | 0,51 Mio ; ne traite pas les flux RSS |
| Taille du fichier ZIP | 4 610 962 octets |
| Vérification indépendante | Les 10 000 événements ont tous été vérifiés |

Cette mesure porte sur le chemin d'enregistrement/d'exportation séquentiel local sur cet hôte Windows. Elle ne mesure pas la transmission MTProto, les comptes simultanés, la limitation de débit imposée par Telegram, les fichiers multimédias, une charge de travail de longue durée, ni un nombre garanti de conversations réelles. La mesure est antérieure à la mise en place définitive de l’outil d’horodatage hors ligne, qui ne modifie pas le chemin des messages mesurés.

## Observations environnementales

Les restrictions du bac à sable Windows ont bloqué les répertoires temporaires par défaut de pytest/pip ainsi que le sous-processus Playwright. Pytest a utilisé un nouveau répertoire temporaire au sein du projet ; les processus d’installation et du navigateur ont nécessité une exécution autorisée en dehors du bac à sable.

AdGuard a injecté dans le navigateur des requêtes vers local.adguard.org. L'historique du navigateur conserve ces requêtes. Ce test **ne** prouve **pas** l'absence totale de requêtes sortantes dans un environnement de navigation non modifié ; le code source de l'application lui-même ne contient aucune requête vers des ressources externes, des CDN ou des outils d'analyse. Les paramètres d'AdGuard n'ont pas été modifiés.

La dernière exécution du navigateur a également enregistré une erreur OSError 10022 liée au nettoyage des sockets asyncio sous Windows. Toutes les assertions du navigateur ont été validées et aucune erreur JavaScript n’est survenue sur les pages. Sa cause n’a pas été établie et cette exécution ne prouve pas l’absence de problèmes de transport au niveau de l’hôte.

Le premier test HTTP sur le paquet installé, utilisant les requêtes de fermeture de connexion d’urllib, a rencontré des réinitialisations de connexion, tant à l’intérieur qu’à l’extérieur du bac à sable et avec les deux ensembles de dépendances. Le test final a utilisé des connexions persistantes HTTP/1.1 standard via http.client et a réussi. Les requêtes du navigateur ont également réussi le test. L’origine exacte des réinitialisations n’a pas été établie ; elles n’ont pas été qualifiées de défaut fixe de l’application.

## Autres précisions

Le journal en temps réel conservé consigne les collectes effectives, les modifications, les notifications de suppression, les pièces jointes, les vérifications croisées et la gestion des limites de débit. Il ne rend pas compte de manière exhaustive des envois ni ne fournit une matrice contrôlée de visibilité des rôles, des acteurs intervenant dans les réactions, des délais prolongés de « FloodWait », des suspensions de compte et de la reprise après interruption du réseau ou des processus. L’émission de jetons QR reste distincte de la confirmation QR mobile finalisée.

La compilation/l’exécution sous Docker, l’installation sous Linux/macOS, la gestion d’une charge élevée en continu, l’audit de sécurité indépendant, une réponse TSA véritablement indépendante, la validation de la révocation/archivage des certificats et la certification judiciaire ne font pas partie de la qualification enregistrée. La sauvegarde de l’état MTProto et la synchronisation sont implémentées ; la relecture atomique et durable n’est pas encore établie. La collecte des journaux d’administration, les listes de réacteurs supplémentaires et l’interrogation prioritaire à intervalle court restent des fonctionnalités distinctes. Veuillez consulter [l’acceptation en direct](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) pour la matrice de qualification contrôlée.

Les reçus locaux détaillés et les captures d'écran se trouvent dans le répertoire test-results/ (ignoré par Git). La capture d'écran publique située dans le répertoire docs/assets/ ne contient que des données de démonstration fictives.

## Préparation du site web public et de la publication · 27 octobre 2026

La présentation distincte « `website/` » et la version Pages ont été ajoutées après les vérifications mentionnées ci-dessus. Aucune configuration de compte actif ni aucune logique de collecte n’a été modifiée.

- La suite d’applications existante a été validée : 138 tests réussis, 1 test ignoré (exclusivement POSIX) et un avertissement de dépréciation en amont concernant Starlette/httpx. Les 11 tests de compilation du site ajoutés ont été validés de manière indépendante, y compris le rejet des sorties inattendues et le rejet des entrées liées.
- Les deux scripts de navigateur de l’application ont été testés avec succès à l’aide de project-venv Playwright et du shell « headless » Chromium 156. Aucune erreur JavaScript de page ni aucune requête externe n’a été enregistrée. Tous les scénarios de compte ont utilisé un transport fictif et des données fictives.
- `tools/check_site.py` a été validé aux largeurs 320, 390, 768, 1024 et 1440, avec un sous-chemin d'URL du projet, les onglets du clavier, l'accès au presse-papiers autorisé ou refusé, les animations réduites et JavaScript désactivé. Aucune requête d'éléments ou requête externe n'a échoué.
- `tools/build_site.py` a généré 10 fichiers publics figurant sur la liste blanche, pour un total d'environ 460 Ko. Les captures d'écran du navigateur et un reçu se trouvent dans le fichier `test-results/site/`, qui est ignoré.
- La roue a été générée avec succès après l’installation des outils setuptools/wheel destinés uniquement à la compilation dans l’environnement du projet. Son installation sur une cible isolée et l’exécution de la commande « `tools/check_install.py` » ont donné des résultats satisfaisants : ressources statiques, contrôle d’accès, une exportation synthétique signée de 32 événements et un téléchargement en continu vérifié de manière indépendante.
- `pip check` a été validé. Une analyse par motifs des candidats publics sélectionnés via Git n’a révélé aucun bloc de clé privée identifiable, aucun jeton GitHub/bot/AWS, aucune affectation littérale de secret de grande longueur, ni aucun marqueur de conflit de fusion. Cela ne prouve pas pour autant que tous les formats de secrets possibles soient absents. Les sondes de données d’exécution, de session et de clé ont été ignorées par Git.
- L’authentification GitHub CLI n’était pas valide ; aucun serveur distant n’était configuré et aucun commit initial n’existait. Aucun push, workflow hébergé, déploiement Pages ou publication n’a été effectué. Docker et la qualification en temps réel de Telegram/de la plateforme ne sont pas pris en compte dans cette vérification.

Sur cet hôte, le verrouillage du téléchargement de Playwright a échoué sur le système de fichiers de l'espace de travail E:. L'installation de Chromium sous `%LOCALAPPDATA%/tgwitness-playwright` et l'utilisation de ce même `PLAYWRIGHT_BROWSERS_PATH` pour les vérifications ont abouti. Il s'agit d'une solution de contournement au niveau de l'environnement, et non d'une modification des dépendances d'exécution de l'application.

## Documentation interactive et métadonnées du site web · 29 octobre 2026

Le site public comprend 12 pages HTML en anglais : une page d’accueil, un index des guides et dix guides. L’artefact contient 28 fichiers de présentation explicitement répertoriés, d’un poids d’environ 1,85 Mo, et aucune donnée de collecte. Le site web public est en anglais ; les traductions de l’application et les guides traduits du référentiel sont fournis séparément.

- Tests du site, de la publication source et des limites de la version : **18 réussis, 2 ignorés**. Les tests ignorés concernent la création de liens symboliques sur ce système de fichiers Windows. Les tests vérifient l'unicité des métadonnées des pages, les pages publiques en anglais uniquement, les URL canoniques, toutes les entrées du plan du site, les ressources et ancres locales, la navigation structurée et l'exclusion des fichiers privés.
- Les tests « `tools/check_site.py` » et « `tools/check_docs_site.py` » ont tous deux réussi dans Chromium à des résolutions de 320, 390, 768, 1 024 et 1 440 pixels sous un sous-chemin d’URL du projet. Les vérifications du guide couvrent l’ensemble des 11 pages de documentation, la recherche et la navigation au clavier, la gestion du presse-papiers (succès/échec) ainsi que la lisibilité du contenu sans JavaScript.
- Cinq exemples interactifs validés : lecture/avancement pas à pas/pause/réinitialisation des messages avec mouvement réduit et suspension hors écran ; chaînes de hachage originales/modifiées/reconstituées/tronquées ; décisions de témoin concernant l’acceptation/la restauration/la bifurcation/l’absence de réponse ; et scénarios de livraison complète/retardée/manquante ; ainsi qu’une carte d’enquête reliant des observations fictives issues de discussions croisées par identifiant d’expéditeur, destination et hachage de pièce jointe . Les contrôles d’enquête ont passé avec succès les tests de navigation au clavier et de solution de secours sans JavaScript . Les résultats SHA-256 du navigateur ont été comparés de manière indépendante avec le `hashlib` de Python et le JSON canonique. L’exemple de hachage a également conservé sa solution de secours lisible lorsque Web Crypto n’était pas disponible.
- Les taux de livraison et les marqueurs du graphique ont été alignés sur le tableau accessible. Les libellés de l’axe « Mobile » ont été agrandis après vérification visuelle. Chaque exemple est identifié comme « illustratif » ou « synthétique », et aucun exemple de navigateur ne contacte Telegram.
- Aucune requête externe, aucune requête HTTP ayant échoué ni aucune erreur JavaScript n’ont été enregistrées. Les captures d’écran et les reçus pour ordinateur de bureau/mobile se trouvent sous les répertoires ignorés `test-results/site/` et `test-results/docs-site/`. L’index de la documentation, les exemples de messages/hachages, la mise en page de Witness, le tableau de livraison et la carte d’enquête ont été examinés aux tailles « ordinateur de bureau » et « mobile ».
- La vérification des publications a été validée pour 282 fichiers de sources publiques et 1 426 liens vers la documentation locale. Ruff a validé les outils et tests Python modifiés du site.
- `docs/HOW-IT-WORKS.md` fournit un complément Markdown pour GitHub avec des diagrammes Mermaid et des formules. `docs/INVESTIGATION.md` couvre l’ensemble du compte, l’acquisition de l’historique par conversation, les profils des utilisateurs, les références entre conversations, les chronologies et le transfert vérifié d’un dossier. Ses étapes et ses limites ont été vérifiées par rapport au code actuel concernant le champ d’application, la collecte, le dossier, l’exportation, le vérificateur et le panneau. Le rendu hébergé sur GitHub n’a pas été vérifié.

Il s’agit d’une vérification locale du site web et de la documentation. Elle n’ajoute pas de validation en temps réel de Telegram ni ne confirme le déploiement de Pages hébergées, la réussite d’une infrastructure de confiance (CI) à distance ou l’indexation par les moteurs de recherche. Veuillez consulter [la procédure de publication](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) et [les notes relatives aux métadonnées du site web](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md).
