# SGE Game Demo by @TokyoEdTech AKA /u/wynand1004
# Requires SGE Version 0.4
# Navigate using the arrow keys
# Green objects are worth 10 points
# Yellow objects are worth 0 points
# Red objects are worth -10 points
from SGE import *

# Create Classes
class Player(SGE.Sprite):
    def __init__(self, shape, color, x, y):
        SGE.Sprite.__init__(self, shape, color, x, y)
        self.speed = 3
        self.score = 0

    def tick(self):
        self.move()

    def move(self):
        self.fd(self.speed)

        if self.xcor() > game.SCREEN_WIDTH / 2:
            self.goto(-game.SCREEN_WIDTH / 2, self.ycor())

        if self.xcor() < -game.SCREEN_WIDTH /2 :
            self.goto(game.SCREEN_WIDTH / 2, self.ycor())

        if self.ycor() > game.SCREEN_HEIGHT / 2:
            self.goto(self.xcor(), -game.SCREEN_HEIGHT / 2)

        if self.ycor() < -game.SCREEN_HEIGHT / 2:
            self.goto(self.xcor(), game.SCREEN_HEIGHT / 2)

    def rotate_left(self):
        self.lt(30)

    def rotate_right(self):
        self.rt(30)

    def accelerate(self):
        self.speed += 0.5

class Orb(SGE.Sprite):
    def __init__(self, shape, color, x, y):
        SGE.Sprite.__init__(self, shape, color, x, y)
        self.speed = 2
        self.setheading(random.randint(0,360))
        self.turn = 0

    def tick(self):
        self.move()
        if random.randint(0, 100) < 5:
            self.clear()

    def move(self):
        self.rt(random.randint(-10, 10))
        self.fd(self.speed)

        if self.xcor() > game.SCREEN_WIDTH / 2:
            self.goto(-game.SCREEN_WIDTH / 2, self.ycor())

        if self.xcor() < -game.SCREEN_WIDTH / 2:
            self.goto(game.SCREEN_WIDTH / 2, self.ycor())

        if self.ycor() > game.SCREEN_HEIGHT / 2:
            self.goto(self.xcor(), -game.SCREEN_HEIGHT / 2)

        if self.ycor() < -game.SCREEN_HEIGHT / 2:
            self.goto(self.xcor(), game.SCREEN_HEIGHT / 2)

# Initial Game setup
game = SGE(800, 600, "blue", "SGE Game Demo 2 by @TokyoEdTech AKA /u/wynand1004")
game.clear_terminal_screen()

# Create Sprites
# Create Player
player = Player("triangle", "white", -400, 0)

# Create Orbs
for i in range(100):
    color = random.choice(["red", "yellow", "green"])
    shape = random.choice(["circle", "square", "triangle", "arrow"])
    orb = Orb(shape, color, 0, 0)
    speed = random.randint(1, 5)
    orb.speed = speed

# Create Labels
score_label = SGE.Label("Score: 0", "white", -380, 280)

# Set Keyboard Bindings
game.set_keyboard_binding(SGE.KEY_UP, player.accelerate)
game.set_keyboard_binding(SGE.KEY_LEFT, player.rotate_left)
game.set_keyboard_binding(SGE.KEY_RIGHT, player.rotate_right)

while True:
    # Call the game tick method
    game.tick()

    # Put your game logic here
    for sprite in SGE.sprites:
        # Check collisions with Orbs
        if sprite.state and isinstance(sprite, Orb):
            if game.is_collision(sprite, player):
                game.play_sound("collision.wav")
                sprite.destroy()
                # Update Score
                if sprite.pencolor() == "red":
                    player.score -= 10
                if sprite.pencolor() == "green":
                    player.score += 10
                # Update Score
                score_label.update("Score: {}".format(player.score))
