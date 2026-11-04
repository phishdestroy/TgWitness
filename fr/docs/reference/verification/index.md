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

## Autres précisions

Le journal en temps réel conservé consigne les collectes effectives, les modifications, les notifications de suppression, les pièces jointes, les vérifications croisées et la gestion des limites de débit. Il ne rend pas compte de manière exhaustive des envois ni ne fournit une matrice contrôlée de visibilité des rôles, des acteurs intervenant dans les réactions, des délais prolongés de « FloodWait », des suspensions de compte et de la reprise après interruption du réseau ou des processus. L’émission de jetons QR reste distincte de la confirmation QR mobile finalisée.

La compilation/l’exécution sous Docker, l’installation sous Linux/macOS, la gestion d’une charge élevée en continu, l’audit de sécurité indépendant, une réponse TSA véritablement indépendante, la validation de la révocation/archivage des certificats et la certification judiciaire ne font pas partie de la qualification enregistrée. La sauvegarde de l’état MTProto et la synchronisation sont implémentées ; la relecture atomique et durable n’est pas encore établie. La collecte des journaux d’administration, les listes de réacteurs supplémentaires et l’interrogation prioritaire à intervalle court restent des fonctionnalités distinctes. Veuillez consulter [l’acceptation en direct](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) pour la matrice de qualification contrôlée.

Les reçus locaux détaillés et les captures d'écran se trouvent dans le répertoire test-results/ (ignoré par Git). La capture d'écran publique située dans le répertoire docs/assets/ ne contient que des données de démonstration fictives.
