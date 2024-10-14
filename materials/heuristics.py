class Heuristic:
    def get_evaluation(self, state):
        pass


class ExampleHeuristic(Heuristic):
    def get_evaluation(self, state):
        return 0

class Hamming(Heuristic):
    def get_evaluation(self, state):
        positions = []
        for i in range(len(state) - 1):
            positions.append(i + 1)
        positions.append(0)
        ham = 0
        for i in range(len(state)):
            if(state[i] != positions[i]): ham += 1
        return ham

class Manhattan(Heuristic):
    def get_evaluation(self, state):
        size = int(len(state) ** 0.5)
        positions = []
        for i in range(len(state) - 1):
            positions.append(i + 1)
        positions.append(0)

        manh = 0
        for value in state:
            if value != 0:
                index1 = state.index(value)
                index2 = positions.index(value)
                row1, col1 = divmod(index1, size)
                row2, col2 = divmod(index2, size)
                manh += abs(row1 - row2) + abs(col1 - col2)
        return manh
