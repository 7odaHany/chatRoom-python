import socket              # For network communication
import threading           # For running the bot listener in background
import time                # For delays in bot responses
from datetime import datetime   # For time/date responses

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

                    # Bot response logic for various keywords
                    if "hello" in lower_msg or "hi" in lower_msg or "اهلا" in lower_msg or "مرحبا" in lower_msg:
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: أهلا بك! كيف يمكنني مساعدتك؟".encode('utf-8'))
                    elif "how are you" in lower_msg or "كيف حالك" in lower_msg or "كيفك" in lower_msg:
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: أنا بخير، شكرا لسؤالك! كيف يمكنني مساعدتك اليوم؟".encode('utf-8'))
                    elif "bye" in lower_msg or "مع السلامة" in lower_msg or "وداعا" in lower_msg:
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: إلى اللقاء! أتمنى لك يوماً سعيداً.".encode('utf-8'))
                    elif "thank" in lower_msg or "شكرا" in lower_msg:
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: العفو! سعيد بمساعدتك.".encode('utf-8'))
                    elif "help" in lower_msg or "مساعدة" in lower_msg:
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: يمكنني الإجابة على الأسئلة البسيطة. جرب أن تقول 'مرحبا' أو 'كيف حالك' أو 'شكرا'.".encode('utf-8'))
                    elif "time" in lower_msg or "الوقت" in lower_msg or "الساعة" in lower_msg:
                        current_time = datetime.now().strftime("%H:%M:%S")
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: الوقت الحالي هو {current_time}".encode('utf-8'))
                    elif "date" in lower_msg or "التاريخ" in lower_msg or "اليوم" in lower_msg:
                        current_date = datetime.now().strftime("%Y-%m-%d")
                        time.sleep(1)
                        client_socket.send(f"{bot_name}: التاريخ اليوم هو {current_date}".encode('utf-8'))
                    elif "?" in message or "؟" in message:
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
