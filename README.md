# 🔐 SecureShare for IoT Devices

A secure peer-to-peer file and clipboard sharing system using **ECDH key exchange** and **AES encryption**. Built with a Python GUI (Tkinter) and powered by Flask for encrypted HTTP transfers — perfect for lightweight, private communication between IoT or personal devices over a secure network.

![SecureShare Banner](https://github.com/mohdabdullah0312/SecureShare/blob/main/utils/SecureShare.png)

---

## ✨ Features

- 🔑 **Elliptic Curve Diffie-Hellman (ECDH)** for secure key exchange
- 🔒 **AES Encryption** for data confidentiality
- 🖥️ **Tkinter GUI / CLI** for user-friendly interaction
- 🔁 **Clipboard & File Sharing** across devices
- 🌐 **Flask Server** for simple encrypted HTTP data transfer
- ⚡ **Fast & Lightweight**, suitable for IoT devices
- 🔁 **Two-way Key Exchange** with symmetric key derivation

---

## 📷 Architecture

```
+----------------+             +----------------+
|    Device A    |             |    Device B    |
| (Sender/Client)|             |(Receiver/Server)|
|                |             |                |
| GUI/CLI (Tkinter)           GUI/CLI (Tkinter) |
|                |             |                |
| Generate ECDH  |<-- Public -->| Generate ECDH  |
|  Key Pair      |             |  Key Pair      |
|                |             |                |
| AES Encrypt    |             | AES Decrypt    |
| File/Clipboard |             | File/Clipboard |
| Send via Flask | --> HTTP -->| Receive Flask  |
+----------------+             +----------------+
```

---

## 🚀 Getting Started

### 🧱 Prerequisites

- Python 3.8+
- Pip
- (Optional) Use our pre-built apps for Windows and Linux — no setup required!

### 📦 Installation

```bash
git clone https://github.com/mohdabdullah0312/SecureShare.git
cd SecureShare
pip install -r requirements.txt
```
> 💡 Use the `requirements_installer.py` script to install dependencies directly via the GUI if you skip the command line.

💡 Alternatively, use the pre-built apps for **Windows** and **Linux** — just run and go!
No need to install Python or pip.

---

## 🛠️ Usage

### Option 1: GUI Mode (Recommended)

```bash
python main.py
```

### Option 2: CLI Mode

```bash
python main.py --cli
```

### 🔁 Clipboard & File Transfer

- Select **Clipboard** or **File** mode in the GUI.
- Ensure both devices are running the app and connected over the same network.
- Exchange public keys (done automatically).
- Sender encrypts → Flask HTTP transfer → Receiver decrypts.

---

## 🔍 Tech Stack

- **Python 3**
- **Tkinter** – GUI Interface
- **Flask** – Local HTTP Server
- **ECDSA** – ECDH Key Generation
- **PyCryptodome** – AES Encryption/Decryption

---

## 📂 Folder Structure

```
SecureShare/
│
├── main.py                 # Entry point (GUI/CLI)
├── file_share.py         # Flask server handler
├── encryption_utils.py     # ECDH & AES logic
├── requirements_installer.py
├── utils/                  # Shared utilities
├── README.md
└── requirements.txt
```

---

## 🧪 Testing

To test file transfer:

1. Run `main.py` on **Device A** and **Device B**.
2. Ensure public key exchange occurs.
3. Try sending a `.txt`, `.pdf`, or clipboard text.
4. Confirm the decrypted file/data is correct on the receiver's end.

---

## 🔐 Security Notes

- ECDH ensures **ephemeral, symmetric key** generation per session.
- AES-256 encryption guarantees **confidentiality** of transferred data.
- Flask is bound to local or private IP (use Tailscale or VPN for secure remote access).

---

## 💡 Future Improvements

- 🔄 Persistent key store / session reuse
- 🌍 QR code scanning for public key sharing
- 📡 WebSocket/ZeroMQ backend for real-time interaction
- 📱 Android/Linux build with Kivy or PyQt
- 🌈 Theming and UI polish

---

## 🤝 Contributing

Contributions are welcome! Please fork the repo and submit a pull request.

```bash
git checkout -b feature/your-feature
git commit -m "Add some feature"
git push origin feature/your-feature
```

---

## 📜 License

MIT License © [Muhammad Abdullah Asim](https://github.com/mohdabdullah0312)

---

## 🙌 Acknowledgments

- [PyCryptodome](https://www.pycryptodome.org/)
- [ECDSA Python Library](https://github.com/warner/python-ecdsa)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Flask](https://flask.palletsprojects.com/)

---

> ⚠️ Disclaimer: This tool is for educational and personal use only. Ensure proper legal compliance when handling private data across networks.