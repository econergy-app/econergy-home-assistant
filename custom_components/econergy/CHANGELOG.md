## 2.1.13 — bêta — 19 novembre 2026

### Prise en charge des nouveaux retours API 1.12.0
- Traite explicitement les réponses HTTP 410 `DEVICE_REPLACED` et `DEVICE_DELETED` renvoyées par les routes d'un radiateur.
- Lors d'un réappairage, récupère `details.replacedBy`, vérifie le nouvel appareil dans l'inventaire et migre l'identifiant du registre Home Assistant.
- Migre les identifiants uniques des entités Econergy en conservant leurs `entity_id` lorsque cela ne crée aucun conflit ; recharge ensuite l'entrée pour reconstruire les entités avec le nouvel identifiant API.
- Transfère l'archive locale de consommation vers le nouvel identifiant ; les programmes et réglages sont relus depuis l'API pour ne pas réutiliser un cache de l'ancien identifiant. Les statistiques long terme sont réimportées sous l'identifiant du nouveau radiateur ; les anciennes statistiques restent disponibles sous leur ancien identifiant.
- Lorsqu'un radiateur est supprimé sans remplacement, retire ses entités et son appareil du registre Home Assistant.
- Aucun ordre de chauffage n'est automatiquement rejoué sur le nouveau radiateur.

### Synchronisation de l'inventaire
- Avant de supprimer un ancien appareil absent de `GET /homes/{homeId}/devices`, vérifie son endpoint de statut afin de récupérer le code 410 et l'identifiant de remplacement.
- Si l'endpoint direct reste temporairement accessible ou renvoie une erreur réseau, diffère le nettoyage plutôt que de supprimer prématurément l'appareil.
- Détecte également les radiateurs ajoutés au domicile et recharge les plateformes pour créer leurs entités.

### Multi-domicile et informations
- Conserve la demande OAuth des scopes `readonly write multihome`. Le scope `multihome` reste sans effet négatif pour un compte à un seul domicile.
- Clarifie les textes de configuration : autorisation d'un ou plusieurs domiciles côté Econergy, puis une entrée Home Assistant distincte par domicile.
- Actualise `info.md` et le README sur les conditions d'accès actuelles à la bêta : domicile premium, administrateur et ajout manuel des domiciles de test par le mainteneur.
- Prépare les liens du dépôt sous son futur nom `econergy-home-assistant` ; le renommage GitHub du dépôt devra être effectué avant la publication de cette version.

### Compatibilité
- Le domaine `econergy`, les identifiants uniques et le parcours OAuth restent inchangés, à l'exception de la migration nécessaire lorsque l'API fournit `replacedBy`.
- Aucun appel de commande n'est automatiquement rejoué après une réponse 410.

# Changelog

## 2.1.12 — bêta — 18 novembre 2026

### Actualisations d'état
- Partage une même demande de statut lorsqu'une actualisation automatique et une actualisation manuelle concernent le même radiateur au même moment. La seconde action réutilise la demande en cours au lieu d'envoyer une nouvelle commande.
- Conserve la limite Econergy d'une demande par radiateur et par minute, ainsi que la gestion des réponses HTTP 429 et de `Retry-After`.
- Les simples reports liés au délai minimal (`RATE_LIMIT_COOLDOWN`) ne génèrent plus d'avertissement dans les journaux : ils sont consignés au niveau `DEBUG`. Les erreurs et les actualisations réellement non confirmées restent signalées.

### Lisibilité des journaux
- Remplace les identifiants seuls par le nom du radiateur, suivi de son identifiant entre parenthèses, dans les journaux du coordinateur et du thermostat.
- Applique le même format aux erreurs de lecture des programmes, réglages, consommations, aux demandes de statut et aux modifications de programme.

## 2.1.11 — bêta — 17 novembre 2026

