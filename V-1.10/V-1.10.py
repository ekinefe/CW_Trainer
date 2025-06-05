import random
import time
import json
import sys
import os

# =============================================================================
#  1) Load or create settings.json
# =============================================================================
def load_settings():
    """
    Attempt to load settings from 'settings.json' in the current directory.
    If the file does not exist, create it with default values.
    If it exists but contains invalid JSON, overwrite it with defaults.
    Returns a dict with keys: WPM, FREQUENCY, LINES, CHARS_PER_LINE.
    """
    default = {
        "WPM": 20,
        "FREQUENCY": 1000,
        "LINES": 1,
        "CHARS_PER_LINE": 5
    }

    settings_path = os.path.join(os.getcwd(), "settings.json")

    # If settings.json is missing, create it with defaults
    if not os.path.isfile(settings_path):
        print("settings.json not found. Creating with default values...")
        with open(settings_path, "w") as f:
            json.dump(default, f, indent=4)
        return default

    # If it exists, try to load it
    try:
        with open(settings_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, PermissionError):
        # Malformed JSON (or cannot read). Overwrite with defaults.
        print("settings.json is invalid or unreadable. Overwriting with default values...")
        with open(settings_path, "w") as f:
            json.dump(default, f, indent=4)
        return default

    # If loaded successfully, ensure all keys are present; otherwise fill in defaults
    for key, val in default.items():
        if key not in data or not isinstance(data[key], int):
            data[key] = val

    # Save back any missing keys (so user sees all four in the file)
    with open(settings_path, "w") as f:
        json.dump(data, f, indent=4)

    return data


settings = load_settings()
WPM = settings["WPM"]
FREQUENCY = settings["FREQUENCY"]
LINES = settings["LINES"]
CHARS_PER_LINE = settings["CHARS_PER_LINE"]


# =============================================================================
#  2) Define Morse‐code dictionary & timing constants
# =============================================================================

MORSE_CODE_DICT = {
    "A": ".-",   "B": "-...", "C": "-.-.",
    "D": "-..",  "E": ".",    "F": "..-.",
    "G": "--.",  "H": "....", "I": "..",
    "J": ".---", "K": "-.-",  "L": ".-..",
    "M": "--",   "N": "-.",   "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...",  "T": "-",    "U": "..-",
    "V": "...-", "W": ".--",  "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----","1": ".----","2": "..---",
    "3": "...--","4": "....-","5": ".....",
    "6": "-....","7": "--...","8": "---..",
    "9": "----."
}

# Dot duration in milliseconds: 1200 / WPM
DOT_DURATION = int(1200 / WPM)
DASH_DURATION = DOT_DURATION * 3
INTRA_CHAR_SPACE = DOT_DURATION         # gap between symbols (dot/dash)
INTER_CHAR_SPACE = DOT_DURATION * 3     # gap between letters
WORD_SPACE = DOT_DURATION * 7           # (not used in single‐letter training, but here for reference)


# =============================================================================
#  3) Audio output: winsound on Windows, simpleaudio elsewhere
# =============================================================================

if sys.platform.startswith("win"):
    import winsound

    def play_tone(frequency, duration_ms):
        """
        On Windows, use winsound.Beep. Blocks until the beep is done.
        """
        winsound.Beep(int(frequency), int(duration_ms))

else:
    # Non‐Windows: try to import simpleaudio + numpy
    try:
        import numpy as np
        import simpleaudio as sa

        def play_tone(frequency, duration_ms):
            """
            Generate a sine‐wave tone with simpleaudio + numpy.
            """
            fs = 44100
            duration_s = duration_ms / 1000.0
            t = np.linspace(0, duration_s, int(fs * duration_s), False)
            wave = np.sin(frequency * t * 2 * np.pi)
            audio = (wave * 32767).astype(np.int16)
            play_obj = sa.play_buffer(audio, 1, 2, fs)
            play_obj.wait_done()

    except ImportError:
        print()
        print("ERROR: On non‐Windows platforms you must install 'simpleaudio' and 'numpy' to play tones.")
        print("Run:")
        print("    pip install simpleaudio numpy")
        print()
        sys.exit(1)


