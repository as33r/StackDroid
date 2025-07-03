# 📦 StackDroid

**StackDroid** is a Python-based CLI tool to analyze Android APK files and detect the underlying **tech stacks** and **frameworks** used (e.g., Flutter, Unity, React Native, Cordova, Kotlin, Firebase, etc.).

It uses [`apktool`](https://github.com/iBotPeaches/Apktool) to decompile APKs and scans file names, paths, and contents for known tech signatures.

---

## 🚀 Features

- Detects Android frameworks: Flutter, Unity, React Native, Cordova, Capacitor, Xamarin, etc.
- Uses signature-based matching via customizable JSON config.
---

## 📦 Installation

> Requires: Python 3.6+, `apktool` in your system path.

```bash
git clone https://github.com/as33r/stackdroid.git
```

Make sure apktool is installed and available globally:
``` bash
sudo apt install apktool    # Debian/Ubuntu
```
## 🛠 Usage
```
python stackdroid.py <apk_path> [options]

📋 Options
Option	Description
-o, --output	Output directory for apktool decompilation (default: /tmp/decompiled_apk)
-s, --signatures	JSON file containing tech stack signatures (default: tech_stacks.json)
-v, --verbose	Show exact file paths and line numbers for matched signatures
```
🧪 Example
```
python stackdroid.py sample_game.apk -v
Expected output:

[*] Loading tech stack signatures...
[*] Running apktool to decompile the APK...
[*] Detecting tech stacks used in the APK...

[MATCH:PATH] Flutter ← 'flutter_assets' matched in path: /tmp/decompiled_apk/assets/flutter_assets
[MATCH:CONTENT] Firebase ← 'firebase-config' found in /tmp/decompiled_apk/AndroidManifest.xml:45

[+] Detected Tech Stacks:
  🔹 Flutter
  🔹 Firebase

[✓] Cleaned up: removed temporary directory '/tmp/decompiled_apk'
```

## 📚 Customizing Tech Stack Signatures

You can edit tech_stacks.json to add, update, or remove tech signatures.

Example format:
``` json
{
  "Flutter": ["libflutter.so", "flutter_assets", "dart:core"],
  "Unity": ["libunity.so", "UnityPlayerActivity", "com/unity3d/player"]
}
```
