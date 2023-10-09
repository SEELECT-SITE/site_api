# imports
import random
import time

# Setting time as seed.
random.seed(time.time())

# Function to generate a random and unique hash.
def generateRandomHash(size=128):
    # Getting a random integer with size equal to 128 bits
    hash = random.getrandbits(size)
    # Converting this number to hexadecimal
    hash = '%032x' % hash

    return hash