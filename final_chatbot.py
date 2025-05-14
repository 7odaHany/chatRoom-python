import socket              # For network communication
import threading           # For running the bot listener in background
import time                # For delays in bot responses
from datetime import datetime   # For time/date responses
import re                  # For regular expressions to clean text
def normalize_arabic(text):
    """
    Normalize Arabic text by:
    - Removing diacritics (tashkeel)
    - Removing non-Arabic characters
    - Normalizing common letter variations
    """
    text = re.sub(r'[\u064B-\u0652]', '', text)  # Remove diacritics (Tashkeel)
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)  # Remove non-Arabic characters
    text = text.replace("أ", "ا")  # Normalize Hamza forms
    text = text.replace("إ", "ا")
    text = text.replace("آ", "ا")
    text = text.replace("ة", "ه")  # Normalize Ta marbuta
    text = text.replace("ى", "ي")  # Normalize Alif Maqsura
    return text
def run_bot():
    
    """
    Starts the chatbot client, connects to the server, and listens for messages.
    Responds automatically to certain keywords or phrases.
    """
    bot_name = "ChatBot"
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create TCP socket
        client_socket.connect(('localhost', 5005))                         # Connect to chat server
        client_socket.send(bot_name.encode('utf-8'))                       # Send bot name as username

        def listen():
            """
            Listen for messages from the server and respond if needed.
            """
            while True:
                try:
                    message = client_socket.recv(1024).decode('utf-8')     # Receive message from server
                    if not message:
                        break
                    print(f"Received: {message}")

                    if message.startswith(bot_name):
                        continue  # Ignore bot's own messages

                    lower_msg = message.lower()
                    arabic_msg = normalize_arabic(message)

                    # Bot response logic for various keywords (expanded)
                    if ("hello" in lower_msg or "hi" in lower_msg or 
                        "اهلا" in arabic_msg or "مرحبا" in arabic_msg or 
                        "سلام" in arabic_msg or "السلام عليكم" in arabic_msg):
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: أهلا بك! كيف يمكنني مساعدتك؟".encode('utf-8'))
                    elif ("how are you" in lower_msg or "كيف حالك" in arabic_msg or 
                            "كيفك" in arabic_msg or "عامل ايه" in arabic_msg or "اخبارك" in arabic_msg):
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: أنا بخير، شكرا لسؤالك! كيف يمكنني مساعدتك اليوم؟".encode('utf-8'))
                    elif ("bye" in lower_msg or "مع السلامة" in arabic_msg or 
                            "وداعا" in arabic_msg or "الى اللقاء" in arabic_msg or "باي" in arabic_msg):
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: إلى اللقاء! أتمنى لك يوماً سعيداً.".encode('utf-8'))
                    elif ("thank" in lower_msg or "شكرا" in arabic_msg or "متشكر" in arabic_msg or "thx" in lower_msg):
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: العفو! سعيد بمساعدتك.".encode('utf-8'))
                    elif ("help" in lower_msg or "مساعدة" in arabic_msg or "ممكن تساعدني" in arabic_msg):
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: يمكنني الإجابة على الأسئلة البسيطة. جرب أن تقول 'مرحبا' أو 'كيف حالك' أو 'شكرا'.".encode('utf-8'))
                    elif ("time" in lower_msg or "الوقت" in arabic_msg or "الساعة" in arabic_msg):
                        current_time = datetime.now().strftime("%H:%M:%S")
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: الوقت الحالي هو {current_time}".encode('utf-8'))
                    elif ("date" in lower_msg or "التاريخ" in arabic_msg or "اليوم" in arabic_msg):
                        current_date = datetime.now().strftime("%Y-%m-%d")
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: التاريخ اليوم هو {current_date}".encode('utf-8'))
                    elif ("من انت" in arabic_msg or "who are you" in lower_msg):
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: أنا روبوت دردشة بسيط هنا لمساعدتك!".encode('utf-8'))
                    elif ("احبك" in arabic_msg or "i love you" in lower_msg):
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: وأنا أيضا أحبك! 😊".encode('utf-8'))
                    elif ("?" in message or "؟" in message):
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: هذا سؤال مثير للاهتمام. دعني أفكر في الإجابة.".encode('utf-8'))

                except Exception as e:
                    print(f"Error: {e}")
                    break

        listen_thread = threading.Thread(target=listen)    # Create a thread for listening to messages
        listen_thread.daemon = True                        # Set as daemon so it closes with main program
        listen_thread.start()                              # Start listening thread

        print(f"{bot_name} is running and connected to the server...")
        listen_thread.join()                               # Wait for the thread to finish

    except Exception as e:
        print(f"Failed to connect to server: {e}")

if __name__ == "__main__":
    run_bot()   # Start the chatbot if the file is run directly