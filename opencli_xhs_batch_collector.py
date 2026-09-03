import subprocess
import json
import os
import re

KEYWORDS = [
    "仙逆 王林 凝气期 壁纸",
    "仙逆 王林 筑基期 壁纸",
    "仙逆 王林 结丹期 壁纸",
    "仙逆 白发王林 高清",
    "仙逆 黑发王林 高清",
    "仙逆 王林 本尊 4K壁纸",
    "仙逆 王林 化神期 壁纸",
    "仙逆 王林 婴变期 壁纸",
    "仙逆 王林 问鼎期 壁纸",
    "仙逆 王林 极境 壁纸 高清"
]

def run_opencli_xhs_search(query):
    cmd = f'opencli xiaohongshu search "{query}" -f json'
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=25)
        if res.returncode == 0 and res.stdout.strip():
            data = json.loads(res.stdout.strip())
            return data
    except Exception as e:
        print(f"Error search '{query}': {e}")
    return []

all_results = {}

for kw in KEYWORDS:
    print(f"\nSearching Xiaohongshu for: {kw}")
    notes = run_opencli_xhs_search(kw)
    print(f"  Found {len(notes)} notes")
    all_results[kw] = notes[:5] # save top 5 notes for each

with open(r'D:\逆天主题\workers\xiaohongshu_search_results.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print("\nXiaohongshu search finished successfully!")
