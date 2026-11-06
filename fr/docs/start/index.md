# Commencez en quelques minutes

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/start/

Explorez d’abord la démo, puis connectez votre propre compte.

## Parcourez le site sans créer de compte

Récupérez le projet, ayez **Python 3.11 ou plus récent** et lancez la démo. Le lanceur s’occupe du reste.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

Un espace avec des messages inventés s’ouvre dans le navigateur. Ouvrez un chat, comparez une modification, jetez un œil à un export. Telegram n’intervient pas.

![Affichage d'une conversation dans TgWitness avec des exemples de messages](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Un exemple d'espace de travail. Votre propre journal commence séparément.

## Créez votre propre espace de travail

Fermez la démo, puis :

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Ouvrez l’adresse affichée par le lanceur et collez le **jeton d’accès au panneau** depuis le fichier indiqué. C’est pour TgWitness, pas pour Telegram.

## Enregistrez votre premier message

1. [Connectez un compte Telegram dédié.](https://phishdestroy.github.io/TgWitness/fr/docs/accounts/)
2. Choisissez un groupe ou un canal et lancez l’observation.
3. Envoyez un message dans votre groupe de test et regardez-le apparaître dans le journal.

Pour une installation sur serveur, veuillez suivre les instructions de la section « [Keep it running](https://phishdestroy.github.io/TgWitness/fr/docs/server/) ».
