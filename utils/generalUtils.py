import random
import string

class GeneralUtils:
    def __init__(self):
        self.data = ''

    def randToken(self, length):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string