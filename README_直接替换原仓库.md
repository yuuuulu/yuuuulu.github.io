# 直接修改你原来的 yuuuulu.github.io 仓库（不创建新仓库）

这份压缩包针对 **https://github.com/yuuuulu/yuuuulu.github.io** 的已有 `main` 分支。最终网址仍是 **https://yuuuulu.github.io/**。这套迁移项目使用 al-folio 的真实 Jekyll 主题（发布时下载官方 starter 和相关 Gems），并保留原 Rmd/Qmd 文件在 `_source_archive/`。不会删除之前的 Git commit 历史。

> **请注意**：这个 ZIP 只是可供你提交的代码与内容，我没有你的 GitHub 写入授权，没有直接修改云端 repo。GitHub Actions 首次构建尚未在你的仓库环境中验证，如果构建失败可以查看 Actions 日志并调整。正式更新只有你 `git push origin main` 后发生。

## 推荐操作：先把原网站完整备份到同一个仓库，再替换 `main`

准备好电脑上的 Git（macOS 可用 Terminal，Windows 可用 PowerShell）、Python 3，以及 PyYAML：

```bash
python -m pip install pyyaml
```

### 1. 下载并解压本 ZIP

假设解压后文件夹名叫 `Yu_Lu_al_folio_原仓库直接替换版`，里面直接有 `_config.yml`、`_pages`、`scripts` 和隐藏的 `.github` 文件夹。

**不要在 GitHub 网站上把 ZIP 当成单个文件上传。** 网页上上传 ZIP 并不会将它解压成站点文件。

### 2. 克隆【你的原仓库】

终端切换到你希望存放项目的目录，然后：

```bash
git clone https://github.com/yuuuulu/yuuuulu.github.io.git
```

它会生成 `yuuuulu.github.io` 文件夹；这个文件夹中已包含 `.git`，必须保留。

### 3. 运行脚本，先检查，再真正应用

**在同时包含这两个文件夹的目录**运行（下述路径用自己的实际文件夹路径替换）：

```bash
python "Yu_Lu_al_folio_原仓库直接替换版/scripts/apply_to_existing_repo.py" --repo "yuuuulu.github.io"
```

这条命令只检查，不改文件。确认没有报错后运行：

```bash
python "Yu_Lu_al_folio_原仓库直接替换版/scripts/apply_to_existing_repo.py" --repo "yuuuulu.github.io" --apply
```

`--apply` 会**先在原 GitHub 仓库推送**一个名为 `backup-before-al-folio-<旧提交ID>` 的备份分支；只有远程备份成功，才会替换电脑上 `main` 的旧站文件并把新文件 `git add` 到暂存区。它**不会自动向 main 提交或推送**。

如果你遇到 `permission denied` 或登录失败，先在 GitHub Desktop 登录或配置 Git 身份/认证；由于备份没成功，脚本不会继续删除原网站文件。

### 4. 核对并正式更新旧仓库

```bash
cd yuuuulu.github.io
git diff --cached --stat
```

确认变化符合预期后：

```bash
git commit -m "Migrate to al-folio and reorganize notes"
git push origin main
```

你的原仓库将出现新的 `_pages/`、`_bibliography/`、`assets/`、`.github/workflows/deploy.yml`、`scripts/`，且旧 R Markdown 文件保存在 `_source_archive/`。

### 5. 开通 GitHub Actions（只设置一次）

打开 **https://github.com/yuuuulu/yuuuulu.github.io** → **Settings** → **Actions** → **General** → **Workflow permissions** → **Read and write permissions** → Save。如果 Actions 被禁用，先启用。

再打开仓库的 **Actions** 标签页，找到 `Deploy Yu Lu al-folio`；如没有自动触发，选择 **Run workflow**。等它显示绿色成功，才继续下面的设置。

### 6. 切换 Pages 发布来源（关键）

在原仓库 **Settings** → **Pages** → **Build and deployment**：

- **Source:** Deploy from a branch
- **Branch:** `gh-pages`
- **Folder:** `/ (root)`

保存。不要再选择旧的 `main/docs`。页面最终访问：**https://yuuuulu.github.io/**。

### 7. 检查页面

首页 `/`；`/about-me/`；`/math/`（Lecture Notes）；`/reading/` 和 Philosophy 子页面；`/projects/`；`/resources/`；PDF；图片；LaTeX 公式；手机布局；原有 `philosophy/`、`statistics/`、`teaching.html`、`hello.html`、`resource.html` 等旧链接跳转。

## 不满意？怎么恢复旧网站？

因为创建了名为 `backup-before-al-folio-<旧提交ID>` 的分支，原仓库和全部 Git 历史都在。

最简单的回滚方式是在仓库 `main` 里对迁移的那个提交执行 `git revert <迁移提交ID>` 并推送（不要用 `git reset --hard` 加 `--force` 来覆盖历史）。如果迁移后没有其他提交，通常可以在 `main` 执行：

```bash
git revert HEAD
git push origin main
```

**回滚后还需要**在 Settings → Pages 把源从 `gh-pages/(root)` 改回之前的 `main/docs`（如果你旧站确实是从 `main/docs` 发布的），否则还会看到新主题的静态输出。

## 网站加载慢的问题

主页现在使用 WebP 压缩图片。Reading 首页是索引，具体正文拆成 Statistics History、Estimation、KL Divergence、Reading Books，另有 Philosophy 独立页面，因此不会打开目录就加载整篇长笔记。Math 与 Statistics 的独立笔记已从 `github.zip` 合并为站内页面。**主题不是自动加速器**，MathJax、网络和原始图片大小仍影响速度。

## 修改网站内容的位置

- `_pages/about.md` → 主页
- `_pages/about-me.md` → 完整个人介绍
- `_pages/notes/philosophy.md` → Reading 下的 Philosophy；`_pages/philosophy.md` 保留旧网址跳转
- `_pages/reading.md` → Reading 目录
- `_pages/notes/*.md` → 拆分后的原始阅读笔记
- `_pages/projects.md` → 项目链接
- `_pages/resources.md` → 资源页
- `_data/socials.yml` → 社交账号
- `assets/img/` → 显示用图片
- `_source_archive/` → 完整的原始 `.Rmd`、`.qmd` 与原图

内容核验：`python scripts/audit_content.py`。如果公式渲染不正确，先检查 GitHub Actions 中 Jekyll 和 MathJax 构建日志。更多文件对应关系请见 `MIGRATION_MANIFEST.json`。

注意：构建脚本会从 al-folio 的 `main` 分支获取最新版 starter，未来上游发生重大更新时可能影响构建。为长期稳定，可以以后再固定到已验证的 al-folio commit。
