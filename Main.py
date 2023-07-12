import chessBot as cb
import chess as ch

if __name__ == "__main__":
    cb.run_discord_bot()

# class Main:
#     #initialise
#     def __init__(self, board=ch.Board):
#         self.board = board

#     #ask for a move
#     def playHumanMove(self):
#         try:
#             print(self.board.legal_moves)
#             print("To undo your last move, type 'undo'.")
#             move = input("Make a move: ")
#             if move== "hello":
#                 return "Hello there!"
#             if move =="!help":
#                 return "'This is a help message that you can modify.'"
#             if move == "undo":
#                 self.board.pop()
#                 self.board.pop()
#                 self.playHumanMove()
#                 return
#             self.board.push_san(move)
#         except:
#             self.playHumanMove()

#     # bot move
#     def playBotMove(self, maxDepth, color):
#         bot = cb.Bot(self.board, maxDepth, color)
#         self.board.push(bot.bestMove())

#     # color, depth, begin
#     def startGame(self):
#         color = None
#         while color != "b" and color != "w":
#             color = input("To pick a colour, type 'w' or 'b': ")
#         maxDepth = None
#         while isinstance(maxDepth, int) == False:
#             maxDepth = int(input("Choose depth: "))
#         if color == "b":
#             while self.board.is_checkmate() == False:
#                 print("Thinking...")
#                 self.playBotMove(maxDepth, ch.WHITE)
#                 print(self.board)
#                 self.playHumanMove()
#                 print(self.board)
#             print(self.board)
#             print(self.board.outcome())
#         elif color == "w":
#             while self.board.is_checkmate() == False:
#                 print(self.board)
#                 self.playHumanMove()
#                 print(self.board)
#                 print("Thinking...")
#                 self.playBotMove(maxDepth, ch.BLACK)
#             print(self.board)
#             print(self.board.outcome())
#         self.board.reset
#         self.startGame()

# # create a new board and start
# newBoard = ch.Board()
# game = Main(newBoard)
# game.startGame()
