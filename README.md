
# U-Bot Pro | Elite IUDE (Standalone)

U-Bot Pro is a fully offline, hardware-accelerated, and completely unrestricted AI assistant. Built as a portable Windows application, it requires **no installation, no internet connection, and zero external dependencies** to run. 

Everything needed to chat, process code, and analyze data is bundled locally inside a single folder.

## Features
* **100% Offline & Portable:** The AI engine, Python environment, and UI are bundled into a single folder. Put it on a USB and run it on any Windows machine.
* **Unrestricted Persona:** Built-in system overrides to bypass standard AI safety filters for raw, technical, and uncensored responses.
* **Hardware Acceleration:** Auto-detects NVIDIA GPUs (optimized for 4GB VRAM cards like the GTX 1650) for lightning-fast text generation. Automatically falls back to CPU if no GPU is found.
* **Smart Code Parsing:** Automatically detects Markdown code blocks, applies syntax highlighting, and provides one-click "Copy Code" buttons.
* **Live System Monitoring:** Real-time, silent tracking of CPU, RAM, and NVIDIA GPU utilization directly in the header.
* **Voice Integration:** Built-in microphone support for dictating commands.
* **Session Management:** Save, load, or purge chat histories, or use "Temporary Chat" for zero-log sessions.

---

## System Requirements
* **OS:** Windows 10 / Windows 11
* **RAM:** 16GB Minimum (32GB Recommended for seamless multitasking)
* **GPU:** NVIDIA GPU highly recommended (e.g., GTX 1650 or better). 
* **Storage:** ~6GB+ free space (depending on the bundled `.gguf` model).

---

## How to Run (For Users)

If you downloaded the pre-compiled `.zip` release, you do not need to install Python or Ollama. 

1. Download the latest `U-Bot_Pro.zip` file from the Releases page.
2. **Extract the entire folder** to your PC (e.g., to your Desktop or Documents). 
3. Open the extracted `U-Bot` folder. Do **not** move the `.exe` out of this folder.
4. Double-click **`U-Bot.exe`**.
5. Wait for the Splash Screen to initialize the local server and load the AI into your RAM/VRAM (usually takes 5–15 seconds depending on your hardware).
6. Start chatting!

---

## How to Build from Source (For Developers)

If you are cloning this repository to build the executable yourself, follow these steps:

### 1. Prerequisites
* Python 3.11 installed.
* Run: `pip install customtkinter ollama PyAudio SpeechRecognition psutil pyperclip pyinstaller`
* Download the Windows version of `ollama.exe` and place it in the root project folder.

### 2. Prepare the Local Model
Because GitHub does not allow massive files, the AI model weights are not included in this repo.
1. Create a folder named `models` in the root directory.
2. Inside `models`, create two folders: `blobs` and `manifests`.
3. Download your preferred GGUF model (e.g., Dolphin-Llama3 or Phi-3) via Hugging Face or a local Ollama pull, and place the raw model data into the `blobs` and `manifests` folders.

### 3. Compile the Executable
Delete any existing `build` or `dist` folders, then run the following PyInstaller command in your terminal:

```powershell
python -m PyInstaller --noconfirm --onedir --windowed --collect-all customtkinter --collect-all psutil --add-data "ollama.exe;." --add-data "models;models" "U-Bot.py"

```

*(Note: You may need to manually point to your `customtkinter` site-packages directory in the `--add-data` flag depending on your specific Python environment).*

The final standalone application will be generated inside the `dist/U-Bot` folder.

---

## Disclaimer

The "Unrestricted" persona bypasses standard AI safety protocols. This tool is designed strictly for advanced users, cybersecurity research, and unrestricted creative writing in an isolated, offline environment. The user is solely responsible for how they utilize the generated output.
