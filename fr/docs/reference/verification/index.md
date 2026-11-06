# Ce qui a été testé

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/

Le test Telegram en direct, les vérifications automatisées, les vérifications au niveau du navigateur et ce qui reste à vérifier.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | Résultat | Portée |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | Enregistre | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| Vérifier | Résultat | Qualification |
| --- | --- | --- |
| Core pytest | 1,461 passed | 37 platform skips |
| Browser / browser UX / evidence / site | 102 / 66 / 15 / 9 passed | These programs overlap other tests; counts are not additive |
| Capture addon | 124 passed | Three Official Web checks blocked by the required Chromium sandbox |
| API authorization | 269 routes; 538 requests passed | Missing credentials and revoked access |
| Retained archives | 48 of 48 verified | 3,598,381 records; pinned workspace keys |
| Live fleet read checks | 24 of 40 profiles passed | 16 WARP routes failed qualification; those profiles were not connected |

The [signed report](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) records all open findings, including three defects in an unpublished secret-chat snapshot absent from the audited main build. The earlier [public-history qualification](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) used a different revision and workload; its rates must not be combined with this comparison.

Verify the original report using the [pinned key and verifier](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Its signature protects the operator's report from alteration. It is not independent attestation, proof of Telegram authorship or GDPR certification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## Déploiement en production sur Phala Cloud · 4 novembre 2026

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| Configuration | Recorded value |
| --- | --- |
| Fournisseur | Phala Cloud · `tdx.small` · US-WEST-1 |
| Déploiement | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

Les deux premiers déploiements ont révélé cinq différences par rapport au Phala Cloud simulé. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) reproduit désormais chacune d’entre elles et échoue sans sa correction :

| Sur Phala Cloud | Avant la correction | Correction |
| --- | --- | --- |
| `compose_file.name` est obligatoire | Code HTTP 422, rien n’a été créé | La configuration Docker Compose porte le nom de la CVM |
| À moins qu’on ne lui en fournisse une vide, Phala ajoute son propre script de pré-lancement à l’app-compose mesuré (v0.0.20 : identifiant Docker, `docker compose pull`, mot de passe root, clés SSH issues de `user_config`) | Échec de `tdx_compose` : code ne figurant pas dans la configuration Docker Compose publiée | app-compose définit `pre_launch_script` sur `""` ; Phala ne le prend alors pas en compte |
| En l’absence de `image`, Phala choisit `dstack-dev-0.5.12`, la version de développement, avec l’accès SSH activé | `server_state` échoue. Seul l’enregistrement d’attestation matérielle a été validé pour cette image ; seuls l’enregistrement du fournisseur et `tdx_os` l’indiquent. | Le déploiement requiert la version de production de la dernière version de Phala, `dstack-0.5.12` |
| Lorsque la passerelle dstack est désactivée, les détails du CVM n’affichent jamais le code d’erreur `instance_id` | Le déploiement attend 30 minutes puis échoue | L’identifiant de l’instance est extrait de l’état du CVM |
| Les redémarrages, arrêts et démarrages sont des opérations CVM, et non des révisions d’application | `provider_actions` n’a pas répertorié les redémarrages | Les opérations de lecture sont également prises en compte |

**Deployment 3 · attestation, access checks and restart evidence**

