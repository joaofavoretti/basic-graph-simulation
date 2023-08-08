import tkinter as tk
import networkx as nx
import pickle
import matplotlib.pyplot as plt

# Define the size of the grid
GRID_SIZE = 10

# Define the size of each cell
CELL_SIZE = 50

# Border selector thickness
BORDER_THICKNESS = 2

SELECTED_BORDER_FILL = '#a0a0a0'
SELECTED_BORDER_HOVER = '#909090'

UNSELECTED_BORDER_FILL = ''
UNSELECTED_BORDER_HOVER = '#c0c0c0'

def on_save():
    global coords, GRID_SIZE

    G = nx.Graph()

    # Adding the nodes
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            
            node_id = i * GRID_SIZE + j
            G.add_node(node_id, pos=(i, j), signal=0.0, is_source=False)

    # Adding the edges
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):

            node_id = i * GRID_SIZE + j

            # Iterate 4-neighbor
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if abs(k) + abs(l) != 1:
                        continue

                    if i + k < 0 or i + k >= GRID_SIZE or j + l < 0 or j + l >= GRID_SIZE:
                        continue

                    neighbor_id = (i + k) * GRID_SIZE + (j + l)

                    border_set = coords[i][j].intersection(coords[i + k][j + l])

                    if border_set:
                        border = border_set.pop()

                        if canvas.itemcget(border, 'fill') == UNSELECTED_BORDER_FILL:
                            G.add_edge(node_id, neighbor_id)

    with open('graph.pkl', 'wb') as f:
        pickle.dump(G, f)

# Create the main window
root = tk.Tk()

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a "File" menu with a "New" option
file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="Save", command=on_save)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create a canvas to draw on
canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
canvas.pack()

# Create a 2D list to store the rectangles
coords = [[set() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Iterate through all the grid cells
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):

        x = i * CELL_SIZE
        y = j * CELL_SIZE

        # Iterate through the neighbors
        for k in range(-1, 2):
            for l in range(-1, 2):
                if abs(k) + abs(l) != 1:
                    continue

                if i + k < 0 or i + k >= GRID_SIZE or j + l < 0 or j + l >= GRID_SIZE:
                    continue

                # If intersection of coords[i][j] and coords[i + k][j + l] is empty
                if coords[i][j].intersection(coords[i + k][j + l]):
                    continue
                
                # See the border 
                x1 = x + CELL_SIZE * (k == 1) - BORDER_THICKNESS * (l == 0)
                y1 = y + CELL_SIZE * (l == 1) - BORDER_THICKNESS * (k == 0)
                x2 = x + CELL_SIZE * (k != -1) + BORDER_THICKNESS * (l != 1)
                y2 = y + CELL_SIZE * (l != -1) + BORDER_THICKNESS * (l == 1)

                # Add the rectangle to the canvas
                rect = canvas.create_rectangle(x1, y1, x2, y2, fill=UNSELECTED_BORDER_FILL, outline='')
                coords[i][j].add(rect)
                coords[i + k][j + l].add(rect)
    

# Define a function to change the color of the clicked cell
def change_color(event):
    global canvas, coords

    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    
    dx = event.x / CELL_SIZE - x - 0.5
    dy = event.y / CELL_SIZE - y - 0.5

    _x = x + 1 * (dx > abs(dy)) - 1 * (dx < -abs(dy))
    _y = y + 1 * (dy > abs(dx)) - 1 * (dy < -abs(dx))

    # If the cell is out of bounds, return
    if (_x < 0 or _x >= GRID_SIZE or _y < 0 or _y >= GRID_SIZE):
        return

    border_set = coords[x][y].intersection(coords[_x][_y])

    if border_set:
        border = border_set.pop()

        canvas.lift(border)
        
        if canvas.itemcget(border, 'fill') == SELECTED_BORDER_FILL or canvas.itemcget(border, 'fill') == SELECTED_BORDER_HOVER:
            canvas.itemconfig(border, fill=UNSELECTED_BORDER_FILL)
        else:
            canvas.itemconfig(border, fill=SELECTED_BORDER_FILL)


def on_motion(event):
    global canvas, coords

    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    
    if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
        return

    for border in coords[x][y]:
        canvas.lift(border)
        if canvas.itemcget(border, 'fill') == SELECTED_BORDER_FILL or canvas.itemcget(border, 'fill') == SELECTED_BORDER_HOVER:
            canvas.itemconfig(border, fill=SELECTED_BORDER_FILL)
        else:
            canvas.itemconfig(border, fill=UNSELECTED_BORDER_FILL)

    dx = event.x / CELL_SIZE - x - 0.5
    dy = event.y / CELL_SIZE - y - 0.5

    _x = x + 1 * (dx > abs(dy)) - 1 * (dx < -abs(dy))
    _y = y + 1 * (dy > abs(dx)) - 1 * (dy < -abs(dx))

    # If the cell is out of bounds, return
    if _x < 0 or _x >= GRID_SIZE or _y < 0 or _y >= GRID_SIZE:
        return

    border_set = coords[x][y].intersection(coords[_x][_y])

    if border_set:
        border = border_set.pop()

        canvas.lift(border)
        
        if canvas.itemcget(border, 'fill') == SELECTED_BORDER_FILL or canvas.itemcget(border, 'fill') == SELECTED_BORDER_HOVER:
            canvas.itemconfig(border, fill=SELECTED_BORDER_HOVER)
        else:
            canvas.itemconfig(border, fill=UNSELECTED_BORDER_HOVER)

def on_leave(event):
    global canvas, coords

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            for border in coords[i][j]:
                canvas.lift(border)
                if canvas.itemcget(border, 'fill') == SELECTED_BORDER_FILL or canvas.itemcget(border, 'fill') == SELECTED_BORDER_HOVER:
                    canvas.itemconfig(border, fill=SELECTED_BORDER_FILL)
                else:
                    canvas.itemconfig(border, fill=UNSELECTED_BORDER_FILL)

# # Bind the Button-1 event to the change_color function
canvas.bind('<Button-1>', change_color)

canvas.bind('<Motion>', on_motion)
canvas.bind('<Leave>', on_leave)

# Start the main event loop
root.mainloop()