import random
import time
from time import sleep

import winsound
import json

# Morse kodu sözlüğü
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

# === GLOBAL AYARLAR ===
# Artık BPM yerine doğrudan WPM kullanacağız:
WPM = 15             # Örneğin başlangıç değeri 20 WPM
FREQUENCY = 1000     # Beep frekansı (Hz)
LINES = 1            # Kaç satır rastgele karakter
CHARS_PER_LINE = 5   # Her satırda kaç karakter

# Dot süresi (ms) => 1200 / WPM
DOT_DURATION = int(1200 / WPM)
DASH_DURATION = DOT_DURATION * 3

# JSON dosyasından ayarları yükleyen fonksiyon
def load_settings():
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
            return settings
    except FileNotFoundError:
        print("No settings.json found. Creating default...")
        default = {"WPM": 20, "FREQUENCY": 1000, "LINES": 1, "CHARS_PER_LINE": 5}
        with open("settings.json", "w") as f:
            json.dump(default, f, indent=4)
        return default
    except json.JSONDecodeError:
        print("settings.json is invalid. Using default settings.")
        return {}

# JSON’dan yükleyip global değişkenleri güncelle
settings = load_settings()
if settings:
    WPM = settings.get("WPM", WPM)
    FREQUENCY = settings.get("FREQUENCY", FREQUENCY)
    LINES = settings.get("LINES", LINES)
    CHARS_PER_LINE = settings.get("CHARS_PER_LINE", CHARS_PER_LINE)

# Yükledikten sonra DOT_DURATION ve DASH_DURATION’ı yeniden hesaplıyoruz
DOT_DURATION = int(1200 / WPM)
DASH_DURATION = DOT_DURATION * 3

# Morse çalma fonksiyonu
def play_morse(morse_code):
    for symbol in morse_code:
        if symbol == '.':
            winsound.Beep(FREQUENCY, DOT_DURATION)
        elif symbol == '-':
            winsound.Beep(FREQUENCY, DASH_DURATION)
        elif symbol == ' ':
            time.sleep((DOT_DURATION * 3) / 1000.0)
        # Sembol arası boşluk
        time.sleep(DOT_DURATION / 1000.0)

# Rastgele karakter üretip çalma
def generate_and_play(chars):
    all_lines = []

    for line in range(LINES):
        random_chars = random.choices(chars, k=CHARS_PER_LINE)
        all_lines.append(random_chars)
        print(f"\nLine {line + 1}: Playing...")

        for char in random_chars:
            morse = MORSE_CODE_DICT[char.upper()]
            play_morse(morse)
            # Her karakter arası boşluk (3 dot süresi)
            time.sleep((DOT_DURATION * 3) / 1000.0)

    # Sonuçları gösterme sorusu
    answer = input("\nPress Enter to see the results, or type anything to skip: ").strip().lower()
    if not answer:  # Eğer sadece Enter’a basıldıysa
        for index, line_chars in enumerate(all_lines):
            print(f"\nLine {index + 1}: {' '.join(line_chars)}")
            for c in line_chars:
                print(f"{c}: {MORSE_CODE_DICT[c.upper()]}")
    else:
        print("Okay, results will not be shown.")
        user_input()

    # Yeniden oyna sorusu
    answer2 = input("\ndo you wanna do it again? (yes/no)\t")

    if answer2.lower() in ["yes", "y"]:
        user_input()
    elif answer2.lower() in ["no", "n"]:
        exit(0)
    else:
        user_input()

# Harfleri gösterip sonra çalma fonksiyonu
def show_the_chars(chars):
    answer = input("\nWould you like to see the chars first? (yes/no)\t")

    if answer.lower() in ["yes", "y"]:
        for char in chars:
            morse = MORSE_CODE_DICT[char.upper()]
            print(f"{char}: {morse}")
            play_morse(morse)
            time.sleep((DOT_DURATION * 3) / 1000.0)

        answer2 = input("\nAre you ready to listen some random characters? (yes/no)\t")
        if answer2.lower() in ["yes", "y"]:
            time.sleep(2)
            generate_and_play(chars)
        else:
            user_input()

    elif answer.lower() in ["no", "n"]:
        generate_and_play(chars)
    else:
        print("Your answer is not valid!")
        show_the_chars(chars)

# Bölümler
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

# Kullanıcı girişi
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
            user_input()

if __name__ == "__main__":
    print("\n\t  CW_Trainer"
          "\n\t      BY"
          "\n\tEkin Efe "
          "\n\t    V-1.8\n\n")
    user_input()