# =============================================================================
#  4) Functions to play Morse and handle user interaction
# =============================================================================

def play_morse(letter_code: str):
    """
    Play a single letter in Morse (letter_code is a string of '.' and '-'),
    inserting the correct intra‐symbol and inter‐letter pauses.
    """
    for i, symbol in enumerate(letter_code):
        if symbol == ".":
            play_tone(FREQUENCY, DOT_DURATION)
        elif symbol == "-":
            play_tone(FREQUENCY, DASH_DURATION)

        # Pause between symbols in the same letter
        if i < len(letter_code) - 1:
            time.sleep(INTRA_CHAR_SPACE / 1000.0)

    # Pause between letters
    time.sleep(INTER_CHAR_SPACE / 1000.0)


def generate_and_play(chars):
    """
    Build `LINES` random strings of length `CHARS_PER_LINE` from `chars`,
    play each line’s letters in Morse, then optionally show the user what they were.
    """
    all_lines = []

    for line_idx in range(LINES):
        # Pick CHARS_PER_LINE random characters from `chars`
        random_chars = random.choices(chars, k=CHARS_PER_LINE)
        all_lines.append(random_chars)

        print(f"\nLine {line_idx + 1}: Playing...")
        for ch in random_chars:
            morse = MORSE_CODE_DICT[ch]
            play_morse(morse)

    # After playing all lines, ask if user wants to see the actual letters & codes
    answer = input("\nPress Enter to see the results, or type anything to skip: ").strip().lower()
    if not answer:
        for idx, line_chars in enumerate(all_lines):
            print(f"\nLine {idx + 1}: {' '.join(line_chars)}")
            for ch in line_chars:
                print(f"  {ch}: {MORSE_CODE_DICT[ch]}")
    else:
        print("Okay, results will not be shown.")

    # Ask if they want to repeat
    again = input("\nDo you want to do it again? (yes/no)\t").strip().lower()
    if again in ["yes", "y"]:
        user_input()
    else:
        print("Goodbye!")
        sys.exit(0)


def show_the_chars(chars):
    """
    First, optionally show the user all selected characters with their Morse codes
    (each code is played once). Then either proceed to random drills or back to menu.
    """
    answer = input("\nWould you like to see the chars first? (yes/no)\t").strip().lower()
    if answer in ["yes", "y"]:
        for ch in chars:
            code = MORSE_CODE_DICT[ch]
            print(f"{ch}: {code}")
            play_morse(code)

        ready = input("\nAre you ready to listen to random characters? (yes/no)\t").strip().lower()
        if ready in ["yes", "y"]:
            time.sleep(1)
            generate_and_play(chars)
        else:
            user_input()

    elif answer in ["no", "n"]:
        generate_and_play(chars)

    else:
        print("Invalid input. Please type 'yes' or 'no'.")
        show_the_chars(chars)


def part1():
    chars = list("ADIK")
    show_the_chars(chars)


def part2():
    chars = list("MRUB")
    show_the_chars(chars)


def all_chars():
    chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    show_the_chars(chars)


def custom_chars():
    """
    Prompt the user to type a sequence (e.g. 'ABC123'), filter out any
    invalid characters, and then launch the drill with only those.
    """
    user_input_str = input("Enter the characters you want to train with (A-Z, 0-9):\n> ").upper()
    filtered = [c for c in user_input_str if c in MORSE_CODE_DICT]
    if not filtered:
        print("No valid characters entered. Try again.\n")
        user_input()
        return

    print(f"You selected: {' '.join(filtered)}")
    show_the_chars(filtered)


def user_input():
    """
    Display the main menu; read the user’s choice; call the corresponding function.
    """
    print("\n\t1 - Part_1  (ADIK)")
    print("\t2 - Part_2  (MRUB)")
    print("\t9 - Custom_Chars")
    print("\t0 - All_Chars (A–Z, 0–9)\n")

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
            print("Unknown option. Try again.\n")
            user_input()


if __name__ == "__main__":
    print(
        "\n\t   CW_Trainer"
        "\n\t       BY"
        "\n\t Ekin Efe GUNGOR"
        "\n\t     V-1.10 "
        "\n\t (Config via JSON)\n"
    )
    user_input()
