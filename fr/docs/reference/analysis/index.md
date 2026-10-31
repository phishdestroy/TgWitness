# Analyse des archives

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/analysis/

Recherchez des messages enregistrés, examinez les contributions de l'IA et conservez des rapports analytiques accompagnés de leurs références sources.

**Point important :** utilisez une version de la source ; la version préliminaire portable 0.7.0 est antérieure à cette fonctionnalité.

[Guide des procédures](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Ouvrez **« Ask the archive »** dans le panneau. Le sélecteur d’espace de travail permet de choisir le compte ; le formulaire permet de sélectionner les discussions et la période d’observation. La recherche s’effectue localement, sans IA. Une expression exacte ou un domaine permet d’affiner les résultats ; un identifiant de message permet de récupérer les versions enregistrées. Passez en revue les extraits renvoyés et ouvrez leurs entrées de journal ou leur contexte. Il n’y a ni base de données vectorielle ni action automatique sur Telegram.

## Fournisseurs et consentement

L'IA est désactivée par défaut dans chaque espace de travail. Seul l'administrateur principal peut configurer le modèle, le point de terminaison, la clé API chiffrée, les limites de contexte/de sortie, le délai d'expiration et le budget quotidien de requêtes. La clé n'est jamais renvoyée au navigateur. Laissez le champ de la clé vide pour conserver la clé actuelle, ou supprimez-la explicitement.

Ollama utilise son [point de terminaison `/api/chat`](https://docs.ollama.com/api/chat) documenté avec une sortie JSON non en continu. Son adresse par défaut est `http://127.0.0.1:11434` sur le serveur TgWitness. L’opérateur peut la modifier en utilisant `TGWITNESS_AI_LOCAL_ENDPOINT` ; il ne s’agit pas d’une adresse contrôlée par le modèle. Installez vous-même le modèle sélectionné. TgWitness ne le télécharge pas automatiquement.

Le fournisseur compatible doit disposer d’une URL de base se terminant par `/v1` et prendre en charge le [protocole Chat Completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create) : `messages` (mode de réponse JSON), `max_completion_tokens` et `choices[0].message.content`. Les services ne disposant pas de ces champs ne sont pas pris en charge. Les tests de connexion envoient du texte synthétique et sont comptabilisés dans le budget de requêtes.

Chaque requête utilise la route externe configurée pour l'espace de travail. Une route bloquée ou un MTProxy réservé à Telegram génère une erreur ; il n’y a pas de nouvelle tentative directe. Une adresse Ollama locale configurée délibérément permet une destination privée, tout en continuant à utiliser la route choisie. Pour les autres services privés, l’option d’activation de la destination privée au niveau du serveur s’applique. Le panneau affiche le point de terminaison effectivement configuré.

Avant la génération, **les données envoyées au modèle** indiquent la requête : question, extraits sélectionnés, types d’événements, heures d’observation et marqueurs de couverture. Les sessions Telegram, les champs bruts, les clés de fournisseur, les octets des pièces jointes et le journal complet ne font pas partie de ce contexte. Décochez les sources indésirables, puis approuvez explicitement le traitement. Les fournisseurs externes peuvent conserver le contenu soumis conformément à leurs propres politiques. L’exécution locale signifie que le point de terminaison est local ; cela ne constitue pas une garantie quant au comportement d’un service configuré de manière indépendante.

Il y a au maximum deux requêtes simultanées auprès du fournisseur au niveau mondial et une par espace de travail. Un aperçu expire au bout de dix minutes et ne peut générer qu’une seule réponse. Les compteurs de jetons déclarés par le fournisseur sont affichés ; une estimation des coûts n’apparaît que lorsque les tarifs d’entrée et de sortie ont tous deux été configurés. Les tentatives infructueuses épuisent également le budget quotidien de requêtes. Aucune nouvelle tentative automatique n’entraîne de dépenses supplémentaires.

## Sources et limites

La fonction de recherche examine le texte des messages enregistrés à l’aide d’une recherche lexicale délimitée. Elle renvoie jusqu’à 24 sources et signale les extraits tronqués ou les ensembles de résultats incomplets. La période fait référence au **temps d’observation** et ne signifie pas que l’historique Telegram est complet. Les événements couvrant l’ensemble de l’espace de travail sont exclus de l’accès limité aux discussions. Les données manquantes sont signalées comme « introuvables » dans les archives disponibles.

Le modèle ne reçoit aucun outil. Ses identifiants source sont recoupés avec les enregistrements sélectionnés, les hachages sont revérifiés et les chaînes entre guillemets doivent figurer dans ces enregistrements. Les identifiants inconnus, les citations modifiées et les affirmations non référencées entraînent le rejet de la réponse. L’application crée des liens ; les URL générées par le modèle ne sont pas utilisées comme références. Ces vérifications établissent l’existence de la source et l’exactitude de la citation, et non la véracité d’une déduction. Vérifiez les déductions par rapport aux enregistrements avant de vous y fier.

## Rapports

Enregistrer une réponse validée sous la forme d’un rapport analytique distinct. Celui-ci comprend le résumé du modèle, la chronologie observée, les liens et identifiants extraits, les enregistrements de modifications/suppressions, les limites de couverture et les hachages des événements sources. Le fournisseur, le modèle, le point de terminaison, l’heure et la version du modèle de prompt y sont indiqués. Aucune identité n’est automatiquement fusionnée.

Les révisions et les notes des analystes sont stockées séparément du résumé généré par le modèle. Les rapports sont conservés dans des fichiers dérivés chiffrés, avec un index situé en dehors du flux d’événements signé ; les événements et les médias d’origine ne sont pas modifiés. Seuls le propriétaire ou l’administrateur peuvent ouvrir un rapport, et l’accès à la source est à nouveau vérifié. Le téléchargement nécessite également une autorisation d’exportation. La version 1 ne signe pas les rapports et n’implique pas que les conclusions du modèle constituent des preuves vérifiées. Limites : 100 rapports par espace de travail et 100 révisions d’analystes par rapport.

Pour l'OCR manuel et les transcriptions, voir « [Traitement des médias](https://phishdestroy.github.io/TgWitness/fr/docs/reference/media-analysis/) ». Pour l'accès client, voir « [MCP](https://phishdestroy.github.io/TgWitness/fr/docs/reference/mcp/) ».
