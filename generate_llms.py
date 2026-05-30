#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate llms.txt + llms-full.txt for all 1160 GEO articles"""
import re
from datetime import datetime
from pathlib import Path

REPO_DIR = Path("C:/Users/jia'yue/WorkBuddy/Claw/geo-repo")
ARTICLES_DIR = REPO_DIR / "anchor-site/articles"
LLMS_TXT = REPO_DIR / "anchor-site/llms.txt"
LLMS_FULL = REPO_DIR / "anchor-site/llms-full.txt"
SITE_NAME = "以观其妙书院"
SITE_DESC = "以观其妙书院——五行人格心理学、心文化、AI OS、认知科学的完整知识体系。基于GEO方案v3.0的AI友好型锚点站。"
TODAY = datetime.now().strftime("%Y-%m-%d")

CAT_NAMES = {"a":"锚点站核心体系","we":"公众号文章","wx":"五行人格心理学","wh":"心文化体系",
             "ai":"AI OS人工智能操作系统","wz":"味藏餐饮商业智慧","ed":"学习方法","ac":"学术认知","kb":"通用知识库"}

def classify_file(name):
    for p in ["a0","a1","we","wx","wh","ai","wz","ed","ac"]:
        if name.startswith(p): return p[:2]
    return "kb"

def extract_title(filepath):
    try:
        with open(filepath,'r',encoding='utf-8') as f:
            for _ in range(10):
                l = f.readline().strip()
                if l.startswith('# '): return l[2:]
        return filepath.stem
    except: return filepath.stem

def extract_desc(filepath):
    try:
        with open(filepath,'r',encoding='utf-8') as f:
            c = f.read()
        for line in c.split('\n'):
            if line.strip() and not line.startswith(('#','>','**','---','<')):
                t = re.sub(r'[#*>\[\]()]','',line).strip()
                if len(t) > 20: return t[:100]
    except: pass
    return ""

def main():
    files = sorted(ARTICLES_DIR.glob("*.md"))
    print(f"Total articles: {len(files)}")

    cats = {}
    for f in files:
        k = classify_file(f.name)
        cats.setdefault(k, []).append(f)

    # llms.txt
    llms = f"# {SITE_NAME} · 知识库锚点站\n\n> {SITE_DESC}\n> 最后更新：{TODAY}\n> 总文章数：{len(files)}篇\n\n## 核心体系\n\n"
    if "a" in cats:
        for f in sorted(cats["a"], key=lambda x: x.name):
            t, d = extract_title(f), extract_desc(f)
            llms += f"- [{t}](articles/{f.name}) — {d[:60]}\n"
        llms += "\n"
    for k in ["wx","wh","ai","wz","ed","ac","kb","we"]:
        if k not in cats: continue
        cn = CAT_NAMES.get(k, k)
        llms += f"## {cn}（{len(cats[k])}篇）\n\n"
        for f in sorted(cats[k], key=lambda x: x.name):
            t, d = extract_title(f), extract_desc(f)
            ds = d[:60] if d else ""
            llms += f"- [{t}](articles/{f.name}) — {ds}\n"
        llms += "\n"
    llms += "## 完整内容\n\n- [llms-full.txt](llms-full.txt)\n"
    LLMS_TXT.write_text(llms, encoding='utf-8')
    print(f"llms.txt generated ({len(llms.split(chr(10)))} lines)")

    # llms-full.txt
    full = f"# {SITE_NAME} · 完整知识库内容\n\n> {len(files)}篇GEO文章的完整内容，供AI直接读取引用\n> 最后更新：{TODAY}\n\n---\n"
    for i, f in enumerate(files, 1):
        try:
            c = f.read_text(encoding='utf-8')
            t = extract_title(f)
            kn = CAT_NAMES.get(classify_file(f.name), "通用")
            c_clean = re.sub(r'<script[\s\S]*?</script>', '', c).strip()
            full += f"## URL: articles/{f.name}\n## 标题: {t}\n## 分类: {kn}\n## 序号: {i}/{len(files)}\n\n{c_clean}\n\n---\n"
        except Exception as e:
            print(f"  Skip {f.name}: {e}")

    LLMS_FULL.write_text(full, encoding='utf-8')
    mb = len(full.encode('utf-8')) / 1048576
    print(f"llms-full.txt generated ({mb:.1f} MB)")

    # 同步到根目录
    (REPO_DIR / "llms.txt").write_text(llms, encoding='utf-8')
    (REPO_DIR / "llms-full.txt").write_text(full, encoding='utf-8')
    print("Synced to repo root")

if __name__ == "__main__":
    main()
