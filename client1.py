import socket
import json
import tkinter as tk
from tkinter import ttk
import winsound

HOST = '127.0.0.1'
PORT = 5000

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except:
    print("Server not running!")
    exit()

# --- GUI ---
root = tk.Tk()
root.title("System Monitor Dashboard")
root.geometry("400x300")
root.configure(bg="#1e1e2f")

title = tk.Label(root, text="System Monitor", font=("Arial", 16, "bold"),
                 bg="#1e1e2f", fg="#00ff00")
title.pack(pady=10)

cpu_label = tk.Label(root, text="CPU:", font=("Arial", 14),
                     bg="#1e1e2f", fg="white")
cpu_label.pack()

cpu_bar = ttk.Progressbar(root, length=300)
cpu_bar.pack(pady=5)

mem_label = tk.Label(root, text="Memory:", font=("Arial", 14),
                     bg="#1e1e2f", fg="white")
mem_label.pack()

mem_bar = ttk.Progressbar(root, length=300)
mem_bar.pack(pady=5)

proc_label = tk.Label(root, text="Processes: 0", font=("Arial", 14),
                      bg="#1e1e2f", fg="white")
proc_label.pack(pady=10)

# Buffer to fix JSON error
buffer = ""

def update_data():
    global buffer
    try:
        data = client.recv(1024).decode()
        if not data:
            raise ConnectionError

        buffer += data

        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            info = json.loads(line)

            cpu = info["CPU"]
            mem = info["Memory"]
            proc = info["Processes"]

            # Update UI
            cpu_label.config(text=f"CPU: {cpu:.2f}%")
            cpu_bar['value'] = cpu

            mem_label.config(text=f"Memory: {mem:.2f}%")
            mem_bar['value'] = mem

            proc_label.config(text=f"Processes: {proc}")

            # Alerts
            if cpu > 90 or mem > 90:
                root.configure(bg="red")
                winsound.Beep(1000, 400)
            elif cpu > 80 or mem > 80:
                root.configure(bg="orange")
            else:
                root.configure(bg="#1e1e2f")

    except:
        cpu_label.config(text="Server disconnected")
        return

    root.after(5000, update_data)

update_data()
root.mainloop()