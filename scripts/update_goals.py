import os
from github import Github, Auth
from datetime import datetime, timedelta, timezone
import pytz

# ==========================================
# 🔧 CONFIGURATION
# ==========================================
USERNAME = "Achi-456"
GIF_URL = "https://raw.githubusercontent.com/Achi-456/Achi-456/main/gif3%20(1).gif" 

REPOS = {
    "Rhel-Automation-Scripts": {"goal": 4, "label": "RHEL Scripts"},
    "Infrastructure-Playground": {"goal": 3, "label": "Infra Playground"},
    "K8S-Lab-Experiments": {"goal": 5, "label": "K8s Labs"},
    "Engineering-Journal": {"goal": 7, "label": "Eng Journal"}
}

# ==========================================
# 1. HEADER & ARSENAL (Standard)
# ==========================================
HEADER_TOP = """<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=2E64FE&height=300&section=header&text=Achintha%20Rukshan&fontSize=90&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=DevOps%20and%20Infrastructure%20Engineer&descAlignY=55&descAlign=62"/>
</div>

<div align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=25&pause=1000&color=2E64FE&center=true&vCenter=true&width=500&lines=Building+Resilient+Infrastructure;Automating+The+Boring+Stuff;Exploring+RHEL+and+VMware;Intern+at+MillenniumIT+ESP" alt="Typing SVG" />
  </a>
</div>
<br/>
<div align="center">
  <a href="https://www.linkedin.com/in/achintha-rukshan-583671344/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
  <a href="mailto:achinthar456@gmail.com"><img src="https://img.shields.io/badge/Gmail-800020?style=for-the-badge&logo=gmail&logoColor=white" /></a>
  <a href="mailto:hathurusinghahar.22@uom.lk"><img src="https://img.shields.io/badge/UoM_Email-005a9c?style=for-the-badge&logo=minutemailer&logoColor=white" /></a>
  <a href="https://kodekloud.com/"><img src="https://img.shields.io/badge/KodeKloud-2E64FE?style=for-the-badge&logo=kubernetes&logoColor=white" /></a>
</div>
<br/>
<div align="center">
<h3>🧙‍♂️ About Me</h3>
I am a **DevOps enthusiast** and undergraduate at the **University of Moratuwa**. Currently, I am applying my skills as a Trainee Infrastructure Engineer at **MillenniumIT ESP**.
</div>
---
"""

ARSENAL_HTML = f"""
### 🔮 The Arsenal
<table border="0">
  <tr>
    <td width="55%" valign="top">
      <br/>
      <h4 align="left">☁️ Infrastructure & Virtualization</h4>
      <p>
        <img src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white" />
        <img src="https://img.shields.io/badge/VMware-607078?style=flat-square&logo=vmware&logoColor=white" />
        <img src="https://img.shields.io/badge/Red_Hat-EE0000?style=flat-square&logo=red-hat&logoColor=white" />
      </p>
      <h4 align="left">🚀 DevOps & Automation</h4>
      <p>
        <img src="https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white" />
        <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" />
        <img src="https://img.shields.io/badge/Ansible-000000?style=flat-square&logo=ansible&logoColor=white" />
      </p>
      <h4 align="left">💻 Scripting & Languages</h4>
      <p>
        <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
        <img src="https://img.shields.io/badge/Bash-800020?style=flat-square&logo=gnu-bash&logoColor=white" />
        <img src="https://img.shields.io/badge/C++-00599C?style=flat-square&logo=c%2B%2B&logoColor=white" />
      </p>
    </td>
    <td width="45%" valign="middle" align="center">
       <img src="{GIF_URL}" width="100%" alt="Coding Gif"/>
    </td>
  </tr>
</table>
---
"""

FOOTER_HTML = """
### 📊 Github Stats
<div align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user=Achi-456&theme=dark&hide_border=true&background=0d1117&ring=2E64FE&fire=2E64FE&currStreakNum=2E64FE&currStreakLabel=2E64FE" alt="streak stats" />
  <br/><br/>
  <img src="https://raw.githubusercontent.com/Achi-456/Achi-456/main/profile-summary-card-output/default/0-profile-details.svg" width="45%" />
  <img src="https://raw.githubusercontent.com/Achi-456/Achi-456/main/profile-summary-card-output/default/2-most-commit-language.svg" width="45%" />
</div>
"""

