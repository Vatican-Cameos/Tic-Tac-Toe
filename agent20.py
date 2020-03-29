# Tic Tac Toe with alpha beta pruning
#board = [[. . .][. . .][. . .]]
import random

MIN,MAX = float("-inf"),float("inf")
global player, opponent
name = "Player"
def generate_all_moves(board):
    # Generates all possible moves for a given board
    # Author : Pavan
    result = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == ".":
                result.append((row, col))

    return result


def min_max(board, depth, ismaxplayer, isX, alpha, beta):
    # Run the recursvie algorithm with alpha beta pruning to generate best possible move
    res = generate_all_moves(board)
    if depth == 0:
      return None, evaluate_board(board, isX)
    best_max_move = None;
    best_min_move = None;
    if ismaxplayer:
        bestscore = MIN
        for each_move in res:
            #score = evaluate_board(board)
            row = each_move[0]
            col = each_move[1]

            board[row][col] = player

            _, score = min_max(board, depth - 1, False, isX, alpha, beta)
            if(score > bestscore):
              best_max_move = each_move
            
            bestscore = max(bestscore,score)
            alpha = max(alpha, bestscore)


            board[row][col] = "."
            if beta <= alpha:
              break

        return best_max_move, bestscore
    else:
        bestscore = MAX
        for each_move in res:
            #score = evaluate_board(board)
            row = each_move[0]
            col = each_move[1]
            board[row][col] = opponent
            _, score = min_max(board, depth - 1, True, isX, alpha, beta)
            if(score < bestscore):
              best_min_move = each_move
            
            bestscore = min(bestscore, score)
            beta = min(beta, bestscore)
            board[row][col] = "."
            if beta <= alpha:
              break
        return best_min_move, bestscore

# sym = X
def calculate_points(s, sym):
    value = 0
    if s == sym + sym + sym:
        value += 3 * 100
    elif s == sym + sym + "." or s == sym + "." + sym or s == "." + sym + sym:
        value += 2 * 10
        # X..
    elif s == sym + ".." or s == ".." + sym or s == "." + sym + ".":
        value += 1
    return value


def evaluate_for_symbol(symbol, board):
    value = 0
    for row in range(len(board)):
        s = ""
        for col in range(len(board[0])):
            s += board[row][col]
        value += calculate_points(s, symbol)

    # columns
    for col in range(len(board[0])):
        s = ""
        for row in range(len(board)):
            s += board[row][col]
        value += calculate_points(s,symbol)

    # left to bottom right
    s = board[0][0] + board[1][1] + board[2][2]
    value += calculate_points(s,symbol)

    # right to bottom left diagonal
    s = board[0][2] + board[1][1] + board[2][0]
    value += calculate_points(s,symbol)
    return value


# X X . | O O . | X . .
# . O X | X . . | . . .
# X X X | X . X | . . .
#
def evaluate_board(board, isX):
    # Evaluate the quality of the board
    # Author : Pavan
    # rows
    value = 0
    if isX:
      value += evaluate_for_symbol("X", board)
      value -= evaluate_for_symbol("O", board)
    else:
      value -= evaluate_for_symbol("X", board)
      value += evaluate_for_symbol("O", board)
    
    #beatify_board(board)
    #print(isX)
    #print(value)
    return value


def test_generate():
    print(
        generate_all_moves([[".", ".", "."], [".", ".", "."], [".", ".",
                                                               "."]]))
    print(
        generate_all_moves([["X", "O", "."], [".", "O", "."], ["O", "O",
                                                               "."]]))
    print(
        generate_all_moves([["X", "X", "X"], ["X", "X", "X"], ["X", "X",
                                                               "X"]]))


