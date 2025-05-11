import random
import time
import winsound

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

# User settings
BPM = 260
FREQUENCY = 1000

# Timing calculations
beat_duration = 60 / BPM
DOT_DURATION = int(beat_duration * 1000)
DASH_DURATION = DOT_DURATION * 3


def play_morse(morse_code):
    for symbol in morse_code:
        if symbol == '.':
            winsound.Beep(FREQUENCY, DOT_DURATION)
        elif symbol == '-':
            winsound.Beep(FREQUENCY, DASH_DURATION)
        elif symbol == ' ':
            time.sleep(DOT_DURATION * 3 / 1000.0)
        time.sleep(DOT_DURATION / 1000.0)


def generate_and_play(chars, lines=1, chars_per_line=5):
    for line in range(lines):
        random_chars = random.choices(chars, k=chars_per_line)
        print(f"\nLine {line + 1}: Listen carefully...")

        for char in random_chars:
            morse = MORSE_CODE_DICT[char]
            play_morse(morse)
            time.sleep(DOT_DURATION * 3 / 1000.0)

        answer = input("Do you want to see the results? (yes/no): ").strip().lower()
        if answer in ["yes", "y"]:
            print(f"Characters: {' '.join(random_chars)}")
            for char in random_chars:
                print(f"{char}: {MORSE_CODE_DICT[char]}")
        else:
            print("Moving to next line...")


def part1():
    chars = list('ADIK')
    generate_and_play(chars)


def part2():
    chars = list('BCEF')
    generate_and_play(chars)


def user_input():
    print("\t 1 - Part_1 \n"
          "\t 2 - Part_2 \n")

    choice = input("Enter function name : ").strip().lower()

    match choice:
        case "1":
            part1()
        case "2":
            part2()
        case _:
            print("Unknown option. Try again.")


# Start program
if __name__ == "__main__":
    user_input()
