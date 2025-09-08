import requests
import time
import csv
import os

# Constants
GITHUB_API_URL = "https://api.github.com/search/repositories"
TOTAL_REPOS_TO_FETCH = 5000
PER_PAGE = 100
PAGES = TOTAL_REPOS_TO_FETCH // PER_PAGE
TIME_BETWEEN_PAGES = 5  # seconds
TIME_BETWEEN_TOPIC_FETCH = 0  # seconds


# GitHub token recommended to avoid rate-limit (60 → 5000 requests/hour)
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"
}


def categorize_repo(repo, topics):
    name = repo["name"].lower()
    desc = (repo.get("description") or "").lower()
    text = " ".join([name, desc] + topics)

    def match(keywords):
        return any(kw in text for kw in keywords)

    if match(["django", "flask", "fastapi", "starlette", "uvicorn", "sanic", "falcon", "litestar"]):
        return "web_frameworks"
    if match(["numpy", "pandas", "scipy", "matplotlib", "seaborn", "plotly", "statsmodels", "dask", "xarray"]):
        return "data_science"
    if match(["huggingface", "transformers", "datasets", "keras", "tensorflow", "pytorch", "lightning", "scikit-learn", "ml", "nlp"]):
        return "ml_nlp"
    if match(["cli", "linter", "formatter", "pytest", "tox", "black", "flake8", "mypy", "debug"]):
        return "dev_tools"
    if match(["visualization", "charts", "graph", "bokeh", "altair"]):
        return "visualization"
    if match(["database", "sql", "nosql", "mongodb", "redis", "postgresql", "mysql", "sqlite"]):
        return "database"
    if match(["security", "cryptography", "oauth", "jwt", "encryption"]):
        return "security"
    if match(["docker", "kubernetes", "container", "helm"]):
        return "containers"
    if match(["game", "pygame", "arcade", "godot", "unity"]):
        return "game_dev"
    if match(["android", "ios", "flutter", "react-native", "mobile"]):
        return "mobile"
    if match(["bio", "genomics", "protein", "health", "clinical", "drug"]):
        return "medicine"
    if match(["stock", "trading", "finance", "crypto", "portfolio", "bank"]):
        return "finance"
    if match(["edu", "teaching", "course", "tutorial", "learn"]):
        return "education"
    if match(["api", "rest", "http", "requests", "aiohttp", "grpc", "websocket"]):
        return "networking_api"
    if match(["automation", "script", "bot", "selenium", "scrapy", "ansible"]):
        return "automation"
    if match(["cli", "command", "tool", "shell"]):
        return "cli_tools"
    if match(["image", "opencv", "pillow", "cv2", "image-processing"]):
        return "image_processing"
    if match(["audio", "speech", "music", "pyaudio", "librosa"]):
        return "audio"
    if match(["video", "ffmpeg", "opencv", "moviepy"]):
        return "video_processing"
    if match(["iot", "sensor", "raspberry", "arduino", "robotics"]):
        return "iot_robotics"

    return "utils"

def fetch_topics(full_name):
    """Fetch topics for a repo (requires token)"""
    url = f"https://api.github.com/repos/{full_name}/topics"
    r = requests.get(url, headers={**HEADERS, "Accept": "application/vnd.github.mercy-preview+json"})
    if r.status_code == 200:
        return r.json().get("names", [])
    return []

# def fetch_repos():
#     all_repos = []
#     for page in range(1, PAGES + 1):
#         print(f"Fetching page {page}/{PAGES}...")
#         params = {
#             "q": "language:python",
#             "sort": "stars",
#             "order": "desc",
#             "per_page": PER_PAGE,
#             "page": page
#         }
#         response = requests.get(GITHUB_API_URL, headers=HEADERS, params=params)

#         if response.status_code == 200:
#             data = response.json()
#             for repo in data["items"]:
#                 topics = fetch_topics(repo["full_name"]) or []
#                 category = categorize_repo(repo, topics)
#                 all_repos.append({
#                     "name": repo["name"],
#                     "full_name": repo["full_name"],
#                     "html_url": repo["html_url"],
#                     "description": repo.get("description", ""),
#                     "stargazers_count": repo["stargazers_count"],
#                     "forks_count": repo["forks_count"],
#                     "open_issues_count": repo["open_issues_count"],
#                     "watchers_count": repo["watchers_count"],
#                     "topics": ",".join(topics),
#                     "category": category
#                 })
#         else:
#             print(f"GitHub API error: {response.status_code}")
#             break

#         time.sleep(2)  # Avoid rate limit
#     return all_repos

def fetch_repos():
    all_repos = []
    for page in range(1, PAGES + 1):
        print(f"Fetching page {page}/{PAGES}...")
        params = {
            "q": "language:python",
            "sort": "stars",
            "order": "desc",
            "per_page": PER_PAGE,
            "page": page
        }
        response = requests.get(GITHUB_API_URL, headers={"Accept": "application/vnd.github.v3+json"}, params=params)

        if response.status_code == 200:
            data = response.json()
            for repo in data["items"]:
                topics = fetch_topics(repo["full_name"]) or []
                category = categorize_repo(repo, topics)
                all_repos.append({
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "html_url": repo["html_url"],
                    "description": repo.get("description", ""),
                    "stargazers_count": repo["stargazers_count"],
                    "forks_count": repo["forks_count"],
                    "open_issues_count": repo["open_issues_count"],
                    "watchers_count": repo["watchers_count"],
                    "topics": ",".join(topics),
                    "category": category
                })
                time.sleep(TIME_BETWEEN_TOPIC_FETCH)  # small delay per repo
        else:
            print(f"GitHub API error: {response.status_code}")
            break

        time.sleep(TIME_BETWEEN_PAGES)  # wait before fetching next page
    return all_repos


def save_to_csv(repos, filename="SubTask2/python_repos_dataset.csv"):
    keys = repos[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(repos)
    print(f"✅ Saved {len(repos)} repos to {filename}")

def main():
    repos = fetch_repos()
    if repos:
        save_to_csv(repos)

if __name__ == "__main__":
    main()
