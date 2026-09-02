import os
import glob

ALL_OPTIONS_HTML = """      <option value="" disabled selected style="background:#0f172a; color:#fff;">🔀 Select Computer Based Note...</option>
      <option value="index.html" style="background:#0f172a; color:#fff;">🏠 SPVM3 Tech Solution Hub (All 21 Notes)</option>
      <option value="verify-certificate.html" style="background:#0f172a; color:#fff;">🔍 Verify Certificate Portal</option>
      <option value="ai-systems-notes.html" style="background:#0f172a; color:#fff;">🤖 AI Systems & LLM Agents Notes</option>
      <option value="blockchain-notes.html" style="background:#0f172a; color:#fff;">⛓️ Blockchain & Cryptography Notes</option>
      <option value="data-structures-notes.html" style="background:#0f172a; color:#fff;">🧩 Data Structures & Algorithms (DSA)</option>
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
      <option value="deep-learning-notes.html" style="background:#0f172a; color:#fff;">🧠 Deep Learning & AI Notes</option>"""

files = glob.glob("*.html")
updated_count = 0

for f in files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    if "<select" in content and "</select>" in content:
        start_pos = content.find("<select")
        open_tag_end = content.find(">", start_pos)
        end_pos = content.find("</select>", open_tag_end)
        
        if open_tag_end != -1 and end_pos != -1:
            new_content = content[:open_tag_end+1] + "\n" + ALL_OPTIONS_HTML + "\n    " + content[end_pos:]
            with open(f, "w", encoding="utf-8") as file:
                file.write(new_content)
            updated_count += 1
            print(f"Updated dropdown selector in {f}")

print(f"\nSuccessfully updated dropdown menus across {updated_count} HTML files!")
