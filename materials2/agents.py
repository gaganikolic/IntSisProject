import math
import random
import time

import config
from state import State


class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_column(self, state, max_depth):
        pass

class Human(Agent):
    pass

class ExampleAgent(Agent):
    def get_chosen_column(self, state, max_depth):
        time.sleep(random.random())
        columns = state.get_possible_columns()
        return columns[random.randint(0, len(columns) - 1)]


def custom_sort(item):
    niz = [3, 2, 4, 1, 5, 0, 6]
    x = 7 - niz.index(item[1])
    #return (item[0], -abs(item[1] - config.N//2))
    return (item[0], x)

def evaluation(state, caller):
    red_wins = 0
    yellow_wins = 0

    wins = State.win_masks
    for win in wins:
        if not (win & state.checkers_yellow):
            red_wins += 1
        if not (win & state.checkers_red):
            yellow_wins += 1

    if (caller == 1):
        return red_wins - yellow_wins
    else:
        return yellow_wins - red_wins

def sort_columns(state, columns):
    sorted_columns = []
    for column in columns:
        new_state = state.generate_successor_state(column)
        eval = evaluation(new_state, new_state.next_on_move)
        sorted_columns.append((eval, column))
    sorted_data = sorted(sorted_columns, key=custom_sort, reverse=True)
    col = []
    for item in sorted_data:
        col.append(item[1])
    return col


class MinimaxAgent(Agent):
    def minimax(self, state, depth, alpha, beta, MAXPlayer, caller):
        if depth == 0 or state.get_state_status() is not None:
            if state.get_state_status() is not None:
                if (caller == state.get_state_status()):
                    num_of_coins_bin = bin(state.get_checkers(caller))
                    num_of_coins = num_of_coins_bin.count('1')
                    k = 1.0 / (num_of_coins)
                    return None, 1000 * k
                elif (state.get_state_status() != State.DRAW):
                    num_of_coins_bin = bin(state.get_checkers(1 - caller))
                    num_of_coins = num_of_coins_bin.count('1')
                    k = -1.0 / (num_of_coins)
                    return None, 1000 * k
                else:
                    return None, 0
            else:
                return None, evaluation(state, state.next_on_move)

        possible_columns = state.get_possible_columns()
        sorted_columns = sort_columns(state, possible_columns)

        if MAXPlayer:
            value = -math.inf
            # column = sorted_columns[0]
            for col in sorted_columns:
                new_state = state.generate_successor_state(col)
                new_score = self.minimax(new_state, depth - 1, alpha, beta, False, caller)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else:
            value = math.inf
            # column = sorted_columns[0]
            for col in sorted_columns:
                new_state = state.generate_successor_state(col)
                new_score = self.minimax(new_state, depth - 1, alpha, beta, True, caller)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_chosen_column(self, state, max_depth):
        if max_depth == 0:
            max_depth = math.inf
        column, x = self.minimax(state, max_depth, -math.inf, math.inf, True, state.next_on_move)
        return column


class NegascoutAgent(Agent):
    def negascout(self, state, MINPlayer, alpha, beta, depth, caller):
        if depth == 0 or state.get_state_status() is not None:
            if state.get_state_status() is not None:
                if (caller == state.get_state_status()):
                    # caller win
                    num_of_coins_bin = bin(state.get_checkers(caller))
                    num_of_coins = num_of_coins_bin.count('1')
                    k = 1.0 / (num_of_coins)
                    return None, 1000 * k * (-1 if MINPlayer else 1)
                elif (state.get_state_status() != State.DRAW):
                    # caller lose
                    num_of_coins_bin = bin(state.get_checkers(1 - caller))
                    num_of_coins = num_of_coins_bin.count('1')
                    k = -1.0 / (num_of_coins)
                    return None, 1000 * k * (-1 if MINPlayer else 1)
                else:
                    return None, 0
            else:
                return None, evaluation(state, state.next_on_move) * (-1 if MINPlayer else 1)

        possible_columns = state.get_possible_columns()
        sorted_columns = sort_columns(state, possible_columns)

        score = -math.inf
        col = sorted_columns[0]
        for column in sorted_columns:
            new_state = state.generate_successor_state(column)
            if column == sorted_columns[0]:
                val = -self.negascout(new_state, not MINPlayer, -beta, -alpha, depth - 1, caller)[1]
            else:
                val = -self.negascout(new_state, not MINPlayer, -alpha - 1, -alpha, depth - 1, caller)[1]
                if alpha < val < beta:
                    val = -self.negascout(new_state, not MINPlayer, -beta, -alpha, depth - 1, caller)[1]
            if (val > score):
                score = val
                col = column
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return col, score

    def get_chosen_column(self, state, max_depth):
        if max_depth == 0:
            max_depth = math.inf
        column, x = self.negascout(state, False, -math.inf, math.inf, max_depth, state.next_on_move)
        return column


'''
def negamax(node, player):
    if is_terminal_node(node):
        return node_evaluation(node) * (-1 if player == Player.MIN else 1)
    score = -math.inf
    for succ in node.successors():
        score = max(score, -negamax(succ, switch(player)))
    return score

def negamax_alpha_beta(node, player, alpha, beta):
    if is_terminal_node(node):
        return node_evaluation(node) * (-1 if player == Player.MIN else 1)
    score = -math.inf
    for succ in node.successors():
        val = -negamax_alpha_beta(succ, switch(player), -beta, -alpha)
        score = max(score, val)
        alpha = max(alpha, score)
        if alpha >= beta : break
    return score
'''