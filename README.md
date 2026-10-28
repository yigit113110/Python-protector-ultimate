# 🛡️ Advanced Python Polymorphic Obfuscator & Protector & Anti Vm

An advanced **Builder,Antivm,Encrypter** tool designed to protect your Python scripts against static/dynamic analysis, reverse engineering, and antivirus heuristic detections.

ANTIVIRUSES LIKE KASPERSKY THINKS THIS IS A VIRUS HOWEVER ITS NOT. IF U DONT TRUST U CAN RUN THIS IN A VIRTUAL MACHINE HOWEVER MIGHT NOT WORK
---
-- written with python 3.14
## 🚀 Key Features
* **I** used **ai** however its only like %40 ai, i only used it for creating a really powerfull obfuscator and encryptor

* **Polymorphism (`secrets`):** Randomizes all variable and function names on every build to eliminate static signatures.
* **Multi-Stage Encryption:** Combines Zlib compression, custom bit-shift/XOR matrices, and **AES-256-CBC** encryption.
* **Advanced Anti-VM & Anti-Debug:** 
  * Cursor telemetry and randomness verification.
  * Real-time running process scanning (`x64dbg`, `ida`, `wireshark`, etc.).
  * Virtual machine artifact (file path and driver) detection.
  * Sandbox time-acceleration (Anti-Emulation) checks.
* **In-Memory Execution:** The payload is decrypted and executed directly in memory without being written to disk in plain text.
* **Automatic Import Injection:** Automatically scans the target script for used modules and configures necessary dependencies.
* **Optional `.exe` Compilation:** Fully compatible with Python 3.14+, offering an optional standalone `.exe` export via PyInstaller.

---

## ⚙️ Requirements & Installation

Install the required Python libraries before running the project:

pip install cryptography psutil pyinstaller, pywin32,requests,threading,sounddevice etc... if you run the program as admin in a cmd u can see which error does python give
