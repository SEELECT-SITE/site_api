# Imports
import random
import string

# Algorithm to generate random password
def generate_random_password(size=12):
    
    password = ''.join(random.choice(string.printable) for i in range(size))
    
    return password