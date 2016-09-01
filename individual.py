import operator
from collections import deque
def selectClosest(board):
    distance = 0
    selected = False
    for item in board.items():
        if item[1] > 0:
            for other in board.items():
                if other[1] < 0:
                    store = abs(item[0][0] - other[0][0]) + abs(item[0][1] - other[0][1])
                    if store > distance:
                        distance = store
                        selected = item[0]
    return (selected, distance)
def selectFarthest(board):
    distance = 100
    selected = False
    for item in board.items():
        if item[1] > 0:
            for other in board.items():
                if other[1] < 0:
                    store = abs(item[0][0] - other[0][0]) + abs(item[0][1] - other[0][1])
                    if store < distance:
                        distance = store
                        selected = item[0]
    return (selected, distance)
def selectClosestInverted(board):
    distance = 0
    selected = False
    for item in board.items():
        if item[1] < 0:
            for other in board.items():
                if other[1] > 0:
                    store = abs(item[0][0] - other[0][0]) + abs(item[0][1] - other[0][1])
                    if store > distance:
                        distance = store
                        selected = item[0]
    return (selected, distance)
def selectFarthestInverted(board):
    distance = 100
    selected = False
    for item in board.items():
        if item[1] < 0:
            for other in board.items():
                if other[1] > 0:
                    store = abs(item[0][0] - other[0][0]) + abs(item[0][1] - other[0][1])
                    if store < distance:
                        distance = store
                        selected = item[0]
    return (selected, distance)
def backmost(board):
    selected = (7,7)
    for key in board:
        if key[1] < selected [1] and board[key] > 0:
            selected = key
    return (selected, selected[1])
def backmostInverted(board):
    selected = (0,0)
    for key in board:
        if key[1] > selected [1] and board[key] < 0:
            selected = key
    return (selected, 7-selected[1])
def leftmost(board):
    selected = (7,7)
    for key in board:
        if key[0] < selected [0] and board[key] > 0:
            selected = key
    return (selected, selected[0])
def leftmostInverted(board):
    selected = (0,0)
    for key in board:
        if key[0] > selected [0] and board[key] < 0:
            selected = key
    return (selected, 7-selected[0])
def frontmost(board):
    selected = (7,7)
    for key in board:
        if key[1] < selected [1] and board[key] > 0:
            selected = key
    return (selected, selected[1])
def frontmostInverted(board):
    selected = (0,0)
    for key in board:
        if key[1] > selected [1] and board[key] < 0:
            selected = key
    return (selected, 7-selected[1])
def rightmost(board):
    selected = (0,0)
    for key in board:
        if key[0] > selected [0] and board[key] > 0:
            selected = key
    return (selected, 7-selected[0])
def rightmostInverted(board):
    selected = (7,7)
    for key in board:
        if key[0] < selected [0] and board[key] < 0:
            selected = key
    return (selected, selected[0]) 
selectors = [selectClosest, selectFarthest, backmost, frontmost, leftmost, rightmost, selectClosestInverted, selectFarthestInverted, backmostInverted, frontmostInverted, leftmostInverted, rightmostInverted]


class Individual:
    def __init__(this, root, starting):
        this.root = root
        this.current = root
        this.starting = starting
        this.capturedBad = 0
        this.capturedGood = 0
        this.sneakyWin = 0  
        this.win = 0
        this.loss = 0

    def next(this, board,invert):
        for x in range(100):
            result = this.current.next(board, invert)
            if result[1]:
                this.current = result[1]
            else:
                this.current = this.root
            if this.current.moveDirection:
                move = tuple(map(operator.add, result[0], this.current.moveDirection))
                if move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0:
                    continue
                return (result[0], move)
        return (False,False)
    def copy(this):
        nodes = this.root.copy()
        result = Individual(nodes[-1], this.starting)
        return (result, nodes)
    def stats(this):
        states = dict(this.__dict__)
        try:
            states["winRatio"] = this.win/(this.win+this.loss)
            states["starting"] = this.starting
            states["age"] = this.win + this.loss
            del states["root"]
            del states["current"]
            states["sneakiness"] = this.sneakyWin/(this.win+this.loss) 
            states["sneakiness"] += this.capturedBad/(4*(this.capturedBad + this.capturedGood))
        except Exception as e:
            pass
        return states

class Node:
    def __init__(this, selector, cutoff, direction, moveDirection = None, passed = None, failed = None):
        this.selector = selector
        this.cutoff = cutoff
        this.direction = direction
        if moveDirection:
            this.moveDirection = moveDirection
        else:
            this.moveDirection = False
        if passed:
            this.passed = passed
        else:
            this.passed = False
        if failed:
            this.failed = failed
        else:
            this.failed = False
    def next(this, board, invert):
        result = selectors[(this.selector + 6) if invert else this.selector](board)
        if result == False:
            if this.failed:
                return((-10,-10), this.failed)
            else:
                return((-10,-10), False)
        if (result[1] < this.cutoff) == this.direction:
            if this.passed:
                return (result[0], this.passed)
            else:
                return (result[0], False)
        else:
            if this.failed:
                return(result[0], this.failed)
            else:
                return(result[0], False)
    def copy(this):
        result = Node.__new__(this.__class__)
        result.__dict__.update(this.__dict__)
        nodes = False
        if this.passed:
            nodes = this.passed.copy()
            result[x].passed = nodes[-1]
        if this.failed:
            faileds = this.failed.copy()
            if nodes:
                nodes.extend(faileds)
            else:
                nodes = faileds
            result[x].failed = nodes[-1]
        if nodes:
            nodes.append(result)
        else:
            nodes = [result]
        return nodes