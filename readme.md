# CMPT 371 A3 Socket Programming `Encrypted Chat & File Transfer`

**Course:** CMPT 371 – Data Communications & Networking  
**Instructor:** Mirza Zaeem Baig  
**Semester:** Spring 2026

<span style="color: purple;">**_RUBRIC NOTE: Only one group member will submit the repository link on Canvas._**</span>

---

## **Group Members**

| Name          | Student ID | Email         |
| :------------ | :--------- | :------------ |
| Srinjay Mitra | 301582986  | sma367@sfu.ca |

---

## **1. Project Overview & Description**

This project implements a **secure, encrypted chat application** with optional **file transfer** using Python TCP sockets. Features include:

- Real-time **text chat** between multiple clients.
- **End-to-end encryption** for all messages and files.
- **Simple, dark-themed GUI** using Tkinter.
- Safe **file transfer** with file headers, ensuring the connection remains stable.

The server handles all client connections, message broadcast, and file reception, guaranteeing an **authoritative source** for all communication and preventing message loss or corruption.

---

## **2. System Limitations & Edge Cases**

- **Multiple Clients:**
  - <span style="color: green;">_Solution:_</span> Python `threading` handles multiple clients concurrently. Each client connection runs in a daemon thread for non-blocking operation.
  - <span style="color: red;">_Limitation:_</span> Thread creation is limited by system resources; high-scale deployments would require async networking (`asyncio`) or a thread pool.

- **TCP Stream Handling:**
  - <span style="color: green;">_Solution:_</span> File transfer uses a header (`FILE:<filename>:<size>\n`) and then reads the exact number of bytes to avoid TCP buffering issues. Chat messages are split using an application-level newline delimiter (`\n`).

- **Security & Validation:**
  - <span style="color: green;">_Solution:_</span> All messages and files are encrypted before transmission.
  - <span style="color: red;">_Limitation:_</span> The client assumes a valid message format; malicious users could manipulate the client to send invalid data.

---

## **3. Video Demo**

<span style="color: purple;">**_RUBRIC NOTE: Include a clickable link._**</span>

Our 2-minute video demo covers:

- Client connection
- Real-time encrypted chat
- File transfer workflow
- Graceful disconnection

[**▶️ Watch Project Demo on YouTube**](https://youtu.be/KFpFTYBKZA8)

---

## **4. Prerequisites**

- Python **3.10** or higher
- Standard libraries only: `socket`, `threading`, `tkinter`, `os`, `random`
- Optional: VS Code or Terminal

<span style="color: purple;">**_RUBRIC NOTE: No external pip libraries required._**</span>

---

## **5. Project File Structure**

```bash
encryptedChat/
│
├─ client.py # GUI client script
├─ server.py # Server script handling
```

---

## **6. Step-by-Step Run Guide**

<span style="color: purple;">**_RUBRIC NOTE: Grader must be able to copy-paste these commands._**</span>

### **Step 1: Start the Server**

```bash
#install dependencies
pip install -r requirements.txt


# start the server
python3 server.py

# Console: "[START] Server listening on 127.0.0.1:5050"ing connections and broadcast
├─ config.py # HOST and PORT configuration
├─ crypto.py # Encryption/decryption helper functions
├─ README.md # This documentation
```

# Step 2: Connect a Client

### Open a new terminal for each client and run:

```bash
python3 client.py
# GUI launches
# Chat area shows: "[INFO] You joined as <GeneratedUsername>"
```

### Step 3: Chat and Send Files

- Type a message and press Enter or click Send.
- Click Send File to choose a file. The file is encrypted and sent safely.
- All clients see broadcast messages and file notifications.

### Step 4: Disconnect

- Closing the window sends `[INFO] <username> has left the chat.`
- Server remains running for other clients.

## 7. Technical Protocol Details (Encrypted TCP)

- **Chat Messages:** AES-encrypted UTF-8 strings.
- **File Transfer:**
  - Header: `FILE:<filename>:<size>\n`
  - Followed by exactly `<size>` bytes of raw file data.
- **Message Broadcast:** Server relays all messages/files to all connected clients.
- **Encryption:** AES-based symmetric encryption (see `crypto.py`) ensures end-to-end confidentiality.

## 8. Academic Integrity & References

- **Code Origin:** Socket boilerplate adapted from course TCP Echo Server tutorial. GUI design and threading logic written by the group.
- **GenAI Usage:**
  - ChatGPT assisted in GUI layout and encryption-safe protocols.
  - GitHub Copilot helped plan threading workflow and header-based file transfer.
- **References:**
  - Python Socket Programming HOW TO
  - Tkinter GUI Documentation
  - Real Python: Intro to Python Threading
