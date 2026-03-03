import sys
import time
GRAY = "\033[90m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"
def tqdm_style_bar(total=63.6, width=40, speed=0.05):
    start_time = time.time()
    downloaded = 0
    step = 0.5
    while downloaded <= total:
        percent = downloaded / total
        filled_length = int(width * percent)
        bar = RED + '█' * filled_length + GRAY + ' ' * (width - filled_length) + RESET
        elapsed_time = time.time() - start_time
        velocity = downloaded / elapsed_time if elapsed_time > 0 else 0
        remaining_mb = total - downloaded
        eta = remaining_mb / velocity if velocity > 0 else 0
        elapsed_str = time.strftime("%M:%S", time.gmtime(elapsed_time))
        eta_str = time.strftime("%M:%S", time.gmtime(eta))
        output = (
            f"\r{percent:>3.0%}|{bar}| "
            f"{downloaded:.1f}/{total:.1f} MB "
            f"[{elapsed_str}<{eta_str}, {velocity:.2f}MB/s]"
        )
        sys.stdout.write(output)
        sys.stdout.flush()
        time.sleep(speed)
        downloaded += step
    final_bar = GREEN + '█' * width + RESET
    elapsed_total = time.strftime("%M:%S", time.gmtime(time.time() - start_time))
    sys.stdout.write(f"\r100%|{final_bar}| {total:.1f}/{total:.1f} MB [{elapsed_total}<00:00, {velocity:.2f}MB/s]\n")
if __name__ == "__main__":
    tqdm_style_bar()