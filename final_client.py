import socket                           # For network communication
import threading                        # For running receive in background
import tkinter as tk                    # For GUI
from tkinter import simpledialog, messagebox, scrolledtext
from tkinter import font as tkfont
from datetime import datetime           # For timestamps

class ChatClient:
    def __init__(self, root):
        """
        Initialize the chat client:
        - Set up fonts, theme, GUI, and network connection.
        """
        self.root = root
        self.setup_fonts()               # Set up fonts for the GUI
        self.setup_theme()               # Set up color theme
        self.setup_gui()                 # Build the GUI
        self.setup_network()             # Connect to the server
        self.username = ""               # Store the username

    def setup_fonts(self):
        """
        Set up fonts for main text and headers.
        """
        try:
            self.font_main = tkfont.Font(family="Cairo", size=12)
            self.font_header = tkfont.Font(family="Cairo", size=16, weight="bold")
        except:
            self.font_main = tkfont.Font(size=12)
            self.font_header = tkfont.Font(size=16, weight="bold")

    def setup_theme(self):
        """
        Set up color theme for the GUI.
        """
        self.bg_color = "#e0f7fa"
        self.header_color = "#006064"
        self.msg_color_self = "#b2ebf2"
        self.msg_color_others = "#ffffff"
        self.send_btn_color = "#00838f"

    def setup_gui(self):
        """
        Build the GUI: window, labels, chat area, input, and send button.
        """
        self.root.title("🌟 دردشة جماعية")
        self.root.geometry("600x600")
        self.root.configure(bg=self.bg_color)

        # Username label at the top
        self.user_label = tk.Label(
            self.root,
            text="اسم المستخدم: ...",  # Will be updated after login
            font=self.font_main,
            bg=self.bg_color,
            fg="#006064",
            anchor="e",
            pady=5
        )
        self.user_label.pack(fill="x", padx=10)

        # Header label
        self.header = tk.Label(
            self.root,
            text="🌟 غرفة الدردشة",
            font=self.font_header,
            bg=self.header_color,
            fg="white",
            pady=10
        )
        self.header.pack(fill="x")

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            font=self.font_main,
            bg="#ffffff",
            wrap=tk.WORD,
            state="disabled",
            relief="flat",
            bd=5
        )
        self.chat_area.pack(padx=10, pady=10, expand=True, fill="both")

        # Input area (frame for entry and button)
        self.input_frame = tk.Frame(self.root, bg=self.bg_color)
        self.input_frame.pack(fill="x", pady=10, padx=10)

        self.msg_entry = tk.Entry(
            self.input_frame,
            font=self.font_main,
            bg="white",
            relief="solid",
            bd=2
        )
        self.msg_entry.pack(side="right", expand=True, fill="x", padx=(5, 0))
        self.msg_entry.bind("<Return>", self.send_message)  # Send on Enter

        self.send_button = tk.Button(
            self.input_frame,
            text="إرسال ➤",
            font=self.font_main,
            bg=self.send_btn_color,
            fg="white",
            command=self.send_message
        )
        self.send_button.pack(side="left")

    def setup_network(self):
        """
        Connect to the chat server and start the receive thread.
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(('localhost', 5005))
            username = simpledialog.askstring(
                "اسم المستخدم",
                "من فضلك أدخل اسمك:",
                parent=self.root
            )
            if not username:
                username = "مجهول"
            self.username = username
            # Update username label at the top
            self.user_label.config(text=f"اسم المستخدم: {self.username}")
            self.client_socket.send(username.encode('utf-8'))
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل الاتصال بالسيرفر: {e}")
            self.root.destroy()

    def receive_messages(self):
        """
        Continuously receive messages from the server and display them.
        """
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.display_message(message)
            except:
                break

    def display_message(self, message):
        """
        Display a message in the chat area with formatting.
        Shows sender name above the message.
        """
        self.chat_area.config(state='normal')
        time_now = datetime.now().strftime("%H:%M")

        if ":" in message:
            sender, msg_text = message.split(":", 1)
            sender = sender.strip()
            # Show sender name in a separate line and bold
            self.chat_area.insert('end', f"{sender}\n", "sender_name")
            bubble = f"{msg_text.strip()} ({time_now})\n\n"
            tag = "self_msg" if sender == self.username else "others_msg"
            self.chat_area.insert('end', bubble, tag)
        else:
            system_msg = f"*** {message} ({time_now}) ***\n\n"
            self.chat_area.insert('end', system_msg, "system_msg")

        # Tag styles for formatting
        self.chat_area.tag_config("self_msg", background=self.msg_color_self, justify='right')
        self.chat_area.tag_config("others_msg", background=self.msg_color_others, justify='left')
        self.chat_area.tag_config(
            "system_msg",
            background="#fff3e0",
            justify='center',
            font=("Cairo", 10, "italic")
        )
        self.chat_area.tag_config(
            "sender_name",
            font=("Cairo", 11, "bold"),
            foreground="#00838f",
            justify='right'
        )
        self.chat_area.config(state='disabled')
        self.chat_area.see('end')

    def send_message(self, event=None):
        """
        Send the message typed by the user to the server and display it locally.
        """
        message = self.msg_entry.get().strip()
        if message:
            try:
                # Show the message immediately in the chat area
                self.display_message(f"{self.username}: {message}")
                self.client_socket.send(message.encode('utf-8'))
                self.msg_entry.delete(0, 'end')
            except:
                self.display_message("فشل إرسال الرسالة!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()