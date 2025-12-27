import requests
import datetime
import os
import sys

# --- CONFIGURATION ---
USERNAME = "Achi-456"

# Format: "Repo Name": Goal_Commits_Per_Week
REPOS = {
    "rhel-automation-scripts": 4,
    "infrastructure-playground": 3,
    "k8s-lab-experiments": 5,
    "engineering-journal": 7
}

def get_weekly_commits(repo_name):
    """Fetches commit count for the current week (starting Monday)."""
    today = datetime.datetime.now()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    iso_date = start_of_week.isoformat() + "Z"

    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/commits?since={iso_date}"
    
    if "GITHUB_TOKEN" not in os.environ:
        print("Error: GITHUB_TOKEN is missing.")
        return 0

    headers = {"Authorization": f"token {os.environ['GITHUB_TOKEN']}"}
    
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return len(r.json())
        else:
            print(f"Failed to fetch {repo_name}: {r.status_code}")
            return 0
    except Exception as e:
        print(f"Error fetching {repo_name}: {e}")
        return 0

def create_progress_bar(current, goal):
    """Generates a text-based progress bar."""
    if goal == 0: goal = 1 
    percent = min(current / goal, 1.0)
    bar_length = 10
    filled = int(bar_length * percent)
    bar = "▓" * filled + "░" * (bar_length - filled)
    
    status = "✅" if current >= goal else "🚧"
    return f"`{bar}` {status} **{current}/{goal}**"

def main():
    print(f"Starting update for user: {USERNAME}")
    
    # --- SAFE MARKER CONSTRUCTION ---
    # We build these strings so copy-paste doesn't break them
    start_marker = "<" + "!-- START_WEEKLY_GOALS --" + ">"
    end_marker = "<" + "!-- END_WEEKLY_GOALS --" + ">"
    
    # Debug print to prove they are not empty
    print(f"DEBUG: Using markers '{start_marker}' and '{end_marker}'")

    # Generate the Markdown Table
    markdown_output = ["### 🎯 Weekly Goal Tracker\n"]
    markdown_output.append("| Repository | Weekly Progress | Status |")
    markdown_output.append("| :--- | :--- | :--- |")
    
    for repo, goal in REPOS.items():
        count = get_weekly_commits(repo)
        bar = create_progress_bar(count, goal)
        display_name = repo.replace("-", " ").title().replace("K8s", "K8s")
        markdown_output.append(f"| **{display_name}** | {bar} |")
        print(f"Processed {repo}: {count}/{goal}")
    
    markdown_output.append(f"\n*Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("Error: README.md not found.")
        sys.exit(1)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the positions instead of splitting (Safer!)
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker)

    if start_pos != -1 and end_pos != -1:
        # Keep everything before the start marker
        pre_content = content[:start_pos + len(start_marker)]
        # Keep everything after the end marker
        post_content = content[end_pos:]
        
        # Combine
        new_content = pre_content + "\n" + "\n".join(markdown_output) + "\n" + post_content
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("SUCCESS: README updated successfully.")
    else:
        print("WARNING: Markers not found in README.md.")
        print(f"Make sure you have exactly {start_marker} and {end_marker} in your README.")

if __name__ == "__main__":
    main()
