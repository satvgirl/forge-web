# forge-web

Public marketing/launch site + legal pages for [Forge](https://github.com/satvgirl/forge)
— a strength-training app with a companion dragon that grows as your training
adds up. Served by **Cloudflare Workers** at <https://forge-app.ca>.

## Contents

| Path | URL | Notes |
|---|---|---|
| `public/index.html` | `/` | Launch page — product pitch + email waitlist |
| `public/privacy/index.html` | `/privacy` | Privacy policy (linked from the App Store listing, TestFlight, and in-app Settings) |
| `public/terms/index.html` | `/terms` | Terms of service (linked from in-app Settings) |
| `public/about/index.html` | `/about` | About page (linked from in-app Settings) |
| `public/404.html` | any missing path | Custom not-found page, served by the Worker |
| `public/favicon.svg` | — | Shared favicon (dragon egg mark) |
| `src/worker.js` | — | Cloudflare Worker: static-asset fallthrough for unmatched paths + the waitlist API (`POST /api/waitlist`, `GET /api/waitlist/export`) |
| `wrangler.toml` | — | Worker + static-assets + KV config |
| `MIGRATION.md` | — | One-time runbook for the GitHub Pages → Cloudflare DNS cutover |

Each HTML page is self-contained (inline `<style>`, light/dark via
`prefers-color-scheme`, no build step, no shared CSS/JS file). When editing
one page's look, check whether the same change is expected on the others and
apply it by hand to each.

## Local development

```bash
npm install
npm run dev        # wrangler dev — serves public/ + the Worker locally
```

## Waitlist

`POST /api/waitlist` (JSON or form-encoded body: `email`, plus a hidden
`company` honeypot field) stores signups in the `WAITLIST` KV namespace,
keyed by lowercased email (a repeat signup just overwrites, so it's
idempotent). No third-party email/CRM service and no confirmation email —
this keeps the site's "no ads, no third-party tracking" stance from the
About page.

To pull the signup list:

```bash
curl -H "Authorization: Bearer <ADMIN_TOKEN>" https://forge-app.ca/api/waitlist/export
```

`ADMIN_TOKEN` is a Worker secret (`wrangler secret put ADMIN_TOKEN`), never
committed.

## Publishing

```bash
npm run deploy      # wrangler deploy
```

There's no CI/staging step — a deploy is a deploy to production. See
`MIGRATION.md` for the one-time DNS cutover from GitHub Pages.

## Legal pages

`privacy`, `terms`, and `about` were drafted from the Forge codebase and are
a minimal starting point, **not legal advice** — have them reviewed before
relying on them. Operator details (Judy Leach · Ontario, Canada ·
privacy@forge-app.ca) and the "Last updated" dates are inline in each file;
keep the dates current on material changes.