### Suivi des demandes d'actualisation
- Porte à **40 secondes** (au lieu de 20) le délai maximal de suivi de l'acquittement d'une demande de statut envoyée à Econergy, afin de mieux tolérer un traitement plus lent côté cloud.
- Conserve ensuite la vérification de fraîcheur de l'état pendant **30 secondes** : la température n'est considérée comme actualisée que si `state.updatedAt` est postérieur à la demande.
- Ne modifie pas le cycle d'actualisation ciblé sur cinq minutes par radiateur, la limite minimale d'une demande par radiateur et par minute, ni l'intervalle de suivi des commandes de deux secondes.
- Si le cloud ne confirme toujours pas la commande ou ne renvoie pas de nouvel état, l'intégration continue de signaler que l'actualisation n'a pas été confirmée.

## 2.1.10 — bêta — 16 novembre 2026

### Synchronisation et nettoyage des appareils
- Contrôle l'inventaire Econergy une fois par heure au lieu de toutes les cinq minutes.
- Supprime automatiquement du registre Home Assistant les anciens appareils Econergy absents de l'inventaire confirmé, ainsi que leurs entités Econergy, dès l'initialisation puis à chaque synchronisation horaire.
- Ne supprime jamais les appareils encore présents dans la réponse de l'API ; si des entités d'une autre intégration restent associées, l'appareil est conservé.

### Actualisation des températures et respect des limites API
- Maintient le cycle indépendant de demandes de statut radio avec une cible de cinq minutes par radiateur (environ 75 secondes entre deux demandes pour un domicile de quatre radiateurs).
- Conserve le délai minimal d'une minute par radiateur, la persistance des demandes après redémarrage et la gestion des réponses 429/Retry-After ; le changement de cadence de l'inventaire ne modifie pas ces protections.

## 2.1.9 — bêta — 16 novembre 2026

### Organisation de la fiche appareil
- Réordonne visuellement les réglages : « Appareil · Nom du radiateur », butée maximale, consignes Confort et Éco, correction de sonde, puis les trois options de détection de fenêtre, protection enfant et verrouillage du clavier.
- Préserve les anciens identifiants suggérés pour le nom du radiateur et les interrupteurs : les `entity_id` existants ne sont pas renommés et les nouvelles installations conservent les mêmes bases d’identifiants.
- Déplace les informations techniques (date d’installation, communication, remontée d’état, firmware, puissance nominale et statut de commande) dans la catégorie Home Assistant « Diagnostics ». Les capteurs utiles au quotidien restent dans « Capteurs ».

### Notice PDF
- Traite explicitement le code API `MANUAL_NOT_FOUND` comme une absence de document : une notification persistante indique qu'aucun PDF n'est disponible, sans faire échouer l'action `button.press`.
- Si une URL PDF HTTPS est fournie, le lien temporaire reste affiché dans une notification comme auparavant.
- Une erreur API différente de `MANUAL_NOT_FOUND` continue d'être signalée comme une véritable erreur.

## 2.1.7 — bêta — 14 novembre 2026

## Actualisation automatique des températures
- Rétablit les demandes de statut radio automatiques : les radiateurs ne sont plus dépendants d'une remontée spontanée du cloud.
- Les radiateurs sont interrogés séquentiellement et répartis sur un cycle cible de cinq minutes. Avec quatre radiateurs, une demande est lancée environ toutes les 75 secondes, ce qui donne environ une actualisation par radiateur toutes les cinq minutes.
- Respecte un délai minimal de 60 secondes entre deux demandes pour un même radiateur et conserve le bouton « Actualiser les infos » pour une demande manuelle.
- Conserve le dernier état le plus récent si la liste générale du cloud renvoie ensuite un instantané plus ancien.

## Nettoyage des anciens appareils
- Ajoute la prise en charge de la suppression des appareils Econergy dans le registre Home Assistant.
- La suppression est autorisée uniquement lorsque l'identifiant de l'appareil n'est plus présent dans l'inventaire actuel du domicile Econergy.
- Les appareils encore présents dans le compte restent protégés contre la suppression.

