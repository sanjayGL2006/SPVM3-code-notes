import os
import glob
import re

files = glob.glob("*.html")
updated_count = 0

for f in files:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    if "verify-certificate.html" in content and f != "verify-certificate.html":
        # Already has link or is the verification page
        pass

    # Update global header dropdown or button bar
    if "<!-- SPVM3 TECH SOLUTION GLOBAL HEADER -->" in content:
        # Check if verify-certificate link is in the header
        if 'value="verify-certificate.html"' not in content:
            old_opt = '<option value="index.html" style="background:#0f172a; color:#fff;">🏠 SPVM3 Tech Solution Hub (All 18 Notes)</option>'
            new_opt = old_opt + '\n      <option value="verify-certificate.html" style="background:#0f172a; color:#fff;">🔍 Verify Certificate Portal</option>'
            content = content.replace(old_opt, new_opt)
            
            with open(f, "w", encoding="utf-8") as file:
                file.write(content)
            updated_count += 1
            print(f"Added Verify Certificate option to header in {f}")

print(f"\nUpdated header dropdown in {updated_count} files!")
