import os
import re

NEW_SUBJECTS_JS = """,
  {
    id: "ai-systems",
    title: "AI Systems & LLM Agents Notes",
    file: "ai-systems-notes.html",
    category: "ai",
    level: "Advanced",
    readTime: "60 min",
    readTimeMin: 60,
    accent: "#06b6d4",
    accentDark: "#0891b2",
    icon: "🤖",
    description: "Autonomous Intelligent Agents, Multi-Agent Systems, ReAct Loops, LLM/VLM/SLM/LCM Architectures.",
    topics: ["Intelligent Agent Types", "LLM / VLM / SLM Models", "ReAct Loops & Tool Use", "Multi-Agent Frameworks", "Hierarchical Control Stacks", "Generative AI Architectures"]
  },
  {
    id: "blockchain",
    title: "Blockchain & Cryptography Notes",
    file: "blockchain-notes.html",
    category: "systems",
    level: "Advanced",
    readTime: "60 min",
    readTimeMin: 60,
    accent: "#e2933d",
    accentDark: "#c98f10",
    icon: "⛓️",
    description: "Cryptographic Hashing, Proof of Work/Stake, Merkle Trees, zk-SNARKs & Layer-2 Rollups.",
    topics: ["Cryptographic Hashes", "Consensus Algorithms", "Merkle Tree Proofs", "Smart Contracts & Gas", "zk-SNARKs & zk-STARKs", "Layer-2 Rollups"]
  },
  {
    id: "dsa-notes",
    title: "Data Structures & Algorithms (DSA) Notes",
    file: "data-structures-notes.html",
    category: "systems",
    level: "Intermediate to Advanced",
    readTime: "75 min",
    readTimeMin: 75,
    accent: "#7fe0b3",
    accentDark: "#059669",
    icon: "🧩",
    description: "Linear & Non-Linear Data Structures, Linked Lists, Trees, Graphs, Sorting & Complexity.",
    topics: ["Arrays & Linked Lists", "Stack & Queue (LIFO/FIFO)", "Binary Search Trees", "Graph Algorithms (BFS/DFS)", "Sorting Algorithms", "Time & Space Complexity"]
  }
"""

files_to_update = ["index.html", "all-subject-notes.html"]

for f in files_to_update:
    if not os.path.exists(f):
        continue
    
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    
    # 1. Update text counters (18 -> 21)
    content = content.replace("18 Connected Subjects", "21 Connected Subjects")
    content = content.replace("All Computer Based Notes (18 Subjects)", "All Computer Based Notes (21 Subjects)")
    content = content.replace("0 / 18 Notes Completed", "0 / 21 Notes Completed")
    content = content.replace("Showing 18 of 18 subjects", "Showing 21 of 21 subjects")
    content = content.replace("All (18)", "All (21)")
    content = content.replace("Systems & Core (3)", "Systems & Core (5)")
    content = content.replace("AI & Testing (2)", "AI & Testing (3)")
    content = content.replace("TechVault Hub (All 18 Notes)", "TechVault Hub (All 21 Notes)")
    content = content.replace("SPVM3 Tech Solution Hub (All 18 Notes)", "SPVM3 Tech Solution Hub (All 21 Notes)")

    # 2. Append new subjects to SUBJECTS_DATA in JS
    if "ai-systems" not in content and 'id: "deep-learning"' in content:
        target_str = 'id: "deep-learning"'
        pos = content.find(target_str)
        closing_bracket_pos = content.find('}', pos)
        if closing_bracket_pos != -1:
            content = content[:closing_bracket_pos+1] + NEW_SUBJECTS_JS + content[closing_bracket_pos+1:]

    with open(f, "w", encoding="utf-8") as file:
        file.write(content)
    
    print(f"Updated datasets and counters in {f}")

print("\nSuccessfully updated master hub datasets to 21 subjects!")
