import pygame
import math

from pygame.constants import MOUSEBUTTONUP

# -----------------------------------------------
#                  Parameters
# -----------------------------------------------
pygame.init()

WIDTH, HEIGHT = 800, 600    # Size of the screen

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Sliggshot Effect")

PLANET_MASS = 100   # Mass of the planet
SHIP_MASS = 5       # Mass of the ship
G = 5               # Gravity
FPS = 60            # Frame Per Second
PLANET_SIZE = 50    # Radius of the planet
OBJ_SIZE = 10       # Radius of the ship object
VEL_SCALE = 50      # Veleocity Scale

# Load the images
BG = pygame.transform.scale(pygame.image.load('images/space.jpg'), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load('images/jupiter.png'), (PLANET_SIZE *2, PLANET_SIZE *2))
SHIP = pygame.transform.scale(pygame.image.load('images/asteroide.png'), (OBJ_SIZE *2, OBJ_SIZE *2))

# Set up the colors needed
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# -----------------------------------------------
#                    Class
# -----------------------------------------------
class Planet:
    def __init__(self, x, y, mass) -> None:
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self) -> None:
        win.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))


class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass) -> None:
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.image = SHIP.copy()            # Create a copy the original image
        self.angle = 0                      # Angle of the image for animation

    def move(self, planet:Planet) -> None:
        # Move the object
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)       # Distance between ship and planet
        force = (G * self.mass * planet.mass) / distance ** 2                       # Force of gravity
        acceleration = force / self.mass                                            # Acceleration vector (Linear acceleration)
        angle = math.atan2(planet.y - self.y, planet.x - self.x)                    # Acceleration = hypothénuse, so we need to calculate the angle of the adjacent angle

        acceleration_x = acceleration * math.cos(angle)         # x composant of te acceleration vector
        acceleration_y = acceleration * math.sin(angle)         # y composant of te acceleration vector

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self) -> None:
        win.blit(SHIP, (int(self.x), int(self.y)))

# ----------------- Function ----------------------

def creat_ship(location, mouse) -> Spacecraft:
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, OBJ_SIZE)

    return obj

# -----------------------------------------------
#                    Main
# -----------------------------------------------
def main():
    running = True
    clock = pygame.time.Clock()                         # Put the current time of execution in clock. Usefull for time space

    planet = Planet(WIDTH//2, HEIGHT//2, PLANET_MASS)   # Planet Object present on the screen
    objects = []                                        # Array containing spacecraft objet on the screen
    temp_obj_pos = None                                 # Temporary Object Ship Position

    # Main loop of the game
    while running:
        clock.tick(FPS)                                 # Update the clock rating to the FPS
        mouse_pos = pygame.mouse.get_pos()              # get the position of the mouse

        for event in pygame.event.get():                # Check all the pygame event
            if event.type == pygame.QUIT:               # If the Event is QUIT (close the screen) then...
                running = False                         # ... so exit the loop (and the game)

            if event.type == pygame.MOUSEBUTTONDOWN:            # When left button of the mouse is clicked (down) at a position then
                temp_obj_pos = mouse_pos                        # ...Set up the position of the object

            if event.type == pygame.MOUSEBUTTONUP:              # When left butter of the mouse is release (up) then...
                obj = creat_ship(temp_obj_pos, mouse_pos)       # ...Create the ship Object at this position
                objects.append(obj)                             # ...Add the object to the array
                temp_obj_pos = None                             # ...Reinitialize the initial position


        win.blit(BG, (0,0))                                                             # Print the BG on the screen, and refresh it at each loop
        if temp_obj_pos:                                                                # if a temp object position is set then...
            win.blit(SHIP, (temp_obj_pos[0] - OBJ_SIZE, temp_obj_pos[1] - OBJ_SIZE))    # ...Draw the object on the screen
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)                    # ...Draw the vector of the object

        for obj in objects:                                                                     # For each spaceship Object in the array
            obj.move(planet)                                                                    # Move the object according to the location of the planet
            obj.draw()                                                                          # Draw the object
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT              # Check if the object if out of the screen
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE  # Check if the object collide the planet
            if off_screen or collided:                                                          # If the object go out of the screen or enter in collision whith the planet then...
                objects.remove(obj)                                                             # ...Delete it so save memory

        planet.draw()

        pygame.display.update()                                         # Update the screen and show all element

    pygame.quit()   # Exit clearly pygame



if __name__ == '__main__':
    main()
