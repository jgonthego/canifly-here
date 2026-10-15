# Can I Fly Here? — Maintenance
- Data: `data/states.json`. `reviewed` = last-reviewed date (shown on every page). `focus.<slug>` = in-depth state: `laws` [[text,url]], `parks` [text,url], `local` [text,(url)]. Only add facts with a source URL.
- To deepen a state: add an entry under `focus` with its slug (e.g. `ohio`).
- Build: `BASE=https://<user>.github.io/<repo> python3 build.py` → outputs `docs/` (static HTML, sitemap.xml, robots.txt).
- Deploy (GitHub Pages): `gh auth login`; `gh repo create canifly-here --public --source . --push`; then repo Settings → Pages → branch `main`, folder `/docs`. Rebuild + push to update.
- Placeholders: Formspree form ID (`FORM` in build.py), affiliate slots (`AFFILIATE SLOT` comments), sponsor block.
