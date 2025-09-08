import requests
import time

# Constants
GITHUB_API_URL = "https://api.github.com/search/repositories"
INPUT_FILE = "repos_500.txt"
OUTPUT_FILE = "repos_500_filled.txt"
TOTAL_REPOS_TO_FETCH = 700
PER_PAGE = 100
PAGES = TOTAL_REPOS_TO_FETCH // PER_PAGE

# Optional: add your GitHub token here to increase rate limits
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    # "Authorization": "token YOUR_GITHUB_TOKEN"  # Uncomment and add your token if needed
}

# def categorize_repo(repo):
#     name = repo["name"].lower()
#     desc = (repo.get("description") or "").lower()
#     # Topics require a separate API call (see note below)
#     topics = repo.get("topics", [])
#     # Sometimes topics are not included in search results, so fallback to empty list
#     if not topics:
#         topics = []

#     def match(keywords):
#         # Check if any keyword appears in name, description or topics
#         text_to_search = ' '.join([name, desc] + topics)
#         return any(kw in text_to_search for kw in keywords)

#     if match(["django", "flask", "fastapi", "web", "framework", "starlette", "uvicorn", "sanic", "falcon", "litestar", "gunicorn", "click"]):
#         return "web_frameworks"
#     elif match(["numpy", "pandas", "data-science", "dask", "xarray", "scipy", "statistics", "matplotlib", "plotly", "plotly.py", "statsmodels", "seaborn"]):
#         return "data_science"
#     elif match(["ml", "nlp", "transformers", "huggingface", "deep-learning", "machine-learning", "keras", "pytorch", "tensorflow", "scikit-learn", "optuna", "ray", "lightning", "ultralytics", "spacy", "haystack"]):
#         return "ml_nlp"
#     elif match(["cli", "formatter", "linter", "tooling", "devtool", "debug", "testing", "pytest", "tox", "black", "flake8", "mypy"]):
#         return "dev_tools"
#     elif match(["viz", "visualization", "plotly", "charts", "graph", "matplotlib", "seaborn"]):
#         return "visualization"
#     else:
#         return "utils"

def categorize_repo(repo):
    name = repo["name"].lower()
    desc = (repo.get("description") or "").lower()
    topics = repo.get("topics", [])
    if not topics:
        topics = []
    text = ' '.join([name, desc] + topics)

    def match(keywords):
        return any(kw in text for kw in keywords)

    if match(["django", "flask", "fastapi", "starlette", "uvicorn", "sanic", "falcon", "litestar", "gunicorn", "click"]):
        return "web_frameworks"
    if match(["numpy", "pandas", "scipy", "matplotlib", "seaborn", "plotly", "statsmodels", "dask", "xarray", "pyodide", "data-science"]):
        return "data_science"
    if match(["huggingface", "transformers", "datasets", "keras", "tensorflow", "pytorch", "lightning", "optuna", "ray", "ultralytics", "spacy", "haystack", "scikit-learn", "deep-learning", "machine-learning", "nlp"]):
        return "ml_nlp"
    if match(["cli", "linter", "formatter", "testing", "pytest", "tox", "black", "flake8", "mypy", "debug", "profiling", "tooling"]):
        return "dev_tools"
    if match(["visualization", "matplotlib", "plotly", "charts", "graph", "seaborn", "bokeh", "altair"]):
        return "visualization"
    if match(["networking", "socket", "http", "grpc", "websocket", "requests", "aiohttp", "paramiko", "netmiko", "ssh", "dns", "httpx", "proxy"]):
        return "networking"
    if match(["database", "sql", "nosql", "mongodb", "redis", "sqlite", "postgresql", "mysql", "sqlalchemy", "orm", "cassandra", "influxdb", "timescale"]):
        return "database"
    if match(["security", "cryptography", "oauth", "jwt", "authentication", "encryption", "hashing", "ssl", "tls"]):
        return "security"
    if match(["automation", "ci", "cd", "github-actions", "ansible", "terraform", "saltstack", "chef", "puppet", "scripting"]):
        return "automation"
    if match(["docker", "kubernetes", "k8s", "container", "podman", "helm"]):
        return "containers"
    if match(["game", "pygame", "arcade", "godot", "unity", "unreal"]):
        return "game_dev"
    if match(["android", "ios", "flutter", "react-native", "mobile"]):
        return "mobile"
    if match(["robotics", "ros", "automation", "sensors", "motors"]):
        return "robotics"

    return "utils"


def fetch_repos():
    all_repos = []
    for page in range(1, PAGES + 1):
        print(f"Fetching page {page} of {PAGES}...")
        params = {
            "q": "language:python",
            "sort": "stars",
            "order": "desc",
            "per_page": PER_PAGE,
            "page": page
        }
        response = requests.get(GITHUB_API_URL, headers=HEADERS, params=params)

        if response.status_code == 200:
            data = response.json()
            # Note: Search API doesn't include topics by default
            # To get topics, we'd need to call repo topics API for each repo (rate-limiting concern)
            for repo in data["items"]:
                all_repos.append(repo)
        else:
            print(f"GitHub API error: {response.status_code}")
            break
        time.sleep(2)  # Respect rate limits
    return all_repos

def main():
    # Fetch repos
    repos = fetch_repos()

    # Categorize and format lines
    categorized_lines = []
    for repo in repos:
        category = categorize_repo(repo)
        line = f"{category}: {repo['html_url']}\n"
        categorized_lines.append(line)

    # Read original file and keep first 100 lines
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        original_lines = f.readlines()

    header = original_lines[0] if original_lines else "# Stratified 500-repo list (edit freely; you can pin with @SHA)\n"
    first_100 = original_lines[1:101] if len(original_lines) > 100 else original_lines[1:]

    # Calculate how many repos to add (total 500 lines, first 100 preserved)
    slots_to_fill = 500 - len(first_100)

    # Fill placeholders with fetched repos (truncate if necessary)
    new_repos_lines = categorized_lines[:slots_to_fill]

    # Compose final lines
    final_lines = [header] + first_100 + new_repos_lines

    # Write output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(final_lines)

    print(f"\n✅ Saved {len(final_lines)} lines to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
