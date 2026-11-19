# Econergy Home Assistant — version 2.1.13 (Bêta)

## Radiateurs réappairés ou supprimés

- Prise en charge des réponses HTTP 410 `DEVICE_REPLACED` et `DEVICE_DELETED` de l'API Econergy 1.12.0.
- Lorsqu'un radiateur est réappairé, l'intégration lit `details.replacedBy`, vérifie le nouvel identifiant dans l'inventaire et migre le registre Home Assistant.
- Les `unique_id` des entités Econergy sont mis à jour pour suivre le nouvel identifiant. Les `entity_id` sont conservés lorsque c'est possible, sans conflit.
- L'archive de consommation locale est transférée vers le nouvel identifiant. Les programmes et réglages sont relus depuis l'API ; le statut d'une ancienne commande n'est pas réattribué au nouveau radiateur. Les statistiques long terme sont réimportées sous le nouvel identifiant ; les anciennes entrées restent dans Recorder.
- Un radiateur supprimé sans remplacement est retiré du registre Home Assistant avec ses entités Econergy.
- Les plateformes sont rechargées après une modification d'identifiant afin de reconstruire les entités à partir de l'inventaire actualisé.
- Aucune commande de chauffage n'est automatiquement rejouée sur le nouveau radiateur.

## Inventaire

- Avant le nettoyage d'un identifiant qui disparaît de l'inventaire, l'intégration consulte son endpoint de statut afin de recevoir les nouveaux codes 410 et l'identifiant de remplacement.
- Si la liste des domiciles et `replacedBy` ne sont pas encore synchronisés, l'intégration interroge directement le nouvel identifiant et diffère la migration si le remplaçant n'est pas encore accessible.
- Les nouveaux radiateurs ajoutés au domicile sont pris en compte après synchronisation et rechargement des plateformes.

## Multi-domicile et informations

- Le scope OAuth `multihome` reste demandé, en plus de `readonly` et `write`. Il ne bloque pas les comptes ne possédant qu'un domicile.
- Mise à jour des explications d'installation : l'autorisation des domiciles se fait côté Econergy, puis chaque domicile est configuré comme une entrée Home Assistant distincte.
- Mise à jour de `info.md` et du README pour expliquer la procédure manuelle d'ajout des domiciles de test, les conditions premium/administrateur et les limites actuelles de la bêta.
- Préparation des liens pour le futur nom de dépôt `flo1990m/econergy-home-assistant`. Le dépôt GitHub devra être renommé manuellement avant la publication.

## Compatibilité

- Le domaine d'intégration `econergy` et le flux OAuth PKCE sont conservés.
- Aucun changement volontaire des identifiants Home Assistant, hormis la migration nécessaire de l'ancien identifiant Econergy vers `replacedBy`.