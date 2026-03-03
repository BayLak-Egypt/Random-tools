import sys
import time
GRAY = "\033[90m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"
def fancy_unicode_bar(total=63.6, width=50, speed=0.02):
    downloaded = 0
    step = 0.3
    while downloaded <= total:
        percent = downloaded / total
        filled_width = int(width * percent)
        remaining_width = width - filled_width
        if remaining_width > 0:
            bar = (RED + "━" * filled_width + GRAY + "╺" + GRAY + "━" * (remaining_width - 1))
        else:
            bar = RED + "━" * width
        sys.stdout.write(f"\r{bar}{RESET} {downloaded:.1f}/{total:.1f}MB")
        sys.stdout.flush()
        time.sleep(speed)
        downloaded += step
    final_bar = GREEN + "━" * width
    sys.stdout.write(f"\r{final_bar}{RESET} {total:.1f}/{total:.1f}MB\n")
if __name__ == "__main__":
    fancy_unicode_bar()