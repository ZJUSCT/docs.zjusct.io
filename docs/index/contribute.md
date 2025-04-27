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

本文档使用 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 构建。Clone 本仓库后，你可使用下面的命令在本地启动文档服务：

```bash
pip install -r requirements.txt
mkdocs serve
```

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

    本文档已启用 [mkdocs-drawio](https://github.com/tuunit/mkdocs-drawio) 插件，能够渲染 `.drawio` 文件。

    ```markdown
    ![示例图片](path/to/image.drawio)
    ```

    我们推荐直接插入 `.drawio` 文件，以便后续修改。

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

## 📊 文档状态

下面是文档 Tag，用于标记文档的完成状态。

| Tag | 说明 |
| --- | --- |
| `完善` | 内容完整，符合写作规范 |
| `不完善` | 内容不完整或有误，不符合写作规范 |
| `废弃` | 即将移除 |

请考虑优先贡献被标记为 `不完善` 的文档。

<!-- material/tags -->
