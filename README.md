# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Kabantuhi/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Kabantuhi/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image that sums up the world's news of Monday 23 November 2026: the COP31 climate talks collapse with no deal, two Russian ships hit by drones in two seas, a deadly drone strike near Kyiv, the capture of cartel boss "El Chapo Isidro" in Mexico, a factory fire in Indonesia, the Democrats' biggest US House win since 1992, and the UN's "killer robots" talks. Drawn as a newspaper front page — "The World Today" — by a small Python program using only the Pillow library and the DejaVu fonts.

## Run it

```sh
python3 render.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`render.py` reads `news.json` and draws `entry.png` (1024×1024, under 1 MiB). `main.py` validates that image and copies it to the output directory. Both runs write the same bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=c45jj78w&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
