# Telegram · Recherche en texte intégral

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/

Recherchez les messages enregistrés par formes de mots, expressions exactes, domaines et @noms d'utilisateurs, en affichant les résultats les plus pertinents en premier, grâce à l'index lié au journal signé.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Enquête](https://phishdestroy.github.io/TgWitness/fr/docs/reference/investigation/)

![Enquête](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Analyse des archives](https://phishdestroy.github.io/TgWitness/fr/docs/reference/analysis/) · [OCR et transcription en local](https://phishdestroy.github.io/TgWitness/fr/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Aperçu.** Dans **«** **Journal** », sélectionnez **« Meilleure correspondance · formes du mot »** à côté du champ de recherche. Les résultats sont classés selon l’algorithme BM25 et correspondent à d’autres formes du même mot : *« перевод »* trouve *« переводом »* et *«* *переводы »*, *« transfer »* trouve *« transfers »*, une phrase en chinois est trouvée sans espaces. L’option « **Les plus récents en premier · texte exact »** conserve la recherche de sous-chaîne précédente sur l’ensemble de l’enregistrement.

L'index est constitué de données dérivées. Il est reconstruit à partir du journal signé, n'est jamais signé en soi et n'est jamais inclus dans une exportation. Les enregistrements d'origine ne sont pas modifiés.

**Sur cette page**

- [Syntaxe de recherche](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#search-syntax)
- [Langues](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#languages)
- [Emplacement de l'index](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#where-the-index-lives)
- [Résultats et journal signé](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#results-and-the-signed-journal)
- [Texte reconnu](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#recognized-text)
- [Accès](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#access)
- [Consulter les archives et MCP](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#ask-the-archive-and-mcp)
- [Dépendances](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#dependencies)
- [Benchmark](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#benchmark)

## Syntaxe de recherche

| Rédiger | Résultats |
| --- | --- |
| `перевод карта` | Enregistrements contenant les deux mots, sous quelque forme que ce soit |
| `"переводом на карту"` | La phrase exacte, dans cet ordre |
| `бонус OR подарок` | L'un ou l'autre |
| `перевод -казино` | Enregistrements ne contenant pas le mot exclu |
| `example.com` | Le domaine et ses sous-domaines, y compris dans les liens masqués et les URL des boutons |
| `@username`, `t.me/username` | Mentions et liens du compte, ainsi que les messages qu'il a envoyés |
| `#tag` | Le hashtag |
| `+79991234567`, une adresse de portefeuille, une adresse e-mail | La même valeur sous forme de texte ou de liens |
| `from:@username`, `from:123456` | Messages provenant de cet expéditeur |
| `chat:-1001234567890` | Une seule conversation ; cela ne peut restreindre que votre propre accès |
| `id:42` | Versions enregistrées du message 42 |
| `since:2026-01-01 until:2026-01-31` | Période d'observation : une date sans heure couvre toute la journée |
| `kind:edited` | Uniquement les modifications (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Texte reconnu à la place des messages ou en complément de ceux-ci |

Les prépositions et autres mots fonctionnels sont ignorés lorsqu'ils sont accompagnés d'autres mots. Les lettres similaires mélangées au sein d'un mot (un *« a »* latin dans un mot cyrillique), les lettres Unicode de pleine largeur et décoratives, ainsi que les caractères invisibles sont normalisés.

## Langues

La langue est détectée pour chaque enregistrement à partir de son script et de ses caractères :

| Script | Correspondance |
| --- | --- |
| Cyrillique | Lemmes russes et ukrainiens avec [pymorphy3](https://github.com/no-plagiarism/pymorphy3). En l'absence du dictionnaire ukrainien optionnel, un stemmer ukrainien allégé est utilisé. |
| Latin | Stemmer « Snowball » en anglais ; les signes diacritiques sont ignorés |
| Chinois, japonais, coréen, thaï, laotien, khmer, birman | Paires de caractères qui se chevauchent : toute expression est recherchée sans espaces. Les requêtes en chinois sont divisées en mots à l'aide de Jieba. |
| Autres scripts | Termes exacts |

Le dictionnaire ukrainien (`pymorphy3-dicts-uk`) est distribué sous licence GPL-3.0 ; il n’est donc pas installé par défaut. Installez-le à l’aide de `pip install "tgwitness[uk-dictionary]"`; l'index détecte le nouvel analyseur et se reconstruit automatiquement.

## Emplacement de l'index

| Mode | Stockage | Utilisation |
| --- | --- | --- |
| Sur disque (par défaut) | `search/fulltext.sqlite3` dans le répertoire de l'espace de travail | Archives volumineuses ; résiste aux redémarrages |
| En mémoire uniquement | Rien n'est stocké sur le disque ; l'outil est reconstruit à chaque démarrage | Aucune copie dérivée du texte des messages n'est conservée sur le disque |
| Désactivé | Pas d'index ; **les plus récents en premier · le texte exact** est conservé | Installations minimales |

L'administrateur principal choisit le mode sous **Journal → Filtres → Index de recherche** pour chaque espace de travail. `TGWITNESS_FULLTEXT=disk|memory|off` Il définit la valeur par défaut pour les espaces de travail ne disposant pas de leur propre choix. Le passage en mode « mémoire » ou la désactivation suppriment le fichier. Le fichier d’index bénéficie de la même protection que le journal : il se trouve dans le répertoire des données privées . Il n’est pas chiffré et ne fait pas partie des sauvegardes ni des copies hors site.

Les nouveaux enregistrements sont indexés en arrière-plan en quelques secondes ; une recherche indexe également en priorité un petit historique, ce qui permet de retrouver un enregistrement sauvegardé il y a quelques instants. Un journal existant est indexé après la mise à jour sans bloquer le panneau ; jusqu’à ce moment-là, les résultats couvrent les enregistrements indexés et le journal affiche la progression. **La reconstruction de l’index** recommence à partir du premier enregistrement.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` nécessite l'arrêt du panneau (code de sortie 3 dans le cas contraire). Avec `--json`, la sortie standard ne contient que le résultat ; la progression est affichée sur la sortie d'erreur standard.

## Résultats et journal signé

L'index stocke le numéro de séquence et le hachage du dernier enregistrement du journal qu'il couvre et les compare au journal lors de son ouverture. Un journal remplacé, restauré ou modifié entraîne une reconstruction. Chaque réponse signale cette position, et chaque résultat est récupéré à partir du journal signé grâce à son numéro de séquence : l'index décide quels enregistrements afficher et dans quel ordre, mais jamais leur contenu. L'accès au chat s'applique au champ de discussion du journal lui-même, et non au contenu de l'index.

## Texte reconnu

L'OCR et les transcriptions restent dans leurs artefacts chiffrés. Leur index n'existe qu'en mémoire et est reconstruit à la fin de chaque tâche de reconnaissance. Un résultat apparaît dans son `media.saved` enregistrement, identifié comme une reconnaissance automatique avec le moteur, le modèle et un extrait ; il n’est jamais présenté comme du texte envoyé via Telegram. Le même index alimente la fonctionnalité « **Recherche de texte reconnu** », qui permet également de trouver des sous-chaînes en clair.

## Accès

L'accès limité aux discussions ne trouve que les enregistrements provenant de ces discussions, y compris le texte reconnu de leurs pièces jointes. `chat:` et d’autres filtres ne peuvent que restreindre cet ensemble. L’état de l’index affiché pour l’accès limité omet les totaux du journal. Seul l’administrateur principal peut modifier le mode ou reconstruire l’index.

## Consultez les archives et le MCP

**Demandez à l’archive** de récupérer ses sources à partir de cet index lorsqu’il est complet : les meilleures correspondances parmi les discussions sélectionnées, chaque texte enregistré n’étant compté qu’une seule fois. Jusqu’à 24 sources sont envoyées ; les textes longs sont tronqués autour de leur correspondance et marqués comme tronqués. Les requêtes concernant les modifications récentes, les versions enregistrées d’un message et les recherches pendant que l’index est encore en cours de construction utilisent la récupération chronologique précédente. L’aperçu indique quelle méthode a été utilisée.

Les clients MCP peuvent appeler `search_messages` avec `ranked=true` et les pages avec `next_offset`. Les connexions à portée restreinte ne reçoivent que leurs propres discussions.

La pagination classée couvre au maximum les premiers résultats 1,000, quelle que soit la taille de la page. Affiner la requête, la conversation ou la période pour examiner d’autres correspondances. Les recherches les plus récents en premier classent les messages, les résultats OCR et les transcriptions avant la sélection de chaque page.

## Dépendances

| Paquet | Licence | Pourquoi |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Lemmes en russe et en ukrainien ; les dictionnaires sont chargés localement |
| snowballstemmer | Clause BSD-3 | Racines en anglais, Python pur |
| jieba | MIT | Segmentation des requêtes en chinois, en Python pur (distribution du code source uniquement) |
| pymorphy3-dicts-uk (facultatif) | GPL-3.0 | Dictionnaire ukrainien complet |

SQLite FTS5 nécessite le `unicode61` tokenizer est indispensable ; il fait partie de SQLite dans les versions actuelles de Python. Sans lui, la recherche de la meilleure correspondance signale que la fonctionnalité n'est pas disponible.

## Test de performance

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`Crée un journal signé et déterministe contenant un mélange de messages en russe, ukrainien, anglais, chinois et japonais, avec des liens et des identifiants, issus de 200 discussions ; génère l'index et mesure la durée des recherches types (50 résultats, médiane sur 7 exécutions).

Mesures effectuées sous Windows 11, processeur Intel Core i9-13900K, 128 Go de RAM, Python 3.12.10, SQLite 3.49.1, données stockées sur un disque exFAT, analyseur `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| Mesure | Résultat |
| --- | --- |
| Journal signé | 1 000 000 de messages, 1,50 GiB, enregistrés en 19 minutes |
| Création d'un index à partir du journal | 71 s, soit environ 14 141 messages par seconde |
| Fichier d'index | 58 Mio, soit 3,8 % du journal |
| Recherche immédiatement après un nouvel enregistrement | Médiane de 8 ms, p95 de 9 ms |
| Recherche de sous-chaîne précédente, même journal | `перевод` 3,2 s, `银行转账` 2,6 s, `verify-account.example` 2,6 s |

| Rechercher | Enregistrements correspondants | Meilleure correspondance, médiane | p95 | Les plus récents en premier, par ordre médian |
| --- | --- | --- | --- | --- |
| Mots courants, formes des mots : `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| Deux mots : `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Mot rare : `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Phrase exacte : `"переказ коштів на картку"` | non pris en compte | 35 ms | 36 ms | 6 ms |
| Domaine avec sous-domaines : `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @nomdutilisateur : `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Chinois sans espaces : `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Japonais : `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| Racine en anglais : `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| OU et exclusion : `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Filtre de discussion : `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Filtre de période : `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

Une expression exacte est vérifiée littéralement sur les candidats classés par ordre de pertinence jusqu’à ce que la page soit pleine ; son total n’est donc pas pris en compte. Le temps de traitement augmente avec le nombre d’enregistrements correspondants ; restreindre le chat ou la période permet d’accélérer les recherches larges. Le corpus synthétique réutilise un vocabulaire restreint, de sorte que les mots courants correspondent à bien plus d’enregistrements que dans les chats réels.
