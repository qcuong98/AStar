from tkinter import *
from tkinter import messagebox
from array import *
from tkinter.filedialog import askopenfilename
import math
import heapq
import time

# region A Star initialization
n = 1
Sx = -1
Sy = -1
Gx = -1
Gy = -1
arr = [[]]
adj = [[]]
visited = set()


def initialize_astar():
    global n
    global Sx
    global Sy
    global Gx
    global Gy
    global arr
    global visited

    n = 1
    Sx = -1
    Sy = -1
    Gx = -1
    Gy = -1
    arr = [[]]
    visited = set()
# endregion

# region Window layout

# Theming
COLOR_RIGHTPANEL_BACKGROUND = '#c3fdff' 
COLOR_RIGHTPANEL_FOREGROUND = "#102027"
COLOR_LEFTCANVAS_BACKGROUND = "#90caf9"

# Window object
window = Tk()
# window.geometry("700x500")
window.minsize(width=800, height=600)
window.grid_propagate(0)
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# Left frame (contains main canvas)
left_frame = Frame(window)
left_frame.grid(column=0, row=0, sticky='snew')
#    Main canvas
main_canvas = Canvas(left_frame, background=COLOR_LEFTCANVAS_BACKGROUND)
main_canvas.pack(fill=BOTH, expand=1)

# Right frame (contains legends)
right_frame = Frame(window, width=200, background=COLOR_RIGHTPANEL_BACKGROUND)
right_frame.grid(column=1, row=0, sticky='snew')
right_frame.grid_propagate(0)

loadinput_button = Button(right_frame, text="Load input ...")
loadinput_button.grid(column=0, row=0, sticky='snew', pady=10, padx=10)

run_button = Button(right_frame, text="Run from file", state=DISABLED)
run_button.grid(column=0, row=1, sticky='snew', pady=5, padx=10)

saveoutput_button = Button(
    right_frame, text="Export results...", state=DISABLED)
saveoutput_button.grid(column=0, row=2, sticky='snew', pady=5, padx=10)

reset_button = Button(right_frame, text="Reset states")
reset_button.grid(column=0, row=3, sticky='snew', pady=5, padx=10)

create_grid_label = Label(right_frame, text="Grid size (n×n):",
                          background=COLOR_RIGHTPANEL_BACKGROUND, foreground=COLOR_RIGHTPANEL_FOREGROUND, justify=LEFT)
create_grid_label.grid(column=0, row=4, sticky='w', pady=5, padx=10)

create_grid_size_textbox = Entry(right_frame)
create_grid_size_textbox.grid(column=0, row=5, sticky='snew', padx=10)

create_grid_button = Button(right_frame, text="Create empty grid")
create_grid_button.grid(column=0, row=6, sticky='snew', pady=5, padx=10)

edit_map_label = Label(right_frame, text="Mode:",
                       background=COLOR_RIGHTPANEL_BACKGROUND, foreground=COLOR_RIGHTPANEL_FOREGROUND, justify=LEFT)
edit_map_label.grid(column=0, row=7, sticky='w', pady=5, padx=10)

edit_mode_var = IntVar()
MODE_NORMAL = 0
MODE_OBSTACLE = 1
MODE_START = 2
MODE_GOAL = 3

Radiobutton(right_frame, text="Travelable", background=COLOR_RIGHTPANEL_BACKGROUND, variable=edit_mode_var, value=0).grid(column=0, row=8, sticky='w', pady=5, padx=10)
Radiobutton(right_frame, text="Obstacle", background=COLOR_RIGHTPANEL_BACKGROUND, variable=edit_mode_var, value=1).grid(column=0, row=9, sticky='w', pady=5, padx=10)
Radiobutton(right_frame, text="Start", background=COLOR_RIGHTPANEL_BACKGROUND, variable=edit_mode_var, value=2).grid(column=0, row=10, sticky='w', pady=5, padx=10)
Radiobutton(right_frame, text="Goal", background=COLOR_RIGHTPANEL_BACKGROUND, variable=edit_mode_var, value=3).grid(column=0, row=11, sticky='w', pady=5, padx=10)

run_gui_button = Button(right_frame, text="Run from GUI")
run_gui_button.grid(column=0, row=12, sticky='snew', pady=5, padx=10)

# Drawing objects:
#    Dimensions (ignore initial values)
grid_width_graphical = 0
grid_height_graphical = 0
grid_cell_size = 20
grid_width_cells = 0
grid_height_cells = 0
grid_padding = 50
x_left_corner = 0
y_top_corner = 0
hover_box = main_canvas.create_rectangle(
    -100, -100, -100, -100, fill="#ff00ff", outline="#5272a8")
