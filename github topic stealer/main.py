import sys
import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import threading


MAX_WORKERS = 10       
CHUNK_SIZE = 256 * 1024 
LOG_FILE = "download_log.json"


GREEN_BG = "\033[42m"
BLACK_TEXT = "\033[30m"
RESET = "\033[0m"

ASCII_ART = r"""
            /\
           /  \
      .---<    >---.
      |   _\  /_   |   
    _,',_|  \/  |_,',_ Github‑clone‑all topic downloader
_.-'     '-./\.-'     '-._
 '-._   _.-'\/'-._   _.-'
     `,` |__/\__| `,`     Created by baylak 
      |    /  \    |
      '---<    >---'
           \  /
            \/                                     
"""

HEADERS = {
    "User-Agent": "topic-fast-downloader"
}


line_counter = 0
line_lock = threading.Lock()

def print_line(msg):
    global line_counter
    with line_lock:
        line_counter += 1
        print(f"[{line_counter}] {msg}")


def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_log(log_data):
    with open(LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=2)

def format_size(size_kb):
    if size_kb >= 1024 * 1024:
        return f"{size_kb / (1024 * 1024):.2f} GB"
    elif size_kb >= 1024:
        return f"{size_kb / 1024:.2f} MB"
    else:
        return f"{size_kb} KB"

def discover_repos(topic):
    print(ASCII_ART)
    print_line(f"[*] Discovering repositories for topic: {topic}\n")
    repos = []
    page = 1
    total_found = 0

    while True:
        url = f"https://api.github.com/search/repositories?q=topic:{topic}&per_page=100&page={page}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print_line(f"[!] API Error {r.status_code}")
            break

        items = r.json().get("items", [])
        if not items:
            break

        for repo in items:
            repos.append({
                "name": repo["full_name"].replace("/", "_"),
                "owner": repo["owner"]["login"],
                "repo": repo["name"],
                "url": repo["html_url"],
                "size": repo.get("size", 0)
            })
        total_found += len(items)
        print_line(f"[+] Repositories discovered: {total_found}")
        page += 1

    print_line(f"[✓] Total repositories discovered: {len(repos)}\n")
    return repos

def get_default_branch(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            return r.json().get("default_branch", "main")
    except:
        pass
    return "main"

def get_unique_path(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    i = 1
    while True:
        new_path = f"{base}-{i}{ext}"
        if not os.path.exists(new_path):
            return new_path
        i += 1

def download_zip(url, path):
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            if r.status_code != 200:
                return False
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
        return True
    except Exception as e:
        print_line(f"[!] Error downloading {url}: {e}")
        return False


def download_repo(index, repo, folder, total, log_data, results):
    size_text = format_size(repo["size"])
    box = f"{GREEN_BG}{BLACK_TEXT} {size_text} {RESET}"


    if repo["name"] in log_data:
        results[index] = f"{repo['url']} {box} [SKIPPED - already downloaded]"
        return

    path = os.path.join(folder, f"{repo['name']}.zip")
    path = get_unique_path(path)

    branch = get_default_branch(repo["owner"], repo["repo"])
    url = f"https://codeload.github.com/{repo['owner']}/{repo['repo']}/zip/refs/heads/{branch}"

    print_line(f"{repo['url']} {box} [DOWNLOADING]")

    if download_zip(url, path):
        log_data[repo["name"]] = {
            "path": path,
            "url": repo["url"],
            "branch": branch,
            "size_kb": repo["size"],
            "downloaded_at": str(datetime.now())
        }
        save_log(log_data)
        results[index] = f"{repo['url']} {box} [DOWNLOADED]"
    else:
        results[index] = f"{repo['url']} {box} [FAILED]"

def download_all(topic, repos):
    os.makedirs(topic, exist_ok=True)
    log_data = load_log()
    total = len(repos)
    results = [None] * total

    print_line(f"[*] Downloading {total} repositories (FAST MODE)\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(download_repo, i, repo, topic, total, log_data, results) for i, repo in enumerate(repos)]
        for _ in as_completed(futures):
            pass


    print_line("\n[✓] All downloads finished\n")
    for line in results:
        if line:
            print_line(line)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <topic>")
        sys.exit(1)

    topic = sys.argv[1]
    repos = discover_repos(topic)
    print_line(f"\n[✓] Found {len(repos)} repositories")
    download_all(topic, repos)

