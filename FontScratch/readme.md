# FontScratch

### Your Path Toward Building Systems

**FontScratch** is a lightweight command-line tool made for **Scratch** and Scratch-related development.

It allows you to convert **TTF** and **OTF** font files into Scratch-compatible `.sprite3` files, making custom font asset creation easier for Scratch projects and tools.

> **Made by BayLak.**

---

## ✨ Features

* 🎨 Designed for **Scratch**.
* 🔤 Supports **TrueType Font (`.ttf`)**.
* 🔤 Supports **OpenType Font (`.otf`)**.
* 📦 Generates Scratch-compatible `.sprite3` files.
* 🏷️ Supports custom Sprite names.
* 🚀 Simple command-line interface.
* ⚡ Lightweight and easy to use.
* 💻 Works from Terminal or CMD.
* ℹ️ Built-in `--about` page.
* ❓ Built-in `-h` / `--help` page.
* 🌐 Fetches BayLak social links live from GitHub.

---

## 📋 Requirements

### Python

FontScratch requires **Python 3**.

Check your Python version:

```bash
python --version
```

or:

```bash
python3 --version
```

### Pillow

Install the required Pillow library:

```bash
pip install Pillow
```

---

## 💻 Usage

The basic command is:

```bash
python main.py <font>
```

FontScratch automatically detects whether the input file is a `.ttf` or `.otf` font.

---

## 🔤 TTF Font

Convert a TrueType font:

```bash
python main.py myfont.ttf
```

The output name will automatically be taken from the font filename.

For example:

```text
myfont.ttf
    ↓
myfont.sprite3
```

---

## 🔤 OTF Font

Convert an OpenType font:

```bash
python main.py myfont.otf
```

Example:

```text
myfont.otf
    ↓
myfont.sprite3
```

---

## 🏷️ Custom Output Name

Use `-o` or `--output` to specify a custom Sprite name:

```bash
python main.py myfont.ttf -o ScratchFont
```

or:

```bash
python main.py myfont.otf --output ScratchFont
```

The generated file will be:

```text
ScratchFont.sprite3
```

You can also provide the `.sprite3` extension:

```bash
python main.py myfont.otf -o ScratchFont.sprite3
```

FontScratch will prevent the extension from being duplicated.

---

## ❓ Help

Display the FontScratch help page with:

```bash
python main.py -h
```

or:

```bash
python main.py --help
```

The help page shows the available commands, options, and usage syntax.

---


## 📌 Command Syntax

```text
python main.py <font> [-o <output_name>]
```

### Arguments

| Argument   | Description                          |
| ---------- | ------------------------------------ |
| `font`     | Path to a `.ttf` or `.otf` font file |
| `-o`       | Set a custom Sprite name             |
| `--output` | Set a custom Sprite name             |
| `-h`       | Display the help page                |
| `--help`   | Display the help page                |
| `--about`  | Display the FontScratch About Page   |

---

## 🧪 Examples

### Convert TTF

```bash
python main.py Arial.ttf
```

### Convert OTF

```bash
python main.py Arial.otf
```

### Custom Sprite Name

```bash
python main.py MyFont.ttf -o MyScratchFont
```

### Custom Sprite Name with OTF

```bash
python main.py MyFont.otf -o MyScratchFont
```

### Show Help

```bash
python main.py -h
```

### Show About

```bash
python main.py --about
```

---

## 🎨 Scratch Workflow

FontScratch is designed to simplify the workflow of preparing custom font assets for **Scratch**.

```text
TTF / OTF Font
      │
      ▼
   FontScratch
      │
      ▼
Scratch Sprite3
      │
      ▼
 Scratch Project
```

Example:

```text
ScratchFont.otf
      │
      ▼
python main.py ScratchFont.otf -o ScratchFont
      │
      ▼
ScratchFont.sprite3
```

---

## 🧩 Scratch Use Cases

FontScratch can be useful for developers and creators working with:

* 🎮 Scratch Projects
* 🧱 Scratch Tools
* 🛠️ Scratch Utilities
* 🎨 Scratch UI Development
* 🔤 Scratch Font Resources
* 🌐 Scratch Website-related Projects
* 🧩 Scratch Extensions and Tools
* 📦 Scratch Asset Processing

---

## 📁 Project Structure

A basic FontScratch project can look like:

```text
FontScratch/
│
├── main.py
├── README.md
└── fonts/
    ├── MyFont.ttf
    └── MyFont.otf
```

---

## ⚠️ Notes

* Python 3 is required.
* Pillow is required.
* Both `.ttf` and `.otf` formats are supported.
* Make sure the font path is correct.
* Use quotation marks if the font path contains spaces.
* Make sure you have permission to use the font files you process.
* Internet access is only required for retrieving the live BayLak social links.
* The generated `.sprite3` file is intended for Scratch-related workflows.

---

## 🚀 Why FontScratch?

Working with custom font assets for **Scratch** can involve repetitive manual steps.

FontScratch provides a simple command-line workflow:

```bash
python main.py ScratchFont.otf -o ScratchFont
```

Result:

```text
ScratchFont.sprite3
```

Simple, lightweight, and built with **Scratch** in mind.

---

## ⭐ Support

If FontScratch is useful for your **Scratch projects or development tools**, consider giving the project a ⭐ on GitHub.

**Made by BayLak ❤️**
