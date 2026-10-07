import json,pathlib,html,re
root=pathlib.Path(__file__).parent
repos=json.loads((root/'repository-snapshot.json').read_text())
meta={
'hotspot-radar':('热搜雷达','内容创作','雷达','抓取微博与百度热搜，结合关键词评分，找到值得写的选题。'),
'biz-fiction':('商业叙事写作','内容创作','故事','把真实商业人物与事件，组织成有场景、有细节的叙事长文。'),
'voice-preserving-editor':('保留你的声音','内容创作','润色','减少模板感和空话，保留原文事实、立场与作者的表达节奏。'),
'slide-story-architect':('演示叙事架构师','内容创作','演示','围绕观众和决策，整理故事线、逐页标题、证据与讲者过渡。'),
'cn-ads-skills':('中国广告投放技能库','营销增长','投放','覆盖用户洞察、广告文案、创意、转化路径和投放诊断的技能组合。'),
'google-ads-pilot':('Google Ads 副驾驶','营销增长','广告','辅助搜索词评估、否定词筛选、预算优化和账户诊断。'),
'ai-seo':('AI 搜索优化','营销增长','搜索','检查内容可引用性、爬虫访问和结构化数据，梳理 GEO 改进方向。'),
'growth-experiment-planner':('增长实验规划师','营销增长','实验','把增长想法拆成假设、指标、护栏、停止规则和实验复盘。'),
'product-brief-builder':('产品决策简报','产品开发','产品','梳理需求、MVP 范围与验收条件，让团队知道这次要决定什么。'),
'ui-critique-coach':('UI / UX 评审教练','产品开发','界面','从任务、信息层级、交互状态、响应式与可访问性检查界面。'),
'cloud-incident-coach':('云安全事件响应','产品开发','安全','保全证据、梳理时间线与影响范围，制定可逆遏制和恢复方案。'),
'fresh-signal-researcher':('近期趋势研究员','研究决策','趋势','校验最近 30 天的事件日期、独立来源、社区情绪与市场信号。'),
'earnings-signal-reviewer':('财报信号审阅','研究决策','财报','拆解盈利质量、现金流、业绩预期差和管理层指引。'),
'research-citation-auditor':('论文引用核验','研究决策','引用','核验文献真实性，检查论断与证据之间是否真正对应。'),
'wisdom-council':('智者议会','研究决策','议会','模拟七位思想家的思维视角，讨论商业选择与复杂问题。'),
'ai-navigator-2026':('AI 航海家大会知识库','研究决策','知识','检索大会嘉宾分享、逐字稿和问答，引用原始观点与方法。'),
'career-fit-coach':('岗位匹配教练','个人成长','职业','用 JD 和真实经历建立证据矩阵，判断岗位匹配与简历修改方向。'),
'dating-chat-coach':('自然聊天教练','个人成长','沟通','结合个人语言习惯和聊天上下文，整理自然、尊重的回复建议。')}
order=list(meta); selected=sorted([r for r in repos if r['skills']],key=lambda r:order.index(r['name']) if r['name'] in order else 99)
count=sum(len(r['skills']) for r in selected)
for r in selected:
 m=meta.get(r['name'],(r['name'],'其他','工具',r['description'] or '查看项目文档'))
 r.update(title=m[0],category=m[1],icon=m[2],summary=m[3])
 r['licenseLabel']='MIT' if r['license']=='MIT' else ('自定义许可' if r['license'] else '许可未标注')
 r['skillUrl']=r['url']+'/blob/'+r['branch']+'/'+r['skills'][0]
 # Only carry public catalog fields into the browser.
