# Telegram · Connecter un compte

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/accounts/

Un espace = un compte, son journal et sa clé.

## Choisissez votre mode de connexion

**Comptes** → ajouter un espace → paramètres de connexion. Utilisez un compte séparé pour cela.

- **Code QR :** scannez-le depuis l’écran Appareils de Telegram et confirmez.
- **Numéro de téléphone :** numéro, code, puis mot de passe 2FA si vous en avez un.
- **Import de session :** votre propre fichier de session ou vos données Telegram Desktop.

Utilisez un profil d’API intégré ou votre propre API ID et hash. Il identifie seulement l’application : il ne vous connecte pas et ne cache rien.

**Avez-vous d'abord besoin d'un proxy ?**

Vous pouvez [choisir et tester l'itinéraire de connexion](https://phishdestroy.github.io/TgWitness/fr/docs/proxies/) avant de vous connecter. Chaque compte dispose de son propre itinéraire.

## Choisissez ce que vous souhaitez surveiller

1. Choisissez les chats, groupes ou canaux dont vous avez besoin.
2. Vérifiez les paramètres de collecte, médias compris.
3. Démarrez et vérifiez la connexion et l’activité récente.

Le compte doit avoir accès. Admins et membres ne voient pas la même chose ; le journal montre ce que ce compte a reçu.

Le compte entier ? **Sources → Périmètre d’observation → Mode enquête**, vérifiez puis **Enregistrer le périmètre**. Guide complet : [enquêter sur un compte entier](https://phishdestroy.github.io/TgWitness/fr/docs/cases/).

## Vérifiez l'intégralité du chemin d'accès

Dans votre groupe de test, envoyez un message depuis un autre compte, modifiez-le, supprimez-le. Les trois événements doivent apparaître dans le journal. Ensuite, [exportez et vérifiez](https://phishdestroy.github.io/TgWitness/fr/docs/exports/).

« Connecté » signifie que la connexion fonctionne. Un message de test capturé signifie que les événements arrivent vraiment.

## Ajouter un autre compte

Nouvel espace dans **Comptes**, mêmes étapes. Notez l’empreinte de clé de chaque compte pour distinguer les exports plus tard.
