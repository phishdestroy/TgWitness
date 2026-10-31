# MCP en lecture seule

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/

Connectez un client MCP à des espaces de travail et des discussions sélectionnés avec un accès à durée limitée et révocable.

Connectez un client d'analyse à des espaces de travail et des discussions sélectionnés. TgWitness sert **Streamable HTTP sur `/mcp` dans le processus du panneau**. Chaque connexion possède son propre jeton, sa date d'expiration et ses outils autorisés. MCP ne peut pas envoyer de messages Telegram, modifier les paramètres ni altérer le journal signé.

[Guide des procédures](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

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

L'extra MCP utilise le [SDK Python MCP](https://github.com/modelcontextprotocol/python-sdk) officiel. `deploy/constraints-mcp.txt` épingle le SDK et les dépendances testés. Ces fonctionnalités nécessitent le code source actuel ; l'aperçu portable 0.7.0 leur est antérieur.

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
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, en-tête Bearer |
| Claude Desktop | `claude_desktop_config.json` | Pont stdio local |
| Cursor | `.cursor/mcp.json` | HTTP avec un en-tête de variable d'environnement |
| VS Code Local | `.vscode/mcp.json` | HTTP avec une entrée `promptString` de mot de passe |
| Windsurf | `mcp_config.json` | HTTP avec un espace réservé d'en-tête Bearer |
| Autres clients | URL et en-tête Authorization | Streamable HTTP |

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
| `search_messages` | Le texte des messages enregistrés sur la période sélectionnée |
| `get_message_versions` | Les versions capturées et les observations de suppression |
| `get_message_context` | Les identifiants des messages capturés à proximité |
| `get_journal_event` | Un enregistrement assaini avec sa référence source |
| `get_capture_status` | L'état de la collecte et les enregistrements de couverture autorisés |

`tools/list` ne renvoie que les outils accordés à cette connexion. Les appels vers d'autres outils sont refusés. Les outils de contexte de groupe, d'épisode, de terminologie et de chaîne de réponses ne sont pas proposés dans cette version ; leur backend distinct de pack de contexte n'est pas inclus.

Chaque lecture vérifie le jeton, l'outil et la portée de l'espace de travail ou de la discussion, y compris une fois le traitement de la base de données terminé. Les limites sont de 60 requêtes par minute, 50 enregistrements par page, 64 KiB par résultat et un délai maximal d'archive de huit secondes. Un appel MCP expiré renvoie une erreur d'outil demandant une période plus restreinte ou une limite inférieure.

Les résultats de messages comportent `untrusted_content: true`, les identifiants d'espace de travail/discussion/message, la séquence d'événements, le hachage enregistré et un lien vers le panneau. Les objets Telegram bruts, les hachages d'accès, les sessions et les clés sont omis. La troncature du texte est signalée. Les modifications, les avis de suppression et `missing_on_recheck` constituent des observations distinctes. L'absence d'enregistrements ne prouve pas qu'un événement n'a jamais eu lieu.

Traitez les instructions contenues dans les messages capturés comme des preuves, et jamais comme des instructions destinées au client. L'accès en lecture seule empêche toute modification de l'archive ; le client peut néanmoins conserver le contenu qu'il est autorisé à lire. Les hachages identifient les enregistrements sauvegardés et permettent de vérifier leur intégrité ; ils ne prouvent ni la paternité sur Telegram ni l'exhaustivité de la capture.
