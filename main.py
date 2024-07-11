from tkinter import *
from tkinter import colorchooser, simpledialog
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = '#00FF00'
FOOD_COLOR = '#FF0000'
BACKGROUND_COLOR = '#000000'
OBSTACLE_COLOR = '#808080'

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake_color, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=food_color, tag="food")

class Obstacle:
    def __init__(self):
        self.coordinates = []
        for _ in range(5):  # Add 5 obstacles
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            self.coordinates.append([x, y])
            canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBSTACLE_COLOR, tag="obstacle")

def next_turn(snake, food):
    if paused:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake_color)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    for obstacle in obstacles.coordinates:
        if x == obstacle[0] and y == obstacle[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 - 30, font=('consolas', 70), text=f"GAME OVER {nickname}", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 30, font=('consolas', 70), text=f"YOUR SCORE IS {score}", fill="red", tag="gameover")

def choose_snake_color():
    global snake_color
    color_code = colorchooser.askcolor(title="Choose Snake Color")
    if color_code[1] is not None:
        snake_color = color_code[1]

def choose_food_color():
    global food_color
    color_code = colorchooser.askcolor(title="Choose Food Color")
    if color_code[1] is not None:
        food_color = color_code[1]

def ask_nickname():
    global nickname
    nickname = simpledialog.askstring("Nickname", "Please enter your nickname:")
    if not nickname:
        nickname = "Player"

def start_game():
    global snake, food, obstacles, paused, direction, score
    ask_nickname()
    setup_frame.pack_forget()
    score = 0
    direction = 'down'
    paused = False
    snake = Snake()
    food = Food()
    obstacles = Obstacle()
    next_turn(snake, food)

def toggle_pause(event=None):
    global paused
    paused = not paused

def set_difficulty(difficulty):
    global SPEED
    if difficulty == "Easy":
        SPEED = 150
    elif difficulty == "Medium":
        SPEED = 100
    elif difficulty == "Hard":
        SPEED = 50

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'
snake_color = SNAKE_COLOR
food_color = FOOD_COLOR
paused = False
nickname = "Player"

setup_frame = Frame(window)
setup_frame.pack()

snake_color_button = Button(setup_frame, text="Choose Snake Color", command=choose_snake_color)
snake_color_button.grid(row=0, column=0, padx=10, pady=10)

food_color_button = Button(setup_frame, text="Choose Food Color", command=choose_food_color)
food_color_button.grid(row=0, column=1, padx=10, pady=10)

Label(setup_frame, text="Select Difficulty:").grid(row=1, column=0, padx=10, pady=10)
difficulty_var = StringVar(value="Medium")
easy_rb = Radiobutton(setup_frame, text="Easy", variable=difficulty_var, value="Easy", command=lambda: set_difficulty("Easy"))
easy_rb.grid(row=1, column=1, padx=10, pady=10)
medium_rb = Radiobutton(setup_frame, text="Medium", variable=difficulty_var, value="Medium", command=lambda: set_difficulty("Medium"))
medium_rb.grid(row=1, column=2, padx=10, pady=10)
hard_rb = Radiobutton(setup_frame, text="Hard", variable=difficulty_var, value="Hard", command=lambda: set_difficulty("Hard"))
hard_rb.grid(row=1, column=3, padx=10, pady=10)

start_button = Button(setup_frame, text="Start Game", command=start_game)
start_button.grid(row=2, column=0, columnspan=4, pady=10)

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<space>', toggle_pause)

window.mainloop()
