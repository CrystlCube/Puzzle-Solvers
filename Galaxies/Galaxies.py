class Galaxies:
    def __init__(self, input_size, test_case = []) -> None:
        self.size = input_size
        self.centers = test_case
        self.board = [[-1 for _ in range(self.size)] for _ in range(self.size)]

        self.input_centers()
        self.random_solver_starter()
        self.output_grid()

    def input_centers(self):
        if not self.centers:
            while True:
                user_input = input('Enter a center in the following format: X,Y. If you are finished, type \'quit\'.\n')
                if user_input == 'quit':
                    return
                self.centers.append([float(i) for i in user_input.split(',')])

    def output_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                print(chr(self.board[i][j]+65), end='')
            print()

    def out_of_bounds(self, point):
        return point < 0 or point >= self.size
    
    def setup_board(self):
        for id in range(len(self.centers)):
            x, y = self.centers[id]
            x_range = [int(x)]
            if int(x) != x:
                x_range.append(int(x+0.5))
            y_range = [int(y)]
            if int(y) != y:
                y_range.append(int(y+0.5))
            for x in x_range:
                for y in y_range:
                    self.board[x][y] = id

    def solver(self):
        self.setup_board()
        free_spot = True
        while free_spot:
            free_spot = False
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == -1:
                        free_spot = True
                        found_center = 0
                        center_id = 0
                        for c_id in range(len(self.centers)):
                            x, y = self.centers[c_id]
                            a = int(2*x - i)
                            b = int(2*y - j)
                            if not self.out_of_bounds(a) and not self.out_of_bounds(b):
                                if self.board[a][b] == -1:
                                    if found_center:
                                        found_center = 2
                                        break
                                    else:
                                        found_center = 1
                                        center_id = c_id
                                        r_i = a
                                        r_j = b
                        if found_center == 1:
                            self.board[i][j] = center_id
                            self.board[r_i][r_j] = center_id


    def random_solver_starter(self):
        unlocked = [i for i in range(len(self.centers))]
        self.setup_board()
        self.random_solver(self.board, unlocked)


    def get_neighbors(self, node, grid):
        neighbors = set()
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] == node:
                    if i != 0 and grid[i-1][j] == -1:
                        neighbors.add((i-1, j))
                    if j != 0 and grid[i][j-1] == -1:
                        neighbors.add((i, j-1))
        return neighbors


    def random_solver(self, grid, unlocked):
        new_unlocked = unlocked.copy()
        for node in unlocked:
            for neighbor in self.get_neighbors(node, grid):
                x, y = self.centers[node]
                a = int(2*x - neighbor[0])
                b = int(2*y - neighbor[1])
                if not self.out_of_bounds(a) and not self.out_of_bounds(b) and grid[a][b] == -1:
                    grid[neighbor[0]][neighbor[1]] = node
                    grid[a][b] = node
                    result = self.random_solver(grid, new_unlocked)
                    if not result:
                        grid[neighbor[0]][neighbor[1]] = -1
                        grid[a][b] = -1
                    else:
                        return result
                        
            new_unlocked.remove(node)
        
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] == -1:
                    return False
        return grid
                    



if __name__ == "__main__":
    size = int(input('What size of board are you playing with?\n'))
    test_1 = [[0,2],[0.5,0.5],[0.5,6],[1,3],[1.5,4],[2,0],[3,5.5],[3.5,2],[5,0.5],[5,4.5],[6,4.5]]
    test_2 = [[0,0],[0,3],[0,8],[1,1.5],[1,4],[1,9],[1.5,6],[2,0],[2,8],[2.5,5],[3,2],[4,2],[5,5],[5,6.5],[5,9],[5.5,8],[6,0],[6.5,2],[6.5,3],[6.5,4],[7.5,9],[8,6],[8.5,0.5],[8.5,8],[9,3.5],[9,7]]
    gal = Galaxies(size, test_2)

