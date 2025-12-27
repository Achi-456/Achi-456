
import requests
import datetime
import os

# --- CONFIGURATION ---
USERNAME = "Achi-456"
# Format: "Repo Name": Goal_Commits_Per_Week
REPOS = {
    "rhel-automation-scripts": 4,
    "infrastructure-playground": 3,
    "k8s-lab-experiments": 5,
    "engineering-journal": 7  # 1 per day
}

def get_weekly_commits(repo_name):
    # Calculate start of the week (Monday)
    today = datetime.datetime.now()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    iso_date = start_of_week.isoformat() + "Z"

    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/commits?since={iso_date}"
    headers = {"Authorization": f"token {os.environ['GITHUB_TOKEN']}"}
    
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return len(r.json())
        return 0
    except:
        return 0

def create_progress_bar(current, goal):
    # Create a visual bar: [■■■■□□]
    percent = min(current / goal, 1.0)
    bar_length = 10
    filled = int(bar_length * percent)
    bar = "▓" * filled + "░" * (bar_length - filled)
    
    status = "✅" if current >= goal else "🚧"
    return f"`{bar}` {status} **{current}/{goal}**"

def main():
    markdown_output = ["### 🎯 Weekly Goal Tracker\n"]
    markdown_output.append("| Repository | Weekly Progress | Status |")
    markdown_output.append("| :--- | :--- | :--- |")
    
    for repo, goal in REPOS.items():
        count = get_weekly_commits(repo)
        bar = create_progress_bar(count, goal)
        # Beautify repo name
        display_name = repo.replace("-", " ").title().replace("K8s", "K8s")
        markdown_output.append(f"| **{display_name}** | {bar} |")
    
    markdown_output.append(f"\n*Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    
    # Read the README
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Regex-like replacement using string splitting
    start_marker = ""
    end_marker = ""
    
    if start_marker in content and end_marker in content:
        pre_content = content.split(start_marker)[0]
        post_content = content.split(end_marker)[1]
        new_content = pre_content + start_marker + "\n" + "\n".join(markdown_output) + "\n" + end_marker + post_content
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README updated successfully.")
    else:
        print("Markers not found in README.")

if __name__ == "__main__":
    main()
