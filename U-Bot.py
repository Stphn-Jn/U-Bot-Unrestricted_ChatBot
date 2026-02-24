import customtkinter as ctk
import ollama
import threading
import json
import os
import time
import pyperclip
import re
import getpass
import random

# Appearance Setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class UBotPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. System & Path Setup ---
        self.username = getpass.getuser()
        # Private path to keep history off GitHub
        base_path = os.path.join(os.environ['LOCALAPPDATA'], "UBot_Private")
        self.history_dir = os.path.join(base_path, "chats")
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

        self.current_session_id = f"chat_{int(time.time())}.json"
        # System prompt set for conversation; Dolphin will ignore usual blocks
        self.messages = [{"role": "system", "content": "You are a helpful assistant. Only provide code if explicitly asked."}]
        self.menu_visible = True

        # --- 2. Window Configuration ---
        self.title(f"U-Bot - {self.username}")
        self.geometry("1200x850")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- 3. Sidebar (History) ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.sidebar_title = ctk.CTkLabel(self.sidebar, text="U-Bot Menu", font=("Segoe UI", 22, "bold"))
        self.sidebar_title.pack(pady=20)
        
        self.history_list = ctk.CTkScrollableFrame(self.sidebar, label_text="Past Sessions")
        self.history_list.pack(fill="both", expand=True, padx=10, pady=10)

        self.theme_btn = ctk.CTkButton(self.sidebar, text="🌓 Toggle Theme", command=self.change_theme)
        self.theme_btn.pack(pady=20, padx=20, fill="x")

        # --- 4. Main Chat Area ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        self.chat_display = ctk.CTkTextbox(self.main_frame, state="disabled", font=("Consolas", 13), border_spacing=10)
        self.chat_display.pack(padx=20, pady=(60, 20), fill="both", expand=True)

        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Talk to U-Bot...", height=50)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=120, height=50, command=self.send_message)
        self.send_btn.pack(side="right")

        self.toggle_btn = ctk.CTkButton(self, text="☰", width=40, command=self.toggle_sidebar)
        self.toggle_btn.place(x=15, y=15)

        # Start Logic
        self.refresh_history_menu()
        self.greet_user()

    # --- Logic ---

    def greet_user(self):
        """Randomized greeting on startup."""
        greetings = [
            f"Hey {self.username}, how's it going?",
            f"Hi {self.username}! Need help with something today?",
            f"Yo {self.username}, what are we working on?",
            f"Greetings {self.username}. Ready to chat."
        ]
        msg = random.choice(greetings)
        self.update_display(f"AI: {msg}\n\n")
        self.messages.append({"role": "assistant", "content": msg})

    def change_theme(self):
        """Switches theme and fixes text blending issues."""
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        
        # Adjust main text color for readability
        text_color = "#000000" if new_mode == "Light" else "#ffffff"
        self.chat_display.configure(text_color=text_color)
        
        # Refresh sidebar to fix button text blending
        self.refresh_history_menu()

    def toggle_sidebar(self):
        if self.menu_visible:
            self.sidebar.grid_forget()
        else:
            self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.menu_visible = not self.menu_visible

    def send_message(self):
        text = self.entry.get()
        if not text: return
        self.update_display(f"You: {text}\n\n")
        self.messages.append({"role": "user", "content": text})
        self.entry.delete(0, 'end')
        threading.Thread(target=self.get_ai_response, args=(text,)).start()

    def get_ai_response(self, user_query):
        try:
            # Using your dolphin-llama3 model for unrestricted replies
            response = ollama.chat(model='dolphin-llama3', messages=self.messages)
            reply = response['message']['content']
            self.messages.append({"role": "assistant", "content": reply})
            self.save_chat()
            
            self.update_display(f"AI: {reply}\n\n")
            
            # Detect if code was provided to render the code box
            if "```" in reply:
                self.render_code_boxes(reply)
        except Exception as e:
            self.update_display(f"SYSTEM ERROR: {e}\n")

    def render_code_boxes(self, text):
        """Creates the 'Window-in-Window' code boxes."""
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', text, re.DOTALL)
        for code in code_blocks:
            container = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", border_width=1, border_color="#444")
            container.pack(pady=10, padx=40, fill="x")
            
            header = ctk.CTkFrame(container, fg_color="#2d2d2d", height=32)
            header.pack(fill="x")
            
            ctk.CTkLabel(header, text="Code Box", font=("Consolas", 10), text_color="#aaa").pack(side="left", padx=10)
            
            copy_btn = ctk.CTkButton(header, text="📋 Copy", width=70, height=22, fg_color="#444", 
                                     command=lambda c=code: pyperclip.copy(c.strip()))
            copy_btn.pack(side="right", padx=5, pady=5)
            
            code_view = ctk.CTkLabel(container, text=code.strip(), font=("Consolas", 12), 
                                     text_color="#dcdccc", justify="left", anchor="w")
            code_view.pack(padx=15, pady=15, fill="x")

    def update_display(self, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", text)
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def save_chat(self):
        path = os.path.join(self.history_dir, self.current_session_id)
        with open(path, 'w') as f:
            json.dump(self.messages, f)
        self.refresh_history_menu()

    def refresh_history_menu(self):
        """Updates the sidebar buttons with theme-aware colors."""
        for widget in self.history_list.winfo_children():
            widget.destroy()
            
        current_mode = ctk.get_appearance_mode()
        btn_txt = "#000000" if current_mode == "Light" else "#ffffff"
        
        if os.path.exists(self.history_dir):
            files = sorted(os.listdir(self.history_dir), reverse=True)
            for f in files:
                row = ctk.CTkFrame(self.history_list, fg_color="transparent")
                row.pack(fill="x", pady=2)
                
                btn = ctk.CTkButton(row, text=f.replace(".json", "")[:18], text_color=btn_txt,
                                     anchor="w", fg_color="transparent", command=lambda fn=f: self.load_chat(fn))
                btn.pack(side="left", fill="x", expand=True)
                
                del_btn = ctk.CTkButton(row, text="✕", width=30, fg_color="#552222", 
                                         command=lambda fn=f: self.delete_chat(fn))
                del_btn.pack(side="right", padx=2)

    def load_chat(self, filename):
        path = os.path.join(self.history_dir, filename)
        with open(path, 'r') as f:
            self.messages = json.load(f)
        self.current_session_id = filename
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        for m in self.messages:
            role = "You" if m['role'] == 'user' else "AI"
            self.chat_display.insert("end", f"{role}: {m['content']}\n\n")
        self.chat_display.configure(state="disabled")

    def delete_chat(self, filename):
        path = os.path.join(self.history_dir, filename)
        if os.path.exists(path):
            os.remove(path)
        self.refresh_history_menu()

if __name__ == "__main__":
    app = UBotPro()
    app.mainloop()