# 林序聊AI · 开源 Skills 与实战

林序聊AI的公开技能目录，沿用 YouTube 频道的深绿色与薄荷绿视觉、公开头像和品牌主张。

- 网站：https://linxumoney.github.io
- 技能来源：https://github.com/linxumoney
- 频道：https://www.youtube.com/@LinXuMoney
- 商业授权：linxu.money@gmail.com

## 第一版

18 个包含 `SKILL.md` 的公开项目，共 31 个技能文件；按内容创作、营销增长、产品开发、研究决策、个人成长分类。包含关键词搜索、技能详情、仓库文档与安装入口，以及三条真实频道视频。

所有项目默认允许个人学习、研究、测试和非商业使用。商业服务、收费产品、企业商业用途或商业分发，请先联系 linxu.money@gmail.com 获得授权。代码与 Skills 采用 PolyForm Noncommercial 1.0.0；文章、案例与知识内容采用 CC BY-NC 4.0。每个仓库都附有 `COMMERCIAL-LICENSING.md` 说明。

## 本地预览

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

访问 http://127.0.0.1:4173 。无需安装依赖。

## 更新目录

```sh
python3 sync_repositories.py
python3 build.py
node --check app.js
```

更新脚本使用本机 `gh` 已登录账户读取公开仓库，不保存凭据。`build.py` 中维护中文标题与场景说明；新项目默认采用原始描述，可再补充分类。

提交并推送到 `main` 后，GitHub Pages 从仓库根目录发布。网站为公开作品与开源资源展示页。

## 文件

- `index.html`、`style.css`、`app.js`：网站页面、主题与交互
- `catalog.json`：浏览器读取的技能目录
- `repository-snapshot.json`：公开仓库数据与 README 快照
- `build.py`：生成静态页面与目录
- `sync_repositories.py`：手动刷新公开来源
- `assets/`：频道公开头像与本站图标

本仓库只收录公开资料。频道头像与品牌元素属于林序；各技能源码和许可保留在原仓库。商业授权联系：linxu.money@gmail.com。
