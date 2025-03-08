import turtle
import time
import random
import pygame

# Initialize pygame for sound and display handling
pygame.init()

# Set up sound effects and background music
pygame.mixer.music.load('background_music.mp3')  # Replace with your music file
pygame.mixer.music.set_volume(0.1)  # Set the background music volume
pygame.mixer.music.play(-1, 0.0)  # Loop the background music

eat_sound = pygame.mixer.Sound('eat_sound.wav')  # Replace with your sound file
game_over_sound = pygame.mixer.Sound('game_over.wav')  # Replace with your sound file

delay = 0.1
score = 0
high_score = 0
level = 1

# Setup window using turtle
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("blue")
wn.setup(width=600, height=600)
wn.tracer(0)

# Snake head setup
head = turtle.Turtle()
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# Food setup
food = turtle.Turtle()
colors = random.choice(['red', 'green', 'black'])
shapes = random.choice(['square', 'triangle', 'circle'])
food.speed(0)
food.shape(shapes)
food.color(colors)
food.penup()
food.goto(0, 100)

# Score display
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score : 0  High Score : 0", align="center", font=("candara", 24, "bold"))

# Menu setup
def show_menu():
    menu_screen = turtle.Screen()
    menu_screen.title("Snake Game Menu")
    menu_screen.bgcolor("gray")
    menu_screen.setup(width=600, height=600)
    pen.clear()
    pen.goto(0, 200)
    pen.write("SNAKE GAME", align="center", font=("candara", 30, "bold"))
    
    pen.goto(0, 100)
    pen.write("Press '1' for Level 1 (Easy)", align="center", font=("candara", 20, "bold"))
    
    pen.goto(0, 50)
    pen.write("Press '2' for Level 2 (Medium)", align="center", font=("candara", 20, "bold"))
    
    pen.goto(0, 0)
    pen.write("Press '3' for Level 3 (Hard)", align="center", font=("candara", 20, "bold"))
    
    pen.goto(0, -50)
    pen.write("Press 'Q' to Quit", align="center", font=("candara", 20, "bold"))

    menu_screen.listen()
    menu_screen.onkeypress(lambda: start_game(1), "1")
    menu_screen.onkeypress(lambda: start_game(2), "2")
    menu_screen.onkeypress(lambda: start_game(3), "3")
    menu_screen.onkeypress(quit_game, "q")
    menu_screen.mainloop()

# Start the game with a specific level
def start_game(level_choice):
    global level, delay, score, game_over
    level = level_choice
    delay = 0.1 * (4 - level)  # Higher level = Faster snake
    score = 0
    game_over = False
    pen.clear()
    pen.goto(0, 250)
    pen.write(f"Score : {score} High Score : {high_score} Level : {level}", align="center", font=("candara", 24, "bold"))
    game_loop()

# Assigning key directions using arrow keys
def group():
    if head.direction != "down":
        head.direction = "up"


def godown():
    if head.direction != "up":
        head.direction = "down"


def goleft():
    if head.direction != "right":
        head.direction = "left"


def goright():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)


# Main gameplay function
def game_loop():
    global score, high_score, delay, game_over
    segments = []

    # Set up controls
    wn.listen()
    wn.onkeypress(group, "Up")
    wn.onkeypress(godown, "Down")
    wn.onkeypress(goleft, "Left")
    wn.onkeypress(goright, "Right")

    while True:
        wn.update()

        if game_over:
            game_over_sound.play()
            show_game_over()
            break

        # Check for collision with walls (top, bottom, left, right)
        if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
            game_over = True

        # Check for food collision
        if head.distance(food) < 20:
            x = random.randint(-270, 270)
            y = random.randint(-270, 270)
            food.goto(x, y)
            eat_sound.play()  # Play sound when food is eaten

            # Add segment to snake
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("orange")  # Tail color
            new_segment.penup()
            segments.append(new_segment)
            score += 10

            # Update score
            if score > high_score:
                high_score = score

            pen.clear()
            pen.write(f"Score : {score} High Score : {high_score} Level : {level}", align="center", font=("candara", 24, "bold"))

        # Move the snake body
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        move()

        # Check for collision with self (body)
        for segment in segments:
            if segment.distance(head) < 20:
                game_over = True
                break

        time.sleep(delay)

# Game Over Screen
def show_game_over():
    pen.clear()
    pen.goto(0, 0)
    pen.write("Game Over\nPress 'R' to Restart", align="center", font=("candara", 24, "bold"))
    wn.onkeypress(restart_game, "r")

# Restart the game
def restart_game():
    global score, high_score, level, game_over
    score = 0
    level = 1
    delay = 0.1
    game_over = False
    head.goto(0, 0)
    head.direction = "Stop"
    show_menu()

# Quit the game
def quit_game():
    print("Exiting the game...")  # You can also use sys.exit() if needed
    turtle.bye()

# Start the game with the menu
show_menu()
