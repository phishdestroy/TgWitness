# Gérer un groupe de comptes

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/groups/

Gérez simultanément plusieurs comptes de collecte tout en conservant la distinction entre les enregistrements et l’identité de signature de chaque compte.

Un groupe de comptes regroupe l'état de la connexion, les contrôles de surveillance, les paramètres partagés et les exportations dans une seule vue de travail. Cela s'avère utile lorsque plusieurs comptes concernent la même enquête ou nécessitent une configuration opérationnelle cohérente.

## Ouvrir l'aperçu du groupe

Dans **la** **section** **« Comptes »**, ouvrez le groupe. Chaque compte affiche son état de surveillance, l’itinéraire de connexion, la dernière latence mesurée sur l’itinéraire lors d’une vérification réussie et le dernier message enregistré. Les liens **« À surveiller »** renvoient vers les comptes nécessitant une intervention ; **le bouton « Corriger »** ouvre l’espace de travail et les commandes correspondants.

Les commandes « **Tout démarrer »** et « **Tout mettre en pause »** s’appliquent aux comptes éligibles après confirmation. **Les paramètres de groupe** permettent de partager les paramètres sélectionnés ; les comptes disposant de leurs propres valeurs les conservent jusqu’à ce que vous choisissiez de les remplacer.

### Vérifier un changement d'itinéraire au sein d'un groupe

Exemple synthétique · vérifications et résultats à titre d’illustration

1. **Sélectionner.** Choisissez le groupe et vérifiez quels comptes vont être modifiés.
2. **Préparation.** Conserver le chemin d’accès propre à chaque compte lorsqu’il doit rester distinct.
3. **Vérifier.** Tester la connexion proposée et examiner les résultats des mesures.
4. **Appliquer.** Vérifier à nouveau avant d'enregistrer et contrôler le résultat pour chaque compte.

#### Équipe chargée de l’affaire

Collecteur de canaux · Collecteur de groupes · Compte de référence

3 espaces de travail distincts

#### Sélection révisée

2 comptes suivent la démarche proposée.

Le compte de référence suit son propre parcours.

#### Vérifications préalables

Collecteur de canaux : temps de transfert Telegram de 84 ms

Collecteur de groupe : temps de transfert Telegram : 91 ms

Ces chiffres sont des valeurs fictives fournies à titre d’exemple.

#### Résultats de l'application

Collecteur de canaux : acheminement enregistré, observation reprise.

Collecteur de groupe : nouvelle vérification échouée, paramètres précédents restaurés.

Compte de référence : itinéraire conservé.

## Modifier le parcours en ajoutant une étape de révision

1. Sélectionnez « **Modifier l'itinéraire du groupe** », puis choisissez le type de connexion et les paramètres.
2. Sélectionnez « **Review selection** ». Passez en revue les comptes répertoriés et leurs dérogations d’itinéraire individuelles.
3. Sélectionnez « **Préparer et vérifier** ». La vérification utilise un nouveau transport Telegram ; les routes HTTP prises en charge signalent également leur vérification de sortie HTTPS.
4. Sélectionnez « **Appliquer la connexion cochée »** et examinez les résultats de chaque compte. L’observation en cours reprend là où l’application a abouti ; les comptes inactifs restent inactifs.

La latence décrit le temps mesuré pour l'établissement de la connexion Telegram. Une vérification de l'adresse IP de sortie décrit cet itinéraire au moment de la vérification enregistrée. L'autorisation du compte et l'état de la surveillance disposent de leurs propres indicateurs ; un changement de groupe peut aboutir à des résultats différents selon les comptes.

## Utiliser l’accès par chevauchement

**La section « Discussions consultées par plusieurs comptes »** affiche les sources partagées et la couverture d’observation disponible dans l’espace de travail. Les canaux et supergroupes éligibles peuvent utiliser **la fonction** **« Exporter avec… comptes »** pour fractionner l’acquisition de l’historique d’une discussion. Les discussions privées et les groupes ordinaires restent associés au compte d’origine, car leurs numéros de message font partie de l’historique de ce compte.

## Exporter le groupe sous forme de package

**La fonction « Export group »** crée un fichier ZIP contenant l’exportation signée de chaque compte ainsi qu’une liste signée de ces fichiers. Les identités et empreintes digitales d’origine de l’espace de travail restent disponibles à des fins de vérification. Construisez un récit inter-comptes à l’aide de ces références ; une chronologie unique fusionnée est toujours assemblée séparément.

Poursuivez avec [la conception du rapport](https://phishdestroy.github.io/TgWitness/fr/docs/reports/), [un « Case Board » au sein d’un espace de travail](https://phishdestroy.github.io/TgWitness/fr/docs/case-board/) ou [la vérification des exportations](https://phishdestroy.github.io/TgWitness/fr/docs/exports/).
