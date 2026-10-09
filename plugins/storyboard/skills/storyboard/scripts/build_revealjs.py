#!/usr/bin/env python3
"""
Emit a Reveal.js HTML presentation from a frozen boards.md.

Each deliverable frame becomes one <section>. On-screen text from the
frame's Text cell is the slide body; the VO / Dialogue cell becomes the
speaker notes. Brand colours come from a brand-guardrails.md when supplied.

Dry run (default): prints a slide summary to stdout; nothing is written.
Pass --out to write the HTML file.

Usage:
    python3 build_revealjs.py ~/work/acme/boards.md
    python3 build_revealjs.py ~/work/acme/boards.md --out deck.html
    python3 build_revealjs.py ~/work/acme/boards.md \\
        --brand reference/brand-guardrails.md --out deck.html
    python3 build_revealjs.py ~/work/acme/boards.md \\
        --transition fade --theme dark --out deck.html
    python3 build_revealjs.py ~/work/acme/boards.md \\
        --allow-unapproved --out deck.html
"""
from __future__ import annotations

import argparse
import html as _html
import re
import sys
from pathlib import Path

# Import the shared parser so every adapter feeds from one frozen source.
_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))
from boards import load_boards, Boards, Frame, BoardsError  # noqa: E402


# ---------------------------------------------------------------------------
# Brand extraction
# ---------------------------------------------------------------------------

def _extract_brand(path: str) -> dict[str, str]:
    """
    Pull hex values by role from a brand-guardrails.md.

    Looks for table rows like:
        | **Background** | `#000000` | ... |
        | **Primary accent** | `#FF282D` | ... |

    Returns a dict keyed by lowercase role strings, plus shorthand aliases
    ("bg", "accent", "secondary") for the slots the template uses.
    """
    text = Path(path).read_text(encoding="utf-8")
    roles: dict[str, str] = {}
    row_re = re.compile(
        r"\|[^|]*\*\*([^*]+)\*\*[^|]*\|\s*`(#[0-9A-Fa-f]{3,8})`", re.IGNORECASE
    )
    for m in row_re.finditer(text):
        key = m.group(1).strip().lower()
        val = m.group(2).strip()
        roles[key] = val
        if "background" in key:
            roles["bg"] = val
        if "primary accent" in key or "fastly red" in key:
            roles["accent"] = val
        if "secondary accent" in key or "fastly blue" in key:
            roles["secondary"] = val
        if "primary text" in key:
            roles["text"] = val
    return roles


_DEFAULTS: dict[str, str] = {
    "bg":        "#000000",
    "accent":    "#FF282D",
    "secondary": "#0073EB",
    "text":      "#FFFFFF",
    "muted":     "#666666",
}


def _palette(brand_path: str | None) -> dict[str, str]:
    pal = dict(_DEFAULTS)
    if brand_path:
        pal.update(_extract_brand(brand_path))
    return pal


# ---------------------------------------------------------------------------
# Reveal.js transition mapping
# ---------------------------------------------------------------------------

_TRANS_MAP: dict[str, str] = {
    "DISSOLVE":   "fade",
    "FADE TO":    "fade",
    "FADE FROM":  "fade",
    "FADE IN":    "fade",
    "FADE OUT":   "fade",
    "CUT":        "none",
    "MATCH CUT":  "none",
    "WIPE":       "slide",
    "BUILD":      "convex",
    "WHIP":       "zoom",
    "HOLD":       "none",
}

_SHOT_TITLE = {"TITLE"}


def _reveal_transition(frame: Frame, default: str) -> str:
    """Map a card's Trans out vocabulary to a Reveal.js transition name."""
    t = frame.transition_out_type.upper().strip()
    for key, val in _TRANS_MAP.items():
        if t.startswith(key):
            return val
    return default


# ---------------------------------------------------------------------------
# Slide classification
# ---------------------------------------------------------------------------

def _is_section_break(frame: Frame) -> bool:
    """
    A section-break: a TITLE-shot frame, or text with ≤ 8 words and no
    structural markers (bullets, colons, line breaks).
    """
    if frame.shot.strip().upper() in _SHOT_TITLE:
        return True
    content = (frame.screen_text or frame.visual).strip()
    if not content:
        return False
    if any(c in content for c in ("•", "*", "–", ":", "\n")):
        return False
    return len(content.split()) <= 8


