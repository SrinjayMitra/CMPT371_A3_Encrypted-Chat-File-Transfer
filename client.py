import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog
from config import HOST, PORT
from crypto import encrypt, decrypt
import random
import os

# ---------------- NETWORK ---------------- #
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# ---------------- USERNAME ---------------- #
adjectives = ["Silent","Neon","Cosmic","Shadow","Epic","Frozen","Wild",
              "Crimson","Electric","Mystic","Turbo","Golden","Phantom"]
nouns = ["Falcon","Penguin","Ninja","Tiger","Dragon","Wizard",
         "Panda","Hacker","Samurai","Knight","Ghost","Robot"]

def generate_username():
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    number = random.randint(10, 99)
    return f"{adj}{noun}{number}"

username = generate_username()

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("🔒 Encrypted Chat")
root.geometry("500x600")
root.configure(bg="#1E1E1E")

# Header
header = tk.Label(root, text=f"Logged in as {username}", bg="#1E1E1E", fg="#FFD700", font=("Consolas", 12, "bold"))
header.pack(pady=5)

# Chat area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#2E2E2E", fg="#FFFFFF", font=("Consolas", 11))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.config(state=tk.NORMAL)

# Message entry
msg_entry = tk.Entry(root, bg="#3E3E3E", fg="#FFFFFF", font=("Consolas", 11), insertbackground='white')
msg_entry.pack(padx=10, pady=5, fill=tk.X)
msg_entry.focus()

# Buttons
send_btn = tk.Button(root, text="Send", command=lambda: send_message(), bg="#FFD700", fg="#1E1E1E", font=("Consolas", 11, "bold"))
send_btn.pack(pady=5)

file_btn = tk.Button(root, text="Send File", command=lambda: send_file(), bg="#FFD700", fg="#1E1E1E", font=("Consolas", 11, "bold"))
file_btn.pack(pady=5)

msg_entry.bind("<Return>", lambda event: send_message())

# ---------------- FUNCTIONS ---------------- #
# def receive_messages():
#     while True:
#         try:
#             data = client.recv(8192)
#             if not data:
#                 continue
            
#             # Check if data is a file
#             if data.startswith(b"FILE:"):
#                 # Split: FILE:filename:encrypted_content
#                 parts = data.split(b":", 2)
#                 filename = parts[1].decode()
#                 encrypted_content = parts[2]

#                 save_path = filedialog.asksaveasfilename(initialfile=filename)
#                 if save_path:
#                     with open(save_path, "wb") as f:
#                         f.write(decrypt(encrypted_content))
#                     chat_area.insert(tk.END, f"[INFO] Received file: {filename}\n")
#                     chat_area.yview(tk.END)
#                 continue

#             # Otherwise it's a regular message
#             message = decrypt(data)
#             chat_area.insert(tk.END, message + "\n")
#             chat_area.yview(tk.END)

#         except:
#             chat_area.insert(tk.END, "[ERROR] Connection lost\n")
#             break

def receive_messages():

    while True:

        try:

            data = client.recv(8192)

            if not data:
                continue

            # ---------- FILE HEADER ----------
            if data.startswith(b"FILE:"):

                parts = data.split(b":", 2)

                filename = parts[1].decode()

                file_size = int(parts[2].decode())

                received_data = b''

                while len(received_data) < file_size:

                    chunk = client.recv(4096)

                    if not chunk:
                        break

                    received_data += chunk

                decrypted_file = decrypt(received_data)

                save_path = filedialog.asksaveasfilename(
                    initialfile=filename
                )

                if save_path:

                    with open(save_path, "wb") as f:
                        f.write(decrypted_file)

                chat_area.insert(
                    tk.END,
                    f"[INFO] Received file: {filename}\n"
                )

                chat_area.yview(tk.END)

                continue

            # ---------- NORMAL MESSAGE ----------

            message = decrypt(data).decode()

            chat_area.insert(
                tk.END,
                message + "\n"
            )

            chat_area.yview(tk.END)

        except Exception as e:

            chat_area.insert(
                tk.END,
                f"[ERROR] Connection lost: {e}\n"
            )

            break

def send_message():
    msg = msg_entry.get()
    if msg.strip() == "":
        return
    full_msg = f"{username}: {msg}"
    encrypted_msg = encrypt(full_msg)
    try:
        client.send(encrypted_msg)
    except:
        chat_area.insert(tk.END, "[ERROR] Failed to send message\n")
        return
    chat_area.insert(tk.END, "You: " + msg + "\n")
    chat_area.yview(tk.END)
    msg_entry.delete(0, tk.END)

# def send_file():
#     file_path = filedialog.askopenfilename()
#     if not file_path:
#         return
#     filename = os.path.basename(file_path)
#     with open(file_path, "rb") as f:
#         file_data = f.read()
#     encrypted_data = encrypt(file_data)
#     try:
#         client.send(b"FILE:" + filename.encode() + b":" + encrypted_data)
#         chat_area.insert(tk.END, f"[INFO] Sent file: {filename}\n")
#         chat_area.yview(tk.END)
#     except:
#         chat_area.insert(tk.END, "[ERROR] Failed to send file\n")
def send_file():
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    filename = os.path.basename(file_path)

    try:
        with open(file_path, "rb") as f:
            file_data = f.read()

        encrypted_data = encrypt(file_data)

        # Send header with filename and size
        header = (
            b"FILE:"
            + filename.encode()
            + b":"
            + str(len(encrypted_data)).encode()
        )

        client.send(header)

        # Small pause ensures header arrives first
        import time
        time.sleep(0.1)

        # Send encrypted file
        client.sendall(encrypted_data)

        chat_area.insert(
            tk.END,
            f"[INFO] Sent file: {filename}\n"
        )

        chat_area.yview(tk.END)

    except Exception as e:
        chat_area.insert(
            tk.END,
            f"[ERROR] Failed to send file: {e}\n"
        )


def on_closing():
    try:
        leave_msg = f"[INFO] {username} has left the chat."
        client.send(encrypt(leave_msg))
    except:
        pass
    client.close()
    root.destroy()

# ---------------- START ---------------- #
root.protocol("WM_DELETE_WINDOW", on_closing)

# Send join notification
try:
    join_msg = f"[INFO] {username} has joined the chat."
    client.send(encrypt(join_msg))
except:
    pass

threading.Thread(target=receive_messages, daemon=True).start()
chat_area.insert(tk.END, f"[INFO] You joined as {username}\n\n")
root.mainloop()