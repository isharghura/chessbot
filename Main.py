import chessBot as cb
import chess as ch


class Main:
    def __init__(self, board=ch.board):
        self.board = board

    def playHumanMove(self):
        try:
            print(self.board.legal_moves)
            print("To undo your last move, type 'undo'.")
            play = input("Your move: ")
            if play == "undo":
                self.board.pop()
                self.board.pop()
                self.playHumanMove()
                return
            self.board.push_san(play)
        except:
            self.playHumanMove()

    def playBotMove(self, maxDepth, color):
        bot = cb.Bot(self, maxDepth, color)
        self.board.push(bot.getBestMove())

    def startGame(self):
        color = None
        while color != "b" and color != "w":
            color = input("To pick a colour, type 'w' or 'b': ")
        maxDepth = None
        while isinstance(maxDepth, int) == False:
            maxDepth = int(input("Choose depth: "))
        if color == "b":
            while self.board.is_checkmate() == False:
                print("Thinking...")
                self.playBotMove(maxDepth, ch.WHITE)
                print(self.board)
                self.playHumanMove()
                print(self.board)
            print(self.board)
            print(self.board.outcome())
        elif color == "w":
            while self.board.is_checkmate() == False:
                print(self.board)
                self.playHumanMove()
                print(self.board)
                print("Thinking...")
                self.playBotMove(maxDepth, ch.BLACK)
            print(self.board)
            print(self.board.outcome())
        self.board.reset
        self.startGame()


newBoard = ch.Board()
game = Main(newBoard)
game.startGame()
