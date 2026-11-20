# Arrow Mind: Puzzle Path — legal & support pages

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

The three content modules were regenerated on **2026-11-20** from the game
repository's `docs/legal/*.md` (5 languages × privacy / terms / support). When the
game repository's legal markdown changes, re-generate the modules from it first,
then run the build — do not edit the HTML.

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