## Fiabilité
- Le cycle d'actualisation automatique est arrêté proprement lors du déchargement ou du rechargement de l'intégration.
- Aucun changement d'autorisation OAuth, d'identifiants d'entités, de scripts ou de services existants.


## 2.1.6 — bêta — 12 novembre 2026

- Fusionne les demandes d'actualisation de l'état et de la consommation dans l'action « Actualiser les infos », en conservant l'identifiant unique de l'ancien bouton d'état.
- Remplace le graphique 15 jours basé sur ApexCharts par des graphiques natifs journaliers Recorder pour l'énergie estimée et la durée de chauffe.
- Simplifie la page « Programmes du radiateur » : retrait de l'activation depuis cette page et passage au vouvoiement dans l'éditeur.
- Harmonise le texte d'information sur les créneaux et le mode Programmation.
- Conserve la route officielle de récupération de notice et remonte les erreurs API sans affirmer à tort que le PDF est absent.

## 2.1.5 — bêta — 12 novembre 2026

### Thermostat et libellés
- Expose `hvac_action` : Home Assistant distingue maintenant le radiateur arrêté, allumé au repos et réellement en chauffe.
- Renomme l'action en « Programmes du radiateur », le réglage en « Butée de température max » et le capteur en « Détection fenêtre ouverte » (état natif Ouvert/Fermé conservé).
- Traduit les statuts techniques des commandes en libellés français, tout en conservant le code API dans les attributs.
- Utilise la même icône d'actualisation pour les deux boutons d'actualisation.

### Lovelace et programmation
- Ajoute des exemples de cartes facultatives pour l'état, la consommation 15 jours/30 jours, les réglages, le diagnostic et les actions.
- La carte 30 jours utilise les identifiants de statistiques externes Recorder Econergy ; la carte 15 jours affiche les dates en JJ/MM.
- Retire les relevés de consommation de la page « Programmes du radiateur » : cette page est désormais réservée à l'éditeur et à l'activation de la programmation.


## 2.1.4 — bêta — 12 novembre 2026

### Tuiles Lovelace
- Ajoute à l'archive de l'intégration des exemples de tuiles Lovelace Econergy, avec les modèles `button_card_templates` réutilisables et une tuile complète pour le Bureau.
- Distingue visuellement les états arrêté, actif sans chauffe et chauffe effective à partir du capteur de fonctionnement publié par l'intégration.
- Conserve un affichage cohérent du mode Hors gel, même lorsque le climate expose `hvac_mode: off`.
- Lit la température ambiante directement depuis l'entité `climate` et adapte les boutons de consigne aux limites réelles `min_temp` et `max_temp`.
- Documente l'installation et la duplication de la tuile pour les autres radiateurs.

### Compatibilité
- Aucun changement des commandes API, de l'autorisation OAuth ou des identifiants uniques des entités.
- Les exemples Lovelace nécessitent la carte personnalisée `custom:button-card` et sont ajoutés manuellement au tableau de bord.

## 2.1.3 — bêta — 12 novembre 2026

### Tuile Lovelace
- Modernise l'exemple de tuile de pilotage des radiateurs en conservant son apparence et ses commandes, avec une structure factorisée et réutilisable via `button_card_templates`.
- Exploite les états Econergy pour distinguer visuellement le radiateur arrêté, allumé sans chauffe et en chauffe effective.
- Utilise directement la température ambiante publiée par l'entité `climate` et adapte les boutons de consigne aux limites `min_temp` et `max_temp` exposées par le radiateur.
- Préserve la dernière consigne manuelle lors des transitions entre les modes arrêt, hors-gel et chauffage.


