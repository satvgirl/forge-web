# forge-web

Public static site for [Forge](https://github.com/satvgirl/forge) — the marketing
landing page and legal pages. Served by **GitHub Pages** from `main` / root.

## Contents

| Path | URL | Notes |
|---|---|---|
| `index.html` | `/` | Placeholder landing page |
| `privacy/index.html` | `/privacy` | Privacy policy (linked from the App Store listing and TestFlight) |
| `404.html` | any missing path | Custom not-found page |
| `.nojekyll` | — | Disables Jekyll; files are served as-is |

## Publishing

Push to `main` — GitHub Pages redeploys automatically (Settings → Pages).

## Custom domain

Not yet configured. To point `forge-app.ca` here:

1. Settings → Pages → **Custom domain** → `forge-app.ca` (this adds a `CNAME` file).
2. At the DNS provider, add the four GitHub Pages `A` records and four `AAAA`
   records for the apex (see GitHub's docs). `api.forge-app.ca` stays a separate
   record pointing at AWS.
3. Wait for the green check, then enable **Enforce HTTPS**.

Until then the site is at `https://satvgirl.github.io/forge-web/`.

## Privacy policy

Before the policy is relied on, replace the placeholders in `privacy/index.html`:
`{{OPERATOR}}`, `{{JURISDICTION}}`, `{{CONTACT_EMAIL}}`. It was drafted from the
Forge codebase and is not legal advice — have it reviewed.
