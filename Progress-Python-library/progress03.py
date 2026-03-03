import sys
import time
GRAY = "\033[90m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"
def fancy_loading_bar(total=63.6, width=40, step=0.5, speed=0.05, head_symbol='>'):
    """
    شريط تحميل متقدم:
    - رمادي + أحمر تدريجي
    - رأس تحميل يتحرك
    - نسبة مئوية + الوقت
    - بعد الانتهاء يتحول كله أخضر مع وميض
    """
    downloaded = 0
    start_time = time.time()
    while downloaded <= total:
        percent = downloaded / total
        filled_width = int(width * percent)
        remaining_width = width - filled_width
        if filled_width < width:
            head = head_symbol if remaining_width > 0 else ''
            right_gray = "━" * (remaining_width - len(head))
            bar = RED + "━" * filled_width + head + GRAY + right_gray
        else:
            bar = RED + "━" * width
        elapsed = max(time.time() - start_time, 0.001)
        speed_current = downloaded / elapsed
        percent_display = int(percent * 100)
        eta = time.strftime('%H:%M:%S', time.gmtime(elapsed))
        sys.stdout.write(
            f"\r{bar}{RESET} {percent_display}% "
            f"{downloaded:.1f}/{total:.1f} MB "
            f"{speed_current:.1f} MB/s {eta}"
        )
        sys.stdout.flush()
        time.sleep(speed)
        downloaded += step
    for _ in range(2):
        bar = GREEN + "━" * width
        sys.stdout.write(f"\r{bar}{RESET} 100% {total:.1f}/{total:.1f} MB Done!   ")
        sys.stdout.flush()
        time.sleep(0.2)
        sys.stdout.write(f"\r{' ' * width}{RESET}")
        sys.stdout.flush()
        time.sleep(0.2)
    bar = GREEN + "━" * width
    sys.stdout.write(f"\r{bar}{RESET} 100% {total:.1f}/{total:.1f} MB Done!\n")
    sys.stdout.flush()
if __name__ == "__main__":
    fancy_loading_bar()