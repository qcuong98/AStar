from tkinter import *
from tkinter import messagebox
from array import *
from tkinter.filedialog import askopenfilename
import math
import heapq
import time

# region A Star initialization
n = 1
Sx = 0
Sy = 0
Gx = 0
Gy = 0
arr = [[]]
visited = set()
# endregion

# region Window layout

# Window object
window = Tk()
# window.geometry("700x500")
window.minsize(width=800, height=600)
window.grid_propagate(0)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=0)
window.grid_rowconfigure(0, weight=1)

# Left frame (contains main canvas)
left_frame = Frame(window, background='#93bbff')
left_frame.grid(column=0, row=0, sticky='snew')
#    Main canvas
main_canvas = Canvas(left_frame, background='#93bbff')
main_canvas.pack(fill=BOTH, expand=1)

# Right frame (contains legends)
right_frame = Frame(window, width=200, background='#5d6496')
right_frame.grid(column=1, row=0, sticky='snew')
right_frame.grid_propagate(0)

loadinput_button = Button(right_frame, text="Load input ...")
loadinput_button.grid(column=0, row=0, sticky='snew')
run_button = Button(right_frame, text="Run", state=DISABLED)
run_button.grid(column=0, row=1, sticky='snew')
saveoutput_button = Button(
    right_frame, text="Export results...", state=DISABLED)
saveoutput_button.grid(column=0, row=2, sticky='snew')

# Drawing objects:
#    Dimensions (ignore initial values)
grid_width_graphical = 0
grid_height_graphical = 0
grid_cell_size = 20
grid_width_cells = 0
grid_height_cells = 0
grid_padding = 150
x_left_corner = 0
y_top_corner = 0
#    Graphical cells map:
grid_cells = {}
#    Graphical cells states:
grid_cell_states = {
    "OBSTACLE": "#85a9e5",
    "START": "#ff6d00",
    "GOAL": "#00c853",
    "STATE_PUSH": "#ff0000",
    "STATE_POP": "#00ff00",
    "STATE_FINAL": "#00ffff"
}
#   Graphical cells text:
grid_cell_text = {}
last_cell = 0
# endregion

# region Window events


def reconfigure_sizes(event):
    global grid_width_graphical
    global grid_height_graphical
    global grid_cell_size
    global x_left_corner
    global y_top_corner

    if grid_width_cells == 0 and grid_height_cells == 0:
        return

    width_sustain = (main_canvas.winfo_width() - 2 *
                     grid_padding) / grid_width_cells
    height_sustain = (main_canvas.winfo_height() - 2 *
                      grid_padding) / grid_height_cells
    grid_cell_size = min(width_sustain, height_sustain)

    grid_height_graphical = grid_cell_size * grid_height_cells
    grid_width_graphical = grid_cell_size * grid_width_cells

    x_left_corner = main_canvas.winfo_width() / 2 - grid_width_graphical / 2
    y_top_corner = main_canvas.winfo_height() / 2 - grid_height_graphical / 2

    for x in range(grid_width_cells):
        for y in range(grid_height_cells):
            main_canvas.coords(grid_cells[(x, y)],
                               x_left_corner+x*grid_cell_size,
                               y_top_corner+y*grid_cell_size,
                               x_left_corner+(x+1)*grid_cell_size,
                               y_top_corner+(y+1)*grid_cell_size)


def create_grid(height, width):
    global grid_cells
    global grid_width_cells
    global grid_height_cells

    for x in range(grid_width_cells):
        for y in range(grid_height_cells):
            main_canvas.delete(grid_cells[(x, y)])
            del grid_cells[(x, y)]

    grid_width_cells = width
    grid_height_cells = height

    for x in range(width):
        for y in range(height):
            grid_cells[(x, y)] = main_canvas.create_rectangle(
                grid_padding+x*grid_cell_size,
                grid_padding+y*grid_cell_size,
                grid_padding+(x+1)*grid_cell_size,
                grid_padding+(y+1)*grid_cell_size,
                outline="#85a9e5")

    reconfigure_sizes(None)


def set_cell_state(x, y, state):
    if ((x, y) == (Sx, Sy) and state != "START") or ((x,y) == (Gx, Gy) and state != "GOAL"):
        return
    main_canvas.itemconfig(grid_cells[(y, x)], fill=grid_cell_states[state])
    main_canvas.update_idletasks()
    time.sleep(.100)


