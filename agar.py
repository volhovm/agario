import pygame,random,math

# Dimension Definitions
SCREEN_WIDTH, SCREEN_HEIGHT = (800,500)
PLATFORM_WIDTH, PLATFORM_HEIGHT = (2000,2000)

# Other Definitions
NAME = "agar.io"
VERSION = "0.2"

# Pygame initialization
pygame.init()
pygame.display.set_caption("{} - v{}".format(NAME, VERSION))
clock = pygame.time.Clock()
try:
    font = pygame.font.Font("Ubuntu-B.ttf",20)
    big_font = pygame.font.Font("Ubuntu-B.ttf",24)
except:
    print("Font file not found: Ubuntu-B.ttf")
    font = pygame.font.SysFont('Ubuntu',20,True)
    big_font = pygame.font.SysFont('Ubuntu',24,True)

# Surface Definitions
MAIN_SURFACE = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
SCOREBOARD_SURFACE = pygame.Surface((95,25),pygame.SRCALPHA)
LEADERBOARD_SURFACE = pygame.Surface((155,278),pygame.SRCALPHA)
SCOREBOARD_SURFACE.fill((50,50,50,80))
LEADERBOARD_SURFACE.fill((50,50,50,80))

# Auxiliary Functions
def drawText(message,pos,color=(255,255,255)):
    """Blits text to main (global) screen.
    """
    MAIN_SURFACE.blit(font.render(message,1,color),pos)

def getDistance(a, b):
    """Calculates Euclidean distance between given points.
    """
    diffX = math.fabs(a[0]-b[0])
    diffY = math.fabs(a[1]-b[1])
    return ((diffX**2)+(diffY**2))**(0.5)


# Auxiliary Classes
class Painter:
    """Used to organize the drawing/ updating procedure.
    Implemantation based on Strategy Pattern.
    Note that Painter draws objects in a FIFO order.
    Objects added first, are always going to be drawn first.
    """

    def __init__(self):
        self.paintings = []

    def add(self, drawable):
        self.paintings.append(drawable)

    def paint(self):
        for drawing in self.paintings:
            drawing.draw()


