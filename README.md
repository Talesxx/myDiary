## 我的个人笔记（VitePress）

这是我的个人笔记仓库，使用 VitePress 搭建，支持数学公式（MathJax）与 GitHub Pages 自动部署。

### 在线预览

- 生产站点（GitHub Pages）：`https://<你的 GitHub 用户名>.github.io/myDiary/`
- 本地预览：见下方命令

### 技术栈

- VitePress: 2.0.0-alpha.12
- 数学公式: `markdown-it-mathjax3`
- 部署: GitHub Actions 自动发布到 `gh-pages` 分支

### 脚本命令

仓库已在 `package.json` 中提供以下命令：

```bash
# 本地开发（热更新）
pnpm docs:dev

# 生产构建（已设置 base 为 /myDiary/）
pnpm docs:build

# 本地预览已构建产物
pnpm docs:preview
```

如果未安装 pnpm，也可以使用 npm：

```bash
npm install
npm run docs:dev
npm run docs:build
npm run docs:preview
```

环境要求：Node.js 22.x（见工作流），pnpm 10.15 或 npm。

### 开发与目录结构

主要内容位于 `docs/`，站点配置在 `docs/.vitepress/config.mts`。

```text
docs/
  .vitepress/
    config.mts        # 站点与主题配置（已开启数学公式）
    dist/             # 构建输出目录（自动生成）
  AdvancedMathematics/  # 高等数学笔记与图片
  web/               # Web 前端相关笔记
  index.md           # 首页
  api-examples.md    # 示例文档
```

数学公式已在配置中启用：

```ts
// docs/.vitepress/config.mts
export default defineConfig({
  markdown: { math: true },
  // ...
})
```

### 部署（GitHub Pages）

仓库已配置工作流 `.github/workflows/static.yml`：

- 触发条件：推送到 `master` 分支
- 构建命令：`npm run docs:build`
- 发布目录：`docs/.vitepress/dist`
- 目标分支：`gh-pages`

首次启用 Pages：

1) 在 GitHub 仓库 Settings → Pages：
   - Source 选择 `Deploy from a branch`
   - Branch 选择 `gh-pages` 和 `/ (root)`
2) 仓库可见性设为 Public 或配置好私有仓库的访问策略

站点的 `base` 已在 `package.json` 的构建脚本里指定为 `/myDiary/`：

```json
"docs:build": "vitepress build docs --base /myDiary/"
```

如果你的仓库名或发布路径不同，请同步修改上面的 `base` 为你的实际路径（例如 `/repo-name/`）。

### 常见问题

- 访问 404：通常是 `base` 未与 GitHub Pages 的发布路径一致。确保 `--base` 与最终访问路径前缀一致。
- 图片或静态资源路径：站内相对路径推荐以根为起点（例如 `/AdvancedMathematics/image/...`），或使用相对路径并在本地验证。
- Node 版本：工作流使用 Node 22.x，本地建议保持一致。

### 许可证

本项目使用 ISC 协议。


