import chess as ch
import random as rd


class Bot:
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def bestMove(self):
        return self.bot(None, 1)

    def evalFunction(self):
        compt = 0
        for i in range(64):
            compt += self.squareResPoints(ch.SQUARES[i])
        compt += self.mateOpportunity() + self.opening() + 0.001 * rd.random()

    def opening(self):
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return 1 / 30 * self.board.legal_moves.count()
            else:
                return 1 / 30 * self.board.legal_moves.count()
        else:
            return 0

    def mateOpportunity(self):
        if self.board.legal_moves.count() == 0:
            if self.board.turn == self.color:
                return -999
            else:
                return 999
        else:
            return 0

    def squareResPoints(self, square):
        pieceValue = 0
        if self.board.piece_type_at(square) == ch.PAWN:
            pieceValue = 1
        if self.board.piece_type_at(square) == ch.KNIGHT:
            pieceValue = 3.2
        if self.board.piece_type_at(square) == ch.BISHOP:
            pieceValue = 3.33
        if self.board.piece_type_at(square) == ch.ROOK:
            pieceValue = 5.1
        if self.board.piece_type_at(square) == ch.QUEEN:
            pieceValue = 8.8

    def bot(self, candidate, depth):
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            return self.evalFunction()

        else:
            moveList = list(self.board.legal_moves)

            newCandidate = None

            if depth % 2 != 0:
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")

            for i in moveList:
                self.board.push()

                value = self.bot(newCandidate, depth + 1)

                if value > newCandidate and depth % 2 != 0:
                    newCandidate = value
                    if depth == 1:
                        move = i

                elif value < newCandidate and depth % 2 == 0:
                    newCandidate = value

                if candidate != None and value < candidate and depth % 2 == 0:
                    self.board.pop()
                    break

                elif candidate != None and value > candidate and depth % 2 != 0:
                    self.board.pop()
                    break

                self.board.pop()

        if depth > 1:
            return candidate
        else:
            return move
