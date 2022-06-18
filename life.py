from itertools import count
import arcade
import random
import sys, os
from arcade.experimental import Shadertoy


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 8

SCREEN_TITLE = "Life Test"
OXYGEN = 10000
WATER = 10000
FOOD = 10000
WOOD = 1000

MAX_TREE = 1000
START_TREE = 40
MAX_PEOPLE = 1000
START_PEOPLE = 15
START_CRAB = 10
MAX_CRAB = 1000
CLOUD_MAX = 2

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TREE = ROOT_DIR + "/images/tree.png"




"""
Creates Point class, used to keep track of location
"""
class Point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
"""
Creates Velocity class, used to keep track of movement
"""        
class Velocity:
    def __init__(self):
        self.dx = 0.0
        self.dy = 0.0

class Oxygen():
    def __init__(self):
        self.count = OXYGEN
        self.center = Point()
    def draw(self):
        if self.count <= 0:
            self.count = 0
        arcade.draw_text(f"Oxygen: {self.count:.0f}", 50, SCREEN_HEIGHT - 40, arcade.color.WHITE, DEFAULT_FONT_SIZE * 2)
    def update(self, adjust):
        self.count += adjust

class Water():
    def __init__(self):
        self.count = WATER
        self.center = Point()
    def draw(self):
        if self.count <= 0:
            self.count = 0
        arcade.draw_text(f"Water: {self.count:.0f}", 50, SCREEN_HEIGHT - 80, arcade.color.WHITE, DEFAULT_FONT_SIZE * 2)
    def update(self, adjust):
        self.count += adjust

class Food():
    def __init__(self):
        self.count = FOOD
        self.center = Point()
    def draw(self):
        if self.count <= 0:
            self.count = 0
        arcade.draw_text(f"Food: {self.count:.0f}", 50, SCREEN_HEIGHT - 120, arcade.color.WHITE, DEFAULT_FONT_SIZE * 2)
    def update(self, adjust):
        self.count += adjust

class Wood():
    def __init__(self):
        self.count = WOOD
        self.center = Point()
    def draw(self):
        if self.count <= 0:
            self.count = 0
        arcade.draw_text(f"Wood: {self.count:.0f}", 50, SCREEN_HEIGHT - 160, arcade.color.WHITE, DEFAULT_FONT_SIZE * 2)
    def update(self, adjust):
        self.count += adjust

class effectObject():
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0
        self.count = 0
        self.maxpopulation = random.randint(30,50)
        self.oxygenGen = 0
        self.waterGen = 0
        self.lifespan = 0
        self.energy = 0
        self.label = ""
        #self.image = "images/tree.png"
        #self.texture = arcade.load_texture(TREE)
    def draw(self):
        pass
   
 


class Organism(effectObject):
    def __init__(self, xSpot, ySpot):
        super().__init__()
        self.center = Point()
        self.alive = True
        self.center.x = xSpot
        self.center.y = ySpot
        self.velocity = Velocity()
        self.velocity.dx = random.uniform(-1, 1)/2
        self.velocity.dy = random.uniform(-1, 1)/2
        self.count = 0
        self.oxygenGen = -1
        self.waterGen = -1
        self.label = "human"
        self.size = 2
        self.maxspeed = 1
        self.variation = random.randint(1, 5)
        self.image = "img/h" + str(self.variation) + ".png"
        self.texture = arcade.load_texture(self.image)
    def draw(self):
        #arcade.draw_circle_filled(self.center.x, self.center.y, self.size, arcade.color.BLACK, 2)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width * self.size, self.texture.height * self.size, self.texture, 0, 255)
        #arcade.draw_text(self.label, self.center.x, self.center.y, arcade.color.BLACK, DEFAULT_FONT_SIZE)
    def advance(self):
        self.center.y += self.velocity.dy
        self.center.x += self.velocity.dx

        self.velocity.dx += random.uniform(-1, 1)/8
        self.velocity.dy += random.uniform(-1, 1)/8
        if self.velocity.dx > self.maxspeed:
            self.velocity.dx = .3
        if self.velocity.dx < -self.maxspeed:
            self.velocity.dx = -.3
        if self.velocity.dy > self.maxspeed:
            self.velocity.dy = .3
        if self.velocity.dy < -self.maxspeed:
            self.velocity.dy = -.3

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        is_off_screen = False
        
        #Creates Screen Wrapping effect
        if self.center.x > SCREEN_WIDTH:
            self.center.x = SCREEN_WIDTH -2
            self.velocity.dx *= -1
        elif self.center.x < 0:
            self.center.x = 2
            self.velocity.dx *= -1
        elif self.center.y > SCREEN_HEIGHT:
            self.velocity.dy *= -1
        elif self.center.y < 0:
            self.velocity.dy *= -1
        return is_off_screen

