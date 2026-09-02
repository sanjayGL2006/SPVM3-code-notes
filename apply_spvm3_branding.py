import os
import glob
import re

# New SPVM3 Tech Solution Global Navigation Bar
SPVM3_HEADER_NAV = """<!-- SPVM3 TECH SOLUTION GLOBAL HEADER -->
<div id="techvault-global-header" style="position: sticky; top: 0; z-index: 99999; background: #0b0f19; border-bottom: 1px solid rgba(99, 102, 241, 0.3); padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif; color: #f8fafc; box-shadow: 0 4px 20px rgba(0,0,0,0.5); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);">
  <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
    <a href="index.html" style="display: inline-flex; align-items: center; gap: 10px; background: linear-gradient(135deg, #6366f1, #06b6d4); color: #ffffff; padding: 8px 18px; border-radius: 10px; text-decoration: none; font-weight: 800; font-size: 0.95rem; box-shadow: 0 4px 14px rgba(99,102,241,0.4); transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
      <span style="font-size: 1.1rem;">⚡</span>
      <span>SPVM3 Tech Solution</span>
    </a>
    <span style="font-size: 0.85rem; background: rgba(99,102,241,0.15); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); padding: 4px 12px; border-radius: 20px; font-weight: 600;" class="tv-subject-label">💻 All Computer Based Notes</span>
  </div>
  <div style="display: flex; align-items: center; gap: 12px;">
    <select onchange="if(this.value) window.location.href=this.value;" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(99,102,241,0.4); color: #f8fafc; padding: 8px 16px; border-radius: 10px; font-size: 0.88rem; outline: none; cursor: pointer; max-width: 340px; font-weight: 500;">
      <option value="" disabled selected style="background:#0f172a; color:#fff;">🔀 Select Computer Based Note...</option>
      <option value="index.html" style="background:#0f172a; color:#fff;">🏠 SPVM3 Tech Solution Hub (All 18 Notes)</option>
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
<!-- END SPVM3 TECH SOLUTION GLOBAL HEADER -->
"""

# SPVM3 Unified Design Tokens & Theme Override CSS
SPVM3_UNIFIED_CSS = """<!-- SPVM3 TECH SOLUTION UNIFIED DESIGN THEME -->
<style id="spvm3-theme-sync">
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
  
  :root {
    --spvm3-primary: #6366f1;
    --spvm3-cyan: #06b6d4;
    --spvm3-dark: #0b0f19;
    --spvm3-card-bg: rgba(18, 26, 43, 0.75);
    --spvm3-border: rgba(99, 102, 241, 0.25);
  }

  ::selection {
    background: #6366f1 !important;
    color: #ffffff !important;
  }

  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  ::-webkit-scrollbar-track {
    background: #0b0f19;
  }
  ::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #6366f1;
  }

  /* SPVM3 Brand Footer Injection */
  .spvm3-global-footer {
    background: #0b0f19;
    border-top: 1px solid rgba(99, 102, 241, 0.3);
    padding: 30px 20px;
    text-align: center;
    color: #94a3b8;
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    font-size: 0.9rem;
    margin-top: 60px;
  }
  .spvm3-global-footer strong {
    color: #f1f5f9;
  }
</style>
"""

# Process all 18 subject files
files = glob.glob("*.html")
subject_names = {
    "C-Programming-Complete-Notes.html": "C Programming Complete Notes",
    "cpp-notes.html": "C++ Programming Notes",
    "DBMS-and-SQL-Complete-Reference.html": "DBMS & SQL Complete Reference Notes",
    "deep-learning-notes.html": "Deep Learning & AI Notes",
    "docker-notes.html": "Docker Containerization Notes",
    "electron-js-notes.html": "Electron.js Desktop Apps Notes",
    "fundamentals-of-computers-notes.html": "Fundamentals of Computers Notes",
    "git-clone-guide.html": "Git & Version Control Notes",
    "HTML-CSS-Complete-Notes.html": "HTML & CSS Complete Notes",
    "java-notes.html": "Java Brewed Complete Notes",
    "js-notes.html": "JavaScript A–Z Interactive Notes",
    "kubernetes-a-to-z-guide.html": "Kubernetes Orchestration Notes",
    "operating-systems-complete-notes.html": "Operating Systems Notes",
    "php-notes.html": "PHP Complete Reference Notes",
    "python_notes.html": "Python A–Z Master Notes",
    "react-field-manual.html": "React Field Manual Notes",
    "react-notes.html": "React.js Complete Interactive Notes",
    "software-testing-notes.html": "Software Testing & QA Notes"
}

updated_count = 0

for f in files:
    if f in ["index.html", "all-subject-notes.html"]:
        continue
    
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    # 1. Remove old header if exists
    if "<!-- TECHVAULT GLOBAL NAVIGATION BAR -->" in content:
        pattern = re.compile(r"<!-- TECHVAULT GLOBAL NAVIGATION BAR -->.*?<!-- END TECHVAULT GLOBAL NAVIGATION BAR -->\n?", re.DOTALL)
        content = re.sub(pattern, "", content)
    if "<!-- SPVM3 TECH SOLUTION GLOBAL HEADER -->" in content:
        pattern = re.compile(r"<!-- SPVM3 TECH SOLUTION GLOBAL HEADER -->.*?<!-- END SPVM3 TECH SOLUTION GLOBAL HEADER -->\n?", re.DOTALL)
        content = re.sub(pattern, "", content)

    # 2. Inject updated SPVM3 Global Navigation Bar right after <body>
    if "<body>" in content:
        content = content.replace("<body>", "<body>\n" + SPVM3_HEADER_NAV, 1)
    elif "<body" in content:
        pos = content.find("<body")
        end_pos = content.find(">", pos)
        if end_pos != -1:
            content = content[:end_pos+1] + "\n" + SPVM3_HEADER_NAV + content[end_pos+1:]

    # 3. Inject SPVM3 Unified Design CSS in <head>
    if "spvm3-theme-sync" not in content:
        if "</head>" in content:
            content = content.replace("</head>", SPVM3_UNIFIED_CSS + "\n</head>", 1)

    # 4. Standardize Title tag
    sub_name = subject_names.get(f, "Computer Based Notes")
    new_title = f"<title>{sub_name} — SPVM3 Tech Solution (All Computer Based Notes)</title>"
    content = re.sub(r"<title>.*?</title>", new_title, content, flags=re.IGNORECASE)

    # 5. Append SPVM3 Brand Footer before </body> if not present
    if "spvm3-global-footer" not in content and "</body>" in content:
        footer_html = """
<footer class="spvm3-global-footer">
  <p><strong>SPVM3 Tech Solution</strong> — All Computer Based Notes & Software Engineering Library.</p>
  <p style="margin-top: 6px; font-size: 0.8rem; opacity: 0.8;">Complete Reference Field Notes • Built for Professional Learning</p>
</footer>
"""
        content = content.replace("</body>", footer_html + "\n</body>", 1)

    with open(f, "w", encoding="utf-8") as file:
        file.write(content)
    
    updated_count += 1
    print(f"Updated SPVM3 branding & design on {f}")

print(f"\nSuccessfully applied SPVM3 Tech Solution branding and uniform design across {updated_count} files!")
