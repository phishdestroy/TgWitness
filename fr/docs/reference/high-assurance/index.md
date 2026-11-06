# Déploiement hautement sécurisé

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/

Un serveur sécurisé disponible 24 h/24 et 7 j/7 sur Hetzner ou Phala Cloud, un DNS Gateway et des vérifications reproductibles par un tiers.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Déploiement et restauration](https://phishdestroy.github.io/TgWitness/fr/docs/reference/deployment/)

![Déploiement et restauration](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Un déploiement à haute fiabilité ajoute des contrôles indépendants de l’environnement de collecte à la vérification des archives. Le réviseur interroge les enregistrements de déploiement et d’accès détenus par le fournisseur de services cloud et Cloudflare, et un déploiement Intel TDX ajoute une attestation matérielle de l’environnement du collecteur.

L'utilisation classique en local et avec Docker reste inchangée. Rien ne fonctionne ici à moins que vous ne déployiez avec `python -m tgwitness.cloud`, et le collecteur ne lit son hôte que lorsque le déploiement est configuré `TGWITNESS_ASSURANCE`.

Organigramme · Opérateur → Serveur, pare-feu sans règles entrantes (API du fournisseur); Opérateur → Tunnel et DNS (API Cloudflare); Serveur, pare-feu sans règles entrantes → Tunnel et DNS (sortant uniquement); Serveur, pare-feu sans règles entrantes → Clé de signature créée sur le serveur; Verifier, jetons en lecture seule → Journal du fournisseur et pare-feu; Verifier, jetons en lecture seule → Adresse du connecteur de tunnel et point d’entrée; Verifier, jetons en lecture seule → Déclaration /api/assurance signée; Verifier, jetons en lecture seule → Fichier ZIP de preuves · Opérateur · Verifier, jetons enlecture seule · Serveur, pare-feu sansrègles entrantes · Journal du fournisseur etpare-feu · Adresse du connecteur detunnel et point d’entrée · Déclaration /api/assurancesignée · Fichier ZIP de preuves · Tunnel et DNS · Clé de signature créée surle serveur · API du fournisseur · API Cloudflare · sortant uniquement

**Schéma sous forme de texte**

1. Opérateur → Serveur, pare-feu sans règles entrantes (API du fournisseur)
2. Opérateur → Tunnel et DNS (API Cloudflare)
3. Serveur, pare-feu sans règles entrantes → Tunnel et DNS (sortant uniquement)
4. Serveur, pare-feu sans règles entrantes → Clé de signature créée sur le serveur
5. Verifier, jetons en lecture seule → Journal du fournisseur et pare-feu
6. Verifier, jetons en lecture seule → Adresse du connecteur de tunnel et point d’entrée
7. Verifier, jetons en lecture seule → Déclaration /api/assurance signée
8. Verifier, jetons en lecture seule → Fichier ZIP de preuves

**Sur cette page**

- [Ce qu'un vérificateur peut contrôler](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#what-a-verifier-can-check)
- [Fournisseurs](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#providers)
- [Machine virtuelle confidentielle sur Phala Cloud (Intel TDX)](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)
- [Avant de commencer](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#before-you-start)
- [Extrait du panneau](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#from-the-panel)
- [Tunnel rapide sans domaine](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#quick-tunnel-without-a-domain)
- [Déployer](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#deploy)
- [Déploiement de débogage et verrouillage](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#debug-deployment-and-lock)
- [Supprimer un déploiement](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#remove-a-deployment)
- [N'importe quel serveur (auto-certifié)](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#any-server-self-attested)
- [Vérifier](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#verify)
- [Rapport pour la remise des preuves](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#report-for-evidence-handover)
- [Cloudflare en tant que témoin externe](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)
- [Lecture du résultat du déploiement](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#reading-the-deployment-result)

## Ce qu’un vérificateur peut contrôler

| Revendication | Comment cela est-il vérifié ? | Géré par |
| --- | --- | --- |
| Le serveur a été créé via l’API du fournisseur à une date connue. | L'objet « Server » et sa création dans le journal propre au fournisseur | Fournisseur |
| Personne n'a utilisé les chemins d'accès du fournisseur | Journal des requêtes de la console, des opérations de secours, des réinitialisations de mot de passe, des reconstructions, des fichiers ISO, des images et des sauvegardes | Fournisseur |
| Aucune connexion n'a pu être établie | Le pare-feu du fournisseur ne comporte aucune règle d'entrée ; le protocole SSH est masqué dès le premier démarrage. | Fournisseur (pare-feu), hôte (SSH) |
| L'accès au panneau se fait uniquement via le tunnel | L'entrée du tunnel redirige uniquement vers le panneau ; le connecteur s'exécute à partir de l'adresse du serveur | Cloudflare |
| Ce logiciel fonctionne exactement ainsi | Le hachage signé de l'arborescence source du collecteur correspond à une extraction du commit déployé. | Collector, synchronisé avec Git |
| La clé de signature a été créée sur ce serveur | La clé signe une déclaration indiquant l’identifiant du serveur du fournisseur et le hachage du fichier cloud-init qu’elle a reçu. | Collector, vérifié par le fournisseur |
| Le journal appartient à cette clé et à ce serveur | Chaque processus lancé dans la preuve ZIP comporte la mesure de l'hôte pour ce serveur | Preuves ZIP |

Le collecteur enregistre l'état SSH, les sessions, l'historique des connexions et les informations de démarrage dans des enregistrements signés process-start et `host.state`. Sur une machine virtuelle ordinaire, il s'agit d'enregistrements d'inventaire locaux, que le vérificateur compare aux enregistrements indépendants du fournisseur. Le déploiement Intel TDX ci-dessous vérifie en outre les mesures basées sur le matériel.

## Fournisseurs

| `--provider` | Identifiants | Accès en lecture seule du vérificateur | Journal du fournisseur destiné au vérificateur | Conservé pour |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Jeton de lecture du même projet | Actions sur le serveur et le pare-feu | Tant que ces ressources existent |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Jeton d’accès personnel en lecture seule | Actions Droplet | Tant que le Droplet existe |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` portées en lecture seule | Événements liés aux comptes, versions des règles de pare-feu | 90 jours |
| `vultr` | `VULTR_API_KEY` | Utilisateur disposant d’un accès en lecture et de l’ `activity_logs` autorisation | Journal d'activité du compte (méthode, chemin d'accès, acteur) | 30 jours, voire plus avec un abonnement au journal d'audit |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | Historique des événements CloudTrail | 90 jours |
| `phala` | `PHALA_CLOUD_API_KEY` | Une clé API du même espace de travail | Révisions de l’application et opérations CVM : modifications de la configuration et de l’environnement Docker Compose, redémarrages, mises à niveau du système d’exploitation | Bien que l'application existe |
| `generic` | aucun | aucun | aucun : **auto-certifié** | – |

Utilisez un projet, une équipe, un compte ou un sous-compte dédié pour chaque dossier : l’accès en lecture seule du vérificateur n’affiche alors que ce déploiement. Les identifiants sont lus à partir `--provider-token-file` ou de la variable ci-dessus, jamais depuis la ligne de commande. Pour AWS, le fichier contient `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; la région est `--location`.

Ce que les enregistrements de chaque fournisseur ne peuvent pas montrer est indiqué dans chaque rapport. En résumé : Hetzner enregistre les requêtes de la console ; la console de récupération de DigitalOcean, Lish/Glish de Linode et la console web de Vultr ne sont pas enregistrées en tant que telles, de sorte que le compte root est verrouillé dès le premier démarrage et qu’une connexion à la console nécessiterait une réinitialisation du mot de passe ou une modification du mode de démarrage, opérations qui sont quant à elles enregistrées. Vultr renvoie l’adresse de la console à toute clé capable de lire l’instance ; ni l’enregistrement ni le rapport ne la stockent.

## Machine virtuelle confidentielle sur Phala Cloud (Intel TDX)

Le `--provider phala` le collecteur s’exécute dans une machine virtuelle confidentielle Intel TDX sur [Phala Cloud](https://phala.com/), gérée par dstack. L’hébergeur et le personnel de Phala ne peuvent pas lire sa mémoire, et le processeur signe une attestation indiquant ce que la machine a démarré. Le vérificateur ne se contente pas de croire Phala sur parole : `tgwitness.tdx` il vérifie lui-même chaque attestation, jusqu’à l’autorité de certification racine Intel SGX épinglée, en les comparant aux listes de révocation d’Intel et aux données de plateforme signées par Intel, et refuse les machines pouvant être déboguées ou migrées.

| Saisie d'un rapport | Ce qu’il présente |
| --- | --- |
| `tdx_binding` | L'attestation porte sur la déclaration signée du collecteur et la valeur aléatoire de cette requête. |
| `tdx_quote` | Intel se porte garant de cette attestation ; celle-ci n’est validée que si Intel estime que la plateforme est à jour. |
| `tdx_compose_hash` | RTMR3, généré à partir du journal d'événements dstack, mesure les rapports de composition d'application fournis par le collecteur |
| `tdx_compose` | Ce code est, octet par octet, celui généré par le commit déployé : les fichiers source sont identifiés par leur hachage, les deux images par leur digest, il n'y a pas d'autre code. |
| `tdx_identity` | L'attestation provient de l'application et de l'instance déployées, avec des clés issues du KMS de Phala et d'un disque chiffré. |
| `tdx_os` | Les valeurs de MRTD et RTMR0-2 correspondent à celles calculées par le vérificateur à partir de l’image du système d’exploitation dstack publiée par Dstack-TEE, déterminées par le hachage de l’image du système d’exploitation rapporté par le CVM, et à partir des tables ACPI générées par QEMU pour la configuration de la machine virtuelle : micrologiciel, noyau, initrd, ligne de commande avec le hachage du système de fichiers racine, mémoire, vCPU et périphériques. Une image de développement échoue |

L'image du système d'exploitation (environ 180 Mo, dont 21 Mo sont conservés) est téléchargée une seule fois depuis [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) vers `dstack-images` à côté de l'enregistrement ; `--tdx-image FOLDER` utilise un autre dossier ou une image décompressée, `--tdx-image none` ignore la comparaison. La mesure suit `dstack-mr` et le paquet Rust `qemu-acpi` provenant de Dstack-TEE/dstack ; `tools/check_dstack_image.py` la vérifie par rapport à la sortie ACPI propre à QEMU et par rapport à un enregistrement d’attestation matériel Phala Cloud réel, `--live` la vérifie également par rapport à l’image publiée. `--tdx-measurements` compare toujours MRTD et RTMR0-2, fournis sous forme de JSON à la place.

Chaque démarrage du collecteur enregistré dans le journal comporte une telle attestation ; ainsi, `verify --evidence` vérifie chaque démarrage ainsi que l’image du système d’exploitation à partir de laquelle il a démarré. Les révisions de l’application Phala et les opérations du CVM constituent le journal du fournisseur : une configuration Docker Compose modifiée après le déploiement entraîne l’échec du rapport, et les redémarrages sont répertoriés à des fins de vérification.

Dans le panneau, sélectionnez « **Machine virtuelle confidentielle · Phala Cloud »** sous « **Extras** → **Serveur 24/7 »** et collez une clé API Phala Cloud ; le tunnel rapide fonctionne comme sur Hetzner. Depuis la ligne de commande :

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` lit les certificats et les listes de révocation d’Intel à partir d’un fichier au lieu de les télécharger depuis le site d’Intel. Le DNS de passerelle n’est pas disponible ici : Phala ne dispose pas de pare-feu de fournisseur d’accès pour le trafic sortant.

### Certificat d’attestation

Pour un déploiement Phala, `verify --report certificate.md` écrit également le certificat : un `certificate.html` autonome et un `certificate.pdf` au format A4 contenant le verdict, la chaîne de confiance allant de la racine Intel à la clé collectrice, une comparaison avec les serveurs standard et à haute sécurité, les mesures à côté des valeurs calculées à partir de l’image publiée, les responsables de chaque élément, la chaîne de certificats Intel, chaque vérification, le journal du fournisseur, ainsi que la procédure à suivre pour répéter la vérification. Le rapport JSON reste le document faisant autorité ; les pages en assurent l’affichage.

Le rapport est scellé numériquement à l’aide de signatures et d’horodatages, dans le fichier `certificate.seal.json` et dans les fichiers `.tsq`/`.tsr` qui l’accompagnent :

| Sceau | Ce qu'il apporte |
| --- | --- |
| Horodatage électronique qualifié, `http://tsa.belgium.be/connect` | Horodatage RFC 3161 portant sur les octets exacts de `certificate.json`, émis par le prestataire de services de confiance qualifié du gouvernement fédéral belge (SPF Politique et Soutien, BOSA). Cette entité figure sur la liste de confiance de l’UE de la Belgique en tant que service d’horodatage qualifié, statut accordé ; la racine (Belgium Root CA6) et les entrées de la liste, telles qu’elles figurent dans la liste publiée le 20 octobre 2026, sont intégrées dans `tgwitness/tsa_roots.py`. En vertu de l’article 41 du règlement (UE) n° 910/2014, un tel horodatage est présumé exact quant à la date et à l’heure, ainsi qu’à l’intégrité des données, dans chaque État membre de l’UE |
| Horodatage RFC 3161, FreeTSA | Un deuxième horodatage, indépendant |
| Signature du vérificateur | Ed25519 sur une déclaration mentionnant le SHA-256 du rapport et chaque horodatage, avec la clé propre au vérificateur (`--sign-with FOLDER`, par défaut `~/.tgwitness/verifier`) ; le PDF porte une signature établie avec cette même clé |

`--timestamp URL` (répétable) choisit d’autres autorités, `--timestamp none` n’en choisit aucune, `--sign-with
none` laisse le sceau non signé. `check-report` vérifie le hachage du rapport, la signature du vérificateur, chaque horodatage par rapport à une racine de confiance et son statut qualifié, ainsi que la signature du PDF. La valeur juridique d’un horodatage qualifié en dehors de l’UE, ainsi que celle du rapport dans son ensemble, relève de la compétence du tribunal ou de l’autorité qui le reçoit ; le sceau indique la date à laquelle le rapport existait et atteste qu’il n’a pas été modifié.

Une attestation ne peut exclure la présence d’une faille dans le module TDX ou le microcode d’Intel, ni un accès physique au bus mémoire. Quiconque contrôle l’application sur le compte de Phala peut déployer un autre « compose » ; celui-ci apparaît alors comme une nouvelle révision dotée d’un nouveau hachage de « compose ». L’hôte contrôle la source de l’heure de la machine et le réseau.

Le déploiement, la vérification avec `--evidence`, les redémarrages, la comparaison des images du système d’exploitation, le certificat scellé numériquement avec des signatures et des horodatages, ainsi que la destruction ont été exécutés sur Phala Cloud lui-même ; voir [, l’exécution du 4 novembre 2026,](https://phishdestroy.github.io/TgWitness/fr/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026).

## Avant de commencer

1. Une zone Cloudflare, son identifiant de compte et un jeton API disposant des autorisations « **Cloudflare Tunnel Edit** », « **Zone Read** » et « **DNS Edit »**, fourni avec `--cloudflare-token-file` ou `CLOUDFLARE_API_TOKEN`. Pour le vérificateur : **Cloudflare Tunnel Read**, **DNS Read** et, pour le journal d’audit, **Account Settings Read**. Sans domaine, un [tunnel rapide](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#quick-tunnel-without-a-domain) n’a besoin d’aucun de ces éléments.
2. Identifiants du fournisseur avec accès en écriture à un projet dédié ; `lock` utilise la même chose :

   - Hetzner : jeton API avec droits de lecture et d'écriture ;
   - DigitalOcean : jeton d'accès personnel avec droit d'écriture ;
   - Linode : jeton d'accès personnel avec `linodes`, `firewall` et `events` des droits de lecture/écriture ;
   - Vultr : clé API d’un compte dédié ou d’un sous-compte ;
   - AWS : identifiants IAM autorisés `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` et `ec2:RevokeSecurityGroupIngress`.
3. Le commit à exécuter. Une balise de version est résolue une seule fois vers son commit avec `git ls-remote`; le serveur ne reçoit jamais que le commit de 40 caractères.

## Depuis le panneau

Sur votre propre ordinateur, **Extras → Server 24/7** exécute la même `deploy` pour Hetzner en trois étapes : choisissez l’Europe ou les États-Unis, collez un jeton Hetzner (lecture et écriture), puis vérifiez le type de serveur, le prix mensuel, l’adresse et la version que le panneau a trouvés avec ce jeton. Rien n’est créé avant que vous ne confirmiez. Le panneau affiche chaque étape en `deploy` elle les signale, puis l’ adresse, le jeton du panneau et l’empreinte de la clé de signature. Sans domaine, le serveur bénéficie d’un [tunnel rapide](https://phishdestroy.github.io/TgWitness/fr/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ; **« Vos serveurs → Trouver l’adresse actuelle »** la recherche à nouveau après un redémarrage. Pour une adresse fixe sous votre propre domaine, ouvrez **« Optionnel · votre propre domaine »** et ajoutez un jeton Cloudflare (le lien préparé sélectionne « Zone Lecture », « Modification DNS » et « Modification du tunnel Cloudflare »).

Les jetons circulent à chaque requête depuis l'onglet du navigateur vers TgWitness sur le même ordinateur et ne sont enregistrés nulle part ; l'enregistrement de déploiement, le fichier cloud-init expurgé, le jeton du panneau et, pour un tunnel rapide, la clé d'adresse sont conservés dans `deployments/NAME` au sein du répertoire de données. Le panneau n’offre cette fonctionnalité qu’à l’administrateur principal via une connexion directe en boucle fermée (`127.0.0.1`, sans en-têtes de proxy ni de tunnel) ; un panneau accessible via un réseau affiche les commandes à la place. La version par défaut correspond à la balise de publication du panneau en cours d’exécution, déterminée via l’ API GitHub. L’emplacement, le type de serveur et le prix proviennent de l’API de Hetzner : `cpx22` là où elle est proposée, sinon le type x86 le moins cher avec au moins 2 Go de mémoire.

## Tunnel rapide sans domaine

`--quick-tunnel` remplace `--zone`, `--cloudflare-account` et `--panel-host`; aucun compte ni jeton Cloudflare n’est impliqué :

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

Sur le serveur, cloudflared ouvre un [tunnel rapide](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) vers le panneau : une adresse aléatoire `https://….trycloudflare.com` qui change à chaque redémarrage de cloudflared ou du serveur. Un petit service sur le serveur publie chaque adresse dans un sujet aléatoire de ntfy.sh , signée (HMAC-SHA256) avec une clé que seul le répertoire de déploiement contient (`address-key.txt`), et la répète toutes les trois heures car ntfy.sh conserve les publications pendant 12. `deploy` et **« Find the current address** » n’acceptent que les messages signés ; ainsi, un message falsifié ne peut pas vous rediriger, vous et votre jeton de panneau, vers l’adresse de quelqu’un d’autre. Le sujet figure dans l’historique et dans le fichier cloud-init publié : quiconque y a accès peut lire l’adresse actuelle, qui demande toujours le jeton de panneau. Le serveur ne conserve aucun port entrant, quel que soit le cas.

Un vérificateur ne dispose d’aucune clé d’adresse, et toute personne lisant le sujet peut y publier un message. Ainsi, le collecteur publie également l’adresse elle-même, signée avec sa propre clé Ed25519, et `verify` retient le message le plus récent signé par la clé du collecteur dans l’enregistrement de déploiement ; les messages sont classés par ordre chronologique de réception par ntfy.sh, et non selon l’heure qu’ils indiquent. Un collecteur datant d’avant cette modification ne signe rien, et `verify` sélectionne alors la dernière publication et l’indique lors de la vérification `statement` ; une publication falsifiée ne peut que faire échouer cette vérification, puisque l’adresse doit toujours répondre avec la clé du collecteur.

Coût : aucun compte Cloudflare ne conserve de trace d’un tunnel temporaire ; par conséquent, `verify` signale que le tunnel, le connecteur et la vérification DNS sont indisponibles, et le résultat est au mieux `incomplete` (sur Phala Cloud, la vérification réussit en revanche : le connecteur s’exécute au sein de la configuration Docker Compose mesurée) ; les enregistrements du fournisseur, le pare-feu, la déclaration signée, les mesures de l’hôte et la comparaison avec le programme d’installation sont vérifiés comme d’habitude. La comparaison d’octets avec le programme d’installation de référence nécessite un commit déployé qui connaît déjà `--quick-tunnel` ; une version 0.7.0 permet de compiler le programme d’installation du domaine et signale la différence. Cloudflare n’offre aucune garantie de disponibilité pour les tunnels rapides, autorise 200 requêtes en cours et ne prend pas en charge les Server-Sent Events ; par conséquent, les mises à jour en temps réel du panneau (versions postérieures à la 0.7.0) peuvent ne pas parvenir via ce type de tunnel, ce qui nécessite de recharger la page ; cet aspect n’a pas été testé. Pour un cas qui doit fonctionner de manière fiable, utilisez votre propre domaine.

## Déployer

Consultez d’abord tout ce qui va être envoyé. `plan` N'effectue aucune requête auprès d'un fournisseur d'accès ou de Cloudflare :

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

Déployez ensuite avec les mêmes options et les mêmes identifiants :

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Types de serveurs pour débuter : `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` et `--image` par défaut, Ubuntu 24.04 de chaque fournisseur dans une région européenne.

`--repository` récupère le commit depuis un autre dépôt Git https, sans identifiants dans l’ URL (par défaut `https://github.com/phishdestroy/TgWitness.git`). `deploy` accepte également `--out` un autre répertoire de déploiement (par défaut `deployments/NAME`; un répertoire contenant déjà un déploiement est refusé) et `--wait`, le nombre de minutes à attendre pour la déclaration signée du collecteur : de 1 à 240, par défaut 20, ou 60 pour `generic`.

La commande :

1. crée un tunnel Cloudflare dont l’entrée redirige le nom d’hôte du panneau vers le panneau et, le cas échéant, le nom d’hôte du témoin vers `/api/witness/head` et `/api/assurance` uniquement ;
2. crée des enregistrements CNAME par proxy pour ces noms d'hôte, en refusant ceux qui existent déjà ;
3. crée un pare-feu fournisseur sans règles entrantes et un serveur derrière celui-ci, sans clé SSH, sans sauvegardes, sans agent de console, et avec cloud-init qui masque SSH, verrouille l'accès root, installe `cloudflared`, récupère exactement le commit, le vérifie et lance TgWitness en tant que service systemd renforcé ;
4. attend la déclaration signée du collecteur et vérifie qu’elle mentionne ce serveur ainsi que le hachage de ce cloud-init.

`deployments/case-2026-11/` Il contient ensuite :

| Fichier | Sommaire | Partager ? |
| --- | --- | --- |
| `deployment.json` | Les identifiants, les hachages, les appels API effectués (méthode, chemin, statut) et la première déclaration signée | Oui, avec le vérificateur |
| `cloud-init.redacted.yaml` | Le script cloud-init exact, dont les deux secrets ont été remplacés par `REDACTED` | Oui |
| `panel-token.txt` | Le jeton du panneau | Non |

Le mot de passe root du fournisseur, le jeton de tunnel et le jeton du panneau ne sont jamais enregistrés `deployment.json`. Publiez l’empreinte du collecteur indiquée à la fin via un canal que vous ne contrôlez pas seul, par exemple un canal de témoins ou un message adressé au destinataire.

Connectez-vous à Telegram à l’adresse `https://case.example.org` à l’aide du jeton du panneau, comme indiqué dans le [guide de configuration du compte](https://phishdestroy.github.io/TgWitness/fr/docs/reference/accounts/). Les actions du panneau sont enregistrées dans le journal signé ; il ne s’agit pas de sessions SSH. Un [témoin](https://phishdestroy.github.io/TgWitness/fr/docs/reference/witness/) peut interroger `https://case-witness.example.org`.

Il n’y a pas de SSH : si le démarrage échoue, le collecteur ne répond jamais. Supprimez le serveur et redéployez-le, ou utilisez un déploiement de débogage pour identifier la cause.

### Les secrets contenus dans les données utilisateur

Le script cloud-init contient deux secrets : le jeton du panneau et le jeton du tunnel Cloudflare. La clé de signature n’en fait pas partie ; elle est créée sur le serveur. Hetzner, DigitalOcean et Linode ne renvoient pas les données utilisateur via leur API. Vultr les renvoie à toute clé capable de lire l’ instance, et EC2 via `DescribeInstanceAttribute`. Pour AWS, ne donnez au vérificateur que les trois actions du tableau, jamais `ec2:Describe*`. Pour Vultr, partez du principe que la clé du vérificateur peut lire les deux jetons. Un jeton de tunnel permet à quelqu’un d’exécuter un deuxième connecteur : `verify` signale tout connecteur ne se trouvant pas sur le serveur, et les déclarations du collecteur ne peuvent pas être falsifiées de cette manière car chacune signe un nouveau défi. Avec `--quick-tunnel` le deuxième secret, c’est plutôt la clé d’adresse : quiconque la lit peut publier une fausse adresse que le panneau accepterait.

La déclaration publique du collecteur ne mentionne ni l'adresse du serveur ni les sources des connexions ; ces deux informations figurent dans le journal signé.

## Déploiement de débogage et verrouillage

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` Conserve une clé SSH provenant d’une seule adresse ou d’un petit réseau, au maximum un /24 pour IPv4 ou un /48 pour IPv6. `KEY` est déjà enregistré auprès du fournisseur : le nom ou l’identifiant d’une clé SSH dans le projet Hetzner, l’identifiant ou l’empreinte d’une clé SSH dans l’équipe DigitalOcean, un nom d’utilisateur Linode dont les clés SSH du profil sont ajoutées à root, l’identifiant d’une clé SSH dans le compte Vultr, ou le nom d’une paire de clés EC2 dans la région. Ces options ne s’appliquent pas à `generic`. Un tel déploiement est enregistré comme `debug` et n’est **jamais** signalé comme « haute sécurité ». Une fois que vous avez terminé, exécutez `sudo tgwitness-lock` comme dernière commande de la dernière session SSH, puis :

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

Le pare-feu perd toutes les règles entrantes. Les rapports indiquent alors quand le SSH a été autorisé et quand il a été fermé ; cette fenêtre reste visible.

## Supprimer un déploiement

`destroy` Supprime le serveur et son pare-feu, identifiés par l’étiquette du déploiement, de sorte qu’un déploiement ayant échoué en cours de route soit également supprimé, puis les enregistrements DNS pointant vers son tunnel, ainsi que le tunnel lui-même. Le journal du serveur et la clé de signature sont supprimés en même temps : exportez d’abord les preuves. L’enregistrement reste, marqué `removed`, avec les appels API de la suppression.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

La suppression via l’API est implémentée pour Hetzner. Pour les autres fournisseurs `destroy` s'arrête avant de supprimer quoi que ce soit et indique le nom du label à supprimer dans la console du fournisseur. Un serveur installé manuellement (`generic`) ne perd que son tunnel et ses enregistrements DNS. Un déploiement rapide de tunnel ne nécessite aucun jeton Cloudflare : son tunnel se termine au niveau du serveur, et ses publications expirent sur ntfy.sh dans un délai de 12 heures.

## N'importe quel serveur (auto-certifié)

`--provider generic` Conçu pour un serveur acheté ou installé manuellement. `deploy` crée le tunnel et le DNS, écrit `install.sh` (privé) et `install.redacted.sh` (à publier), puis attend. Copiez `install.sh` sur un serveur Ubuntu 24.04 fraîchement installé et exécutez-le à cet endroit :

```
sudo bash install.sh
```

Il enregistre l’hôte tel qu’il était (connexions, comptes, `authorized_keys`, sockets d’écoute, services, tâches planifiées, paquets), installe le commit, active le pare-feu de l’hôte, s’efface lui-même, masque le SSH et met fin à la session. Le rapport concernant un tel serveur est, au mieux, **AUTO-ATTESTÉ** : la personne qui a exécuté le programme d’installation disposait des droits root avant celle-ci, et aucun enregistrement du fournisseur n’est disponible pour le vérificateur. C’est tout de même mieux qu’un serveur inexpliqué : l’inventaire, le hachage du programme d’installation et chaque connexion ultérieure sont signés.

## Vérifier

Le vérificateur a besoin `deployment.json`, le programme d'installation publié, des identifiants en lecture seule et, idéalement, une copie du commit et une preuve ZIP :

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

Chaque fournisseur et chaque valeur Cloudflare sont demandés par le vérificateur à ce moment-là ; l'enregistrement ne fournit que les identifiants à interroger. Le code de sortie est 0 pour **PASS**, 1 pour **FAIL** et 2 pour **REVIEW**, **INCOMPLETE** ou **SELF-ATTESTED**. `--fingerprint` devrait provenir d’un canal indépendant ; sans cela, la clé est comparée uniquement à l’enregistrement de l’opérateur. `python verify.py` vérifie toujours les preuves ZIP, comme dans la section « [Preuves](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/) ».

Les actions du fournisseur sont classées : la création et le démarrage dans les 30 minutes suivant la création sont validés ; la console, le sauvetage, la réinitialisation du mot de passe, la reconstruction, l’ISO, les images, les instantanés, les sauvegardes, Systems Manager, EC2 Instance Connect et les ouvertures de pare-feu échouent ; les actions liées à l’alimentation et tout élément inattendu sont signalés pour examen. Une action inconnue n’est jamais ignorée.

## Rapport pour la remise des preuves

`--report report.md` rédige le rapport au format Markdown et `report.json` à côté :

1. résultat, empreinte de la clé du collecteur, déploiement, fournisseur, commit, serveur, pare-feu, tunnel ;
2. chaque vérification avec son statut et sa source (API du fournisseur, API Cloudflare, relevé du collecteur, journal des preuves) ;
3. le journal du prestataire avec l'évaluation de chaque action et, lorsque le prestataire l'enregistre, l'acteur ;
4. les points de terminaison Cloudflare contenant les connexions du tunnel, la configuration et le journal d'audit ;
5. la déclaration signée du collecteur ;
6. ce que le rapport établit et ce qu’il n’établit pas ;
7. les commandes permettant de le reproduire, ainsi que l'SHA-256 de chaque fichier qui lui a été fourni.

Remettez le rapport, `report.json`, `deployment.json`, le programme d’installation publié et les preuves ZIP. Rédigez le rapport rapidement : les journaux des fournisseurs ne sont conservés que pendant une durée limitée.

## Cloudflare en tant que témoin externe

Tout ce qui est présenté ici est facultatif. Même sans compte Cloudflare, le serveur continue de fonctionner, et deux de ces solutions sont opérationnelles dès aujourd’hui :

| Qu'est-ce que | Ce qu’il présente | Dans TgWitness |
| --- | --- | --- |
| Tunnel rapide ou tunnel de votre domaine | L'accès au panneau se fait uniquement via le tunnel | L'assistant de configuration du serveur, voir ci-dessus |
| relais drand `drand.cloudflare.com` | Les enregistrements postérieurs à une session de drand sont plus récents que celui-ci : le journal a été rédigé au fur et à mesure. | mode « evidence », « **More witnesses** », « no account » ([format](https://phishdestroy.github.io/TgWitness/fr/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Notifications sur l'état du tunnel | lorsque le tunnel était hors service, par e-mail ou via un webhook de Cloudflare | Configurez-les dans le tableau de bord Cloudflare |
| Gateway DNS (`--gateway-dns`, ou **DNS de la passerelle Cloudflare** dans l'assistant) | chaque nom recherché par le serveur, auquel Cloudflare a répondu via TLS ; le pare-feu Hetzner empêche le DNS d’accéder à quoi que ce soit d’autre ; si une politique de passerelle pouvait réécrire les réponses | Hetzner, forfait Zero Trust gratuit, sans domaine ; `verify` vérifie le pare-feu, l’emplacement, la journalisation, les politiques, les requêtes du serveur et le journal d’audit ; le mode « evidence » copie le journal dans le registre |
| Passerelle avec le client Cloudflare One sur le serveur, un pare-feu sortant qui n'autorise que Cloudflare | chaque connexion établie par le serveur, et pas seulement les requêtes DNS | pas encore développé |
| Accès devant le panneau | qui s'est connecté au tableau de bord et à quel moment | Non implémenté : nécessite votre propre domaine |
| Journalisation des commandes SSH | chaque commande d'une session de débogage | pas encore développé |

Logpush, qui permettrait de conserver une copie propre à Cloudflare dans R2, est une fonctionnalité Enterprise : avec la formule gratuite , Cloudflare répond `logpush is not enabled for this account`. Son journal Gateway y est conservé pendant 24 heures ; le mode « evidence » le copie donc dans le journal signé (**le journal de Cloudflare Gateway contenant les requêtes DNS de ce serveur**, un jeton en lecture seule avec l’autorisation « Account Analytics Read »).

Sans stratégie « Zero Trust », un compte dispose d’un seul emplacement DNS. Lorsque Cloudflare en refuse un autre, le serveur partage l’emplacement existant et ses requêtes sont distinguées par leur adresse ; ce filtre nécessite également l’accès « Zero Trust PII Read », et `destroy` laisse une localisation partagée. Une requête de journalisation s’étend sur trois heures au maximum ; ainsi, la copie et la `verify` lecture de la journée s’effectuent par tranches de trois heures.

Le DNS de la passerelle gère le résolveur du système. Le DNS sur HTTPS sur le port 443 vers un autre résolveur, ainsi que les connexions vers une adresse non répertoriée (les centres de données de Telegram, par exemple), ne figurent pas dans son journal.

Cloudflare ne peut pas accéder au contenu chiffré de Telegram, ni aux autres appareils associés au compte Telegram (la liste des appareils du mode « evidence » les recense depuis le côté de Telegram), ni à l’hyperviseur du fournisseur d’accès.

## Lecture du résultat du déploiement

Pour une machine virtuelle classique, le fournisseur contrôle l’infrastructure hôte, et l’inventaire local est vérifié parallèlement aux enregistrements du fournisseur. Pour Intel TDX, le vérificateur contrôle en outre la configuration matérielle, la liaison du collecteur, la composition et les mesures du système d’exploitation. Consultez les résultats individuels pour voir quelles vérifications ont été réussies ou n’étaient pas disponibles.

Les détails historiques relatifs au pare-feu dépendent du fournisseur ; Linode conserve les versions des règles. L'enregistrement de validation   répertorie les déploiements testés et les vérifications en cours, et la portée de vérification   relie ces vérifications d'environnement à l'acquisition et à l'intégrité des archives.
