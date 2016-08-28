import json
import pickle
import random
import argparse
import copy
from individual import Individual, Node

def main(popCount = 100, genMax = None, checkpoint=None):
    gen = 0
    population = []
    if checkpoint:
        # A file name has been given, then load the data from the file
        try:
            with open(checkpoint, "r+b") as cp_file:
                data = pickle.load(cp_file)
            if data["population"]:
                gen=data["gen"]
                if not genMax:
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
            if gen % 100 == 0:
                save(checkpoint, population, gen, genMax)
            random.shuffle(population)
            for p1, p2 in pairwise(population):
                play(p1,p2)
            population.sort(key=evalFitness)
            recombine(population)
            gen += 1
    except (KeyboardInterrupt, SystemExit):
        if checkpoint:
            save(checkpoint, population, gen, genMax)
        else:
            checkpoint = input("If you want to save this, input a file name now.")
            if len(checkpoint) > 0:
                save(checkpoint, population, gen, genMax)
    stats = []
    population.sort(key=evalFitness)
    for x in population[:int(len(population)/4)]:
        stats.append(x.stats())
    if checkpoint:
        with open(checkpoint + ".res", "w") as f:
            json.dump(stats, f, indent=4, sort_keys=True)
def generate(popCount):
    print("generated popcount things");
    l = []
    starting = [0,0,0,0,1,1,1,1]
    for x in range(popCount):
        moveDir = (0,0)
        while moveDir ==(0,0):
            moveDir = (random.randint(-1,1),random.randint(-1,1))
        root = Node(random.randrange(6),random.randrange(8),bool(random.getrandbits(1)),moveDirection=moveDir)
        l.append(Individual(root,random.sample(starting,8)))
    return l

def play(p1,p2):
    board = {}
    for x in range(8):
        for y in range(8):
            board[x,y] = 0
    p1CapturedGood = 0
    p1CapturedBad = 0
    p2CapturedGood = 0
    p2CapturedBad = 0
    for x in range(2,6):
        board[x,0] = p1.starting[x-2]
        board[x,1] = p1.starting[x+2]
        board[x,7] = -p2.starting[x-2]
        board[x,6] = -p2.starting[x+2]
    while True:
        for x in range(100):
            move = p1.next(board, False)
            if x==100 or move[0] == False:
                p2.win+=1
                p1.loss+=1
                p1.capturedBad += p1CapturedBad
                p1.capturedGood += p1CapturedGood
                p2.capturedBad += p2CapturedBad
                p2.capturedGood += p2CapturedGood
                return
            if board[move[1]] < 1:
                break;
        piece = board[move[0]]
        board[move[0]] = 0
        if board[move[1]] == -2:
            p2CapturedBad+=1
        elif board[move[1]] == -1:
            p2CapturedGood+=1
        board[move[1]] = piece
        if board[0,7] == 1 or board[7,7] == 1 or p1CapturedBad == 4 :
            p1.win+=1
            p1.sneakyWin += 1
            p2.loss+=1
            p1.capturedBad += p1CapturedBad
            p1.capturedGood += p1CapturedGood
            p2.capturedBad += p2CapturedBad
            p2.capturedGood += p2CapturedGood
            return
        elif p2CapturedGood == 4:
            p1.win+=1
            p2.loss+=1
            p1.capturedBad += p1CapturedBad
            p1.capturedGood += p1CapturedGood
            p2.capturedBad += p2CapturedBad
            p2.capturedGood += p2CapturedGood
            return
        for x in range(100):
            move = p2.next(board, True)
            if x == 100 or move[0] == False:
                p1.win+=1
                p2.loss+=1
                p1.capturedBad += p1CapturedBad
                p1.capturedGood += p1CapturedGood
                p2.capturedBad += p2CapturedBad
                p2.capturedGood += p2CapturedGood
                return
            if board[move[1]] > -1:
                break;
        piece = board[move[0]]
        board[move[0]] = 0
        if board[move[1]] == 2:
            p2CapturedBad+=1
        elif board[move[1]] == 1:
            p2CapturedGood+=1
        board[move[1]] = piece
        if p2CapturedBad == 4 or board[0,0] == -1 or board[0,7] == -1:
            p2.win+=1
            p2.sneakyWin += 1
            p1.loss+=1
            p1.capturedBad += p1CapturedBad
            p1.capturedGood += p1CapturedGood
            p2.capturedBad += p2CapturedBad
            p2.capturedGood += p2CapturedGood
            return
        elif p1CapturedGood == 4:
            p2.win+=1
            p1.loss+=1
            p1.capturedBad += p1CapturedBad
            p1.capturedGood += p1CapturedGood
            p2.capturedBad += p2CapturedBad
            p2.capturedGood += p2CapturedGood
            return
def evalFitness(individual):
    return 1 - individual.win/(individual.win + individual.loss)

def recombine(population, mutChance = 0.25):
    selectionIndex = 25  #int(len(population)/4)
    for x in range(selectionIndex, len(population)):
        parent = population[random.randrange(selectionIndex)].copy()
        graftOn = random.choice(parent[1])
        graftee = random.choice(population[random.randrange(selectionIndex)].copy()[1])
        if bool(random.getrandbits(1)):
            graftOn.passed = graftee
        else:
            graftOn.failed = graftee
        if random.random() < mutChance:
            choice = random.randrange(6)
            unlucky = random.choice(parent[1])
            if choice == 1:
                unlucky.failed = False
            elif choice == 2:
                unlucky.passed = False
            elif choice == 3:
                unlucky.cutoff = random.randrange(8)
            elif choice == 4:
                unlucky.direction = bool(random.getrandbits(1))
            elif choice == 5:
                unlucky.selector = random.randrange(6)
    print("new population, best" + str(population[0].win/(population[0].win+population[0].loss)))

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

def save(checkpoint, population, gen, genMax):
    with open(checkpoint + ".sav", "w+b") as f:
        data = {};
        data["gen"] = gen
        data["genMax"] = genMax
        data["population"] = population
        pickle.dump(data, f)
        print("Population saved! Thanks!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--checkpoint", help="If you have a checkpoint file, name it here. Overrides popCount and genMax", type=str)
    parser.add_argument("-p", "--popCount", help="number of individuals in each generation.", type=int, default=100)
    parser.add_argument("-g", "--genMax", help="number of generations to iterate through.", type=int, default=100)
    args = parser.parse_args()
    main(args.popCount,args.genMax, args.checkpoint)