def test_board_evaluation():
    beatify_board([[".", ".", "X"], [".", ".", "X"], [".", ".", "X"]])
    print(evaluate_board([[".", ".", "X"], [".", ".", "X"], [".", ".", "X"]], True))
    beatify_board([[".", ".", "X"], [".", "X", "."], [".", ".", "X"]])
    print(evaluate_board([[".", ".", "X"], [".", "X", "."], [".", ".", "X"]], True))
    #print(evaluate_board([["O", "O", "."], ["X", ".", "."], ["X", ".", "X"]]))
    #print(evaluate_board([["X", ".", "."], [".", ".", "."], [".", ".", "."]]))
    #print(evaluate_board([["O", "O", "O"], ["X", ".", "."], ["X", ".", "X"]]))
    #print(evaluate_board([[".", ".", "."], [".", ".", "."], [".", ".", "."]]))

def beatify_board(board):
  for row in range(len(board)):
    print(board[row])

def check_winner_condition(s):
  if s == "XXX":
    print(name, " won")
    return True
  elif s == "OOO":
    print(name, "got rekt")
    return True

def is_winning(board):
  for row in range(len(board)):
      s = ""
      for col in range(len(board[0])):
        s += board[row][col]
      if(check_winner_condition(s)):
        return True

  # columns
  for col in range(len(board[0])):
    s = ""
    for row in range(len(board)):
      s += board[row][col]
    if(check_winner_condition(s)):
        return True

  # left to bottom right
  s = board[0][0] + board[1][1] + board[2][2]
  if(check_winner_condition(s)):
        return True

  # right to bottom left diagonal
  s = board[0][2] + board[1][1] + board[2][0]
  if(check_winner_condition(s)):
        return True
  count = 0
  for row in range(len(board)):
    for col in range(len(board[row])):
      if board[row][col] != ".":
        count += 1
  if count == 9:
    print("Nice battle,", name, ". It is a Draw!")
    return True
  return False

def play_game(board, p, is_player_start):
  is_player_x = False
  global player, opponent
  if p == "X":
    player = "X"
    opponent = "O"
    is_player_x = True
  else:
    player = "O"
    opponent = "X"
    is_player_x = False
  
  while(not is_winning(board)):
    if is_player_start:
      move,_ = min_max(board, 2, True, is_player_x, float("-inf"), float("inf"))
      board[move[0]][move[1]] = player
      print("Player made move :")
      beatify_board(board)
      is_player_start = False
    else:
      move,_ = min_max(board, 2, True, is_player_x, float("-inf"), float("inf"))
      board[move[0]][move[1]] = opponent
      print("Opponent made move :")
      beatify_board(board)
      is_player_start = True

def play_game_player_computer(board, p = "X", is_player_start = True):
  is_player_x = False
  global player, opponent
  if p == "X":
    player = "X"
    opponent = "O"
    is_player_x = True
  else:
    player = "O"
    opponent = "X"
    is_player_x = False
  beatify_board(board)
  while(not is_winning(board)):
    if is_player_start:
      print("Make a move", name)
      move = [100,100]
      while(0 > move[0] or move[0] > 2 or 0 > move[1] or move[1] > 2):
        print("Enter valid input sperated by comma. Eg : 1,1")
        move = input()
        move = move.split(",")
        move[0] = int(move[0].strip())
        move[1] = int(move[1].strip())

      
      board[move[0]][move[1]] = player
      print("Player made move :")
      beatify_board(board)
      is_player_start = False
    else:
      move,_ = min_max(board, 2, True, is_player_x, float("-inf"), float("inf"))
      board[move[0]][move[1]] = opponent
      print("Opponent made move :")
      beatify_board(board)
      is_player_start = True

def main():
    #test_generate()
    #test_board_evaluation()
    global player, opponent
    player = "O"
    opponent = "X"
    print("Starting game -----------------")
    board_1 = [["X", "X", "."], [".", "O", "X"], ["X", "X", "."]]
    board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    beatify_board(board)
    print("-------------------------------------------")
    move,_ = min_max(board, 3, True, False, float("-inf"), float("inf"))
    print("Score", _)
    board[move[0]][move[1]] = player
    print("move made")
    beatify_board(board)

#test_board_evaluation()
#main()
print("Please enter your name")
name = input()
board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
#random.randint(0,2)
play_game_player_computer(board, is_player_start=random.randint(0,1))
#play_game_player_computer(board)

