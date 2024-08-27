import socket
import threading
import select  # For non-blocking socket
from queue import Queue
import json
import time

clients = {}
lock = threading.Lock()  # To handle shared access to clients dictionary
shutdown_flag = threading.Event()  # Event to signal shutdown

# Function to handle each client connection
def handle_client(client_socket, addr, client_name, q):
    print(f"Client {client_name} connected from {addr}")

    try:
        while not shutdown_flag.is_set():
            try:
                got = False
                while not got and not shutdown_flag.is_set():
                    data = q.get()
                    if data['client'] == client_name:
                        client_socket.sendall(json.dumps(data).encode('utf-8'))
                        print(f"Sent {data} to {client_name}")
                        got = True
                    else:
                        q.put(data)  # Put the data back in the queue if it's not for this client
            except Exception as e:
                print(f"Error handling client {client_name}: {e}")
                break
    finally:
        # Clean up client socket and remove from clients dictionary
        with lock:
            print(f"Client {client_name} disconnected")
            client_socket.close()
            if client_name in clients:
                del clients[client_name]

# Function to start the server and listen for clients
def start_server(host, port, q):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_socket.settimeout(5)  # Set server socket to non-blocking
    print(f"Server listening on {host}:{port}")

    try:
        while not shutdown_flag.is_set():
            ready_to_read, _, _ = select.select([server_socket], [], [], 1)
            if ready_to_read:
                print("Ready to read")
                try:
                    client_socket, addr = server_socket.accept()
                    client_name = client_socket.recv(1024).decode('utf-8')  # Expecting the client to send its name first
                    with lock:
                        clients[client_name] = client_socket
                    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, client_name, q))
                    client_thread.daemon = True
                    client_thread.start()
                except OSError as e:
                    print(f"Error accepting connection: {e}")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Shutting down server...")
        shutdown_flag.set()
        shutdown_server(server_socket)
    except Exception as e:
        print(f"Server error: {e}")
        shutdown_flag.set()
        shutdown_server(server_socket)

# Function to shut down the server gracefully
def shutdown_server(server_socket):
    print("Closing server socket...")
    server_socket.close()
    with lock:
        print("Closing client sockets...")
        for client_name, client_socket in clients.items():
            client_socket.close()
    print("Server shut down gracefully.")

if __name__ == "__main__":
    q = Queue()
    start_server('0.0.0.0', 5550, q)
