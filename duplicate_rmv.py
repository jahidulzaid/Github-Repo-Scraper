INPUT_FILE = "v3.txt"
OUTPUT_FILE = "v3_deduped.txt"

def main():
    seen = set()
    unique_lines = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            normalized = line.strip().lower()  # for case-insensitive deduplication
            if normalized not in seen:
                seen.add(normalized)
                unique_lines.append(line)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(unique_lines)

    print(f"✅ Removed duplicates. {len(unique_lines)} unique lines saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
