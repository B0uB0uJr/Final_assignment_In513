# -*- coding: utf-8 -*-
from math import gcd

class Scheduler:
    def __init__(self, tasksSet, ignoredTaskName=None):
        """
        :param tasksSet: liste de dictionnaires, chacun représentant une tâche
        :param ignoredTaskName: nom de la tâche pouvant tolérer un dépassement
        """
        self.tasksSet = tasksSet
        self.ignoredTaskName = ignoredTaskName


    def computeHyperPeriod(self, periodsList):
        """
        Calcule la période globale en combinant tous les T_i
        :param periodsList: liste de périodes
        :return: la période globale
        """
        accum = periodsList[0]
        for value in periodsList[1:]:
            accum = abs(accum * value) // gcd(accum, value)
        return accum


    def listAllArrangements(self, sequence):
        """
        Génère toutes les permutations possibles d'une séquence
        :param sequence: liste d'éléments
        :return: un générateur d'arrangements
        """
        if len(sequence) <= 1:
            yield sequence
        else:
            for idx in range(len(sequence)):
                subPart = sequence[:idx] + sequence[idx+1:]
                for subCombo in self.listAllArrangements(subPart):
                    yield [sequence[idx]] + subCombo


    def simulateSystem(self, arrangement, globalPeriod):
        """
        Simule l'exécution des tâches dans un certain ordre, calcule les temps de réponse et le temps d'inactivité
        :param arrangement: ordre des tâches (liste de dicos)
        :param globalPeriod: hyper-période calculée
        :return: un dictionnaire contenant les temps de réponse, ainsi que le temps d'inactivité
        """
        tasksInTime = []
        # Construire la liste des tâches (jobs) à l'intérieur de l'hyper-période
        for item in arrangement:
            howManyInHyper = globalPeriod // item["period"]
            for timeslot in range(howManyInHyper):
                tasksInTime.append({
                    "refName":       item["name"],
                    "executionTime": item["C_i"],
                    "period":        item["period"],
                    "startPoint":    timeslot * item["period"],
                    "timeLeft":      item["C_i"]
                })

        # Ordonner ces "jobs" en fonction de leur arrivée
        tasksInTime.sort(key=lambda x: x["startPoint"])

        # Dictionnaire pour stocker les temps de réponse
        answerTimeRecords = {}
        for elem in arrangement:
            answerTimeRecords[elem["name"]] = []

        timeIndex = 0
        idleDurations = 0

        # Exécution en pas de 1 unité de temps
        while tasksInTime:
            # Récupérer les tâches prêtes à être exécutées
            readyList = []
            for job in tasksInTime:
                if job["startPoint"] <= timeIndex and job["timeLeft"] > 0:
                    readyList.append(job)

            if readyList:
                # Prendre la première, à la FCFS
                currentJob = readyList[0]
                currentJob["timeLeft"] -= 1

                # Si elle se termine
                if currentJob["timeLeft"] == 0:
                    actualFinish = timeIndex + 1 - currentJob["startPoint"]
                    answerTimeRecords[currentJob["refName"]].append(
                        (actualFinish, currentJob["executionTime"])
                    )
            else:
                idleDurations += 1

            timeIndex += 1

            # On ne garde que les tâches dont le "timeLeft" n'est pas épuisé
            nextCycle = []
            for job in tasksInTime:
                if job["timeLeft"] > 0:
                    nextCycle.append(job)
            tasksInTime = nextCycle

        return answerTimeRecords, idleDurations


    def computeWaitingCost(self, answerTimeRecords):
        """
        Calcule la somme des attentes (temps de réponse - exécution)
        :param answerTimeRecords: dictionnaire de listes (fin d'exécution, C_i)
        :return: somme cumulée des temps d'attente
        """
        totalCost = 0
        for refName, dataPoints in answerTimeRecords.items():
            for (finishTime, duration) in dataPoints:
                waitSpan = finishTime - duration
                totalCost += waitSpan
        return totalCost


    def isArrangementViable(self, arrangement, answerTimeRecords):
        """
        Vérifie la viabilité d'un arrangement.
        Soit le temps de réponse est contenu dans T_i, soit la tâche est celle qu'on ignore.
        :param arrangement: liste des tâches
        :param answerTimeRecords: données sur les temps de réponse
        :return: booléen
        """
        allConstraints = []
        for refName, measures in answerTimeRecords.items():
            for (finVal, _) in measures:
                periodVal = None
                for dic in self.tasksSet:
                    if dic["name"] == refName:
                        periodVal = dic["period"]
                        break

                constraint = (finVal <= periodVal) or (refName == self.ignoredTaskName)
                allConstraints.append(constraint)

        # L'arrangement est viable si toutes les contraintes sont satisfaites
        return all(allConstraints)


def main():
    # Ensemble de tâches : chaque item est un dictionnaire
    tasksSet = [
        {"name": "T1", "C_i": 2, "period": 10},
        {"name": "T2", "C_i": 3, "period": 10},
        {"name": "T3", "C_i": 2, "period": 20},
        {"name": "T4", "C_i": 2, "period": 20},
        {"name": "T5", "C_i": 2, "period": 40},
        {"name": "T6", "C_i": 2, "period": 40},
        {"name": "T7", "C_i": 3, "period": 80}
    ]

    # Tâche pouvant tolérer un dépassement
    ignoredTaskName = None

    # Instancier la classe Scheduler
    sched = Scheduler(tasksSet, ignoredTaskName)

    # Calculer la période globale (hyper-période)
    globalPeriod = sched.computeHyperPeriod([task["period"] for task in tasksSet])
    print(f"Période globale calculée : {globalPeriod}")

    # Générer toutes les permutations (listAllArrangements) de la liste de tâches
    allPossibleOrders = list(sched.listAllArrangements(tasksSet))
    print(f"Nombre total d'ordres possibles : {len(allPossibleOrders)}")
    
    validConfigs = []
    # Tester chaque permutation
    for pattern in allPossibleOrders:
        # Simuler
        answers, idleLen = sched.simulateSystem(pattern, globalPeriod)
        # Calculer le temps d'attente cumulé
        waitScore = sched.computeWaitingCost(answers)
        # Vérifier la viabilité
        viableArrangement = sched.isArrangementViable(pattern, answers)

        # Affichage en fonction du résultat
        if viableArrangement:
            validConfigs.append((pattern, answers, waitScore, idleLen))
            print(f"\nSéquence : {[job['name'] for job in pattern]}")
            print(f"  Attente cumulée : {waitScore}")
            print(f"  Inactivité totale : {idleLen}")

    print(f"\nNombre de séquences viables : {len(validConfigs)} sur {len(allPossibleOrders)}")

    # Recherche de la configuration offrant le plus faible temps d'attente total
    bestWaitTime = float('inf')
    bestIdleTime = None
    bestOrder = None
    bestAnswers = None

    for arrangement, recTimes, waitSum, idleSum in validConfigs:
        if waitSum < bestWaitTime:
            bestWaitTime = waitSum
            bestIdleTime = idleSum
            bestOrder = arrangement
            bestAnswers = recTimes

    # Affichage final
    if bestOrder:
        print(f"\nConfiguration optimale : {[it['name'] for it in bestOrder]}")
        print(f"  Score d'attente minimal : {bestWaitTime}")
        print(f"  Inactivité processeur : {bestIdleTime}")
        for refName, finalData in bestAnswers.items():
            finishing = [val for val, _ in finalData]
            print(f"  {refName} : Fin = {finishing}")
    else:
        print("\nAucune configuration viable identifiée.")


if __name__ == "__main__":
    main()
