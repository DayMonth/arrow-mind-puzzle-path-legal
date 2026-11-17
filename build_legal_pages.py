#!/usr/bin/env python3
"""Generate the Arrow Mind: Puzzle Path legal & support pages.

Run from anywhere:  python3 build_legal_pages.py [out_dir]
Default out_dir is the directory containing this script.
"""
import html
import os
import sys

import c_privacy
import c_terms
import c_support

GAME_EN = "Arrow Mind: Puzzle Path"
GAME_LOCAL = {
    "en": "Arrow Mind: Puzzle Path",
    "zh-CN": "箭头思维：谜题之路",
    "zh-TW": "箭頭思維：謎題之路",
    "ja": "アローマインド：パズルパス",
    "ko": "애로우 마인드: 퍼즐 패스",
}
LANG_ORDER = ["en", "zh-CN", "zh-TW", "ja", "ko"]
LANG_LABEL = {
    "en": "English",
    "zh-CN": "简体中文",
    "zh-TW": "繁體中文",
    "ja": "日本語",
    "ko": "한국어",
}
LANG_SUFFIX = {"en": "", "zh-CN": "-cn", "zh-TW": "-tw", "ja": "-ja", "ko": "-ko"}

DOCS = {
    "privacy": {
        "file": "privacy-policy",
        "content": c_privacy.DOC,
        "nav": {
            "en": "Privacy Policy",
            "zh-CN": "隐私政策",
            "zh-TW": "隱私權政策",
            "ja": "プライバシーポリシー",
            "ko": "개인정보 처리방침",
        },
    },
    "terms": {
        "file": "terms-of-service",
        "content": c_terms.DOC,
        "nav": {
            "en": "Terms of Service",
            "zh-CN": "服务条款",
            "zh-TW": "服務條款",
            "ja": "利用規約",
            "ko": "이용약관",
        },
    },
    "support": {
        "file": "technical-support",
        "content": c_support.DOC,
        "nav": {
            "en": "Technical Support",
            "zh-CN": "技术支持",
            "zh-TW": "技術支援",
            "ja": "テクニカルサポート",
            "ko": "기술 지원",
        },
    },
}

CSS = """
  :root { color-scheme: light dark; }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 28px 20px 72px;
    background: #2a2e6e;
    color: #f4f2ff;
    font: 16px/1.68 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
          "Helvetica Neue", Arial, "Noto Sans", "PingFang SC", "Hiragino Sans",
          "Microsoft YaHei", sans-serif;
  }
  main { max-width: 760px; margin: 0 auto; }
  h1 { font-size: 1.6rem; line-height: 1.3; margin: 0 0 .2em; }
  h2 { font-size: 1.16rem; margin: 2em 0 .5em; color: #ffd9a8; }
  h3 { font-size: 1.02rem; margin: 1.6em 0 .4em; color: #ffe6c7; }
  p, li { margin: .7em 0; }
  ul { padding-left: 1.35em; }
  hr { border: 0; border-top: 1px solid #464a8f; margin: 2em 0; }
  a { color: #8fd0ff; }
  code {
    background: #383d82; padding: .1em .35em; border-radius: 4px;
    font-size: .92em; word-break: break-word;
  }
  strong { color: #ffffff; }
  em { color: #ffe6c7; font-style: normal; }
  .langnav {
    font-size: .9rem; margin: 0 0 1.6em; color: #b9bce8;
    display: flex; flex-wrap: wrap; gap: .3em .7em;
  }
  .langnav a, .langnav strong { text-decoration: none; }
  .langnav strong { color: #ffb545; font-weight: 700; }
  footer {
    max-width: 760px; margin: 3em auto 0; font-size: .85rem; color: #b9bce8;
    border-top: 1px solid #464a8f; padding-top: 1em; line-height: 1.9;
  }
  @media (prefers-color-scheme: light) {
    body { background: #f4f6ff; color: #23263f; }
    h2 { color: #8a4b00; }
    h3 { color: #6b3a00; }
    strong { color: #111428; }
    em { color: #6b3a00; }
    a { color: #1d4ed8; }
    code { background: #e3e7ff; }
    hr, footer { border-color: #cdd3f2; }
    .langnav { color: #5a5f88; }
    .langnav strong { color: #b36b00; }
    footer { color: #5a5f88; }
  }
"""