def _slide_class(frame: Frame) -> str:
    if frame.shot.strip().upper() in _SHOT_TITLE:
        return "title-slide"
    if _is_section_break(frame):
        return "section-slide"
    return "content-slide"


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

def _esc(text: str) -> str:
    return _html.escape(str(text))


def _render_text_block(text: str) -> str:
    """
    Convert multi-line Text cell content into HTML.

    Lines starting with - • * or a number-dot become <li>; everything
    else becomes <p>. Empty lines close an open list.
    """
    if not text.strip():
        return ""
    lines = [ln.rstrip() for ln in text.splitlines()]
    bullet_re = re.compile(r"^[-•*]\s+|^\d+[.)]\s+")
    in_list = False
    parts: list[str] = []
    for line in lines:
        if not line:
            if in_list:
                parts.append("</ul>")
                in_list = False
            continue
        if bullet_re.match(line):
            if not in_list:
                parts.append("<ul>")
                in_list = True
            item = bullet_re.sub("", line)
            parts.append(f"  <li>{_esc(item)}</li>")
        else:
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<p>{_esc(line)}</p>")
    if in_list:
        parts.append("</ul>")
    return "\n".join(parts)


def _render_slide(frame: Frame, default_transition: str) -> str:
    """Emit one <section> for a frame card."""
    slide_cls = _slide_class(frame)
    trans     = _reveal_transition(frame, default_transition)

    beat_html = ""
    if frame.beat.strip():
        beat_html = f'<div class="beat-label">{_esc(frame.beat.strip())}</div>\n    '

    content     = frame.screen_text or ""
    visual_desc = frame.visual.strip()
    notes_text  = frame.vo.strip() if frame.has_line else ""

    if slide_cls in ("title-slide", "section-slide"):
        main_text = content or visual_desc
        body = f"<h2>{_esc(main_text)}</h2>"
    else:
        body = _render_text_block(content)
        if not body and visual_desc:
            body = f'<p class="visual-desc">{_esc(visual_desc)}</p>'

    notes_html = ""
    if notes_text:
        notes_html = f'\n  <aside class="notes">{_esc(notes_text)}</aside>'

    return (
        f'<section class="{slide_cls}" data-transition="{trans}">\n'
        f'  <div class="slide-inner">\n'
        f'    {beat_html}{body}\n'
        f'  </div>'
        f'{notes_html}\n'
        f'</section>'
    )


_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600&family=Inter+Tight:wght@300;400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg:        {bg};
      --accent:    {accent};
      --secondary: {secondary};
      --fg:        {text};
      --muted:     {muted};
    }}
    html, body {{ background: var(--bg); margin: 0; padding: 0; }}
    .reveal {{
      font-family: 'Inter Tight', 'Inter', sans-serif;
      background: var(--bg);
      color: var(--fg);
      font-size: 22px;
    }}
    .reveal .slides {{ text-align: left; }}
    .reveal .slides > section {{ padding: 0; overflow: hidden; }}
    .reveal .progress {{ color: var(--accent); }}
    .reveal .controls {{ color: var(--accent); }}
    .reveal .slide-number {{ font-size: 12px; color: var(--muted); }}
    .reveal h2 {{
      font-family: 'Inter', sans-serif; font-weight: 300;
      font-size: 2.8em; color: var(--fg);
      line-height: 1.1; margin: 0 0 0.4em; letter-spacing: -0.02em;
    }}
    .reveal p {{
      font-size: 0.88em; color: #ddd; line-height: 1.7; margin: 0 0 0.5em;
    }}
    .reveal ul {{ margin: 0.4em 0 0.4em 1.3em; padding: 0; }}
    .reveal ul li {{
      font-size: 0.85em; line-height: 1.65; color: #ddd; margin-bottom: 0.3em;
    }}
    .reveal ul li::marker {{ color: var(--accent); }}
    .reveal strong {{ color: var(--fg); }}
    .slide-inner {{
      height: 100%; padding: 44px 56px 56px;
      box-sizing: border-box;
      display: flex; flex-direction: column;
      overflow: hidden; position: relative;
    }}
    .section-slide .slide-inner,
    .title-slide   .slide-inner {{ justify-content: center; }}
    .title-slide h2 {{ font-size: 3.6em; font-weight: 200; }}
    .beat-label {{
      font-size: 0.58em; font-weight: 700; text-transform: uppercase;
      letter-spacing: 0.12em; color: #fff;
      background: var(--accent); display: inline-block;
      padding: 3px 10px; border-radius: 3px; margin-bottom: 14px;
    }}
    .visual-desc {{ font-style: italic; color: var(--muted); font-size: 0.85em; }}
    .reveal .slides section::after {{
      content: "{footer}";
      position: absolute; bottom: 10px; left: 56px;
      font-size: 12px; color: #333; font-family: 'Inter', sans-serif;
    }}
  </style>
