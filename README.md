# Econergy Home Assistant — Econergy Cloud

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://www.hacs.xyz/)
[![Version bêta](https://img.shields.io/badge/version-2.1.13--b%C3%AAta-orange.svg)](https://github.com/econergy-app/econergy-home-assistant/releases)

Intégration Home Assistant pour les radiateurs Econergy / Carrera, développée en collaboration avec Econergy et basée sur l'API officielle SmartHome.

> **Version bêta :** l'intégration est développée en collaboration avec Econergy, mais reste en phase de test. L'accès des utilisateurs est actuellement limité aux domiciles de test ajoutés manuellement dans l'application Econergy Lab. Le domicile doit être premium et l'utilisateur doit en être administrateur. Contacte le mainteneur avant l'installation pour faire ajouter ton domicile de test.

## Fonctionnalités

- Découverte des domiciles autorisés par le compte Econergy et des radiateurs associés. L’identité Home Assistant de chaque radiateur repose sur son `deviceId` Econergy, jamais sur son nom ou son emplacement.
- Entité `climate` : arrêt, hors-gel, manuel et programmation ; température ambiante et consigne.
- Programmation hebdomadaire avec un éditeur en français : sept jours, jusqu'à trois plages Confort par jour, consignes Éco/Confort et copie des réglages entre jours. L'activation du mode Programmation reste gérée depuis le pilotage du radiateur.
- Réglages : butée de température max, protection enfant, verrouillage du clavier, activation/désactivation de la détection de fenêtre ouverte et correction manuelle de la sonde (−8 à +8 °C).
- Capteurs : température ambiante, puissance nominale, firmware, date d'installation, dernière communication, dernière remontée d'état, régime appliqué, état de chauffe, détection de fenêtre ouverte et consommation estimée.
- Actualisation automatique des températures par demande de statut radio, avec un cycle cible d'environ cinq minutes par radiateur et un espacement minimal de 60 secondes entre demandes.
- Actions : actualisation combinée manuelle de l'état et de la consommation, renommage du radiateur et récupération de la notice PDF via l'API Econergy. Si aucun PDF n'est publié (`MANUAL_NOT_FOUND`), une notification informative s'affiche sans erreur de service.
- Contrôle de l'inventaire Econergy une fois par heure ; suppression automatique des anciens appareils et de leurs entités Home Assistant lorsque leurs identifiants ne sont plus renvoyés par l'API, dès le démarrage puis à chaque synchronisation horaire.
- Archivage durable des relevés journaliers de consommation estimée et de durée de chauffe, avec import dans les statistiques long terme de Home Assistant.
- Suivi des commandes avec attente de leur confirmation par l'API ; le dernier statut est conservé après un redémarrage de Home Assistant et aucune commande incertaine n'est renvoyée automatiquement.
- Régime appliqué déterminé à partir de l'état du radiateur et, en mode Programmation, de la consigne et du créneau hebdomadaire en cours.
- Authentification OAuth 2.0 avec PKCE ; aucun mot de passe Econergy ni jeton à copier dans YAML.
- Exemples Lovelace facultatifs : tuile de pilotage de base, état détaillé, réglages, diagnostic, actions, graphique des 15 derniers jours et statistiques sur 30 jours.

## Accès bêta et prérequis

L'application Econergy Lab est actuellement en mode test. Les utilisateurs ne peuvent pas encore autoriser librement leur domicile : le mainteneur doit l'ajouter à la liste des domiciles de test dans le tableau de bord Econergy Lab. Pour participer, contacte le mainteneur et communique l'identifiant de ton domicile. Tu dois en être administrateur et le domicile doit être premium (compteur Linky enregistré dans l'application Econergy). Cette étape manuelle disparaîtra lorsque Econergy aura validé et ouvert l'application à tous les utilisateurs.

Le scope OAuth `multihome` est demandé pour tous les comptes. Il permet à Econergy de proposer plusieurs domiciles sur l'écran de consentement, mais ne gêne pas les utilisateurs qui n'en possèdent qu'un. Chaque domicile autorisé est ensuite configuré dans Home Assistant au moyen d'une entrée distincte.

## Installation avec HACS / Marketplace

Le dépôt doit d'abord être ajouté comme dépôt personnalisé :

1. Ouvre **Paramètres → Marketplace** dans Home Assistant.
2. Choisis **Ajouter à partir d'un lien**.
3. Saisis `econergy-app/econergy-home-assistant` (ou `https://github.com/econergy-app/econergy-home-assistant`).
4. Sélectionne le type **Intégration**, puis valide.
5. Télécharge **Econergy Cloud** et redémarre Home Assistant.
6. Va dans **Paramètres → Appareils et services → Ajouter une intégration**, puis recherche **Econergy Cloud**.
7. Termine l'autorisation Econergy dans la fenêtre OAuth. L'application demande `readonly`, `write` et `multihome`. Econergy confirme que `multihome` n'a aucun effet négatif pour un compte avec un seul domicile. Pour plusieurs domiciles, sélectionne ceux que tu souhaites autoriser sur la page de consentement Econergy ; dans Home Assistant, crée une entrée distincte pour chaque domicile à piloter.

Après une mise à jour HACS, redémarre Home Assistant si nécessaire. Ne supprime pas l'entrée d'intégration lors d'une mise à jour : elle contient l'autorisation OAuth.

## Installation manuelle

1. Télécharge le dépôt et décompresse-le.
2. Copie `custom_components/econergy` vers `/config/custom_components/econergy`.
3. Redémarre Home Assistant.
4. Ajoute **Econergy Cloud** depuis **Appareils et services** et termine l'autorisation OAuth.

## Programmation hebdomadaire

Sur la fiche de chaque radiateur, utilise l'action **Programmes du radiateur**. L'éditeur présente les jours de la semaine et permet de définir jusqu'à trois plages Confort par jour. En dehors de ces plages, le radiateur reste en Éco.

L'enregistrement du planning et l'activation du mode `PROG` sont deux opérations distinctes : après avoir sauvegardé les horaires, active le mode Programmation pour que le radiateur les applique.

## Organisation de la fiche appareil

Les réglages sont présentés dans un ordre lisible : identité du radiateur, butée et consignes, correction de sonde, puis les trois interrupteurs regroupés sous « Options ». Les informations purement techniques sont classées dans la catégorie Home Assistant « Diagnostics ». Les identifiants uniques et les identifiants d'entités existants sont conservés.

## Exemples Lovelace facultatifs

Le dossier `custom_components/econergy/examples/lovelace` contient plusieurs cartes indépendantes : tu peux en ajouter seulement certaines à ton tableau de bord.

- `radiateur_bureau.yaml` : tuile de pilotage compacte avec l'indicateur de chauffe réel (modèle de base, nécessite `custom:button-card`).
- `radiateur_bureau_etat.yaml` : état, température, régime, chauffe, fenêtre et ventilateur.
- `radiateur_bureau_consommation.yaml` : graphiques Recorder sur 30 jours à partir des statistiques long terme Econergy.
- `radiateur_bureau_consommation_15_jours.yaml` : graphiques journaliers Recorder des 15 derniers jours, pour l'énergie et la durée de chauffe.
- `radiateur_bureau_reglages.yaml` : consignes Éco/Confort, butée max, protection enfant, verrouillage du clavier, détection de fenêtre et correction de sonde.
- `radiateur_bureau_diagnostic.yaml` : firmware, puissance, dernière communication et statut de commande.
- `radiateur_bureau_actions.yaml` : actualisation, programmation et notice.

Les exemples sont fournis pour `climate.econergy_bureau`. Les identifiants des radiateurs et certains `entity_id` peuvent différer selon le nom et l'historique de ton installation : vérifie-les dans **Paramètres → Appareils et services → Econergy → Bureau** avant de coller une carte.

**Historique de consommation :** les relevés du cloud sont importés comme statistiques long terme externes, avec des identifiants de la forme `econergy:<identifiant_du_radiateur>_estimated_consumption` et `econergy:<identifiant_du_radiateur>_heating_duration`. La carte `statistics-graph` doit utiliser ces identifiants de statistiques, pas les entités `sensor.*` qui n'exposent que la dernière journée. L'onglet Historique natif d'une entité Home Assistant montre les changements d'état de cette entité ; il ne présente pas les statistiques externes. Après la mise à jour, appuie une fois sur **Actualiser les infos** sur le radiateur pour actualiser l'état, relire la consommation et relancer l'import des jours archivés dans Recorder. Le graphique 30 jours affiche alors les jours disponibles (jusqu'aux 15 derniers jours fournis par l'API au premier import), puis s'enrichit au fil de l'archivage.

## Graphiques de consommation dans Lovelace

Les entités `Consommation estimée (dernier jour)` et `Durée de chauffe (dernier jour)` exposent seulement le dernier relevé quotidien reçu de l'API. Leur valeur change lors d'une nouvelle actualisation. Elles ne représentent pas l'historique des journées précédentes.

Pour cette raison, les graphiques automatiquement suggérés par Home Assistant à partir de ces entités ne doivent pas être utilisés comme graphiques de consommation journalière historique. Ils affichent les statistiques calculées à partir de la valeur courante de ces capteurs ; si le dernier relevé vaut 0, leurs graphiques peuvent rester à 0 jusqu'au prochain relevé.

Pour représenter chaque journée, utilisez une carte manuelle **Graphique des statistiques** avec l'identifiant externe Recorder Econergy, par exemple :

```yaml
type: statistics-graph
title: Consommation estimée — 30 derniers jours
entities:
  - econergy:68c5597e5cb480c6cc800d66_estimated_consumption
period: day
days_to_show: 30
chart_type: bar
stat_types:
  - state
hide_legend: true
```

Pour la durée de chauffe, utilisez `econergy:68c5597e5cb480c6cc800d66_heating_duration`. Remplacez `68c5597e5cb480c6cc800d66` par l'identifiant du radiateur concerné. Les identifiants externes commencent par `econergy:` ; ils ne sont pas les `entity_id` des capteurs. Vous pouvez les retrouver dans **Paramètres → Outils de développement → Statistiques**.

## Radiateurs réappairés ou supprimés

Depuis l'API 1.12.0, un ancien identifiant de radiateur renvoie HTTP 410 : `DEVICE_REPLACED` avec `details.replacedBy` lorsqu'il a été réinitialisé puis appairé de nouveau, ou `DEVICE_DELETED` lorsqu'il a été retiré sans remplacement. L'intégration vérifie l'inventaire, migre l'identifiant du registre Home Assistant et les identifiants uniques de ses entités lorsque le remplacement est confirmé, puis recharge l'entrée pour reconstruire les entités. Les `entity_id` sont conservés lorsque la migration ne rencontre aucun conflit. L'archive locale de consommation est transférée vers le nouvel identifiant et les statistiques correspondantes sont réimportées. Aucun ordre de chauffage n'est rejoué automatiquement sur le nouvel appareil.

## Données et limites connues

- En mode `FROST`, le thermostat affiche désormais la valeur `state.setpointC` renvoyée par l'API Econergy (7 °C selon la documentation 1.10.0), et non une valeur codée en dur.
- Le capteur `windowOpen` indique une ouverture détectée. L’interrupteur « Activation détection de fenêtre » commande séparément le réglage `windowDetection`.
- La correction de sonde `calibrationC` est un réglage manuel de −8 à +8 °C par pas de 1 °C. `state.measuredC` est déjà corrigé par Econergy : l’intégration ne lui applique aucune correction supplémentaire. Ne modifie ce réglage qu’après comparaison avec un thermomètre.
- Le code `HOME_SUSPENDED` signifie que le pilotage du domicile est suspendu par Econergy : les lectures restent disponibles, mais les commandes et modifications sont refusées.
- La notice est demandée à l'API via `GET /devices/{deviceId}/manual?lang=fr`. Si un lien HTTPS est disponible, il est proposé dans une notification. Si l'API renvoie `MANUAL_NOT_FOUND` ou ne fournit aucun lien PDF, une notification indique que la notice n'est pas disponible ; les autres erreurs API restent signalées.
- L'endpoint de consommation utilisé par l'intégration retourne les 15 dernières journées complètes, mais l'intégration les archive durablement dans Home Assistant et alimente ses statistiques long terme. Les valeurs restent des estimations calculées à partir de la durée de chauffe et de la puissance nominale ; ce ne sont pas des relevés Linky ni des mesures électriques directes. Lorsqu'une journée est renvoyée sans mesure (`null`), la tuile affiche `0` par convention, tandis que l'archive conserve l'absence de donnée.
- L'inventaire cloud (GET /homes/{homeId}/devices) est contrôlé une fois par heure. Indépendamment, l'intégration demande une nouvelle remontée d'état radio toutes les cinq minutes environ par radiateur : avec quatre radiateurs, une demande est espacée d'environ 75 secondes. Le délai minimal de 60 secondes par radiateur, la persistance des dernières demandes et le respect des réponses 429/Retry-After sont conservés. Ce cycle actualise les températures et les états sans attendre le prochain contrôle de l'inventaire. Le bouton « Actualiser les infos » reste disponible pour forcer une demande manuelle.
- Les scénarios, configurations avancées, gestion des membres et les commandes de présence/absence ne sont pas exposés par les routes publiques actuellement utilisées/documentées par cette version ; ils ne sont pas simulés par l'intégration.

## API utilisée

Base : `https://econergy-app.fr/api/smarthome/v1`

Routes utilisées par cette version :

- `GET /me`, `GET /homes`, `GET /homes/{homeId}/devices`
- `GET /devices/{deviceId}/status`, `PATCH /devices/{deviceId}`
- `GET /devices/{deviceId}/settings`, `PATCH /devices/{deviceId}/settings`
- `GET /devices/{deviceId}/program`, `PATCH /devices/{deviceId}/program`
- `GET /devices/{deviceId}/consumption`, `GET /devices/{deviceId}/manual?lang=fr`
- `POST /devices/{deviceId}/status-request`
- `POST /devices/{deviceId}/commands`, `GET /commands/{commandId}`

Documentation officielle de l'API : https://econergy-app.fr/lab/doc

Dépôt du projet : https://github.com/econergy-app/econergy-home-assistant

## Sécurité et confidentialité

- OAuth 2.0 Authorization Code avec PKCE ; aucun `client_secret` n'est intégré.
- Les jetons sont stockés dans l'entrée Home Assistant et ne doivent jamais être publiés dans une issue ou un journal.
- Les diagnostics Home Assistant retirent les données d'authentification.
- Ne partage jamais de capture contenant des jetons, codes OAuth ou identifiants de compte.

## Signaler un problème

Ouvre une issue en indiquant la version Home Assistant, la version de l'intégration, le modèle du radiateur et les étapes pour reproduire le problème. **N'ajoute jamais de mot de passe, jeton OAuth, code d'autorisation ou identifiant privé.**

## Licence

MIT — voir [LICENSE](LICENSE).
