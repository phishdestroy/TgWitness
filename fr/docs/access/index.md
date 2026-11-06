# Telegram · Partager un cas

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/access/

Partagez les informations dont quelqu’un a besoin. Gardez le contrôle sur le reste.

01**Choisissez les preuves**

Des espaces entiers ou des chats isolés.

02**Choisissez les actions**

Voir, exporter, ou seulement les opérations nécessaires.

03**Définir les limites**

Un jeton personnel avec expiration, limites de session et règles IP si vous le souhaitez.

Le périmètre de collecte détermine ce qui est enregistré. Le périmètre d’accès détermine ce qu’une personne peut voir et faire.

## Accorder un accès à quelqu’un

1. En tant qu’administrateur, ouvrez **Accès**.
2. Nommez-le, choisissez espaces et chats.
3. Un relecteur n’a besoin que de **Voir**. Ajoutez **Exporter** pour les téléchargements.
4. Définissez les limites, puis cliquez sur « **Créer un accès** ».
5. Copiez le jeton (affiché une seule fois) et envoyez-le en privé avec l’adresse du panneau.
6. Vérifiez d’abord ce que la personne verra, dans une session de navigateur séparée.

## Commencez par la mission qu’ils doivent accomplir

| Personne | Accès | Résultat |
| --- | --- | --- |
| Réviseur | Discussions sélectionnées ; consultation uniquement | Lit le chat, ne peut rien changer. |
| Analyste | Discussions sélectionnées ; consultation et exportation | Lit et télécharge ce dont l’affaire a besoin. |
| Opérateur | Espaces de travail complets sélectionnés ; sources et collecte | Décide de ce qui est observé, démarre et arrête les collecteurs. |

Ce ne sont que des exemples, pas des rôles figés. Un accès limité à des chats n’obtient jamais les paramètres du compte ni d’exports complets du journal. L’accès à tous les espaces inclut les comptes ajoutés plus tard.

## Vous pouvez changer d'avis à tout moment

Modifiez l’accès quand vous voulez, c’est effectif dès la requête suivante. Terminez une session ou révoquez tout. Les fichiers déjà téléchargés sont perdus pour de bon. La collecte continue.

**Limites de sessions et d'adresses IP**

Limitez les sessions parallèles et les connexions, fixez une date de fin, autorisez des IP ou sous-réseaux ou liez l’accès à l’IP de la première connexion. L’expiration compte l’inactivité ; un panneau ouvert compte comme actif. Derrière un proxy, vérifiez quelle IP client l’application voit.

**La clé principale et le journal d'activité**

Le jeton principal reste chez l’administrateur. Un accès émis ne peut ni gérer l’accès des autres ni ouvrir la console d’administration. Les changements d’accès et les sessions sont signés dans le journal, sans les jetons. L’administrateur du serveur voit toujours tout.

Les sept droits et les règles de session : [référence des accès](https://phishdestroy.github.io/TgWitness/fr/docs/reference/access/).
