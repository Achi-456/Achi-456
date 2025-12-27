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

def generate_ascii_bar(count, goal, length=20):
    """Creates a text-based progress bar"""
    if goal == 0:
        percent = 1.0
    else:
        percent = min(count / goal, 1.0)
    
    filled_length = int(length * percent)
    bar = "█" * filled_length + "░" * (length - filled_length)
    return bar, int(percent * 100)

def get_weekly_progress():
    token = os.getenv('GH_TOKEN')
    if not token:
        raise ValueError("GH_TOKEN environment variable is missing")
    
    auth = Auth.Token(token)
    g = Github(auth=auth)
    user = g.get_user(USERNAME)
    
    # Calculate start of the week (Monday)
    now = datetime.now(pytz.utc)
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    rows = []
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

            # Generate ASCII Bar
            bar, pct = generate_ascii_bar(count, goal)

            # Determine Icon
            if count >= goal:
                status = "✅"
            elif count > 0:
                status = "🚧" 
            else:
                status = "💤"

            # Create the Table Row
            row = f"| {status} **{label}** | `{bar}` | **{pct}%** | **{count}/{goal}** |"
            rows.append(row)

            # Generate Mermaid Data
            if count > 0:
                mermaid_data += f'    "{label}" : {count}\n'
            else:
                 mermaid_data += f'    "{label}" : 0.01\n'

        except Exception as e:
            print(f"Error checking {repo_name}: {e}")
            rows.append(f"| ❌ **{repo_name}** | Error | 0% | 0/0 |")

    return rows, total_commits_all, mermaid_data

def update_readme(stats_rows, total_commits, mermaid_pie):
    readme_path = "README.md"
    
    # Get Current Date
    now = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    # 1. HTML Table Construction
    table_header = """
<div align="center">
<h3>🚀 Weekly Engineering Velocity</h3>
<p><i>Last updated: {}</i></p>

| Repository | Weekly Progress | % | Status |
| :--- | :--- | :--- | :--- |""".format(now)

    stats_content = "\n".join(stats_rows)
    table_footer = "</div>"

    # 2. Total Badge
    badge_url = f"https://img.shields.io/badge/Total_Commits-{total_commits}-2E64FE?style=for-the-badge&logo=github&logoColor=white"
    badge_html = f'\n<p align="center"><img src="{badge_url}" /></p>\n'

    # 3. Mermaid Chart 
    # WE USE SIMPLE STRING CONCATENATION HERE TO AVOID SYNTAX ERRORS
    mermaid_header = "```mermaid\n"
    mermaid_header += "%%{init: {'theme': 'dark', 'themeVariables': { 'pie1': '#800020', 'pie2': '#2E64FE', 'pie3': '#2ea44f', 'pie4': '#dbab09' }}}%%\n"
    mermaid_header += "pie title Work Distribution\n"
    
    mermaid_footer = "```\n"
    
    mermaid_section = mermaid_header + mermaid_pie + mermaid_footer

    new_content = f"{table_header}\n{stats_content}\n{table_footer}\n{badge_html}\n{mermaid_section}"

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        start_marker = ""
        end_marker = ""

        start_index = content.find(start_marker)
        end_index = content.find(end_marker)

        if start_index != -1 and end_index != -1:
            before = content[:start_index + len(start_marker)]
            after = content[end_index:]
            
            final_content = f"{before}\n{new_content}\n{after}"
            
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(final_content)
            print("README updated successfully.")
        else:
            print("Markers not found in README.md!")
    else:
        print("README.md not found!")

if __name__ == "__main__":
    rows, total, pie_data = get_weekly_progress()
    update_readme(rows, total, pie_data)
