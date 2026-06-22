import tkinter as tk
import customtkinter as ctk
import ollama
import threading
import json
import os

# --- Visual Theme Framework (Premium Minimalist Slate) ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue") 

HISTORY_FILE = "apex_history.json"

class ApexAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("APEX AI - Premium Workspace v2.0")
        self.geometry("1200x800")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Runtime Flags & Memory
        self.is_generating = False
        self.stop_signal = False
        
        self.chats = self.load_histories()
        self.active_chat_id = "Main Thread"
        if self.active_chat_id not in self.chats:
            self.chats[self.active_chat_id] = []

        self.model_options = [
            "qwen2.5-coder:3b",       
            "qwen2.5-coder:7b",       
            "deepseek-r1:7b",         
            "qwen2.5-coder:1.5b",     
            "qwen2.5-coder:0.5b",     
            "llama3.1:8b",            
            "mistral:7b",             
            "phi3:3.8b",              
            "gemma2:2b",              
            "codellama:7b"            
        ]

        self.init_ui()
        self.load_chat_into_view()

    def init_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- SIDEBAR MATRIX ----------------
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#1e1e24")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="APEX STUDIO", 
            font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"), 
            text_color="#f0f0f5"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 15))

        self.model_label = ctk.CTkLabel(
            self.sidebar, 
            text="COMPUTE ENGINE:", 
            font=ctk.CTkFont(size=10, weight="bold"), 
            text_color="#a0a0aa"
        )
        self.model_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.model_dropdown = ctk.CTkOptionMenu(
            self.sidebar, 
            values=self.model_options, 
            button_color="#3a3a44", 
            fg_color="#2b2b36"
        )
        self.model_dropdown.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="ew")
        self.model_dropdown.set("qwen2.5-coder:3b") 

        self.history_label = ctk.CTkLabel(
            self.sidebar, 
            text="RECENT CHATS:", 
            font=ctk.CTkFont(size=10, weight="bold"), 
            text_color="#a0a0aa"
        )
        self.history_label.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="w")

        self.listbox_frame = ctk.CTkFrame(self.sidebar, fg_color="#141417")
        self.listbox_frame.grid(row=4, column=0, padx=20, pady=5, sticky="nsew")
        self.listbox_frame.grid_columnconfigure(0, weight=1)
        self.listbox_frame.grid_rowconfigure(0, weight=1)

        self.chat_listbox = tk.Listbox(
            self.listbox_frame, 
            bg="#141417", 
            fg="#d1d1d6", 
            selectbackground="#3a3a44",
            selectforeground="white",
            bd=0, 
            highlightthickness=0, 
            exportselection=False,
            font=("Helvetica", 11)
        )
        self.chat_listbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.chat_listbox.bind("<<ListboxSelect>>", self.on_chat_selected)
        self.update_sidebar_list()

        self.new_chat_btn = ctk.CTkButton(
            self.sidebar, 
            text="+ New Session", 
            fg_color="#3a3a44", 
            hover_color="#4e4e5a", 
            text_color="white", 
            command=self.create_new_chat
        )
        self.new_chat_btn.grid(row=5, column=0, padx=20, pady=20)

        # ---------------- MAIN CONSOLE HUB ----------------
        self.main_container = ctk.CTkFrame(self, fg_color="#141416") 
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Text Console Box
        self.text_display = ctk.CTkTextbox(
            self.main_container, 
            font=("Helvetica", 13), 
            wrap="word", 
            fg_color="#1a1a1e", 
            text_color="#e4e4e7"
        )
        self.text_display.grid(row=0, column=0, sticky="nsew", padx=30, pady=(30, 10))
        self.text_display.configure(state="disabled")

        # Control Bar
        self.control_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.control_frame.grid(row=1, column=0, sticky="w", padx=30, pady=0)
        
        self.stop_btn = ctk.CTkButton(
            self.control_frame, 
            text="🛑 Stop", 
            width=80, 
            height=26, 
            fg_color="#7f1d1d", 
            hover_color="#991b1b", 
            text_color="#fca5a5", 
            command=self.stop_generation
        )
        self.stop_btn.grid(row=0, column=0, padx=(0, 10))
        self.stop_btn.grid_remove() 

        self.retry_btn = ctk.CTkButton(
            self.control_frame, 
            text="🔄 Retry Last Message", 
            width=140, 
            height=26, 
            fg_color="#27272a", 
            hover_color="#3f3f46", 
            text_color="#e4e4e7", 
            command=self.retry_generation
        )
        self.retry_btn.grid(row=0, column=1)

        # Input Box Frame
        self.entry_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.entry_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=(10, 30))
        self.entry_frame.grid_columnconfigure(0, weight=1)

        self.input_field = ctk.CTkEntry(
            self.entry_frame, 
            placeholder_text="Ask your local engine anything...", 
            font=("Helvetica", 13), 
            fg_color="#202024", 
            border_color="#2e2e33", 
            text_color="white", 
            height=45
        )
        self.input_field.grid(row=0, column=0, sticky="ew", padx=(0, 15))
        self.input_field.bind("<Return>", lambda event: self.start_generation_thread())

        self.send_btn = ctk.CTkButton(
            self.entry_frame, 
            text="Send", 
            width=100, 
            height=45, 
            fg_color="#2b2b36", 
            hover_color="#3a3a44", 
            text_color="white", 
            command=self.start_generation_thread
        )
        self.send_btn.grid(row=0, column=1)

    # ---------------- RENDER ENGINE FOR THE PREMIUM CARD ----------------
    def insert_premium_code_block(self, code_text, lang_title="Python"):
        """Embeds a fully standalone rounded code terminal card inside the textbox"""
        self.text_display.configure(state="normal")
        self.text_display.insert(tk.END, "\n")

        # 1. Base Container Card (Dark Matte Background)
        card = ctk.CTkFrame(self.text_display, fg_color="#0d0d11", corner_radius=10, border_width=1, border_color="#262631")
        card.grid_columnconfigure(0, weight=1)

        # 2. Sleek Header Bar
        header = ctk.CTkFrame(card, fg_color="#16161f", height=34, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        title = ctk.CTkLabel(
            header, 
            text=lang_title.upper(), 
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), 
            text_color="#8e8e9f"
        )
        title.pack(side="left", padx=15, pady=4)

        # Copy Action Icon/Button Layout
        def copy_code():
            self.clipboard_clear()
            self.clipboard_append(code_text)
            copy_btn.configure(text="Copied! ✓", text_color="#4ade80")
            self.after(2000, lambda: copy_btn.configure(text="📋 Copy", text_color="#a1a1aa"))

        copy_btn = ctk.CTkButton(
            header, 
            text="📋 Copy", 
            width=60, 
            height=24, 
            fg_color="transparent", 
            hover_color="#22222f", 
            text_color="#a1a1aa", 
            font=("Helvetica", 11), 
            command=copy_code
        )
        copy_btn.pack(side="right", padx=10, pady=5)

        # 3. Clean Code Display Area
        code_box = ctk.CTkTextbox(
            card, 
            font=("Consolas", 13), 
            fg_color="transparent", 
            text_color="#38bdf8", # Premium cyan tint syntax color
            wrap="none", 
            activate_scrollbars=False
        )
        code_box.insert("1.0", code_text.strip())
        code_box.configure(state="disabled")
        
        # Calculate dynamic window spacing matching the code volume
        line_count = int(code_box.index('end-1c').split('.')[0])
        box_height = min(max(line_count * 19, 45), 450)
        code_box.grid(row=1, column=0, sticky="ew", padx=10, pady=(10, 5))
        code_box.configure(height=box_height)

        # Embed widget directly inside standard tk text block pipeline
        self.text_display.window_create(tk.END, window=card, stretch=True)
        self.text_display.insert(tk.END, "\n\n")
        self.text_display.see(tk.END)
        self.text_display.configure(state="disabled")

    # ---------------- WORKFLOW EXECUTIONS ----------------
    def start_generation_thread(self, custom_prompt=None):
        if self.is_generating:
            return

        user_text = custom_prompt if custom_prompt else self.input_field.get().strip()
        if not user_text:
            return

        if not custom_prompt:
            self.input_field.delete(0, tk.END)

        self.append_text(f"\n✨ You\n{user_text}\n", "user")

        if not custom_prompt:
            self.chats[self.active_chat_id].append({"role": "user", "content": user_text})
        
        is_first_message = len(self.chats[self.active_chat_id]) <= 1
        if is_first_message and (self.active_chat_id.startswith("New Session") or self.active_chat_id == "Main Thread"):
            words = user_text.split()
            clean_title = " ".join(words[:4]) + ("..." if len(words) > 4 else "")
            self.chats[clean_title] = self.chats.pop(self.active_chat_id)
            self.active_chat_id = clean_title
            self.update_sidebar_list()

        self.save_histories()

        self.is_generating = True
        self.stop_signal = False
        self.send_btn.configure(state="disabled")
        self.stop_btn.grid() 

        threading.Thread(target=self.stream_ai_response, daemon=True).start()

    def stream_ai_response(self):
        selected_model = self.model_dropdown.get()
        self.append_text(f"\n🤖 APEX AI ({selected_model})\n", "ai")

        try:
            stream = ollama.chat(model=selected_model, messages=self.chats[self.active_chat_id], stream=True)
            full_reply = ""

            for chunk in stream:
                if self.stop_signal:
                    self.append_text("\n\n⚠️ [Generation terminated]\n", "system")
                    break
                
                token = chunk['message']['content']
                full_reply += token
                self.append_text(token, "ai_chunk")

            if not self.stop_signal:
                self.chats[self.active_chat_id].append({"role": "assistant", "content": full_reply})
                self.save_histories()
                
                # Instantly refresh the screen view to draw cards over pure texts
                self.load_chat_into_view()

        except Exception as e:
            self.append_text(f"\n\n❌ [Engine offline]: Make sure Ollama is open.\nDetails: {str(e)}", "error")

        self.is_generating = False
        self.send_btn.configure(state="normal")
        self.stop_btn.grid_remove()

    def stop_generation(self):
        if self.is_generating:
            self.stop_signal = True

    def retry_generation(self):
        if self.is_generating or not self.chats[self.active_chat_id]:
            return
        
        history = self.chats[self.active_chat_id]
        last_user_prompt = None
        for msg in reversed(history):
            if msg["role"] == "user":
                last_user_prompt = msg["content"]
                break
        
        if last_user_prompt:
            if history[-1]["role"] == "assistant":
                history.pop()
            self.start_generation_thread(custom_prompt=last_user_prompt)

    def append_text(self, text, tag_type):
        self.text_display.configure(state="normal")
        self.text_display.insert(tk.END, text)
        self.text_display.see(tk.END)
        self.text_display.configure(state="disabled")

    def create_new_chat(self):
        new_id = f"New Session {len(self.chats) + 1}"
        self.chats[new_id] = []
        self.active_chat_id = new_id
        self.update_sidebar_list()
        self.load_chat_into_view()
        self.save_histories()

    def update_sidebar_list(self):
        self.chat_listbox.delete(0, tk.END)
        for chat_id in self.chats.keys():
            self.chat_listbox.insert(tk.END, chat_id)
        try:
            idx = list(self.chats.keys()).index(self.active_chat_id)
            self.chat_listbox.selection_set(idx)
        except:
            pass

    def on_chat_selected(self, event):
        selection = self.chat_listbox.curselection()
        if selection:
            self.active_chat_id = self.chat_listbox.get(selection[0])
            self.load_chat_into_view()

    def load_chat_into_view(self):
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", tk.END)
        
        for msg in self.chats[self.active_chat_id]:
            role = "✨ You" if msg['role'] == "user" else "🤖 Assistant"
            content = msg['content']
            
            if "```" in content:
                # Intelligently separate normal chat replies from raw blocks
                parts = content.split("```")
                for i, part in enumerate(parts):
                    if i % 2 != 0: # This item contains code contents
                        lines = part.split("\n")
                        detected_lang = lines[0].strip() if lines[0].strip() else "Code"
                        code_body = "\n".join(lines[1:]) if lines[0].strip() else part
                        self.insert_premium_code_block(code_body, lang_title=detected_lang)
                    else:
                        if part.strip():
                            self.text_display.insert(tk.END, f"\n{role}\n{part}\n")
            else:
                self.text_display.insert(tk.END, f"\n{role}\n{content}\n")
        
        self.text_display.see(tk.END)
        self.text_display.configure(state="disabled")

    def save_histories(self):
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.chats, f, indent=4)

    def load_histories(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def on_closing(self):
        self.destroy()

if __name__ == "__main__":
    app = ApexAIApp()
    app.mainloop()