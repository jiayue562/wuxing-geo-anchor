---
title: Wiki Schema
type: schema
created: 2026-05-15
updated: 2026-05-15
---

# Wiki Schema

## Directory Structure
```
wiki-knowledge/
├── raw/              # Immutable source documents
│   └── assets/       # Downloaded images
├── wiki/             # LLM-maintained markdown files
│   ├── index.md      # Content catalog
│   └── log.md        # Chronological operation log
└── WIKI-SCHEMA.md    # This file
```

## Page Format
```markdown
---
title: Page Title
type: entity | concept | source-summary | comparison | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [list of source filenames]
tags: [relevant tags]
---

# Page Title

Content with [[wiki-links]].

## See Also
- [[related-page]]
```

## Categories
- 学习方法论 (learning-methods)
- AI工具 (ai-tools)
- 认知科学 (cognitive-science)
- 五行人格 (five-elements)
- 教育心理学 (educational-psychology)

## Cross-reference Rules
- Always use [[wiki-links]] for concept references
- Every page must have at least 2 inbound links
- Update index.md on every ingest
- Use tags for discoverability
- Add "See Also" section at bottom of every page