import random
import time
import json
import sys
import os

# =============================================================================
#  1) Load or create settings.json
# =============================================================================
def load_settings():
    """
    Attempt to load settings from 'settings.json' in the current directory.
    If the file does not exist, create it with default values.
    If it exists but contains invalid JSON, overwrite it with defaults.
    Returns a dict with keys: WPM, FREQUENCY, LINES, CHARS_PER_LINE.
    """
    default = {
        "WPM": 20,
        "FREQUENCY": 1000,
        "LINES": 1,
        "CHARS_PER_LINE": 5
    }

    settings_path = os.path.join(os.getcwd(), "settings.json")

    # If settings.json is missing, create it with defaults
    if not os.path.isfile(settings_path):
        print("settings.json not found. Creating with default values...")
        with open(settings_path, "w") as f:
            json.dump(default, f, indent=4)
        return default

    # If it exists, try to load it
    try:
        with open(settings_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, PermissionError):
        # Malformed JSON (or cannot read). Overwrite with defaults.
        print("settings.json is invalid or unreadable. Overwriting with default values...")
        with open(settings_path, "w") as f:
            json.dump(default, f, indent=4)
        return default

    # If loaded successfully, ensure all keys are present; otherwise fill in defaults
    for key, val in default.items():
        if key not in data or not isinstance(data[key], int):
            data[key] = val

    # Save back any missing keys (so user sees all four in the file)
    with open(settings_path, "w") as f:
        json.dump(data, f, indent=4)

    return data


settings = load_settings()
WPM = settings["WPM"]
FREQUENCY = settings["FREQUENCY"]
LINES = settings["LINES"]
CHARS_PER_LINE = settings["CHARS_PER_LINE"]


# =============================================================================
#  2) Define Morse‐code dictionary & timing constants
# =============================================================================

MORSE_CODE_DICT = {
    "A": ".-",   "B": "-...", "C": "-.-.",
    "D": "-..",  "E": ".",    "F": "..-.",
    "G": "--.",  "H": "....", "I": "..",
    "J": ".---", "K": "-.-",  "L": ".-..",
    "M": "--",   "N": "-.",   "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...",  "T": "-",    "U": "..-",
    "V": "...-", "W": ".--",  "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----","1": ".----","2": "..---",
    "3": "...--","4": "....-","5": ".....",
    "6": "-....","7": "--...","8": "---..",
    "9": "----."
}

# Dot duration in milliseconds: 1200 / WPM
UNIT = int (1200 / WPM)
DOT_DURATION = UNIT
DASH_DURATION = UNIT * 3
INTRA_CHAR_SPACE = UNIT         # gap between symbols (dot/dash)
INTER_CHAR_SPACE = UNIT * 3     # gap between letters
WORD_SPACE = UNIT * 7           # (not used in single‐letter training, but here for reference)


# =============================================================================
#  3) Audio output: winsound on Windows, simpleaudio elsewhere
# =============================================================================

if sys.platform.startswith("win"):
    import winsound

    def play_tone(frequency, duration_ms):
        """
        On Windows, use winsound.Beep. Blocks until the beep is done.
        """
        winsound.Beep(int(frequency), int(duration_ms))

else:
    # Non‐Windows: try to import simpleaudio + numpy
    try:
        import numpy as np
        import simpleaudio as sa

        def play_tone(frequency, duration_ms):
            """
            Generate a sine‐wave tone with simpleaudio + numpy.
            """
            fs = 44100
            duration_s = duration_ms / 1000.0
            t = np.linspace(0, duration_s, int(fs * duration_s), False)
            wave = np.sin(frequency * t * 2 * np.pi)
            audio = (wave * 32767).astype(np.int16)
            play_obj = sa.play_buffer(audio, 1, 2, fs)
            play_obj.wait_done()

    except ImportError:
        print()
        print("ERROR: On non‐Windows platforms you must install 'simpleaudio' and 'numpy' to play tones.")
        print("Run:")
        print("    pip install simpleaudio numpy")
        print()
        sys.exit(1)


# =============================================================================
#  4) Functions to play Morse and handle user interaction
# =============================================================================

