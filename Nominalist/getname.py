import sys
import argparse
from collections import defaultdict
def load_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
def show_header():
    print(f"{'Line':<10}{'Name'}")
    print("-" * 25)
def normalize(text, case_insensitive):
    return text.lower() if case_insensitive else text
def show_duplicates(lines, case_insensitive=False):
    names = defaultdict(list)
    for index, line in enumerate(lines, start=1):
        clean = line.strip()
        key = normalize(clean, case_insensitive)
        names[key].append((index, clean))
    show_header()
    displayed = []
    for key, values in names.items():
        if len(values) > 1:
            for ln, original in values:
                print(f"{ln:<10}{original}")
                displayed.append(original)
    print("-" * 25)
    print(f"Total Rows: {len(displayed)}")
    return displayed
def filter_similar(lines, case_insensitive=False):
    show_header()
    displayed = []
    for i, line in enumerate(lines, start=1):
        clean = line.strip()
        compare_i = normalize(clean, case_insensitive)
        for other in lines:
            compare_j = normalize(other.strip(), case_insensitive)
            if compare_i in compare_j and clean != other.strip():
                print(f"{i:<10}{clean}")
                displayed.append(clean)
                break
    print("-" * 25)
    print(f"Total Rows: {len(displayed)}")
    return displayed
def search_name(lines, keyword, partial=False, case_insensitive=False):
    show_header()
    keyword = normalize(keyword, case_insensitive)
    displayed = []
    for index, line in enumerate(lines, start=1):
        clean = line.strip()
        compare = normalize(clean, case_insensitive)
        if (partial and keyword in compare) or (not partial and keyword == compare):
            print(f"{index:<10}{clean}")
            displayed.append(clean)
    print("-" * 25)
    print(f"Total Rows: {len(displayed)}")
    return displayed
def save_output(displayed, output_file):
    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                for line in displayed:
                    f.write(line + "\n")
            print(f"Saved results to '{output_file}'")
        except Exception as e:
            print(f"Error saving file: {e}")
def main():
    parser = argparse.ArgumentParser(
        description="Duplicate & search tool with output file support"
    )
    parser.add_argument("file", help="Wordlist file")
    parser.add_argument("-f", "--filter", action="store_true", help="Filter similar names")
    parser.add_argument("-s", "--search", help="Search specific name")
    parser.add_argument("-u", "--ignore-case", action="store_true", help="Case insensitive search")
    parser.add_argument("-o", "--output", help="Save results to a file")
    args = parser.parse_args()
    lines = load_file(args.file)
    if args.search:
        displayed = search_name(lines, args.search, partial=args.filter, case_insensitive=args.ignore_case)
    elif args.filter:
        displayed = filter_similar(lines, case_insensitive=args.ignore_case)
    else:
        displayed = show_duplicates(lines, case_insensitive=args.ignore_case)
    if args.output:
        save_output(displayed, args.output)
if __name__ == "__main__":
    main()