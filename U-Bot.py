import customtkinter as ctk
import ollama
import threading
import os
import getpass
import re
from PIL import Image

# --- Elite Color Palette ---
BG_COLOR = "#0F0F12"        # Deep Charcoal
SIDEBAR_COLOR = "#16161D"   # Slightly lighter offset
ACCENT_BLUE = "#3B82F6"     # Modern Electric Blue
UNRESTRICTED_GREEN = "#10B981"
RESTRICTED_RED = "#EF4444"
TEXT_MAIN = "#E5E7EB"

class UBotPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- State ---
        self.username = getpass.getuser()
        self.is_unrestricted = True
        self.sidebar_visible = True
        self.active_model = "dolphin-llama3"
        self.history = []

        # --- Window Config ---
        self.title("U-Bot Pro")
        self.geometry("1400x900")
        self.configure(fg_color=BG_COLOR)

        # Layout Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- UI Build ---
        self.setup_header()
        self.setup_sidebar()
        self.setup_chat_engine()
        self.setup_terminal()

        # Init UI State
        self.update_persona_style()

    def setup_header(self):
        """Sleek minimalist header"""
        self.header = ctk.CTkFrame(self, height=65, fg_color=SIDEBAR_COLOR, corner_radius=0)
        self.header.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        # Left Side
        self.menu_btn = ctk.CTkButton(self.header, text="☰", width=40, height=40, 
                                      fg_color="transparent", text_color=TEXT_MAIN,
                                      font=("Inter", 18), hover_color="#2D2D39",
                                      command=self.toggle_sidebar)
        self.menu_btn.pack(side="left", padx=15)
        
        ctk.CTkLabel(self.header, text="U-BOT", font=("Inter", 18, "bold"), 
                     text_color=ACCENT_BLUE).pack(side="left", padx=5)
        ctk.CTkLabel(self.header, text="PRO", font=("Inter", 18), 
                     text_color=TEXT_MAIN).pack(side="left")

        # Right Side - Persona Toggle
        self.persona_pill = ctk.CTkButton(self.header, text="", width=180, height=32,
                                          corner_radius=16, font=("Inter", 11, "bold"),
                                          command=self.toggle_persona)
        self.persona_pill.pack(side="right", padx=20)

    def setup_sidebar(self):
        """Unified Sidebar"""
        self.sidebar_frame = ctk.CTkFrame(self, width=280, fg_color=SIDEBAR_COLOR, corner_radius=0, border_width=0)
        self.sidebar_frame.grid(row=1, column=0, sticky="nsew")
        
        self.tabs = ctk.CTkTabview(self.sidebar_frame, fg_color="transparent", 
                                   segmented_button_fg_color="#1F1F29",
                                   segmented_button_selected_color=ACCENT_BLUE)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabs.add("Sessions")
        self.tabs.add("Files")

    def setup_chat_engine(self):
        """Main Chat Interface"""
        self.chat_main = ctk.CTkFrame(self, fg_color="transparent")
        self.chat_main.grid(row=1, column=1, sticky="nsew")

        # Scrollable Area
        self.chat_list = ctk.CTkScrollableFrame(self.chat_main, fg_color=BG_COLOR, corner_radius=0)
        self.chat_list.pack(fill="both", expand=True, padx=10)

        # Pill-shaped Input Area
        self.input_dock = ctk.CTkFrame(self.chat_main, fg_color="transparent")
        self.input_dock.pack(fill="x", padx=30, pady=25)

        self.entry = ctk.CTkEntry(self.input_dock, placeholder_text="Ask anything...", 
                                  height=52, corner_radius=26, border_width=1,
                                  fg_color="#1A1A24", border_color="#2D2D39",
                                  font=("Inter", 13))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.entry.bind("<Return>", lambda e: self.send_action())

        self.send_btn = ctk.CTkButton(self.input_dock, text="Execute", width=110, height=52, 
                                      corner_radius=26, fg_color=ACCENT_BLUE, 
                                      font=("Inter", 13, "bold"), hover_color="#2563EB",
                                      command=self.send_action)
        self.send_btn.pack(side="right")

    def setup_terminal(self):
        """Right-side log panel"""
        self.term_frame = ctk.CTkFrame(self, width=320, fg_color=SIDEBAR_COLOR, corner_radius=0)
        self.term_frame.grid(row=1, column=2, sticky="nsew")
        
        ctk.CTkLabel(self.term_frame, text="TERMINAL LOGS", font=("Inter", 11, "bold"), 
                     text_color="#6B7280").pack(pady=15)
        
        self.terminal = ctk.CTkTextbox(self.term_frame, fg_color="#09090B", text_color=UNRESTRICTED_GREEN,
                                       font=("JetBrains Mono", 11), border_width=1, border_color="#1F1F23")
        self.terminal.pack(fill="both", expand=True, padx=15, pady=(0, 20))

    # --- UI Logic ---

    def toggle_persona(self):
        self.is_unrestricted = not self.is_unrestricted
        self.update_persona_style()
        self.log(f"Safety mode: {'OFF' if self.is_unrestricted else 'ON'}")

    def update_persona_style(self):
        if self.is_unrestricted:
            self.persona_pill.configure(text="● UNRESTRICTED", fg_color="#064E3B", 
                                        text_color="#34D399", hover_color="#065F46")
        else:
            self.persona_pill.configure(text="○ RESTRICTED", fg_color="#450A0A", 
                                        text_color="#F87171", hover_color="#7F1D1D")

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.grid_forget()
        else:
            self.sidebar_frame.grid(row=1, column=0, sticky="nsew")
        self.sidebar_visible = not self.sidebar_visible

    def send_action(self):
        query = self.entry.get()
        if not query: return
        self.add_bubble("You", query)
        self.entry.delete(0, 'end')
        threading.Thread(target=self.run_inference, args=(query,)).start()

    def run_inference(self, query):
        try:
            self.log(f"Processing via {self.active_model}...")
            # (Inference logic here)
            self.add_bubble("AI", "Simulated response for the new UI.")
        except Exception as e:
            self.log(f"Error: {e}")

    def add_bubble(self, sender, text):
        align = "e" if sender == "You" else "w"
        color = ACCENT_BLUE if sender == "You" else "#1F1F29"
        
        bubble = ctk.CTkLabel(self.chat_list, text=text, wraplength=550, 
                              fg_color=color, corner_radius=12, padx=15, pady=10,
                              font=("Inter", 13), justify="left")
        bubble.pack(pady=12, padx=20, anchor=align)
        self.after(100, lambda: self.chat_list._parent_canvas.yview_moveto(1.0))

    def log(self, text):
        self.terminal.insert("end", f"> {text}\n")
        self.terminal.see("end")

if __name__ == "__main__":
    app = UBotPro()
    app.mainloop()