class Crab(effectObject):
    def __init__(self, xSpot, ySpot):
        super().__init__()
        self.center = Point()
        self.alive = True
        self.center.x = xSpot
        self.center.y = ySpot
        self.velocity = Velocity()
        self.velocity.dx = random.uniform(-1, 1)/2
        self.velocity.dy = random.uniform(-1, 1)/2
        self.count = 0
        self.oxygenGen = -1
        self.waterGen = -1
        self.label = "crab"
        self.size = 1
        self.maxspeed = .5
        self.image = "img/crab.png"
        self.texture = arcade.load_texture(self.image)
    def draw(self):
        #arcade.draw_circle_filled(self.center.x, self.center.y, self.size, arcade.color.BLACK, 2)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width * self.size, self.texture.height * self.size, self.texture, 0, 255)
        #arcade.draw_text(self.label, self.center.x, self.center.y, arcade.color.BLACK, DEFAULT_FONT_SIZE)
    def advance(self):
        self.center.y += self.velocity.dy
        self.center.x += self.velocity.dx

        self.velocity.dx += random.uniform(-1, 1)/15
        self.velocity.dy += random.uniform(-1, 1)/15
        if self.velocity.dx > self.maxspeed:
            self.velocity.dx = .2
        if self.velocity.dx < -self.maxspeed:
            self.velocity.dx = -.2
        if self.velocity.dy > self.maxspeed:
            self.velocity.dy = .2
        if self.velocity.dy < -self.maxspeed:
            self.velocity.dy = -.2

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        is_off_screen = False
        
        #Creates Screen Wrapping effect
        if self.center.x > SCREEN_WIDTH:
            self.center.x = SCREEN_WIDTH -2
            self.velocity.dx *= -1
        elif self.center.x < 0:
            self.center.x = 2
            self.velocity.dx *= -1
        elif self.center.y > SCREEN_HEIGHT:
            self.velocity.dy *= -1
        elif self.center.y < 0:
            self.velocity.dy *= -1
        return is_off_screen



class Tree(effectObject):
    def __init__(self, xSpot, ySpot):
        super().__init__()
        self.alive = True
        self.center.x = xSpot
        self.center.y = ySpot
        self.count = 0
        self.oxygenGen = 3
        self.waterGen = -2
        self.label = "tree"
        self.size = random.randint(3, 5)
        self.variation = random.randint(1, 4)
        self.image = "img/t" + str(self.variation) + ".png"
        self.texture = arcade.load_texture(self.image)
    def draw(self):
        #arcade.draw_circle_filled(self.center.x, self.center.y, self.size, arcade.color.GREEN, 2)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width * self.size / 3, self.texture.height * self.size / 3, self.texture, 0, 255)
        #arcade.draw_text(self.label, self.center.x, self.center.y, arcade.color.BLACK, DEFAULT_FONT_SIZE)
    def grow(self):
        self.size += 1


class Hut(effectObject):
    def __init__(self, xSpot, ySpot):
        super().__init__()
        self.alive = True
        self.center.x = xSpot
        self.center.y = ySpot
        self.count = 0
        self.oxygenGen = 0
        self.waterGen = 0
        self.foodGen = 3
        self.woodGen = -5
        self.label = "hut"
        self.size = 3
        self.size2 = 2
        self.image = "img/hut.png"
        self.texture = arcade.load_texture(self.image)

        self.image2 = "img/field.png"
        self.texture2 = arcade.load_texture(self.image2)
    def draw(self):
        #arcade.draw_circle_filled(self.center.x, self.center.y, self.size, arcade.color.GREEN, 2)
        
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width * self.size, self.texture.height * self.size, self.texture2, 0, 255)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width * self.size2, self.texture.height * self.size2, self.texture, 0, 255)
        
        #arcade.draw_text(self.label, self.center.x, self.center.y, arcade.color.BLACK, DEFAULT_FONT_SIZE)
    def grow(self):
        self.size += 1

