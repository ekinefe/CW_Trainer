import random
import time
import numpy as np
import simpleaudio as sa
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

def load_settings():
    try:
        with open("settings.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("No settings.json found. Creating default...")
        default = {"WPM": 20, "FREQUENCY": 1000, "LINES": 1, "CHARS_PER_LINE": 5}
        with open("settings.json", "w") as f:
            json.dump(default, f, indent=4)
        return default
    except json.JSONDecodeError:
        print("settings.json is invalid. Using default settings.")
        return {"WPM": 20, "FREQUENCY": 1000, "LINES": 1, "CHARS_PER_LINE": 5}

settings = load_settings()

WPM = settings.get("WPM", 20)
FREQUENCY = settings.get("FREQUENCY", 1000)
LINES = settings.get("LINES", 1)
CHARS_PER_LINE = settings.get("CHARS_PER_LINE", 5)

DOT_DURATION = int(1200 / WPM)
DASH_DURATION = DOT_DURATION * 3
INTRA_CHAR_SPACE = DOT_DURATION
INTER_CHAR_SPACE = DOT_DURATION * 3
WORD_SPACE = DOT_DURATION * 7

def play_tone(frequency, duration_ms):
    fs = 44100
    duration_s = duration_ms / 1000.0
    t = np.linspace(0, duration_s, int(fs * duration_s), False)
    wave = np.sin(frequency * t * 2 * np.pi)
    audio = (wave * 32767).astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, fs)
    play_obj.wait_done()

def play_morse(morse_code):
    for i, symbol in enumerate(morse_code):
        if symbol == '.':
            play_tone(FREQUENCY, DOT_DURATION)
        elif symbol == '-':
            play_tone(FREQUENCY, DASH_DURATION)
        if i < len(morse_code) - 1:
            time.sleep(INTRA_CHAR_SPACE / 1000.0)
    time.sleep(INTER_CHAR_SPACE / 1000.0)

def generate_and_play(chars):
    all_lines = []
    for line in range(LINES):
        random_chars = random.choices(chars, k=CHARS_PER_LINE)
        all_lines.append(random_chars)
        print(f"\\nLine {line + 1}: Playing...")
        for char in random_chars:
            morse = MORSE_CODE_DICT[char.upper()]
            play_morse(morse)
    answer = input("\\nPress Enter to see the results, or type anything to skip: ").strip().lower()
    if not answer:
        for index, line_chars in enumerate(all_lines):
            print(f"\\nLine {index + 1}: {' '.join(line_chars)}")
            for char in line_chars:
                print(f"{char}: {MORSE_CODE_DICT[char]}")
    else:
        print("Okay, results will not be shown.")
        user_input()
    answer2 = input("\\ndo you wanna do it again? (yes/no)\\t").strip().lower()
    if answer2 in ["yes", "y"]:
        user_input()
    elif answer2 in ["no", "n"]:
        exit(0)
    else:
        user_input()

def show_the_chars(chars):
    answer = input("\\nWould you like to see the chars first? (yes/no)\\t").strip().lower()
    if answer in ["yes", "y"]:
        for char in chars:
            morse = MORSE_CODE_DICT[char.upper()]
            print(f"{char}: {morse}")
            play_morse(morse)
        ready = input("\\nAre you ready to listen some random characters? (yes/no)\\t").strip().lower()
        if ready in ["yes", "y"]:
            time.sleep(1)
            generate_and_play(chars)
        else:
            user_input()
    elif answer in ["no", "n"]:
        generate_and_play(chars)
    else:
        print("Invalid input.")
        show_the_chars(chars)

def part1():
    chars = list('ADIK')
    show_the_chars(chars)

def part2():
    chars = list('MRUB')
    show_the_chars(chars)

def all_chars(include_numbers=True):
    chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    if include_numbers:
        chars += list('0123456789')
    show_the_chars(chars)

def custom_chars():
    user_input_str = input("Enter the characters you want to train with (A-Z, 0-9):\\n> ").upper()
    filtered = [c for c in user_input_str if c in MORSE_CODE_DICT]
    if not filtered:
        print("No valid characters entered. Try again.")
        user_input()
        return
    print(f"You selected: {' '.join(filtered)}")
    show_the_chars(filtered)

def user_input():
    print("\\t1 - Part_1\\n"
          "\\t2 - Part_2\\n"
          "\\t9 - Custom_Chars\\n"
          "\\t0 - All_Chars\\n")
    choice = input("Enter function number: ").strip()
    match choice:
        case "0":
            all_chars()
        case "1":
            part1()
        case "2":
            part2()
        case "9":
            custom_chars()
        case _:
            print("Unknown option. Try again.")
            user_input()

if __name__ == "__main__":
    print("\\n\\t  CW_Trainer"
          "\\n\\t      BY"
          "\\n\\tEkin Efe "
          "\\n\\t    V-1.9 (WINDOWS READY)\\n")
    user_input()