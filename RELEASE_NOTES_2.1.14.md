# Econergy Cloud 2.1.14

## Actualisation des températures
- Lecture groupée des derniers états publiés par le cloud toutes les dix minutes, sans réveil radio.
- Ajout de l’interrupteur « Actualisation forcée des températures », activé par défaut et visible dans la catégorie Diagnostics de chaque radiateur. L’interrupteur pilote le cycle radio de tout le domicile.
- Lorsque l’option est activée, une vague de demandes radio démarre toutes les cinq minutes, avec cinq secondes entre chaque radiateur.
- Une demande automatique est ignorée si `state.updatedAt` date de moins de cinq minutes, par exemple après une commande récente.
- Le suivi d’une demande est limité à deux vérifications, vers 2 puis 10 secondes.
- Le délai minimal d’une minute par radiateur et le respect des réponses HTTP 429 / `Retry-After` sont conservés.

## Actualisation manuelle
- Le bouton « Actualiser les infos » reste indépendant de l’interrupteur.
- Chaque appui envoie sa propre demande radio après expiration du délai minimal d’une minute pour le radiateur concerné.
- La récupération de consommation reste associée au bouton.

## Firmware
- Détection des changements de version de firmware avec mémorisation locale de la dernière version connue.
- Création d’une notification persistante Home Assistant indiquant le radiateur, l’ancienne version et la nouvelle version.
- Les mises à jour réalisées pendant un arrêt de Home Assistant sont également détectées à la prochaine synchronisation.

## Confidentialité
- Masquage des identifiants de domicile et de radiateur dans les diagnostics et les principaux journaux, avec conservation des quatre derniers caractères.
- Retrait de la mention « Bêta » du nom de l’intégration.

## Compatibilité
- Le domaine `econergy`, le parcours OAuth PKCE, les identifiants uniques existants et les données stockées sont conservés.
- Pour les entrées existantes, l’interrupteur est considéré activé tant qu’aucune valeur n’a été enregistrée.
