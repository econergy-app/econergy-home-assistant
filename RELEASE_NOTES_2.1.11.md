# Econergy Cloud 2.1.11 — Bêta

## Suivi des demandes d'actualisation
- Le délai maximal de suivi de l'acquittement d'une demande de statut Econergy passe de 20 à 40 secondes, afin de mieux tolérer les retards de traitement côté cloud.
- La vérification d'un nouvel état reste limitée à 30 secondes après le suivi de commande. Une actualisation n'est confirmée que si `state.updatedAt` est postérieur à la demande.
- Le cycle ciblé sur cinq minutes par radiateur, la limite d'une demande par radiateur et par minute et le suivi des commandes toutes les deux secondes restent inchangés.
- Si aucun nouvel état n'est reçu dans les délais, l'intégration continue de signaler que l'actualisation n'a pas été confirmée.

**Statut :** version bêta.
