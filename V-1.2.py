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

DOT_DURATION = 100  # milliseconds
DASH_DURATION = DOT_DURATION * 3
FREQUENCY = 800  # Hz


def play_morse(morse_code):
    for symbol in morse_code:
        if symbol == '.':
            winsound.Beep(FREQUENCY, DOT_DURATION)
        elif symbol == '-':
            winsound.Beep(FREQUENCY, DASH_DURATION)
        elif symbol == ' ':
            time.sleep(DOT_DURATION / 1000.0 * 3)
        time.sleep(DOT_DURATION / 1000.0)  # Pause between symbols


def generate_and_play_morse(length=5, include_numbers=True):
    # chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    chars = list('ADIK')
    # if include_numbers:
    #     chars += list('0123456789')

    random_chars = random.choices(chars, k=length)
    print("Random characters:", ' '.join(random_chars))
    print("Morse code:")

    for char in random_chars:
        morse = MORSE_CODE_DICT[char]
        print(f"{char}: {morse}")
        play_morse(morse)
        time.sleep(DOT_DURATION / 1000.0 * 3)  # Pause between letters


# Example
generate_and_play_morse(length=6, include_numbers=True)