</head>
<body>
<div class="reveal">
<div class="slides">

{slides}

</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<script>
Reveal.initialize({{
  hash:                true,
  slideNumber:         true,
  transition:          '{default_transition}',
  transitionSpeed:     'fast',
  backgroundTransition:'fade',
  controls:            true,
  progress:            true,
  center:              false,
  width:               1456,
  height:              816,
  margin:              0,
}});
</script>
</body>
</html>
"""


def build_html(boards: Boards, transition: str, brand_path: str | None, theme: str) -> str:
    pal = _palette(brand_path)
    if theme == "light":
        pal = {**pal, "bg": "#FFFFFF", "text": "#000000", "muted": "#555555"}

    title  = boards.meta.get("title", "Presentation")
    footer = boards.meta.get("footer", "")

    slides = "\n\n".join(
        _render_slide(f, transition)
        for f in boards.deliverable_frames()
    )

    return _HTML_TEMPLATE.format(
        title=_esc(title),
        footer=_esc(footer),
        default_transition=transition,
        slides=slides,
        bg=pal["bg"],
        accent=pal["accent"],
        secondary=pal["secondary"],
        text=pal["text"],
        muted=pal["muted"],
    )


# ---------------------------------------------------------------------------
# Dry-run summary
# ---------------------------------------------------------------------------

def _dry_run_summary(boards: Boards, transition: str, brand_path: str | None) -> None:
    pal    = _palette(brand_path)
    frames = boards.deliverable_frames()
    title  = boards.meta.get("title", "(untitled)")
    print(f"Dry run — {len(frames)} slides from: {boards.source}")
    print(f"Title:      {title}")
    print(f"Transition: {transition}")
    print(f"Palette:    bg={pal['bg']}  accent={pal['accent']}  secondary={pal['secondary']}")
    print()
    print(f"{'#':<4}  {'Class':<14}  {'Trans':<7}  {'Beat':<14}  Text preview")
    print("-" * 76)
    for f in frames:
        cls   = _slide_class(f)
        trans = _reveal_transition(f, transition)
        text  = (f.screen_text or f.visual)[:42].replace("\n", " ")
        beat  = (f.beat or "")[:13]
        print(f"{f.number:<4}  {cls:<14}  {trans:<7}  {beat:<14}  {text}")
    print()
    print("Pass --out <path> to write the HTML file.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Emit a Reveal.js HTML deck from a frozen boards.md.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("boards", help="Path to the production's boards.md")
    p.add_argument(
        "--out", metavar="PATH",
        help="Write HTML to this file (default: dry run, prints summary)",
    )
    p.add_argument(
        "--brand", metavar="PATH",
        help="brand-guardrails.md to extract the palette from (optional)",
    )
    p.add_argument(
        "--transition", default="fade",
        choices=["fade", "slide", "convex", "concave", "zoom", "none"],
        help="Default Reveal.js transition (default: fade)",
    )
    p.add_argument(
        "--theme", default="dark", choices=["dark", "light"],
        help="Background theme (default: dark)",
    )
    p.add_argument(
        "--allow-unapproved", action="store_true",
        help="Skip the frozen-boards guard (use with care)",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        boards = load_boards(args.boards)
    except (OSError, BoardsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not boards.is_frozen and not args.allow_unapproved:
        print(
            f"error: boards status is {boards.status!r}, expected 'approved' or "
            "'animatic-locked'.\n       Pass --allow-unapproved to override.",
            file=sys.stderr,
        )
        return 2

    if not args.out:
        _dry_run_summary(boards, args.transition, args.brand)
        return 0

    html = build_html(boards, args.transition, args.brand, args.theme)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {len(boards.deliverable_frames())} slides → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
