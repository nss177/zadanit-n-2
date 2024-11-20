import socket
import threading

# Обработчик клиента
def handle_client(client_socket, clients):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Получено сообщение: {message}")
                # сообщениеподключенным клиентам
                for client in clients:
                    if client != client_socket:
                        client.send(message.encode('utf-8'))
            else:
                break
    except ConnectionResetError:
        pass
    finally:
        clients.remove(client_socket)
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))  # Локальный адрес
    server.listen(5)
    print("Сервер запущен и ожидает подключения...")
    
    clients = []
    
    while True:
        client_socket, addr = server.accept()
        print(f"Подключен клиент {addr}")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, clients))
        client_thread.start()


if __name__ == "__main__":
    start_server()
