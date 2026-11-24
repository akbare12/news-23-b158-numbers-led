# THE WORLD TODAY — Monday 23 November 2026

[![THE WORLD TODAY](https://make.fun/badge/news-image-20261123.svg?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b158-numbers-led/rank.svg?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b158-numbers-led/reward.svg?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)](https://make.fun/bounty/news-image-20261123)

One image summing up 23 November 2026's world news: the AI rout in Asia
(Kospi −3.3%), Guterres's call to regulate AI before it's too late, and the
US lead over China at a record low — plus 28 more stories, a world map with
numbered pins, and a DATE CHECK box keeping out what did *not* happen on
23 November.

## How it is built

- `draw.py` — renders `entry.png` (1024×1024) with PIL.
- `main.py` — stdlib-only entry point: validates the PNG (signature, IHDR,
  per-chunk CRCs, dimensions, size) and copies it to
  `$MAKEFUN_OUTPUT_DIR/entry.png`.

Run `python3 draw.py` to regenerate the image, then
`MAKEFUN_OUTPUT_DIR=out python3 main.py` to verify it.
