# Ligne de commande

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/cli/

Rechercher, lire le contexte, compter les activités et exporter les messages enregistrés à partir de scripts et d'agents, avec une sortie au format --json, des codes de sortie stables et des jetons en lecture seule à portée limitée.

[MCP en lecture seule](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/) · [Recherche en texte intégral](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Aperçu.** `tgwitness search`, `context`, `messages`, `stats` et `export` lire les observations enregistrées pour les scripts et les agents IA. Ils ne peuvent rien envoyer vers Telegram, ni modifier les paramètres ou le journal signé.

Avec `--json`, la sortie standard (stdout) contient exactement un document JSON (`export` écrit des lignes JSON). La progression, les conseils et les erreurs sont envoyés vers stderr. Les codes de sortie sont stables :

| Code | Signification |
| --- | --- |
| `0` | Succès, y compris en cas de résultat vide |
| `1` | Échec : panneau inaccessible, données illisibles, exportation interrompue |
| `2` | Erreur d'utilisation ou requête non valide : date incorrecte, option inconnue, index de recherche désactivé |
| `3` | Indisponible pour le moment : l'espace de travail est ouvert dans un panneau en cours d'exécution, ou le panneau demande de réessayer plus tard (limite de débit, délai d'attente) |
| `4` | Accès refusé : jeton manquant, expiré ou révoqué, discussion hors de son champ d'application, outil non autorisé |

## Deux façons de lire

**Via le panneau (`--url`).** La commande utilise la même API d'archivage à portée que MCP. Créez une connexion dans **Intégrations → MCP** : choisissez des espaces de travail et des discussions, des outils et une durée de validité, puis copiez le jeton une seule fois. La connexion est en lecture seule, limitée à ces discussions, plafonnée à 60 requêtes par minute et peut être révoquée ou renouvelée à tout moment. Les jetons de connexion au panneau et les identifiants Telegram ne fonctionnent pas ici.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

Un panneau distant nécessite le protocole HTTPS ; le protocole HTTP simple n'est accepté que pour `127.0.0.1`, `localhost` et `::1`. Les variables d’environnement de proxy sont ignorées et les redirections sont refusées, de sorte que le jeton n’atteigne que l’adresse que vous indiquez.

**Directement à partir d’un espace de travail arrêté (`--data-dir`).** Lit le répertoire de données avec un accès local complet, sans jeton. À utiliser sur une copie d’un répertoire de données ou lorsque la collecte est arrêtée. Les enregistrements signés ne sont jamais modifiés ; comme dans le panneau, l’ouverture d’un espace de travail peut mettre à jour ses index dérivés. Lorsque le panneau a l’espace de travail ouvert, la commande se termine avec le code `3`; lisez plutôt via le panneau. En l’absence de `--data-dir`, `TGWITNESS_DATA`, `./data/live` ou le répertoire de données de l’installation exécutant la commande est utilisé.

`--workspace ID` sélectionne un espace de travail (par défaut `default`). `tgwitness messages
--workspaces` affiche la liste de ceux que vous pouvez consulter.

## Commandes

| Commande | Résultat |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | Résultats les plus pertinents en premier, avec les formes des mots, les expressions exactes entre guillemets, les domaines et `@username` ([syntaxe](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | Texte exact, du plus récent au plus ancien, sans l'index |
| `tgwitness context CHAT_ID MESSAGE_ID` | Messages enregistrés dans un intervalle de dix identifiants de message de part et d'autre |
| `tgwitness messages` | Discussions que vous pouvez lire |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | Messages enregistrés de la conversation, les plus récents en premier |
| `tgwitness messages CHAT_ID --message ID` | Chaque version enregistrée et chaque enregistrement de suppression d'un message |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | Statistiques d'activité, ci-dessous |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | Observations enregistrées sous forme de lignes JSON dans l'ordre du journal |

Les dates sont exprimées en `2026-10-01` (minuit UTC) ou exprimées selon le format ISO avec un fuseau horaire, `2026-10-01T09:00+03:00`. Pour `search`, `messages` et `export` ils sélectionnent l'heure de l'observation. Les pages peuvent contenir jusqu'à 50 enregistrements : suivez `next_offset` (`--offset`) pour la recherche par classement et `next_before` (`--before`) ailleurs.

Ranked search stops at 1,000 results. The final page may be shorter than `--limit`; narrow the query, chat or period when more matching observations exist.

Chaque résultat de message comporte `untrusted_content: true`: les identifiants de l'espace de travail, de la conversation et du message, le numéro de séquence du journal, le hachage de l'enregistrement sauvegardé et un lien vers le panneau. Les modifications, les notifications de suppression et les `missing_on_recheck` constituent des enregistrements distincts. L’absence d’un enregistrement ne prouve pas qu’un événement ne s’est jamais produit.

### Statistiques d'activité

`stats` Compte le nombre d'observations enregistrées pour une conversation, un expéditeur ou toutes les conversations concernées :

- messages par heure UTC et par jour de la semaine (en commençant par le lundi), heures et jours les plus chargés ;
- modifiés, supprimés et `missing_on_recheck` partages ;
- les expéditeurs avec le nombre de messages ainsi que les heures du premier et du dernier message ;
- les domaines les plus fréquents et `@handles`, comptés une fois par message parmi ses versions enregistrées ;
- Couverture : `coverage.gap` enregistrements et, pour l'accès à l'ensemble de l'espace de travail, périodes sans signal de présence du collecteur connecté (`collector_liveness`).

La période correspond à **l’heure des messages telle que rapportée par Telegram**. Le nombre d’heures et de jours de la semaine peut aider à estimer le fuseau horaire de l’expéditeur ; il ne permet toutefois pas de le déterminer avec certitude. Les chiffres sont calculés sur demande à partir du journal et ne sont pas stockés. Chaque résultat indique l’en-tête du journal qu’il couvre lorsque votre accès s’étend sur l’espace de travail. La lecture s’arrête après cinq secondes via le panneau, ou `--timeout` secondes en local (30 par défaut) ; ensuite, `complete` est faux et `partial` indique le premier enregistrement qui n’a pas été lu. Seuls les enregistrements les plus récents sont pris en compte dans ce cas.

### Exporter

`export` Il génère un objet JSON par observation enregistrée (nouveaux messages, captures d’écran, modifications, messages récupérés, notifications de suppression, `missing_on_recheck` et les enregistrements de médias sauvegardés) dans l’ordre du journal. Chaque ligne comporte les mêmes champs que les autres résultats, avec le texte intégral. Avec `--output`, le fichier est enregistré sous un `.partial` nom et n'est renommé qu'après l'enregistrement de la fin du panneau ; une exportation interrompue ne laisse aucun fichier et se termine avec le code `1`. `--output` ne remplace jamais un fichier existant. Avec `--output` et `--json`, stdout affiche un résumé : nombre d’enregistrements, dernière séquence du journal et, pour l’accès à l’ensemble de l’espace de travail, l’en-tête du journal.

Une exportation via le panneau nécessite une connexion autorisant **l’exportation des messages (ligne de commande uniquement)** ; cette option n’est pas sélectionnée par défaut. Ce fichier est une copie de travail, et non une preuve : pour un transfert vérifiable, utilisez l’exportation signée dans **la** **section** **« Exportations »**, qui `python -m tgwitness.verify`effectue des vérifications.

The panel rechecks access before emitting each record, including the completion record. Revoked or expired access leaves an incomplete export. Lazy page reads share the archive worker limit with other queries and have a bounded wait.

## Compétences de l'agent

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) explique à un agent comment utiliser ces commandes, comment citer les enregistrements et comment traiter le texte capturé. Les agents qui lisent `.agents/skills` le chargent à partir d’un dépôt de code. Pour Claude Code, copiez le `tgwitness-cli` dossier dans `.claude/skills/` dans votre projet ou `~/.claude/skills/`.

## MCP et la ligne de commande

Les deux utilisent les mêmes connexions, les mêmes vérifications de portée et les mêmes limites. Les résultats de MCP sont limités à une page de 64 KiB ; MCP ne propose donc pas d’exportation en masse ; la ligne de commande les transmet en continu. `get_activity_stats` est disponible pour les deux.
