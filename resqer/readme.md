# resqer project

## 🔒 Overview

**resqer** is a **simple encrypted chat application** designed to demonstrate strong encryption combined with stealthy data representation on the network.

Each client is assigned a **random, unique encryption key**, and all messages are protected using **AES-EAX authenticated encryption**. Before transmission, encrypted data is encoded into **dots (`.`) and spaces (` `)** only, making the payload appear meaningless in packet sniffers.

The goal of resqer is:

* Secure message exchange
* No readable plaintext in packet captures
* Simple and clear architecture

---

## ✨ Features

* 💬 Simple client/server chat
* 🔑 Random encryption key per client
* 🔐 Strong encryption using **AES-EAX**
* 🫥 Stealth encoding using dots and spaces
* 📡 Payload appears unreadable in packet sniffers
* 🧪 Ideal for learning and experimentation

---

## 🧠 How It Works

### Sending a message

```
Message
  ↓
AES-EAX Encryption (per-client random key)
  ↓
Encrypted bytes
  ↓
Binary (0 / 1)
  ↓
0 → .
1 → space
  ↓
Sent over TCP
```

### Receiving a message

```
Dots & spaces payload
  ↓
Binary
  ↓
Encrypted bytes
  ↓
AES-EAX Decryption
  ↓
Original message
```

---

## 🛠️ Requirements

* Python 3.8+
* PyCryptodome

Install dependencies:

```bash
pip install pycryptodome
```

---

## 📂 Project Structure

```
resqer/
│
├── crypto_utils.py    # Encryption and random key generation
├── client.py          # Chat client
├── server.py          # Chat server
└── README.md
```

---

## 🚀 Basic Usage Example

### Generate a random key

```python
from crypto_utils import generate_key
key = generate_key(16)
```

### Encrypt and encode a message

```python
cipher = encrypt(key, b"Hello resqer")
binary = bytes_to_binary(cipher)
payload = binary_to_dots_spaces(binary)
```

### Decode and decrypt after receiving

```python
binary = dots_spaces_to_binary(payload)
raw = binary_to_bytes(binary)
plain = decrypt(key, raw)
print(plain.decode())
```

---

## 🕵️ What Packet Sniffers See

* Normal TCP/IP headers
* Unreadable payload
* No plaintext
* No structured formats (JSON, Base64, etc.)

Example output:

```
E..@.@........
..............
```

This behavior is **expected** and indicates that resqer is functioning correctly.

---

## ⚠️ Security Notes

* This project is intended for **educational and research purposes only**
* Do not use for illegal activities
* Always use strong, random keys
* Do not reuse keys across clients

---

## 🧪 Possible Future Improvements

* ⏱️ Random timing delays between packets
* 📦 Micro-packet fragmentation
* 🔀 Random padding patterns
* 🌐 Traffic blending with common protocols

---

## 📜 License

MIT License

---

## 👤 Author

Developed by **BayLak - Egypt**