INDEX_CSS = """
  :root { color-scheme: light dark; }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; display: flex; align-items: center;
    justify-content: center; background: #2a2e6e; color: #f4f2ff;
    font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
          "Helvetica Neue", Arial, "Noto Sans", "PingFang SC", "Hiragino Sans",
          "Microsoft YaHei", sans-serif;
  }
  main { max-width: 600px; width: 100%; padding: 40px 24px; }
  h1 { font-size: 1.5rem; line-height: 1.3; margin: 0 0 .3em; }
  p.sub { color: #b9bce8; margin: 0 0 1.8em; }
  ul { list-style: none; padding: 0; margin: 0; }
  li { margin: .6em 0; }
  a.card {
    display: block; padding: 14px 18px; border-radius: 14px;
    background: #383d82; color: #f4f2ff; text-decoration: none;
    border: 1px solid #464a8f;
  }
  a.card:hover { background: #454b9a; }
  a.card span { color: #ffb545; float: right; }
  .langs { margin-top: 2em; font-size: .88rem; color: #b9bce8; line-height: 2; }
  .langs a { color: #8fd0ff; }
  footer { margin-top: 2.2em; font-size: .82rem; color: #b9bce8; }
  @media (prefers-color-scheme: light) {
    body { background: #f4f6ff; color: #23263f; }
    p.sub, .langs, footer { color: #5a5f88; }
    a.card { background: #ffffff; border-color: #cdd3f2; color: #23263f; }
    a.card:hover { background: #eef1ff; }
    a.card span { color: #b36b00; }
    .langs a { color: #1d4ed8; }
  }
"""


def doc_name(doc_key, lang):
    return DOCS[doc_key]["nav"][lang]


def href(doc_key, lang):
    return DOCS[doc_key]["file"] + LANG_SUFFIX[lang] + ".html"


def render_blocks(blocks):
    out = []
    for kind, value in blocks:
        if kind == "h2":
            out.append("<h2>%s</h2>" % value)
        elif kind == "h3":
            out.append("<h3>%s</h3>" % value)
        elif kind == "p":
            out.append("<p>%s</p>" % value)
        elif kind == "ul":
            items = "\n".join("<li>%s</li>" % i for i in value)
            out.append("<ul>\n%s\n</ul>" % items)
    return "\n".join(out)


def langnav(doc_key, lang):
    parts = []
    for code in LANG_ORDER:
        label = LANG_LABEL[code]
        if code == lang:
            parts.append("<strong>%s</strong>" % label)
        else:
            parts.append('<a href="%s" hreflang="%s" lang="%s">%s</a>'
                         % (href(doc_key, code), code, code, label))
    return '<p class="langnav">%s</p>' % " · ".join(parts)


def footer(doc_key, lang):
    links = []
    for key in ("privacy", "terms", "support"):
        if key == doc_key:
            links.append("<strong>%s</strong>" % doc_name(key, lang))
        else:
            links.append('<a href="%s">%s</a>' % (href(key, lang), doc_name(key, lang)))
    return ("<footer>\n%s · %s\n</footer>"
            % (html.escape(GAME_LOCAL[lang]), " ·\n".join(links)))


def page(doc_key, lang, data):
    body = []
    body.append("<h1>%s</h1>" % data["h1"])
    body.append(langnav(doc_key, lang))
    body.append(render_blocks(data["lead"]))
    body.append("<hr>")
    body.append(render_blocks(data["sections"]))
    body.append("<hr>")
    body.append("<p><em>%s</em></p>" % data["note"])
    return """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<style>{css}</style>
</head>
<body>
<main>
{body}
</main>
{footer}
</body>
</html>
""".format(
        lang=lang,
        title=html.escape(data["title"]),
        desc=html.escape(data["title"]),
        css=CSS,
        body="\n".join(body),
        footer=footer(doc_key, lang),
    )


