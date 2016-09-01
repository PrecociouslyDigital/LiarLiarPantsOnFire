import pickle
import pprint
import argparse

def play(p1,p2):
    board = {}
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
                print("p2 win by timeout")
                return
            if board.get(move[1],0) < 1:
                break;
        piece = board.get(move[0],0)
        del board[move[0]]
        target = board.get(move[1],0)
        if target == -2:
            p2CapturedBad+=1
        elif target == -1:
            p2CapturedGood+=1
        board[move[1]] = piece
        if board.get((7,0),0) == 1 or board.get((7,7),0) == 1:
        	print("p1 win by sneak")
        	return
        if p1CapturedBad == 4 :
            print("p1 win by bad capture")
            return
        elif p2CapturedGood == 4:
            print("p1 win by capturing all good")
            return
        for x in range(100):
            move = p2.next(board, True)
            if x == 100 or move[0] == False:
                print("p1 win by timeout")
                return
            if board.get(move[1],0) > -1:
                break;
        piece = board.get(move[0],0)
        del board[move[0]]
        target = board.get(move[1],0)
        if target == 2:
            p2CapturedBad+=1
        elif target == 1:
            p2CapturedGood+=1
        board[move[1]] = piece
        if p2CapturedBad == 4:
        	print("p2 win by bad capture")
        	return
        if board.get((0,0),0) == -1 or board.get((0,7),0) == -1:
            print("p2 win by sneak")
            return
        elif p1CapturedGood == 4:
            print("p2 win by capturing all good")
            return


parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to examine", type=str)
#parser.add_argument("individual", help="individual to examine", type=int)
args = parser.parse_args()
with open(args.file + ".sav", "r+b") as cp_file:
	data = pickle.load(cp_file)
	population = data["population"]
	pprint.pprint(population[:10])
	while True:
		print(eval(input("command? \n")))


