# Imports
import random
import time

# Global variables
random.seed(time.time())

def generateRandomSalt(salt_size=10):
    random_salt = ''

    for i in range(salt_size):
        random_salt = random_salt + random_salt.join(chr(random.randint(32, 127)))

    return random_salt