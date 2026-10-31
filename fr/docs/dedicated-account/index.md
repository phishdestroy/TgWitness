# Utilisez un compte distinct. Jamais votre compte principal.

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/dedicated-account/

À lire avant de connecter un compte

Notre conseil de ne pas utiliser votre compte principal n’est pas une plaisanterie. C’est une réalité.

Compte principal

- Hash de votre propre application : 99 % déconnectés
- Les suspensions motivées uniquement par un faible niveau de confiance sont fréquentes
- L’utiliser est une idée vraiment stupide

Compte supplémentaire sur les paires publiques

- Plus d’un million de comptes ont été enregistrés via ces paires
- Ces paires sont en service depuis plus de 5 ans
- Personne ne peut voir quoi que ce soit vous concernant par leur intermédiaire

01

## Pourquoi pas votre compte principal ?

Ces informations sont exactes. Nous savons exactement où se situent les écueils liés à ces problèmes.

1. ### Hash de votre propre application : 99 % déconnectés

   Se connecter à my.telegram.org à partir d’un compte auquel vous n’avez pas accès, afin d’obtenir un hachage d’application, puis effectuer toute requête via ce hachage d’application, signifie qu’il y a 99 % de chances que le compte soit déconnecté. Vous pouvez le vérifier.
2. ### Les suspensions motivées uniquement par un faible niveau de confiance sont fréquentes

   Les comptes sont bannis simplement parce que Telegram ne leur fait pas confiance, et ces interdictions sont fréquentes. Vous pouvez également vérifier cela. Utiliser votre propre compte est une idée vraiment stupide.
