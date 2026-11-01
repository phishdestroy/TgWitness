# Webhooks sortants

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/webhooks/

Envoi d’événements ciblés vers des destinataires HTTPS avec signatures HMAC, tentatives de réenvoi et suivi de la livraison.

[Guide des procédures](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Ouvrez « **Intégrations » → « Webhooks sortants »** dans l’espace de travail sélectionné. Ajoutez un récepteur HTTPS, choisissez les événements « collector/media/export » et, si vous le souhaitez, sélectionnez les discussions pour les nouvelles observations et les modifications. Le texte des messages est désactivé par défaut. L’activation des extraits ajoute au maximum 1 000 caractères aux événements de modification de message ; les champs bruts de Telegram et les identifiants ne sont jamais envoyés.

Copiez une seule fois la clé secrète HMAC dans la configuration protégée du récepteur. Elle est chiffrée dans le coffre-fort de TgWitness et ne peut pas être récupérée depuis le panneau de configuration. Supprimez et recréez une destination pour la faire tourner. **Envoyez** aux files d’attente **de test synthétiques** un test sans contenu de discussion ; actualisez le statut de livraison pour voir le résultat.

La mise en œuvre étend la boucle de notification existante en complément d’Apprise. Elle utilise la route externe de l’espace de travail et les restrictions existantes relatives aux destinations privées. Il n’y a ni solution de secours directe ni redirection. Les URL ne doivent pas contenir d’identifiants, de chaînes de requête ni de fragments ; les adresses privées nécessitent une activation au niveau du serveur, et non un paramètre que l’utilisateur du panneau peut contourner.

## Données utiles et signature

Schéma : [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Chaque charge utile contient `event_id`, `timestamp`, `workspace`, `type`, `synthetic` et des compteurs. Les événements consignés dans le journal incluent leur séquence et leur hachage. L'achèvement de l'exportation complète et les tests synthétiques constituent des événements de livraison, sans référence inventée au journal signé. Les notifications de suppression de Telegram et `missing_on_recheck` restent des types distincts.

L'en-tête `X-TgWitness-Signature` est `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`. Calculez le HMAC sur les octets exacts `timestamp + "." + raw_request_body`, en utilisant le secret affiché sous forme d'octets UTF-8. Comparez les signatures en temps constant avant d'analyser ou de traiter le corps du message. Rejetez les horodatages s'écartant de plus de cinq minutes de votre horloge. L'horodatage est actualisé à chaque tentative de livraison.

Utilisez `event_id` comme clé d’idempotence dans un stockage durable, avec une contrainte d’unicité atomique avant les effets secondaires. Une signature valide ne suffit pas à elle seule à empêcher la reproduction d’une requête récente. Conservez les identifiants traités au moins pendant toute la durée de la fenêtre de réessai ; conservez-les plus longtemps si le destinataire peut retraiter les événements stockés.

## Nouvelles tentatives

Les livraisons sont mises en file d’attente de manière durable avant les requêtes HTTP. Elles utilisent la sémantique « au moins une fois » : une confirmation perdue ou un redémarrage peut entraîner la livraison d’un événement à nouveau avec le même identifiant. Il y a huit tentatives avec un délai d’attente exponentiel, commençant à 15 secondes et plafonné à une heure. Une réponse 2xx est nécessaire pour que l’opération soit considérée comme réussie. Les tâches épuisées laissent une erreur visible ; la transmission n’est pas garantie une fois les tentatives de réessai terminées.

La file d’attente peut contenir 1 000 envois. Lorsqu’elle est pleine, l’analyse des événements du journal est mise en pause et reprend dès que de l’espace est disponible. Une exportation complète qui ne peut pas être mise en file d’attente génère une erreur de file d’attente visible. Jusqu’à cinq tentatives d’envoi sont effectuées par cycle de notification , et les 100 derniers enregistrements de tentatives sont conservés. La suppression d’une destination entraîne également la suppression de ses envois en attente.

## Exemple n8n

Importez [l'exemple de workflow](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json). Il est inactif et ne contient aucune information confidentielle ni aucune action en aval. Définissez `TGWITNESS_WEBHOOK_SECRET` dans l’environnement du worker n8n, autorisez l’accès à cet environnement et autorisez la fonction intégrée `crypto` pour le nœud Code. L’exemple utilise l’option raw-body du nœud Webhook, vérifie la signature et la fraîcheur des données, et accuse réception des événements validés. Cela correspond à l’[implémentation documentée](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts) du nœud.

Avant d’ajouter des écritures ou des notifications SIEM, ajoutez un stockage idempotent durable indexé par `event_id`. Limitez la modification des workflows n8n et la conservation des journaux d’exécution en fonction des données que vous avez choisi d’envoyer. TgWitness n’ajoute aucune commande entrante.
