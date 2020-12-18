class Board(object):
    def __init__(self):
        self._board = ['-' for _ in range(9)]
        self._board = ['1','2','3','4','5','6','7','8','9']
        self._history = [] # borad history
        
    # move piece
    def _move(self, action, take):
        if self._board[action] == '-':
            self._board[action] = take
            
            self._history.append((action, take)) 
            
    # unmove piece
    def _unmove(self, action):
        self._board[action] = '-'
        
        self._history.pop()
            
        
    # Legal actions
    def get_legal_actions(self):
        actions = []
        for i in range(9):
            if self._board[i] == '-':
                actions.append(i)
        return actions
        
    # Detect action is legal or not
    def is_legal_action(self, action):
        return self._board[action] == '-'
        
    # Stop dectect
    def teminate(self):
        board = self._board
        lines = [board[0:3], board[3:6], board[6:9], board[0::3], board[1::3], board[2::3], board[0::4], board[2:7:2]]
        
        if ['X']*3 in lines or ['O']*3 in lines or '-' not in board:
            return True 
        else:
            return False
            
    # Check result
    def get_winner(self):
        board = self._board
        lines = [board[0:3], board[3:6], board[6:9], board[0::3], board[1::3], board[2::3], board[0::4], board[2:7:2]]
        
        if ['X']*3 in lines:
            return 0 
        elif ['O']*3 in lines:
            return 1 
        else:
            return 2
            
    # Print board
    def print_b(self):
        board = self._board
        for i in range(len(board)):
            print(board[i], end='')
            if (i+1)%3 == 0:
                print()
    
    # Print
    def print_history(self):
        print(self._history)


# Player
class Player(object):
   
    def __init__(self, take='X'): # default piece take = 'X'
        self.take=take
    
    def think(self, board):
        pass
        
    def move(self, board, action):
        board._move(action, self.take)


# Human player
class HumanPlayer(Player):
    def __init__(self, take):
        super().__init__(take)
    
    def think(self, board):
        while True:
            action = input('Please input a num in 0-8:')
            if len(action)==1 and action in '012345678' and board.is_legal_action(int(action)):
                return int(action)


# Game player
class AIPlayer(Player):
    def __init__(self, take):
        super().__init__(take)
    
    def think(self, board):
        print('AI is thinking ...')
        take = ['X','O'][self.take=='X']
        player = AIPlayer(take)    
        _, action = self.minimax(board, player)
        #print('OK')
        return action
        
    # minimax search
    def minimax(self, board, player, depth=0) :
        if self.take == "O": 
            bestVal = -10
        else:
            bestVal = 10
            
        if board.teminate() :
            if board.get_winner() == 0 :
                return -10 + depth, None
            elif board.get_winner() == 1 :
                return 10 - depth, None
            elif board.get_winner() == 2 :
                return 0, None

        for action in board.get_legal_actions() :
            board._move(action, self.take)
            val, _ = player.minimax(board, self, depth+1) 
            board._unmove(action) 
            
            if self.take == "O" :
                if val > bestVal:
                    bestVal, bestAction = val, action
            else :
                if val < bestVal:
                    bestVal, bestAction = val, action
        
        return bestVal, bestAction



# Game
class Game(object):
    def __init__(self):
        self.board = Board()
        self.current_player = None
        
    # make player
    def mk_player(self, p, take='X'): # p in [0,1]
        if p==0:
            return HumanPlayer(take)
        else:
            return AIPlayer(take)
            
    # switch player
    def switch_player(self, player1, player2):
        if self.current_player is None:
            return player1
        else:
            return [player1, player2][self.current_player == player1]
            
    # print winner
    def print_winner(self, winner): # winner in [0,1,2]
        print(['Winner is player1','Winner is player2','Draw'][winner])

    # run game
    def run(self):
        ps = input("Please select two player's type:\n\t0.Human\n\t1.AI\nSuch as:0 0\n")
        p1, p2 = [int(p) for p in ps.split(' ')]
        player1, player2 = self.mk_player(p1, 'X'), self.mk_player(p2, 'O') # first player X，second O
        
        print('\nGame start!\n')
        self.board.print_b() # print board
        while True:
            self.current_player = self.switch_player(player1, player2) 
            
            action = self.current_player.think(self.board) 
            
            self.current_player.move(self.board, action)   
            
            self.board.print_b() 
            
            if self.board.teminate(): 
                winner = self.board.get_winner() 
                break
        
        self.print_winner(winner)
        print('Game over!')
        
        self.board.print_history()
    
    
if __name__ == '__main__':
    Game().run()