3. ### Les clés de session copiées peuvent être révoquées

   L'exécution simultanée d'une clé TData/session importée dans Telegram Desktop et TgWitness peut déclencher l'erreur `AUTH_KEY_DUPLICATED`. Telegram invalide cette autorisation ; les deux copies doivent donc s'identifier à nouveau. Un compte dédié n'empêche pas cela.

   Quittez complètement le client d’origine et laissez-le fermé pendant que vous utilisez sa session importée. Pour une utilisation en parallèle, connectez-vous à TgWitness par téléphone ou via un code QR afin de créer une autorisation distincte ; les autres clients disposant d’une autorisation distincte peuvent rester connectés.

   [Veuillez lire l’avertissement relatif à l’importation de session](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=fr#session-warning)

Documentation Telegram

- [Erreurs de déconnexion : AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [Créer le hachage de votre propre application : obtenir l’api_id](https://core.telegram.org/api/obtaining_api_id)

02

## Pourquoi TgWitness fonctionne grâce à des paires publiques de hachage d’application/ID d’application

C’est pourquoi nous avons conçu TgWitness sur la base de paires publiques « hachage d’application/identifiant d’application ». Selon notre raisonnement, celles-ci réduisent le risque de suspension : plus d’un million de comptes Telegram ont été enregistrés via ces paires, et de nombreux programmes différents fonctionnent grâce à elles. Selon notre raisonnement, cette approche est préférable à l’utilisation directe d’un hachage d’application personnel : ces paires existent bel et bien depuis plus de 5 ans.

### Votre nouvelle paire

Créé sur my.telegram.org à partir du compte.

- Environ 99 % des comptes se sont déconnectés
- Une nouvelle application, un seul compte

### Paires publiques du pool

Les mêmes paires que celles utilisées par de nombreux programmes.

- Plus d’un million de comptes enregistrés
- De nombreux programmes différents
- Plus de 5 ans d’expérience

### Pourquoi personne ne peut voir quoi que ce soit de ce qui vous concerne grâce à ces paires

- #### La paire est un nom, et non une clé

  Telegram demande l’identifiant API et le hachage API lorsqu’un programme se connecte et lorsqu’il demande un code de connexion. Ceux-ci identifient l’application et ne donnent accès à aucun compte ; la documentation de Telethon précise qu’une seule paire fonctionne avec n’importe quel numéro de téléphone.
- #### Votre clé de session ne quitte jamais votre serveur

  La connexion crée une clé d’autorisation via un échange Diffie-Hellman entre votre TgWitness et Telegram ; la clé elle-même n’est jamais transmise. Documentation de Telegram : après l’autorisation, la clé est associée à l’utilisateur, et chaque appel utilisant cette clé s’exécute au nom de cet utilisateur. Les autres programmes disposant de la même paire de clés possèdent leurs propres clés et ne peuvent pas utiliser la vôtre.
- #### Le trafic est chiffré à l’aide de votre clé

  Chaque requête et chaque réponse sont chiffrées à l’aide de la clé d’autorisation de la session, et non à l’aide du hachage de l’API. La connaissance du hachage de l’API ne permet de déchiffrer aucune donnée.
- #### Le propriétaire d’une paire ne voit rien

  Telegram ne dispose d’aucune méthode permettant de répertorier les comptes, les sessions ou les messages par identifiant API. Le propriétaire d’une paire ne voit que les paramètres de son application sur my.telegram.org.
- #### Seul votre compte peut identifier de quelle application il s’agit

  La rubrique « Paramètres → Appareils » de votre propre compte répertorie pour chaque session le nom de l’application et l’identifiant API, l’appareil, l’adresse IP et les dates. Personne d’autre n’a accès à cette liste.

Documentation Telegram

- [Autorisation de l’utilisateur : la clé devient l’utilisateur](https://core.telegram.org/api/auth)
- [auth.sendCode : api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [Création d’une clé d’autorisation](https://core.telegram.org/mtproto/auth_key)
- [Chiffrement MTProto](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [Contenu d’un enregistrement de session](https://core.telegram.org/constructor/authorization)
- [Obtention de l’api_id](https://core.telegram.org/api/obtaining_api_id)
- [Code source ouvert des applications Telegram](https://telegram.org/apps#source-code)

Bibliothèques et discussions

- [Téléthon : connexion](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele : API de l’application officielle](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele : TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow : l’api_hash doit-il rester confidentiel ?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### Les mêmes paires dans d’autres programmes7

Les paires d’applications Telegram officielles sont publiques et intégrées à de nombreux programmes et bibliothèques indépendants :

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  Liste sur le forum des paires d’applications officielles, publiée pour l’enregistrement des comptes

03

## Méthodes pour créer un compte supplémentaire

Un compte Telegram nécessite un numéro de téléphone sur lequel le code de connexion est envoyé. Choisissez-le en fonction de la durée de vie prévue du compte.

- Meilleur choix

  ### Carte SIM prépayée ou eSIM

  ********

  Derniers éléments

  À condition de veiller à ce qu’il reste toujours approvisionné

  Attention

  Le plus fiable : Telegram accepte de préférence les numéros de téléphone mobile réels. Un numéro réattribué par l’opérateur est attribué à quelqu’un d’autre.
- ### Application de numéros virtuels

  ********

  Derniers éléments

  Bien que l’application conserve le nombre

  Attention

  Telegram peut refuser un numéro virtuel, ne pas envoyer le code ou limiter d’emblée le nouveau compte ; certaines applications récupèrent les numéros qui ne sont pas utilisés.
- ### Location de numéros

  ********

  Derniers éléments

  La durée de location

  Attention

  Une fois ce numéro épuisé, il revient au client suivant.
- ### Activation unique

  ********

  Derniers éléments

  Un code

  Attention

  Le numéro revient immédiatement dans le pool, souvent accompagné de l’historique de ses anciens propriétaires. Définissez le mot de passe du cloud avant toute autre chose.

Toute personne détenant ce numéro par la suite peut demander un code de connexion. Un mot de passe cloud (vérification en deux étapes) l’empêche de se connecter ; sans celui-ci, le compte revient au prochain détenteur du numéro.

Documentation Telegram

- [FAQ sur le spam : numéros virtuels et anciens propriétaires](https://telegram.org/faq_spam)
- [Vérification en deux étapes](https://core.telegram.org/api/srp)

### Numéros +888 loués (Fragment)

Certaines places de marché et certains services proposent la location temporaire des numéros officiels +888 de Telegram via Fragment.

Prix approximatif : 20 dollars américains par jour.

- Vous pouvez créer un compte directement sur Telegram Web ou Telegram Desktop.
- Vous pouvez supprimer les comptes associés à ce numéro et en créer de nouveaux.
- Ces comptes font généralement l’objet de moins de contrôles anti-fraude, mais ils ne confèrent ni immunité ni privilèges particuliers.

Ce numéro ne vous appartient pas. À l’issue de la location, le propriétaire pourra le récupérer. Définissez immédiatement un mot de passe « cloud » et ne considérez pas ce compte comme un compte à long terme.

Il est plus fiable de posséder vous-même le numéro +888 ou d’utiliser une carte SIM prépayée que vous contrôlez.

### Comptes prêts à l’emploi provenant de places de marché

Certaines plateformes (par exemple G2G ou Z2U) vendent des comptes Telegram prêts à l’emploi — neufs, anciens ou accompagnés de fichiers de session.

- [G2G : annonces de comptes Telegram](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U : annonces de comptes Telegram](https://www.z2u.com/telegram/accounts-5-15140)

N’UTILISEZ JAMAIS VOTRE COMPTE PRINCIPAL ! Un compte dédié obtenu de cette manière reste plus sûr que d’enregistrer votre compte Telegram principal dans TgWitness.

#### Avertissements avant l’achat

- Cela constitue une violation des Conditions d’utilisation de Telegram.
- De nombreux comptes ont été créés en masse (inscription automatique) ou présentent un historique inconnu.
- Certains vendeurs peuvent encore disposer d’un accès de récupération.
- Les comptes provenant de ces marchés sont souvent bannis ou soumis à des restrictions par la suite.
- Évitez les plateformes qui vendent ouvertement des logiciels de piratage, des outils de hameçonnage ou des comptes manifestement volés.
- L’achat d’un compte — même s’il est présenté comme « à inscription automatique » — sur des plateformes qui vendent ouvertement des outils de phishing, des logiciels de vol de données, des sessions piratées ou des comptes volés enfreint non seulement les Conditions d’utilisation de Telegram, mais également la législation de la plupart des pays. Cela peut par la suite invalider vos preuves. Faites preuve de prudence dans votre choix.

#### Si vous utilisez cette option

1. Considérez ce compte comme jetable.
2. Mettez fin à toutes les autres sessions, définissez un mot de passe « cloud » et modifiez immédiatement les méthodes de récupération.
3. Utilisez 2 à 3 comptes provenant de différents fournisseurs ou que vous avez créés vous-même.

**Premium, suppression et délai de sept jours**

Si le compte dispose de l’abonnement Premium, une personne ayant accès au numéro de téléphone ne peut pas supprimer le compte immédiatement. Vous recevez une notification et disposez d’un délai de sept jours avant la suppression.

C’est important car votre enquête dépend de ce compte : vous avez le temps de préparer un compte de remplacement.

**Comptes récents et identifiants API**

Si vous obtenez et utilisez votre propre api_id/api_hash à partir d’un nouveau compte que vous avez vous-même créé à l’aide d’un numéro issu d’un service SMS, le compte sera déconnecté dès la première requête API ou autorisation de session. Gardez cela à l’esprit lorsque vous planifiez une enquête.

04

## Création du compte

D’un numéro à la première conversation enregistrée.

1. ### Obtenir un numéro

   Une carte SIM prépayée ou une eSIM lorsque le compte doit être actif pendant une longue période ; une location ou une activation ponctuelle pour une mission de courte durée. Les services sont répertoriés ci-dessous.
2. ### Inscrivez-vous séparément de votre compte principal

   Inscrivez-vous dans l’application Telegram officielle sur un appareil distinct, un émulateur ou un profil de téléphone, et non à côté de votre compte principal.
3. ### Protégez-le à l’aide d’un mot de passe cloud

   Définissez immédiatement un mot de passe pour le cloud et une adresse e-mail de récupération qui ne sont utilisés nulle part ailleurs.
4. ### Fermez les paramètres de confidentialité

   Numéro de téléphone **« Personne** », « Retrouvez-moi grâce à mon numéro », « **Mes contacts** », « Vu pour la dernière fois », « Photos de profil » et « Biographie » : **« Personne »** ou « **Mes contacts** » ; désactivez la synchronisation des contacts.
5. ### Empêchez-le de s’autodétruire

   Réglez l’autodestruction du compte sur la durée la plus longue possible, afin qu’un arrêt de TgWitness ne vous fasse pas perdre votre compte.
6. ### Donnez-lui un profil neutre

   Aucun nom, photo, nom d’utilisateur ou biographie provenant de vos autres comptes, aucun contact personnel.
7. ### Laissez-le se mettre en route

   Rejoignez d’abord quelques discussions par jour. Les nouveaux comptes qui se précipitent sont les premiers à être limités.
8. ### Ne partagez rien avec les bots

   N’appuyez jamais sur « Partager le numéro de téléphone » ou « Partager la localisation » pour un bot. Ouvrez les liens et les mini-applications via un VPN ou un proxy sur cet appareil.
9. ### Connectez-le à TgWitness

   Dans votre propre espace de travail, connectez-vous via **Compte → Code QR**, puis appuyez sur **Sources → Mode enquête**. L’application est l’endroit où vous agissez, TgWitness est le registre.

Documentation Telegram

- [Vérification en deux étapes](https://core.telegram.org/api/srp)
- [Paramètres de confidentialité](https://core.telegram.org/api/privacy)
- [Autodestruction du compte](https://core.telegram.org/method/account.setAccountTTL)

05

## Services de numérotation

Options de départ. Les pays, les tarifs et la possibilité de modifier son numéro sur Telegram changent souvent ; vérifiez avant de payer.

### Cartes SIM prépayées et eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - Prépayé

  Formule PayGo, très bon marché
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - Prépayé
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - Prépayé
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - Prépayé
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### Applications de numéros virtuels 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  États-Unis uniquement ; l’inscription nécessite un numéro de téléphone américain
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  Le numéro vous est retiré si vous ne l’utilisez pas
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - Autres pays
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - Payant

  Avec une période d’essai
- [Hushedhushed.com](https://hushed.com)

  - De nombreux pays
  - Payant

  Bon marché
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  Numéros de téléphone mobiles européens dans une application
- [Sonetelsonetel.com](https://sonetel.com)

  - De nombreux pays
  - Numéro gratuit
- [Zadarmazadarma.com](https://zadarma.com)

  - De nombreux pays

  Numéros virtuels

### Nombre de locations et d’activations : 12

La location conserve un numéro pendant plusieurs semaines ou plusieurs mois. Une activation unique génère un code unique : définissez le mot de passe du cloud immédiatement après votre inscription.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Location
  - Activations
- [SMSPVAsmspva.com](https://smspva.com)

  - Location
  - Activations
- [5SIM5sim.net](https://5sim.net)

  - Location
  - Activations
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Location
  - À usage unique
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Location
  - Activations
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Location
  - Activations
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Location
  - Activations
- [365SMS365sms.org](https://365sms.org)

  - Location
  - Activations
- [SIMSMSsimsms.org](https://simsms.org)

  - Location
  - Activations
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - À usage unique
- [SMS-MANsms-man.com](https://sms-man.com)

  - À usage unique
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - À usage unique
