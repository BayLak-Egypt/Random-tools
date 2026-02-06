# 🌉 CloudBridge

**CloudBridge** is a powerful automation utility designed to seamlessly bridge your local development environment to the public internet. Built with Python, it automates the setup of an **Apache** web server and secures it using a **Cloudflare Tunnel (Argo)**, providing you with a public URL in seconds.



---

## ✨ Features

* **Dual Platform Support:** Fully compatible with **Linux** distributions (Ubuntu, Kali, Debian, etc.) and **Termux** on Android.
* **Auto-Dependency Handling:** Automatically detects and installs missing requirements like `apache2` and `cloudflared`.
* **Smart Port Management:** Scans for available ports to prevent conflicts and automatically updates server configurations.
* **Real-time Status:** Features a professional CLI with a custom loading spinner and ASCII art for a better user experience.
* **Secure Public Access:** Generates a temporary `https` link via Cloudflare, bypassing the need for port forwarding or static IPs.

---

## 🚀 Installation & Usage

### 1. Prerequisites
Ensure you have Python 3 installed on your system.

### 2. Run the Script
Clone your script or create a file named `CloudBridge.py`, then run:

**On Linux:**
```bash
sudo python3 main.py
On Termux:

Bash

python3 main.py
🛠 How it Works
System Check: Identifies if the environment is Termux or a standard Linux distro.

Service Setup: Starts the Apache service and configures the Listen ports.

Tunneling: Launches a Cloudflare Argo tunnel pointing to your local Apache port.

Expose: Extracts the public .trycloudflare.com URL from the logs and displays it in a clean UI box.

📂 Directory Paths
Depending on your system, the tool manages the following web roots:

Linux: /var/www/html

Termux: ~/../usr/share/apache2/default-site/htdocs

⚠️ Security Warning
CloudBridge is intended for development and testing purposes only. Once the tunnel is active, any files located in your web root directory will be accessible to anyone with the link. Do not host sensitive data or unencrypted configuration files.

📜 License
This project is open-source. Feel free to modify and distribute.

Created by: BayLak


---

**Would you like me to add a section for "Troubleshooting" or "Common Issues" to help users who might run into permission problems?**