### Consommation et historique
- Les capteurs de consommation estimée et de durée de chauffe exploitent désormais les relevés disponibles sans se limiter à la dernière journée de la fenêtre API.
- Affiche 0 dans les tuiles lorsqu'une journée existe mais que l'API renvoie `null`, sans transformer cette absence de mesure en zéro dans les données archivées.
- Fusionne chaque nouvelle fenêtre de 15 jours avec l'historique local permanent : les journées antérieures sont conservées et une valeur `null` ne peut pas effacer une mesure déjà connue.
- Enregistre l'archive dans le stockage persistant Home Assistant et importe les valeurs quotidiennes disponibles dans les statistiques long terme du Recorder, pour l'énergie estimée et la durée de chauffe.

### Compatibilité
- Aucune modification de l'autorisation OAuth ni de la configuration des radiateurs.
- Les identifiants uniques des entités existantes sont conservés.

## 2.1.2 — bêta — 12 novembre 2026

### Correctifs
- Corrige le cycle de vie de l'écouteur ponctuel `homeassistant_started` : il n'est plus désinscrit une seconde fois lors du déchargement de l'intégration.
- Conserve une désinscription explicite si l'intégration est déchargée avant le démarrage complet de Home Assistant.

### Compatibilité
- Version bêta ; aucune modification de l'autorisation OAuth ni de la configuration des appareils.

## 2.1.1 — bêta — 11 novembre 2026

### Correctifs
- Corrige la classe d'état des capteurs de consommation énergétique : les consommations journalières utilisent désormais `total`, tandis que la durée de chauffe conserve `measurement`.
- Améliore le capteur « Régime appliqué » : interprète le mode réel du radiateur et, en mode programmation, la consigne et le créneau hebdomadaire courant lorsque l'API ne fournit pas `setpointKind`.
- Conserve le statut de la dernière commande dans le stockage Home Assistant afin de le retrouver après un redémarrage. Affiche « Aucune commande enregistrée » lorsqu'aucune commande n'a encore été suivie.
- Affiche une notification informative lorsque l'API renvoie `MANUAL_NOT_FOUND`, sans faire échouer l'action du bouton.

### Compatibilité
- Aucun changement de configuration OAuth requis.
- L'entrée Econergy existante et ses appareils sont conservés lors de la mise à jour.

# Econergy Cloud — historique des versions

## 2.1.0 — bêta — couverture de l'API publique Econergy Lab

- Ajout des routes documentées `GET/PATCH /devices/{deviceId}/settings` : butée maximale, verrouillage clavier et protection enfant.
- Ajout de `GET /devices/{deviceId}/consumption` : 15 jours de durée de chauffe et d'énergie estimée, cache quotidien.
- Ajout de `GET /devices/{deviceId}/manual` : récupération à la demande d'un lien PDF temporaire.
- Ajout des états runtime `heating`, `windowOpen`, `fanBoost`, `setpointKind`.
- Mise en cohérence avec l’API 1.9 : manuel à partir de 13,5 °C, hors-gel affiché à 7,5 °C et consigne maximale respectée dans l’entité climate et l’éditeur.
- Ajout de `GET /devices/{deviceId}/status` et conservation des dates de fraîcheur d'état.
- Boutons d'action sur la fiche du radiateur : programmer, actualiser l'état, télécharger la notice.
- Retrait du lien générique « Visiter » ; le bouton « Programmer le radiateur » ouvre directement l'éditeur hebdomadaire.
- Renommage conforme à la limite API de 50 caractères ; champ vide pour revenir au nom calculé.
- Les écritures de réglages utilisent exclusivement les routes et paramètres publiés par Econergy et sont vérifiées par relecture.
- La lecture automatique ne réveille plus les radiateurs : la demande radio est réservée au bouton d'actualisation et à la vérification des commandes.

## 2.0.0b2 — bêta locale précédente

- Première version OAuth locale avec éditeur de programme hebdomadaire.
- Pilotage des radiateurs, demande d'actualisation d'état et renommage.
