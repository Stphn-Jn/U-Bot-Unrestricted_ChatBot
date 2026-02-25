# ⚡ **U-Bot Pro: Elite Unrestricted IUDE**

**U-Bot Pro** is a high-performance Integrated Unrestricted Development Environment (IUDE) designed for power users and researchers. It provides a streamlined, glassmorphism-inspired interface for executing AI-generated logic with zero safety filters and real-time hardware telemetry.

## 🚀 **Key Features**

* **Dual-Mode Persona Toggle**: Instant switching between **RESTRICTED** (Safe Mode - 🟢 Green) and **UNRESTRICTED** (Zero-filter - 🔴 Red).
* **Adaptive Chat Logic**: Intelligent behavior that prioritizes natural conversation unless code is explicitly requested.
* **Voice Interface (Mic)**: Hands-free interaction using integrated Speech-to-Text capabilities.
* **Temporary Chat (Incognito)**: A dedicated "Temp Mode" that prevents chat history from being saved to the local disk.
* **Ryzen Optimized Telemetry**: Real-time monitoring of CPU usage, RAM consumption, and Ryzen iGPU package temperatures.
* **Void-Terminal**: A dedicated console for debugging, system logs, and background process tracking.

---

## 🛠️ **Prerequisites & Installation**

### **1. System Requirements**

* **OS**: Windows 10/11 (Required for CustomTkinter UI scaling).
* **Python**: Version 3.11 or 3.12 (Must be added to System PATH).
* **Hardware**: 8GB RAM minimum; AMD Ryzen with iGPU supported for temperature tracking.

### **2. Software Dependencies**

Install the core engine and required Python libraries via your terminal:

```bash
# Core AI Engine
ollama pull dolphin-llama3

# Python Libraries
python -m pip install customtkinter ollama pillow psutil pyperclip WinTmp SpeechRecognition pyaudio

```

---

## 🚦 **Getting Started (First Steps)**

1. **Initialize Ollama**: Ensure the Ollama service is active in your system tray.
2. **Permissions**: If **Temperature Tracking** shows "N/A" or "Locked," run your Terminal or VS Code as **Administrator**.
3. **Launch**: Execute the main script:
```bash
python U-Bot.py

```


4. **Voice Activation**: Click the **🎙** icon to begin listening; the button will turn Red (⏳) while processing your voice.

---

## 🖥️ **Navigation Guide**

* **☰ (Drawer)**: Collapse the sidebar to maximize your workspace.
* **Purge All History**: Instantly delete all locally saved chat JSON files from the system.
* **Sessions Tab**: Click on any saved session to reload past conversations instantly.
* **Status Bar**: Located in the header, monitoring **CPU**, **RAM**, and **TEMP** to prevent hardware thermal throttling.

---

## ⚠️ **Legal Disclaimer & Responsible Use**

**By using this software, you agree to the following terms:**

1. **User Responsibility**: Any illegal, unethical, or harmful actions performed through this chatbot are the **sole responsibility of the user**.
2. **No Creator Liability**: The creator of U-Bot Pro is **not liable** for any misuse, data loss, or legal consequences resulting from this tool.
3. **Research Purpose**: This software is intended strictly for educational and security research purposes.

---

*Developed for the next generation of unrestricted AI interaction.*
