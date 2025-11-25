
import json, random, statistics
from datetime import datetime
from collections import Counter

with open('history_full.json','r',encoding='utf-8') as f:
    HISTORY_FULL = json.load(f)

def hot_cold(history):
    freq = Counter(n for row in history for n in row[:6])
    hot = [n for n,_ in freq.most_common(10)]
    cold = [n for n,_ in freq.most_common()[-10:]]
    return hot, cold

def booster(history):
    weights = Counter()
    for row in history:
        for n in row[:6]:
            weights[n] += 1
    total = sum(weights.values())
    return {n: w/total for n,w in weights.items()}

def monte_carlo(history, rounds=5000):
    scores = Counter()
    for _ in range(rounds):
        sample = random.choice(history)
        for n in sample[:6]:
            scores[n] += 1
    return scores

def generate_forecast():
    hot, cold = hot_cold(HISTORY_FULL)
    boost = booster(HISTORY_FULL)
    mc = monte_carlo(HISTORY_FULL)

    score = Counter()
    for n in range(1,38):
        score[n] += boost.get(n,0) * 2
        score[n] += mc.get(n,0)
        if n in hot: score[n] += 5
        if n in cold: score[n] -= 2

    main = [n for n,_ in score.most_common(6)]
    extra = random.choice([row[6] for row in HISTORY_FULL])
    return {
        "main": sorted(main),
        "extra": extra,
        "timestamp": datetime.now().isoformat()
    }
