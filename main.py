import tkinter as tk
import random
import ctypes

# Default settings
DEFAULT_ROWS = 30
DEFAULT_COLS = 30
DEFAULT_CELL_SIZE = 15
DEFAULT_SPEED = 100

# Colors
BG_COLOR = "#000"
GRID_COLOR = "#222"
LIVE_COLOR = "#fff"

running = False

# Grid variables
ROWS = DEFAULT_ROWS
COLS = DEFAULT_COLS
CELL_SIZE = DEFAULT_CELL_SIZE
SPEED = DEFAULT_SPEED

grid = []


class CellularAutomata:
    def __init__(self, root):
        self.root = root
        self.root.title("Cellular Automata")
        root.iconbitmap("resources/icon.ico")

        # ===== Settings Frame =====
        settings_frame = tk.Frame(root)
        settings_frame.pack(pady=5)

        tk.Label(settings_frame, text="Rows").grid(row=0, column=0)
        self.rows_entry = tk.Entry(settings_frame, width=5)
        self.rows_entry.insert(0, str(DEFAULT_ROWS))
        self.rows_entry.grid(row=0, column=1)

        tk.Label(settings_frame, text="Cols").grid(row=0, column=2)
        self.cols_entry = tk.Entry(settings_frame, width=5)
        self.cols_entry.insert(0, str(DEFAULT_COLS))
        self.cols_entry.grid(row=0, column=3)

        tk.Label(settings_frame, text="Cell Size").grid(row=0, column=4)
        self.cell_entry = tk.Entry(settings_frame, width=5)
        self.cell_entry.insert(0, str(DEFAULT_CELL_SIZE))
        self.cell_entry.grid(row=0, column=5)

        tk.Label(settings_frame, text="Speed (ms)").grid(row=0, column=6)
        self.speed_entry = tk.Entry(settings_frame, width=6)
        self.speed_entry.insert(0, str(DEFAULT_SPEED))
        self.speed_entry.grid(row=0, column=7)

        apply_button = tk.Button(
            settings_frame,
            text="Apply",
            command=self.apply_settings
        )
        apply_button.grid(row=0, column=8, padx=5)

        # ===== Canvas =====
        self.canvas = tk.Canvas(root, bg=BG_COLOR)
        self.canvas.pack()

        # ===== Controls =====
        controls = tk.Frame(root)
        controls.pack(pady=5)

        self.start_button = tk.Button(
            controls,
            text="Start",
            command=self.start_stop
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(
            controls,
            text="Clear",
            command=self.clear
        )
        clear_button.pack(side=tk.LEFT, padx=5)

        random_button = tk.Button(
            controls,
            text="Random",
            command=self.randomize
        )
        random_button.pack(side=tk.LEFT, padx=5)

        # Mouse interaction
        self.canvas.bind("<Button-1>", self.toggle_cell)

        # Initialize grid
        self.create_grid()

    def create_grid(self):
        global grid, ROWS, COLS, CELL_SIZE

        width = COLS * CELL_SIZE
        height = ROWS * CELL_SIZE

        self.canvas.config(width=width, height=height)

        grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        self.draw()

    def apply_settings(self):
        global ROWS, COLS, CELL_SIZE, SPEED

        try:
            ROWS = int(self.rows_entry.get())
            COLS = int(self.cols_entry.get())
            CELL_SIZE = int(self.cell_entry.get())
            SPEED = int(self.speed_entry.get())

            self.create_grid()

        except ValueError:
            print("Invalid input")

    def draw(self):
        self.canvas.delete("all")

        for y in range(ROWS):
            for x in range(COLS):

                x1 = x * CELL_SIZE
                y1 = y * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = LIVE_COLOR if grid[y][x] else BG_COLOR

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline=GRID_COLOR
                )

    def count_neighbors(self, x, y):
        total = 0

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:

                if dx == 0 and dy == 0:
                    continue

                nx = (x + dx) % COLS
                ny = (y + dy) % ROWS

                total += grid[ny][nx]

        return total

    def update(self):
        global grid, running

        new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

        for y in range(ROWS):
            for x in range(COLS):

                neighbors = self.count_neighbors(x, y)

                if grid[y][x] == 1:
                    if neighbors in [2, 3]:
                        new_grid[y][x] = 1
                else:
                    if neighbors == 3:
                        new_grid[y][x] = 1

        grid = new_grid

        self.draw()

        if running:
            self.root.after(SPEED, self.update)

    def toggle_cell(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE

        if 0 <= x < COLS and 0 <= y < ROWS:
            grid[y][x] = 1 - grid[y][x]
            self.draw()

    def start_stop(self):
        global running

        running = not running

        if running:
            self.start_button.config(text="Pause")
            self.update()
        else:
            self.start_button.config(text="Start")

    def clear(self):
        global grid

        grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.draw()

    def randomize(self):
        global grid

        grid = [
            [random.choice([0, 1]) for _ in range(COLS)]
            for _ in range(ROWS)
        ]

        self.draw()

# IMPORTANT: set BEFORE Tk()
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    "cellular.automata.app"
)

# Run app
root = tk.Tk()
app = CellularAutomata(root)
root.mainloop()