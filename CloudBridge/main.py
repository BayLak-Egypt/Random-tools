import os
import re
import sys
import time
import subprocess
import threading
import socket
import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
R = "\033[91m"
W = "\033[0m"
B = "\033[1m"
chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
console = Console()
seen_ips = {}
def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]
def get_ip_info(ip):
   
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if response.get('status') == 'success':
            return f"{response.get('country')} ({response.get('countryCode')}) | {response.get('city')} | {response.get('isp')}"
        return "N/A"
    except:
        return "Failed"
def generate_table():
    table = Table(title="[bold cyan]visted[/bold cyan]", border_style="bright_blue")
    table.add_column("IP Address", style="cyan", no_wrap=True)
    table.add_column("Host", style="magenta")
    table.add_column("Location & ISP", style="green")
    table.add_column("User-Agent", style="white")
    table.add_column("Visits", style="bold red", justify="center")
    table.add_column("Last Seen", style="blue")
    sorted_ips = sorted(seen_ips.items(), key=lambda x: x[1]['last_seen'], reverse=True)
    for ip, data in sorted_ips:
        table.add_row(
            ip,
            data["host"],
            data["info"],
            data["ua"][:40] + "..." if len(data["ua"]) > 40 else data["ua"],
            str(data["count"]),
            data["last_seen"]
        )
    return table
def log_data(data):
    try:
        raw = data.decode('utf-8', errors='ignore')
        ua = re.search(r"User-Agent: (.*)\r", raw)
        host = re.search(r"Host: (.*)\r", raw)
        xff = re.search(r"X-Forwarded-For: (.*?)(,|\r)", raw)
        visitor_ip = xff.group(1).strip() if xff else None
        if not visitor_ip:
            return
        now = datetime.now().strftime("%H:%M:%S")
        if visitor_ip not in seen_ips:
            seen_ips[visitor_ip] = {
                "count": 1,
                "last_seen": now,
                "host": host.group(1) if host else "Unknown",
                "ua": ua.group(1) if ua else "N/A",
                "info": get_ip_info(visitor_ip)
            }
        else:
            seen_ips[visitor_ip]["count"] += 1
            seen_ips[visitor_ip]["last_seen"] = now
            if host: seen_ips[visitor_ip]["host"] = host.group(1)
    except Exception:
        pass
def bridge(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data: break
            if b"User-Agent" in data or b"X-Forwarded-For" in data:
                log_data(data)
            destination.sendall(data)
    except: pass
    finally:
        source.close()
        destination.close()
def start_sniffer(local_port, target_host, target_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', local_port))
    server.listen(10)
    while True:
        client_sock, addr = server.accept()
        target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            target_sock.connect((target_host, int(target_port)))
            threading.Thread(target=bridge, args=(client_sock, target_sock), daemon=True).start()
            threading.Thread(target=bridge, args=(target_sock, client_sock), daemon=True).start()
        except: client_sock.close()
def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    art = f"""{C}
              ⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
     ⠀⢠⠄⠀⡐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠳⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
     ⠀⡈⣀⡴⢧⣀⠀⠀⣀⣠⠤⠤⠤⠤⣄⣀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀
     ⠀⠀⠀⠘⠏⢀⡴⠊⠁⠀⠄⠀⠀⠀⠀⠈⠙⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀
     ⠀⠀⠀⠀⣰⠋⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠘⢶⣶⣒⡶⠦⣠⣀⠀
     ⠀⠀⢀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠈⣟⠲⡎⠙⢦⠈⢧
     ⠀⣠⢴⡾⢟⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡰⢃⡠⠋⣠⠋
     ⠞⣱⠋⢰⠁⢿⠀⠀⠀⠀⠄⢂⠀⠀⠀⠀⠀⣀⣠⠠⢖⣋⡥⢖⣩⠔⠊⠀⠀
     ⠹⢤⣈⣙⠚⠶⠤⠤⠤⠴⠶⣒⣒⣚⣨⠭⢵⣒⣩⠬⢖⠏⠁⢀⣀⠀⠀⠀
     ⠀⠈⠓⠒⠦⠍⠭⠭⣭⠭⠭⠭⠭⡿⡓⠒⠛⠉⠉⠀⠀⣠⠇⠀⠀⠘⠞⠀⠀⠀
     ⠀⠀⠀⠀⠀⠀⠈⠓⢤⣀⠀⠁⠀⠀⠀⠀⣀⡤⠞⠁⠀⣰⣆⠀⠀⠀⠀⠀Made By BayLak
     ⠀⠀⠀⠿⠀⠀⠀⠀⠀⠉⠉⠙⠒⠒⠚⠉⠁⠀⠀⠀⠁⢣⡎⠁⠀⠀⠀⠀
    {W}"""
    print(art)
    print(f"{G}{B}          [ CloudBridge v1.0 ]{W}")
    print(f"{C}--------------------------------------------------{W}")
def start_process():
    banner()
    try:
        t_host = input(f"{Y}[?] Target Host (127.0.0.1): {W}").strip() or "127.0.0.1"
        t_port = input(f"{Y}[?] Target Port (80): {W}").strip() or "80"
        random_port = get_free_port()
        threading.Thread(target=start_sniffer, args=(random_port, t_host, t_port), daemon=True).start()
        cmd = ["cloudflared", "tunnel", "--url", f"http://127.0.0.1:{random_port}"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        public_url = None
        idx = 0
        while True:
            line = proc.stdout.readline()
            if not line: break
            sys.stdout.write(f"\r{C}[{chars[idx % len(chars)]}] Creating Tunnel... {W}")
            sys.stdout.flush()
            idx += 1
            match = re.search(r"https://[-\w]+\.trycloudflare\.com", line)
            if match:
                public_url = match.group(0)
                break
            time.sleep(0.1)
        if public_url:
            banner()
            print(f"{G}╔══════════════════════════════════════════════════════{W}")
            print(f"{G}║{W} {B}BRIDGE MODE: {G}ACTIVE{W}                       ")
            print(f"{G}╠══════════════════════════════════════════════════════{W}")
            print(f"{C}║ [>] Target Site  :{W} {t_host}:{t_port}")
            print(f"{C}║ [>] Public Link  :{W} {Y}{B}{public_url}{W}")
            print(f"{C}║ [>] Local Proxy  :{W} 127.0.0.1:{random_port}")
            print(f"{G}╚══════════════════════════════════════════════════════{W}")

            with Live(generate_table(), refresh_per_second=2) as live:
                while True:
                    live.update(generate_table())
                    time.sleep(0.5)
        else:
            print(f"\n{R}[!] Error: Could not generate tunnel URL.{W}")
    except KeyboardInterrupt:
        print(f"\n{R}[-] Shutting down...{W}")
if __name__ == "__main__":
    start_process()
