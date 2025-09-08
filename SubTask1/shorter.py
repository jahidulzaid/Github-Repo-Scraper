INPUT_FILE = "repos_500_filled.txt"
OUTPUT_FILE = "repos_500_sorted.txt"

def sort_by_category(line):
    parts = line.split(":", 1)
    return parts[0].strip().lower() if len(parts) > 1 else ""

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Separate header and actual repo lines
    header = lines[0] if lines[0].startswith("#") else ""
    body = lines[1:] if header else lines

    # Sort lines by category prefix
    sorted_lines = sorted(body, key=sort_by_category)

    # Write to new file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        if header:
            f.write(header)
        f.writelines(sorted_lines)

    print(f"✅ Sorted lines saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
