# ⚡ U-Bot Pro: Elite Unrestricted IUDE

**U-Bot Pro** is a high-performance, Integrated Unrestricted Development Environment (IUDE) designed for power users and researchers working with local Large Language Models. It provides a streamlined, glassmorphism-inspired interface for executing and managing AI-generated logic with zero safety filters.

## 🚀 Overview

U-Bot Pro bridges the gap between local LLMs and functional software development. It offers a secure environment to generate, test, and execute code instantly, featuring real-time system telemetry and an adaptive security engine.

## 🛠️ Key Features

* **Dual-Mode Persona Toggle**: Instant switching between `RESTRICTED` (Safety-first) and `UNRESTRICTED` (Zero-filter) system logic via a dedicated header pill.
* **Unified IUDE Interface**: A professional-grade dark theme featuring a collapsible navigation drawer for a focused workspace.
* **Integrated Python Sandbox**: Execute AI-generated code snippets in a secure local environment with real-time STDOUT/STDERR logging.
* **Live System Analytics**: Real-time monitoring of CPU and RAM usage to effectively manage local LLM resource consumption.
* **Void-Terminal**: A dedicated console for debugging, system logs, and background process tracking.

## 📦 Installation & Setup

### 1. Prerequisites

* **Python 3.11+**: Ensure Python is installed and added to your system PATH.
* **Ollama**: The backend engine required to run models locally.

### 2. Dependency Installation

Install the necessary Python libraries via terminal:

```bash
pip install customtkinter ollama pillow psutil pyperclip

```

### 3. Model Configuration

Pull the optimized **Dolphin-Llama3** model via Ollama:

```bash
ollama pull dolphin-llama3

```

## 🖥️ Usage Guide

1. **Initialize**: Ensure the Ollama service is active.
2. **Launch**: Run the main script: `python U-Bot.py`.
3. **Configure**: Use the top-right pill button to set your desired restriction level before sending commands.
4. **Execute**: Enter instructions in the pill-shaped input bar and monitor the terminal for output.

## 📂 Project Structure

* **`/chats`**: Persistent storage for session history.
* **`/bin`**: Secure vault for saved Python scripts and binaries.
* **`sys_config.json`**: Local configuration file for user preferences and persona settings.

## ⚠️ Disclaimer

U-Bot Pro is intended for research and development purposes. The "Unrestricted" mode bypasses standard AI safety filters. Users are solely responsible for ensuring that all generated content and executed code comply with local laws and ethical standards.

---

*Developed for the next generation of unrestricted AI interaction.*
