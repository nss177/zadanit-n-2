import socket
import threading
import tkinter as tk
from tkinter import scrolledtext


def receive_messages(sock, text_widget):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                
                text_widget.config(state=tk.NORMAL)
                text_widget.insert(tk.END, "Собеседник: " + message + '\n')
                text_widget.yview(tk.END)  # Прокрутка вниз
                
                text_widget.config(state=tk.DISABLED)
        except:
            break


def send_message(sock, message_entry, text_widget):
    message = message_entry.get()
    if message:
        #редактирования перед отправкой нового сообщения
        text_widget.config(state=tk.NORMAL)
        sock.send(message.encode('utf-8'))
        text_widget.insert(tk.END, "Вы: " + message + '\n')
        text_widget.yview(tk.END)  
        message_entry.delete(0, tk.END)  
        
        text_widget.config(state=tk.DISABLED)


def start_chat():
    # сокет 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 12345))  # Подключение к серверу на localhost
    
    # окно чата
    root = tk.Tk()
    root.title("Чат")
    
    
    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    text_widget.pack(padx=10, pady=10)
    
    
    text_widget.config(state=tk.DISABLED)
    
    # Поле для ввода сообщений
    message_entry = tk.Entry(root, width=40)
    message_entry.pack(padx=10, pady=5)
    
    # Кнопка отправки сообщений
    send_button = tk.Button(root, text="Отправить", command=lambda: send_message(sock, message_entry, text_widget))
    send_button.pack(pady=5)

   
    threading.Thread(target=receive_messages, args=(sock, text_widget), daemon=True).start()

    root.mainloop()

# Окно для начала чата 
def open_chat_window():
    window = tk.Tk()
    window.title("Мини-приложение")

    label = tk.Label(window, text="Нажмите кнопку для начала чата", font=("Arial", 14))
    label.pack(pady=20)

    # Кнопки для начала чата для каждого клиента
    start_button_1 = tk.Button(window, text="Запустить чат для первого пользователя", command=lambda: [window.destroy(), start_chat()])
    start_button_1.pack(pady=20)
    
    start_button_2 = tk.Button(window, text="Запустить чат для второго пользователя", command=lambda: [window.destroy(), start_chat()])
    start_button_2.pack(pady=20)

    window.mainloop()


if __name__ == "__main__":
    open_chat_window()
