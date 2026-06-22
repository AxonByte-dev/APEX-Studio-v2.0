# 🚀 APEX Studio v2.0 - Local AI Workspace
> 🧠 **Developer Note:** Created by an 11-year-old developer.
🐛 *If you find any bugs or have ideas for improvements, please report them in the Issues tab!*
An advanced, premium desktop dashboard designed to orchestrate and interface with multiple local Large Language Models (LLMs) completely offline. Built from scratch to bypass expensive cloud API keys and put a mini-data center right on your desk.

---

## 🖥️ System Requirements (READ BEFORE RUNNING)
Running AI models locally requires modern computer architecture. Please check your specs to ensure a smooth experience:

* **Absolute Minimum (To prevent system crashes):**
    * **CPU:** 64-bit Intel or AMD processor with **AVX2 instruction support** (No ancient Pentium/Celeron chips).
    * **System RAM:** 8 GB Minimum.
    * **Storage:** 15 GB+ of free space (SSD strongly recommended; old mechanical HDDs will load models very slowly).
* **Recommended (For smooth speed):**
    * **Processor:** Modern 6+ Core CPU (Intel Core i5/Ryzen 5 or newer).
    * **System RAM:** 16 GB RAM.
    * **Graphics Card (GPU):** Dedicated NVIDIA or AMD GPU with **6 GB+ VRAM** (e.g., RTX 3060, RTX 4050).
    * *Note: If your system has less than 6GB VRAM, Ollama will automatically split the larger 7B models onto your System RAM, which will run significantly slower.*

---

## ⚡ The 10-Model Matrix
This workspace is dynamically built to hook into Ollama's local engine, managing a specialized squad of digital brains tailored for specific tasks:
* **The Coding Experts:** `qwen2.5-coder` (0.5b, 1.5b, 3b, 7b) & `codellama:7b`
* **The Deep Thinker:** `deepseek-r1:7b` (Local Advanced Reasoning)
* **The Logic Heavyweights:** `llama3.1:8b` & `mistral:7b`
* **The VRAM Sweet-Spots:** `phi3:3.8b` & `gemma2:2b`

---

## 🛠️ How to Setup & Run

### Step 1: Install Ollama & Pull the Models
1. Download and install [Ollama](https://ollama.com) for your operating system.
2. Open your terminal application and run the bulk download command that matches your computer to pull the 10-model matrix:

#### 🪟 For Windows Users (PowerShell)
```powershell
ollama pull qwen2.5-coder:3b; ollama pull qwen2.5-coder:7b; ollama pull deepseek-r1:7b; ollama pull qwen2.5-coder:1.5b; ollama pull qwen2.5-coder:0.5b; ollama pull llama3.1:8b; ollama pull mistral:7b; ollama pull phi3:3.8b; ollama pull gemma2:2b; ollama pull codellama:7b
🪟 For Windows Users (Legacy CMD)
ollama pull qwen2.5-coder:3b && ollama pull qwen2.5-coder:7b && ollama pull deepseek-r1:7b && ollama pull qwen2.5-coder:1.5b && ollama pull qwen2.5-coder:0.5b && ollama pull llama3.1:8b && ollama pull mistral:7b && ollama pull phi3:3.8b && ollama pull gemma2:2b && ollama pull codellama:7b
🍎 For macOS & 🐧 Linux Users
ollama pull qwen2.5-coder:3b; ollama pull qwen2.5-coder:7b; ollama pull deepseek-r1:7b; ollama pull qwen2.5-coder:1.5b; ollama pull qwen2.5-coder:0.5b; ollama pull llama3.1:8b; ollama pull mistral:7b; ollama pull phi3:3.8b; ollama pull gemma2:2b; ollama pull codellama:7b

Step 2: Prepare Your System Environment
To let the app communicate safely with your local models across all platforms, execute the package setup matching your OS framework:
🪟 Windows Terminal:
python -m pip install requests
🍎 macOS / 🐧 Linux Terminal:
python3 -m pip install requests
(Make sure the Ollama desktop application is actively running in your system tray background so the local server is open!)

Step 3: Launch the APEX Studio Dashboard
Download this repository's source code files and extract the folder.

Open your terminal or command prompt inside the extracted project folder.

Launch your custom local AI environment by running:
🪟 Windows:
python apex_ai.py
🍎 macOS / 🐧 Linux:
python3 apex_ai.py

Your custom UI window will pop up. Select any downloaded model from your custom dropdown bar, type your query, and start generating completely local, secure AI responses!
