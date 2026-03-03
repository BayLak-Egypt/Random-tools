import sys
import time
def moving_head_bar(width=40, gap=1, speed=0.05, cycles=3):
    """
    شريط ثابت مع فراغ يتحرك داخله
    width: طول الشريط الكامل
    gap: طول الفراغ المتحرك
    speed: سرعة الحركة (ثواني)
    cycles: عدد مرات تكرار الحركة
    """
    bar = "━" * width
    for _ in range(cycles):
        for i in range(width - gap + 1):
            left = bar[:i]
            head = " " * gap
            right = bar[i+gap:]
            sys.stdout.write(f"\r{left}{head}{right}")
            sys.stdout.flush()
            time.sleep(speed)
    print()
if __name__ == "__main__":
    moving_head_bar()