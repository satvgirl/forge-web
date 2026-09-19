# Migrating forge-app.ca: GitHub Pages → Cloudflare Workers

This is the runbook for moving `forge-app.ca` off GitHub Pages onto
Cloudflare Workers (static assets + the `/api/waitlist` route in
`src/worker.js`). **Follow it in order — steps 1–6 are all reversible /
non-production-affecting; step 7 is the live cutover.**

## Background (found while planning this migration)

- **Registrar of record is AWS Route53 Domains** (whois shows registrar
  `Gandi`/reseller `Amazon Registrar, Inc.` — the standard signature of a
  `.ca` domain bought through Route53 Domains, since Amazon isn't itself
  accredited for `.ca`). **Nameserver changes happen in the Route53 console
  → Registered domains → `forge-app.ca`, not at Gandi directly.**
- The current Route53 hosted zone (`Z088178031SES09ERAT3F`) also holds an
  **issued wildcard ACM certificate** (`forge-app.ca` + `*.forge-app.ca`)
  validated via a CNAME record, currently attached (unused in live DNS) to
  the avatar CDN's CloudFront distribution. Decision: **keep the
  certificate** — it's reusable later for `api.forge-app.ca`
  (`forge` repo's `Documentation/ROADMAP.md` item 1.7) so its DNS validation
  record must be recreated in Cloudflare too. The CloudFront alias itself is
  confirmed unused; no action needed there.
- No DMARC or CAA record exists on the zone today — this migration
  preserves that (doesn't add either), it's parity-only.

## Step 1 — Add the zone to Cloudflare

In the Cloudflare dashboard: **Add a site** → `forge-app.ca` → pick the Free
plan → Cloudflare scans existing DNS and shows you a pending zone. It'll give
you two nameservers (e.g. `xxx.ns.cloudflare.com`, `yyy.ns.cloudflare.com`).
**Don't change anything at the registrar yet.**

## Step 2 — Recreate the non-web DNS records

Cloudflare's auto-scan usually picks up the `A`/`AAAA`/`www` `CNAME` already
(pointing at GitHub Pages) — those get replaced in Step 4, so ignore them.
**Manually add these** (all **DNS only**, grey-clouded, not proxied — MX and
these TXT/CNAME records must not be proxied):

| Type | Name | Value | Priority |
|---|---|---|---|
| MX | `forge-app.ca` | `mx.zohocloud.ca` | 10 |
| MX | `forge-app.ca` | `mx2.zohocloud.ca` | 20 |
| MX | `forge-app.ca` | `mx3.zohocloud.ca` | 50 |
| TXT | `forge-app.ca` | `v=spf1 include:zohocloud.ca ~all` | — |
| TXT | `forge-app.ca` | `zoho-verification=zb62907535.zmverify.zohocloud.ca` | — |
| TXT | `zmail._domainkey.forge-app.ca` | `v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCDwBYV6kPHb2/e0QLFy4dFy2Lo45GdINP9oxGOkS84z8v2oL+YOFJpLiSMsO1aI1OllbvIahmJJ9iblNLdWBLVusDmLsgRrigEpNLKNSiMDG4A+4Tvs9Kyp77v3dNtdrfiOqfGJ+17PzE99ovB1AvEl9cN5G0+mIDIyPg4Vu5Q6wIDAQAB` | — |
| CNAME | `_18a6b5ec0134a9944b3181001feb59ee.forge-app.ca` | `_0bebbfdd20c05a09f799af90882c4ef5.jkddzztszm.acm-validations.aws.` | — |

Do **not** recreate `_github-pages-challenge-satvgirl` — it was GitHub Pages'
domain-ownership proof and isn't needed once we're off GitHub Pages.

## Step 3 — Install deps, create the KV namespace, deploy

```bash
cd ~/git_repos/forge-web
npm install
npx wrangler login                     # opens a browser, authorizes wrangler
npx wrangler kv namespace create WAITLIST
# copy the returned id into wrangler.toml, replacing REPLACE_WITH_KV_NAMESPACE_ID
npx wrangler secret put ADMIN_TOKEN    # paste a long random string when prompted — this is how you'll authenticate `/api/waitlist/export`
npx wrangler deploy
```

Verify at the `*.workers.dev` URL wrangler prints: check `/`, `/about`,
`/privacy`, `/terms`, a bogus path (should show the custom 404), and submit
the waitlist form.

## Step 4 — Attach the custom domains

Cloudflare dashboard → **Workers & Pages → forge-web → Settings → Domains &
Routes → Add → Custom Domain** → add both `forge-app.ca` and
`www.forge-app.ca`. This auto-creates the proxied DNS records Cloudflare
needs — you don't manually add `A`/`AAAA` records for these.

## Step 5 — Redirect `www` → apex

Cloudflare dashboard → **Rules → Redirect Rules** → create a rule:
`www.forge-app.ca/*` → `https://forge-app.ca/$1` (301, preserve query
string). This replaces what GitHub Pages did automatically for the
apex/`www` pair.

## Step 6 — Verify the pending zone before touching anything live

Query Cloudflare's assigned nameservers directly (works even while the zone
is still "pending" at the registrar):

```bash
dig @<cloudflare-ns-1> forge-app.ca A
dig @<cloudflare-ns-1> forge-app.ca MX
dig @<cloudflare-ns-1> forge-app.ca TXT
dig @<cloudflare-ns-1> zmail._domainkey.forge-app.ca TXT
```

Confirm MX/TXT/DKIM match Step 2's table exactly, and that `A`/`www` resolve
(via the Custom Domain from Step 4) to Cloudflare, not GitHub Pages.

## Step 7 — Cut over nameservers (the live step)

AWS Console → **Route53 → Registered domains → forge-app.ca → Edit name
servers** → replace the four `awsdns-*` nameservers with Cloudflare's two.
`.ca` (CIRA) propagation is typically fast (often under an hour), but can
take up to 24–48h depending on caching resolvers.

## Step 8 — Post-cutover verification

- `dig forge-app.ca` from a normal resolver — should return Cloudflare, not
  GitHub Pages IPs.
- Load `https://forge-app.ca` and `https://www.forge-app.ca` in a browser
  (confirm the redirect).
- **Send a real test email** to a `@forge-app.ca` Zoho mailbox and confirm
  it arrives — this is the one step that silently breaks if any Zoho record
  from Step 2 was mistyped.
- Submit the waitlist form on the live domain; confirm via
  `npx wrangler kv key get --binding=WAITLIST <email>` or the export
  endpoint (`curl -H "Authorization: Bearer <ADMIN_TOKEN>" https://forge-app.ca/api/waitlist/export`).

## Step 9 — Cleanup (after a stable soak period — not same-day)

- GitHub repo `satvgirl/forge-web` → Settings → Pages → disable/remove the
  Pages site.
- Once confident nothing depends on it, delete the now-dead Route53 hosted
  zone (`Z088178031SES09ERAT3F`) to stop the small monthly charge for it.
