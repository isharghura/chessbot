# import chessBot as cb
# import chess as ch


# class Main:
#     def __init__(self, board=ch.Board()):
#         self.board = board

#     async def playHumanMove(self, message):
#         try:
#             await message.channel.send(
#                 "Legal moves: " + str(list(self.board.legal_moves))
#             )
#             await message.channel.send("To undo your last move, type 'undo'.")
#             user_move = await message.channel.send("Make your move:")

#             def check(m):
#                 return m.author == message.author and m.channel == message.channel

#             response = await message.client.wait_for("message", check=check)
#             move = response.content

#             if move == "!help":
#                 await message.channel.send(
#                     "Type in a legal move, for example: 'e4' or 'e5' or type 'undo'"
#                 )
#             elif move == "undo":
#                 self.board.pop()
#                 self.board.pop()
#                 await self.playHumanMove(message)
#                 return
#             else:
#                 self.board.push_san(move)

#         except Exception as e:
#             await message.channel.send("Invalid move. Please try again.")
#             await self.playHumanMove(message)

#     def playBotMove(self, maxDepth, color):
#         bot = cb.Bot(maxDepth, color)
#         self.board.push(bot.bestMove())

#     async def startGame(self, message):
#         color = None
#         while color != "b" and color != "w":
#             await message.channel.send("To pick a color, type 'w' or 'b':")
#             response = await message.client.wait_for(
#                 "message",
#                 check=lambda m: m.author == message.author
#                 and m.channel == message.channel,
#             )
#             color = response.content.lower()

#         maxDepth = None
#         while not isinstance(maxDepth, int):
#             await message.channel.send("Choose depth:")
#             response = await message.client.wait_for(
#                 "message",
#                 check=lambda m: m.author == message.author
#                 and m.channel == message.channel,
#             )
#             try:
#                 maxDepth = int(response.content)
#             except ValueError:
#                 pass

#         if color == "b":
#             while not self.board.is_checkmate():
#                 await message.channel.send("Thinking...")
#                 self.playBotMove(maxDepth, ch.WHITE)
#                 await message.channel.send(str(self.board))
#                 await self.playHumanMove(message)
#                 await message.channel.send(str(self.board))

#             await message.channel.send(str(self.board))
#             await message.channel.send(str(self.board.outcome()))
#         elif color == "w":
#             while not self.board.is_checkmate():
#                 await message.channel.send(str(self.board))
#                 await self.playHumanMove(message)
#                 await message.channel.send(str(self.board))
#                 await message.channel.send("Thinking...")
#                 self.playBotMove(maxDepth, ch.BLACK)

#             await message.channel.send(str(self.board))
#             await message.channel.send(str(self.board.outcome()))

#         self.board.reset()
