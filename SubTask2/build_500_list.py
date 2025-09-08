import csv

INPUT_FILE = "SubTask2/repos_500.txt"
CSV_FILE = "SubTask2/python_repos_dataset.csv"
OUTPUT_FILE = "SubTask2/repos_800_filled.txt"

def main():
    # Load dataset CSV
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        repos = list(reader)

    # Read original repos_500.txt
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        original_lines = f.readlines()

    header = original_lines[0] if original_lines else "# Stratified 500-repo list\n"
    first_100 = original_lines[1:101] if len(original_lines) > 100 else original_lines[1:]

    # Deduplicate: remove repos already in first_100
    used_urls = {line.strip().split(":")[-1] for line in first_100 if ":" in line}
    new_repos = []
    for repo in repos:
        if repo["html_url"] not in used_urls:
            new_repos.append(f"{repo['category']}: {repo['html_url']}\n")

    slots_to_fill = 800 - len(first_100)
    final_lines = [header] + first_100 + new_repos[:slots_to_fill]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(final_lines)

    print(f"✅ Saved {len(final_lines)} lines to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
