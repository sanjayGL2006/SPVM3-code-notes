import os
import glob

HEADER_NAV = """<!-- TECHVAULT GLOBAL NAVIGATION BAR -->
<div id="techvault-global-header" style="position: sticky; top: 0; z-index: 99999; background: #0b0f19; border-bottom: 1px solid rgba(255,255,255,0.12); padding: 10px 24px; display: flex; align-items: center; justify-content: space-between; font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif; color: #f8fafc; box-shadow: 0 4px 20px rgba(0,0,0,0.4); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);">
  <div style="display: flex; align-items: center; gap: 14px;">
    <a href="index.html" style="display: inline-flex; align-items: center; gap: 8px; background: linear-gradient(135deg, #6366f1, #06b6d4); color: #ffffff; padding: 7px 16px; border-radius: 8px; text-decoration: none; font-weight: 700; font-size: 0.88rem; box-shadow: 0 4px 12px rgba(99,102,241,0.35); transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
      <span>🏠 Hub</span>
      <span style="opacity: 0.85;">| All Subject Notes</span>
    </a>
    <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 600;" class="tv-subject-label">⚡ TechVault Connected Library</span>
  </div>
  <div style="display: flex; align-items: center; gap: 12px;">
    <select onchange="if(this.value) window.location.href=this.value;" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.2); color: #f8fafc; padding: 7px 14px; border-radius: 8px; font-size: 0.85rem; outline: none; cursor: pointer; max-width: 320px;">
      <option value="" disabled selected style="background:#0f172a; color:#fff;">🔀 Switch Subject Note...</option>
      <option value="index.html" style="background:#0f172a; color:#fff;">🏠 TechVault Hub (All 18 Notes)</option>
      <option value="HTML-CSS-Complete-Notes.html" style="background:#0f172a; color:#fff;">🌐 HTML & CSS Field Notes</option>
      <option value="js-notes.html" style="background:#0f172a; color:#fff;">⚡ JavaScript A–Z Notes</option>
      <option value="react-notes.html" style="background:#0f172a; color:#fff;">⚛️ React.js Interactive Reference</option>
      <option value="react-field-manual.html" style="background:#0f172a; color:#fff;">📘 React Field Manual</option>
      <option value="electron-js-notes.html" style="background:#0f172a; color:#fff;">💻 Electron.js Desktop Apps</option>
      <option value="php-notes.html" style="background:#0f172a; color:#fff;">🐘 PHP Notes from Scratch</option>
      <option value="python_notes.html" style="background:#0f172a; color:#fff;">🐍 Python A–Z Master Notes</option>
      <option value="C-Programming-Complete-Notes.html" style="background:#0f172a; color:#fff;">🔤 C Programming Complete</option>
      <option value="cpp-notes.html" style="background:#0f172a; color:#fff;">⚡ C++ Interactive Notes</option>
      <option value="java-notes.html" style="background:#0f172a; color:#fff;">☕ Java Brewed Notes</option>
      <option value="DBMS-and-SQL-Complete-Reference.html" style="background:#0f172a; color:#fff;">🗄️ DBMS & SQL Reference</option>
      <option value="operating-systems-complete-notes.html" style="background:#0f172a; color:#fff;">🖥️ Operating Systems Reference</option>
      <option value="fundamentals-of-computers-notes.html" style="background:#0f172a; color:#fff;">🕹️ Computer Fundamentals</option>
      <option value="software-testing-notes.html" style="background:#0f172a; color:#fff;">🧪 Software Testing & QA</option>
      <option value="git-clone-guide.html" style="background:#0f172a; color:#fff;">🌿 Git & Version Control</option>
      <option value="docker-notes.html" style="background:#0f172a; color:#fff;">🐳 Docker Interactive Guide</option>
      <option value="kubernetes-a-to-z-guide.html" style="background:#0f172a; color:#fff;">☸️ Kubernetes A to Z Guide</option>
      <option value="deep-learning-notes.html" style="background:#0f172a; color:#fff;">🧠 Deep Learning & AI Notes</option>
    </select>
  </div>
</div>
<!-- END TECHVAULT GLOBAL NAVIGATION BAR -->
"""

files = glob.glob("*.html")
excluded = ["index.html", "all-subject-notes.html"]

count = 0
for f in files:
    if f in excluded:
        continue
    
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    if "techvault-global-header" in content:
        print(f"Skipping {f}, already injected.")
        continue
    
    if "<body>" in content:
        new_content = content.replace("<body>", "<body>\n" + HEADER_NAV, 1)
        with open(f, "w", encoding="utf-8") as file:
            file.write(new_content)
        count += 1
        print(f"Successfully injected header into {f}")
    elif "<body" in content:
        # Handle cases with body class or attributes
        pos = content.find("<body")
        end_pos = content.find(">", pos)
        if end_pos != -1:
            new_content = content[:end_pos+1] + "\n" + HEADER_NAV + content[end_pos+1:]
            with open(f, "w", encoding="utf-8") as file:
                file.write(new_content)
            count += 1
            print(f"Successfully injected header into {f} (with attributes)")

print(f"Finished! Injected global header into {count} files.")
