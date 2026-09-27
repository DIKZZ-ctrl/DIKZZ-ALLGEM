#!/usr/bin/env python3
"""Add a floating "← เมนู" button (link to index.html) to every root-level .html
file that does not already link back to index.html. Idempotent."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
MARKER = "<!--auto-home-btn-->"
HAS_HOME_LINK = re.compile(r"""href\s*=\s*["']?(?:\./)?index\.html(?:[#?"'\s>])""", re.I)
BODY_END = re.compile(r"</body\s*>", re.I)

SNIPPET = MARKER + """
<a href="index.html" class="auto-home-btn" aria-label="กลับไปหน้าเมนู">&#8592; เมนู</a>
<style>
.auto-home-btn{position:fixed;left:calc(12px + env(safe-area-inset-left,0px));bottom:calc(12px + env(safe-area-inset-bottom,0px));z-index:2147483000;display:inline-flex;align-items:center;gap:4px;padding:8px 14px;border-radius:999px;background:#ffffff;color:#1f2937;border:1px solid rgba(0,0,0,.15);box-shadow:0 2px 8px rgba(0,0,0,.18);font:600 14px/1.2 system-ui,-apple-system,"Segoe UI",sans-serif;text-decoration:none;-webkit-tap-highlight-color:transparent}
.auto-home-btn:hover,.auto-home-btn:focus-visible{background:#f3f4f6;outline:none}
@media (prefers-color-scheme:dark){.auto-home-btn{background:#1f2937;color:#f3f4f6;border-color:rgba(255,255,255,.2)}.auto-home-btn:hover,.auto-home-btn:focus-visible{background:#374151}}
@media print{.auto-home-btn{display:none!important}}
</style>
"""


def process(path: pathlib.Path) -> bool:
    if path.name.lower() == "index.html":
        return False
    text = path.read_text(encoding="utf-8")
    if MARKER in text or HAS_HOME_LINK.search(text):
        return False
    matches = list(BODY_END.finditer(text))
    if matches:
        i = matches[-1].start()
        new = text[:i] + SNIPPET + text[i:]
    else:
        new = text.rstrip("\n") + "\n" + SNIPPET
    path.write_text(new, encoding="utf-8")
    return True


def main() -> int:
    changed = [p.name for p in sorted(ROOT.glob("*.html")) if process(p)]
    for name in changed:
        print(f"added home button: {name}")
    if not changed:
        print("no changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
