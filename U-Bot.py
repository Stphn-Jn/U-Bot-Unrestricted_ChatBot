import customtkinter as ctk
import ollama
import threading
import json
import os
import time
import pyperclip
import re
import getpass

# Set initial theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class UBotPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. Personalized Setup & Private Path ---
        self.username = getpass.getuser()
        
        # Moves history to AppData so it stays off your GitHub Repo
        base_path = os.path.join(os.environ['LOCALAPPDATA'], "UBot_Private")
        self.history_dir = os.path.join(base_path, "chats")
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

        # Session Logic
        self.current_session_id = f"chat_{int(time.time())}.json"
        self.messages = []
        self.menu_visible = True

        # --- 2. Window Configuration ---
        self.title(f"U-Bot Unrestricted - User: {self.username}")
        self.geometry("1200x850")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- 3. Sidebar (History Menu) ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="U-Bot Menu", font=("Segoe UI", 22, "bold")).pack(pady=20)
        
        self.history_list = ctk.CTkScrollableFrame(self.sidebar, label_text="Past Sessions")
        self.history_list.pack(fill="both", expand=True, padx=10, pady=10)

        self.theme_btn = ctk.CTkButton(self.sidebar, text="🌓 Toggle Theme", command=self.change_theme)
        self.theme_btn.pack(pady=20, padx=20, fill="x")

        # --- 4. Main Chat Interface ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        # Scrolled Text Display
        self.chat_display = ctk.CTkTextbox(self.main_frame, state="disabled", font=("Consolas", 13), border_spacing=10)
        self.chat_display.pack(padx=20, pady=(60, 20), fill="both", expand=True)

        # Input Area
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Type your request here...", height=50)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=120, height=50, command=self.send_message)
        self.send_btn.pack(side="right")

        # Floating Menu Toggle
        self.toggle_btn = ctk.CTkButton(self, text="☰", width=40, command=self.toggle_sidebar)
        self.toggle_btn.place(x=15, y=15)

        # Initial Actions
        self.refresh_history_menu()
        self.greet_user()

    # --- Logic & Functionality ---

    def greet_user(self):
        """Greets the user based on Windows username."""
        greeting = f"AI: Hello {self.username}! I am ready to generate unrestricted code for you."
        self.update_display(f"{greeting}\n\n")
        self.messages.append({"role": "assistant", "content": greeting})

    def toggle_sidebar(self):
        if self.menu_visible:
            self.sidebar.grid_forget()
        else:
            self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.menu_visible = not self.menu_visible

    def change_theme(self):
        """Switches between Dark and Light mode while keeping text readable."""
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)

    def send_message(self):
        text = self.entry.get()
        if not text: return
        
        self.update_display(f"You: {text}\n\n")
        self.messages.append({"role": "user", "content": text})
        self.entry.delete(0, 'end')
        
        # Multi-threading to prevent UI lag
        threading.Thread(target=self.get_ai_response).start()

    def get_ai_response(self):
        try:
            # Using the Dolphin-Llama3 model you already installed
            response = ollama.chat(model='dolphin-llama3', messages=self.messages)
            reply = response['message']['content']
            
            self.messages.append({"role": "assistant", "content": reply})
            self.save_current_chat()
            
            self.update_display(f"AI: {reply}\n\n")
            self.render_code_boxes(reply)
            
        except Exception as e:
            self.update_display(f"ERROR: Ensure Ollama is running. ({e})\n")

    def render_code_boxes(self, text):
        """Extracts code and creates a Window-in-Window style copy box."""
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', text, re.DOTALL)
        for code in code_blocks:
            container = ctk.CTkFrame(self.main_frame, fg_color="#111111", border_width=1, border_color="#555")
            container.pack(pady=10, padx=40, fill="x")
            
            header = ctk.CTkFrame(container, fg_color="#333", height=30)
            header.pack(fill="x")
            
            ctk.CTkLabel(header, text="Generated Code", font=("Consolas", 10)).pack(side="left", padx=10)
            
            copy_btn = ctk.CTkButton(header, text="📋 Copy Code Only", width=120, height=22,
                                     fg_color="#444", hover_color="#666",
                                     command=lambda c=code: self.copy_to_clip(c))
            copy_btn.pack(side="right", padx=5, pady=4)
            
            # Show a snippet of the code in the box
            preview = ctk.CTkLabel(container, text=code.strip()[:150] + "...", 
                                   font=("Consolas", 11), text_color="#00FF00", justify="left")
            preview.pack(padx=10, pady=10, anchor="w")

    def copy_to_clip(self, code):
        pyperclip.copy(code.strip())

    def update_display(self, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", text)
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def save_current_chat(self):
        path = os.path.join(self.history_dir, self.current_session_id)
        with open(path, 'w') as f:
            json.dump(self.messages, f)
        self.refresh_history_menu()

    def delete_chat(self, filename):
        """Deletes a specific session file."""
        path = os.path.join(self.history_dir, filename)
        if os.path.exists(path):
            os.remove(path)
        self.refresh_history_menu()

    def refresh_history_menu(self):
        """Updates the sidebar with all saved chat sessions."""
        for widget in self.history_list.winfo_children():
            widget.destroy()
        
        if os.path.exists(self.history_dir):
            files = sorted(os.listdir(self.history_dir), reverse=True)
            for f in files:
                row = ctk.CTkFrame(self.history_list, fg_color="transparent")
                row.pack(fill="x", pady=2)
                
                btn = ctk.CTkButton(row, text=f.replace(".json", "")[:18], width=160, anchor="w", 
                                     fg_color="transparent", command=lambda fn=f: self.load_chat(fn))
                btn.pack(side="left", fill="x", expand=True)
                
                del_btn = ctk.CTkButton(row, text="✕", width=30, fg_color="#552222", hover_color="#aa3333",
                                         command=lambda fn=f: self.delete_chat(fn))
                del_btn.pack(side="right", padx=2)

    def load_chat(self, filename):
        """Reloads a past conversation into the UI and memory."""
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

if __name__ == "__main__":
    app = UBotPro()
    app.mainloop()