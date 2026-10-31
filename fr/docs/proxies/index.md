# Choisissez un proxy

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/proxies/

Veillez à ce que le compte reste connecté. Déterminez explicitement à quel moment son itinéraire peut utiliser l’adresse du serveur.

## Choisissez d'abord le mode IP

01**Masquer l'adresse IP**

Utilisez un proxy. Si aucun ne fonctionne, patientez sans connexion directe à Telegram.

02**Autoriser une solution de secours**

Autoriser l'accès direct une fois le délai configuré écoulé ; revenir à un proxy opérationnel dès qu'un proxy répond.

03**Tunnel / VPN**

Autorisez les connexions directes via le réseau de l’hébergeur. Cette option n’installe ni ne vérifie aucun VPN.

L'itinéraire détermine la connexion. Le mode IP détermine si une connexion directe est autorisée.

## Laissez le pool gérer l'itinéraire

1. Ouvrez **votre compte → Paramètres → Paramètres de connexion**.
2. Sélectionnez le mode IP et **MTProxy automatique**, ou saisissez un itinéraire fixe.
3. Enregistrez et lancez **le test de connexion à Telegram**. Cela fonctionne également avant la connexion.
4. Une fois la collecte lancée, vérifiez qu’un message de contrôle parvient bien au journal.

Les nouveaux espaces de travail utilisent automatiquement MTProxy avec la fonctionnalité « Hide IP ». Le pool combine quatre sources publiques, teste les entrées, conserve les routes opérationnelles et remplace les proxys défaillants. Les téléchargements ayant échoué conservent les instantanés précédents.

## Utilisez votre propre proxy

Saisissez les paramètres SOCKS5 ou HTTP CONNECT, collez un lien de proxy Telegram pris en charge ou fournissez un catalogue d’opérateurs. Mettez l’observation en pause avant de modifier un itinéraire actif. Les faux secrets TLS MTProxy commençant par `ee` ne sont toujours pas pris en charge.

**Paramètres de rotation, de partage et de nouvelle tentative**

Sous **Paramètres → MTProxy automatique**, définissez les seuils d’échec, les délais d’attente, la rotation planifiée et le nombre de comptes par proxy. Une limite de partage fixée à un oblige un compte à patienter lorsqu’aucune entrée exclusive n’est disponible. Les intervalles de rafraîchissement de la liste et de sondage suivent les valeurs de l’espace de travail principal. Des proxys distincts ne garantissent pas des adresses IP de sortie distinctes.

## Dissocier Telegram des demandes externes

MTProxy achemine uniquement le trafic Telegram. Les horodatages, les notifications, les copies et les vérifications à la source utilisent un proxy SOCKS5/HTTP distinct, la route SOCKS5/HTTP du compte, ou le mode Direct lorsque le mode IP le permet. Ces requêtes externes peuvent être désactivées.

Une configuration explicite « `TGWITNESS_PROXY_FEED_PROXY` » définit l’itinéraire du téléchargeur de flux. Le [témoin indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/witness/) conserve ses propres paramètres. Ces commandes n’installent pas de VPN système et ne redirigent pas le trafic du navigateur.

Consultez [tous les modes, paramètres par défaut et listes de sources](https://phishdestroy.github.io/TgWitness/fr/docs/reference/connection/#ip-modes), ou [choisissez qui est autorisé à modifier l'acheminement d'un compte](https://phishdestroy.github.io/TgWitness/fr/docs/access/).
