import chess as ch

class Bot:

    def __init__(self, board, maxDepth, color):
        self.board=board
        self.maxDepth=maxDepth
        self.color=color

    def bot(self, candidate, depth):
        if(depth==self.maxDepth or self.board.legal_moves.count()==0):
            return self.evalFunction()
        
        else:
            moveList = list(self.board.legal_moves)

            newCandidate=None

            if(depth % 2 != 0):
                newCandidate=float("-inf")
            else:
                newCandidate=float("inf")

            for i in moveList:
                self.board.push()

                value = self.bot(newCandidate, depth+1)

                if(value>newCandidate and depth%2!=0):
                    newCandidate=value
                    if(depth==1):
                        move=i

                elif(value<newCandidate and depth%2==0):
                    newCandidate=value
