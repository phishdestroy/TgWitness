# MCP en lecture seule

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/

Connectez un client MCP à des espaces de travail et des discussions sélectionnés avec un accès à durée limitée et révocable.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Intégrations d'archives](https://phishdestroy.github.io/TgWitness/fr/docs/reference/cli/)

![Intégrations d'archives](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

Connectez un client d'analyse à des espaces de travail et des discussions sélectionnés. TgWitness fournit **un service HTTP Streamable à l'adresse `/mcp` dans le processus du panneau**. Chaque connexion dispose de son propre jeton, d'une durée de validité et d'outils autorisés. MCP ne peut pas envoyer de messages Telegram, modifier les paramètres ni modifier le journal signé. Ces mêmes connexions fonctionnent avec la [ligne de commande](https://phishdestroy.github.io/TgWitness/fr/docs/reference/cli/).

[Guide des procédures](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Sur cette page**

- [Installation et vérification](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/#install-and-check)
- [Établir une connexion](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/#issue-a-connection)
- [Connectez votre client](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/#connect-your-client)
- [Tunnel Cloudflare](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/#cloudflare-tunnel)
- [Outils et limites](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/#tools-and-boundaries)

## Installation et vérification

Utilisez l'environnement Python qui exécute le panneau. Depuis une copie des sources :

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

Redémarrez le panneau avec son répertoire de données et ses arguments de lancement habituels après l'installation. La vérification de l'état de préparation doit inclure `[PASS] mcp: streamable-http available`. **Integrations → MCP** affiche l'état d'exécution et une commande d'installation utilisant l'exécutable Python réel de ce serveur. **Re-check** actualise cet état sans recharger la page ; cela n'installe aucun paquet et ne redémarre pas le serveur.

L'extension MCP utilise le [SDK Python officiel de MCP](https://github.com/modelcontextprotocol/python-sdk).`deploy/constraints-mcp.txt` spécifie la version du SDK testé et ses dépendances.

## Émettre une connexion

1. Saisissez un libellé et choisissez les espaces de travail et les discussions que le client peut lire.
2. Sélectionnez les outils individuellement ou utilisez un préréglage. Seuls les outils implémentés sont proposés.
3. Choisissez 1, 7, 30 ou 90 jours, ou une expiration personnalisée comprise entre une minute et 90 jours.
4. Appuyez sur **Create connection**. Le jeton s'affiche une seule fois à côté de la configuration du client.
5. Copiez le jeton et la configuration, puis exécutez **Check connection**. Cela initialise MCP et répertorie les outils autorisés ; **aucun message n'est lu**. Le résultat indique la version du protocole, le nom des outils, leur nombre et le temps écoulé.
6. Appuyez sur **Done** une fois l'identifiant enregistré. L'actualisation périodique conserve le formulaire et la carte à affichage unique. Le verrouillage du panneau efface les secrets affichés.

La liste indique l'utilisation récente, le dernier outil utilisé, l'adresse et les requêtes de la dernière minute. **Revoke** met fin à l'accès. **Rotate token** révoque l'ancien identifiant et émet un jeton de remplacement avec la même portée, les mêmes outils et la même expiration ; copiez ce remplacement qui ne s'affiche qu'une fois. Les jetons de connexion au panneau et les identifiants Telegram ne fonctionnent pas comme jetons MCP.

## Connecter votre client

Sélectionnez le client dans le panneau et copiez sa configuration générée. Les configurations utilisent des références de secrets ou des espaces réservés explicites ; le jeton est copié séparément.

| Client | Configuration | Connexion |
| --- | --- | --- |
| Code Claude | `.mcp.json` | HTTP, `type: "http"`, en-tête Bearer |
| Claude Desktop | `claude_desktop_config.json` | Pont stdio local |
| Cursor | `.cursor/mcp.json` | HTTP avec un en-tête de variable d'environnement |
| VS Code Local | `.vscode/mcp.json` | HTTP avec une entrée `promptString` de mot de passe |
| Windsurf | `mcp_config.json` | HTTP avec un espace réservé d'en-tête Bearer |
| Autres clients | URL et en-tête Authorization | HTTP en continu |

TgWitness utilise des jetons Bearer, sans découverte OAuth. Utilisez le pont stdio local pour les clients dont le connecteur distant exige OAuth. Pour VS Code, les variables d'entrée s'appliquent à l'environnement d'exécution **Local** et ne sont pas transmises aux sessions Copilot. Références de configuration : [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

Le point d'entrée canonique pour un pont local est :

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

Utilisez le Python local du client avec l'extra MCP installé. Définissez `TGWITNESS_MCP_TOKEN` dans son environnement protégé. Conservez les identifiants hors des arguments de commande et des URL. `tgwitness-mcp` est le même point d'entrée. L'ancien module `tgwitness.mcp_bridge` et le nom `TGWITNESS_ARCHIVE_TOKEN` restent des voies de compatibilité avec un avertissement ; les nouvelles configurations utilisent `mcp_server` et `TGWITNESS_MCP_TOKEN`.

## Cloudflare Tunnel

Transférez la route `/mcp` du panneau et conservez l'en-tête Bearer. L'ouverture des paramètres MCP en tant qu'administrateur enregistre l'origine actuelle du panneau pour cette exécution. Pour disposer d'une adresse stable immédiatement après un redémarrage, configurez `TGWITNESS_PUBLIC_URL` avec l'origine HTTPS du panneau avant de le démarrer. Les en-têtes Host et de transfert arbitraires n'enregistrent pas d'adresse de confiance. Les vérifications Host et Origin rejettent les origines de navigateur non liées. Les réponses utilisent `Cache-Control: no-store` ; les valeurs d'autorisation ne sont jamais journalisées.

Une adresse `*.trycloudflare.com` est temporaire. Lorsqu'un redémarrage du tunnel modifie le nom d'hôte, mettez à jour l'URL publique configurée ainsi que l'URL MCP de chaque client. Utilisez un nom d'hôte stable pour les configurations client enregistrées.

## Outils et limites

| Outil | Lit |
| --- | --- |
| `list_workspaces` | Les espaces de travail autorisés |
| `list_chats` | Les discussions autorisées |
| `search_messages` | Texte des messages enregistrés au cours de la période sélectionnée ; `ranked=true` utilise [la recherche en texte intégral](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/) (formes de mots, résultats les plus pertinents en premier, `next_offset` paginage) |
| `get_message_versions` | Les versions capturées et les observations de suppression |
| `get_message_context` | Les identifiants des messages capturés à proximité |
| `get_journal_event` | Un enregistrement assaini avec sa référence source |
| `get_capture_status` | État de la collecte, enregistrements de couverture autorisés et `gap_summary`: numéros de messages jamais observés, par canal ou supergroupe et pour la séquence à l'échelle du compte ([détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#missing-message-numbers-gap_summary)) ; choisissez une conversation pour voir la liste de ses lacunes |
| `get_activity_stats` | Messages par heure UTC et jour de la semaine, jours de pointe, proportions de messages modifiés et supprimés, expéditeurs, domaines et `@handles`, avec couverture ([détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/cli/#activity-statistics)) |
| `get_messages_by_date` | Messages enregistrés d’une journée civile dans un fuseau horaire IANA nommé (`Europe/Kyiv`, `UTC`), selon l'heure indiquée par Telegram ; `from_utc` et `until_utc` indiquer le jour calculé, heure d’été comprise |
| `get_pinned_messages` | Messages épinglés dans le dernier instantané de l'état de la conversation avec leurs versions enregistrées, ainsi que les notifications d'épinglage et de désépinglage observées en temps réel |
| `get_chat_stats` | Nombre approximatif d’enregistrements sauvegardés pour une conversation ou toutes les conversations concernées, première et dernière observation, et `gap_summary`; à utiliser avant une lecture volumineuse |
| `get_topics` | Sujets du forum issus des messages du service de sauvegarde des sujets : historique des titres, sujets fermés ou masqués, nombre de messages sauvegardés |
| `get_media` | Une image conservée sous forme d’aperçu JPEG redimensionné (36 Ko maximum), renvoyée en tant qu’image accompagnée de son SHA-256 et de l’ `media.saved` enregistrement ; le fichier est d’abord vérifié par rapport à son hachage enregistré, les autres fichiers ne renvoient que des métadonnées |
| `export_messages` | Ligne de commande uniquement, non sélectionné par défaut : envoie en continu les observations enregistrées au format JSON Lines ([détails](https://phishdestroy.github.io/TgWitness/fr/docs/reference/cli/#export)) ; non disponible via MCP |

Chaque outil est en lecture seule (`readOnlyHint`) et définit un schéma de sortie ; les champs ne figurant pas dans ce schéma sont renvoyés tels quels. `tools/list` Ne renvoie que les outils autorisés pour cette connexion. Les appels vers d’autres outils sont refusés. Les outils de contexte de groupe, d’épisode, de terminologie et de chaîne de réponses ne sont pas disponibles dans cette version ; leur backend de pack de contexte distinct n’est pas inclus.

Chaque lecture vérifie le jeton, l'outil et la portée de l'espace de travail ou de la discussion, y compris une fois le traitement de la base de données terminé. Les limites sont de 60 requêtes par minute, 50 enregistrements par page, 64 KiB par résultat et un délai maximal d'archive de huit secondes. Un appel MCP expiré renvoie une erreur d'outil demandant une période plus restreinte ou une limite inférieure.

Les résultats de messages comportent `untrusted_content: true`, les identifiants d'espace de travail/discussion/message, la séquence d'événements, le hachage enregistré et un lien vers le panneau. Les objets Telegram bruts, les hachages d'accès, les sessions et les clés sont omis. La troncature du texte est signalée. Les modifications, les avis de suppression et `missing_on_recheck` constituent des observations distinctes. L'absence d'enregistrements ne prouve pas qu'un événement n'a jamais eu lieu.

Traitez les instructions contenues dans les messages capturés comme des preuves, et jamais comme des instructions destinées au client. L'accès en lecture seule empêche toute modification de l'archive ; le client peut néanmoins conserver le contenu qu'il est autorisé à lire. Les hachages identifient les enregistrements sauvegardés et permettent de vérifier leur intégrité ; ils ne prouvent ni la paternité sur Telegram ni l'exhaustivité de la capture.