# ==========================================
# 🧠 HELPER FUNCTIONS
# ==========================================
def time_ago(past_time):
    # Calculate simple "time ago" string
    now = datetime.now(timezone.utc)
    diff = now - past_time
    
    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600}h ago"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60}m ago"
    else:
        return "Just now"

def get_modern_tracker():
    token = os.getenv('GH_TOKEN')
    if not token: raise ValueError("GH_TOKEN is missing")
    
    auth = Auth.Token(token)
    g = Github(auth=auth)
    user = g.get_user(USERNAME)
    
    now = datetime.now(timezone.utc)
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    left_column_html = []
    right_column_html = []
    total_commits = 0
    
    print(f"Fetch start: {start_of_week.strftime('%Y-%m-%d')}")

    for repo_name, config in REPOS.items():
        try:
            repo = user.get_repo(repo_name)
            repo_url = repo.html_url
            
            # Get Weekly Commits
            commits = repo.get_commits(since=start_of_week, author=USERNAME)
            count = commits.totalCount
            
            goal = config['goal']
            label = config['label']
            total_commits += count
            
            # --- LEFT COLUMN: Progress Bar ---
            if goal == 0: pct = 100
            else: pct = min(int((count / goal) * 100), 100)
            
            # Color logic: Green if hit goal, Yellow if progress, Red if 0
            bar_color = "90EE90" # Light Green
            if pct < 30: bar_color = "ff6961" # Light Red
            elif pct < 100: bar_color = "ffb347" # Pastel Orange

            left_block = f"""
            <div style="margin-bottom: 12px;">
                <a href="{repo_url}">
                    <img src="https://img.shields.io/badge/{label}-181717?style=flat&logo=github&logoColor=white" height="20" />
                </a><br/>
                <img src="https://geps.dev/progress/{pct}?color={bar_color}&height=8" />
                <br/>
                <code>{count}/{goal} commits</code>
            </div>"""
            left_column_html.append(left_block)
            
            # --- RIGHT COLUMN: Last Commit Activity ---
            try:
                # Get the absolute latest commit (even if not this week) for context
                last_commit = repo.get_commits(author=USERNAME)[0]
                msg = last_commit.commit.message.split('\n')[0] # First line only
                if len(msg) > 35: msg = msg[:32] + "..." # Truncate
                
                c_date = last_commit.commit.author.date.replace(tzinfo=timezone.utc)
                t_ago = time_ago(c_date)
                
                # Activity styling
                right_block = f"""
                <div style="margin-bottom: 12px; font-size: 13px;">
                    <b>{label}</b> <span style="color: #8b949e; font-size: 11px;">({t_ago})</span><br/>
                    <span style="font-family: monospace; color: #a5d6ff;">↳ {msg}</span>
                </div>"""
                right_column_html.append(right_block)
                
            except IndexError:
                # No commits ever
                right_column_html.append(f"""<div style="margin-bottom: 12px;"><b>{label}</b><br/><span style="color: #8b949e;">No activity yet</span></div>""")

        except Exception as e:
            print(f"Error {repo_name}: {e}")

    return "\n".join(left_column_html), "\n".join(right_column_html), total_commits

# ==========================================
# 📝 WRITE TO FILE
# ==========================================
if __name__ == "__main__":
    left_col, right_col, total = get_modern_tracker()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    
    # 2-Column Layout for Velocity Section
    velocity_section = f"""
<div align="center">
<h3>🚀 Weekly Engineering Velocity</h3>
<p><i>Last updated: {now_str}</i></p>

<table border="0" width="90%">
    <tr>
        <td width="45%" valign="top">
            <h4 align="center">🎯 Goals vs Reality</h4>
            {left_col}
        </td>
        <td width="10%"></td> <td width="45%" valign="top">
            <h4 align="center">⚡ Latest Activity</h4>
            {right_col}
        </td>
    </tr>
</table>
</div>
"""
    
    badge_html = f'\n<p align="center"><img src="https://img.shields.io/badge/Total_Weekly_Commits-{total}-2E64FE?style=for-the-badge&logo=github&logoColor=white" /></p>\n'
    full_readme = HEADER_TOP + "\n" + ARSENAL_HTML + "\n" + velocity_section + "\n" + badge_html + "\n" + FOOTER_HTML

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(full_readme)
    
    print("✅ README.md successfully rebuilt with Activity Feed.")