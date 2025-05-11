import random
import time
from time import sleep

import winsound
import json

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.',
    'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..',
    'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.'
}

# === GLOBAL SETTINGS ===
BPM = 260               # Beats per minute
FREQUENCY = 1000        # Frequency in Hz for beep sound
LINES = 1               # Number of lines of Morse code
CHARS_PER_LINE = 5      # Characters per line

# Timing calculations based on BPM
beat_duration = 60 / BPM
DOT_DURATION = int(beat_duration * 1000)
DASH_DURATION = DOT_DURATION * 3

# Function to load settings from the JSON file
def load_settings():
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
            return settings
    except FileNotFoundError:
        print("No settings.json found. Creating default...")
        default = {"BPM": 260, "FREQUENCY": 1000, "LINES": 1, "CHARS_PER_LINE": 5}
        with open("settings.json", "w") as f:
            json.dump(default, f, indent=4)
        return default
    except json.JSONDecodeError:
        print("settings.json is invalid. Using default settings.")
        return {}


# Applying settings from the loaded JSON file
settings = load_settings()

if settings:
    BPM = settings.get("BPM", BPM)
    FREQUENCY = settings.get("FREQUENCY", FREQUENCY)
    LINES = settings.get("LINES", LINES)
    CHARS_PER_LINE = settings.get("CHARS_PER_LINE", CHARS_PER_LINE)

# Function to play Morse code
def play_morse(morse_code):
    for symbol in morse_code:
        if symbol == '.':
            winsound.Beep(FREQUENCY, DOT_DURATION)
        elif symbol == '-':
            winsound.Beep(FREQUENCY, DASH_DURATION)
        elif symbol == ' ':
            time.sleep(DOT_DURATION * 3 / 1000.0)
        time.sleep(DOT_DURATION / 1000.0)

# Function to generate random characters and play their Morse code
def generate_and_play(chars):
    all_lines = []

    for line in range(LINES):
        random_chars = random.choices(chars, k=CHARS_PER_LINE)
        all_lines.append(random_chars)
        print(f"\nLine {line + 1}: Playing...")

        for char in random_chars:
            morse = MORSE_CODE_DICT[char.upper()]
            play_morse(morse)
            time.sleep(DOT_DURATION * 3 / 1000.0)

    # Ask to show results
    answer = input("\nPress Enter to see the results, or type anything to skip: ").strip().lower()
    if not answer:  # If user presses Enter without typing anything
        for index, line_chars in enumerate(all_lines):
            print(f"\nLine {index + 1}: {' '.join(line_chars)}")
            for char in line_chars:
                print(f"{char}: {MORSE_CODE_DICT[char]}")

    answer2 = input("\ndo you wanna do it again?")

    if answer2 in ["yes", "y", "Yes", "YES", "Y"]:
        user_input()
    if answer2 in ["no", "n", "No", "NO", "N"]:
        exit(0)

    else:
        print("Okay, results will not be shown.")

def show_the_chars (chars):
    answer = input("\nWould you like to see the chars first? (yes/no)")

    if answer in ["yes", "y", "Yes", "YES", "Y"]:
        for char in chars:
            morse = MORSE_CODE_DICT[char.upper()]
            print(f"{char}: {morse}")
            play_morse(morse)
            time.sleep(DOT_DURATION * 3 / 1000.0)

        answer2 = input("\nAre you ready to listen some random characters?")

        if answer2 in ["yes", "y", "Yes", "YES", "Y"]:
            time.sleep(2)
            generate_and_play(chars)
        if answer2 in ["no", "n", "No", "NO", "N"]:
            user_input()

    if answer in ["no", "n", "No", "NO", "N"]:
        generate_and_play(chars)
    else:
        print("you answer is n ot valid!!!")
        show_the_chars()


# Functions for parts 1 and 2
def part1():
    chars = list('ADIK')
    show_the_chars(chars)

def part2():
    chars = list('BCEF')
    show_the_chars(chars)

def all_chars(include_numbers=True):
    chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    if include_numbers:
         chars += list('0123456789')
    show_the_chars(chars)

# User input function
def user_input():
    print("\t1 - Part_1\n"
          "\t2 - Part_2\n"
          "\t0 - All_Chars\n")

    choice = input("Enter function number: ").strip().lower()

    match choice:
        case "0":
            all_chars()
        case "1":
            part1()
        case "2":
            part2()
        case _:
            print("Unknown option. Try again.")

# Start program
if __name__ == "__main__":
    user_input()
