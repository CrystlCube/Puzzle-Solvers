import copy
import tkinter as tk

class Towers:
    def __init__(self, input_size, test_case) -> None:
        self.setup_start_screen()

        self.restrict_by_start()
        self.solve()

    def setup_start_screen(self):
        self.root = tk.Tk()
            
        window_width = 300
        window_height = 200
        center_x = 500
        center_y = 300
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        tk.Label(self.root, text='Welcome to Towers!').pack()
        self.slider = tk.Scale(self.root, to=10, orient='horizontal')
        self.slider.pack()
        tk.Button(self.root, text='Start', command=self.start_game).pack()

        self.root.mainloop()

    def setup_game_screen(self):
        self.root.columnconfigure(0, weight=2)
        for i in range(self.size):
            self.root.columnconfigure(i+1, weight=1)
        self.root.columnconfigure(self.size+1, weight=2)
        
        self.root.rowconfigure(0, weight=2)
        for i in range(self.size):
            self.root.rowconfigure(i+1, weight=1)
        self.root.rowconfigure(self.size+1, weight=2)

        for i in range(self.size):
            entry = tk.Entry(self.root)
            entry.grid(row=0, column=i+1, stick=tk.EW)
            entry.bind("<KeyRelease>", self.save_value)
        for i in range(self.size):
            entry = tk.Entry(self.root)
            entry.grid(row=self.size+1, column=i+1, stick=tk.EW)
            entry.bind("<KeyRelease>", self.save_value)
        for i in range(self.size):
            entry = tk.Entry(self.root)
            entry.grid(row=i+1, column=0, stick=tk.EW)
            entry.bind("<KeyRelease>", self.save_value)
        for i in range(self.size):
            entry = tk.Entry(self.root)
            entry.grid(row=i+1, column=self.size+1, stick=tk.EW)
            entry.bind("<KeyRelease>", self.save_value)

        for i in range(self.size):
            for j in range(self.size):
                entry = tk.Entry(self.root)
                entry.grid(row=i+1, column=j+1)
                entry.bind("<KeyRelease>", self.save_value)

    def save_value(self, event):
        widget = event.widget
        info = widget.grid_info()
        row = info['row']-1
        col = info['column']-1

        top_or_bottom = row < 0 or row >= self.size
        if top_or_bottom or col < 0 or col >= self.size:
            side = int(row >= self.size) if top_or_bottom else 2 + int(col >= self.size)
            index = col if top_or_bottom else row
            self.readings[side][index] = int(widget.get())
        else:
            self.field_vals[row][col] = set([int(widget.get())])

    def start_game(self):
        self.size = self.slider.get()
        self.field_vals = [[set(range(1,self.size+1)) for i in range(self.size)] for j in range(self.size)]
        self.readings = [[0 for i in range(self.size)] for j in range(4)]

        self.clear_screen()
        self.setup_game_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def get_start_vals(self):
        top_readings_str = input("Enter the values of the top row from left to right without separation. Blank values should be entered as zeros (i.e. 503221):\n")
        self.readings[0] = [int(i) for i in top_readings_str]
        bottom_readings_str = input("Enter the values of the bottom row from left to right without separation. Blank values should be entered as zeros (i.e. 503221):\n")
        self.readings[1] = [int(i) for i in bottom_readings_str]
        left_readings_str = input("Enter the values of the left column from top to bottom without separation. Blank values should be entered as zeros (i.e. 503221):\n")
        self.readings[2] = [int(i) for i in left_readings_str]
        right_readings_str = input("Enter the values of the right column from top to bottom without separation. Blank values should be entered as zeros (i.e. 503221):\n")
        self.readings[3] = [int(i) for i in right_readings_str]

    
    def restrict_by_start(self):
        for side in range(4):
            is_row = side > 1
            invert = side % 2

            for index in range(self.size):
                start_val = self.readings[side][index]
                if start_val != 0:
                    row = index if is_row else (0 if not invert else self.size-1)
                    col = index if not is_row else (0 if not invert else self.size-1)
                    i = 0
                    while start_val-i > 1:
                        self.field_vals[row][col] = set(range(1,2+self.size-start_val+i)).intersection(self.field_vals[row][col])
                        i += 1
                        row += 0 if is_row else (-1 if invert else 1)
                        col += 0 if not is_row else (-1 if invert else 1)
    

    def given_mid_vals(self):
        while True:
            user_input = input('If you have a value already filled in, specift its x, y, and value (i.e. 2 1 3 means a 3 in the 3rd row and 2nd column)\nIf you don\'t have any more values, simply type quit.\n')
            if user_input == 'quit':
                return
            x,y,val = [int(i) for i in user_input.split(' ')]
            self.field_vals[x][y] = set([val])

    def solve(self):
        grid = [[0 for i in range(self.size)] for j in range(self.size)]
        print(self.solve_helper(grid))

    def solve_helper(self, grid):
        result = self.get_random_pos(grid)
        if result:
            x, y = result
            for val in self.field_vals[x][y]:
                if not self.find_in_row_col(grid, x, y, val):
                    grid[x][y] = val
                    final_result = self.solve_helper(copy.deepcopy(grid))
                    if final_result:
                        return final_result
            return False
        else:
            return self.evaluate_grid(grid)
        
    def find_in_row_col(self, grid, x, y, val):
        for i in range(self.size):
            if val == grid[x][i] or val == grid[i][y]:
                return True
        return False

    def evaluate_grid(self, grid):
        for side in range(4):
            is_row = side > 1
            invert = side % 2

            for index in range(self.size):
                start_val = self.readings[side][index]
                if start_val != 0:
                    row = index if is_row else (0 if not invert else self.size-1)
                    col = index if not is_row else (0 if not invert else self.size-1)
                    i = 0
                    max = 0
                    count = 0
                    while i < self.size:
                        if grid[row][col] > max:
                            max = grid[row][col]
                            count += 1
                        if grid[row][col] == self.size:
                            if count != start_val:
                                return False
                        i += 1
                        row += 0 if is_row else (-1 if invert else 1)
                        col += 0 if not is_row else (-1 if invert else 1)
        return grid

    def get_random_pos(self, grid):
        for i in range(self.size):
            for j in range(self.size):
                if grid[i][j] == 0:
                    return i,j
        return False
                


if __name__ == "__main__":
    size = 6 #int(input('What size of board are you playing with?\n'))
    test_case_1 = [[2,5,2,1,4],[2,1,2,4,2],[3,3,1,3,2],[2,3,2,1,4]]
    tower = Towers(size, [])