import sys
import time
def format_size(size):
    return f"{size:.1f}"
def progress_bar(total, width=40):
    start_time = time.time()
    downloaded = 0
    while downloaded <= total:
        percent = downloaded / total
        filled = int(width * percent)
        bar = "━" * filled + " " * (width - filled)
        elapsed = time.time() - start_time
        speed = downloaded / elapsed if elapsed > 0 else 0
        remaining = (total - downloaded) / speed if speed > 0 else 0
        sys.stdout.write(
            f"\r{bar} {format_size(downloaded)}/{format_size(total)} MB "
            f"{speed:.1f} MB/s {time.strftime('%H:%M:%S', time.gmtime(elapsed))}"
        )
        sys.stdout.flush()
        time.sleep(0.1)
        downloaded += 0.5
    print()
if __name__ == "__main__":
    progress_bar(63.6)