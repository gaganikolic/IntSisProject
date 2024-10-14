import random
import time

import config


class Algorithm:
    def __init__(self, heuristic=None):
        self.heuristic = heuristic
        self.nodes_evaluated = 0
        self.nodes_generated = 0

    def get_legal_actions(self, state):
        self.nodes_evaluated += 1
        max_index = len(state)
        zero_tile_ind = state.index(0)
        legal_actions = []
        if 0 <= (up_ind := (zero_tile_ind - config.N)) < max_index:
            legal_actions.append(up_ind)
        if 0 <= (right_ind := (zero_tile_ind + 1)) < max_index and right_ind % config.N:
            legal_actions.append(right_ind)
        if 0 <= (down_ind := (zero_tile_ind + config.N)) < max_index:
            legal_actions.append(down_ind)
        if 0 <= (left_ind := (zero_tile_ind - 1)) < max_index and (left_ind + 1) % config.N:
            legal_actions.append(left_ind)
        return legal_actions

    def apply_action(self, state, action):
        self.nodes_generated += 1
        copy_state = list(state)
        zero_tile_ind = state.index(0)
        copy_state[action], copy_state[zero_tile_ind] = copy_state[zero_tile_ind], copy_state[action]
        return tuple(copy_state)

    def get_steps(self, initial_state, goal_state):
        pass

    def get_solution_steps(self, initial_state, goal_state):
        begin_time = time.time()
        solution_actions = self.get_steps(initial_state, goal_state)
        print(f'Execution time in seconds: {(time.time() - begin_time):.2f} | '
              f'Nodes generated: {self.nodes_generated} | '
              f'Nodes evaluated: {self.nodes_evaluated}')
        return solution_actions


class ExampleAlgorithm(Algorithm):
    def get_steps(self, initial_state, goal_state):
        state = initial_state
        solution_actions = []
        while state != goal_state:
            legal_actions = self.get_legal_actions(state)
            action = legal_actions[random.randint(0, len(legal_actions) - 1)]
            solution_actions.append(action)
            state = self.apply_action(state, action)
        return solution_actions

from collections import deque
import heapq

class BFS(Algorithm):
    def get_steps(self, initial_state, goal_state):
        visited_nodes = set()
        queue_states = deque([initial_state])
        queue_solutions = deque([])

        while queue_states:
            curr_state = queue_states.popleft()
            if(queue_solutions): curr_solution = queue_solutions.popleft()
            else: curr_solution = []

            #ako je pronadjeno krajnje stanje onda se vraca lista akcija
            if(curr_state == goal_state): return curr_solution

            #u suprotnom se prave sva moguca pomeranja ako cvor nijje posecen,
            #beleze se moguce akcije i dodaju u red i belezi se da je cvor posecen (cvor je state)
            if(curr_state not in visited_nodes):
                visited_nodes.add(curr_state)
                legal_actions = self.get_legal_actions(curr_state)
                for action in legal_actions:
                    new_state = self.apply_action(curr_state, action)
                    new_solution = curr_solution + [action]
                    if (new_state == goal_state): return new_solution
                    queue_states.append(new_state)
                    queue_solutions.append(new_solution)

        return None

class Best_First(Algorithm):
    def __init__(self, heuristic=None):
        super().__init__(heuristic)

    def get_steps(self, initial_state, goal_state):
        heuristic = self.heuristic.get_evaluation(initial_state)
        heap = []
        #heuristic, state, path
        heapq.heappush(heap, (0, (initial_state), []))
        visited_nodes = set()

        while heap:
            curr_heuristic, curr_state, curr_solution = heapq.heappop(heap)

            if (curr_state == goal_state): return curr_solution

            if(curr_state not in visited_nodes):
                visited_nodes.add(curr_state)
                legal_actions = self.get_legal_actions(curr_state)
                for action in legal_actions:
                    new_state = self.apply_action(curr_state, action)
                    new_solution = curr_solution + [action]
                    new_heuristic = self.heuristic.get_evaluation(new_state)
                    if(new_state == goal_state): return new_solution
                    heapq.heappush(heap, (new_heuristic, (new_state), new_solution))

        return None

class A_Star(Algorithm):
    def __init__(self, heuristic=None):
        super().__init__(heuristic)

    def get_steps(self, initial_state, goal_state):
        heuristic = self.heuristic.get_evaluation(initial_state)
        heap = []
        #price + heuristic, initial_state, heuristic, path, price
        heapq.heappush(heap, (0, (initial_state), 0,  [], 0))
        visited_nodes = set()

        while list:
            curr_sum, curr_state, curr_heuristic, curr_solution, curr_price = heapq.heappop(heap)

            if (curr_state == goal_state): return curr_solution

            if(curr_state not in visited_nodes):
                visited_nodes.add(curr_state)
                legal_actions = self.get_legal_actions(curr_state)
                for action in legal_actions:
                    new_state = self.apply_action(curr_state, action)
                    new_solution = curr_solution + [action]
                    if (new_state == goal_state): return new_solution
                    new_heuristic = self.heuristic.get_evaluation(new_state)
                    new_price = curr_price + 1
                    new_sum = new_price + new_heuristic
                    heapq.heappush(heap, (new_sum, (new_state), new_heuristic, new_solution, new_price))
        return None