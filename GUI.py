from tkinter import *
from array import *

# Window object
window = Tk()
window.geometry("700x500")
window.minsize(width=700, height=500)
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
#    Legends canvas

# Drawing objects:
#    Dimensions (ignore initial values)
grid_width_graphical = 0
grid_height_graphical = 0
grid_cell_size = 20
grid_width_cells = 0
grid_height_cells = 0
grid_padding = 50
#    Graphical cells array
grid_cells = {}


def reconfigure_sizes(event):
    global grid_width_graphical
    global grid_height_graphical
    global grid_cell_size

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


def create_grid(width, height):
    global grid_cells
    global grid_width_cells
    global grid_height_cells

    for x in range(grid_width_cells):
        for y in range(grid_height_cells):
            main_canvas.delete(grid_cells[(x,y)])
            del grid_cells[(x,y)] 

    grid_width_cells = width
    grid_height_cells = height

    for x in range(width):
        for y in range(height):
            grid_cells[(x, y)] = main_canvas.create_rectangle(
                grid_padding+x*grid_cell_size,
                grid_padding+y*grid_cell_size,
                grid_padding+(x+1)*grid_cell_size,
                grid_padding+(y+1)*grid_cell_size)

    reconfigure_sizes(None)


def shown():
    print("test")


def button_click():
    create_grid(4, 9)


btn = Button(right_frame, text="OK", command=button_click)
btn.place(x=0,y=0)
create_grid(10, 5)
window.after(0, shown)
window.bind("<Configure>", reconfigure_sizes)
window.mainloop()
