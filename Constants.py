import os

# Constants that represent "what pile is what" for the game
PLAYER_AREA = 0
COMPUTER_AREA = 1
MAIN_AREA = 2

# Amout of init Cards for every player_area
INIT_CARDS = 6

# How fast to move, and how fast to run the animation
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5

ANIMATION_STEPS = 30

# Difficulties
EASY = 0
MEDIUM = 1
HARD = 2

# Win/Lose png relative path
# get current working directory
cwd = os.getcwd()
# get the path to the images folder
images_path = os.path.join(cwd, "resources")
WIN = f"{images_path}/win.png"
LOSE = f"{images_path}/lose.png"
