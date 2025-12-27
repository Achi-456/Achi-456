import os
from github import Github
from datetime import datetime, timedelta
import pytz

# --- CONFIGURATION ---
USERNAME = "YOUR_GITHUB_USERNAME"  # <--- REPLACE THIS
# Define your repositories and their weekly goal numbers
REPOS = {
    "Rhel-Automation-Scripts": {"goal": 4, "label": "RHEL Scripts"},
    "Infrastructure-Playground": {"goal": 3, "label": "Infra Playground"},
    "K8S-Lab-Experiments": {"goal": 5, "label": "K8s Labs"},
    "Engineering-Journal": {"goal": 7, "label": "Eng Journal"}
}

def get_weekly_progress():
    # Get GitHub Token from environment variables (set by GitHub Actions)
    token = os.getenv('GH_TOKEN')
    g = Github(token)
    user = g.get_user(USERNAME)
    
    # Calculate start of the week (Monday)
    now = datetime.now(pytz.utc)
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    stats = []
    total_commits_all = 0
    mermaid_data = ""

    print(f"Checking commits since: {start_of_week.strftime('%Y-%m-%d')}")

    for repo_name, config in REPOS.items():
        try:
            repo = user.get_repo(repo_name)
            # Get commits since start of week
            commits = repo.get_commits(since=start_of_week, author=USERNAME)
            count = commits.totalCount
            
            goal = config['goal']
            label = config['label']
            total_commits_all += count

            # Calculate Percentage
            pct = min(int((count / goal) * 100), 100)
            
            # Determine Color based on progress
            if count >= goal:
                color = "2ea44f" # Green
                status_icon = "✅"
            elif count > 0:
                color = "dbab09" # Yellow
                status_icon = "🚧" 
            else:
                color = "ff0000" # Red
                status_icon = "💤"

            # 1. Generate HTML Row
            progress_url = f"https://progress-bar.dev/{pct}/?scale=100&title=progress&width=120&color={color}&suffix=%"
            
            row = f"""
| **{label}** | <img src="{progress_url}" alt="{pct}%" /> | {status_icon} **{count}/{goal}** |"""
            stats.append(row)

            # 2. Generate Mermaid Data (Only add if commits > 0 to keep graph clean)
            if count > 0:
                mermaid_data += f'    "{label}" : {count}\n'
            else:
                 mermaid_data += f'    "{label}" : 0.1\n' # Small value to show empty slice

        except Exception as e:
            print(f"Error checking {repo_name}: {e}")
            stats.append(f"| **{repo_name}** | Error | ❌ |")

    return stats, total_commits_all, mermaid_data

def update_readme(stats_rows, total_commits, mermaid_pie):
    readme_path = "README.md"
    
    # HTML Table Header
    table_header = """
<div align="center">

| 📦 Repository | 📊 Weekly Progress | 📈 Status |
| :--- | :--- | :--- |"""
    
    table_footer = "</div>"
    
    # Join the rows
    stats_content = "\n".join(stats_rows)

    # Generate the Total Commits Badge
    badge_url = f"https://img.shields.io/badge/Total_Commits_This_Week-{total_commits}-blue?style=for-the-badge&logo=git&logoColor=white"
    badge_html = f'<p align="center"><br/><img src="{badge_url}" alt="Total Commits" /></p>'

    # Generate Mermaid Chart
    mermaid_section = f"""
```mermaid
%%{{init: {{'theme': 'base', 'themeVariables': {{ 'pie1': '#2ea44f', 'pie2': '#dbab09', 'pie3': '#2188ff', 'pie4': '#ff5555' }}}}}}%%
pie title Work Distribution (By Commits)
{mermaid_pie}
