# Analyse des archives

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/analysis/

Recherchez des messages enregistrés, examinez les contributions de l'IA et conservez des rapports analytiques accompagnés de leurs références sources.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Investigation](https://phishdestroy.github.io/TgWitness/fr/docs/reference/investigation/)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Guide des procédures](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Utilisez **Journal** pour effectuer une recherche locale sans IA ; [la recherche en texte intégral](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/) (aperçu) reconnaît les formes de mots, les expressions, les domaines et les @noms d'utilisateur. Pour **utiliser** **« Ask the archive »**, commencez par activer et configurer un fournisseur dans **la** **section** **« Intégrations** ». Le sélecteur d'espace de travail permet de choisir le compte ; le formulaire permet de sélectionner les discussions et la période d'observation. La recherche s’effectue localement. Une expression exacte ou un domaine affine la recherche ; un identifiant de message permet de récupérer les versions enregistrées. Passez en revue les extraits et ouvrez leurs entrées de journal ou leur contexte. Il n’y a pas de base de données vectorielle ni d’action automatique sur Telegram.

## Fournisseurs et consentement

L'IA est désactivée par défaut dans chaque espace de travail. Seul l'administrateur principal peut configurer le modèle, le point de terminaison, la clé API chiffrée, les limites de contexte/de sortie, le délai d'expiration et le budget quotidien de requêtes. La clé n'est jamais renvoyée au navigateur. Laissez le champ de la clé vide pour conserver la clé actuelle, ou supprimez-la explicitement.

Ollama utilise son [point de terminaison `/api/chat`](https://docs.ollama.com/api/chat) documenté avec une sortie JSON non en continu. Son adresse par défaut est `http://127.0.0.1:11434` sur le serveur TgWitness. L’opérateur peut la modifier en utilisant `TGWITNESS_AI_LOCAL_ENDPOINT` ; il ne s’agit pas d’une adresse contrôlée par le modèle. Installez vous-même le modèle sélectionné. TgWitness ne le télécharge pas automatiquement.

Le fournisseur compatible doit disposer d’une URL de base se terminant par `/v1` et prendre en charge le [protocole Chat Completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) : `messages` (mode de réponse JSON), `max_completion_tokens` et `choices[0].message.content`. Les services ne disposant pas de ces champs ne sont pas pris en charge. Les tests de connexion envoient du texte synthétique et sont comptabilisés dans le budget de requêtes.

Chaque requête utilise l’itinéraire externe configuré de l’espace de travail. Un itinéraire bloqué ou un MTProxy réservé à Telegram constitue une erreur ; il n’y a pas de nouvelle tentative directe. Une adresse Ollama locale configurée délibérément permet une destination privée. Un point de terminaison IA en boucle fermée nécessite la route externe « Direct » de l’espace de travail ; les routes par proxy sont rejetées avant la transmission. Pour les autres services privés, l’option d’activation de la destination privée au niveau du serveur s’applique. L’aperçu affiche le point de terminaison et la route externe, y compris l’hôte proxy le cas échéant. La modification de cette route nécessite un nouvel aperçu.

Avant la génération, **les données envoyées au modèle** indiquent la requête : question, extraits sélectionnés, types d’événements, heures d’observation et marqueurs de couverture. Les sessions Telegram, les champs bruts, les clés de fournisseur, les octets des pièces jointes et le journal complet ne font pas partie de ce contexte. Décochez les sources indésirables, puis approuvez explicitement le traitement. Les fournisseurs externes peuvent conserver le contenu soumis conformément à leurs propres politiques. L’exécution locale signifie que le point de terminaison est local ; cela ne constitue pas une garantie quant au comportement d’un service configuré de manière indépendante.

Il y a au maximum deux requêtes simultanées auprès du fournisseur au niveau mondial et une par espace de travail. Un aperçu expire au bout de dix minutes et ne peut générer qu’une seule réponse. Les compteurs de jetons déclarés par le fournisseur sont affichés ; une estimation des coûts n’apparaît que lorsque les tarifs d’entrée et de sortie ont tous deux été configurés. Les tentatives infructueuses épuisent également le budget quotidien de requêtes. Aucune nouvelle tentative automatique n’entraîne de dépenses supplémentaires.

## Sources et limites

La recherche utilise l’[index](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#ask-the-archive-and-mcp) [en texte intégral](https://phishdestroy.github.io/TgWitness/fr/docs/reference/search/#ask-the-archive-and-mcp) lorsqu’il est complet : les meilleures correspondances parmi les discussions sélectionnées, y compris les variantes lexicales. Les requêtes concernant les modifications récentes ou les versions d’un message, ainsi que les recherches effectuées pendant la construction de l’index, utilisent une recherche lexicale limitée aux enregistrements les plus récents. L’aperçu indique le nom de la méthode. La recherche renvoie jusqu’à 24 sources ; les textes longs sont tronqués autour de leur correspondance. Les extraits tronqués et les ensembles de résultats incomplets sont signalés. La période fait référence au **temps d’observation** et ne signifie pas que l’historique de Telegram est complet. Les événements couvrant l’ensemble de l’espace de travail sont exclus de l’accès limité au chat. Les données manquantes sont décrites comme « introuvables » dans les archives disponibles.

Le modèle ne reçoit aucun outil. Ses identifiants source sont recoupés avec les enregistrements sélectionnés, les hachages sont revérifiés et les chaînes entre guillemets doivent figurer dans ces enregistrements. Les identifiants inconnus, les citations modifiées et les affirmations non référencées entraînent le rejet de la réponse. L’application crée des liens ; les URL générées par le modèle ne sont pas utilisées comme références. Ces vérifications établissent l’existence de la source et l’exactitude de la citation, et non la véracité d’une déduction. Vérifiez les déductions par rapport aux enregistrements avant de vous y fier.

## Rapports

Enregistrer une réponse validée sous la forme d’un rapport analytique distinct. Celui-ci comprend le résumé du modèle, la chronologie observée, les liens et identifiants extraits, les enregistrements de modifications/suppressions, les limites de couverture et les hachages des événements sources. Le fournisseur, le modèle, le point de terminaison, l’heure et la version du modèle de prompt y sont indiqués. Aucune identité n’est automatiquement fusionnée.

Les révisions et les notes des analystes sont stockées séparément du résumé généré par le modèle. Les rapports sont conservés dans des fichiers dérivés chiffrés, avec un index situé en dehors du flux d’événements signé ; les événements et les médias d’origine ne sont pas modifiés. Seuls le propriétaire ou l’administrateur peuvent ouvrir un rapport, et l’accès à la source est à nouveau vérifié. Le téléchargement nécessite également une autorisation d’exportation. La version 1 ne signe pas les rapports et n’implique pas que les conclusions du modèle constituent des preuves vérifiées. Limites : 100 rapports par espace de travail et 100 révisions d’analystes par rapport.

Pour l'OCR manuel et les transcriptions, voir « [Traitement des médias](https://phishdestroy.github.io/TgWitness/fr/docs/reference/media-analysis/) ». Pour l'accès client, voir « [MCP](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/) ».