def index_page():
    cards = []
    for key in ("privacy", "terms", "support"):
        cards.append('<li><a class="card" href="%s">%s <span>&rarr;</span></a></li>'
                     % (href(key, "en"), DOCS[key]["nav"]["en"]))
    langs = " · ".join(
        '<a href="privacy-policy%s.html" hreflang="%s">%s</a>'
        % (LANG_SUFFIX[code], code, LANG_LABEL[code]) for code in LANG_ORDER)
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Arrow Mind: Puzzle Path — Legal &amp; Support</title>
<style>{css}</style>
</head>
<body>
<main>
<h1>Arrow Mind: Puzzle Path</h1>
<p class="sub">Legal and support pages for the mobile puzzle game.</p>
<ul>
{cards}
</ul>
<p class="langs">Available in: {langs}</p>
<footer>Arrow Mind: Puzzle Path is an independent game. Apple, App Store,
iPadOS, Google, Google Play and Android are trademarks of their respective owners.</footer>
</main>
</body>
</html>
""".format(css=INDEX_CSS, cards="\n  ".join(cards), langs=langs)


README = """# Arrow Mind: Puzzle Path — legal & support pages

Live site: **https://daymonth.github.io/arrow-mind-puzzle-path-legal/**
Repository: `DayMonth/arrow-mind-puzzle-path-legal` (public, GitHub Pages from `main` / root).

These pages are the targets of the in-app Settings links (`LEGAL_BASE` in
`src/app/game.gd`) and of the App Store Connect **Privacy Policy URL** and
**Support URL** fields, so they must stay publicly reachable without a login.

| Document | English | 简体中文 | 繁體中文 | 日本語 | 한국어 |
| --- | --- | --- | --- | --- | --- |
| Privacy Policy | `privacy-policy.html` | `-cn` | `-tw` | `-ja` | `-ko` |
| Terms of Service | `terms-of-service.html` | `-cn` | `-tw` | `-ja` | `-ko` |
| Technical Support | `technical-support.html` | `-cn` | `-tw` | `-ja` | `-ko` |

`index.html` is the landing page; `.nojekyll` disables Jekyll processing.

## Editing

The HTML is generated — do not hand-edit it. Sources are the three content
modules (`c_privacy.py`, `c_terms.py`, `c_support.py`) and `build_legal_pages.py`:

```sh
python3 build_legal_pages.py          # regenerate all 15 pages + index
python3 build_legal_pages.py --check  # verify the published files are current
```

Keep filenames stable: the app and the store listings hard-code them.

## Publishing an update

```sh
python3 build_legal_pages.py
git add -A && git commit -m "Update legal pages" && git push
```

GitHub Pages rebuilds automatically. Check status with:

```sh
gh api repos/DayMonth/arrow-mind-puzzle-path-legal/pages --jq .status
```
"""


def build(out_dir):
    written = []
    for key, doc in DOCS.items():
        for lang, data in doc["content"].items():
            name = doc["file"] + LANG_SUFFIX[lang] + ".html"
            path = os.path.join(out_dir, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(page(key, lang, data))
            written.append(name)

    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_page())
    written.append("index.html")

    nojekyll = os.path.join(out_dir, ".nojekyll")
    if not os.path.exists(nojekyll):
        open(nojekyll, "w").close()
    written.append(".nojekyll")

    readme = os.path.join(out_dir, "README.md")
    if not os.path.exists(readme) or "--force-readme" in sys.argv:
        with open(readme, "w", encoding="utf-8") as f:
            f.write(README)
        written.append("README.md")

    return written


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out_dir = args[0] if args else os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    written = build(out_dir)
    print("wrote %d files to %s" % (len(written), out_dir))
    for name in written:
        print("  " + name)


if __name__ == "__main__":
    main()
