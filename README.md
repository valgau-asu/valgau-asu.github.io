# Personal website — Valentin Gaucher

Plain HTML/CSS/JS. No build step, no dependencies. Edit a file, refresh the browser.

## Files

```
index.html          About / landing page
experience.html     Research and engineering positions
projects.html       Project cards
publications.html   Publication list
media.html          Talks, videos, slides
css/style.css       All styling. Colors live in :root at the top.
js/main.js          Mobile menu + footer year
pictures/           Photo and project images
pictures/logo/      Affiliation logos
pdfs/               CV, papers, slides, BibTeX
.nojekyll           Tells GitHub Pages to serve files as-is
```

## Preview locally (with live reload)

```bash
cd ~/Documents/Website && python3 dev.py
```

Open http://localhost:8000. Save any file and the browser refreshes itself —
no need to hit reload. Ctrl-C in the terminal to stop.

`dev.py` is a development tool only. It injects a small reload script into pages
as it serves them; your files on disk are never modified, and GitHub Pages serves
them plainly. Pass a port if 8000 is busy: `python3 dev.py 3000`.

## Editing

- **Text and links:** open the `.html` file and edit between the tags. Anything in
  `[square brackets]` or named `YOUR_USERNAME` / `VIDEO_ID` is a placeholder to replace.
- **Adding a project or paper:** each page has a commented block marked
  `COPY THIS BLOCK` — duplicate it and fill it in.
- **The nav bar** is copied into all five pages. If you add a page, add the link in
  all five, and set `aria-current="page"` on the current page's own link.
- **Colors and fonts:** the `:root` block at the top of `css/style.css`. Change
  `--accent` to restyle the whole site. Dark mode is handled automatically.

## Images

Replace the `.svg` placeholders with real images and update the `src` in the HTML:

- `profile` — the hero photo; portrait is fine, CSS crops it to a square
- project thumbnails — 16:9, around 800×450
- Keep files under ~500 KB so pages stay fast.

Once you have a real profile photo, also point `og:image` in `index.html` at it
using a full URL (`https://YOUR_USERNAME.github.io/assets/img/profile.jpg`) — that
is what shows when someone shares your link.

## Deploying to GitHub Pages

1. Create a repo on GitHub named exactly **`YOUR_USERNAME.github.io`** (public).
2. Then, from this folder:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_USERNAME.github.io.git
git branch -M main
git push -u origin main
```

3. On GitHub: **Settings → Pages → Source: Deploy from a branch → `main` / `(root)`**.
4. Your site appears at `https://YOUR_USERNAME.github.io` within a minute or two.

Afterwards, publishing changes is just:

```bash
git add -A && git commit -m "Update site" && git push
```
