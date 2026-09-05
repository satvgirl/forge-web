# forge-web

Public static site for [Forge](https://github.com/satvgirl/forge) — the marketing
landing page and legal pages. Served by **GitHub Pages** from `main` / root at
<https://forge-app.ca>.

## Contents

| Path | URL | Notes |
|---|---|---|
| `index.html` | `/` | Placeholder landing page |
| `privacy/index.html` | `/privacy` | Privacy policy (linked from the App Store listing, TestFlight, and in-app Settings) |
| `terms/index.html` | `/terms` | Terms of service (linked from in-app Settings) |
| `about/index.html` | `/about` | About page (linked from in-app Settings) |
| `404.html` | any missing path | Custom not-found page |
| `CNAME` | — | Custom domain (`forge-app.ca`) |
| `.nojekyll` | — | Disables Jekyll; files are served as-is |

## Publishing

Push to `main` — GitHub Pages redeploys automatically (Settings → Pages).

## Legal pages

`privacy`, `terms`, and `about` were drafted from the Forge codebase and are a
minimal starting point, **not legal advice** — have them reviewed before relying
on them. Operator details (Judy Leach · Ontario, Canada · privacy@forge-app.ca)
and the "Last updated" dates are inline in each file; keep the dates current on
material changes.
