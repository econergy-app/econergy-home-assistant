# Econergy Cloud 2.1.12 — Bêta

## Actualisations d'état
- Une actualisation automatique et une actualisation manuelle simultanées sur le même radiateur partagent désormais la même demande. L'intégration ne déclenche pas une deuxième commande lorsque la première est encore en cours.
- La limite d'une demande par radiateur et par minute, ainsi que la gestion de HTTP 429 et de `Retry-After`, sont conservées.
- Les reports normaux liés au délai minimal passent en journalisation `DEBUG` au lieu d'apparaître comme des avertissements. Les véritables erreurs restent visibles.

## Journaux plus lisibles
- Les messages du coordinateur et du thermostat affichent désormais le nom du radiateur, suivi de son identifiant entre parenthèses.
- Ce format est appliqué aux actualisations d'état, aux programmes, réglages, consommations et commandes.

## Compatibilité
- Aucun changement des identifiants d'appareils ou d'entités Home Assistant.
- Aucune modification de la configuration OAuth ni des commandes de pilotage.

**Statut :** version bêta.
