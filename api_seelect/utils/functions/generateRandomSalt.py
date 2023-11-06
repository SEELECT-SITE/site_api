# Imports
import random
import time

# Global variables
random.seed(time.time())

# Function which creates a random salt
def generate_random_salt(salt_size=10):
    random_salt = ''

    for i in range(salt_size):
        random_salt = random_salt + random_salt.join(chr(random.randint(40, 127)))
        
    return random_salt