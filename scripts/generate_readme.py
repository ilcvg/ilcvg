# scripts/generate_readme.py


if not USERNAME:
raise SystemExit('GH_USERNAME (or GITHUB_ACTOR) environment variable is required')


if not TOKEN:
print('Warning: No token provided. You may hit rate limits for large requests.')
gh = Github()
else:
gh = Github(TOKEN)


user = gh.get_user(USERNAME)


# Fetch repos sorted by stars then recent push
repos = [r for r in user.get_repos() if not r.fork]
repos_sorted = sorted(repos, key=lambda r: (r.stargazers_count, r.pushed_at), reverse=True)


top_repos = []
for r in repos_sorted[:6]:
top_repos.append({
'name': r.name,
'html_url': r.html_url,
'description': r.description,
'stargazers_count': r.stargazers_count,
'pushed_at': r.pushed_at,
'lang': r.language or '—'
})


# Optional: fetch blog RSS
blog_posts = []
if BLOG_RSS and feedparser:
d = feedparser.parse(BLOG_RSS)
for e in d.entries[:5]:
blog_posts.append({
'title': e.get('title'),
'link': e.get('link'),
'published': e.get('published', e.get('updated', ''))
})


# Render template
env = Environment(
loader=FileSystemLoader('templates'),
autoescape=select_autoescape(['html', 'xml', 'j2', 'md'])
)
template = env.get_template('README.j2')


out = template.render(
name=user.name or user.login,
bio=(user.bio or '').strip() or '—',
location=LOCATION,
focus=FOCUS,
skills=SKILLS,
top_repos=top_repos,
blog_posts=blog_posts,
email=EMAIL,
linkedin=LINKEDIN,
twitter=TWITTER,
generated_at=datetime.utcnow().isoformat() + 'Z'
)


with open('README.md', 'w', encoding='utf8') as f:
f.write(out)


print('README.md generated successfully')
