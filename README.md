# Python GitHub Repositories Dataset and Categorization Scripts

This repository contains Python scripts and supporting files to fetch, categorize, and organize Python-related GitHub repositories. The dataset generated can be used for research, analysis, or for building curated lists of repositories based on categories like Machine Learning, Web Development, Automation, Data Science, etc.

---

## **Project Objective**

The task is to pre-fill a **sorted list of Python repositories** from GitHub, along with their relevant metadata, and categorize them for easier shortlisting. The key objectives include:

1. Fetching popular Python repositories from GitHub, sorted by star counts.
2. Extracting key metadata for each repository:
   - Repository name
   - Repository URL
   - Description
   - Star count
   - Fork count
   - Open issues count
   - Watchers count
   - Topics
3. Categorizing each repository into logical categories such as:
   - `ml_nlp` (Machine Learning / NLP)
   - `data_science`
   - `web_frameworks`
   - `dev_tools`
   - `medicine`
   - `finance`
   - `automation`
   - `visualization`
   - `containers`
   - `game_dev`
   - `mobile`
   - `education`
   - `security`
   - `networking_api`
   - `iot_robotics`
   - `other` (for uncategorized or miscellaneous repos)
4. Saving all fetched and categorized data in a CSV file for easy use and analysis.


## **Setup Instructions**

1. **Clone the repository**
```bash
git clone https://github.com/jahidulzaid/Github-Repo-Scraper.git
cd SubTask2
```




## Install dependencies

```bash
pip install requests
```



## Set your GitHub Personal Access Token 

### Linux / macOS
```bash
export GITHUB_TOKEN="ghp_yourtokenhere"
```

### Windows (CMD)
```cmd
setx GITHUB_TOKEN "ghp_yourtokenhere"
```

### Windows (PowerShell)
```powershell
[System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_yourtokenhere", "User")
```


⚠️ Make sure to restart your terminal or IDE after setting the environment variable so Python can read it.

## Run the repository fetching script

```bash
python fetch_repos_to_csv.py
```

The script will fetch Python repositories from GitHub, collect metadata, categorize them, and save the results to `python_repos_dataset.csv`.

## Verify output

Open `python_repos_dataset.csv` to check that repositories are fetched and categorized correctly.

Each row contains:
`name, full_name, html_url, description, stargazers_count, forks_count, open_issues_count, watchers_count, topics, category.`

## Optional: Customize categories

Edit `categorize_repo.py` to add or adjust categories, keywords, or topics based on your needs.

## Optional: Increase rate-limit handling

The script uses your GitHub token to increase the rate limit to 5000 requests/hour.

You can also add sleep timers or retry logic to safely fetch larger datasets without hitting rate limits.


---


## **How It Works**

### 1. Fetching Repositories

- The script uses the **GitHub Search API** to fetch repositories written in Python.  
- Repositories are sorted by **stars**, ensuring that popular and widely-used repositories are fetched first.  
- To avoid rate limits, a **GitHub Personal Access Token (PAT)** is used. This increases the API limit from 60 requests/hour to 5000 requests/hour.

### 2. Extracting Metadata

For each repository, the following metadata is extracted:

- `name`: Repository name  
- `full_name`: Owner and repository name  
- `html_url`: Repository URL  
- `description`: Short description of the repo  
- `stargazers_count`: Number of stars  
- `forks_count`: Number of forks  
- `open_issues_count`: Number of open issues  
- `watchers_count`: Number of watchers  
- `topics`: List of topics associated with the repository  
- `category`: Assigned category based on topics and keywords  

### 3. Categorization Strategy

- **Step 1:** Check repository topics (more reliable than description).  
- **Step 2:** If topics are missing or empty, match keywords from repository name and description.  
- **Step 3:** Assign a category based on matches.  
- **Step 4:** If no category matches, label as `other`.

Example categories:

| Category           | Keywords / Topics Example                         |
|-------------------|--------------------------------------------------|
| ml_nlp             | `huggingface`, `pytorch`, `tensorflow`, `nlp`  |
| data_science       | `numpy`, `pandas`, `scipy`, `matplotlib`       |
| web_frameworks     | `django`, `flask`, `fastapi`                   |
| dev_tools          | `cli`, `linter`, `formatter`, `pytest`         |
| medicine           | `bio`, `genomics`, `clinical`, `drug`          |
| finance            | `stock`, `trading`, `crypto`, `portfolio`      |
| visualization      | `charts`, `graph`, `bokeh`, `altair`           |
| automation         | `script`, `bot`, `selenium`, `ansible`         |
| containers         | `docker`, `kubernetes`, `helm`                 |
| game_dev           | `pygame`, `godot`, `unity`                     |
| mobile             | `flutter`, `react-native`, `ios`, `android`    |
| education          | `tutorial`, `course`, `learn`                  |
| security           | `security`, `oauth`, `jwt`, `cryptography`     |
| networking_api     | `http`, `requests`, `aiohttp`, `grpc`          |
| iot_robotics       | `iot`, `raspberry`, `arduino`, `robotics`      |
| other              | Uncategorized repos                             |

---

### 4. Output

The final dataset is saved as a **CSV file** (`python_repos_dataset.csv`) with the following columns:

```csv
name,full_name,html_url,description,stargazers_count,forks_count,open_issues_count,watchers_count,topics,category
```

