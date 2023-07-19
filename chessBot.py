import asyncio
import json
import chess as ch
import random as rd
import discord
from discord.ext import commands
import logging
import tracemalloc

tracemalloc.start()


class ChessGame:
    def __init__(self, bot, channel_id, board=ch.Board()):
        self.bot = bot
        self.channel_id = channel_id
        self.board = board

    async def play_human_move(self, message, max_depth):
        if not self.running:
            return

        try:
            legal_moves = [move.uci() for move in self.board.legal_moves]
            await message.channel.send("Make your move:")

            def check(m):
                return m.author == message.author and m.channel == message.channel

            response = await self.bot.wait_for("message", check=check)
            move = response.content.lower()

            if move == "/help":
                await message.channel.send(
                    "Type in a legal move, for example: 'e4' or 'e5'."
                )
                await self.play_human_move(message, max_depth)
            elif move == "/exit":
                await message.channel.send("Game has been exited.")
                self.running = False
                return
            else:
                try:
                    move = self.board.parse_san(move)

                    if move in self.board.legal_moves:
                        self.board.push(move)
                    else:
                        raise ValueError("Invalid move. Please try again.")
                except ValueError as e:
                    await message.channel.send(str(e))
                    await self.play_human_move(message, max_depth)
                except ch.MoveError as e:
                    await message.channel.send("Invalid move format. Please try again.")
                    await self.play_human_move(message, max_depth)

            if self.running:  # Only play bot move if the game is still running
                await self.play_bot_move(max_depth)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            await message.channel.send("An error occurred. Please try again.")
            await self.play_human_move(message, max_depth)

    def format_board(self):
        lines = []
        for row in range(8):
            line = ""
            for col in range(8):
                square = ch.square(col, 7 - row)
                piece = self.board.piece_at(square)
                if piece:
                    symbol = ""
                    if piece.color == ch.WHITE:
                        if piece.piece_type == ch.PAWN:
                            symbol = "♟︎"
                        elif piece.piece_type == ch.KNIGHT:
                            symbol = "♞"
                        elif piece.piece_type == ch.BISHOP:
                            symbol = "♝"
                        elif piece.piece_type == ch.ROOK:
                            symbol = "♜"
                        elif piece.piece_type == ch.QUEEN:
                            symbol = "♛"
                        elif piece.piece_type == ch.KING:
                            symbol = "♚"
                    else:
                        if piece.piece_type == ch.PAWN:
                            symbol = "♙"
                        elif piece.piece_type == ch.KNIGHT:
                            symbol = "♘"
                        elif piece.piece_type == ch.BISHOP:
                            symbol = "♗"
                        elif piece.piece_type == ch.ROOK:
                            symbol = "♖"
                        elif piece.piece_type == ch.QUEEN:
                            symbol = "♕"
                        elif piece.piece_type == ch.KING:
                            symbol = "♔"
                    line += symbol + " "
                else:
                    line += ".    "
            lines.append(line)
        return "\n".join(lines)

    async def play_bot_move(self, max_depth):
        if not self.running:
            return

        await asyncio.sleep(1)  # Add a delay before the bot makes its move (optional)

        bot_color = self.board.turn  # Get the color of the bot
        bot = Bot(self.board, max_depth, bot_color)
        move = bot.best_move()
        self.board.push(move)

        channel = self.bot.get_channel(self.channel_id)

        if self.board.is_checkmate() or self.board.is_stalemate():
            await channel.send(self.format_board())
        else:
            await channel.send(f"The bot played {move.uci()}")  # Send the bot's move
            await channel.send(self.format_board())

        if not self.running:
            return  # Exit early if the game has been exited

        return move

    async def start_game(self, ctx):
        self.running = True
        color = "w"
        # while color != "b" and color != "w":
        #     await ctx.send("To pick a color, type 'w' or 'b':")
        #     response = await self.bot.wait_for(
        #         "message",
        #         check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
        #     )
        # color = response.content.lower()

        max_depth = None
        while not isinstance(max_depth, int):
            await ctx.send("Choose depth:")
            response = await self.bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
            )
            try:
                max_depth = int(response.content)
            except ValueError:
                pass

        if color == "w":
            await ctx.send(self.format_board())
            while (
                self.running
                and not self.board.is_checkmate()
                and not self.board.is_stalemate()
            ):
                if self.board.turn == ch.WHITE:
                    await self.play_human_move(ctx, max_depth)
                    if self.board.is_checkmate() or self.board.is_stalemate():
                        break
                else:
                    await self.play_bot_move(max_depth)

        elif color == "b":
            self.board.turn = ch.WHITE
            while (
                self.running
                and not self.board.is_checkmate()
                and not self.board.is_stalemate()
            ):
                if self.board.turn == ch.WHITE:
                    await self.play_bot_move(max_depth)
                    await ctx.send(self.format_board())
                    if self.board.is_checkmate() or self.board.is_stalemate():
                        break
                else:
                    await self.play_human_move(ctx, max_depth)

        if (
            self.running
        ):  # Only print the final board and outcome if the game is still running
            await ctx.send(self.format_board())
            await ctx.send(self.format_board().outcome())

        self.board.reset()


class Bot:
    def __init__(self, board, max_depth, color):
        self.board = board
        self.max_depth = max_depth
        self.color = color

    def best_move(self):
        return self.bot(None, 1)

    def eval_function(self):
        compt = 0
        for i in range(64):
            compt += self.square_res_points(ch.SQUARES[i])
        compt += self.mate_opportunity() + self.opening() + 0.001 * rd.random()
        return compt

    def opening(self):
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return 1 / 30 * self.board.legal_moves.count()
            else:
                return 1 / 30 * self.board.legal_moves.count()
        else:
            return 0

    def mate_opportunity(self):
        if self.board.legal_moves.count() == 0:
            if self.board.turn == self.color:
                return -999
            else:
                return 999
        else:
            return 0

    def square_res_points(self, square):
        piece_value = 0
        if self.board.piece_type_at(square) == ch.PAWN:
            piece_value = 1
        if self.board.piece_type_at(square) == ch.KNIGHT:
            piece_value = 3.2
        if self.board.piece_type_at(square) == ch.BISHOP:
            piece_value = 3.33
        if self.board.piece_type_at(square) == ch.ROOK:
            piece_value = 5.1
        if self.board.piece_type_at(square) == ch.QUEEN:
            piece_value = 8.8
        return piece_value

    def bot(self, candidate, depth):
        if depth == self.max_depth or self.board.legal_moves.count() == 0:
            return self.eval_function()
        else:
            move_list = list(self.board.legal_moves)
            new_candidate = None

            if depth % 2 != 0:
                new_candidate = float("-inf")
            else:
                new_candidate = float("inf")

            best_move = move_list[0] if move_list else None

            for move in move_list:
                self.board.push(move)

                value = self.bot(new_candidate, depth + 1)

                if value > new_candidate and depth % 2 != 0:
                    new_candidate = value
                    if depth == 1:
                        best_move = move

                elif value < new_candidate and depth % 2 == 0:
                    new_candidate = value

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
            return best_move


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    if not bot.ready:
        bot.ready = True
        print(f"{bot.user} is running!")


@bot.command(name="startgame")
async def start_game(ctx):
    print("Start game command received")

    new_board = ch.Board()
    game = ChessGame(bot, ctx.channel.id, new_board)
    await game.start_game(ctx)


async def run_discord_bot():
    with open("config.json") as config_file:
        config = json.load(config_file)

    try:
        await bot.start(config["token"])
    finally:
        await bot.close()


if __name__ == "__main__":
    bot.ready = False
    asyncio.run(run_discord_bot())
