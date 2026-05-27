# 影视 + 体育 热点榜单

多平台聚合的影视与体育话题榜单，每小时自动更新，适合运营参考。

## 数据来源

| 平台 | 内容类型 | 说明 |
|------|---------|------|
| 微博热搜 | 综合 | 过滤体育/影视关键词 |
| 抖音热搜 | 综合 | 过滤体育/影视关键词 |
| 百度热搜 | 综合 | 过滤体育/影视关键词 |
| 哔哩哔哩 | 综合 | 过滤体育/影视关键词 |
| 虎扑NBA | 体育 | NBA热帖直接接入 |
| 豆瓣电影 | 影视 | 热门电影榜单 |
| 豆瓣剧集 | 影视 | 热门剧集榜单 |

## 部署步骤

1. **Fork/新建仓库**
   - 在 GitHub 创建新仓库（如 `movie-sports-ranking`）
   - 设置为 **Public**

2. **上传文件**
   - 将本压缩包内所有文件上传到仓库根目录
   - 确保目录结构保持原样

3. **开启 GitHub Pages**
   - 进入仓库 Settings → Pages
   - Source 选择 **GitHub Actions**

4. **开启 Actions 权限**
   - Settings → Actions → General
   - Workflow permissions 选择 **Read and write permissions**
   - 勾选 **Allow GitHub Actions to create and approve pull requests**

5. **手动触发第一次更新**
   - 进入 Actions 标签页
   - 选择 "Update Movie & Sports Hot Topics"
   - 点击 **Run workflow**

6. **访问页面**
   - 等待 1-2 分钟
   - 访问 `https://你的用户名.github.io/movie-sports-ranking/`

## 更新频率

- 每小时整点自动更新（UTC时间）
- 支持手动触发更新
- 前端页面每分钟自动拉取最新数据

## 分类逻辑

- **体育**：包含 NBA、足球、网球、F1、奥运等关键词
- **影视**：包含 电影、剧集、综艺、豆瓣、票房等关键词
- **综合**：同时命中体育和影视关键词（如体育题材电影）

## 热度算法

- 同一话题在多个平台出现，热度累加
- 平台权重：微博 > 百度 > 抖音 > 哔哩哔哩 > 虎扑 > 豆瓣
- 综合榜按总热度排序
