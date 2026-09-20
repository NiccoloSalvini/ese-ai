# CLAUDE.md — AI for Business and FinTech (ESE Florence)

Course repository *and* course website for *Artificial Intelligence for Business
and FinTech*, ESE Short Course, European School of Economics, Florence, Term 1
A.Y. 2026–2027. Module leader Niccolò Salvini. One-to-one tutorial and lab.

Live site: <https://niccolosalvini.github.io/ese-ai/> · Repo: `NiccoloSalvini/ese-ai` (public)

## Commands

```bash
make preview   # quarto preview, live reload
make build     # quarto render -> _site/
make deploy    # render locally, then quarto publish gh-pages (pushes _site/ to the gh-pages branch)
make clean
```

No CI. The site is rendered on this machine and `_site/` is pushed to the
`gh-pages` branch; GitHub Pages serves that branch. Same philosophy as
`sbd_26_27`: fewer moving parts on a Monday at 08:50.

## Layout

```
week-NN/
  notes.md        tutor-only: session plan, script, planted errors, tutor's notes — NOT rendered on the site
  cards.md        Marp cards for the projector; ALSO rendered by Quarto as revealjs (front matter serves both)
  session.ipynb   live Colab notebook; rendered read-only on the site, outputs never executed
  homework.md     assignment; rendered on the site
  data/           small snapshots, copied verbatim (resources)
index.qmd         schedule table — the home page, one row per session
syllabus.qmd      web version of syllabus/ESE_AI_FinTech_Course_Design_v2.docx (converted with pandoc, then hand-edited)
setup.qmd         student checklist (Colab, GitHub, Colab Secrets, chat assistant)
styles.scss       ESE brand on top of cosmo
slides.scss       ESE brand for the revealjs cards
_fonts.html       Google Fonts <link>, shared by html and revealjs via include-in-header
images/           ESE logo/favicon (from ese.ac.uk), tutor photo
```

`_quarto.yml` lists the rendered files explicitly under `project.render`.
Anything not listed (notes.md, build_nb.py, `_build/`, `.claude/`) stays off the site.

## Brand (from ese.ac.uk, September 2026)

Red `#AF1F25` (primary, links, navbar hairline), gold `#CDBA80` (labels, accents),
ink `#363636`, square corners everywhere, Source Sans 3 (Google Fonts) for text,
JetBrains Mono for code. Tone: professional, pragmatic, direct — "every line you
submit, you can explain". Motto in the footer: *Visibilia ex Invisibilibus*.

## Gotchas

- `.env.example` was renamed `.env.template`: Quarto reads `.env.example` in
  dotenv safe mode and refuses to render if the variables are unset.
- Reveal font: Quarto interpolates `$font-family-sans-serif` into `--r-main-font`
  unquoted; `Source Sans 3` unquoted is invalid CSS (starts with a digit) and the
  browser falls back to serif. `slides.scss` therefore re-sets the CSS variables
  in the rules section with quotes.
- `cards.md` front matter carries both `marp: true` and `format: revealjs`
  with `slide-level: 0`, so `---` is the only slide separator for both tools.
  `marp cards.md -o cards.pdf` still works for printing.
- The ESE logo SVG has no intrinsic width; `.navbar-logo` sets `height` + `width: auto`.
- Rendered `.ipynb` uses stored outputs only (`execute: enabled: false`). The
  notebooks have no outputs committed, so the preview shows code and prose.

## Weekly loop

Materials for week N are already in the repo. Publishing them is `make deploy`.
To change a date or a link, edit the row in `index.qmd`. When Moodle is available,
add the Moodle link to the navbar and to the syllabus "Materials and channels" row;
the Moodle MCP is configured in `.mcp.json` (see README).
