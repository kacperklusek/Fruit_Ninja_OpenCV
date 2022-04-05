
# Returns 2 bools- if left object is colliding with player or right object is colliding with player


def checkCollisionX(object1, object2):
    global objectLeft, objectRight
    rect1 = object1
    rect2 = object2

    if (rect1.x + rect1.width == rect2.x):
        objectRight = True
    else:
        objectRight = False
    # Object 1 left collision
    if (rect1.x == rect2.x + rect2.width):
        objectLeft = True
    else:
        objectLeft = False
    return objectLeft, objectRight


def checkCollisionY(object1, object2):
    global objectUp, objectDown
    rect1 = object1
    rect2 = object2
    if ((rect1.y + rect1.height >= rect2.y) and (rect1.y < rect2.y + rect2.height)) and (rect1.x >= rect2.x and rect1.x <= (rect2.x + rect2.width)) and not objectLeft:
        objectDown = True
    else:
        objectDown = False
    return objectDown


class Side:
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3
    ERROR = 4  # might be useful


SideString = ["up", "down", "right", "left", "error"]

# checkSide(a,b) :  return what side object A is to object B
#
#   +-----+
#   |     |   +---+
#   |  a  |   | b |
#   |     |   +---+
#   +-----+
#
# In this illustration, a is to the left of b
# so, in this case, the function will return Side.LEFT
#


def checkSide(a, b):
    # Replaced all a and b with rect1 and rect
    rect1 = a
    rect2 = b
    if (rect1.x + rect1.width >= (rect2.x + rect1.vel) + rect2.width and rect1.x >= rect2.x + rect2.width):
        return Side.LEFT
    if (rect2.x + (rect2.width - rect1.vel) >= rect1.x + rect1.width and rect2.x >= rect1.x + rect1.width):
        return Side.RIGHT
    if (rect1.y + rect1.height > rect2.y + rect2.height and rect1.y > rect2.y + rect2.height):
        return Side.DOWN
    if (rect2.y + rect2.height > rect1.y + rect1.height and rect2.y > rect1.y + rect1.height):
        return Side.UP

    # it shouldn't get here but just in case
    return Side.ERROR


# returns true or false whether a collides with b
def checkCollision(a, b):
    rect1 = a
    rect2 = b

    if (rect1.x <= rect2.x + rect2.width and rect1.x + rect1.width >= rect2.x and rect1.y <= rect2.y + rect2.height and rect1.y + rect1.height >= rect2.y):
        return True

    return False
