# valgau-asu.github.io

My personal website. Plain HTML, CSS and JavaScript — no build step, no
dependencies. Edit a file, refresh the browser.

Live at <https://valgau-asu.github.io>.

## Local preview

```bash
python3 dev.py
```

Serves <http://localhost:8000> and reloads the page whenever a file is saved.
Development only — it injects the reload script as it serves, never on disk.
Pass a port if 8000 is taken: `python3 dev.py 3000`.

## Layout

```
index.html           About
experience.html      Positions
phd-research.html    PhD project cards
other-projects.html  Coursework and earlier project cards
publications.html    Publications
newsletter.html      Newsletter index
project-*.html       Project write-ups
post-*.html          Newsletter posts
css/style.css        All styling; colors in :root
js/main.js           Menu, theme toggle, footer year, click-to-play video
pictures/  pdfs/  videos/
```

## Conventions

- The nav bar is duplicated in every page. Adding a page means adding the link
  everywhere and setting `aria-current="page"` on its own entry.
- Dark mode rules are written twice: under `prefers-color-scheme` guarded by
  `:not([data-theme="light"])`, and under `[data-theme="dark"]` for the toggle.
  A new dark rule needs both.
- After changing `css/style.css`, bump `?v=N` on the stylesheet link in every
  page. GitHub Pages caches it for ten minutes otherwise.
- Equations use KaTeX from a CDN, loaded only on the pages that need it.
  It is the site's one external dependency.

## Publish

```bash
git add -A && git commit -m "Update site" && git push
```
