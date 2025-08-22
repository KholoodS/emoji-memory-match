import tkinter as tk
import random

# Emoji list
EMOJIS = ['🍎', '🍌', '🍇', '🍉', '🍒', '🍍', '🥝', '🍑']
EMOJIS *= 2  # Duplicate for pairs
random.shuffle(EMOJIS)

# Game settings
GRID_SIZE = 4
HIDDEN = '❓'

# Game state
first_click = None
buttons = []
revealed = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]

# Create main window
root = tk.Tk()
root.title("Emoji Memory Match")

def check_win():
    return all(all(row) for row in revealed)

def reset_game():
    global EMOJIS, revealed, first_click
    EMOJIS = EMOJIS[:]
    random.shuffle(EMOJIS)
    revealed = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]
    first_click = None
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            buttons[i][j].config(text=HIDDEN, state=tk.NORMAL)

def on_click(i, j):
    global first_click

    if revealed[i][j] or buttons[i][j]['text'] != HIDDEN:
        return

    idx = i * GRID_SIZE + j
    buttons[i][j].config(text=EMOJIS[idx])

    if not first_click:
        first_click = (i, j)
    else:
        x1, y1 = first_click
        x2, y2 = i, j
        if EMOJIS[x1 * GRID_SIZE + y1] == EMOJIS[x2 * GRID_SIZE + y2]:
            revealed[x1][y1] = True
            revealed[x2][y2] = True
            buttons[x1][y1].config(state=tk.DISABLED)
            buttons[x2][y2].config(state=tk.DISABLED)
        else:
            root.after(1000, lambda: hide_emojis(x1, y1, x2, y2))
        first_click = None

    if check_win():
        win_label = tk.Label(root, text="🎉 You won!", font=("Arial", 16))
        win_label.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE)

def hide_emojis(x1, y1, x2, y2):
    buttons[x1][y1].config(text=HIDDEN)
    buttons[x2][y2].config(text=HIDDEN)

# Create grid of buttons
for i in range(GRID_SIZE):
    row = []
    for j in range(GRID_SIZE):
        btn = tk.Button(root, text=HIDDEN, width=6, height=3,
                        font=("Arial", 20), command=lambda i=i, j=j: on_click(i, j))
        btn.grid(row=i, column=j)
        row.append(btn)
    buttons.append(row)

# Reset button
reset_btn = tk.Button(root, text="🔄 Reset", command=reset_game)
reset_btn.grid(row=GRID_SIZE+1, column=0, columnspan=GRID_SIZE)

root.mainloop()