class Camera:
    """Used to represent the concept of POV.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.zoom = 0.5


    def centre(self,blobOrPos):
        """Makes sure that the given object will be at the center of player's view.
        Zoom is taken into account as well.
        """
        if isinstance(blobOrPos, Player):
            x, y = blobOrPos.x, blobOrPos.y
            self.x = (x - (x*self.zoom)) - x + (SCREEN_WIDTH/2)
            self.y = (y - (y*self.zoom)) - y + (SCREEN_HEIGHT/2)
        elif type(blobOrPos) == tuple:
            self.x, self.y = blobOrPos


    def update(self, target):
        self.zoom = 100/(target.mass)+0.3
        self.centre(blob)

class Drawable:
    """Used as an abstract base-class for every drawable element.
    """

    def __init__(self, surface, camera):
        self.surface = surface
        self.camera = camera

    def draw(self):
        pass

class Grid(Drawable):
    """Used to represent the backgroun grid.
    """

    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.color = (230,240,240)

    def draw(self):
        # A grid is a set of horizontal and prependicular lines
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        for i in range(0,2001,25):
            pygame.draw.line(self.surface,  self.color, (x, i*zoom + y), (2001*zoom + x, i*zoom + y), 3)
            pygame.draw.line(self.surface, self.color, (i*zoom + x, y), (i*zoom + x, 2001*zoom + y), 3)

class HUD(Drawable):
    """Used to represent all necessary Head-Up Display information on screen.
    """

    def __init__(self, surface, camera):
        super().__init__(surface, camera)

    def draw(self):
        w,h = font.size("Score: "+str(int(blob.mass*2))+" ")
        MAIN_SURFACE.blit(pygame.transform.scale(SCOREBOARD_SURFACE, (w, h)),
                          (8,SCREEN_HEIGHT-30))
        MAIN_SURFACE.blit(LEADERBOARD_SURFACE,(SCREEN_WIDTH-160,15))
        drawText("Score: " + str(int(blob.mass*2)),(10,SCREEN_HEIGHT-30))
        MAIN_SURFACE.blit(big_font.render("Leaderboard", 0, (255, 255, 255)),
                          (SCREEN_WIDTH-157, 20))
        drawText("1. G #1",(SCREEN_WIDTH-157,20+25))
        drawText("2. G #2",(SCREEN_WIDTH-157,20+25*2))
        drawText("3. ISIS",(SCREEN_WIDTH-157,20+25*3))
        drawText("4. ur mom",(SCREEN_WIDTH-157,20+25*4))
        drawText("5. w = pro team",(SCREEN_WIDTH-157,20+25*5))
        drawText("6. jumbo",(SCREEN_WIDTH-157,20+25*6))
        drawText("7. [voz]plz team",(SCREEN_WIDTH-157,20+25*7))
        drawText("8. G #3",(SCREEN_WIDTH-157,20+25*8))
        drawText("9. doge",(SCREEN_WIDTH-157,20+25*9))
        if(blob.mass <= 500):
            drawText("10. G #4",(SCREEN_WIDTH-157,20+25*10))
        else:
            drawText("10. Viliami",(SCREEN_WIDTH-157,20+25*10),(210,0,0))




class Player(Drawable):
    """Used to represent the concept of a player.
    """
    COLOR_LIST = [
    (37,7,255),
    (35,183,253),
    (48,254,241),
    (19,79,251),
    (255,7,230),
    (255,7,23),
    (6,254,13)]

    FONT_COLOR = (50, 50, 50)


    def __init__(self, surface, camera, name="", initmass=20):
        super().__init__(surface, camera)
        self.x = random.randint(100,400)
        self.y = random.randint(100,400)
        self.mass = initmass
        self.speed = 4
        self.color = col = random.choice(Player.COLOR_LIST)
        self.outlineColor = (
            int(col[0]-col[0]/3),
            int(col[1]-col[1]/3),
            int(col[2]-col[2]/3))
        if name: self.name = name
        else: self.name = "Anonymous"
        self.absorbed = []  # List to store absorbed players
        self.original_mass = initmass  # Track original mass for scaling

    def absorb(self, player):
        """Add a player to the absorbed list"""
        # Store relevant info about the absorbed player
        absorbed_info = {
            'color': player.color,
            'outline_color': player.outlineColor,
            'name': player.name,
            'mass': player.mass,
            'original_mass': player.mass,  # Store original mass for scaling
            'angle': random.uniform(0, 2 * math.pi),  # Random position inside
            'distance_factor': random.uniform(0.2, 0.7)  # How far from center (0-1)
        }
        self.absorbed.append(absorbed_info)

    def add_mass(self, amount):
        """Add mass to the player and scale all absorbed players proportionally"""
        old_mass = self.mass
        self.mass += amount

        # Scale factor based on how much the player grew
        scale_factor = self.mass / old_mass

        # Scale all absorbed players
        for absorbed in self.absorbed:
            absorbed['mass'] *= scale_factor

    def draw(self):
        """Draws the player as an outlined circle with absorbed players inside."""
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        radius = int(self.mass/2*zoom)

        # Draw the outline of the player as a darker, bigger circle
        pygame.draw.circle(self.surface, self.outlineColor, center, int((self.mass/2 + 3)*zoom))
        # Draw the actual player as a circle
        pygame.draw.circle(self.surface, self.color, center, radius)

        # Draw absorbed players as smaller circles inside
        for absorbed in self.absorbed:
            # Calculate position inside the main circle
            # Size is proportional to original mass but scaled with player growth
            inner_radius = min(absorbed['mass'] / 3, self.mass / 4) * zoom

            # Maintain relative position as player grows
            distance = absorbed['distance_factor'] * (radius - inner_radius)
            inner_x = center[0] + math.cos(absorbed['angle']) * distance
            inner_y = center[1] + math.sin(absorbed['angle']) * distance

            # Draw the absorbed player
            inner_center = (int(inner_x), int(inner_y))
            pygame.draw.circle(self.surface, absorbed['outline_color'], inner_center,
                              int(inner_radius + 2))
            pygame.draw.circle(self.surface, absorbed['color'], inner_center,
                              int(inner_radius))

            # Draw a small name indicator if there's enough space
            if inner_radius > 10:
                small_font = pygame.font.SysFont('Ubuntu', 10, True)
                #name_surface = small_font.render(absorbed['name'][:1], True, Player.FONT_COLOR)
                name_surface = small_font.render(absorbed['name'], True, Player.FONT_COLOR)
                name_rect = name_surface.get_rect(center=inner_center)
                self.surface.blit(name_surface, name_rect)

        # Draw player's name
        fw, fh = font.size(self.name)
        drawText(self.name, (self.x*zoom + x - int(fw/2), self.y*zoom + y - int(fh/2)),
                 Player.FONT_COLOR)


    def collisionDetection(self, edibles):
        """Detects cells being inside the radius of current player.
        Those cells are eaten.
        """
        for edible in edibles:
            if(getDistance((edible.x, edible.y), (self.x,self.y)) <= self.mass/2):
                self.add_mass(0.5)  # Use add_mass instead of directly modifying mass
                edibles.remove(edible)

    def move(self):
        """Updates player's position based on arrow key inputs.
        """
        keys = pygame.key.get_pressed()

        # Set movement speed
        vx = 0
        vy = 0

        # Check which keys are pressed and update velocity
        if keys[pygame.K_LEFT]:
            vx = -self.speed
        if keys[pygame.K_RIGHT]:
            vx = self.speed
        if keys[pygame.K_UP]:
            vy = -self.speed
        if keys[pygame.K_DOWN]:
            vy = self.speed

        # Update position
        self.x += vx
        self.y += vy


    def feed(self):
        """Unsupported feature.
        """
        pass

    def split(self):
        """Unsupported feature.
        """
        pass


class Cell(Drawable): # Semantically, this is a parent class of player
    """Used to represent the fundamental entity of game.
    A cell can be considered as a quantom of mass.
    It can be eaten by other entities.
    """
    CELL_COLORS = [
    (80,252,54),
    (36,244,255),
    (243,31,46),
    (4,39,243),
    (254,6,178),
    (255,211,7),
    (216,6,254),
    (145,255,7),
    (7,255,182),
    (255,6,86),
    (147,7,255)]

    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.x = random.randint(20,1980)
        self.y = random.randint(20,1980)
        self.mass = 7
        self.color = random.choice(Cell.CELL_COLORS)

    def draw(self):
        """Draws a cell as a simple circle.
        """
        zoom = self.camera.zoom
        x,y = self.camera.x, self.camera.y
        center = (int(self.x*zoom + x), int(self.y*zoom + y))
        pygame.draw.circle(self.surface, self.color, center, int(self.mass*zoom))

class CellList(Drawable):
    """Used to group and organize cells.
    It is also keeping track of living/ dead cells.
    """

    def __init__(self, surface, camera, numOfCells):
        super().__init__(surface, camera)
        self.count = numOfCells
        self.list = []
        for i in range(self.count): self.list.append(Cell(self.surface, self.camera))

    def draw(self):
        for cell in self.list:
            cell.draw()


class Bot(Player):
    """AI-controlled player that follows food and hunts smaller players"""

    def __init__(self, surface, camera, name="Bot"):
        super().__init__(surface, camera, name)
        self.target = None
        self.decision_cooldown = 0

    def find_target(self, cells, players):
        """Find closest food or smaller player to chase"""
        # Reset target periodically to reassess situation
        if self.target == None or self.decision_cooldown <= 0:
            self.decision_cooldown = 5  # Update target every 30 frames

            closest_food = None
            min_food_dist = float('inf')

            # Find closest food
            for cell in cells:
                dist = getDistance((self.x, self.y), (cell.x, cell.y))
                if dist < min_food_dist:
                    min_food_dist = dist
                    closest_food = cell

            # Sometimes look for players to eat (if they're smaller)
            if random.random() < 0.3:  # 30% chance to look for players
                for player in players:
                    if player != self and player.mass < self.mass * 0.9:  # Only chase if significantly smaller
                        dist = getDistance((self.x, self.y), (player.x, player.y))
                        if dist < min_food_dist * 1.5:  # Prefer closer players
                            min_food_dist = dist
                            closest_food = player

            self.target = closest_food
        else:
            self.decision_cooldown -= 1

    def move(self):
        """Move toward current target"""
        if self.target:
            # Calculate direction to target
            dx = self.target.x - self.x
            dy = self.target.y - self.y

            # Normalize direction
            length = max(0.01, math.sqrt(dx*dx + dy*dy))
            dx /= length
            dy /= length

            # Move toward target
            self.x += dx * self.speed
            self.y += dy * self.speed



def check_player_collisions(players):
    """Check if players can eat each other based on size and proximity"""
    to_remove = []

    for i, player1 in enumerate(players):
        if player1 in to_remove:
            continue

        for j, player2 in enumerate(players):
            # Skip self-comparison
            if i == j:
                continue

            if player2 in to_remove:
                continue

            # Calculate distance between players
            distance = getDistance((player1.x, player1.y), (player2.x, player2.y))

            # Check if player1 can eat player2
            # Player can eat another if it's 10% bigger and centers are close enough
            if (player1.mass > player2.mass * 1.1 and
                distance < player1.mass/2 - player2.mass/4):

                # Player1 absorbs player2 (visually)
                player1.absorb(player2)

                # Player1 gains a portion of player2's mass
                player1.add_mass(player2.mass * 0.8)

                # Mark player2 for removal
                if player2 not in to_remove:
                    to_remove.append(player2)

    return to_remove



# Initialize essential entities
cam = Camera()

grid = Grid(MAIN_SURFACE, cam)
cells = CellList(MAIN_SURFACE, cam, 2000)
blob = Player(MAIN_SURFACE, cam, "GeoVas", initmass=80)
hud = HUD(MAIN_SURFACE, cam)

painter = Painter()
painter.add(grid)
painter.add(cells)
painter.add(blob)
painter.add(hud)

bots = []
num_bots = 5  # Number of bots to add

# Create bots
for i in range(num_bots):
    bot = Bot(MAIN_SURFACE, cam, f"Bot {i+1}")
    bots.append(bot)
    painter.add(bot)  # Add to painter to be drawn


# Game main loop
while(True):

    clock.tick(50)

    for e in pygame.event.get():
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if(e.key == pygame.K_SPACE):
                del(cam)
                blob.split()
            if(e.key == pygame.K_w):
                blob.feed()
        if(e.type == pygame.QUIT):
            pygame.quit()
            quit()

    for bot in bots:
        bot.find_target(cells.list, [blob] + bots)
        bot.move()
        bot.collisionDetection(cells.list)

    blob.move()
    blob.collisionDetection(cells.list)

    all_players = [blob] + bots
    eaten_players = check_player_collisions(all_players)

    # Check eaten
    for player in eaten_players:
        if player == blob:
            print("Game Over! You were eaten!")
            pygame.quit()
            quit()
        elif player in bots:
            print("Removing player", player)
            # Bot was eaten, remove and respawn
            bots.remove(player)
            painter.paintings.remove(player)

    cam.update(blob)
    MAIN_SURFACE.fill((242,251,255))
    # Uncomment next line to get dark-theme
    #surface.fill((0,0,0))
    painter.paint()
    # Start calculating next frame
    pygame.display.flip()
