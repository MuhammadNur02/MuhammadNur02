"""Refresh data/*.json from the GitHub API (run by the update workflow).

Needs GITHUB_TOKEN (provided automatically in Actions). Any dataset that
cannot be fetched is left untouched, so the committed sample keeps working.
"""
import os, json, datetime, urllib.request

USER = os.environ.get("GH_USER", "MuhammadNur02")
TOKEN = os.environ["GITHUB_TOKEN"]
ROOT = os.path.join(os.path.dirname(__file__), "..", "data")
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
TZ_OFFSET = 7  # WIB


def api(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def gql(query):
    return api("https://api.github.com/graphql", {"query": query})["data"]["user"]


def save(name, data):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("updated", name)


def contributions():
    u = gql('{ user(login:"%s") { contributionsCollection { contributionCalendar { totalContributions '
            'weeks { contributionDays { date contributionCount contributionLevel } } } } } }' % USER)
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    levels = [LEVEL[d["contributionLevel"]] for d in days]
    run = longest = 0
    for lv in levels:
        run = run + 1 if lv else 0
        longest = max(longest, run)
    cur = 0
    for i, lv in enumerate(reversed(levels)):
        if lv:
            cur += 1
        elif i > 0:  # today may still be empty; don't break the streak yet
            break
    save("contributions.json", {
        "weeks": len(cal["weeks"]), "days_per_week": 7,
        "start_date": days[0]["date"], "end_date": days[-1]["date"],
        "levels": levels, "raw_counts": [d["contributionCount"] for d in days],
        "total_contributions": cal["totalContributions"],
        "current_streak": cur, "longest_streak": longest,
    })


def languages():
    u = gql('{ user(login:"%s") { repositories(first:100, ownerAffiliations:OWNER, isFork:false) { nodes '
            '{ languages(first:10, orderBy:{field:SIZE, direction:DESC}) { edges { size node { name } } } } } } }' % USER)
    tot = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            tot[e["node"]["name"]] = tot.get(e["node"]["name"], 0) + e["size"]
    if not tot:
        return
    total = sum(tot.values())
    top = sorted(tot.items(), key=lambda kv: -kv[1])[:5]
    rest = total - sum(v for _, v in top)
    out = [{"name": k, "pct": round(v * 100 / total, 1)} for k, v in top]
    out.append({"name": "Lainnya", "pct": round(rest * 100 / total, 1)})
    save("languages.json", {"languages": out})


def activity():
    events = []
    for page in (1, 2, 3):
        events += api(f"https://api.github.com/users/{USER}/events/public?per_page=100&page={page}")
    path = os.path.join(ROOT, "activity_matrix.json")
    m = json.load(open(path, encoding="utf-8"))
    grid = [[0] * 6 for _ in range(7)]
    n = 0
    for ev in events:
        if ev["type"] != "PushEvent":
            continue
        t = datetime.datetime.fromisoformat(ev["created_at"].replace("Z", "+00:00")) + datetime.timedelta(hours=TZ_OFFSET)
        dow = (t.weekday() + 1) % 7                       # 0 = Minggu
        part = t.hour // 4                                # Dini, Subuh, Pagi, Siang, Sore, Malam
        grid[dow][part] += len(ev["payload"].get("commits", [])) or 1
        n += 1
    if n < 10:  # too little data to be meaningful - keep the existing matrix
        return
    peak = max(max(r) for r in grid) or 1
    m["grid"] = [[0 if v == 0 else max(1, round(v * 4 / peak)) for v in r] for r in grid]
    save("activity_matrix.json", m)


for step in (contributions, languages, activity):
    try:
        step()
    except Exception as exc:  # keep going; stale data beats a failed run
        print(f"{step.__name__} skipped: {exc}")
