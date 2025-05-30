# 🪟 How to Compile CW_Trainer to an EXE on Windows

This guide will walk you through creating a standalone `.exe` file from your Python-based CW Trainer project using `PyInstaller`.

---

## ✅ Step 1: Install PyInstaller

Make sure your virtual environment is activated, then run:

```bash
pip install pyinstaller
```

---

## ✅ Step 2: Compile the Python Script

From your project directory, run:

```bash
pyinstaller --onefile V-1.9-linux.py
```

This will create a `dist/` folder with the file:

```
dist/V-1.9-linux.exe
```

You can rename this file if you'd like.

---

## ✅ Step 3: Include settings.json

Make sure to copy your `settings.json` into the same folder as the `.exe`:

```
dist/
├── V-1.9-linux.exe
└── settings.json
```

---

## 🔁 Optional: Create a Custom Icon

If you want a custom icon, prepare a `.ico` file and add:

```bash
pyinstaller --onefile --icon=youricon.ico V-1.9-linux.py
```

---

## 🧼 Step 4: Clean Up (Optional)

PyInstaller leaves behind build files you can delete:

```bash
rmdir /s /q build
del /q *.spec
```

---

## 💡 Tip

You can also write a batch file to automate the build:
```bat
@echo off
pip install pyinstaller
pyinstaller --onefile V-1.9-linux.py
pause
```

Save it as `build.bat`.

---

Enjoy your standalone CW Trainer EXE on Windows! 🎉
