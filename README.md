# U-Bot Pro: Unrestricted Local AI Chatbot

**U-Bot Pro** is a minimalist, high-performance AI chatbot interface built with Python and CustomTkinter. It leverages **Ollama** to run uncensored models like `dolphin-llama3` locally on your machine, ensuring total privacy and freedom from typical AI content restrictions.

## 🚀 Key Features

* **Unrestricted & Uncensored**: Built for use with "abliterated" models, allowing for responses without ethical or safety filters.
* **Privacy First**: Chat history is saved in your local `AppData` folder, keeping your private conversations out of your GitHub repositories.
* **Flicker-Free Theme Toggling**: Instant switching between Dark and Light modes using modern Tuple Color logic to prevent GUI lag or window closing.
* **Window-in-Window Code Blocks**: Automatically detects code and presents it in a dedicated "Code Box" with a one-click copy button.
* **Intelligent History Management**: Each session is automatically saved with a unique ID; sessions can be reloaded, continued, or deleted via the sidebar.
* **Personalized Experience**: Automatically greets you by your Windows username upon launch.

---

## 🛠️ Prerequisites

* **Ollama**: [Download here](https://ollama.com).
* **Python 3.10+**: [Download here](https://www.python.org/).
* **Uncensored Model**:
```bash
ollama run dolphin-llama3

```



---

## 📦 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/YourUsername/U-Bot-Unrestricted_ChatBot.git
cd U-Bot-Unrestricted_ChatBot

```


2. **Install dependencies**:
Ensure you install them for your specific Python executable:
```bash
python -m pip install customtkinter ollama pyperclip

```



---

## 🚦 Usage

1. Ensure **Ollama** is running in the background.
2. Run the application:
```bash
python U-Bot.py

```


3. **Toggle Theme**: Use the sidebar button to switch modes without flickering.
4. **Request Code**: Type keywords like `python` or `script` to trigger the special Code Box rendering.

---

## 💻 Hardware Optimization (For Ryzen APUs)

For users with hardware like the **Ryzen 7 5700G**, performance can be boosted by:

* **Increasing VRAM**: Set your BIOS "UMA Frame Buffer" to 8GB or higher.
* **Environment Variables**: Set `OLLAMA_VULKAN=1` in Windows to force GPU acceleration.
* **RAM Management**: Close high-resource apps like browsers while the AI is thinking.

---

## 📝 License

This project is open-source. Use responsibly. By using local uncensored models, you assume full responsibility for the output generated.

---
