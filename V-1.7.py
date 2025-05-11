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

# === GLOBAL SETTINGS ===
BPM = 260               # Beats per minute
FREQUENCY = 1000        # Frequency in Hz for beep sound
LINES = 1               # Number of lines of Morse code
CHARS_PER_LINE = 5      # Characters per line

# Timing calculations based on BPM
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


def generate_and_play(chars):
    all_lines = []

    for line in range(LINES):
        random_chars = random.choices(chars, k=CHARS_PER_LINE)
        all_lines.append(random_chars)
        print(f"\nLine {line + 1}: Playing...")

        for char in random_chars:
            morse = MORSE_CODE_DICT[char]
            play_morse(morse)
            time.sleep(DOT_DURATION * 3 / 1000.0)

    #    # Ask once after all lines are played
    answer = input("\nPress Enter to see the results, or type anything to skip: ").strip().lower()
    if not answer:  # If user presses Enter without typing anything
        for index, line_chars in enumerate(all_lines):
            print(f"\nLine {index + 1}: {' '.join(line_chars)}")
            for char in line_chars:
                print(f"{char}: {MORSE_CODE_DICT[char]}")
    else:
        print("Okay, results will not be shown.")



def part1():
    chars = list('ADIK')
    generate_and_play(chars)


def part2():
    chars = list('BCEF')
    generate_and_play(chars)


def user_input():
    print("\t1 - Part_1\n"
          "\t2 - Part_2\n")

    choice = input("Enter function number: ").strip().lower()

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
