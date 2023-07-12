import json
import chess as ch
import random as rd
import discord
from discord import Intents


def run_discord_bot():
    # Load configuration from config.json
    with open("config.json") as config_file:
        config = json.load(config_file)

    # create an instance of Intents
    intents = Intents.default()
    intents.typing = False
    intents.presences = False

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is running!")

    client.login(config["token"])


class Bot:
    # initialise class
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    # call bot() to find the best move starting with a depth of 1
    def bestMove(self):
        return self.bot(None, 1)

    # determines who is winning, white (+) or black (-)
    def evalFunction(self):
        compt = 0
        for i in range(64):
            compt += self.squareResPoints(ch.SQUARES[i])
        compt += self.mateOpportunity() + self.opening() + 0.001 * rd.random()
        return compt

    # is the game still in opening or not? encourages bot to develop pieces
    def opening(self):
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return 1 / 30 * self.board.legal_moves.count()
            else:
                return 1 / 30 * self.board.legal_moves.count()
        else:
            return 0

    # once there are no more legal moves it is either checkmate or stalemate
    def mateOpportunity(self):
        if self.board.legal_moves.count() == 0:
            if self.board.turn == self.color:
                return -999
            else:
                return 999
        else:
            return 0

    # assigns values to each piece
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
        return pieceValue

    # minimax algorithm and alpha-beta pruning
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

            bestMove = moveList[0] if moveList else None

            for move in moveList:
                self.board.push(move)

                value = self.bot(newCandidate, depth + 1)

                if value > newCandidate and depth % 2 != 0:
                    newCandidate = value
                    if depth == 1:
                        bestMove = move

                elif value < newCandidate and depth % 2 == 0:
                    newCandidate = value

                if candidate is not None and value < candidate and depth % 2 == 0:
                    self.board.pop()
                    break

                elif candidate is not None and value > candidate and depth % 2 != 0:
                    self.board.pop()
                    break

                self.board.pop()

        if depth > 1:
            return candidate
        else:
            return bestMove
