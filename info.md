Intégration Home Assistant des radiateurs Econergy / Carrera, basée sur l'API officielle SmartHome et développée en collaboration avec Econergy.

L'intégration prend en charge un ou plusieurs domiciles autorisés par le compte Econergy. Chaque domicile est configuré comme une entrée distincte dans Home Assistant.

Elle fournit le pilotage du chauffage, la programmation hebdomadaire, les réglages, les capteurs de diagnostic, l'archivage des consommations journalières et la gestion des radiateurs réappairés ou supprimés.

Les derniers états et températures connus du cloud sont lus toutes les dix minutes. Tant que les firmwares ne transmettent pas régulièrement les températures spontanément, l'interrupteur « Actualisation forcée des températures » est activé par défaut. Il apparaît dans la section « Diagnostics » de chaque radiateur et commande le cycle radio de tout le domicile : une vague toutes les cinq minutes, avec cinq secondes d'espacement entre les demandes. Une notification Home Assistant est créée lorsqu'une nouvelle version de firmware est détectée.

Les diagnostics et journaux masquent partiellement les identifiants des domiciles et des radiateurs, en conservant les quatre derniers caractères.

Dépôt : https://github.com/econergy-app/econergy-home-assistant
Documentation API officielle : https://econergy-app.fr/lab/doc

## Historique et graphiques de consommation

Les capteurs « Consommation estimée (dernier jour) » et « Durée de chauffe (dernier jour) » exposent uniquement la dernière journée complète renvoyée par l'API Econergy. Leur valeur est remplacée lors de la prochaine actualisation : ils ne constituent pas un historique journalier.

Pour afficher l'historique quotidien, ajoute une carte **Graphique des statistiques** en mode YAML et utilise l'identifiant de statistique externe Econergy (préfixe `econergy:`). Remplace l'identifiant d'exemple par celui de ton radiateur. Ces statistiques externes sont distinctes des entités `sensor.*` et se consultent dans **Paramètres → Outils de développement → Statistiques**.
