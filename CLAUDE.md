# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Public marketing/launch site + legal pages for **Forge** (a strength-training
app with a companion dragon that grows as your training adds up). Served by
**Cloudflare Workers** at <https://forge-app.ca> — a Worker (`src/worker.js`)
serves `public/` as static assets and implements a small waitlist API; no
framework, no bundler, no third-party services.

The app itself (iOS + AWS backend) lives in a separate repo, `~/git_repos/forge`
— see its `Documentation/brand_and_avatar_art.md` for brand voice/palette and
`Documentation/ROADMAP.md` for the app's launch status (currently pre-App-Store,
TestFlight only — this site's copy should stay consistent with that: a
waitlist/beta pitch, not a download page).

## Commands

```bash
npm install
npm run dev        # wrangler dev — serves public/ + the Worker locally
npm run deploy      # wrangler deploy — deploys straight to production, no CI/staging step
```

## Structure

Each route under `public/` is a self-contained `.html` file with its own
inline `<style>` block — there is no shared CSS/JS file and no templating
system. When editing one page's look, check whether the same visual change
is expected on the others (index, 404, privacy, terms, about) and apply it
by hand to each.

| Path | URL |
|---|---|
| `public/index.html` | `/` |
| `public/privacy/index.html` | `/privacy` |
| `public/terms/index.html` | `/terms` |
| `public/about/index.html` | `/about` |
| `public/404.html` | any missing path |
| `public/favicon.svg` | shared favicon (dragon egg mark), linked from every page's `<head>` |

Routing: `wrangler.toml`'s `[assets]` binding serves `public/` directly for
any request that matches a file. Anything that doesn't match (including
`/api/*`) falls through to `src/worker.js`'s `fetch()` handler, which either
handles the API route or manually serves `public/404.html` with a real 404
status — see the comment at the top of `worker.js` for why `not_found_handling`
is deliberately left unset rather than `"404-page"` (that setting would let
the asset system intercept `/api/*` requests before the Worker ever saw them).

## Waitlist API

`POST /api/waitlist` — JSON or form-encoded body (`email`, plus a hidden
`company` honeypot field the real form never fills). Stores signups in the
`WAITLIST` KV namespace keyed by lowercased email, so a repeat signup is an
idempotent overwrite, not a duplicate. Responds JSON if the request's
`Accept` header asks for it (the page's own `fetch()` call does), otherwise
responds with a small server-rendered HTML page — this is what makes the
form work with JavaScript disabled.

`GET /api/waitlist/export` — admin-only, gated on a Worker secret
(`ADMIN_TOKEN`, set via `wrangler secret put`, never committed); returns all
signups as CSV. This is the only way to read the list back out — deliberately
no third-party email/CRM tool, matching the site's "no ads, no third-party
tracking" stance (see `public/about/index.html`).

## Design tokens

All pages share the same CSS custom-property palette (light + `prefers-
color-scheme: dark` variants), defined independently in each file's
`<style>` block — these trace back to the brand palette in the `forge` repo's
`Documentation/brand_and_avatar_art.md` (copper/sage/cream/charcoal):

```
--bg, --surface, --text, --muted, --rule, --accent, --link
```

Light: `--bg:#f9f7f3 --text:#2b2b2b --muted:#6b6b6b --rule:#e5e0d8 --accent:#b06a3b --link:#9a5a2f`
Dark: `--bg:#1a1917 --text:#e9e6e0 --muted:#a5a09a --rule:#38352f --accent:#d9945f --link:#e0a276`

`public/index.html` additionally defines `--primary`/`--primary-hover`/
`--primary-text` (sage, `#9caf88` light) for its CTA button, per the brand
doc's "primary buttons are sage, secondary are copper outline" rule — reuse
that pair rather than the copper `--accent` for any new primary buttons.

Keep new/edited pages consistent with these values rather than introducing
new colors, and don't add photographic art — the dragon avatar renders in
the app's CDN are documented first-pass placeholder art there, not final
brand assets; the site instead uses small inline SVG line-art (see the egg
mark in `public/index.html` / `public/favicon.svg`).

## Legal pages

`privacy`, `terms`, and `about` were drafted from the Forge app codebase as a
minimal starting point — **not legal advice**. Each has an inline "Effective"
/ "Last updated" date (`<p class="dates">`) that must be bumped whenever the
page's content changes materially. Operator details (Judy Leach · Ontario,
Canada · privacy@forge-app.ca) are inline in the text, not templated.

## DNS / hosting migration

The move from GitHub Pages to Cloudflare Workers (including exact DNS record
values for the Zoho-hosted email on this domain, and why the domain's
nameserver changes happen in the AWS Route53 console rather than at the
registrar) is documented step-by-step in `MIGRATION.md`. That file is the
source of truth for anything DNS-related on `forge-app.ca` — don't
re-derive it from scratch.
