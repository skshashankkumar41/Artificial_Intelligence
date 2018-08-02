import itertools
import random

def new_board():
    return ((0,0,0),(0,0,0),(0,0,0))

def apply_move(board_state,move,side):
    move_x,move_y=move
    state_list=list(list(s) for s in board_state)
    state_list[move_x][move_y]=side
    return tuple(tuple(s) for s in state_list)

def available_moves(board_state):
    for x,y in itertools.product(range(3),range(3)):
        if board_state[x][y]==0:
            yield(x,y)

def has_3_in_a_line(line):
    return all(x==-1 for x in line)| all(x==1 for x in line)

def has_winner(board_state):
    for x in range(3):
        if has_3_in_a_line(board_state[x]):
            return board_state[x][0]

    for y in range(3):
        if has_3_in_a_line([i[y] for i in board_state]):
            return board_state[0][y]

    if has_3_in_a_line([board_state[i][i] for i in range(3)]):
        return board_state[0][0]

    if has_3_in_a_line([board_state[2-i][i] for i in range(3)]):
        return board_state[0][2]

    return 0

def play_game(first_player_func,seconde_player_func):
    board_state=new_board()
    player_turn=1

    while True:
        _available_moves=list(available_moves(board_state))
        if len(_available_moves)==0:
            print("No Moves Left, Match is Draw...")
            return 0

        if player_turn>0:
            move=first_player_func(board_state,1)
        else:
            move=seconde_player_func(board_state,-1)

        if move not in _available_moves:
            print('illegal Move...')
            return -player_turn

        board_state=apply_move(board_state,move,player_turn)
        print(board_state)

        winner=has_winner(board_state)

        if winner!=0:
            print("We have a winner, size: %s "%player_turn)
            return winner
        player_turn=-player_turn


def score_line(line):
    plus_count=line.count(1)
    minus_count=line.count(-1)
    if plus_count==2 and minus_count==0:
        return 1
    elif minus_count==2 and plus_count==0:
        return -1
    return 0

def evaluate(board_state):
    score=0
    for x in range(3):
        score=score+score_line(board_state[x])
    for y in range(3):
        score=score+score_line([i[y] for i in board_state])
    score=score+score_line([board_state[i][i] for i in range(3)])
    score=score+score_line([board_state[2-i][i] for i in range(3)])

    return score

def min_max(board_state,side,max_depth):
    best_score=None
    best_score_move=None

    moves=list(available_moves(board_state))
    if not moves:
        return 0,None

    for move in moves:
        new_board_state=apply_move(board_state,move,side)
        winner=has_winner(new_board_state)
        if winner!=0:
            return winner*10000,move
        else:
            if max_depth<=1:
                score=evaluate(new_board_state)
            else:
                score,_=min_max(new_board_state,-side,max_depth-1)

        if side>0:
                if best_score is None or score>best_score:
                    best_score=score
                    best_score_move=move
        else:
                if best_score is None or score<best_score:
                    best_score=score
                    best_score_move=move
    return best_score,best_score_move

def random_player(board_state,side):
    moves=list(available_moves(board_state))
    return random.choice(moves)

def AI_player(board_state,side):
    return min_max(board_state,side,5)[1]


play_game(random_player,AI_player)
