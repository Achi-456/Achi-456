import os
from github import Github, Auth
from datetime import datetime, timedelta
import pytz

# --- CONFIGURATION ---
USERNAME = "Achi-456" 
REPOS = {
    "Rhel-Automation-Scripts": {"goal": 4, "label": "RHEL Scripts"},
    "Infrastructure-Playground": {"goal": 3, "label": "Infra Playground"},
    "K8S-Lab-Experiments": {"goal": 5, "label": "K8s Labs"},
    "Engineering-Journal": {"goal": 7, "label": "Eng Journal"}
}

def get_weekly_progress():
    token = os.getenv('GH_TOKEN')
    if not token:
        raise ValueError("GH_TOKEN environment variable is missing")
    
    # FIX 1: Updated Auth method to fix DeprecationWarning
    auth = Auth.Token(token)
    g = Github(auth=auth)
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
            commits = repo.get_commits(since=start_of_week, author=USERNAME)
            count = commits.totalCount
            
            goal = config['goal']
            label = config['label']
            total_commits_all += count

            # Calculate Percentage
            if goal > 0:
                pct = min(int((count / goal) * 100), 100)
            else:
                pct = 100

            # Determine Color
            if count >= goal:
                color = "2ea44f" # Green
                status_icon = "✅"
            elif count > 0:
                color = "dbab09" # Yellow
                status_icon = "🚧" 
            else:
                color = "ff0000" # Red
                status_icon = "💤"

            # Generate HTML Row
            progress_url = f"https://progress-bar.dev/{pct}/?scale=100&title=progress&width=120&color={color}&suffix=%"
            row = f"| **{label}** | <img src=\"{progress_url}\" alt=\"{pct}%\" /> | {status_icon} **{count}/{goal}** |"
            stats.append(row)

            # Generate Mermaid Data
            if count > 0:
                mermaid_data += f'    "{label}" : {count}\n'
            else:
                 mermaid_data += f'    "{label}" : 0.05\n'

        except Exception as e:
            print(f"Error checking {repo_name}: {e}")
            stats.append(f"| **{repo_name}** | Error | ❌ |")

    return stats, total_commits_all, mermaid_data

def update_readme(stats_rows, total_commits, mermaid_pie):
    readme_path = "README.md"
    
    # 1. HTML Table
    table_header = "<div align=\"center\">\n\n| 📦 Repository | 📊 Weekly Progress | 📈 Status |\n| :--- | :--- | :--- |"
    table_footer = "</div>"
    stats_content = "\n".join(stats_rows)

    # 2. Total Commits Badge
    badge_url = f"https://img.shields.io/badge/Total_Commits_This_Week-{total_commits}-blue?style=for-the-badge&logo=git&logoColor=white"
    badge_html = f'<p align="center"><br/><img src="{badge_url}" alt="Total Commits" /></p>'

    # 3. Mermaid Chart
    mermaid_header = """
```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'pie1': '#2ea44f', 'pie2': '#dbab09', 'pie3': '#2188ff', 'pie4': '#ff5555' }}}%%
pie title Work Distribution (By Commits)
"""
    mermaid_footer = "```"
    mermaid_section = mermaid_header + mermaid_pie + mermaid_footer

    # Combine all parts
    new_content = f"{table_header}\n{stats_content}\n{table_footer}\n{badge_html}\n{mermaid_section}"

    # Read and Update File
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        start_marker = ""
        end_marker = ""

        # FIX 2: Use .find() instead of .split() to prevent empty separator errors
        start_index = content.find(start_marker)
        end_index = content.find(end_marker)

        if start_index != -1 and end_index != -1:
            # Keep the markers, insert content between them
            before = content[:start_index + len(start_marker)]
            after = content[end_index:]
            
            final_content = f"{before}\n{new_content}\n{after}"
            
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(final_content)
            print("README updated successfully.")
        else:
            print("Markers and not found in README.md!")
    else:
        print("README.md not found!")

if __name__ == "__main__":
    rows, total, pie_data = get_weekly_progress()
    update_readme(rows, total, pie_data)
