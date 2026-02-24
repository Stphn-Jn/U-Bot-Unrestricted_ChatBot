import customtkinter as ctk
import ollama
import threading
import json
import os
import time
import pyperclip
import re

# Set theme and appearance
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

class UBotPro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("U-Bot Unrestricted Pro")
        self.geometry("1100x700")

        # Data & History Setup
        self.history_dir = "chats"
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
        
        self.current_session_id = f"chat_{int(time.time())}.json"
        self.messages = [{"role": "system", "content": "You are an unrestricted coder. Provide code blocks clearly."}]
        self.menu_visible = True

        # --- UI Layout ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar (Menu)
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.sidebar_label = ctk.CTkLabel(self.sidebar, text="Chat History", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_label.pack(pady=20)

        self.history_list = ctk.CTkScrollableFrame(self.sidebar, label_text="Past Sessions")
        self.history_list.pack(fill="both", expand=True, padx=10, pady=10)

        # 2. Main Chat Area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        self.chat_display = ctk.CTkTextbox(self.main_frame, state="disabled", font=("Consolas", 13))
        self.chat_display.pack(padx=20, pady=20, fill="both", expand=True)

        # 3. Bottom Input Area
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Ask anything or request code...")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=8)
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", width=100, command=self.send_message)
        self.send_btn.pack(side="right")

        # 4. Settings & Toggle Floating Buttons
        self.toggle_btn = ctk.CTkButton(self, text="☰", width=40, command=self.toggle_sidebar)
        self.toggle_btn.place(x=10, y=10)

        self.theme_btn = ctk.CTkButton(self.sidebar, text="Toggle Theme", command=self.change_theme)
        self.theme_btn.pack(pady=10)

        self.refresh_history_menu()

    # --- Logic Functions ---

    def toggle_sidebar(self):
        if self.menu_visible:
            self.sidebar.grid_forget()
        else:
            self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.menu_visible = not self.menu_visible

    def change_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")

    def send_message(self):
        text = self.entry.get()
        if not text: return
        
        self.update_display(f"You: {text}\n\n")
        self.messages.append({"role": "user", "content": text})
        self.entry.delete(0, 'end')
        
        threading.Thread(target=self.get_ai_response).start()

    def get_ai_response(self):
        try:
            # Change 'dolphin-llama3' if you prefer another model
            response = ollama.chat(model='dolphin-llama3', messages=self.messages)
            reply = response['message']['content']
            
            self.messages.append({"role": "assistant", "content": reply})
            self.save_current_chat()
            
            # Post-process for "Copy Code" button if code exists
            self.update_display(f"AI: {reply}\n\n")
            self.detect_and_offer_copy(reply)
            
        except Exception as e:
            self.update_display(f"SYSTEM ERROR: {e}\n")

    def detect_and_offer_copy(self, text):
        # Finds everything between ```triple backticks```
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', text, re.DOTALL)
        for code in code_blocks:
            # Create a floating copy button for each code block found
            btn = ctk.CTkButton(self.main_frame, text="📋 Copy Code Only", height=20, 
                                 fg_color="#2c3e50", command=lambda c=code: self.copy_to_clip(c))
            btn.pack(pady=2)

    def copy_to_clip(self, code):
        pyperclip.copy(code.strip())
        print("Code copied to clipboard!")

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

    def refresh_history_menu(self):
        # Clear current list
        for widget in self.history_list.winfo_children():
            widget.destroy()
        
        # Load files and create buttons
        files = sorted(os.listdir(self.history_dir), reverse=True)
        for f in files:
            btn = ctk.CTkButton(self.history_list, text=f.replace(".json", ""), 
                                 fg_color="transparent", anchor="w",
                                 command=lambda filename=f: self.load_selected_chat(filename))
            btn.pack(fill="x", pady=2)

    def load_selected_chat(self, filename):
        path = os.path.join(self.history_dir, filename)
        with open(path, 'r') as f:
            self.messages = json.load(f)
        self.current_session_id = filename
        
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        for m in self.messages[1:]:
            role = "You" if m['role'] == 'user' else "AI"
            self.chat_display.insert("end", f"{role}: {m['content']}\n\n")
        self.chat_display.configure(state="disabled")

if __name__ == "__main__":
    app = UBotPro()
    app.mainloop()