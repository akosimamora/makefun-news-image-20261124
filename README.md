# The World in One Day — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/akosimamora/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/akosimamora/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-page newspaper front page that sums up Tuesday 24 November 2026 in a
single image: 33 stories across 7 regions, every one dated that Tuesday.

- **3 heroes, each a data diagram** — the Houthi strike on Riyadh's PIF Tower
  as a timeline (second strike in under a week, 11 injured); the Russian
  attack on Zaporizhzhia as a casualty chart (2 killed, 48 wounded); 14
  countries recognising the ICJ Rohingya genocide ruling as a map.
- **10 tiles, each with a big key number** — verified facts with named sources.
- **Verification on every story** — CONFIRMED (2+ major outlets), OFFICIAL
  (on the record), REPORTED (one major outlet), with a HOW WE CHECKED legend
  and an honest corrections line in the footer.
- **The Day in UTC** — a timeline strip; a KPI strip where every box is a
  number plus a full fact sentence; a world map with real land polygons and
  region-coloured numbered pins; a DATE CHECK box that lists what was left
  out (other days) and what had not happened yet.

Every fact was verified against named outlets (Reuters, WSJ, Bloomberg, AP
and others) before building — see `VERIFIED_NEWS.md` for the source list.

## Run

```sh
python3 build/draw.py   # renders entry.png (1024x1024, deterministic)
python3 main.py         # copies entry.png to /output/entry.png
```

No network, no randomness: rendering twice produces identical bytes.
