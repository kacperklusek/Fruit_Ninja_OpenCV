import pygame
import pygame_physics

pygame.init()
counter = 0

level_width = 500
level_height = 500
p_vel = 5
wn = pygame.display.set_mode((level_width, level_height))


global x, y
x = 100
y = 400
collide_top = False
platform_x = 100
platform_y = 300

isJump = False

# create player object at x,y, width: 50, height: 50
player = pygame_physics.objectPhysics(225, 450, 50, 50, (0, 0, 255), wn, p_vel, player=True)
testPlatform = pygame_physics.objectPhysics(300, 350, 100, 50, (255, 255, 255), wn, 0)
testPlatform2 = pygame_physics.objectPhysics(50, 350, 100, 50, (255, 255, 255), wn, 0)

# list of all objects
objectlist = []
# add the player and platform to the list
objectlist.append(player)
objectlist.append(testPlatform)
objectlist.append(testPlatform2)
objectLeft = False
objectRight = False
pygame_physics.objectPhysics.setDimensions(500, 500)
# setting player gravity
# 0 for x gravity (dont want to fall sideways)
# 1 for y gravity (fall downwards)
player.setGravity(0, 4)

# set platform gravity
# testPlatform.setGravity(0.1, 0.1)
while True:

    # listen for key presses
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    # if it jumps too high, just lower the value
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.jump(50, objectlist)

    # handle all objects
    for obj in objectlist:
        obj.update(objectlist)

    if keys[pygame.K_LEFT]:  # and not objectLeft:
        player.move(p_vel, "left")
    if keys[pygame.K_RIGHT]:  # and not objectRight:
        player.move(p_vel, "right")

    wn.fill((128, 128, 128))

    testPlatform.draw()
    testPlatform2.draw()
    player.draw()

    pygame.display.update()
    pygame.time.delay(40)
