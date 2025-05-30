# 🪟 Windows'ta CW_Trainer'ı EXE Dosyasına Derleme Rehberi

Bu rehber, Python tabanlı CW Trainer projenizi bağımsız bir `.exe` dosyasına dönüştürme adımlarını içerir.

---

## ✅ Adım 1: PyInstaller Kurulumu

Öncelikle sanal ortamınızı (virtual environment) aktif hale getirin ve şu komutu çalıştırın:

```bash
pip install pyinstaller
```

---

## ✅ Adım 2: Python Dosyasını Derleme

Proje klasörünüzde şu komutu çalıştırın:

```bash
pyinstaller --onefile V-1.9-linux.py
```

Bu işlem sonucunda `dist/` adlı bir klasör oluşacak ve içinde şunu bulacaksınız:

```
dist/V-1.9-linux.exe
```

İsterseniz bu dosyanın adını değiştirebilirsiniz.

---

## ✅ Adım 3: settings.json Dosyasını Ekleyin

Oluşan `.exe` dosyasının bulunduğu klasöre `settings.json` dosyanızı da kopyalayın:

```
dist/
├── V-1.9-linux.exe
└── settings.json
```

---

## 🔁 Opsiyonel: Özel Simge (Icon) Kullanımı

Eğer özel bir simge kullanmak isterseniz, bir `.ico` dosyası hazırlayın ve komutu şu şekilde güncelleyin:

```bash
pyinstaller --onefile --icon=ikonunuz.ico V-1.9-linux.py
```

---

## 🧼 Adım 4: Temizlik (Opsiyonel)

PyInstaller bazı geçici dosyalar oluşturur. Bunları temizlemek için:

```bash
rmdir /s /q build
del /q *.spec
```

---

## 💡 İpucu: Otomatik Derleme için Batch Dosyası

Aşağıdaki gibi bir `.bat` dosyası hazırlayarak derleme işlemini otomatikleştirebilirsiniz:

```bat
@echo off
pip install pyinstaller
pyinstaller --onefile V-1.9-linux.py
pause
```

Bu dosyayı `build.bat` olarak kaydedin.

---

Artık CW Trainer'ınızı bağımsız bir EXE dosyası olarak Windows'ta kullanabilirsiniz! 🎉
