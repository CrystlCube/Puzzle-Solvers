class Galaxies:
    def __init__(self, input_size, test_case = []) -> None:
        self.size = input_size
        self.centers = test_case
        self.board = [[-1 for _ in range(self.size)] for _ in range(self.size)]

        self.input_centers()
        self.solver()
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

    def solver(self):
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


if __name__ == "__main__":
    size = int(input('What size of board are you playing with?\n'))
    test_1 = [[0,2],[0.5,0.5],[0.5,6],[1,3],[1.5,4],[2,0],[3,5.5],[3.5,2],[5,0.5],[5,4.5],[6,4.5]]
    gal = Galaxies(size, test_1)

