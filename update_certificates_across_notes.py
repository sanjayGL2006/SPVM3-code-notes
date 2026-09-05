import os
import glob
import re

# Map file basenames to subject IDs
FILE_TO_SUBJECT_ID = {
  "HTML-CSS-Complete-Notes.html": "html-css",
  "js-notes.html": "javascript",
  "react-notes.html": "react-notes",
  "react-field-manual.html": "react-manual",
  "electron-js-notes.html": "electron-js",
  "php-notes.html": "php-notes",
  "python_notes.html": "python-notes",
  "C-Programming-Complete-Notes.html": "c-programming",
  "cpp-notes.html": "cpp-notes",
  "java-notes.html": "java-notes",
  "DBMS-and-SQL-Complete-Reference.html": "dbms-sql",
  "operating-systems-complete-notes.html": "operating-systems",
  "fundamentals-of-computers-notes.html": "computer-fundamentals",
  "software-testing-notes.html": "software-testing",
  "git-clone-guide.html": "git-guide",
  "docker-notes.html": "docker-notes",
  "kubernetes-a-to-z-guide.html": "kubernetes-guide",
  "deep-learning-notes.html": "deep-learning"
}

files = glob.glob("*.html")
updated_files = 0

for f in files:
    if f in ["index.html", "all-subject-notes.html"]:
        continue
    
    sub_id = FILE_TO_SUBJECT_ID.get(f)
    if not sub_id:
        continue
    
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    # 1. Inject script import in <head> if not present
    if "spvm3_certificate_system.js" not in content:
        if "</head>" in content:
            content = content.replace("</head>", '<script src="spvm3_certificate_system.js"></script>\n</head>', 1)

    # 2. Update Header Bar to include "🎓 Get Certificate" button
    old_header_pattern = re.compile(r"<!-- SPVM3 TECH SOLUTION GLOBAL HEADER -->.*?<!-- END SPVM3 TECH SOLUTION GLOBAL HEADER -->\n?", re.DOTALL)
    
    new_header = f"""<!-- SPVM3 TECH SOLUTION GLOBAL HEADER -->
<div id="techvault-global-header" style="position: sticky; top: 0; z-index: 99999; background: #0b0f19; border-bottom: 1px solid rgba(99, 102, 241, 0.3); padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif; color: #f8fafc; box-shadow: 0 4px 20px rgba(0,0,0,0.5); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);">
  <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
    <a href="index.html" style="display: inline-flex; align-items: center; gap: 10px; background: linear-gradient(135deg, #6366f1, #06b6d4); color: #ffffff; padding: 8px 18px; border-radius: 10px; text-decoration: none; font-weight: 800; font-size: 0.95rem; box-shadow: 0 4px 14px rgba(99,102,241,0.4); transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
      <span style="font-size: 1.1rem;">⚡</span>
      <span>SPVM3 Tech Solution</span>
    </a>
    <span style="font-size: 0.85rem; background: rgba(99,102,241,0.15); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); padding: 4px 12px; border-radius: 20px; font-weight: 600;" class="tv-subject-label">💻 All Computer Based Notes</span>
  </div>
  <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
    <button onclick="showSPVM3LoginModal()" class="spvm3-login-btn" id="spvm3-header-login-btn" style="background: rgba(99,102,241,0.2); color: #38bdf8; border: 1px solid #6366f1; padding: 8px 14px; border-radius: 8px; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'">
      🔑 Account / Login
    </button>
    <button onclick="showSPVM3Certificate('{sub_id}')" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: #ffffff; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 700; font-size: 0.85rem; cursor: pointer; box-shadow: 0 4px 12px rgba(245,158,11,0.35); transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'">
      🎓 Get Certificate (80% Req)
    </button>
    <select onchange="if(this.value) window.location.href=this.value;" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(99,102,241,0.4); color: #f8fafc; padding: 8px 14px; border-radius: 10px; font-size: 0.88rem; outline: none; cursor: pointer; max-width: 300px; font-weight: 500;">
      <option value="" disabled selected style="background:#0f172a; color:#fff;">🔀 Select Computer Based Note...</option>
      <option value="index.html" style="background:#0f172a; color:#fff;">🏠 SPVM3 Tech Solution Hub (All Notes)</option>
      <option value="HTML-CSS-Complete-Notes.html" style="background:#0f172a; color:#fff;">🌐 HTML & CSS Complete Notes</option>
      <option value="js-notes.html" style="background:#0f172a; color:#fff;">⚡ JavaScript A–Z Notes</option>
      <option value="react-notes.html" style="background:#0f172a; color:#fff;">⚛️ React.js Reference Notes</option>
      <option value="react-field-manual.html" style="background:#0f172a; color:#fff;">📘 React Field Manual</option>
      <option value="electron-js-notes.html" style="background:#0f172a; color:#fff;">💻 Electron.js Desktop Notes</option>
      <option value="php-notes.html" style="background:#0f172a; color:#fff;">🐘 PHP Complete Notes</option>
      <option value="python_notes.html" style="background:#0f172a; color:#fff;">🐍 Python A–Z Master Notes</option>
      <option value="C-Programming-Complete-Notes.html" style="background:#0f172a; color:#fff;">🔤 C Programming Complete Notes</option>
      <option value="cpp-notes.html" style="background:#0f172a; color:#fff;">⚡ C++ Interactive Notes</option>
      <option value="java-notes.html" style="background:#0f172a; color:#fff;">☕ Java Brewed Complete Notes</option>
      <option value="DBMS-and-SQL-Complete-Reference.html" style="background:#0f172a; color:#fff;">🗄️ DBMS & SQL Complete Reference</option>
      <option value="operating-systems-complete-notes.html" style="background:#0f172a; color:#fff;">🖥️ Operating Systems Notes</option>
      <option value="fundamentals-of-computers-notes.html" style="background:#0f172a; color:#fff;">🕹️ Fundamentals of Computers Notes</option>
      <option value="software-testing-notes.html" style="background:#0f172a; color:#fff;">🧪 Software Testing & QA Notes</option>
      <option value="git-clone-guide.html" style="background:#0f172a; color:#fff;">🌿 Git & Version Control Guide</option>
      <option value="docker-notes.html" style="background:#0f172a; color:#fff;">🐳 Docker Interactive Guide</option>
      <option value="kubernetes-a-to-z-guide.html" style="background:#0f172a; color:#fff;">☸️ Kubernetes A to Z Guide</option>
      <option value="deep-learning-notes.html" style="background:#0f172a; color:#fff;">🧠 Deep Learning & AI Notes</option>
    </select>
  </div>
</div>
<script>document.addEventListener('DOMContentLoaded', () => {{ if (typeof initAutoScrollProgressTracker === 'function') initAutoScrollProgressTracker('{sub_id}'); }});</script>
<!-- END SPVM3 TECH SOLUTION GLOBAL HEADER -->
"""
    if "<!-- SPVM3 TECH SOLUTION GLOBAL HEADER -->" in content:
        content = re.sub(old_header_pattern, new_header, content)
    else:
        if "<body>" in content:
            content = content.replace("<body>", "<body>\n" + new_header, 1)

    with open(f, "w", encoding="utf-8") as file:
        file.write(content)
    
    updated_files += 1
    print(f"Added Certificate Button to header of {f}")

print(f"\nFinished updating certificate buttons across {updated_files} subject files!")
