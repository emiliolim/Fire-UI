

# Import the pygame module

from time import sleep
import pygame
import random
from math import sqrt
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
CONTROLS_HEIGHT = 200
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
ENTITY_WIDTH = 30
ENTITY_HEIGHT = 30

SIMULATION_HEIGHT = SCREEN_HEIGHT - CONTROLS_HEIGHT
SIMULATION_WIDTH = SCREEN_WIDTH
 # Define a player object by extending pygame.sprite.Sprite
    # The surface drawn on the screen is now an attribute of 'player'
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, fuel, flamability):
        super(Entity, self).__init__()
        self.x = x
        self.y = y
        self.fuel = fuel
        self.flamability = flamability
        self.surf = pygame.Surface((ENTITY_WIDTH, ENTITY_HEIGHT))
        self.onFire = False
        self.rect = self.surf.get_rect()
    
    def setOnFire(self):
        self.onFire = True
        self.surf.fill((self.fuel, 0, 0))
    def burn(self):
        self.fuel -= random.randrange(0, 10)
        if self.fuel <= 0:
            self.onFire = False
            self.surf.fill((0, 0 , 0))
            return
        self.surf.fill((self.fuel+ 100, 0, 0))


class Tree(Entity):
    def __init__(self, x, y):
        fuel = random.randrange(50, 100)
        flamability = 0.1
        super(Tree, self).__init__(x, y, fuel, flamability)
        self.surf.fill((0, 155+self.fuel, 0))

class Water(Entity):
    def __init__(self, x, y):
        fuel = 0
        flamability = 0
        super(Water, self).__init__(x, y, fuel, flamability)
        self.surf.fill((65,105,225))

class Road(Entity):
    def __init__(self, x, y):
        fuel = 0
        flamability = 0
        super(Road, self).__init__(x, y, fuel, flamability)
        self.surf.fill((105,105,105))

class House(Entity):
    def __init__(self, x, y):
        fuel = 200
        flamability = 0
        super(House, self).__init__(x, y, fuel, flamability)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("Arial", 20)

class Button:
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, text,  pos, font, bg="black", feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)
 
    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self):
        screen.blit(button1.surface, (self.x, self.y))
        pygame.display.flip()
 
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change_text(self.feedback, bg="red")
button1 = Button(
    "Click here",
    (100,100),
    font=30,
    bg="navy",
    feedback="You clicked")
def main():
    # Initialize pygame
    pygame.init()
    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def simulation():
        def simulate():
        # Create and populate tree list
            entities = []
            for i in range(round(SCREEN_WIDTH / ENTITY_WIDTH)):
                for k in range(round((SCREEN_HEIGHT - CONTROLS_HEIGHT)/ ENTITY_HEIGHT)):
                    entities.append(Tree(i, k))

        # Variable to keep the main loop running
            running = False
            while not running:
                # for loop through the event queue
                for event in pygame.event.get():
                    # Check for KEYDOWN event
                    if event.type == KEYDOWN:
                        # If the Esc key is pressed, then exit the main loop
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            break
                    # Check for QUIT event. If QUIT, then set running to false.
                    elif event.type == QUIT:
                        pygame.quit()
                        break
                for entity in entities:
                   
                    screen.blit(entity.surf, (entity.x*ENTITY_WIDTH, CONTROLS_HEIGHT + entity.y * ENTITY_HEIGHT))
                
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            break
                        button1.click(event)
                    button1.show()
                    pygame.display.update()
            pygame.display.flip()
            entities[0].setOnFire()

        # Main loop
        
            firstRun = True
           
            while running:
                sleep(0.25)

                # for loop through the event queue
                for event in pygame.event.get():
                    # Check for KEYDOWN event
                    if event.type == KEYDOWN:
                        # If the Esc key is pressed, then exit the main loop
                        if event.key == K_ESCAPE:
                            running = False
                    # Check for QUIT event. If QUIT, then set running to false.
                    elif event.type == QUIT:
                        running = False

                # Fill the screen with black
                screen.fill((255, 255, 255))
                print("New game cycle")
                # Draw the trees on the screen
                for treeOne in entities:
                    # If the current tree is not on fire, draw the tree as normal
                    screen.blit(treeOne.surf, (treeOne.x*ENTITY_WIDTH, CONTROLS_HEIGHT + treeOne.y * ENTITY_HEIGHT))

                    if not treeOne.onFire:
                        continue
                    treeOne.burn()
                    # If the current tree is on fire, check if it lights other trees on fire
                    for treeTwo in entities:
                        # If the tree is already on fire, no need to see if it will be lit
                        if treeTwo.onFire or treeTwo.fuel <= 0:
                            continue
                        # Calculate the distance between tree one and tree two 
                        dx = treeOne.x - treeTwo.x
                        dy = treeOne.y - treeTwo.y
                        distance = sqrt(pow(dx, 2) + pow(dy, 2))

                        # Determine how likely a tree is to be lit on fire
                        fireChance = (1 / (pow(distance, 4))) * treeTwo.flamability 

                        # Check if the tree will get lit on fire
                        val = random.random()
                        if  val <= fireChance:
                            treeTwo.setOnFire()
                    # Draw the current tree on screen
                    screen.blit(treeOne.surf, (treeOne.x*ENTITY_WIDTH, CONTROLS_HEIGHT + treeOne.y * ENTITY_HEIGHT))


                # Update the display
                pygame.display.flip()
        #screen.fill((255, 255, 255))
        simulate()


    def intro():
        run = False
        while not(run):
            #pygame.init() 
            # white color 
            color = (255,255,255) 
            
            # light shade of the button 
            color_light = (170,170,170) 
            
            # dark shade of the button 
            color_dark = (100,100,100) 
            
            # stores the width of the 
            # screen into a variable 
            width = screen.get_width() 
            
            # stores the height of the 
            # screen into a variable 
            height = screen.get_height() 
                        # defining a font 
            smallfont = pygame.font.SysFont('Corbel',35) 
            
            # rendering a text written in 
            # this font 
            text = smallfont.render('Start' , True , color) 
            
            while True: 
                
                for ev in pygame.event.get(): 
                    
                    if ev.type == pygame.QUIT: 
                        pygame.quit() 
                        
                    #checks if a mouse is clicked 
                    if ev.type == pygame.MOUSEBUTTONDOWN: 
                        
                        #if the mouse is clicked on the 
                        # button the game is terminated 
                        if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                            simulation()
                            
                # fills the screen with a color 
                screen.fill((60,25,60)) 
                # stores the (x,y) coordinates into 
                # the variable as a tuple 
                mouse = pygame.mouse.get_pos() 
                
                # if mouse is hovered on a button it 
                # changes to lighter shade 
                if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                    pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
                    
                else: 
                    pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
                
                # superimposing the text onto our button 
                screen.blit(text , (width/2+30,height/2)) 
                
                # updates the frames of the game 
                pygame.display.update() 
    intro()
if __name__ == "__main__":
    main()