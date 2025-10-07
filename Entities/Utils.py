import os

WAKE_UP_HOUR = 6
BED_TIME = 22
SEPARATOR_LENGTH = 50

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title(text):
    print("=" * SEPARATOR_LENGTH)
    print(text.center(SEPARATOR_LENGTH))
    print("=" * SEPARATOR_LENGTH)

def print_separator():
    print("-" * SEPARATOR_LENGTH)