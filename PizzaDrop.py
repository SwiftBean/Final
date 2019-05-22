# Pizza Drop
# Zach Page
# 4/19


# imports
from superwires import games, color
import random

# global variables


games.init(screen_width=640, screen_height=480, fps=60)


# Classes

class Chef(games.Sprite):
    image = games.load_image("images/giphy.gif")

    def __init__(self, y = 60, speed = 5, odds_change = 100):
        super(Chef, self).__init__(image=Chef.image,
                                   x = games.screen.width / 2,
                                   y = y,
                                   dx = speed)
        self.odds_change = odds_change
        self.time_til_drop = 0

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
            new_pizza = Pizza(x = self.x)
            games.screen.add(new_pizza)

            self.time_til_drop = random.randint(60, 250)



class Pan(games.Sprite):
    image = games.load_image("images2.5/ship3.png")

    def __init__(self):
        super(Pan, self).__init__(image=Pan.image,
                                  x = games.mouse.x,
                                  bottom = games.screen.height)

    def update(self):
        self.x = games.mouse.x

        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width

        self.check_catch()

    def check_catch(self):
        for pizza in self.overlapping_sprites:
            #add_to_score()
            pizza.handle_caught()


class Pizza(games.Sprite):
    image = games.load_image("images2.5/asteroid3.png")
    speed = 10

    def __init__(self, x, y=90, speed=random.randrange(speed) + 1):
        super(Pizza, self).__init__(image=Pizza.image, x=x, y=y, dy=speed)

    def update(self):
        if self.bottom > games.screen.height:
            self.destroy()
            self.end_game()

    def end_game(self):
        """This will end the game."""
        end_message = games.Message(value = "You Died",
                                    size = 95,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 9 * games.screen.fps,
                                    after_death = games.screen.quit)
        games.screen.add(end_message)

    def handle_caught(self):
        self.destroy()


class ScText(games.Text):
    pass


# main
def main():
    # load Data
    wall_image = games.load_image("images2.5/Space.jpg", transparent=False)
    # create objects
    the_pan = Pan()
    the_chef = Chef()
    # draw
    games.screen.background = wall_image
    games.screen.add(the_pan)
    games.screen.add(the_chef)

    # game setup
    games.mouse.is_visible = False
    games.screen.event_grab = True

    # start loop
    games.screen.mainloop()


# starting point
main()
