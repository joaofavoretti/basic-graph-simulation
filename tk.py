import tkinter as tk

# Define the size of the grid
GRID_SIZE = 10

# Define the size of each cell
CELL_SIZE = 50

# Create the main window
root = tk.Tk()

# Create a canvas to draw on
canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
canvas.pack()

# Create a 2D list to store the rectangles
rectangles = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
borders = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Create the rectangles and store them in the list
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        x1 = i * CELL_SIZE
        y1 = j * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        
        rect = canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='')
        rectangles[i][j] = rect
        
        border_top = canvas.create_line(x1, y1, x2, y1, fill='')
        border_right = canvas.create_line(x2, y1, x2, y2, fill='')
        border_bottom = canvas.create_line(x2, y2, x1, y2, fill='')
        border_left = canvas.create_line(x1, y2, x1, y1, fill='')
        borders[i][j] = [border_top, border_right, border_bottom, border_left]


# Define a function to change the color of the clicked cell
def change_color(event):
    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    
    for index, border in enumerate(borders[x][y]):
        canvas.lift(border)

        # Deciding which border will the the next
        if canvas.itemcget(border, 'fill') == 'black':
            canvas.itemconfig(border, fill='')
            canvas.itemconfig(borders[x][y][(index + 1) % 4], fill='black')
            break
        
        # None of the borders are black
        if index == 3:
            canvas.itemconfig(border, fill='black')
            canvas.itemconfig(borders[x][y][0], fill='')

def on_motion(event):
    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE


    for i in range(-1, 2):
        for j in range(-1, 2):
            _x = x + i
            _y = y + j

            if (_x < 0 or _x >= GRID_SIZE or _y < 0 or _y >= GRID_SIZE):
                continue

            canvas.itemconfig(rectangles[_x][_y], fill='white')
    
    if (x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE):
        return

    canvas.itemconfig(rectangles[x][y], fill='#f3f3f3')

def on_leave(event):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            canvas.itemconfig(rectangles[i][j], fill='white')

# Bind the Button-1 event to the change_color function
canvas.bind('<Button-1>', change_color)

canvas.bind('<Motion>', on_motion)
canvas.bind('<Leave>', on_leave)

# Start the main event loop
root.mainloop()