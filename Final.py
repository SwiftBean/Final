# Pizza Drop
# Zach Page
# 4/19


# imports
from superwires import games, color
import random
import math

# global variables


games.init(screen_width=640, screen_height=480, fps=60)

# Classes
class Game(object):
    def __init__(self):
        self.level = 0
        # load sound for level advance
        self.sound = games.load_sound("sounds/level.wav")
        # create score
        self.score = games.Text(value=0,
                                size=30,
                                color=color.white,
                                top=5,
                                right=games.screen.width - 10,
                                is_collideable=False)
        games.screen.add(self.score)

        self.ship = Ship(self)
        games.screen.add(self.ship)



        message1 = games.Message(value="Use your mouse to move left and right",
                                 size=35,
                                 color=color.white,
                                 x=games.screen.width / 2,
                                 y=games.screen.height / 2,
                                 lifetime=3 * games.screen.fps,
                                 is_collideable=False)

        message2 = games.Message(value="Press the space bar to fire your laser",
                                 size=34,
                                 color=color.white,
                                 x=games.screen.width / 2,
                                 y=games.screen.height / 4,
                                 lifetime=3 * games.screen.fps,
                                 is_collideable=False)

        games.screen.add(message1)
        games.screen.add(message2)
        self.advance()


    def advance(self):
        self.level += 1

        level_message = games.Message(value = "Level" + str(self.level),
                                      size = 40,
                                      color = color.yellow,
                                      x = games.screen.width/2,
                                      y = games.screen.height/10,
                                      lifetime = 3 * games.screen.fps,
                                      is_collideable = False)
        games.screen.add(level_message)

        if self.level > 1:
            self.sound.play()

        for i in range(self.level):
            self.ufo = UFO(self)
            games.screen.add(self.ufo)

    def play(self):
        games.music.load("sounds/main_song.wav")
        games.music.play(-1)

        bg_img = games.load_image("images2.5/Space.jpg", transparent=False)
        games.screen.background = bg_img

        games.screen.mainloop()

    def new_ship(self):
        self.ship = Ship(game = self,
                         x = games.mouse.x)
        games.screen.add(self.ship)


class Wrapper(games.Sprite):
    def update(self):
        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

    def die(self):
        self.destroy()

class Collider(Wrapper):
    def update(self):
        """Check for overlapping sprites."""
        super(Collider, self).update()

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        #create explosion
        new_explosion = Explosion(obj_x = self.x, obj_y = self.y)
        #add to screen
        games.screen.add(new_explosion)
        self.destroy()

class UFO(games.Sprite):
    image = games.load_image("images2.5/ufo.png")
    points = 50

    def __init__(self, game, y = 60, speed = 5, odds_change = 100):
        global xscore
        super(UFO, self).__init__(image=UFO.image,
                                   x = games.screen.width / 2,
                                   y = y,
                                   dx = speed)
        self.odds_change = odds_change
        self.time_til_drop = 0
        self.game = game

    def update(self):
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx

        self.check_drop()

    def check_drop(self):
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_asteroid = Asteroid(self.game, x = self.x)
            games.screen.add(new_asteroid)

            self.time_til_drop = random.randint(60, 250)

    def die(self):
        self.game.score.value += int(UFO.points)
        self.game.advance()

        self.destroy()

class Ship(games.Sprite):
    image = games.load_image("images2.5/ship3.png")
    sound = games.load_sound("sounds/thruster.wav")

    missile_delay = 25
    lives = 3

    def __init__(self, game):
        super(Ship, self).__init__(image=Ship.image,
                                  x = games.mouse.x,
                                  bottom = games.screen.height)
        self.missile_wait = 0
        self.lives = games.Text(value="Lives: " + str(Ship.lives), size=25, color=color.white, top=25,
                                right=games.screen.width - 10, is_collideable=False)
        games.screen.add(self.lives)
        self.game = game


    def update(self):
        self.x = games.mouse.x

        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width

        if self.missile_wait > 0:
            self.missile_wait -= 1

        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.missile_delay
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()
            self.end_game()

    def die(self):
        new_explosion = Explosion(obj_x=self.x, obj_y=self.y)
        # add to screen
        games.screen.add(new_explosion)
        self.destroy()


    def lose_life(self):
        Ship.lives -= 1
        self.lives.destroy()
        if Ship.lives <= 0:
            self.game.end()
        else:
            self.game.new_ship()

    def end_game(self):
        """This will end the game."""
        end_message = games.Message(value="You Died",
                                    size=95,
                                    color=color.red,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 2,
                                    is_collideable=False)

        games.screen.add(end_message)

        esc_message = games.Message(value="Press Esc to Exit",
                                    size=45,
                                    color=color.red,
                                    x=games.screen.width / 2,
                                    y=games.screen.height / 1.5,
                                    is_collideable=False)
        games.screen.add(esc_message)



class Asteroid(Collider):
    image = games.load_image("images2.5/asteroid3.png")
    speed = 10
    points = 20
    total = 0

    def __init__(self, game, x, y=90, speed=random.randrange(speed) + 1):
        super(Asteroid, self).__init__(image=Asteroid.image, x=x, y=y, dy=speed)
        self.game = game

    def update(self):
        if self.bottom > games.screen.height:
            self.destroy()
            self.end_game()


    def die(self):
        self.game.score.value += int(Asteroid.points)
        # create explosion
        self.destroy()

    def end_game(self):
        """This will end the game."""
        end_message = games.Message(value = "You Died",
                                    size = 95,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    is_collideable = False)

        games.screen.add(end_message)

        esc_message = games.Message(value = "Press Esc to Exit",
                                    size = 45,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/1.5,
                                    is_collideable = False)
        games.screen.add(esc_message)



class Missile(Collider):
    image = games.load_image("images2.5/laser.png")
    sound = games.load_sound("sounds/laser.wav")
    buffer = 45
    velocity_factor = 7
    lifetime = 60
    def __init__(self, ship_x, ship_y, ship_angle):
        Missile.sound.play()
        angle = ship_angle * math.pi/180

        #calculate missile's starting position
        buffer_x = Missile.buffer * math.sin(angle)
        buffer_y = Missile.buffer * -math.cos(angle)

        x = ship_x + buffer_x
        y = ship_y + buffer_y

        dx = Missile.velocity_factor * math.sin(angle)
        dy = Missile.velocity_factor * -math.cos(angle)
        super(Missile, self).__init__(image = Missile.image,
                                      x = x,
                                      y = y,
                                      dx = dx,
                                      dy = dy)
        self.lifetime  = Missile.lifetime
        self.angle = ship_angle

    def update(self):
        super(Missile, self).update()
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()

class Explosion(games.Animation):
    sound = games.load_sound("sounds/explosion.wav")
    exp_images = ["images2.5/explosion1.bmp",
                       "images2.5/explosion2.bmp",
                       "images2.5/explosion3.bmp",
                       "images2.5/explosion4.bmp",
                       "images2.5/explosion5.bmp",
                       "images2.5/explosion6.bmp",
                       "images2.5/explosion7.bmp",
                       "images2.5/explosion8.bmp",
                "images2.5/explosion9.bmp"]
    def __init__(self, obj_x, obj_y):
        super(Explosion, self).__init__(images = Explosion.exp_images,
                                        x = obj_x, y = obj_y,
                                        repeat_interval = 4,
                                        n_repeats = 1,
                                        is_collideable = False)
        Explosion.sound.play()

# main
def main():
    # load Data

    # create objects
    final = Game()
    final.play()
    # game setup
    games.mouse.is_visible = False
    games.screen.event_grab = True

    # start loop


# starting point
main()