#    Graphical cells map:
grid_cells = {}
#    Graphical cells states:
grid_cell_states_color = {
#    "OBSTACLE": "#85a9e5",
    "OBSTACLE": "#5272a8",
    "START": "#ff6d00",
    "GOAL": "#00c853",
    "STATE_NORMAL": "#93bbff",
    "STATE_HOVER": "#ffffff",
    "STATE_PUSH": "#ff0000",
    "STATE_POP": "#00ff00",
    "STATE_FINAL": "#00ffff"
}
mode_state = {
    MODE_NORMAL: "STATE_NORMAL",
    MODE_OBSTACLE: "OBSTACLE",
    MODE_START: "START",
    MODE_GOAL: "GOAL"
}
#   Cells' state map
grid_cells_state = {}
#   Graphical cells text:
grid_cell_text = {}
last_cell = (-1, -1)
# endregion

# region Utilities


def hex_to_RGB(color):
    return tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))


def alphablend(ca, cb, oa, ob):
    return (int((ca[0]*oa + cb[0]*ob*(1-oa)) / (oa + ob*(1-oa))),
            int((ca[1]*oa + cb[1]*ob*(1-oa)) / (oa + ob*(1-oa))),
            int((ca[2]*oa + cb[2]*ob*(1-oa)) / (oa + ob*(1-oa))))


def RGB_to_hex(rgb):
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
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

    main_canvas.coords(hover_box, -grid_cell_size, -grid_cell_size, 0, 0)
    main_canvas.tag_raise(hover_box)


def create_grid(height, width):
    global grid_cells
    global grid_width_cells
    global grid_height_cells
    global hover_box
    global Sx
    global Sy
    global Gx
    global Gy

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
                # outline="#85a9e5")
                outline="#5272a8")
            #grid_cells_state[(x,y)] = "STATE_NORMAL"

    for x in range(grid_width_cells):
        for y in range(grid_height_cells):
            set_cell_state(x, y, "STATE_NORMAL", None)

    Sx = 0
    Sy = 0
    grid_cells_state[(0, 0)] = "START"
    Gx = grid_width_cells - 1
    Gy = grid_height_cells - 1
    grid_cells_state[(grid_width_cells-1, grid_height_cells-1)] = "GOAL"
    reconfigure_sizes(None)


def set_cell_state(x, y, state, temporarily):

    if ((x, y) == (Sx, Sy) and state != "START") or ((x, y) == (Gx, Gy) and state != "GOAL"):
        return
    if x == -1 or y == -1:
        return

    if state == "START":
        replace_once_state("START", "STATE_NORMAL")

    if state == "GOAL":
        replace_once_state("GOAL", "STATE_NORMAL")

    if not temporarily:
        grid_cells_state[(y, x)] = state
    main_canvas.itemconfig(
        grid_cells[(y, x)], fill=grid_cell_states_color[state])
    main_canvas.update_idletasks()
    # time.sleep(100)


def replace_once_state(old_state, new_state):
    for x in range(grid_width_cells):
        for y in range(grid_height_cells):
            if grid_cells_state[(x, y)] == old_state:
                grid_cells_state[(x, y)] = new_state
                return


def set_cell_text(x, y, cell_text):
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
    create_grid(n, n)

    Sx, Sy = [int(x) for x in next(f).split()]
    Gx, Gy = [int(x) for x in next(f).split()]
    arr = [[int(x) for x in line.split()] for line in f]

    run_button.configure(state="normal")

    for x in range(n):
        for y in range(n):
            if arr[x][y] == 1:
                set_cell_state(x, y, "OBSTACLE", None)

    set_cell_state(Sx, Sy, "START", None)
    set_cell_state(Gx, Gy, "GOAL", None)

    hide_hover_box()


def run_click():
    (ff, path) = aStar(Sx, Sy, Gx, Gy)
    if ff == -1:
        messagebox.showinfo("", "Can't find a path!")
        return
    for i in range(len(path) - 2, 0, -1):
        (x, y) = path[i]
        set_cell_state(x, y, "STATE_FINAL", None)


def reset_states_click():
    run_button.configure(state=DISABLED)
    initialize_astar()
    create_grid(0, 0)


