# Discussions secrètes : implémentation et démonstration

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/secret-chats/

Comprendre la mise en œuvre distincte des Secret Chats, tester l’interface fictive et passer en revue les défauts en suspens.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

**État vérifié le 6 novembre 2026 :** une implémentation distincte des Secret Chats est en cours de développement. Elle n’a pas été fusionnée dans la branche publiée `main` à la version `3d23e52b647b`. Le collecteur standard et l’exportation Takeout ne collectent pas les Secret Chats. Le scénario du site web interactif présente l’interface à l’aide de données fictives ; il ne permet pas la communication via Telegram.

## Où se trouve l'implémentation

Commit `0e60f88e` a ajouté **Sources → Pseudo-secret** dans la branche de développement locale `fix/panel-routes-sessions`. L'instantané vérifié est `bb8788fb685c`. Son implémentation comprend `tgwitness/secret_chats.py`, les routes d'application, `tgwitness/static/views/secret-chats.js` et des tests dédiés.

L'extension optionnelle `secret-chats` de cette branche utilise [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat), épinglée à `d87bf037b90060383c7b704d8a06ebb98c621c6f`. La bibliothèque implémente le protocole de chat de bout en bout de Telegram sur l'autorisation Telethon existante du compte. L'installation de cette bibliothèque seule n'ajoute pas l'intégration manquante à `main`.

## Fonctionnalités de l'interface de développement

| Action | Comportement enregistré |
| --- | --- |
| Lancer une conversation par nom d'utilisateur ou identifiant utilisateur | Envoyez une demande ; l'autre participant doit l'accepter. |
| Accepter une requête entrante | TgWitness devient le point de terminaison de réception pour cette conversation. L'acceptation automatique est un paramètre distinct, désactivé par défaut. |
| Envoyer ou recevoir un message | Ajouter un enregistrement `secret_chat.message` sortant ou entrant et l'afficher dans le fil de discussion. |
| Recevoir une pièce jointe | Le déchiffrer, stocker ses octets selon SHA-256 et enregistrer `secret_chat.file`. |
| Recevoir un rappel de délai ou un avis de suppression | Enregistrer la notification et conserver le contenu précédemment capturé. |
| Passer en revue la conversation | Afficher les messages, les fichiers, les notifications et la visualisation des clés. L'onglet ouvert s'actualise toutes les quatre secondes. |

Dans une version de développement intégrant cette fonctionnalité, l’opérateur active le module pour le compte sélectionné et le connecte. Le lancement, l’acceptation et l’envoi nécessitent une autorisation d’interaction et la désactivation de la protection en lecture seule du compte. L’autre participant doit accepter une nouvelle conversation sortante. Ces contrôles ne sont pas présents dans l’ application publiée à la version mentionnée ci-dessus.

Seules les discussions créées ou acceptées par cette session TgWitness sont prises en compte. Les discussions secrètes existantes sur un téléphone restent sur cet appareil. L’importation d’une session ne fournit pas leurs clés de chiffrement distinctes. Les clés et les compteurs des discussions secrètes sont stockés dans le coffre-fort de l’espace de travail ; les messages conservés et les fichiers déchiffrés sont soumis aux protections habituelles du stockage de l’espace de travail.

## Démonstration sur le site web

Le scénario « **Try Secret Chat** » du site web présente une conversation fictive. Il permet au lecteur de lancer une requête, de simuler son acceptation, d’envoyer un message d’exemple, de recevoir une réponse et un fichier prédéfinis, ainsi que d’examiner un compte à rebours et un avis de suppression. Une requête entrante peut également être acceptée. Les commandes indiquent explicitement les actions simulées des pairs.

Ce scénario s'exécute dans la mémoire du navigateur. Une réinitialisation ou un rafraîchissement de la page l'efface. Il ne se connecte pas, ne contacte pas Telegram, ne crée pas de véritables clés de chiffrement et ne modifie pas les téléchargements d'échantillons signés. Les messages affichés ne constituent pas des preuves signées. Le scénario illustre l'interaction prévue ; il ne certifie pas que la mise en œuvre du développement est prête.

## Vérifications et défauts en suspens

Les cinq tests existants portent sur la persistance des clés chiffrées, le cycle de vie et les enregistrements de messages, la politique d’acceptation des messages entrants, l’envoi en lecture seule et l’exportation des pièces jointes. Ils ont été validés par rapport à la bibliothèque épinglée lors de la révision du 6 novembre. Trois vérifications synthétiques supplémentaires ont reproduit des défauts dans le même instantané :

| Constat | Conséquence |
| --- | --- |
| La fermeture contourne `read_only` | La fonction Fermer peut déclencher une action à distance lorsque les interactions doivent être bloquées. |
| La détection des doublons porte uniquement sur les enregistrements récents de type 500. | Une rediffusion plus ancienne peut créer un doublon après le redémarrage. |
| Un téléchargement d'une pièce jointe ayant échoué supprime son entrée en attente | Une défaillance temporaire entraîne la perte de la tâche de nouvelle tentative. |

Il s’agit de défauts avérés, également consignés dans l’audit [publié](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md). Les cinq tests réussis ne couvrent pas ces défaillances. L’examen a utilisé des espaces de travail synthétiques et simulé des opérations Telegram ; il n’a pas reproduit de procédure d’authentification en conditions réelles ni évalué le déploiement en production.
