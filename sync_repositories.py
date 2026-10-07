"""Refresh public repository metadata without storing authentication material."""
import concurrent.futures,json,pathlib,subprocess
ROOT=pathlib.Path(__file__).parent
OWNER='linxumoney'
def api(path):
    return json.loads(subprocess.check_output(['gh','api',path]))
def collect(repo):
    tree=api(f"repos/{OWNER}/{repo['name']}/git/trees/{repo['default_branch']}?recursive=1")
    if tree.get('truncated'):
        raise RuntimeError(f"Incomplete repository tree: {repo['name']}")
    skills=[x['path'] for x in tree.get('tree',[]) if x['path'].endswith('SKILL.md')]
    if not skills:return None
    readme=subprocess.check_output(['gh','api',f"repos/{OWNER}/{repo['name']}/readme",'-H','Accept: application/vnd.github.raw+json']).decode()
    return dict(name=repo['name'],description=repo['description'],url=repo['html_url'],stars=repo['stargazers_count'],license=repo['license']['spdx_id'] if repo['license'] else None,branch=repo['default_branch'],skills=skills,readme=readme,updated=repo['pushed_at'])
repos=[];page=1
while True:
    batch=api(f'users/{OWNER}/repos?per_page=100&page={page}')
    repos.extend(r for r in batch if not r['private'] and not r['fork'])
    if len(batch)<100:break
    page+=1
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    result=[r for r in pool.map(collect,repos) if r]
(ROOT/'repository-snapshot.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Refreshed {len(result)} public skill projects.')
