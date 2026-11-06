# Telegram · Choisissez un proxy

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/proxies/

Gardez le compte en ligne et décidez vous-même s’il peut un jour montrer l’IP de votre serveur.

## Choisissez d'abord le mode IP

01**Masquer l'adresse**

Proxy uniquement. Si aucun ne marche, il attend.

02**Recourir à Direct en dernier recours**

Passe en direct après un délai, revient à un proxy dès qu’un fonctionne.

03**Serveur derrière un tunnel ou un VPN**

Le direct est permis. Ce mode ne configure ni ne vérifie le VPN à votre place.

L'itinéraire détermine la connexion. Le mode IP détermine si une connexion directe est autorisée.

## Laissez le pool gérer l'itinéraire

1. **Compte → Paramètres → Paramètres de connexion**.
2. Choisissez le mode IP et **MTProxy automatique**, ou un itinéraire fixe.
3. Enregistrez, puis **Tester la connexion Telegram** (fonctionne aussi avant la connexion).
4. Lancez la collecte et envoyez-vous un message de test.

Les nouveaux espaces démarrent en MTProxy automatique avec **Masquer l’adresse**. Le pool utilise quatre listes publiques, teste les serveurs, garde les bons et remplace ceux qui sont tombés.

## Utilisez votre propre proxy

SOCKS5, HTTP CONNECT, un lien de proxy Telegram ou un catalogue d’opérateur. Mettez l’observation en pause avant de changer. Les secrets Fake TLS (`ee`…) ne fonctionnent pas.

**Paramètres de rotation, de partage et de nouvelle tentative**

**Paramètres → MTProxy automatique** : seuils d’échec, temps de pause, rotation, comptes par proxy. Une limite de 1 signifie qu’un compte attend plutôt que de partager. Des proxys différents peuvent quand même partager la même IP de sortie.

## Dissocier Telegram des demandes externes

MTProxy ne transporte que Telegram. Horodatages, notifications, copies et vérifications de code passent par un proxy SOCKS5/HTTP séparé, l’itinéraire SOCKS5/HTTP du compte ou en direct si le mode le permet. Ou désactivez-les.

`TGWITNESS_PROXY_FEED_PROXY` définit l’itinéraire de téléchargement des listes. Le [témoin](https://phishdestroy.github.io/TgWitness/fr/docs/witness/) a ses propres paramètres. Rien de tout cela ne touche votre navigateur ni le réseau du système.

Plus : [modes et valeurs par défaut](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/#ip-modes), [qui peut changer les itinéraires](https://phishdestroy.github.io/TgWitness/fr/docs/access/).
