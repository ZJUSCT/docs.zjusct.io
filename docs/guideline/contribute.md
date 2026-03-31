# 贡献

<style>
h1:before {content: unset;}
h2:before {content: unset;}
h3:before {content: unset;}
h4:before {content: unset;}
h5:before {content: unset;}
</style>

!!! abstract "我们欢迎任何人参与文档建设！"

    贡献方式包括但不限于：

    1. 发现文档中的错误并提出修正
    2. 补充现有文档的内容
    3. 撰写新的技术文档或教程
    4. 优化文档的组织结构和可读性

## 🚀 本地构建

本文档主体使用 [Zensical](https://zensical.org/) 构建，并保持对 Material 风格模板的兼容；首页仍然由 `zjusct-home` 中的 React 组件提供。Clone 本仓库后，你可使用下面的命令在本地启动文档服务：

```bash
uv sync
pnpm --dir zjusct-home install
pnpm --dir zjusct-home build
cp -R zjusct-home/dist/assets/* docs/assets/
uv run zensical serve
```

如果只修改文档正文、不关心首页预览，可跳过 `zjusct-home` 的构建步骤。

## ✍️ 写作规范

!!! tip "💡 我们鼓励个性化写作，以下规范仅为保证基础一致性"

✅ 推荐：

- 使用 Markdown 格式
- 使用 [EditorConfig](https://editorconfig.org/) 统一代码风格
- 使用 [Markdownlint](https://github.com/DavidAnson/markdownlint) 格式化文档
- 使用 [AutoCorrect](https://huacnlee.github.io/autocorrect/) 优化中英文混排
- 标注参考资料来源
- 清晰的 Git 提交信息
- 适当使用 emoji 增强可读性

❌ 避免：

- 直接粘贴未消化的外部内容
- 包含敏感配置信息
- 使用非通用缩写

### 🔧 Git 协作

- **团队成员**：直接提交到 `main` 分支，自行处理冲突（推荐使用 `rebase`）。
    - 如果需要提醒他人审阅，请使用 Pull Request。
    - 如果有值得讨论的话题/需要分配任务，可以使用 Issue 功能。
- **团队外人员**：通过 GitHub 提交 Pull Request。

### 📁 文件管理

- 所有附件（图片/代码等）存放在同名 `.assets` 文件夹中

    示例：`guide.md` 的附件放在 `guide.assets/`

### 🌐 语言风格

- 主要使用中文
- 专业术语格式：

    ```markdown
    图形处理器（Graphics Processing Unit，GPU）
    ```

### 🖼️ 图片规范

!!! tip "关于 draw.io 图片"

    当前站点按 `mkdocs-drawio` 等效逻辑直接渲染 `.drawio` 文件，因此可以直接引用 `.drawio` 源文件。

    ```markdown
    ![示例图片](path/to/image.drawio)
    ```

    多页图可直接用 alt 文本或 `page` 属性指定页面，例如：

    ```markdown
    ![Page-2](path/to/image.drawio)
    ![示例图片](path/to/image.drawio){ page="Page-2" }
    ```

为了减小普通图片体积，建议使用下面的命令转换为 WebP 格式：

```bash
for f in *.jpg *.jpeg *.png; do [ -f "$f" ] && cwebp "$f" -o "${f%.*}.webp" && rm "$f"; done
```

如果图片需要引用备注、说明信息或调整缩放等效果，请使用下面的 [HTML 格式](https://squidfunk.github.io/mkdocs-material/reference/images/#image-captions)：

```html
<figure markdown>
![示例图片](path/to/image.png){ width=80% }
<figcaption>
  图片说明<br>
  <small>[来源](https://example.com)</small>
</figcaption>
</figure>
```

## 📝 博客规范

博客目录现在就是普通的 Zensical 文档目录。要新增博客，请在 `docs/blog/<year>` 目录下创建新的 Markdown 文件，命名为 `<month>-<day>-<title>.md`，内容参考 `templates/blog-post.md`。

文章头部请直接使用简单 front matter：

```yaml
---
title: 博客标题
date: 2026-03-31
author: 你的名字
tags:
  - 分类
---
```

如果需要展示作者、日期、标签或外链，请直接写在正文开头的引用块中。

## 📊 文档状态

下面是文档 Tag，用于标记文档的完成状态。

| Tag | 说明 |
| --- | --- |
| `完善` | 内容完整，符合写作规范 |
| `不完善` | 内容不完整或有误，不符合写作规范 |
| `废弃` | 即将移除 |

请考虑优先贡献被标记为 `不完善` 的文档。

<!-- material/tags -->
