# Changelog

## 2.1.8 — bêta — 16 novembre 2026

### Nouvelles fonctions
- Ajoute l’interrupteur d’activation/désactivation de la détection de fenêtre ouverte (`windowDetection`). Le capteur `windowOpen` reste distinct : il indique l’événement détecté.
- Ajoute le réglage de correction de sonde (`calibrationC`), de −8 à +8 °C par pas de 1 °C. La mesure `measuredC` est déjà corrigée par Econergy et n’est pas recalibrée une seconde fois dans Home Assistant.
- Affiche la consigne hors-gel directement depuis `state.setpointC` ; aucune valeur fixe n’est utilisée.

### Correctifs
- Interprète les erreurs structurées via `error.code`, conserve `details` et reconnaît `HOME_SUSPENDED` sans désactiver la lecture du domicile.
- Exploite `Retry-After` et `details.retryAfterS`. Lorsqu’une réponse `RATE_LIMITED` fournit un `commandId`, l’intégration suit la commande déjà en cours au lieu d’en envoyer une autre.
- Persiste les dernières demandes d’état et les délais de limitation afin d’éviter une nouvelle demande trop rapprochée après redémarrage.
- Supprime le rechargement automatique de l’intégration à chaque mise à jour de l’entrée OAuth : le renouvellement du jeton ne doit plus redémarrer inutilement le cycle d’actualisation des radiateurs.
- Conserve le rythme de demande d’état d’environ cinq minutes par radiateur.
- Les identifiants d’entités et d’appareils restent fondés sur le `deviceId` renvoyé par Econergy, indépendamment du nom d’affichage.

## 2.1.6 — bêta — 12 novembre 2026

- Fusionne les demandes d'actualisation de l'état et de la consommation dans l'action « Actualiser les infos », en conservant l'identifiant unique de l'ancien bouton d'état.
- Remplace le graphique 15 jours basé sur ApexCharts par des graphiques natifs journaliers Recorder pour l'énergie estimée et la durée de chauffe.
- Simplifie la page « Programmes du radiateur » : retrait de l'activation depuis cette page et passage au vouvoiement dans l'éditeur.
- Harmonise le texte d'information sur les créneaux et le mode Programmation.
- Conserve la route officielle de récupération de notice et remonte les erreurs API sans affirmer à tort que le PDF est absent.

## 2.1.5 — bêta — 12 novembre 2026

- Ajoute l'état natif du chauffage réellement actif dans la fenêtre de thermostat Home Assistant.
- Ajoute des exemples Lovelace indépendants : état, consommation, réglages, diagnostic et actions ; le graphique API 15 jours affiche les dates en JJ/MM.
- Retire le graphique de consommation de la page de programmation, désormais exclusivement consacrée aux programmes du radiateur.
- Corrige les libellés des actions et réglages, traduit les statuts de commande en français et harmonise l'icône d'actualisation de la consommation.
- Fournit une carte `statistics-graph` configurée avec les identifiants de statistiques long terme Econergy pour afficher les relevés archivés sur 30 jours.


## 2.1.4 — bêta — 12 novembre 2026

- Ajoute des exemples Lovelace de tuiles Econergy et des modèles réutilisables pour piloter les radiateurs avec l'état de chauffe réel.
- Aucun changement de l'API, des commandes, de l'autorisation OAuth ou des identifiants uniques.

## 2.1.1 — 11 novembre 2026

### Correctifs
- Corrige la classe d'état des capteurs de consommation énergétique : les consommations journalières utilisent désormais `total`, tandis que la durée de chauffe conserve `measurement`.
- Améliore le capteur « Régime appliqué » : interprète le mode réel du radiateur et, en mode programmation, la consigne et le créneau hebdomadaire courant lorsque l'API ne fournit pas `setpointKind`.
- Conserve le statut de la dernière commande dans le stockage Home Assistant afin de le retrouver après un redémarrage.
- Affiche une notification informative lorsque l'API renvoie `MANUAL_NOT_FOUND`, sans faire échouer l'action du bouton.

### Compatibilité
- Aucun changement de configuration OAuth requis.
- L'entrée Econergy existante et ses appareils sont conservés lors de la mise à jour.
