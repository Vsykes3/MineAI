import random

def detect_mob(image):
    possible_mobs = ["zombie", "creeper", "skeleton", None]
    return random.choice(possible_mobs)
