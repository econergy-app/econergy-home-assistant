# Econergy Cloud 2.1.9 — Bêta

## Fiche appareil plus lisible
- Le champ du nom du radiateur apparaît en premier, suivi de la butée maximale, des consignes Confort et Éco et de la correction de sonde.
- Les interrupteurs de détection de fenêtre, protection enfant et verrouillage clavier sont regroupés en fin de section sous « Options ».
- Les informations techniques sont déplacées dans « Diagnostics ».
- Les identifiants d'entités existants et les bases suggérées des nouvelles entités restent préservés.

## Notice PDF
- Si Econergy répond `MANUAL_NOT_FOUND`, Home Assistant affiche une notification indiquant que la notice n'est pas disponible, sans générer d'erreur lors de l'action du bouton.
- Si le PDF est disponible, le lien temporaire est fourni dans une notification.
- Les autres erreurs API restent signalées normalement.
