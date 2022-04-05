import pygame
import collisions


class objectPhysics:
    global jumpCount
    jumpCount = 10

    # All new objects will set their properties here
    def __init__(self, x, y, width, height, color, wn, vel, player=False):
        self.x = x
        self.y = y
        self.velX = 0
        self.velY = 0
        self.gravityX = 0
        self.gravityY = 0
        self.width = width
        self.height = height
        self.vel = vel
        self.color = color
        self.isJumping = False
        self.player = player
        self.wn = wn
        self.objLeft = False
        self.objRight = False

    # Added new function
    def setDimensions(windowWidth, windowHeight):
        global gameHeight, gameWidth
        gameHeight = windowHeight
        gameWidth = windowWidth

    # move player
    def move(self, vel, direction):
        if str(direction).lower() == "left":
            self.x -= vel
        elif str(direction).lower() == "right":
            self.x += vel
        elif str(direction).lower() == "up":
            self.y -= vel
        elif str(direction).lower() == "down":
            self.y += vel
        else:
            print("Direction only takes 4 values: 'left', 'right', 'up', 'down'")

    def setGravity(self, x, y):
        self.gravityX = x
        self.gravityY = y

    def keepInBounds(self):
        # dont go too far left
        if self.x < 0:
            self.x = 0
            self.velY = 0

        # dont go too far right
        if self.x + self.width > gameWidth:
            self.x = gameWidth - self.width

        # dont go too high
        if self.y < 0:
            self.y = 0
            self.velY = 0

        # dont go too low
        if self.y + self.height > gameHeight:
            self.y = gameHeight - self.height
            self.velY = 0
            # if i go too low that means i touched the ground
            # so im no longer jumping
            self.isJumping = False

    def update(self, objectlist):

        # gravity makes user fall
        self.velX += self.gravityX
        self.velY += self.gravityY

        # velocity makes me move
        self.x += self.velX
        self.y += self.velY

        # check if I collided with anyone
        self.processCollisions(objectlist)

        # don't want to fall out of the level
        self.keepInBounds()

    def processCollisions(self, objectlist):
        for obj in objectlist:
            if collisions.checkCollision(self, obj) and self != obj:
                self.objLeft, self.objRight = collisions.checkCollisionX(self, obj)
                self.isJumping = False

                # I'm inside the box, so I have to move out (subtract by velocity)
                # in order to see what side I collided from
                self.x -= self.velX
                self.y -= self.velY

                side = collisions.checkSide(self, obj)

                # left side collision
                if side == collisions.Side.LEFT:
                    self.x += self.vel * 2
                    self.velX = 0

                # right side collision
                if side == collisions.Side.RIGHT:
                    self.x -= self.vel * 2
                    self.velX = 0

                # up side collision
                if side == collisions.Side.UP or self.y + self.height > gameHeight:
                    self.y = obj.y - obj.height - 5
                    self.isJumping = False
                    self.velY = 0
                else:
                    self.isJumping = True

                # down side collision
                if side == collisions.Side.DOWN:
                    self.y = obj.y + obj.height - 5
                    self.velY = 0

    # Each object will draw with its own dimensions
    def draw(self):
        pygame.draw.rect(self.wn, self.color, (self.x, self.y, self.width, self.height))
        # if you need jumpCount back in here, feel free to add it back in

        # now gravity takes care of the falling
        # negative values make you go up

    def jump(self, power, object_list):
        if not self.isJumping:
            self.velY = -power
            self.isJumping = True