def play_morse(letter_code: str):
    """
    Play a single letter in Morse (letter_code is a string of '.' and '-'),
    inserting the correct intra‐symbol and inter‐letter pauses.
    """
    for i, symbol in enumerate(letter_code):
        if symbol == ".":
            play_tone(FREQUENCY, DOT_DURATION)
        elif symbol == "-":
            play_tone(FREQUENCY, DASH_DURATION)

        # Pause between symbols in the same letter
        if i < len(letter_code) - 1:
            time.sleep(INTRA_CHAR_SPACE / 1000.0)

    # Pause between letters
    time.sleep(INTER_CHAR_SPACE / 1000.0)


def generate_and_play(chars):
    """
    Build `LINES` random strings of length `CHARS_PER_LINE` from `chars`,
    play each line’s letters in Morse, then optionally show the user what they were.
    """
    all_lines = []

    for line_idx in range(LINES):
        # Pick CHARS_PER_LINE random characters from `chars`
        random_chars = random.choices(chars, k=CHARS_PER_LINE)
        all_lines.append(random_chars)

        print(f"\nLine {line_idx + 1}: Playing...")
        for ch in random_chars:
            morse = MORSE_CODE_DICT[ch]
            play_morse(morse)

    # After playing all lines, ask if user wants to see the actual letters & codes
    answer = input("\nPress Enter to see the results, or type anything to skip: ").strip().lower()
    if not answer:
        for idx, line_chars in enumerate(all_lines):
            print(f"\nLine {idx + 1}: {' '.join(line_chars)}")
            for ch in line_chars:
                print(f"  {ch}: {MORSE_CODE_DICT[ch]}")
    else:
        print("Okay, results will not be shown.")

    # Ask if they want to repeat
    again = input("\nDo you want to do it again? (yes/no)\t").strip().lower()
    if again in ["yes", "y"]:
        user_input()
    else:
        print("Goodbye!")
        sys.exit(0)


def show_the_chars(chars):
    """
    First, optionally show the user all selected characters with their Morse codes
    (each code is played once). Then either proceed to random drills or back to menu.
    """
    answer = input("\nWould you like to see the chars first? (yes/no)\t").strip().lower()
    if answer in ["yes", "y"]:
        for ch in chars:
            code = MORSE_CODE_DICT[ch]
            print(f"{ch}: {code}")
            play_morse(code)

        ready = input("\nAre you ready to listen to random characters? (yes/no)\t").strip().lower()
        if ready in ["yes", "y"]:
            time.sleep(1)
            generate_and_play(chars)
        else:
            user_input()

    elif answer in ["no", "n"]:
        generate_and_play(chars)

    else:
        print("Invalid input. Please type 'yes' or 'no'.")
        show_the_chars(chars)


def part1():
    chars = list("ADIK")
    show_the_chars(chars)


def part2():
    chars = list("MRUB")
    show_the_chars(chars)


def all_chars():
    chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    show_the_chars(chars)


def custom_chars():
    """
    Prompt the user to type a sequence (e.g. 'ABC123'), filter out any
    invalid characters, and then launch the drill with only those.
    """
    user_input_str = input("Enter the characters you want to train with (A-Z, 0-9):\n> ").upper()
    filtered = [c for c in user_input_str if c in MORSE_CODE_DICT]
    if not filtered:
        print("No valid characters entered. Try again.\n")
        user_input()
        return

    print(f"You selected: {' '.join(filtered)}")
    show_the_chars(filtered)


def user_input():
    """
    Display the main menu; read the user’s choice; call the corresponding function.
    """
    print("\n\t1 - Part_1  (ADIK)")
    print("\t2 - Part_2  (MRUB)")
    print("\t9 - Custom_Chars")
    print("\t0 - All_Chars (A–Z, 0–9)\n")

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
            print("Unknown option. Try again.\n")
            user_input()


if __name__ == "__main__":
    print(
        "\n\t   CW_Trainer"
        "\n\t       BY"
        "\n\t Ekin Efe"
        "\n\t     V-1.10 "
        # "\n\t(Config via JSON)\n"
        "\n"
    )
    print(f"Settings:\n- WPM: {WPM}")
    user_input()
