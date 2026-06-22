# 🚀 APEX Studio v2.0 - Local AI Workspace

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

## 🛠️ How to Setup & Run

1. Download and install [Ollama](https://ollama.com).
2. Open your system's terminal application and run the bulk download command that matches your Operating System to install the 10-model matrix:

### 🪟 For Windows Users

* **If using PowerShell (Recommended default):**
    ```powershell
    ollama pull qwen2.5-coder:3b; ollama pull qwen2.5-coder:7b; ollama pull deepseek-r1:7b; ollama pull qwen2.5-coder:1.5b; ollama pull qwen2.5-coder:0.5b; ollama pull llama3.1:8b; ollama pull mistral:7b; ollama pull phi3:3.8b; ollama pull gemma2:2b; ollama pull codellama:7b
    ```
* **If using Command Prompt (Legacy CMD):**
    ```cmd
    ollama pull qwen2.5-coder:3b && ollama pull qwen2.5-coder:7b && ollama pull deepseek-r1:7b && ollama pull qwen2.5-coder:1.5b && ollama pull qwen2.5-coder:0.5b && ollama pull llama3.1:8b && ollama pull mistral:7b && ollama pull phi3:3.8b && ollama pull gemma2:2b && ollama pull codellama:7b
    ```

### 🍎 For macOS & 🐧 Linux Users
Mac and Linux systems use a Bash/Zsh terminal environment. They chain commands using a single semicolon space wrapper:

```bash
ollama pull qwen2.5-coder:3b; ollama pull qwen2.5-coder:7b; ollama pull deepseek-r1:7b; ollama pull qwen2.5-coder:1.5b; ollama pull qwen2.5-coder:0.5b; ollama pull llama3.1:8b; ollama pull mistral:7b; ollama pull phi3:3.8b; ollama pull gemma2:2b; ollama pull codellama:7b
