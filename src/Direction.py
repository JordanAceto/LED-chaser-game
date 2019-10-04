class Direction():
    LEFT = 1
    RIGHT = -1

def opposite(direction):
    if (direction == Direction.RIGHT):
        return Direction.LEFT
    else:
        return Direction.RIGHT