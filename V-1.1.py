import random

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


def generate_random_morse(length=5, include_numbers=True):
    # chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    chars = list('ADIK')
    # if include_numbers:
    #     chars += list('0123456789')

    random_chars = random.choices(chars, k=length)
    morse_sequence = [MORSE_CODE_DICT[c] for c in random_chars]

    print("Random characters:", ' '.join(random_chars))
    print("Morse code:", ' '.join(morse_sequence))


# Example usage
generate_random_morse(length=8, include_numbers=True)
