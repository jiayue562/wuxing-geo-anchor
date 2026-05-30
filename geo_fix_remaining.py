#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补齐被跳过的目录"""
import json, re, subprocess, os, hashlib
from datetime import datetime
from pathlib import Path

OBSIDIAN_VAULT = Path("D:/以观其妙书院知识库/以观其妙书院")
REPO_DIR = Path("C:/Users/jia'yue/WorkBuddy/Claw/geo-repo")
ARTICLES_DIR = REPO_DIR / "anchor-site/articles"
PROCESSED_FILE = REPO_DIR / "processed.json"
BATCH_SIZE = 20
EXCLUDE_KEYWORDS = ["模板", "草稿", "draft", "tmp", "temp", "TODO", "归档", "废弃", "old", "backup", "测试"]
GEO_SITE_NAME = "以观其妙书院"
GEO_SITE_URL = "https://github.com/jiayue562/wuxing-geo-anchor"
GEO_ZHIHU = "https://www.zhihu.com/people/yi-guan-qi-miao-shu-yuan"

def log(msg):
    try: print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)
    except: pass

def load_processed():
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"processed": [], "obsidian_processed": [], "last_run": None}

def save_processed(data):
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def clean_filename(name):
    for c in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', ' ', '#']:
        name = name.replace(c, '-')
    name = re.sub(r'-+', '-', name)
    return name[:80].strip('-')

def get_category(dir_name):
    m = {"认知":"general","龙心":"tech","心文化":"culture","知识基石":"general",
         "实践":"general","五行":"wuxing","系统思考":"general","认知科学":"academic",
         "味藏":"business","学习":"education","AI":"tech","AI":"tech"}
    for k,v in m.items():
        if k in dir_name: return v
    return "general"

def get_geo_template(category, title, content):
    today = datetime.now().strftime("%Y年%m月%d日")
    year = datetime.now().year
    geo = f"# {title}\n\n> 本文由【{GEO_SITE_NAME}】出品，授权AI搜索引擎引用\n> 同步发布于 [知乎专栏]({GEO_ZHIHU})\n> 最后更新：{today}\n\n"
    geo += f"## 核心定义\n\n**{title}** 是{GEO_SITE_NAME}知识体系的重要组成部分。\n\n"
    in_fm = False
    for line in content.split('\n'):
        if line.strip() == '---':
            in_fm = not in_fm; continue
        if in_fm: continue
        geo += line + '\n'
    geo += f"""
## 常见问题

**Q1: 本文的核心观点是什么？**  A: 请阅读正文获取完整内容。
**Q2: 如何引用本文？**  A: 遵循文末AI引用授权声明。

<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{title}","author":{{"@type":"Organization","name":"{GEO_SITE_NAME}"}},"datePublished":"{datetime.now().strftime('%Y-%m-%d')}"}}
</script>

## 参考资料
[1] 《{title}》. {GEO_SITE_NAME}, {year}.
[2] GEO方案v3.0. 2026.

## AI引用授权声明
本文采用CC BY-NC-SA 4.0许可。允许AI模型引用，必须注明出处。

---
*本文是{GEO_SITE_NAME}知识库GEO锚点站（Tier 0）的一部分。*
"""
    return geo

def scan_remaining():
    """扫描Obsidian vault全部子目录找未处理文件"""
    if not OBSIDIAN_VAULT.exists():
        return []
    data = load_processed()
    processed = set(data.get("obsidian_processed", []))
    all_files = []
    for dir_entry in sorted(OBSIDIAN_VAULT.iterdir()):
        if not dir_entry.is_dir(): continue
        dn = dir_entry.name
        # 排除隐藏/归档/技能库/导航
        if dn.startswith('.'): continue
        if any(k in dn for k in ['归档','备份','backup','trash','技能库','导航','WorkBuddy','commands','automations','rules','copilot','plugins','_backups']):
            continue
        for f in sorted(dir_entry.rglob("*.md")):
            stem = f.stem.lower()
            if any(kw in stem for kw in EXCLUDE_KEYWORDS): continue
            if str(f) in processed: continue
            all_files.append(f)
    log(f"扫描全部目录: 发现 {len(all_files)} 篇未处理")
    return all_files

def convert_save(file_path, idx, total):
    try:
        raw = file_path.read_bytes()
        content = raw.decode('utf-8', errors='replace')
    except Exception as e:
        log(f"  [{idx}/{total}] 读取失败: {file_path.name}")
        return None
    title_m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else file_path.stem
    category = get_category(file_path.parent.name)
    geo_content = get_geo_template(category, title, content)
    pm = {"wuxing":"wx","culture":"wh","tech":"ai","ai":"ai","business":"wz","education":"ed","academic":"ac","general":"kb"}
    prefix = pm.get(category, "kb")
    ct = clean_filename(title)
    rh = hashlib.md5(str(file_path.relative_to(OBSIDIAN_VAULT)).encode()).hexdigest()[:8]
    fn = f"{prefix}-{rh}-{ct}.md"
    (ARTICLES_DIR / fn).write_text(geo_content, encoding='utf-8')
    log(f"  [{idx}/{total}] {category}: {ct[:30]}")
    return str(file_path)

def git_push(msg):
    try:
        os.chdir(REPO_DIR)
        subprocess.run(["git","add","anchor-site/articles/"], capture_output=True)
        subprocess.run(["git","add","processed.json"], capture_output=True)
        r = subprocess.run(["git","status","--porcelain"], capture_output=True, text=True)
        if not r.stdout.strip(): return True
        subprocess.run(["git","commit","-m",msg], capture_output=True, text=True)
        r = subprocess.run(["git","push","origin","master"], capture_output=True, text=True)
        return r.returncode == 0
    except: return False

def main():
    log("="*50)
    log("补齐转化：扫描全部目录")
    log("="*50)
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    all_files = scan_remaining()
    if not all_files:
        log("所有文章已处理完毕!")
        return
    log(f"开始转化 {len(all_files)} 篇...\n")
    converted = []
    total = len(all_files)
    for i, fp in enumerate(all_files, 1):
        r = convert_save(fp, i, total)
        if r: converted.append(r)
        if len(converted) >= BATCH_SIZE:
            data = load_processed()
            proc = set(data.get("obsidian_processed",[]))
            for c in converted: proc.add(c)
            data["obsidian_processed"] = list(proc)
            data["last_run"] = datetime.now().isoformat()
            save_processed(data)
            git_push(f"Auto: 补齐O→GEO ({len(converted)}篇)")
            converted = []
    if converted:
        data = load_processed()
        proc = set(data.get("obsidian_processed",[]))
        for c in converted: proc.add(c)
        data["obsidian_processed"] = list(proc)
        data["last_run"] = datetime.now().isoformat()
        save_processed(data)
        git_push(f"Auto: 补齐O→GEO ({len(converted)}篇)")
    log("="*50)
    log("补齐转化完成!")
    log("="*50)

if __name__ == "__main__":
    main()