def create_grid_click():
    size = 0
    v = create_grid_size_textbox.get()
    try:
        size = int(v)
    except:
        messagebox.showinfo("", "Can't interpret grid size!")
        return

    global n
    global adj
    n = size
    adj = [x[:] for x in [[0] * n] * n]  
    create_grid(size, size)

def run_gui_click():
    global Sx
    global Sy
    global Gx
    global Gy
    global arr

    cnt = 0
    for i in range(n):
        for j in range(n):
            if (adj[i][j] == MODE_START):
                cnt += 1
                (Sx, Sy) = (i, j)
    if (cnt != 1):
        messagebox.showinfo("", "Exactly one start node")
        return

    cnt = 0
    for i in range(n):
        for j in range(n):
            if (adj[i][j] == MODE_GOAL):
                cnt += 1
                (Gx, Gy) = (i, j)
    if (cnt != 1):
        messagebox.showinfo("", "Exactly one goal node")
        return

    arr = [x[:] for x in [[0] * n] * n] 
    for i in range(n):
        for j in range(n):
            if (adj[i][j] == MODE_OBSTACLE):
                arr[i][j] = 1
            
    run_click()
    

def window_postinit():
    loadinput_button.configure(command=loadinput_click)
    run_button.configure(command=run_click)
    reset_button.configure(command=reset_states_click)
    create_grid_button.configure(command=create_grid_click)
    run_gui_button.configure(command=run_gui_click)


def find_xy_from_id(id):
    for x in range(grid_width_cells):
        for y in range(grid_height_cells):
            if grid_cells[(x, y)] == id:
                return (x, y)
            else:
                return (-1, -1)


def hide_hover_box():
    main_canvas.coords(hover_box,
                       0, 0,
                       0, 0)


def mousemove_handler(event, mousebutton):
    #print(event.x, ' - ', event.y)
    global last_cell
    x = (int)((event.x - x_left_corner) / (grid_cell_size))
    y = (int)((event.y - y_top_corner) / (grid_cell_size))

    # if last_cell != (-1, -1) and last_cell != (x, y):
    #main_canvas.itemconfig(last_cell, fill='')
    # set_cell_state(last_cell[1], last_cell[0],
    # grid_cells_state[last_cell], True)

    last_cell = (-1, -1)

    if x < 0 or x >= grid_width_cells:
        hide_hover_box()
        return

    if y < 0 or y >= grid_height_cells:
        hide_hover_box()
        return

    hover_box_x = x_left_corner+x*grid_cell_size
    hover_box_y = y_top_corner+y*grid_cell_size
    main_canvas.coords(hover_box,
                       hover_box_x, hover_box_y,
                       hover_box_x + grid_cell_size, hover_box_y+grid_cell_size)

    current_color = hex_to_RGB(
        grid_cell_states_color[grid_cells_state[(y, x)]])
    toblend_color = hex_to_RGB(grid_cell_states_color["STATE_HOVER"])
    blended_color = RGB_to_hex(alphablend(
        current_color, toblend_color, 0.5, 0.5))

    main_canvas.itemconfig(hover_box, fill=blended_color)

    (x, y) = (y, x)
    if mousebutton == LEFT:
        set_cell_state(x, y, mode_state[edit_mode_var.get()], None)
        adj[x][y] = edit_mode_var.get()

    # print(blended_color)
    # main_canvas.itemconfig(hover_box, fill = blended_color)

    # # Uncomment for small magic

    # for state, color in grid_cell_states_color.items():
    #    if color == grid_cell_states_color[grid_cells_state[(x, y)]]:
    #        create_grid_label.config(text = state)


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
        set_cell_state(x, y, "STATE_POP", None)
        # printHeap(heap)

        if (x, y) == (Gx, Gy):
            path = []
            while (x, y) != (Sx, Sy):
                path.append((x, y))
                (x, y) = tr[x][y]
            path.append((Sx, Sy))
            path.reverse()
            return (ff + 1, path)

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
                    set_cell_state(u, v, "STATE_PUSH", None)
                    # printHeap(heap)

    return (-1, [])
# endregion

# region Entry point


initialize_astar()
#create_grid(5, 10)
window.after(0, window_postinit)
window.bind("<Configure>", reconfigure_sizes)
main_canvas.bind("<Motion>", lambda event: mousemove_handler(event, None))
main_canvas.bind("<B1-Motion>", lambda event: mousemove_handler(event, LEFT))
main_canvas.bind("<B3-Motion>", lambda event: mousemove_handler(event, RIGHT))

window.mainloop()
# endregion
