from repository import *


class controller():
    def __init__(self):
        self.__repository = repository()
    
    def getMap(self):
        return self.__repository.getMap()

    def getDrone(self):
        return self.__repository.getDrone()

    def iteration(self, population):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors

        individuals = population.getIndividuals()

        i1 = rand.randint(0,len(individuals)-1)
        i2 = rand.randint(0,len(individuals)-1)

        while i1 == i2:
            i2 = rand.randint(0, len(individuals) - 1)

        parent1 = individuals[i1]
        parent2 = individuals[i2]

        offspring1, offspring2 = parent1.crossover(parent2)

        offspring1.mutate()
        offspring2.mutate()

        if offspring1.getFitness() > offspring2.getFitness():
            population.addIndividual(offspring1)
        else:
            population.addIndividual(offspring2)

        
    def run(self, cSeed, popSize, indSize, genCount, nrIterations):
        # args - list of parameters needed in order to run the algorithm
        
        # until stop condition
        #    perform an iteration
        #    save the information needed for the statistics
        
        # return the results and the info for statistics

        rand.seed(cSeed)

        population = Population(self.__repository.getDrone(), self.__repository.getMap(), popSize, indSize)
        self.__repository.addPopulation(population)

        bestIndividual = None
        average = 0

        for g in range(genCount):
            for it in range(nrIterations):
                self.iteration(population)
            population.setIndividuals(population.selection(popSize))
            self.__repository.setLastPopulation(population)

            popFitness = []
            for p in population.getIndividuals():
                popFitness.append(p.getFitness())

            bestIndividual = population.selection(1)[0]
            average = np.average(popFitness)

        return bestIndividual, average
    
    
    def solver(self, popSize, indSize, genCount, nrIterations, lastSeed=5):
        # args - list of parameters needed in order to run the solver
        
        # create the population,
        # run the algorithm
        # return the results and the statistics

        bestIndividuals = []
        averages = []

        for i in range(lastSeed):
            best, avg = self.run(i, popSize, indSize, genCount, nrIterations)
            print(str(i)+"      "+str(avg)+"      "+str(best.getFitness()))
            bestIndividuals.append(best)
            averages.append(avg)

        return bestIndividuals, averages

    def setMap(self,newMap):
        self.__repository.setMap(newMap)