import sys
import requests

GREEN_BG = "\033[42m"
BLACK_TEXT = "\033[30m"
RESET = "\033[0m"

def format_size(size_kb):

    if size_kb >= 1024 * 1024:
        return f"{size_kb / (1024 * 1024):.2f} GB"
    elif size_kb >= 1024:
        return f"{size_kb / 1024:.2f} MB"
    else:
        return f"{size_kb} KB"

def stream_repo_links(topic):
    page = 1
    total = 0

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "topic-stealer"
    }

    print(f"[*] Starting fetch for topic: {topic}\n")

    while True:
        api_url = (
            f"https://api.github.com/search/repositories"
            f"?q=topic:{topic}&per_page=100&page={page}"
        )

        r = requests.get(api_url, headers=headers)
        if r.status_code != 200:
            print(f"[!] Error: {r.status_code} - {r.text}")
            break

        data = r.json()
        items = data.get("items", [])
        if not items:
            break

        print(f"[+] Page {page} ({len(items)} repos)")

        for repo in items:
            total += 1
            size_kb = repo.get('size', 0)
            size_text = format_size(size_kb)
            green_box = f"{GREEN_BG}{BLACK_TEXT} {size_text} {RESET}"
            print(f"[{total}] {repo['html_url']}  {green_box}")

        page += 1

    print(f"\n[✓] Done. Total repositories: {total}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <topic>")
        sys.exit(1)

    topic = sys.argv[1]
    stream_repo_links(topic)

