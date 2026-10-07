'use strict';
const cards = [...document.querySelectorAll('.skill-card')];
const filters = [...document.querySelectorAll('.filter')];
const search = document.querySelector('#search');
let active = '全部';
function update() {
  const query = search.value.trim().toLocaleLowerCase();
  let count = 0;
  cards.forEach(card => {
    const match = (active === '全部' || card.dataset.category === active) && card.dataset.search.toLocaleLowerCase().includes(query);
    card.hidden = !match;
    if (match) count++;
  });
  document.querySelector('#result-count').textContent = `${active} · ${count} 个技能项目`;
  document.querySelector('#empty').hidden = count !== 0;
}
filters.forEach(button => button.addEventListener('click', () => {
  active = button.dataset.filter;
  filters.forEach(b => { b.classList.toggle('active', b === button); b.setAttribute('aria-pressed', String(b === button)); });
  update();
}));
search.addEventListener('input', update);
document.querySelector('#reset-search').addEventListener('click', event => {event.preventDefault();search.value = '';filters[0].click();search.focus();});
const dialog = document.querySelector('#detail');
const content = document.querySelector('#detail-content');
const catalog = fetch('catalog.json').then(r => {if (!r.ok) throw new Error('目录加载失败');return r.json();});
const escapeHtml = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
document.querySelectorAll('[data-detail]').forEach(button => button.addEventListener('click', async () => {
  content.textContent = '正在读取项目资料…';
  dialog.showModal();
  try {
    const project = (await catalog).find(p => p.name === button.dataset.detail);
    const e = escapeHtml;
    content.innerHTML = `<span class="eyebrow">${e(project.category)} / ${e(project.name)}</span><h2>${e(project.title)}</h2><p>${e(project.summary)}</p><div class="detail-links"><a href="${e(project.url)}#readme" target="_blank" rel="noopener noreferrer">查看文档与安装 ↗</a><a href="${e(project.skillUrl)}" target="_blank" rel="noopener noreferrer">读取 SKILL.md ↗</a><a href="${e(project.url)}/issues" target="_blank" rel="noopener noreferrer">反馈问题 ↗</a></div><p>${e(project.licenseLabel)} · ${project.skills.length} 个技能文件。兼容工具、依赖和安装步骤请按仓库 README 操作；使用与分发条件以仓库许可证为准。</p><h3>仓库里的 Skills</h3><ul class="detail-skills">${project.skills.map(path => `<li><a href="${e(project.url+'/blob/'+(project.skillUrl.split('/blob/')[1].split('/')[0])+'/'+path)}" target="_blank" rel="noopener noreferrer">${e(path)} ↗</a></li>`).join('')}</ul>`;
  } catch {
    content.replaceChildren();
    const p = document.createElement('p');p.textContent = '项目资料暂时未能加载。你可以直接在 GitHub 查看全部技能。';
    const link = document.createElement('a');link.href = 'https://github.com/linxumoney';link.textContent = '打开 GitHub ↗';content.append(p,link);
  }
}));
document.querySelector('.close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {if (event.target === dialog) {const r = dialog.getBoundingClientRect();if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();}});
