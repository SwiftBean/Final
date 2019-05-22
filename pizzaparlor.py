from superwires import games, color
import random

score = 0
games.init(screen_width = 640, screen_height = 480, fps = 50)

class Pan(games.Sprite):
    def update(self):
        self.x = games.mouse.x
        self.y = games.mouse.y
        self.check_collide()

    def check_collide(self):
        for pizza in self.overlapping_sprites:
            pizza.handle_collide()


class Pizza(games.Sprite):

    def handle_collide(self):
        self.x = random.randrange(games.screen.width)
        self.y = random.randrange(games.screen.width)


    def update(self):
        global score
        #Reverse a velocity component if edge of screen reached.
        if self.right > games.screen.width or self.left < 0:
            self.dx = -self.dx
        if self.bottom > games.screen.height or self.top < 0:
            self.dy = -self.dy
            score +=1

        #teleport mec
        #if self.left > games.screen.width:
            #self.right = 0
            #score +=1
        #if self.right < 0:
            #self.left = games.screen.width
            #score += 1
        #if self.bottom > games.screen.height:
            #self.top = 0
            #score += 1
        #if self.top < 0:
            #self.bottom = games.screen.height
            #score += 1

class ScText(games.Text):
    def update(self):
        self.value = score



def main():
    #loaded img
    global score
    bg_img = games.load_image("images/pizzareia.jpg")
    pizza_img = games.load_image("images/pizza.png")
    pan_img = games.load_image("images/pan.png")

    #added img to bg
    games.screen.background = bg_img

    #create pizza obj
    pizza = Pizza(image = pizza_img,
                  x=games.screen.width/2,
                  y=games.screen.width/2,
                  dx = random.randint(-10, 10),
                  dy = random.randint(-10, 10)
                   )
    pizza1 = Pizza(image=pizza_img,
                  x=games.screen.width / 2,
                  y = games.screen.width / 2,
                  dx = random.randint(-10, 10),
                  dy = random.randint(-10, 10)
                   )
    pizza2 = Pizza(image = pizza_img,
                  x=games.screen.width/2,
                  y=games.screen.width/2,
                  dx = random.randint(-10, 10),
                  dy = random.randint(-10, 10)
                   )
    pizza3 = Pizza(image = pizza_img,
                  x=games.screen.width/2,
                  y=games.screen.width/2,
                  dx = random.randint(-10, 10),
                  dy = random.randint(-10, 10)
                   )
    pizza4 = Pizza(image=pizza_img,
                  x=games.screen.width/2,
                  y=games.screen.width/2,
                  dx = random.randint(-10, 10),
                  dy = random.randint(-10, 10)
                   )
    pizza5 = Pizza(image=pizza_img,
                  x=games.screen.width/2,
                  y=games.screen.width/2,
                  dx = random.randint(-10, 10),
                  dy = random.randint(-10, 10)
                   )

    #create pan obj
    the_pan = Pan(image=pan_img,
                  x=games.mouse.x,
                  y=450)

    #create txt obj
    score_text = ScText(value = score,
                   is_collideable= False,
                   size = 60,
                   color = color.black,
                   x= 550,
                   y = 30)

    #draw objs to screen
    games.screen.add(pizza)
    games.screen.add(pizza1)
    games.screen.add(pizza2)
    games.screen.add(pizza3)
    games.screen.add(pizza4)
    games.screen.add(pizza5)
    games.screen.add(the_pan)
    games.screen.add(score_text)

    games.mouse.is_visible = False
    games.screen.event_grab = True

    #start mainloop
    games.screen.mainloop()

main()