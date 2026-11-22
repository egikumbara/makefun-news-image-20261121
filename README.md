[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/egikumbara/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/egikumbara/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World Today — Saturday 21 November 2026

A one-page newspaper front page summing up the world news of
**Saturday 21 November 2026** as a single 1024×1024 PNG.

Six real stories reported that day:

1. **Russia hits Ukraine with 400+ drones and 110 missiles; two land in Poland** — at least eight killed in Kyiv; PM Tusk calls it a deliberate provocation.
2. **ICJ finds Myanmar guilty of genocide against the Rohingya** — landmark ruling from The Hague.
3. **AI sell-off pushes the S&P 500 into correction** — US stocks fell 3.7%.
4. **UK and EU sign biggest post-Brexit deals yet** — food trade, carbon markets, youth mobility.
5. **COP31 talks run past deadline over fossil fuels** — UN climate summit in Antalya in overtime.
6. **Magnitude 6.8 quake shakes Peru's Andes** — residents of Lima onto the streets.

## How it works

`main.py` is pure Python 3.13 standard library — no PIL, no network, no
clock, no randomness. It draws everything itself: a hand-rolled 5×7 bitmap
font, simple vector motifs for each story, and a hand-written PNG encoder
(`zlib` + `struct`), so two runs produce byte-identical output.

## How to run

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024x1024, under 1 MiB)
```

## Verify

```sh
python3 verify.py
# runs main.py twice into separate dirs, compares bytes, checks size and dimensions
```
