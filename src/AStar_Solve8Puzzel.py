class Node:
    def __init__(self:'Node', data: list, level: int, fval: int):
        """
        @brief: Initializes a Node Object
        @param: data: list(State Matrix), level: int, fval(Hueristic Value): int
        """
        self.data = data
        self.level = level
        self.fval = fval

    def copy(self: 'Node', state: list) -> list:
        """
        @brief: Copies the state matrix
        """
        tempory = []
        for i in range(0, len(state)):
            tempory.append(state[i][:])
        return tempory


    def shuffle(self: 'Node', state: list, x1: int, y1: int, x2: int, y2: int) -> list:
        """
        @brief: Shuffles the empty space in the puzzle if the position value is
                out of bounds then return None
        """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            tempory = []
            tempory = self.copy(state)
            tempVal = tempory[x2][y2]
            tempory[x2][y2] = tempory[x1][y1]
            tempory[x1][y1] = tempVal
            return tempory

        else:
            return None


    def generateSuccessors(self: 'Node') -> list:
        """
        @brief: Generates the sucessor state by moving the
                empty space in four directions
        """

        x, y = self.find(self.data, '_')

        # valList will constians the the values for moving the empty space
        # in either of the four directions resectively
        valList = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []

        for i in valList:
            child = self.shuffle(self.data, x, y, i[0], i[1])
            if child is not None:
                childNode = Node(child, self.level + 1, 0)
                children.append(childNode)
        return children


    def find(self: 'Node', state: list, value: str) -> tuple:
        """
        @brief: Finds the position of the empty space in the puzzle
        """
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if self.data[i][j] == value:
                    return i, j


class Puzzle:
    def __init__(self: 'Puzzle', size: int):
        """
        @brief: Initailizes a Puzzle of specified sizes
        and Sets the open and closed lists to empty Lists
        """
        self.size = size
        self.open = []
        self.closed = []
        self.count = 0


    def accept(self: 'Puzzle'):
        """
        @brief: method to accept the puzzle from the user
        @param: self
        @return: Puzzle Matrix : list
        @useage: input the puzzle as a 2D Matrix
        note: the while spaces are removed in the input phase
        """
        tempPuzzle = []
        for i in range(self.size):
            temp = input().split()
            tempPuzzle.append(temp)
        return tempPuzzle


    def heuristic(self: 'Puzzle', initial: list, goal: list) -> int:
        # Heuristic Fuction to calculate the hueristic value
        # f(x) = h(x) + g(x)
        # We are using the number of misplaced tiles
        return self.misplacedTiles(initial.data, goal) + initial.level


    def misplacedTiles(self: 'Puzzle', intial: list, goal: list) -> int:
        """
        @brief: Calculates the number of misplaced tiles
        @param: intial: list, goal: list
        @return: int
        """
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if intial[i][j] != goal[i][j] and intial[i][j] != '_':
                    count += 1
        return count


    def printArrowHeads(self) -> None:
        # prints the arrow heads for cleaner output
        print("")
        print("  |  ")
        print("  |  ")
        print(" \\\'/\n")


    def solvePuzzle(self: 'Puzzle'):
        """
        @brief: Solves the puzzle using A* Algorithm where the heuristic function
                uses the number of misplaced tiles
        """

        # Accept The Initial Puzzle State
        print("Enter the Initial State of the Puzzle\nIn Matrix Format\n")
        initial = self.accept()

        # Accept The Goal Puzzle State
        print("\n\nEnter the Goal State of the Puzzle\nIn Matriz Format\n")
        goal = self.accept()

        # Create a Node
        initial = Node(initial, 0, 0)
        initial.fval = self.heuristic(initial, goal)

        # as per the method we append the open list with node inital
        self.open.append(initial)

        print("\n\n\nComputing Solution......\n\nInitial State \n")

        # Solving and Printing the Solution
        while True:
            """
            @brief: a node at the start of the list open
                    where open is a list of States
            """
            current = self.open[0]

            for i in current.data:
                for j in i:
                    print(j, end=" ")
                print("")

            self.printArrowHeads()

            # if the current state is the goal state
            # then the difference of misplaced tiles will be 0
            # hence we break
            if(self.misplacedTiles(current.data, goal) == 0):
                break

            # if the current state is not the goal state
            for i in current.generateSuccessors():
                i.fval = self.heuristic(i, goal)
                # we append the generated successors to the open list
                self.open.append(i)
            self.closed.append(current)
            del self.open[0]

            # sort the open list according to the f(x) value
            self.open.sort(key=lambda x: x.fval, reverse=False)
        print("\n\nGoal State Reached\n\n")



def main():
    puzzle = Puzzle(3)
    puzzle.solvePuzzle()


if __name__ == '__main__':
    main()
