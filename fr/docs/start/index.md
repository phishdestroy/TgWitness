# Commencez en quelques minutes

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/start/

Commencez par découvrir un exemple concret. Connectez ensuite votre propre compte.

## Parcourez le site sans créer de compte

Téléchargez ou clonez le projet, installez **Python 3.11 ou une version ultérieure**, puis lancez la démo. Le programme de lancement crée un environnement local et installe les dépendances requises.

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

Le navigateur ouvre un espace de travail contenant des messages fictifs. Ouvrez une conversation, comparez une modification et examinez un fichier exporté. Le mode démo ne se connecte pas à Telegram.

![Affichage d'une conversation dans TgWitness avec des exemples de messages](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Un exemple d'espace de travail. Votre propre journal commence séparément.

## Créez votre propre espace de travail

Fermez la procédure de démonstration, puis utilisez le lanceur habituel :

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Ouvrez l'adresse locale indiquée par le lanceur. Si vous y êtes invité, saisissez le **jeton d'accès au panneau** à partir du fichier local dont le nom s'affiche dans le terminal. Cela déverrouille TgWitness ; cette procédure est distincte de la connexion à Telegram.

## Enregistrez votre premier message

1. [Connectez un compte Telegram dédié.](https://phishdestroy.github.io/TgWitness/fr/docs/accounts/)
2. Sélectionnez un groupe ou une chaîne auquel le compte a accès, puis lancez la surveillance.
3. Envoyez un nouveau message dans un groupe de test que vous contrôlez et vérifiez qu’il apparaît bien dans le journal.

Pour une installation sur serveur, veuillez suivre les instructions de la section « [Keep it running](https://phishdestroy.github.io/TgWitness/fr/docs/server/) ».
