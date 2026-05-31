#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 unified 文件同步到 .workbuddy/skills/ 下对应的 X行人分智能体/SKILL.md
"""

import shutil
from pathlib import Path

# 配置
UNIFIED_DIR = Path("C:/Users/jia'yue/WorkBuddy/Claw/geo-repo/docs/articles")
SKILLS_DIR = Path("C:/Users/jia'yue/.workbuddy/skills")

# 五行映射
MAPPING = {
    "unified-木行人分智能体-v4.0.md": ("木行人分智能体", "木"),
    "unified-火行人分智能体-v4.0.md": ("火行人分智能体", "火"),
    "unified-土行人分智能体-v4.0.md": ("土行人分智能体", "土"),
    "unified-金行人分智能体-v4.0.md": ("金行人分智能体", "金"),
    "unified-水行人分智能体-v4.0.md": ("水行人分智能体", "水"),
}

# 标准 frontmatter 模板
def make_frontmatter(wuxing, wuxing_name):
    traits = {
        "木": ("阳木仁德·阴木愤怒", "生发", "直", "仁德", "愤怒"),
        "火": ("阳火礼明·阴火焦躁", "炎上", "热", "礼明", "焦躁"),
        "土": ("阳土信实·阴土怨妒", "承载", "厚", "信实", "怨妒"),
        "金": ("阳金义气·阴金挑剔", "肃杀", "刚", "义气", "挑剔"),
        "水": ("阳水智慧·阴水恐惧", "润下", "柔", "智慧", "恐惧"),
    }
    yang_yin, root, trait, yang, yin = traits[wuxing]
    return f'''---
title: "{wuxing_name} SKILL.md - 一心三界五行九层·全息发展模型 v4.0"
description: "{wuxing_name}是五行人格心理学OS的L4分智能体之一，专精于{wuxing_name}（{yang_yin}）的分析、诊断与转化。采用一心三界五行九层象思维体系，实现全息诊断与转化。"
version: "4.0"
created: "2026-05-31"
tags: [{wuxing_name}, 五行人格, 一心三界五行九层, 象思维, {yang}, {yin}, 拔阴取阳, 化克为生, B=MAP]
alwaysApply: true
agent_created: true
---

'''

for unified_name, (skill_dir, wuxing) in MAPPING.items():
    unified_path = UNIFIED_DIR / unified_name
    skill_path = SKILLS_DIR / skill_dir / "SKILL.md"
    
    if not unified_path.exists():
        print(f"❌ 未找到: {unified_path}")
        continue
    
    # 读取 unified 内容
    with open(unified_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 组合 frontmatter + 内容
    frontmatter = make_frontmatter(wuxing, skill_dir)
    full_content = frontmatter + content
    
    # 备份旧文件
    backup_path = skill_path.with_suffix('.md.v3-backup')
    if skill_path.exists():
        shutil.copy2(skill_path, backup_path)
        print(f"[BACKUP] {skill_path.name} -> {backup_path.name}")
    
    # 写入新文件
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"[OK] {skill_dir}/SKILL.md ({len(full_content)} bytes)")

print("\n[DONE] All skills updated!")
