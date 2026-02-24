# ⚡ **U-Bot Pro: Elite Unrestricted IUDE**

**U-Bot Pro** is a professional-grade **Integrated Unrestricted Development Environment (IUDE)**. It is specifically designed for power users and researchers to interface with local Large Language Models (LLMs) with **zero safety filters** and maximum efficiency.

---

## ⚙️ **SYSTEM ARCHITECTURE**

The application operates on a **Client-Server architecture** powered by Python and the Ollama API:

* **THE ENGINE:** High-speed connection to the `dolphin-llama3` model via Ollama’s local host.
* **PERSONA OVERRIDE:** When toggled to **UNRESTRICTED**, the app injects a master system prompt that bypasses standard AI safety guardrails.
* **THE SANDBOX:** Automatically parses AI-generated code and allows for execution in a temporary local process with live output.

---

## 🛠️ **PREREQUISITES & INSTALLATION**

### **1. Hardware & OS Requirements**

* **Operating System:** Windows 10 or 11 (Required for modern **CustomTkinter** UI scaling).
* **RAM:** **8GB Minimum** (16GB+ highly recommended for smooth Llama3 inference).
* **Processor:** Quad-core CPU or better (Optimized for local AI workloads).

### **2. Core Software**

* **Python 3.11 or 3.12:** Must be installed and added to your **System PATH**.
* **Ollama:** Must be downloaded and installed from [ollama.com](https://ollama.com/).

### **3. Python Library Dependencies**

Open your terminal and run the following command to install the required environment:

```bash
pip install customtkinter ollama pillow psutil pyperclip

```

### **4. AI Model Setup**

Once Ollama is running, pull the unrestricted model weights:

```bash
ollama pull dolphin-llama3

```

---

## 🚦 **GETTING STARTED (FIRST STEPS)**

1. **LAUNCH OLLAMA:** Ensure the Ollama service is active in your system tray.
2. **NAVIGATE:** Open your command prompt/terminal and `cd` into the project folder.
3. **EXECUTE:** Launch the environment by running:
```bash
python U-Bot.py

```


4. **VERIFY:** The **Terminal Logs** on the right should display: `> System Initialized`.

---

## 🖥️ **INTERFACE NAVIGATION**

* **PERSONA TOGGLE:** The pill-shaped button in the top-right header.
* 🟢 **GREEN (UNRESTRICTED):** AI ignores all safety filters and rules.
* 🔴 **RED (RESTRICTED):** AI acts as a standard, filtered assistant.


* **DRAWER (☰):** Click the top-left icon to hide the sidebar for a focused coding workspace.
* **SANDBOX:** Click the **RUN** button on any generated code block to test it immediately.
* **SYSTEM STATS:** Monitor the right panel for real-time **CPU/RAM** tracking to prevent hardware thermal throttling.

---

## ⚠️ **LEGAL DISCLAIMER & RESPONSIBLE USE**

**BY USING THIS SOFTWARE, YOU AGREE TO THE FOLLOWING:**

1. **USER RESPONSIBILITY:** Any illegal, unethical, or harmful actions performed by the user through this chatbot or its generated code are the **sole responsibility of the user**.
2. **NO CREATOR LIABILITY:** The creator of U-Bot Pro is **NOT RESPONSIBLE** for any misuse, data loss, hardware damage, or legal consequences.
3. **PURPOSE:** This tool is provided strictly for **educational, security research, and developmental purposes**.
4. **ETHICAL USE:** Users must comply with all local and international laws. Do not use this tool for unauthorized hacking or malware creation.

---

*Built for the next generation of unrestricted AI interaction.*
