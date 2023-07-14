import asyncio
import json
import chess as ch
import random as rd
import discord
from discord import Intents, Client


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
        return compt

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
        return pieceValue

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


class Main:
    def __init__(self, board=ch.Board):
        self.board = board

    async def playHumanMove(self, message):
        try:
            await message.channel.send(
                "Legal moves: " + str(list(self.board.legal_moves))
            )
            await message.channel.send("To undo your last move, type 'undo'.")
            user_move = await message.channel.send("Make your move:")

            def check(m):
                return m.author == message.author and m.channel == message.channel

            response = await message.client.wait_for("message", check=check)
            move = response.content

            if move == "/help":
                await message.channel.send(
                    "Type in a legal move, for example: 'e4' or 'e5' or type 'undo'"
                )
            elif move == "undo":
                self.board.pop()
                self.board.pop()
                await self.playHumanMove(message)
                return
            else:
                self.board.push_san(move)

        except Exception as e:
            await message.channel.send("Invalid move. Please try again.")
            await self.playHumanMove(message)

    def playBotMove(self, maxDepth, color):
        bot = Bot(self.board, maxDepth, color)
        self.board.push(bot.bestMove())

    async def startGame(self, message):
        color = None
        while color != "b" and color != "w":
            await message.channel.send("To pick a color, type 'w' or 'b':")
            response = await message.client.wait_for(
                "message",
                check=lambda m: m.author == message.author
                and m.channel == message.channel,
            )
            color = response.content.lower()

        maxDepth = None
        while not isinstance(maxDepth, int):
            await message.channel.send("Choose depth:")
            response = await message.client.wait_for(
                "message",
                check=lambda m: m.author == message.author
                and m.channel == message.channel,
            )
            try:
                maxDepth = int(response.content)
            except ValueError:
                pass

        if color == "b":
            while not self.board.is_checkmate():
                await message.channel.send("Thinking...")
                self.playBotMove(maxDepth, ch.WHITE)
                await message.channel.send(str(self.board))
                await self.playHumanMove(message)
                await message.channel.send(str(self.board))

            await message.channel.send(str(self.board))
            await message.channel.send(str(self.board.outcome()))
        elif color == "w":
            while not self.board.is_checkmate():
                await message.channel.send(str(self.board))
                await self.playHumanMove(message)
                await message.channel.send(str(self.board))
                await message.channel.send("Thinking...")
                self.playBotMove(maxDepth, ch.BLACK)

            await message.channel.send(str(self.board))
            await message.channel.send(str(self.board.outcome()))

        self.board.reset()


intents = Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} is running!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print("Received message:", message.content)

    if message.content.lower().startswith("/startchess"):
        print("Start chess command received")

        newBoard = ch.Board()
        game = Main(newBoard)
        await game.startGame(message)


async def run_discord_bot():
    with open("config.json") as config_file:
        config = json.load(config_file)

    intents.typing = False
    intents.presences = False

    await client.login(config["token"])
    await client.start(config["token"])


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_discord_bot())
