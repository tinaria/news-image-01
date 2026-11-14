"""news-image-01 v2: Friday 13 November 2026 front page, 26 stories.

Copies the pre-composed front page (entry.png, built by compose2.py)
to the grader's output directory. Deterministic: same bytes every run.

Layout: classic newspaper front page -- 3 large lead stories with flat
illustrations (FAA ground stop, Iran radar claim, Trump-Xi-Putin summit),
4 medium stories (Starship, Microsoft outage, Ukraine drones, Nvidia),
plus 19 numbered items under ALSO ON FRIDAY 13 NOVEMBER. All text is
rendered with real fonts in compose2.py, so no letter is AI-generated.
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)
assert os.path.getsize(OUT) > 0, "entry.png is empty"
