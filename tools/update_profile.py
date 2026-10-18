"""Generate a GitHub profile card from public GitHub data; standard library only."""
import json
import os
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

OWNER = 'frostmoon-rui'


def fetch(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': OWNER + '-profile',
               'X-GitHub-Api-Version': '2022-11-28'}
    token = os.getenv('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    request = urllib.request.Request('https://api.github.com' + path, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def collect(get=fetch):
    account = get('/users/' + OWNER)
    repositories = []
    for page in range(1, 101):
        batch = get(f'/users/{OWNER}/repos?type=owner&per_page=100&page={page}')
        repositories.extend(repo for repo in batch if not repo.get('private'))
        if len(batch) < 100:
            break
    else:
        raise RuntimeError('Repository pagination exceeded limit; keep existing card')
    originals = [repo for repo in repositories if not repo.get('fork')]
    return [('PUBLIC REPOS', len(repositories)), ('STARS EARNED', sum(repo.get('stargazers_count', 0) for repo in originals)),
            ('FOLLOWERS', account.get('followers', 0)), ('FORKS RECEIVED', sum(repo.get('forks_count', 0) for repo in originals))]


def render(metrics, date):
    blocks = []
    for index, (label, value) in enumerate(metrics):
        x = 112 + index * 224
        blocks.append(f'<text x="{x}" y="107" fill="#dcc9ff" font-size="36" font-weight="700">{int(value)}</text>'
                      f'<text x="{x}" y="137" fill="#aaa5c2" font-size="10" letter-spacing="1.5">{escape(label)}</text>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="900" height="190" viewBox="0 0 900 190" role="img" aria-labelledby="title desc">'
            '<title id="title">frostmoon-rui GitHub public activity</title>'
            '<desc id="desc">Public repositories, stars on owned non-fork repositories, followers and forks received. No private activity.</desc>'
            '<rect x="1" y="1" width="898" height="188" rx="18" fill="#1c2237" stroke="#45405f"/>'
            '<g font-family="Segoe UI,Arial,sans-serif">'
            '<text x="30" y="34" fill="#dcd4ee" font-size="12" letter-spacing="2">SMALL STEPS, REAL PROGRESS</text>'
            f'<text x="870" y="34" fill="#a59bbd" font-size="11" text-anchor="end">{escape(date)} UTC</text>'
            '<path d="M225 67v81m224-81v81m224-81v81" stroke="#3c3b57"/>'
            '<g text-anchor="middle">' + ''.join(blocks) + '</g>'
            '<text x="30" y="173" fill="#a59bbd" font-size="10">Public GitHub API · Daily refresh · No visitor tracking</text>'
            '</g></svg>\n')


def main():
    metrics = collect()
    content = render(metrics, datetime.now(timezone.utc).strftime('%Y-%m-%d'))
    target = Path(__file__).resolve().parents[1] / 'assets' / 'activity.svg'
    temporary = target.with_suffix('.svg.tmp')
    temporary.write_text(content, encoding='utf-8')
    temporary.replace(target)
    print('Updated public profile card:', dict(metrics))


if __name__ == '__main__':
    main()
