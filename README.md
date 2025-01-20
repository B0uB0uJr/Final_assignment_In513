# Final_assignment_In513

# Scheduler Task Simulation

Ce projet contient une classe `Scheduler` permettant de tester différentes permutations d’un ensemble de tâches temps réel et d’évaluer la viabilité de leur exécution. Il inclut :

- Le calcul de l’hyper-période.
- La génération de toutes les permutations possibles.
- La simulation de l’exécution des tâches et le calcul des temps d’attente.
- La vérification de la viabilité d’une séquence.
- La recherche de la séquence optimale selon le temps d’attente minimal.

## Comment ça marche ?
1. **Définir votre jeu de tâches** : chaque tâche est un dictionnaire avec un nom (`"name"`), un temps d’exécution (`"C_i"`) et une période (`"period"`).
2. **Instancier un Scheduler** : vous pouvez spécifier une tâche pouvant dépasser sa période (champ `ignoredTaskName`).
3. **Calculer l’hyper-période** : via `computeHyperPeriod()`.
4. **Générer toutes les permutations** : grâce à `listAllArrangements()`.
5. **Simuler chaque permutation** : avec `simulateSystem()`, vous obtenez les temps de réponse et le temps d’inactivité.
6. **Vérifier la viabilité** : via `isArrangementViable()`.
7. **Trouver la meilleure permutation** : en comparant les résultats (temps d’attente minimal).

## Remarque sur les résultats
Lors des tests, les seules configurations viables observées (temps de réponse respecté dans les périodes) apparaissent lorsque l’on autorise un dépassement pour les tâches **T1** et **T2**.

- **Pour T1** :
  - Nombre de séquences viables : 2160 sur 5040
  - Configuration optimale : `['T3', 'T4', 'T5', 'T2', 'T1', 'T6', 'T7']`
  - Score d'attente minimal : 137
  - Inactivité processeur : 8

- **Pour T2** :
  - Nombre de séquences viables : 2208 sur 5040
  - Configuration optimale : `['T1', 'T3', 'T4', 'T5', 'T6', 'T2', 'T7']`
  - Score d'attente minimal : 127
  - Inactivité processeur : 8

## Exécution
- Assurez-vous d’avoir Python 3 installé.
- Clonez ce dépôt.
- Exécutez le fichier principal :

```bash
python main.py
