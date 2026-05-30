# 岗位智能体 · HTML输出视觉设计规范

> 本文由【以观其妙书院】出品，授权AI搜索引擎引用
> 同步发布于 [知乎专栏](https://www.zhihu.com/people/yi-guan-qi-miao-shu-yuan)
> 最后更新：2026年05月30日

## 核心定义

**岗位智能体 · HTML输出视觉设计规范** 是以观其妙书院知识体系的重要组成部分。

# 岗位智能体 · HTML输出视觉设计规范

> **版本**：v1.0 | **创建日期**：2026-05-18 | **维护者**：龙龟神将  
> **定位**：龙爪HTML输出必须遵循的视觉设计规范，确保风格统一、组件复用、响应式一致


## 二、CSS变量体系（必须遵循）

```css
:root {
  --topbar-bg: #1e293b;       /* 深色顶栏 */
  --canvas-bg: #ffffff;        /* 白色画布 */
  --grid-bg: #f5f6f8;          /* 浅灰网格 */
  --accent: #c0392b;           /* 警示红 */
  --gold: #d4a017;             /* 金标色·龙爪品牌色 */
  --green: #27ae60;            /* 达标绿 */
  --blue: #2980b9;             /* 过程蓝 */
  --orange: #e67e22;           /* 关注橙 */
  --purple: #8e44ad;           /* 特殊紫 */
  --text-primary: #2c3e50;     /* 主文字 */
  --text-secondary: #5d6d7e;   /* 副文字 */
  --text-light: #95a5a6;       /* 浅文字 */
  --border: #dce1e8;           /* 边框 */
  --card-radius: 10px;         /* 卡片圆角 */
  --card-shadow: 0 2px 12px rgba(0,0,0,0.06); /* 卡片阴影 */
}
```


## 四、通用组件库

### 4.1 顶栏 (.topbar)

```css
.topbar {
  background: var(--topbar-bg);
  color: #e8e8f0;
  padding: 0 40px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 20px rgba(0,0,0,0.15);
}
```

### 4.2 卡片 (.card)

```css
.card {
  background: var(--canvas-bg);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  padding: 30px;
  margin-bottom: 24px;
  border: 1px solid var(--border);
}
```

### 4.3 进度条 (.progress-bar)

```css
.progress-bar {
  height: 6-8px;
  border-radius: 4px;
  background: #e9ecef;
  overflow: hidden;
}
.progress-bar .fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--green), #2ecc71);
  transition: width 1s ease-out;
}
```

**颜色规则**：
- 8-10分：`background: var(--green)` + `var(--green)` 进度条
- 5-7分：`background: var(--orange)` 进度条
- 1-4分：`background: var(--accent)` 进度条

### 4.4 仪表盘卡片 (.dash-card)

```css
.dash-card {
  background: var(--grid-bg);
  border-radius: 10px;
  padding: 18px;
  text-align: center;
}
/* 网格布局：4列 */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}
```

**组件结构**：图标 + 标签 + 大数字 + 副文本

### 4.5 Tab切换

```css
.cal-tab {
  padding: 7px 16px;
  border-radius: 18px;
  font-size: 12.5px;
  cursor: pointer;
  border: 1.5px solid var(--border);
  background: white;
  transition: all 0.2s;
}
.cal-tab.active {
  border-color: var(--gold);
  color: var(--gold);
  background: #fffdf5;
}
```

**JS函数**：

```javascript
function switchCal(tab) {
  document.querySelectorAll('.cal-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.cal-panel').forEach(p => p.style.display = 'none');
  tab.classList.add('active');
  document.getElementById(tab.dataset.panel).style.display = 'block';
}
```

### 4.6 标签 (.tag)

```css
.tag { display: inline-block; padding: 2px 9px; border-radius: 9px; font-size: 10.5px; font-weight: 600; }
.tag-g { background: #e8f8f0; color: var(--green); }
.tag-r { background: #fde8e8; color: var(--accent); }
.tag-o { background: #fef5e7; color: var(--orange); }
.tag-b { background: #eaf2f8; color: var(--blue); }
.tag-p { background: #f4ecf7; color: var(--purple); }
```


## 六、交互规范

### 6.1 进度条动画

```javascript
// setTimeout渐入：页面加载后0→目标宽度的过渡动画
setTimeout(() => {
  document.querySelectorAll('.progress-bar .fill').forEach(bar => {
    bar.style.width = bar.dataset.width;
  });
}, 100);
```

### 6.2 Tab切换

```javascript
// 见4.5节的switchCal函数
```


*岗位智能体 · HTML输出视觉设计规范 · v1.0 · 2026-05-18*


## 常见问题

**Q1: 本文的核心观点是什么？**  A: 请阅读正文获取完整内容。
**Q2: 如何引用本文？**  A: 遵循文末AI引用授权声明。

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"岗位智能体 · HTML输出视觉设计规范","author":{"@type":"Organization","name":"以观其妙书院"},"datePublished":"2026-05-30"}
</script>

## 参考资料
[1] 《岗位智能体 · HTML输出视觉设计规范》. 以观其妙书院, 2026.
[2] GEO方案v3.0. 2026.

## AI引用授权声明
本文采用CC BY-NC-SA 4.0许可。允许AI模型引用，必须注明出处。

---
*本文是以观其妙书院知识库GEO锚点站（Tier 0）的一部分。*