class Cloud(effectObject):
    def __init__(self):
        super().__init__()
        self.alive = True
        self.center = Point()
        self.center.x = random.randint(0, SCREEN_WIDTH)
        self.center.y = random.randint(0, SCREEN_HEIGHT)
        self.velocity = Velocity()
        self.velocity.dx = random.uniform(-1, 1)
        self.velocity.dy = random.uniform(-1, 1)
        self.count = 0
        self.oxygenGen = 1
        self.waterGen = 1
        self.image = "img/cloud.png"
        self.texture = arcade.load_texture(self.image)
        self.label = "cloud"
        self.size = random.randint(40, 80)
    def draw(self):
        #arcade.draw_circle_filled(self.center.x, self.center.y, self.size, arcade.color.LIGHT_GRAY, 2)
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, 0, 255)
        #arcade.draw_ellipse_filled(self.center.x - self.size, self.center.y - self.size, self.center.x + self.size, self.center.y + self.size, arcade.color.LIGHT_GRAY, -1)
    def advance(self):
        self.center.y += self.velocity.dy
        self.center.x += self.velocity.dx

    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        is_off_screen = False
        
        #Creates Screen Wrapping effect
        if self.center.x > SCREEN_WIDTH:
            self.alive = False
        elif self.center.x < 0:
            self.alive = False
        elif self.center.y > SCREEN_HEIGHT:
            self.alive = False
        elif self.center.y < 0:
            self.alive = False
        return is_off_screen

