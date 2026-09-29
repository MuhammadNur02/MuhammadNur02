"""Produce data/contributions.json - a demo dataset shaped like the numbers
the user already had (total ~575, current streak 2, longest streak 20).
This file is what the GitHub Action overwrites with real data on schedule;
generators must only ever read from data/contributions.json, never hardcode
numbers, so the moment the workflow runs once, this sample is replaced.
"""
import json, os, random, datetime

random.seed(42)
WEEKS, DAYS = 53, 7
N = WEEKS * DAYS

levels = [0] * N

# 1) plant the longest streak: 20 consecutive active days, roughly mid-year
start = 150
for i in range(start, start + 20):
    levels[i] = random.choice([1, 1, 2, 2, 3])
# an inactive day right before and after, so it reads as exactly 20
levels[start - 1] = 0
levels[start + 20] = 0

# 2) current streak: exactly the last 2 days active, the day before them empty
levels[N - 1] = random.choice([1, 2])
levels[N - 2] = random.choice([1, 2])
levels[N - 3] = 0

# 3) scatter weekday-biased activity across the rest to build up the total
target_total_counts = 575  # sum of raw contribution counts, not levels
placed = {i for i in range(start - 1, start + 21)} | {N - 1, N - 2, N - 3}
free_idx = [i for i in range(N) if i not in placed]
random.shuffle(free_idx)

raw = [0] * N
level_to_raw = {0: 0, 1: 1, 2: 3, 3: 6, 4: 10}
running = sum(level_to_raw[levels[i]] for i in placed)

for i in free_idx:
    dow = i % DAYS  # 0=Sun ... 6=Sat (matches GitHub's grid orientation)
    weekday_bias = 0.55 if dow in (0, 6) else 1.0
    if running >= target_total_counts:
        break
    if random.random() < 0.62 * weekday_bias:
        c = random.choice([1, 2, 2, 3, 4, 6, 8])
        c = min(c, target_total_counts - running)
        if c <= 0:
            continue
        raw[i] = c
        running += c
        levels[i] = 1 if c <= 1 else 2 if c <= 3 else 3 if c <= 6 else 4

for i in placed:
    raw[i] = level_to_raw[levels[i]] if raw[i] == 0 else raw[i]

total = sum(raw) or sum(level_to_raw[l] for l in levels)

# recompute streaks from the final grid, in day order, to keep the file honest
cur = longest = run = 0
for i, lv in enumerate(levels):
    if lv > 0:
        run += 1
        longest = max(longest, run)
    else:
        run = 0
cur = 0
for lv in reversed(levels):
    if lv > 0:
        cur += 1
    else:
        break

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=N - 1)

data = {
    "weeks": WEEKS,
    "days_per_week": DAYS,
    "start_date": start_date.isoformat(),
    "end_date": end_date.isoformat(),
    "levels": levels,            # 0..4 intensity per cell, column-major (week then day)
    "raw_counts": raw,
    "total_contributions": total,
    "current_streak": cur,
    "longest_streak": longest,
}

out = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as f:
    json.dump(data, f, indent=2)
print("wrote", out, "| total", total, "| current_streak", cur, "| longest_streak", longest)