data=[{k:r[k] for k in ['name','title','category','icon','summary','url','stars','licenseLabel','skillUrl','skills']} for r in selected]
(root/'catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
def card(r,i):
 e=html.escape
 return f'''<article class="skill-card" data-category="{e(r['category'])}" data-search="{e(r['title']+' '+r['name']+' '+r['summary'])}"><div class="card-top"><span class="skill-icon">{e(r['icon'])}</span><span class="card-number">{i+1:02d}</span></div><span class="eyebrow">{e(r['category'])}</span><h3>{e(r['title'])}</h3><p>{e(r['summary'])}</p><div class="repo-name">{e(r['name'])}</div><div class="card-foot"><span>{e(r['licenseLabel'])} · {len(r['skills'])} Skill{'s' if len(r['skills'])>1 else ''}</span><button data-detail="{e(r['name'])}" aria-label="查看{e(r['title'])}详情">了解 / 使用 <span>↗</span></button></div></article>'''
filters=''.join(f'<button class="filter" data-filter="{x}" aria-pressed="false">{x}</button>' for x in ['内容创作','营销增长','产品开发','研究决策','个人成长'])
page='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#123d30"><title>林序聊AI · 开源 Skills 与实战</title><meta name="description" content="林序聊AI的公开AI技能库。探索内容创作、营销增长、产品开发、研究决策与个人成长的开源Skills，查看源码与使用文档。"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script src="app.js" defer></script></head><body>
<a class="skip" href="#skills">跳到技能库</a>
<header><a class="brand" href="#"><span class="brand-mark">LX<span>↗</span></span><span>林序聊AI<small>TECH · AI · BUSINESS</small></span></a><nav aria-label="主导航"><a href="#skills">开源 Skills</a><a href="#practice">实战与思考</a><a href="#start">开始使用</a></nav><a class="header-link" href="https://github.com/linxumoney" target="_blank" rel="noopener noreferrer">GitHub ↗</a></header>
<main><section class="hero"><div class="hero-main"><div class="hero-kicker"><span></span> LIN XU / OPEN SOURCE LAB</div><h1>用技术理解商业，<br>用 <em>AI</em> 放大杠杆<span class="period">。</span></h1><p>把实践中沉淀的工具和方法开放出来。<br>找到你的场景，带走一个能用的 AI Skill。</p><div class="hero-actions"><a class="primary" href="#skills">探索开源技能 <span>↓</span></a><a class="text-link" href="https://www.youtube.com/@LinXuMoney" target="_blank" rel="noopener noreferrer">看我的实战分享 ↗</a></div><div class="hero-stats"><span><strong>__PROJECTS__</strong>公开技能项目</span><span><strong>__SKILLS__</strong>SKILL.md 文件</span><span><strong>05</strong>应用场景</span></div></div><aside class="hero-aside"><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><div class="profile-card"><div class="profile-top"><span>BUILD IN PUBLIC</span><span>↗</span></div><img src="assets/avatar.jpg" alt="林序聊AI频道头像" width="160" height="160"><h2>林序 <small>Lin Xu</small></h2><p>前大厂技术专家<br>8年技术与商业实战 · All in AI</p><div class="profile-tags"><span>技术</span><b>×</b><span>商业</span><b>×</b><span>实战</span></div></div><div class="aside-note"><span>01 / 从想法到工具</span><p>让 AI 进入真实工作。</p><div class="growth-bars" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div></div></aside></section>
<div class="manifesto"><span>分享方法，也交付工具。</span><span>公开源码 / 场景驱动 / 持续打磨 <b>↗</b></span></div>
<section id="skills" class="catalog section"><div class="section-heading"><div><span class="eyebrow">THE TOOLKIT / 开源技能库</span><h2>选一个场景，开始动手。</h2></div><span class="section-count">__PROJECTS__ 个项目 <span>↙</span></span></div><div class="catalog-controls"><div class="filters" role="group" aria-label="按场景筛选"><button class="filter active" data-filter="全部" aria-pressed="true">全部</button>__FILTERS__</div><label class="search"><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="搜索技能、场景…" aria-label="搜索技能"></label></div><div id="result-count" class="result-count" aria-live="polite">全部 __PROJECTS__ 个技能项目</div><div class="card-grid">__CARDS__</div><div id="empty" hidden class="empty">没有找到匹配的技能。换个关键词，或<a href="#skills" id="reset-search">查看全部</a>。</div><p class="catalog-note">目录依据 GitHub 公开仓库整理 · 数据核对：2026.10.07 · 使用与分发条件以各仓库许可证为准。</p></section>
<section id="practice" class="practice section"><div class="section-heading"><div><span class="eyebrow">IN PRACTICE / 实战与思考</span><h2>工具之外，也聊它怎么用。</h2></div><a class="text-link" href="https://www.youtube.com/@LinXuMoney" target="_blank" rel="noopener noreferrer">前往 YouTube 频道 ↗</a></div><div class="video-grid">
<a class="video-card" href="https://www.youtube.com/watch?v=vWxoqGWcXZI" target="_blank" rel="noopener noreferrer"><div class="video-art"><span>AGENT / 工作流</span><strong>把自己<br>装进文件夹。</strong><span class="play">▶</span></div><h3>我如何用 Claude 把自己装进文件夹</h3><p>个人知识、方法与 Agent 工作流</p></a>
<a class="video-card" href="https://www.youtube.com/watch?v=hojynYkUbvI" target="_blank" rel="noopener noreferrer"><div class="video-art art-two"><span>RESEARCH / 实战</span><strong>做一个<br>自动化投研 Agent。</strong><span class="play">▶</span></div><h3>Web3 / 美股全自动化投研 Agent</h3><p>从研究任务到可运行的工作流</p></a>
<a class="video-card" href="https://www.youtube.com/watch?v=H3S7meujFfg" target="_blank" rel="noopener noreferrer"><div class="video-art art-three"><span>BUSINESS / 拆解</span><strong>看懂 AI 生意<br>的收款入口。</strong><span class="play">▶</span></div><h3>拆解卖课、订阅与企业服务</h3><p>AI 创作者的产品与商业路径</p></a></div></section>
<section id="start" class="start section"><div><span class="eyebrow">QUICK START / 开始使用</span><h2>把方法，交给你的 AI。</h2><p>Skill 把一个任务的方法、规则和参考资料<br>整理成 AI 工具可读取的文件。</p><a class="text-link" href="https://github.com/linxumoney" target="_blank" rel="noopener noreferrer">查看全部源码 ↗</a></div><ol><li><span>01</span><div><h3>选一个真实任务</h3><p>从写作、投放、研究或产品工作中，找到你现在需要解决的问题。</p></div></li><li><span>02</span><div><h3>按项目文档安装</h3><p>打开对应仓库的 README。不同项目的目录结构、依赖与适用工具会有区别。</p></div></li><li><span>03</span><div><h3>带着自己的材料试一次</h3><p>参考仓库示例发起任务，核对输出。把遇到的问题提交到项目 Issues。</p></div></li></ol></section>
</main><footer><div class="brand"><span class="brand-mark">LX<span>↗</span></span><span>林序聊AI<small>用技术理解商业，用 AI 放大杠杆。</small></span></div><div><a href="https://github.com/linxumoney">GitHub ↗</a><a href="https://www.youtube.com/@LinXuMoney">YouTube ↗</a><a href="https://x.com/linxumoney">X ↗</a></div><p>© 2026 林序聊AI · 保持好奇，持续动手。</p></footer>
<dialog id="detail"><button class="close" aria-label="关闭详情">×</button><div id="detail-content"></div></dialog></body></html>'''
page=page.replace('__PROJECTS__',str(len(selected))).replace('__SKILLS__',str(count)).replace('__FILTERS__',filters).replace('__CARDS__',''.join(card(r,i) for i,r in enumerate(selected)))
(root/'index.html').write_text(page)
print(f'Built {len(selected)} projects / {count} skills')
