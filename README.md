# Yu Lu al-folio 网站

这是 `yuuuulu.github.io` 的本地源文件。原首页和阅读笔记已迁移；`github.zip` 中的 Math-s-interesting-things 与 stat.pre 笔记也已合并为站内页面。站点更新推送到 `main` 后，由 GitHub Actions 构建并发布到 `gh-pages`。

## 内容位置

- `_pages/math.md`、`_pages/math/`：Lecture Notes 目录与数学笔记。统计理论笔记也从这里进入；ODE 课程笔记和代码笔记位于同一页。
- `_pages/projects.md`：研究与课程项目、报告，以及不在压缩包中的外部项目。
- `_pages/reading.md`、`_pages/notes/math-stat-philosophy.md`：阅读笔记与数学统计哲思；旧 `/philosophy/` 地址会跳转到阅读页下。
- `_pages/statistics/`：stat.pre 导入的内容页。旧 `/statistics/` 地址会跳转到 Projects。
- `assets/pdf/imported/`：从压缩包导入的报告。课堂截图不在网页中展示。
- `_source_archive/github_zip/`：原始 `.qmd`、notebook 和数据文件，供以后重新整理；它们不直接发布。
- `scripts/import_github_zip.py`：保存原始文件及报告。`scripts/restore_full_notes.py` 和 `scripts/restore_reading.py` 可从本地存档重建保留全文、以文字替代课堂图片的页面。

`APH203.qmd` 中仅 AIC、AICc、BIC 内容进入 Prob. and Stat. 末尾；Time Series 页面没有迁入。Survey Sampling Final Report 不再展示。压缩包以外的项目仍使用原链接。

## 本地预览

用 VS Code 打开这个文件夹。站点使用官方 al-folio v1 starter；`scripts/assemble.py` 将本站内容覆盖到 starter 上，然后使用 Jekyll 构建。当前预览可从本地构建目录 `_site_build/_site` 提供服务。`_site_build/` 已被 Git 忽略。

原站迁移及将来部署的说明见 [README_直接替换原仓库.md](README_直接替换原仓库.md)。发布前可先在本地预览；正式发布时提交源码并推送到 `main`，随后检查 GitHub Actions 和 Pages 设置。
