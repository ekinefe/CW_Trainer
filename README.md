# CW_TRAINER BY EKIN EFE GUNGOR

This Python project generates random characters (letters and/or numbers), converts them into Morse code, and plays them as audio beeps.

---

## 📦 Versions

### 🟢 Version A: Basic Random Morse Code (No Sound)
A simple version that prints random characters and their Morse code equivalents to the console.

**File:** `morse_basic.py`

**Features:**
- Generates a random sequence of letters (and numbers optionally).
- Displays the Morse code for each character.

---

### 🟡 Version B: Windows Sound Version using `winsound`
Plays Morse code using system beeps (Windows only).

**File:** `morse_windows_sound.py`

**Requirements:**
- Windows OS
- Python standard `winsound` module (no extra installation)

**Features:**
- Random Morse code generation
- Audio playback with:
  - Configurable **frequency (Hz)**
  - Configurable **BPM (speed)**

**To Configure:**
```python
BPM = 120         # Adjusts playback speed
FREQUENCY = 700   # Tone frequency in Hz
