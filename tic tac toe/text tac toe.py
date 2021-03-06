import random

# text based implementation
# not used by other files

board = ["X", ".", "2",
         "O", "O", "5",
         "/", "/", "X"]


# player will maximise,
# ai will minimise
player, ai = "O", "X"

def print_board(board):
    print("   |   |   ")
    print(" " + board[0] + " | " + board[1] + " | " + board[2] + "  ")
    print("   |   |   ")
    print("---|---|---")
    print("   |   |   ")
    print(" " + board[3] + " | " + board[4] + " | " + board[5] + "  ")
    print("   |   |   ")
    print("---|---|---")
    print("   |   |   ")
    print(" " + board[6] + " | " + board[7] + " | " + board[8] + "  ")
    print("   |   |   ")
 



def static_evaluation(board, depth, boards_considered, list_of_boards_considered, alpha, beta):
    o_won, x_won, draw = check_if_won(board)
    if draw:
        return 0, boards_considered, list_of_boards_considered, alpha, beta
    if o_won:
        return (20 - depth), boards_considered, list_of_boards_considered, alpha, beta
    if x_won:
        return (-20 + depth), boards_considered, list_of_boards_considered, alpha, beta
    else:
        return None


def minimax(board, depth, isMax, max_id, min_id, boards_considered, list_of_boards_considered, alpha, beta):
    if static_evaluation(board, depth, boards_considered, list_of_boards_considered, alpha, beta) != None:
        return static_evaluation(board, depth, boards_considered, list_of_boards_considered, alpha, beta)

    if isMax:
        # set a worst case
        currentMaxEval = -9999
        for i in range(len(board)):
            if not(board[i] == "X" or board[i] == "O"):
                analysis_board = board.copy()
                analysis_board[i] = max_id
                boards_considered += 1
                list_of_boards_considered.append(analysis_board)
                
                evaluation, boards_considered, list_of_boards_considered, alpha, beta = minimax(analysis_board, depth+1, False, max_id, min_id, boards_considered, list_of_boards_considered, alpha, beta)
                
                if evaluation > currentMaxEval:
                    currentMaxEval = evaluation
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
                
        return currentMaxEval, boards_considered, list_of_boards_considered, alpha, beta

    if not isMax:
        # set a worst case
        currentMinEval = 9999
        for i in range(len(board)):
            if not(board[i] == "X" or board[i] == "O"):
                analysis_board = board.copy()
                analysis_board[i] = min_id
                boards_considered += 1
                list_of_boards_considered.append(analysis_board)
                
                evaluation, boards_considered, list_of_boards_considered, alpha, beta = minimax(analysis_board, depth+1, True, max_id, min_id, boards_considered, list_of_boards_considered, alpha, beta)

                if evaluation < currentMinEval:
                    currentMinEval = evaluation
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break

        return currentMinEval, boards_considered, list_of_boards_considered, alpha, beta


def find_computer_move(board, ai, player, boards_considered, list_of_boards_considered, alpha, beta):
    currentEval = 9999

    for i in range(len(board)):
        if not(board[i] == "X" or board[i] == "O"):
            
            # make a test move
            analysis_board = board.copy()
            analysis_board[i] = ai
            boards_considered +=1
            list_of_boards_considered.append(analysis_board)
            # see if its good
            evaluation, boards_considered, list_of_boards_considered, alpha, beta = minimax(analysis_board, 0, False, player, ai, boards_considered, list_of_boards_considered, alpha, beta)

            if evaluation < currentEval:
                bestMove = i
                currentEval = evaluation
                # print(bestMove)
    return bestMove, boards_considered, list_of_boards_considered

def check_if_won(board):
    winning = [[0, 3, 6],
               [1, 4, 7],
               [2, 5, 8],
               [0, 4, 8],
               [2, 4, 6],
               [0, 1, 2],
               [3, 4, 5],
               [6, 7, 8]]

    o_won = False
    x_won = False

    for line in winning:
        if board[line[0]] == board[line[1]] and \
           board[line[1]] == board[line[2]] and \
           board[line[2]] == "O":
            o_won = True

        if board[line[0]] == board[line[1]] and \
           board[line[1]] == board[line[2]] and \
           board[line[2]] == "X":
            x_won = True

    # if there is no winnner
    if not(o_won or x_won):
        draw = True
        for tile in board:
            if not(tile == "X" or tile == "O"):
                draw = False
    else:
        draw = False

    return o_won, x_won, draw

pause_to_display_analysis = False

def game():
    done = False
    while not done:
        if not pause_to_display_analysis:
            # player moves
            player_move = input("Enter move: ")
            if player_move == "pass":
                pass
            else:
                board[int(player_move)] = player
            print_board(board)

            # check if done
            player_won, ai_won, draw = check_if_won(board)

            if player_won:
                print("Player won!!")
                break
            if ai_won:
                print("ai won!!")
                break
            if draw:
                print("Draw!!")
                break

            print("----------")

        # computer moves
        boards_considered = 0
        
        # find how many board
        list_of_boards_considered = []
        computer_move, boards_considered, list_of_boards_considered = find_computer_move(board, ai, player, boards_considered, list_of_boards_considered, -99999, 99999)
        print(boards_considered, list_of_boards_considered)
        
        board[computer_move] = ai
        
        print_board(board)


game()