class populationGroup():
    def __init__(self):
        self.maxpopulation = random.randint(30,50)
 


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.BRITISH_RACING_GREEN)
        self.trees = []
        self.clouds = []
        self.people = []
        self.crabs = []
        self.huts = []
        self.oxygen = Oxygen()
        self.water = Water()
        self.food = Food()
        self.wood = Wood()

        #shader_file_path = "pixelate.glsl"
        #window_size = self.get_size()
        #self.shadertoy = Shadertoy.create_from_file(window_size, shader_file_path)

    def setup(self):
        t = 0
        while t < START_TREE:
            tree = Tree(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            self.trees.append(tree)
            t += 1

        p = 0
        while p < START_PEOPLE:
            person = Organism(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            self.people.append(person)
            p += 1


        c = 0
        while c < START_CRAB:
            crab = Crab(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            self.crabs.append(crab)
            c += 1

        """Set up the game here. Call this function to restart the game."""
        pass

    def update(self, delta_time):

        # Cloud generation
        if len(self.clouds) < CLOUD_MAX:
            i = random.randint(0, 100)
            if i == 100:
                cloud = Cloud()
                self.clouds.append(cloud)

        #Crab population
        if len(self.crabs) < len(self.people)/5:
            i = random.randint(0, 500)
            if i == 500:
                crab = Crab(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
                self.crabs.append(crab)


        #Cloud advancement and Calc
        for cloud in self.clouds:
            self.water.update(cloud.waterGen * cloud.size * 4 * delta_time)
            cloud.advance()

        for hut in self.huts:
            self.food.update(hut.foodGen * hut.size * delta_time)
            self.water.update(-1 * hut.size * delta_time)
            if hut.size < 1:
                hut.alive = False
            

        #People movement
        for person in self.people:
            person.advance()

        #Crab move
        for crab in self.crabs:
            crab.advance()

        #hut creation
        if self.wood.count >= (3000 * (len(self.huts)/2)) and len(self.huts) < len(self.people)/5:
            self.wood.count -= 3000 * (len(self.huts)/2)
            hut = Hut(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
            self.huts.append(hut)

        if self.wood.count >= (500 * len(self.huts)):
            for hut in self.huts:
                c = random.randint(0, 200)
                if c == 200:
                    if hut.size < 6:
                        self.wood.count -= 500 * len(self.huts)
                        hut.grow()


        #Tree growth
        for tree in self.trees:
            x = random.randint(0, 200)
            if x == 200:
                tree.grow()
            if tree.size >= 9:
                newTree = Tree(tree.center.x + random.randint(-40, 40), tree.center.y + random.randint(-40, 40))
                self.trees.append(newTree)
                tree.size /= 2

        #People Birth
        for hut in self.huts:
            if self.oxygen.count > 500 and self.water.count > 100:
                c = random.randint(0, (10 * len(self.people) + 1))
                if c == 1:
                    newPerson = Organism(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
                    self.people.append(newPerson)

        #People Death
        if self.oxygen.count < 2000 or self.water.count < 100 or self.food.count < (100 * len(self.people)):
            for person in self.people:
                c = random.randint(0, 200)
                if c == 200:
                    person.alive = False

        #Tree Death oxygen
        if len(self.trees) > 10:
            if self.oxygen.count > 20000:
                for tree in self.trees:
                    c = random.randint(0, 400)
                    if c == 400:
                        tree.alive = False

        #Tree Death water
        if len(self.trees) > 10:
            if self.water.count < 100:
                for tree in self.trees:
                    c = random.randint(0, 400)
                    if c == 100:
                        tree.alive = False
                for hut in self.huts:
                    c = random.randint(0, 100)
                    if c == 100:
                        hut.size -= 1


        #Oxygen and water calculations
        if self.oxygen.count > 0:
            self.oxygen.update(len(self.people) * -5 * delta_time)
            self.oxygen.update(len(self.trees) * delta_time) 

        if self.water.count > 0:
            self.water.update(len(self.people) * -2 * delta_time)
            self.water.update(len(self.trees) * -3 * delta_time) 


        self.food.update(len(self.people) * -5 * delta_time)
        
        #Cleanups Collision Detections
        self.check_off_screen()
        self.cleanup()
        self.check_collisions()
        

    def on_draw(self):
        self.clear()
        
        for hut in self.huts:
            hut.draw()
        
        for tree in self.trees:
            tree.draw()


        for person in self.people:
            person.draw()

        for crab in self.crabs:
            crab.draw()

        for cloud in self.clouds:
            cloud.draw()
        
       

        self.oxygen.draw()
        self.water.draw()
        self.food.draw()
        self.wood.draw()

        #self.shadertoy.render()
       
        # Code to draw the screen goes here

    def check_collisions(self):


        #People Collisions
        for person in self.people:
            for tree in self.trees:

                if person.alive and tree.alive:
                    too_close = person.size + tree.size
                    if (abs(person.center.x - tree.center.x) < too_close and
                        abs(person.center.y - tree.center.y) < too_close):
                        if tree.size >= 1:
                            tree.size -= 1
                            self.wood.update(100)
                            #person.size += 1
                        if tree.size <= 0:
                            tree.alive = False

            for crab in self.crabs:

                if person.alive and crab.alive:
                    too_close = 5
                    if (abs(person.center.x - crab.center.x) < too_close and
                        abs(person.center.y - crab.center.y) < too_close):
                            self.food.update(50)
                            person.alive = False
                            crab.alive = False

        #Hut collision
        for hut in self.huts:
            for tree in self.trees:

                if hut.alive and tree.alive:
                    too_close = hut.size + tree.size
                    if (abs(hut.center.x - tree.center.x) < too_close and
                        abs(hut.center.y - tree.center.y) < too_close):
                            tree.alive = False

            for crab in self.crabs:

                if hut.alive and crab.alive:
                    too_close = hut.size + crab.size
                    if (abs(hut.center.x - crab.center.x) < too_close and
                        abs(hut.center.y - crab.center.y) < too_close):
                            hut.size -= 1
                            crab.alive = False

        #Cloud Collisions
        for cloud in self.clouds:
            for tree in self.trees:

                if cloud.alive and tree.alive:
                    too_close = cloud.size/2
                    if (abs(cloud.center.x - tree.center.x) < too_close and
                        abs(cloud.center.y - tree.center.y) < too_close):
                        if tree.size <= 7:
                            tree.size += 1
                            #person.size += 1
                        if tree.size <= 0:
                            tree.alive = False

    def check_off_screen(self):
        for person in self.people:
            person.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
        for cloud in self.clouds:
            cloud.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

    def cleanup(self):
        for person in self.people:
            if person.alive == False:
                self.people.remove(person)
        for tree in self.trees:
            if tree.alive == False:
                self.trees.remove(tree)
        for cloud in self.clouds:
            if cloud.alive == False:
                self.clouds.remove(cloud)
        for crab in self.crabs:
            if crab.alive == False:
                self.crabs.remove(crab)
        for hut in self.huts:
            if hut.alive == False:
                self.huts.remove(hut)
        

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()