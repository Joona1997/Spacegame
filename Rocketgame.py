import pygame
import os
import random
pygame.font.init()

#variables for the sice of the screen.
WIDTH, HEIGHT = 500, 700
#variable that is the gamescreen.
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#Name of the game
pygame.display.set_caption("Rocket Game!")

#colors for the game.
WHITE = (255, 255, 255)
BLACK = (0,0,0)
BROWN = (139,69,19)

#variables for the texts in the game.
POINTS_FONT = pygame.font.SysFont('comicsans', 20)
LOSER_FONT = pygame.font.SysFont('comicsans', 50)

#Games FPS (frames per second).
FPS = 60

#Pygame event, for when a meteorite touches the spaceship
METEORITE_HIT = pygame.USEREVENT +1

#Velocity of the spaceship.
VEL = 5
#Variables for the spaceships size.
SPACESHIP_WIDTH, SPACESHIP_HEIGT = 50, 100
#Loading the image for the spaceship.
SPACESHIP = pygame.image.load(os.path.join('Alus2.png'))
#Scaling the image of the spaceship, same size of the spaceship
SPACESHIP = pygame.transform.scale(SPACESHIP, (SPACESHIP_WIDTH,SPACESHIP_HEIGT))

#Variables for the size of the meteorite.
METEORITE_WIDTH, METEORITE_HEIGT = 50, 100 
#Loading the image for the meteorites.
METEORITE = pygame.image.load(os.path.join('meteorite.png'))
#Scaling the picture to the size of a meteorite.
METEORITE = pygame.transform.scale(METEORITE, (METEORITE_WIDTH, METEORITE_HEIGT))

#Loading the image for the space backcround
BACKGROUND = pygame.image.load(os.path.join('space.png'))
#Scaling the picture to the size of the window
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

#Function for writing that a player has lost the game.
#At the end 5 second delay, before the game starts again.
def draw_loser(text):
    draw_text = LOSER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

#Function for randomizing where the meteorites spawn.
#Function is used to define the x position for the meteorite.
#0-450 pixels.
def randomizer(): 
    n = random.randint(0,9)
    paikka = n *50 
    return paikka

#Function for drawing different things on the screen.
#Draws the background, points on the screen, spaceship and the meteorites
def draw_window(ship, meteorites, points):
    WIN.fill(BLACK) 
    WIN.blit(BACKGROUND, (0, 0))
    points_text = POINTS_FONT.render("Points: " + str(points), 1, WHITE )
    WIN.blit(points_text, (WIDTH - points_text.get_width() - 10, 10))
    WIN.blit(SPACESHIP, (ship.x, ship.y)) 
    for meteorite in meteorites:
        WIN.blit(METEORITE, (meteorite.x, meteorite.y))
    pygame.display.update()
    
#Function for moving the meteorites down, checking for collisions 
#with the spaceship and deleting the meteorites when they are off the screen.
def handle_meteorites(meteorites, ship, meteorite_vel):
    for meteorite in meteorites[:]:
        meteorite.y += meteorite_vel
        if ship.colliderect(meteorite):
            pygame.event.post(pygame.event.Event(METEORITE_HIT))
            meteorites.remove(meteorite)
        if meteorite.y >= 750:
            meteorites.remove(meteorite)

#Function for moving the spaceship.
#If the player presses a button, move the spaceship in that direction.
def ship_movement(keys_pressed, ship):
    if keys_pressed[pygame.K_a] and ship.x - VEL > 0: #LEFT
        ship.x -= VEL
    if keys_pressed[pygame.K_d] and ship.x + VEL < 450: #RIGTH
        ship.x += VEL
    if keys_pressed[pygame.K_w] and ship.y - VEL > 0: #UP
        ship.y -= VEL
    if keys_pressed[pygame.K_s] and ship.y + VEL < 600: #DOWN
        ship.y += VEL
    


def main():
    #creates the spaceship
    ship = pygame.Rect(200, 500, SPACESHIP_WIDTH, SPACESHIP_HEIGT)

    #Kello is for keeping track of how much the game needs to advance.
    #It increases by +1, each loop of main. (main loops at max 60 FPS: so kello = 60 = 1sec)
    kello = 0

    #When kello is as much as this variable,
    #two meteorites spawn
    game_advancing2 = 60

    #Increases when meteorites spawn, when 20 meteorites have spawned
    #decreases game_advancin2 (whitch makes the meteorites spawn more often)
    game_advancing = 0
    
    #List of the meteorites
    meteorites = []
    #Velocity of the meteorites (increases as the game goes)
    meteorite_vel = 5
    #Variable for the points in the game.
    points = 0

    #clock for the FPS of the game
    clock = pygame.time.Clock()

    #Keeps the game on
    run = True
    while run:
        #Caps the fps of the game at 60
        clock.tick(FPS)

        #Loop for closing the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        #Loop for making the game faster pace as the goes.
        if game_advancing == 10:
            meteorite_vel += 1
            game_advancing =0
            if game_advancing2 > 4:
                game_advancing2 -= 4
           
        #Loop for spawning the meteorites at a specific time
        # also refreshes kello to zero and adds points.  
        if kello == game_advancing2:
            meteorite2 = pygame.Rect(randomizer(), -50, METEORITE_WIDTH, METEORITE_HEIGT)
            meteorites.append(meteorite2)
            meteorite = pygame.Rect(randomizer(), 0, METEORITE_WIDTH, METEORITE_HEIGT)
            meteorites.append(meteorite)
            kello = 0
            game_advancing += 1
            points += 1

        #Losing text
        lost_text = ""

        #if player hits a meteorite
        #updates the losing text
        if event.type == METEORITE_HIT:
            lost_text = "You lost the game!" 

        #If losing text has something, calls draw_loser function.
        if lost_text != "":
            draw_loser(lost_text)
            break

        #Checks for pressed keys and sends them to ship_movement.
        keys_pressed = pygame.key.get_pressed()
        ship_movement(keys_pressed, ship)

        #Moves meteorites.
        handle_meteorites(meteorites, ship, meteorite_vel)
        #Draws everything on the screen.
        draw_window(ship, meteorites, points)
        
        kello += 1

    main()


if __name__ == "__main__":
    main()
