# Connecter un compte

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/accounts/

Un espace de travail contient un compte, son journal et sa clé de signature.

## Choisissez votre mode de connexion

Créez **des comptes**, ajoutez un espace de travail et ouvrez ses paramètres de connexion. Utilisez un compte dédié à l'observation.

- **Code QR :** scannez-le depuis les paramètres de votre appareil Telegram et confirmez la nouvelle connexion.
- **Numéro de téléphone :** saisissez le numéro, le code envoyé par Telegram et votre mot de passe de vérification en deux étapes s’il est activé.
- **Importation de session :** importez une session prise en charge ou des données de Telegram Desktop vous appartenant.

Choisissez un profil API intégré ou saisissez votre propre identifiant API et votre propre hachage. Un profil API identifie le client ; il ne permet pas de se connecter à un compte ni de rendre la connexion anonyme.

**Avez-vous d'abord besoin d'un proxy ?**

Vous pouvez [choisir et tester l'itinéraire de connexion](https://phishdestroy.github.io/TgWitness/fr/docs/proxies/) avant de vous connecter. Chaque compte dispose de son propre itinéraire.

## Choisissez ce que vous souhaitez surveiller

1. Ouvrez la liste des sources et sélectionnez les discussions, groupes ou chaînes dont vous avez besoin.
2. Vérifiez les paramètres de collecte, y compris ceux relatifs aux fichiers multimédias, avant de commencer la surveillance.
3. Lancez le collecteur et vérifiez sa connexion ainsi que son activité récente.

Le compte doit pouvoir accéder à la source. Selon leur rôle, les utilisateurs peuvent voir des événements différents ; le journal reflète ce que ce compte a reçu.

Pour une enquête portant sur l’intégralité du compte, utilisez **Sources → Portée de l’observation → Mode enquête**, vérifiez les paramètres, puis cliquez sur « **Enregistrer la portée** ». Le [guide complet de l’enquête](https://phishdestroy.github.io/TgWitness/fr/docs/cases/) couvre tous les types de discussions visibles, l’historique ancien, les profils des utilisateurs, les références entre discussions et le transfert des preuves.

## Vérifiez l'intégralité du chemin d'accès

Dans un groupe de test que vous contrôlez, envoyez un message unique depuis un autre compte, modifiez-le puis supprimez-le. Vérifiez que ces trois événements apparaissent bien dans le journal, puis [exportez et vérifiez](https://phishdestroy.github.io/TgWitness/fr/docs/exports/) l'enregistrement.

Un statut « connecté » confirme la connexion. Un message de test capturé confirme qu’un événement particulier a bien été transmis à cet espace de travail.

## Ajouter un autre compte

Créez un autre espace de travail dans **la section « Comptes »** et répétez la configuration. Conservez l’empreinte de la clé de signature de chaque compte afin de pouvoir identifier ses exportations ultérieurement.
