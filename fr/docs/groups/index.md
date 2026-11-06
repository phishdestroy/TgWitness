# Telegram · Gérer un groupe de comptes

Canonical page: https://phishdestroy.github.io/TgWitness/fr/docs/groups/

Gérez plusieurs comptes ensemble, chacun gardant ses entrées et sa clé.

Un groupe réunit sur un écran l’état des connexions, démarrage/pause, les paramètres partagés et les exports. Pratique quand plusieurs comptes travaillent sur la même affaire.

## Ouvrir l'aperçu du groupe

Ouvrez le groupe dans **Comptes**. Chaque compte affiche son état, son itinéraire, sa latence et son dernier message enregistré. **Nécessite une attention** liste ceux qui posent problème, **Corriger** vous y emmène directement.

**Tout démarrer** / **Tout mettre en pause** demandent avant d’agir. Les **Paramètres du groupe** sont partagés, mais les valeurs propres d’un compte restent jusqu’à ce que vous les remplaciez.

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

1. **Changer l’itinéraire du groupe**, choisissez le type et les réglages.
2. **Vérifier la sélection** : quels comptes changent et lesquels ont leur propre itinéraire.
3. **Préparer et vérifier** teste une nouvelle connexion à Telegram et, si possible, l’IP de sortie.
4. **Appliquer la connexion vérifiée** et regardez chaque résultat. Les comptes actifs reprennent, les inactifs le restent.

La latence est le temps d’établissement de la connexion à Telegram ; l’IP de sortie est celle que l’itinéraire a montrée lors de la vérification. Les résultats peuvent varier selon le compte.

## Utiliser l’accès par chevauchement

**Chats que voient plusieurs comptes** liste les sources partagées et leur couverture. Canaux et supergroupes peuvent être exportés par plusieurs comptes à la fois avec **Exporter avec … comptes**. Pas les chats privés ni les groupes simples : leurs numéros de message sont propres à chaque compte.

## Exporter le groupe sous forme de package

**Exporter le groupe** fournit un ZIP avec l’export signé de chaque compte et une liste signée de ces exports. Chacun garde son empreinte pour la vérification. La chronologie fusionnée, c’est toujours à vous de la construire.

Ensuite : [rapports](https://phishdestroy.github.io/TgWitness/fr/docs/reports/), [Case Board](https://phishdestroy.github.io/TgWitness/fr/docs/case-board/), [vérifier les exports](https://phishdestroy.github.io/TgWitness/fr/docs/exports/).
