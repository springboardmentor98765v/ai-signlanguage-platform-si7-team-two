import random

LETTERS = [
    'A','B','C','D','E','F','G','H',
    'I','J','K','L','M','N','O','P',
    'Q','R','S','T','U','V','W','X',
    'Y','Z'
]

def get_random_letter():
    return random.choice(LETTERS)
if __name__ == "__main__":

    for _ in range(10):
        print(get_random_letter())