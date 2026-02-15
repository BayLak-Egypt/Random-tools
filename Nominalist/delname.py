import sys
import argparse
def load_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
def save_file(filename, lines):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.writelines(lines)
    except Exception as e:
        print(f"Error saving file: {e}")
        sys.exit(1)
def normalize(text, case_insensitive):
    return text.lower() if case_insensitive else text
def delete_lines_by_numbers(lines, numbers):
    deleted = []
    total_lines = len(lines)
    remaining = []
    numbers_set = set(numbers)
    for idx, line in enumerate(lines, start=1):
        if idx in numbers_set:
            deleted.append((idx, line.strip()))
        else:
            remaining.append(line)
    missing = [n for n in numbers if n > total_lines or n < 1]
    if missing:
        for m in missing:
            print(f"Line {m} not found!")
    return remaining, deleted
def delete_lines_by_name(lines, keyword, partial=False, case_insensitive=False):
    deleted = []
    remaining = []
    keyword_norm = normalize(keyword, case_insensitive)
    for line in lines:
        line_clean = line.strip()
        line_norm = normalize(line_clean, case_insensitive)
        match = (keyword_norm in line_norm) if partial else (keyword_norm == line_norm)
        if match:
            deleted.append(line_clean)
        else:
            remaining.append(line)
    if not deleted:
        print(f"No lines matched '{keyword}'")
    return remaining, deleted
def show_deleted(deleted):
    if deleted:
        print("\nLine      Name")
        print("-" * 25)
        for item in deleted:
            if isinstance(item, tuple):
                print(f"{item[0]:<10}{item[1]} 'is deleted'")
            else:
                print(f"{item} 'is deleted'")
        print("-" * 25)
        print(f"Total Deleted: {len(deleted)}")
    else:
        print("No lines deleted.")
def main():
    parser = argparse.ArgumentParser(description="Delete lines or words from a file")
    parser.add_argument("file", help="Wordlist file")
    parser.add_argument("-l", "--lines", help="Delete lines by number, comma separated")
    parser.add_argument("-w", "--word", help="Delete lines containing exact word")
    parser.add_argument("-f", "--filter", action="store_true", help="Partial match for -w")
    parser.add_argument("-u", "--ignore-case", action="store_true", help="Case insensitive search")
    parser.add_argument("-o", "--output", help="Save modified file")
    args = parser.parse_args()
    lines = load_file(args.file)
    deleted = []
    if args.lines:
        try:
            numbers = [int(n) for n in args.lines.split(",")]
            lines, del_lines = delete_lines_by_numbers(lines, numbers)
            deleted.extend(del_lines)
        except ValueError:
            print("Invalid line numbers. Use comma separated integers.")
            sys.exit(1)
    if args.word:
        lines, del_lines = delete_lines_by_name(lines, args.word, partial=args.filter, case_insensitive=args.ignore_case)
        deleted.extend(del_lines)
    show_deleted(deleted)
    if args.output:
        save_file(args.output, lines)
        print(f"Modified file saved to '{args.output}'")
    else:
        save_file(args.file, lines)
if __name__ == "__main__":
    main()