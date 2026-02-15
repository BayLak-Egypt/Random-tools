

<img src="https://raw.githubusercontent.com/BayLak-Egypt/Random-tools/refs/heads/main/Nominalist/icon.png?token=GHSAT0AAAAAADQIYFFCO4P2DMJ6TPZBOX6A2MR6QRQ" width="500">
# 🛠️ Name Tools: Nominalist

A collection of simple, fast, and professional Python tools for managing and auditing **Wordlists**. These tools give you full control over inspecting, searching, and cleaning your text files efficiently.

---

## 🚀 Available Tools

### 1️⃣ `getname.py`
A powerful utility for extracting and searching for names or patterns within a wordlist.
* **Core Function:** Displays duplicate names or performs specific searches.
* **Key Features:** Supports partial matching, case-insensitivity, and result exporting.

### 2️⃣ `delname.py`
A cleaning utility designed to remove unwanted entries from your wordlists.
* **Core Function:** Deletes specific lines or names from a file.
* **Key Features:** Live feedback of deleted entries to ensure accuracy.

---

## 🟢 getname.py Usage Guide

### Description
Analyze large text files to find duplicates or specific keywords based on your custom criteria.

### Command Line Options
| Option | Description |
| :--- | :--- |
| `-s, --search NAME` | Search for a specific name or word in the file. |
| `-f, --filter` | Enable **Partial Matching** (finds the word even if it's part of a line). |
| `-u, --ignore-case` | Ignore **Case Sensitivity** (Upper/Lower case) during search. |
| `-o, --output FILE` | Export the found results to an external text file. |
| `-h, --help` | Display the help menu. |

### Practical Examples
* **Show all duplicate names:**
    ```bash
    python3 getname.py wordlist.txt
    ```
* **Advanced search for "hello":**
    ```bash
    python3 getname.py wordlist.txt -s hello -f -u -o results.txt
    ```

---

## 🔴 delname.py Usage Guide

### Description
A rapid tool for purging unwanted entries from your wordlist with real-time reporting of what has been removed to prevent accidental data loss.

---

## 📊 Example Output

When running a search, the results are presented in a clean, organized table:

```text
Line      Name
-------------------------
1         hello
3         hello123
4         Hello_User
-------------------------
Total Rows: 3
✅ Saved results to 'results.txt'
