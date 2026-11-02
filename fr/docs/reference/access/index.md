# Accès et autorisations

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/

Définissez les droits d’accès aux comptes et aux discussions, choisissez les autorisations, limitez les sessions et les adresses IP, et révoquez les accès.

Accordez à un réviseur l’accès à une conversation, à un analyste l’autorisation d’exporter un dossier, ou à un opérateur le contrôle de comptes sélectionnés. Chaque personne dispose de son propre jeton. Le jeton du panneau principal reste entre les mains de l’administrateur.

[Configuration du compte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/) · [Itinéraires de connexion](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/) · [Modèle de sécurité](https://phishdestroy.github.io/TgWitness/fr/docs/reference/security/)

## Deux domaines d’application, deux missions distinctes

**La portée de la collecte** détermine ce qu’un compte enregistre : des discussions sélectionnées, un dossier Telegram ou l’intégralité du compte. **La portée d’accès** détermine lesquels de ces comptes et discussions enregistrés une autre personne peut consulter et utiliser. Accorder l’accès ne revient pas à rejoindre une discussion Telegram, à lancer la collecte ni à octroyer des autorisations sur le compte Telegram.

Un accès peut ouvrir des espaces de travail sélectionnés, des discussions sélectionnées au sein de ceux-ci, tous les espaces de travail ou tous les comptes d’un [groupe de comptes](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/#bulk-import-and-account-groups). **L’accès à tous les espaces de travail, y compris ceux ajoutés ultérieurement**, couvre également les futurs comptes. Un accès à un groupe couvre également les comptes ajoutés ultérieurement à ce groupe. Sélectionnez explicitement les espaces de travail lorsqu’un dossier doit se limiter à ceux-ci.

## Accorder un accès à quelqu’un

1. Connectez-vous en tant qu’administrateur principal et ouvrez la rubrique « **Accès** ».
2. Sous « **Accorder l'accès à quelqu'un** », saisissez un nom que vous pourrez reconnaître dans le journal.
3. Sélectionnez les espaces de travail et, si nécessaire, les discussions individuelles.
4. Sélectionnez ce que cette personne est susceptible de faire. La mention « **Afficher »** est toujours incluse.
5. Définissez la durée de validité, les limites de connexion/de session et les adresses autorisées selon vos besoins.
6. Cliquez sur « **Créer un accès** ». Copiez le jeton dès maintenant : il ne s'affiche qu'une seule fois.
7. Envoyez l'adresse du panneau et le jeton en privé. Le destinataire saisit ce jeton sur la page de connexion habituelle ; il n'a pas besoin de votre jeton principal ni d'une session Telegram.

Ouvrez le panneau contenant le jeton généré dans une session de navigateur distincte et vérifiez les discussions visibles ainsi que les actions autorisées avant de le transmettre.

## Choisissez les autorisations

Pour une démonstration publique en mode texte uniquement, utilisez **la « vitrine publique »** plutôt qu'un accès « réviseur » classique. Elle affiche explicitement les canaux publics sélectionnés, les modifications et suppressions conservées, ainsi que les statistiques signées, les champs d'auteur étant masqués et les fichiers fermés à la limite de l'API. [Créez et vérifiez une vitrine](https://github.com/phishdestroy/TgWitness/blob/main/docs/LIVE-SHOWCASE.md).

| Autorisation | Ce qu’il permet |
| --- | --- |
| `view` | Consultez les discussions autorisées, les messages capturés, les profils, les fichiers et les entrées filtrées du journal. Toujours inclus. |
| `export` | Exportation autorisée de l’historique des discussions et des dossiers. L’exportation des preuves de l’ensemble de l’espace de travail nécessite un accès à l’intégralité de celui-ci. |
| `sources` | Gérez les sources, les instantanés et la capture de profils. L’accès limité aux discussions ne peut s’appliquer qu’aux discussions autorisées ; la détection des sources à l’échelle du compte et les paramètres de portée restent désactivés. |
| `collect` | Démarrer ou arrêter un collecteur. Nécessite un accès à l'ensemble de l'espace de travail, car la collecte a une incidence sur le compte. |
| `interact` | Effectuez les interactions Telegram prises en charge dans les limites de votre périmètre d’accès. L’accès limité au chat ne permet pas d’utiliser les aperçus de liens à l’échelle du compte. |
| `settings` | Modifiez les paramètres de collecte, les horodatages, les notifications, les copies hors site et les paramètres. Nécessite un accès à l'ensemble de l'espace de travail. |
| `account` | Connectez-vous ou déconnectez-vous de Telegram et gérez les itinéraires de connexion. Nécessite un accès à l'ensemble de l'espace de travail. |
| `board.read` | Ne lisez les notes du tableau de suivi de l'affaire que dans l'espace de travail et les discussions autorisés. |
| `board.write` | Ajoutez des signets, des surlignages, des extraits, des commentaires et des statuts « ouvert »/« examiné ». Nécessite également la fonction « `board.read` ». |
| `board.manage` | Gérez les collections, les statuts finaux des équipes et les fiches des autres participants. Nécessite également des droits de lecture/écriture sur le tableau. |

Les autorisations et leur portée sont vérifiées conjointement. Cocher une autorisation n’ouvre pas d’autres discussions ni ne débloque une opération à l’échelle de l’espace de travail pour un accès limité à une discussion. Pour une exportation parallèle, l’accès doit couvrir la conversation exportée dans chaque compte sélectionné. Un accès accordé ne permet pas de créer de nouveaux accès, de gérer les sessions d’autres personnes ni d’ouvrir la console d’administration.

### Trois configurations utiles

| Personne | Portée | Autorisations |
| --- | --- | --- |
| Réviseur | Conversations enregistrées dans le cadre d’une affaire | `view` |
| Analyste préparant un transfert de mission | Les conversations à examiner et à exporter | `view`, `export` ; n'ajoutez `interact` que s'ils doivent agir via Telegram |
| Opérateur de collecte | Espaces de travail complets sélectionnés | `view`, `sources`, `collect` ; n'ajoutez `settings` ou `account` qu'en cas de besoin |

Les paramètres par défaut initiaux du formulaire d’accès incluent également le tableau de suivi des dossiers : le réviseur peut lire, l’analyste peut lire et écrire, et l’opérateur peut le gérer. Les paramètres par défaut restent modifiables, et les autorisations existantes ne sont pas automatiquement étendues. Voir [le tableau de suivi des dossiers](https://phishdestroy.github.io/TgWitness/fr/docs/reference/case-board/) pour les périmètres de discussion hérités et la confidentialité des exportations.

## Limites et sessions

| Contexte | Fonctionnement |
| --- | --- |
| Sessions parallèles | Limitez le nombre de sessions simultanées à 1–100. Lorsque cette limite est atteinte, refusez la connexion suivante ou mettez fin à la session la plus ancienne. |
| Connexions autorisées | Limitez le nombre d’utilisations réussies du jeton pour démarrer des sessions. Les sessions existantes ne sont pas interrompues simplement parce que la dernière connexion autorisée a été utilisée. |
| Valable jusqu’au | Expiration définitive de l’accès. Un accès expiré ne permet plus de se connecter ni de continuer à effectuer des requêtes. |
| Minutes sans activité | Délai d’inactivité de la session, de 5 minutes à 30 jours. Les requêtes abouties le prolongent ; un panneau ouvert peut rester actif grâce à un interrogateur. |
| Adresses autorisées | Acceptez des adresses IP spécifiques ou des sous-réseaux CIDR. Laissez ce champ vide pour autoriser toutes les adresses, sauf si la liaison à la première connexion est activée. |
| Se connecter lors de la première connexion | La première connexion réussie enregistre l’adresse autorisée pour cet accès. |

L'adresse IP correspond à l'adresse du client telle qu'elle est perçue par l'application. Si vous vous trouvez derrière un proxy inverse ou un tunnel, vérifiez l'adresse indiquée dans la section « **Sessions ouvertes »** avant de vous fier aux règles basées sur l'adresse IP : sinon, plusieurs utilisateurs pourraient sembler partager l'adresse du proxy.

## Modifier ou retirer l'accès

Modifiez une entrée sous **« Accès »** pour modifier sa portée, ses autorisations ou ses limites. Les modifications de portée et d’autorisations sont vérifiées lors des requêtes suivantes, y compris les requêtes provenant de sessions déjà ouvertes. La révocation d’un accès met fin à ses sessions et rend le jeton émis inutilisable. La gestion **des sessions ouvertes** permet également à l’administrateur de mettre fin à une session individuelle sans révoquer l’accès dans son intégralité.

Les copies d'exportation enregistrées conservent leur créateur, leur espace de travail, la portée de la conversation et les autorisations requises. Un utilisateur disposant d’un accès peut répertorier ou télécharger ses propres copies uniquement tant que ces autorisations sont encore valides ; les copies contenant le « Case Board » nécessitent également l’autorisation « `board.read` ». L’administrateur peut récupérer toutes les copies. Les copies plus anciennes ne comportant pas ces métadonnées et les lots de groupes sont réservés à l’administrateur. Les tickets de téléchargement et les réponses de fichiers préparées vérifient à nouveau les droits d’accès après la préparation du fichier, avant l’envoi de ses octets.

La révocation ne permet pas de récupérer les fichiers qu’une personne a déjà téléchargés. Se déconnecter, verrouiller le panneau ou mettre fin à une session n’arrête pas un collecteur en cours d’exécution.

## Ce que l'administrateur peut voir

Les réviseurs et analystes reçoivent des informations sur l'avancement de la collecte sans points de terminaison proxy, diagnostics de pool, chemins d'accès aux serveurs ni erreurs de connexion brutes. Les diagnostics de connexion nécessitent l'autorisation « `account` » sur l'ensemble de l'espace de travail. La lecture des notifications, la copie hors site et la configuration des paramètres nécessitent l'autorisation « `settings` ».

Les chaînes complètes « User-Agent » du navigateur ne sont pas conservées dans les sessions d’accès. Une mise à jour les supprime également du cache de session modifiable. Le journal des processus du panneau masque les adresses IP littérales, les identifiants d’URL et les secrets étiquetés. Les journaux de service locaux et les enregistrements de journal précédemment signés ne sont pas réécrits. Les règles d’accès et les enregistrements de connexion signés utilisent toujours l’adresse du client.

### Remplacer la clé principale

Utilisez **Accès → Mes limites → Réémettre la clé administrateur**, ou exécutez `tgwitness token rotate` à partir d’une installation gérée pendant que le panneau est en cours d’exécution. Toutes les sessions de navigateur existantes se terminent, y compris celles ouvertes avec des jetons de collègues. Le navigateur demandeur reçoit une nouvelle session ; enregistrez la nouvelle clé administrateur avant de la masquer. Les jetons de collègues émis restent valides jusqu’à ce qu’ils soient révoqués séparément. Une installation utilisant `TGWITNESS_TOKEN` doit modifier ce paramètre d’environnement et redémarrer.

### Limites des requêtes et des proxys

L'API autorise jusqu'à 600 requêtes par minute par adresse IP client. Dix authentifications rejetées en l'espace d'une minute déclenchent un délai d'attente exponentiel, allant d'une seconde à cinq minutes. Une tentative infructueuse après ce délai d'attente prolonge celui-ci ; dix minutes sans tentative infructueuse réinitialisent l'escalade. Les rejets renvoient les codes HTTP 429 et `Retry-After`. Les limites sont gérées en mémoire et partagées entre les espaces de travail au sein d’un même processus de panneau ; un redémarrage les réinitialise. Les flux en direct sont limités à quatre par jeton de support et à 32 pour le processus de panneau. L’ouverture d’un flux consomme également le budget de requêtes API.

Les corps de requête ont un délai de réception de 60 secondes (8 secondes pour MCP). Chaque application limite les corps inachevés à 32 requêtes et à 64 Mio d’allocations de route réservées. Les corps trop volumineux renvoient le code 413, les corps ayant dépassé le délai d’attente renvoient le code 408, et l’épuisement de la capacité des corps renvoie le code 503 avec « `Retry-After` ».

Les en-têtes IP transférés sont ignorés, sauf si le pair TCP réel appartient à `TGWITNESS_TRUSTED_PROXIES` (adresses IP ou CIDR séparées par des virgules). Définissez `TGWITNESS_PROXY_HEADER` sur `x-forwarded-for` ou `cf-connecting-ip`. Le flux XFF est parcouru depuis le proxy le plus proche vers le premier pair non fiable. Les métadonnées d’adresses de confiance mal formées ou en double sont rejetées ; elles ne peuvent donc pas hériter d’une adresse de proxy figurant sur la liste blanche. Le tunnel rapide géré fait confiance au connecteur Cloudflare local ; la configuration sur le domaine propre fait confiance à Caddy local. Les déploiements directs ne font confiance à aucun proxy par défaut. Si vous lancez Uvicorn vous-même, désactivez son traitement des en-têtes de proxy afin que cette frontière reçoive le pair réel.

`TGWITNESS_PANEL_ALLOWED_IPS` restreint tout accès au panneau de configuration, y compris celui de l’administrateur, aux adresses IP ou CIDR répertoriées. La sonde d’identité de routage du programme d’installation reste publique et ne renvoie aucune donnée de compte. Incluez la route administrative locale requise avant d’activer la liste blanche. Le guide **START-HERE** d’une installation gérée comprend les instructions de configuration du service et de restauration.

Un sélecteur de requête API `ws` doit identifier l'espace de travail dans le chemin d'accès de la requête ; les sélecteurs inconnus, non correspondants ou en double sont rejetés avec un code d'erreur 404.

Les scripts et les styles des panneaux contiennent des métadonnées d’intégrité SHA-384. Une carte d’importation couvre également les modules JS importés localement dans les navigateurs prenant en charge l’intégrité des cartes d’importation. La réponse linguistique générée dynamiquement est distincte. Ces vérifications détectent la substitution d’éléments par rapport à la page fournie ; elles n’établissent pas de confiance envers un serveur compromis capable de remplacer à la fois la page et ses hachages.

**Depuis son lancement, ce journal** combine les journaux de processus avec l’activité de chaque espace de travail : connexions, refus, changements d’itinéraire et actions de l’opérateur. Il s’agit d’une console en mémoire pour le processus en cours, et non d’une copie permanente de chaque message. Les événements fréquents liés aux messages sont conservés dans le journal plutôt que d’encombrer la console.

L'octroi, la modification et la révocation d'accès, ainsi que le démarrage ou la fin de sessions, génèrent également des enregistrements signés dans le journal `access.*`. Les jetons ne figurent pas dans ces enregistrements. Les jetons émis et les identifiants de session sont conservés sous forme de hachages dans le coffre-fort chiffré.

****Administrateur principal et périmètre de confiance**** Le jeton du panneau principal reste sans restriction. Les connexions via un navigateur à l’aide de ce jeton créent des sessions soumises aux limites de session configurées par l’administrateur. Les scripts envoyant le jeton principal directement conservent un accès complet et ne sont pas comptabilisés comme des sessions de navigateur. Il s’agit d’un contrôle d’accès au niveau de l’application au sein d’une même installation. Tous les espaces de travail partagent le processus serveur ; il ne s’agit pas d’une isolation vis-à-vis de l’administrateur de l’hôte. Veillez à préserver la confidentialité du jeton principal, des sessions Telegram, des clés de signature et du répertoire de données. Un jeton « witness » est un identifiant distinct de vérification de l’état de santé du système, et non un jeton d’accès au panneau de contrôle.
