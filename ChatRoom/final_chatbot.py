import socket
import threading
import time
from datetime import datetime

def run_bot():
    bot_name = "ChatBot"
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 5005))
        client_socket.send(bot_name.encode('utf-8'))

        def listen():
            while True:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    if not message:
                        break
                    print(f"Received: {message}")

                    if message.startswith(bot_name):
                        continue  # تجاهل رسائل البوت نفسه

                    lower_msg = message.lower()

                    # تحسين استجابات البوت
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

        listen_thread = threading.Thread(target=listen)
        listen_thread.daemon = True
        listen_thread.start()

        print(f"{bot_name} is running and connected to the server...")
        listen_thread.join()

    except Exception as e:
        print(f"فشل الاتصال بالسيرفر: {e}")

if __name__ == "__main__":
    run_bot()
