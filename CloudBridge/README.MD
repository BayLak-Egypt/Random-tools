# 🌉 CloudBridge

> **Bridge your local Apache server to the public internet — quickly, automatically, and securely through Cloudflare Tunnel.**

**CloudBridge** is a Python-based automation utility that simplifies the process of exposing a local **Apache web server** to the public internet.

The tool automatically detects the environment, handles required dependencies, configures Apache, finds an available port when necessary, launches a temporary **Cloudflare Tunnel**, and extracts the generated public HTTPS URL.

Designed primarily for **development, testing, demonstrations, and temporary deployments**.

---

## ✨ Features

* 🐧 **Linux Support**

  * Ubuntu
  * Debian
  * Kali Linux
  * Other Debian-based distributions

* 📱 **Termux Support**

  * Designed to work on Android through Termux.

* ⚙️ **Automatic Dependency Management**

  * Detects missing dependencies.
  * Helps install required components such as:

    * `apache2`
    * `cloudflared`

* 🔌 **Smart Port Management**

  * Detects available ports.
  * Helps avoid port conflicts.
  * Automatically adjusts Apache configuration when required.

* ☁️ **Cloudflare Tunnel Integration**

  * Creates a temporary public HTTPS endpoint.
  * No port forwarding required.
  * No static public IP required.

* 🖥️ **Professional CLI**

  * Custom ASCII banner.
  * Loading indicators.
  * Real-time status messages.
  * Clean terminal output.

* 🔗 **Automatic URL Detection**

  * Detects the generated Cloudflare Tunnel URL directly from the tunnel output.
  * Displays the public URL in an easy-to-copy format.

---

## 🧰 Requirements

Before running CloudBridge, make sure Python 3 is installed.

### Linux

```bash
python3 --version
```

### Termux

```bash
python3 --version
```

If Python is not installed, install it using your system's package manager.

---

# 🚀 Installation & Usage

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/CloudBridge.git
cd CloudBridge
```

> Replace `YOUR_USERNAME` with your GitHub username.

---

## 2. Run CloudBridge

### 🐧 Linux

Apache and system-level configuration may require administrator privileges:

```bash
sudo python3 main.py
```

### 📱 Termux

Run:

```bash
python3 main.py
```

CloudBridge will automatically detect the environment and configure the appropriate paths and services.

---

# ⚙️ How It Works

CloudBridge follows a simple automated workflow:

```text
┌──────────────────────┐
│   Start CloudBridge  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Detect Environment  │
│ Linux / Termux       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Check Dependencies   │
│ Apache / cloudflared │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Configure Apache     │
│ & Select Port        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Start Apache Server  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Start Cloudflare     │
│ Tunnel                │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Detect Public HTTPS  │
│ URL                   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     CloudBridge      │
│        Ready         │
└──────────────────────┘
```

### 1. Environment Detection

CloudBridge identifies whether it is running on:

* Standard Linux
* Termux / Android

This allows it to use the appropriate Apache paths and service-management commands.

### 2. Dependency Check

The tool checks whether the required components are available.

Depending on the environment, this may include:

```text
Python 3
Apache
Cloudflared
```

Missing dependencies can be handled automatically where supported.

### 3. Apache Configuration

CloudBridge prepares the local Apache server and determines which port should be used.

If the default port is unavailable, the tool can search for another available port to avoid conflicts.

### 4. Cloudflare Tunnel

After Apache is running, CloudBridge starts a temporary Cloudflare Tunnel that forwards traffic to the local Apache server.

### 5. Public URL

The generated Cloudflare URL is detected from the tunnel output and displayed by CloudBridge.

The resulting URL can then be used to access the local web server remotely.

---

# 📂 Web Root Paths

CloudBridge uses different Apache document roots depending on the environment.

### Linux

```text
/var/www/html
```

Place your website files inside this directory.

Example:

```text
/var/www/html/
├── index.html
├── style.css
├── script.js
└── images/
```

### Termux

The Apache document root may be located at:

```text
~/../usr/share/apache2/default-site/htdocs
```

The exact path may vary depending on the Termux/Apache installation.

---

# 🌐 Example

Suppose your local Apache server contains:

```text
index.html
```

After launching CloudBridge, the terminal may display a generated public address similar to:

```text
https://example-random-name.trycloudflare.com
```

Opening the URL allows the Apache website running on your local machine or Android device to be accessed through the internet.

> The generated address is temporary and may change whenever a new tunnel is created.

---

# 🔒 Security Considerations

CloudBridge is primarily intended for:

* Development
* Testing
* Demonstrations
* Temporary web hosting
* Local project previews

Once a public tunnel is active, your local web server may become accessible from the internet.

### ⚠️ Do not expose sensitive files

Avoid placing the following inside your public web root:

```text
.env
config files
database backups
private keys
password files
API credentials
personal documents
```

Also remember that Apache configuration and directory permissions should be reviewed before exposing a server publicly.

**Only expose content that you are comfortable making publicly accessible.**

---

# 🛡️ Important Note About Cloudflare Tunnel

CloudBridge uses a temporary Cloudflare Tunnel endpoint.

The tunnel itself does not automatically make your application secure.

You are still responsible for:

* Web application security
* Apache configuration
* File permissions
* Authentication
* Sensitive information
* Application vulnerabilities

A public URL means that external users may be able to reach the exposed service.

---

# 🐛 Troubleshooting

## Apache fails to start

Check whether another service is already using the configured port.

On Linux, you can inspect listening ports with:

```bash
sudo ss -tulpn
```

You can also verify Apache's status:

```bash
sudo systemctl status apache2
```

---

## Permission denied

On Linux, try running CloudBridge with administrator privileges:

```bash
sudo python3 main.py
```

Be careful when running scripts with `sudo` and only use code you trust.

---

## Cloudflared is not found

Verify that `cloudflared` is available:

```bash
cloudflared --version
```

If it is missing, install it using the appropriate installation method for your operating system.

---

## Website does not appear

Check the following:

1. Apache is running.
2. The selected port is correct.
3. Your website files are inside the correct document root.
4. `index.html` exists if your site depends on it.
5. Cloudflared is forwarding traffic to the same port Apache is listening on.

---

# 📁 Project Structure

A typical CloudBridge project can look like this:

```text
CloudBridge/
│
├── main.py
├── README.md
└── LICENSE
```

Additional files may be added as the project evolves.

---

# 🧪 Intended Use

CloudBridge is useful for quickly testing projects that normally run only on:

```text
localhost
```

For example:

```text
Local Apache
     │
     ▼
127.0.0.1:PORT
     │
     ▼
CloudBridge
     │
     ▼
Cloudflare Tunnel
     │
     ▼
Public HTTPS URL
```

This makes it convenient to share a development website temporarily without configuring traditional router port forwarding.

---

# 📜 License

This project is open-source.

You are free to:

* Use the project
* Modify the source code
* Improve the implementation
* Redistribute modified versions

See the project's `LICENSE` file for the applicable license terms.

---

# 👤 Author

**Created by BayLak**

CloudBridge is part of the **BayLak** project ecosystem.

---

## ⭐ Contributing

Contributions, bug reports, and improvements are welcome.

If you find a problem or have an idea for improving CloudBridge, feel free to open an issue or submit a pull request.

---

## ⚠️ Disclaimer

CloudBridge is provided for legitimate development, testing, and educational purposes.

The author is not responsible for misuse, security issues, data exposure, or damage resulting from improper configuration or use of the tool.

**Use responsibly and only expose systems and content that you own or have permission to expose.**
