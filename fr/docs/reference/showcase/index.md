# Vitrine publique

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/showcase/

Publiez les messages enregistrés des chaînes publiques sélectionnées ainsi que les instantanés signés via des liens à durée limitée et révocables.

**Access → Public showcase** crée une page distincte en lecture seule à l’aide du système d’access-token existant. Elle lit les observations enregistrées par l’installation. Elle ne lance pas de collecteur, ne se connecte pas à Telegram et n’acquiert pas de chaîne pour un visiteur.

## Publier une page

1. Enregistrez un profil source pour chaque chaîne publique que vous souhaitez afficher. Une chaîne doit disposer d’un nom d’utilisateur public dans son dernier profil enregistré ; les groupes et les discussions privées ne sont pas éligibles.
2. Ouvrez **Accès → Vitrine publique** (ou `/showcase-manage.html`) en tant qu'administrateur.
3. Sélectionnez des chaînes parmi un maximum de 16 espaces de travail, saisissez le titre de la page publique, puis choisissez une durée de validité du lien de 1, 7 ou 30 jours. Les libellés internes des espaces de travail ne sont pas publiés. Il est possible d’inclure jusqu’à 64 chaînes.
4. Vérifiez le texte des chaînes sélectionnées avant publication, puis cliquez sur « **Aperçu des enregistrements sélectionnés**». L'aperçu utilise la même projection côté serveur que la page des visiteurs.
5. Cliquez sur « **Créer un lien de présentation** ». Copiez le lien tant qu’il est visible. Ouvrez-le dans un navigateur distinct pour vérifier la page du destinataire avant de la partager.

Le lien contient un jeton d’accès dans son fragment d’URL. La page supprime ce fragment avant d’effectuer des requêtes API et l’échange contre une session de navigateur. Toute personne disposant du lien peut ouvrir le contenu sélectionné jusqu’à son expiration ou sa révocation. Les nouveaux liens autorisent 100 sessions simultanées, chacune d’une durée maximale d’une heure. Les contrôles d’accès existants peuvent également imposer des restrictions d’adresse et des limites de connexion via l’API « grant ». L’accès normal des réviseurs correspond à un mode différent et inclut toujours les messages et fichiers autorisés à l’origine.

## Ce que voient les visiteurs

| Visible | Reste privé |
| --- | --- |
| Sélection de titres de chaînes publiques, de noms d’utilisateurs et de dates d’observation des profils | Identités des comptes, libellés internes des espaces de travail et sources non sélectionnées |
| Texte capturé et chaque modification enregistrée | Identifiants d'expéditeur structurés, noms, noms d'utilisateur, numéros de téléphone et valeurs de profil |
| Observations de suppression avec le texte précédemment enregistré, le cas échéant | Pièces jointes, avatars, vignettes, noms de fichiers et données d'origine |
| Marqueurs indiquant qu'un auteur/profil ou une pièce jointe a été enregistré(e) | Métadonnées de transfert et de réponse, chemins réseau, adresses IP et identifiants |
| Nombre d'événements sur les chaînes sélectionnées, commutateurs de collection actuels, intervalle entre les signaux de vie et les points de contrôle | Commandes de collecte et API standard d’exportation des preuves |
| Empreinte de signature, point de contrôle du journal et preuve de cohérence | Clés de signature et sessions Telegram |

**Le texte des messages publics n’est pas automatiquement anonymisé.** Un nom, une mention, un numéro de téléphone ou un lien figurant dans le message reste intégré à ce texte. `Redacted`s'applique aux champs structurés d'auteur/de profil. Vérifiez le contenu effectivement sélectionné avant de le publier, y compris les modifications et suppressions conservées.

L'éligibilité reflète le **dernier profil source enregistré**, et non une recherche en temps réel sur Telegram. Si un profil ultérieur ne comporte plus de nom d'utilisateur de chaîne publique, les nouvelles requêtes excluent cette chaîne. Actualisez les profils source lorsque la visibilité publique change. Les lecteurs peuvent déjà disposer de contenus qu'ils ont reçus précédemment.

Les enregistrements signés d’origine restent inchangés. La projection affichée est signée séparément et comporte des hachages faisant référence à ses enregistrements d’origine. Une signature de projection authentifie la déclaration affichée ; il ne s’agit pas de la signature de l’événement d’origine appliquée à des octets expurgés.

## Vérifier les signatures et la continuité

Développez « **Empreinte digitale et point de contrôle signé** » et téléchargez un instantané. Après un rafraîchissement de la page, le téléchargement inclut l’instantané précédent du navigateur et une preuve de cohérence de Merkle entre les limites de leurs journaux. Le rafraîchissement automatique a lieu une fois par minute tant que la page est visible et affiche sa première page d’observations.

Une fois TgWitness installé, vérifiez le fichier téléchargé hors ligne :

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

L'empreinte digitale doit provenir d'une référence de confiance distincte. Pour effectuer une comparaison avec un instantané que vous avez conservé vous-même, utilisez `--previous earlier.json`; cela remplace l’instantané précédent inclus dans le téléchargement. La preuve actuelle doit commencer à cette limite conservée. Les clients authentifiés peuvent demander cette preuve à l’aide de `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`. Un journal plus court renvoie un code d’état HTTP 409 au lieu de réinitialiser silencieusement la limite.

Le point de contrôle signé valide l’intégralité du **journal du collecteur**, y compris son nombre d’enregistrements et son hachage d’en-tête opaque. Les nombres de messages affichés ne s’appliquent qu’aux canaux publics sélectionnés. La page ne répertorie jamais le contenu des autres journaux. Il s’agit de nombres d’événements, et non de nombres de messages uniques. Les paramètres décrivent la configuration actuelle, et non chaque intervalle d’enregistrement antérieur.

La vérification de la signature et de la cohérence permet de détecter les modifications par rapport à une limite définie. Elle ne procède pas à un recomptage indépendant des compteurs signés, ne certifie pas l’origine Telegram, ne démontre pas une capture ininterrompue et ne remplace pas un témoin indépendant. Pour cette vérification, utilisez le [vérificateur de preuves](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [le témoin indépendant](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/) et [l’enregistrement à l’échelle testée](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/). Les installations synthétiques sont clairement identifiées comme telles.

## Révoquer ou héberger la page

Utilisez **« Revoke »** dans le gestionnaire de vitrines ou dans la section **« Accès »** existante pour fermer le lien et mettre fin à toutes ses sessions. Le visiteur efface les enregistrements affichés lorsqu’une requête détecte que l’accès a pris fin. L’expiration et les autorisations sont vérifiées à chaque requête. Les autorisations de vitrine ne peuvent pas être converties en accès standard au panneau sur place ; créez une nouvelle autorisation pour changer de mode.

La page est servie via l’adresse HTTPS existante de l’installation. La publication d’un lien n’ouvre pas de nouveau port, ne crée pas de tunnel et ne modifie pas le DNS. Le code HTML et l’API restent sur l’installation de l’utilisateur. Un visiteur de la vitrine ne peut pas utiliser les API habituelles de message, de profil, de média, d’exportation ou de gestion avec cet accès.