- La CVM a exécuté `dstack-0.5.12` avec l’accès SSH désactivé. Le collecteur a publié son adresse signée environ 1,5 minute après sa création. Le déploiement a ensuite validé `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, enregistrement d’attestation matérielle v4, FMSPC `20a06f000000`, pas en mode débogage, non migrable, prenant en charge les données de vérification cryptographique récupérées auprès d’Intel), `tdx_compose_hash`, `tdx_compose` (octet par octet) et `tdx_identity` (clés KMS).
- Le panneau accessible à l’adresse trycloudflare.com a renvoyé un code d’erreur 401 en l’absence de jeton ou avec un jeton incorrect, et un code 200 avec le jeton du panneau.
- `verify` avec `--source` défini sur l’archive GitHub du commit et l’empreinte transmise séparément : serveur, `server_state`, pare-feu (pas de passerelle, pas de point de terminaison public), journal du fournisseur, relevé, empreinte, hachage source, démarrage et les cinq vérifications `tdx_*` ont été validées. Cloudflare et `tdx_os` n’étaient pas disponibles ; le résultat était donc INCOMPLET.
- Deux redémarrages via l’API de Phala : à chaque fois, la CVM était de nouveau opérationnelle en moins de deux minutes avec la même clé de collecteur, une nouvelle adresse signée et l’ancienne répondant par un code 530. `verify` a signalé le nouveau démarrage et les deux redémarrages comme REVIEW. Avec `--evidence`, il a confirmé les signatures du journal et les trois démarrages, chacun disposant de son propre enregistrement d’attestation matérielle Intel TDX provenant du même CVM.
- La commande `destroy` n’a supprimé que cette CVM. L’espace de travail s’est alors retrouvé vide, et l’adresse du panneau a cessé de répondre.
- La vérification du prix dans l’assistant du panneau indiquait `tdx.small` à 0,058 $ de l’heure. Une clé erronée a généré un simple message « la clé API n’a pas été acceptée ».

**Follow-up fixes · signed address discovery and OS measurements**

- En l’absence de clé d’adresse, `verify` a suivi la dernière publication bien formée relative au sujet de l’adresse, qui figure dans la configuration Docker Compose publiée. Une publication falsifiée l’a redirigé vers un hôte qui n’ existe pas, et `statement` a échoué : un faussaire ne pouvait pas se faire passer pour le collecteur, mais pouvait bloquer la vérification par un tiers, pendant jusqu’à 12 heures à l’aide d’un horodatage futur falsifié. Le collecteur publie désormais également son adresse signée avec sa propre clé ; `verify` n’accepte que ces publications lorsque le collecteur les effectue, et les publications sont classées par ordre de réception par ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) rejoue les publications falsifiées. Un CVM n’exécute cela qu’à partir d’un commit qui le contient ; par conséquent, le collecteur de cette exécution n’avait pas encore signé son adresse et `verify` l’a signalé.
- `tdx_os` ne pouvait pas s’exécuter sans `dstack-mr`, dont la version actuelle porte le nom `measure-os` plutôt que le `measure --json` mentionné dans la documentation. Le vérificateur calcule désormais lui-même les valeurs MRTD et RTMR0-2 à partir de l’image publiée et de la configuration de la machine virtuelle, tables ACPI comprises.

**Deployment 4 · all 16 checks, report seals and restart verification**

- Le déploiement a téléchargé une fois le fichier `dstack-0.5.12` publié, l’a comparé au hachage de l’image du système d’exploitation signalé par la CVM , et `tdx_os` a été validé : MRTD, RTMR0, RTMR1 et RTMR2 correspondent aux valeurs calculées pour QEMU 8.2.2, 1 vCPU et 2 GiB. Le même calcul a donné une valeur RTMR0 différente pour une configuration déclarée de 4 GiB, 2 vCPU, QEMU 9.2.1 ou une deuxième carte réseau, et a échoué en cas de modification du noyau, du micrologiciel ou de la ligne de commande ainsi que pour l’image de développement.
- `verify` a réussi l’ensemble de ses 16 contrôles, y compris celui du connecteur du tunnel rapide, ce qui a donné lieu à un résultat « PASS ». Il a généré le certificat au format HTML et PDF, scellé numériquement à l’aide de signatures et d’horodatages comprenant un horodatage eIDAS qualifié provenant de l’unité d’horodatage du gouvernement belge TSU 202301 (statut accordé sur la liste de confiance belge), un horodatage FreeTSA et la signature du vérificateur ; `check-report` a confirmé l’ensemble de ces éléments ainsi que la signature du fichier PDF.
- Après un redémarrage, `verify --evidence` a confirmé deux démarrages, chacun accompagné d’une attestation matérielle générée au sein de la CVM et chacun ayant démarré à partir du fichier `dstack-0.5.12` publié ; le redémarrage et le nouveau démarrage ont été classés REVIEW.
- `destroy` a laissé l’espace de travail vide.

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- Le collecteur a publié son adresse signée avec sa propre clé, à côté de la publication HMAC de l’opérateur. Deux publications falsifiées ont ensuite été ajoutées au sujet, l’une avec un HMAC remis à zéro et l’autre signée par une autre clé Ed25519, toutes deux indiquant une date en l’an 2096. `verify` a pris l’adresse signée par la clé du collecteur et a réussi les 16 contrôles ; le sceau portait à nouveau l’horodatage belge qualifié, l’horodatage de FreeTSA et la signature du vérificateur, et `check-report` les a confirmés.
- Après un redémarrage, le collecteur a publié la nouvelle adresse signée : `verify` l’a détectée immédiatement, l’ opérateur **a trouvé l’adresse actuelle** 27 secondes plus tard à partir de la publication HMAC, et tous deux ont ignoré les publications falsifiées. `verify --evidence` a confirmé deux démarrages à partir de `dstack-0.5.12`.
- Le déploiement a indiqué le montant facturé par Phala pour la CVM, disque compris : 0,06078 $ par heure.

### Panel wizard and remaining scope

L’assistant du panneau a été exécuté deux fois sur Phala Cloud, une fois via son API de tâches et une fois via le navigateur avec un véritable Chromium : la vérification du prix, la création avec la validation sous **Advanced**, les six vérifications d’attestation ont toutes été réussies, la liste des serveurs affichant le prix facturé (44,37 USD par mois), **Find l'adresse actuelle**, le téléchargement de la configuration Docker Compose mesurée, ainsi que la suppression. Le navigateur n’a signalé aucune erreur de page. À chaque fois, l’espace de travail était vide par la suite.

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

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

## Recherche en texte intégral sur un million de messages · 5 novembre 2026

Commande : `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

Un journal signé et déterministe contenant 1 000 000 de messages synthétiques répartis dans 200 discussions (formes de mots en russe, en ukrainien, en anglais, en chinois et en japonais, liens et identifiants) a été indexé en 71 secondes ; l’index occupait 58 Mio en plus d’un journal de 1,50 Gio. Les recherches par meilleure correspondance ont pris entre 9 et 190 ms (médiane), contre 2,4 à 3,2 secondes pour la précédente recherche par sous-chaîne . Résultats complets, matériel et limites : [Recherche en texte intégral](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#benchmark). `tools/test_fulltext.py` vérifie également une archive signée créée avant la recherche en texte intégral (`tools/fixtures/evidence-before-fulltext.zip`) à l’aide du vérificateur actuel, ainsi qu’une archive actuelle par rapport à cette archive elle-même `verify.py`.

## Autres précisions

Le journal en temps réel conservé consigne les collectes effectives, les modifications, les notifications de suppression, les pièces jointes, les vérifications croisées et la gestion des limites de débit. Il ne rend pas compte de manière exhaustive des envois ni ne fournit une matrice contrôlée de visibilité des rôles, des acteurs intervenant dans les réactions, des délais prolongés de « FloodWait », des suspensions de compte et de la reprise après interruption du réseau ou des processus. L’émission de jetons QR reste distincte de la confirmation QR mobile finalisée.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
