# Econergy Cloud 2.1.10 — Bêta

## Synchronisation de l'inventaire et nettoyage automatique
- L'inventaire des radiateurs (GET /homes/{homeId}/devices) est désormais contrôlé toutes les heures, au lieu de toutes les cinq minutes.
- Au démarrage et à chaque contrôle horaire, l'intégration compare les identifiants du registre Home Assistant à la liste renvoyée par Econergy.
- Les anciens appareils absents de la liste sont supprimés automatiquement, avec leurs entités Econergy obsolètes. Les appareils encore présents restent protégés ; un appareil avec des entités d'une autre intégration est conservé.

## Températures et limites API
- Le cycle indépendant d'actualisation radio reste ciblé sur cinq minutes par radiateur.
- Avec quatre radiateurs, une demande est lancée environ toutes les 75 secondes.
- Le délai minimal de 60 secondes par radiateur, la mémorisation des dernières demandes après redémarrage et la gestion des réponses HTTP 429/Retry-After sont inchangés.
- La diminution de fréquence concerne uniquement la lecture de l'inventaire ; elle ne ralentit donc pas l'actualisation des températures et des états.
