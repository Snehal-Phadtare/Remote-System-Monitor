import socket
import psutil
import json
import time

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server started... Waiting for connection")

conn, addr = server.accept()
print("Connected to:", addr)

while True:
    try:
        # Get system data
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        processes = len(psutil.pids())

        data = {
            "CPU": cpu,
            "Memory": memory,
            "Processes": processes
        }

        # IMPORTANT: add '\n' to avoid JSON error
        message = json.dumps(data) + "\n"
        conn.sendall(message.encode())

        time.sleep(4)  # total ~5 sec update

    except:
        print("Client disconnected")
        break

conn.close()
server.close()