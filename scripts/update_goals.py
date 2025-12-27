import os
from github import Github, Auth
from datetime import datetime, timedelta
import pytz

# ==========================================
# 🔧 CONFIGURATION
# ==========================================
USERNAME = "Achi-456"

# ⚠️ URGENT: PASTE YOUR GIF LINK BELOW
# 1. Go to your repo, open 'gif3 (1).gif', click 'Raw', and copy the URL.
# 2. Paste it inside the quotes below.
GIF_URL = "https://raw.githubusercontent.com/Achi-456/Achi-456/main/gif3%20(1).gif" 
# (I added a likely URL above based on standard GitHub patterns, but double-check it!)

REPOS = {
    "Rhel-Automation-Scripts": {"goal": 4, "label": "RHEL Scripts"},
    "Infrastructure-Playground": {"goal": 3, "label": "Infra Playground"},
    "K8S-Lab-Experiments": {"goal": 5, "label": "K8s Labs"},
    "Engineering-Journal": {"goal": 7, "label": "Eng Journal"}
}

# ==========================================
# 1. HEADER SECTION
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
  <a href="https://www.linkedin.com/in/achintha-rukshan-583671344/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="mailto:achinthar456@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-800020?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
  <a href="mailto:hathurusinghahar.22@uom.lk">
    <img src="https://img.shields.io/badge/UoM_Email-005a9c?style=for-the-badge&logo=minutemailer&logoColor=white" />
  </a>
  <a href="https://kodekloud.com/">
    <img src="https://img.shields.io/badge/KodeKloud-2E64FE?style=for-the-badge&logo=kubernetes&logoColor=white" />
  </a>
</div>

<br/>

<div align="center">

### 🧙‍♂️ About Me

I am a **DevOps enthusiast** and undergraduate at the **University of Moratuwa**. Currently, I am applying my skills as a Trainee Infrastructure Engineer at **MillenniumIT ESP**, focusing on Enterprise Linux and Virtualization.

Examples of my work include **6DOF Robotic Arm control** and **Conveyor Belt inspection systems**.

</div>

---
"""

# ==========================================
# 2. ARSENAL SECTION (Table Layout with border="0")
# ==========================================
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

# ==========================================
# 3. STATS SECTION
# ==========================================
FOOTER_HTML = """
### 📊 Github Stats

<div align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user=Achi-456&theme=dark&hide_border=true&background=0d1117&ring=2E64FE&fire=2E64FE&currStreakNum=2E64FE&currStreakLabel=2E64FE" alt="streak stats" />
  <br/>
  <br/>
  <img src="https://raw.githubusercontent.com/Achi-456/Achi-456/main/profile-summary-card-output/default/0-profile-details.svg" width="45%" />
  <img src="https://raw.githubusercontent.com/Achi-456/Achi-456/main/profile-summary-card-output/default/2-most-commit-language.svg" width="45%" />
</div>
"""

# ==========================================
# 🧠 LOGIC: CALCULATE STATS
# ==========================================

def generate_ascii_bar(count, goal, length=20):
    if goal == 0: pct = 1.0
    else: pct = min(count / goal, 1.0)
    filled = int(length * pct)
    return "█" * filled + "░" * (length - filled), int(pct * 100)

def get_data():
    token = os.getenv('GH_TOKEN')
    if not token: raise ValueError("GH_TOKEN is missing")
    
    auth = Auth.Token(token)
    g = Github(auth=auth)
    user = g.get_user(USERNAME)
    
    now = datetime.now(pytz.utc)
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    rows = []
    total_commits = 0
    mermaid_data = ""
    
    print(f"Fetch start: {start_of_week.strftime('%Y-%m-%d')}")

    for repo_name, config in REPOS.items():
        try:
            repo = user.get_repo(repo_name)
            count = repo.get_commits(since=start_of_week, author=USERNAME).totalCount
            
            goal = config['goal']
            label = config['label']
            total_commits += count
            
            bar, pct = generate_ascii_bar(count, goal)
            status = "✅" if count >= goal else "🚧" if count > 0 else "💤"
            
            rows.append(f"| {status} **{label}** | `{bar}` | **{pct}%** | **{count}/{goal}** |")
            
            val = count if count > 0 else 0.01
            mermaid_data += f'    "{label}" : {val}\n'
            
        except Exception as e:
            print(f"Error {repo_name}: {e}")
            rows.append(f"| ❌ {repo_name} | Error | 0% | 0/0 |")

    return rows, total_commits, mermaid_data

# ==========================================
# 📝 WRITE TO FILE
# ==========================================

if __name__ == "__main__":
    rows, total, pie_data = get_data()
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    tracker_html = f"""
<div align="center">
<h3>🚀 Weekly Engineering Velocity</h3>
<p><i>Last updated: {now_str}</i></p>

| Repository | Weekly Progress | % | Status |
| :--- | :--- | :--- | :--- |
""" + "\n".join(rows) + "\n</div>"

    badge_html = f'\n<p align="center"><img src="https://img.shields.io/badge/Total_Commits-{total}-2E64FE?style=for-the-badge&logo=github&logoColor=white" /></p>\n'

    mermaid_block = "```mermaid\n"
    mermaid_block += "%%{init: {'theme': 'dark', 'themeVariables': { 'pie1': '#800020', 'pie2': '#2E64FE', 'pie3': '#2ea44f', 'pie4': '#dbab09' }}}%%\n"
    mermaid_block += "pie title Work Distribution\n"
    mermaid_block += pie_data
    mermaid_block += "```\n"

    full_readme = HEADER_TOP + "\n" + ARSENAL_HTML + "\n" + tracker_html + "\n" + badge_html + "\n" + mermaid_block + "\n" + FOOTER_HTML

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(full_readme)
    
    print("✅ README.md successfully rebuilt.")
