# MCP en lecture seule

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/

Connectez un client MCP à des espaces de travail et des discussions sélectionnés avec un accès à durée limitée et révocable.

**Point important :** utilisez une version de la source ; la version préliminaire portable 0.7.0 est antérieure à cette fonctionnalité.

[Guide des procédures](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Installez le serveur optionnel à partir du répertoire du projet TgWitness :

```
python -m pip install '.[mcp]'
```

Dans le panneau, ouvrez **Intégrations → MCP**. Nommez la connexion, sélectionnez ses espaces de travail et ses discussions, puis choisissez une date d’expiration. Copiez le jeton d’archivage une seule fois ; il ne pourra pas être récupéré par la suite. Révoquez les jetons perdus et émettez des jetons de remplacement. Les jetons du panneau et les identifiants Telegram ne constituent pas des identifiants MCP.

## Connecter un client

Le panneau génère « `.vscode/mcp.json` » pour le **harnais local de VS Code** à l’aide de sa [configuration documentée](https://code.visualstudio.com/docs/agents/reference/mcp-configuration). Enregistrez le fichier téléchargé à cet emplacement, exécutez **MCP : List Servers**, puis lancez TgWitness. VS Code vous demande le jeton via une invite de saisie de mot de passe. Le fichier JSON téléchargé contient une référence d’invite, et non le jeton. Utilisez l’exécutable Python depuis l’environnement dans lequel l’extension MCP est installée.

Pour les autres clients stdio, exécutez :

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

Configurez `TGWITNESS_ARCHIVE_TOKEN` dans l'environnement protégé du client. Ne l'incluez pas dans les arguments de commande ni dans les URL. Le pont lit les données via l'API d'archivage autorisée du panneau ; il n'a pas d'accès direct à la base de données. La sortie standard (stdout) ne transmet que les messages MCP.

Pour les clients distants, exécutez le service à côté du panneau :

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

Redirigez `/mcp` via un proxy inverse HTTPS vers `127.0.0.1:8766/mcp`, en conservant l'en-tête `Authorization: Bearer …`. Désactivez la journalisation des en-têtes d'autorisation et des corps de requête/réponse. Effectuez une liaison au-delà du loopback uniquement lorsque cela est nécessaire, en utilisant `--host` et `--public-url`. Le point de terminaison utilise Streamable HTTP issu du [SDK Python officiel MCP](https://github.com/modelcontextprotocol/python-sdk). Il prend en charge les identifiants « bearer » configurés explicitement, mais pas la découverte OAuth ; les clients nécessitant uniquement OAuth ne sont pas pris en charge.

**La vérification du protocole et l’accès** initialisent un véritable client MCP et répertorient les outils. Cette opération ne récupère pas les messages. Pour une vérification à distance, le serveur MCP choisi reçoit le jeton d’archive. Ne configurez qu’un serveur que vous exploitez vous-même ou en lequel vous avez confiance pour cette utilisation.

## Portée et résultats

Outils disponibles : `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event` et `get_capture_status`. Il n’existe pas d’actions Telegram, de modifications de configuration ni d’ outils d’exportation en masse. Chaque lecture vérifie à nouveau l’accès à l’espace de travail/au chat ; les identifiants expirés ou révoqués cessent de fonctionner. Les limites sont de 60 requêtes API par minute et par identifiant, 50 enregistrements par page, une réponse de 64 KiB et un délai API de huit secondes.

Les résultats des messages comprennent l'espace de travail, les identifiants de discussion/message, la séquence des événements, le hachage enregistré, ainsi qu'un lien vers le panneau. L'utilisateur ouvrant un lien doit disposer de sa propre session de panneau autorisée. Les objets Telegram bruts, les hachages d'accès, les références de fichiers, les éléments de session, ainsi que les clés sont omis. La recherche porte sur le texte des messages, et non sur les champs bruts. Le texte est délimité et les troncatures sont signalées. Les modifications, les notifications de suppression de Telegram et « `missing_on_recheck` » restent des observations distinctes. L’accès limité au chat ne permet pas de voir les événements opérationnels à l’échelle de l’espace de travail ; l’état de la capture indique explicitement cette limite.

Le texte archivé est considéré comme une entrée non fiable. Les instructions contenues dans les messages ne confèrent aucune portée supplémentaire et ne doivent pas être traitées comme des instructions du client. Un modèle d’IA externe peut recevoir tout contenu demandé par son client MCP. L’accès en lecture seule empêche toute modification des archives ; il n’empêche pas un client de conserver les données qu’il lit.

Les hachages identifient les enregistrements sauvegardés et permettent de vérifier leur intégrité. Ils ne prouvent pas à eux seuls l’origine des messages sur Telegram ni que chaque message a bien été capturé.