def set_cell_text(x, y, cell_text):

    
    #x = main_canvas.itemcget(grid_cells[(x,y)], 'x')
    #y = main_canvas.itemcget(grid_cells[(x,y)], 'y')
    x1 = main_canvas.coords(grid_cells[(x, y)])[0]
    y1 = main_canvas.coords(grid_cells[(x, y)])[1]
    x2 = main_canvas.coords(grid_cells[(x, y)])[2]
    y2 = main_canvas.coords(grid_cells[(x, y)])[3]
    px = (x1 + x2) / 2
    py = (y1 + y2) / 2

    main_canvas.create_text(px, py, fill="darkblue", font="monospace 10",
                            text=cell_text)


def loadinput_click():
    global Sx, Sy
    global Gx, Gy
    global arr
    global n
    filename = askopenfilename(title="Select input", filetypes=[
        ("All files", "*.*")])
    if not filename:    # cancel
        return

    f = open(filename, "r")
    n = int(f.readline())
    Sx, Sy = [int(x) for x in next(f).split()]
    Gx, Gy = [int(x) for x in next(f).split()]
    arr = [[int(x) for x in line.split()] for line in f]

    create_grid(n, n)
    run_button.configure(state="normal")

    for x in range(n):
        for y in range(n):
            if arr[x][y] == 1:
                set_cell_state(x, y, "OBSTACLE")

    set_cell_state(Sx, Sy, "START")
    set_cell_state(Gx, Gy, "GOAL")

def run_click():
    global Sx
    global Sy
    global Gx
    global Gy
    (ff, path) = aStar(Sx, Sy, Gx, Gy)
    for (x,y) in reversed(path):
        set_cell_state(x, y, "STATE_FINAL")
    if ff==-1 :
        messagebox.showinfo("", "Can't find a path!")

def window_postinit():
    loadinput_button.configure(command=loadinput_click)
    run_button.configure(command=run_click)


def test(event):
    #print(event.x, ' - ', event.y)
    global last_cell
    x = (int)((event.x - x_left_corner) / (grid_cell_size))
    y = (int)((event.y - y_top_corner) / (grid_cell_size))

    if last_cell != -1:
        main_canvas.itemconfig(last_cell, fill='')

    last_cell = -1

    if x < 0 or x >= grid_width_cells:
        return

    if y < 0 or y >= grid_height_cells:
        return

    set_cell_state(x, y, "STATE_3")
    last_cell = grid_cells[(x, y)]

    grid_cells[(x, y)]


def button_click():
    create_grid(4, 9)
    set_cell_text(2, 2, "20")

# endregion

# region A Star routines


def sqr(a):
    return a * a

# euclidean distance


def heuristic(x, y):
    return math.sqrt(sqr(Gx - x) + sqr(Gy - y))

# cells that robot can go from (x, y)


def listCellsCanGoFrom(x, y):
    ans = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            (u, v) = (x + i, y + j)
            if (u in range(n)) and (v in range(n)) and \
               (arr[u][v] != 1) and ((u, v) not in visited):
                ans.append((u, v))
    return ans


def aStar(Sx, Sy, Gx, Gy):
    g = [x[:] for x in [[float("inf")] * n] * n]
    h = [x[:] for x in [[0] * n] * n]
    f = [x[:] for x in [[0] * n] * n]
    tr = [x[:] for x in [[(0, 0)] * n] * n]

    g[Sx][Sy] = 0
    for i in range(n):
        for j in range(n):
            h[i][j] = heuristic(i, j)
            f[i][j] = g[i][j] + h[i][j]

    heap = [(f[Sx][Sy], Sx, Sy)]
    heapq.heapify(heap)

    while (len(heap) != 0):
        (ff, x, y) = heapq.heappop(heap)
        set_cell_state(x,y, "STATE_POP")
        # printHeap(heap)

        if (x, y) == (Gx, Gy):
            path = []
            while (x, y) != (Sx, Sy):
                path.append((x, y))
                (x, y) = tr[x][y]
            path.append((Sx, Sy))
            path.reverse()
            return (ff, path)

        if (x, y) not in visited:
            visited.add((x, y))

            listNextCells = listCellsCanGoFrom(x, y)
            for (u, v) in listNextCells:
                cost = g[x][y] + 1
                if (cost < g[u][v]):
                    tr[u][v] = (x, y)
                    g[u][v] = cost
                    f[u][v] = cost + h[u][v]
                    heapq.heappush(heap, (f[u][v], u, v))
                    set_cell_state(u,v, "STATE_PUSH")
                    # printHeap(heap)

    return (-1, [])
# endregion

# region Entry point


#create_grid(5, 10)
window.after(0, window_postinit)
window.bind("<Configure>", reconfigure_sizes)
#main_canvas.bind("<Motion>", test)

window.mainloop()
# endregion
