import pickle
import random
import argparse


def main(popCount = 100, genMax = 1000, checkpoint=None):
    gen = 0
    population = []
    if checkpoint:
        # A file name has been given, then load the data from the file
        try:
            with open(checkpoint, "r+b") as cp_file:
                data = pickle.load(cp_file)
            if data["population"]:
                gen=data["gen"]
                genMax=data["genMax"]
                population = data["population"]
            else:
                population = generate(popCount)
        except IOError:
            print("Something was wrong with the checkpoint file. Or it doesn't exist. If you expected this, you're fine.")
            population = generate(popCount)
    else:
        population = generate(popCount)
    try:
        while gen < genMax:
            random.shuffle(population)
            for p1, p2 in pairwise(population):
                play(p1,p2)
            population.sort(key=evalFitness)
            recombine(population)
            gen += 1
    except (KeyboardInterrupt, SystemExit):
        if checkpoint:
            with open(checkpoint, "w+b") as f:
                data = {};
                data["gen"] = gen
                data["genMax"] = genMax
                data["population"] = population
                pickle.dump(data, f)
                print("Population saved! Thanks!")
        else:
            checkpoint = input("If you want to save this, input a file name now.")
            if len(checkpoint) > 0:
                with open(checkpoint, "w+b") as f:
                    data = {};
                    data["gen"] = gen
                    data["genMax"] = genMax
                    data["population"] = population
                    pickle.dump(data, f)
                    print("Population saved! Thanks!")

def generate(popCount):
    print("generated popcount things");
    l = []
    for x in range(popCount):
        l.append(x)
    return l

def play(p1,p2):
    print(str(p1) + " and " + str(p2))
    total = p1+p2
    rand = random.random()
    if(rand < p1/total):
        p1+=1
    else:
        p2+=1

def evalFitness(individual):
    return -individual

def recombine(population):
    for x in range(len(population)):
        if population[x]/10 < random.random():
            population[x] = random.randint(1,10)
    print("new population " + str(population))

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--checkpoint", help="If you have a checkpoint file, name it here. Overrides popCount and genMax", type=str)
    parser.add_argument("-p", "--popCount", help="number of individuals in each generation.", type=int, default=100)
    parser.add_argument("-g", "--genMax", help="number of generations to iterate through.", type=int, default=100)
    args = parser.parse_args()
    main(args.popCount,args.genMax, args.checkpoint)