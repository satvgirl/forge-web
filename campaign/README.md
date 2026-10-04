# Forge on Instagram — campaign plan

Goal: **fill the private beta.** Success = people tapping the link and
submitting the "Request an invite" form, measured per `?src=` label.
Followers and likes are secondary. As of 2026-10-03 the waitlist has 3
signups, none tagged, so every number below starts from roughly zero.

Voice: **the dragon is the brand.** The account speaks as Forge — warm,
direct, never shaming. The human is in the bio only ("built by one person in
Ontario"), which matches the site's "built and run by one person" and keeps
the trust without putting a face on the account.

## Before you post anything

1. **Invites — sorted (2026-10-04).** An external TestFlight group is active and the first three signups were invited by email, so people can be onboarded. Keep sending invites promptly: they're sent by hand, so decide how often you'll batch them. (Original concern: The site says "I'll send you an
   invite." Per `Documentation/releasing_ios.md`, an *external* TestFlight
   group needs Beta App Review (hours to ~a day) and only an internal group
   skips it; internal testers must be users on your App Store Connect team
   (max 100). If no external group has passed review yet, submit one first, or
   people will request an invite you can't send.)
2. **Art check.** The CDN art used here is clean (see `make_assets.py` for the
   two images to avoid). The app itself still serves `copper/mature-balanced.png`,
   which has a grey background and garbled text in the corner — worth fixing
   before testers see a mature dragon (ROADMAP 3.5).
3. **AI-art disclosure.** The brand doc describes the dragons as image-generated.
   Decide whether to say so (bio line or an About highlight). Instagram may also
   add an "AI info" label to posts. Saying it plainly fits your "no gimmicks"
   stance better than being found out.
4. Make a real Instagram **professional account** (Creator or Business) so you
   get Insights. Turn on two-factor auth. Use a brand email (e.g. hello@ on
   your forge-app.ca mail), not your personal one.

## Profile

- **Name:** `Forge · Build your dragon` (name field is searchable; the handle isn't)
- **Handle** (check availability): `forge.dragon`, `forgeapp.ca`, `buildyourdragon`, `forge.dragon.app`
- **Picture:** `assets/profile/profile-picture.png` (egg, centred so the circle crop is safe)
- **Bio** (≤150 chars):
  ```
  Build your dragon, build yourself. 🐉
  Strength tracking where every workout hatches a companion.
  Private beta · iPhone
  Made by one person in Ontario 🇨🇦
  ```
- **Link:** `https://forge-app.ca/?src=instagram-bio`
- **Category:** "Mobile app" or "App page". Contact button → email.
- **Highlights** (make from stories after week 1): *Meet the dragon*, *How it works*, *Join the beta*, *FAQ*.

## Tagged links (so signups are attributable)

The site stores `?src=` with each signup. Instagram captions don't link, so:

| Where | Link |
|---|---|
| Bio | `forge-app.ca/?src=instagram-bio` |
| Story link sticker | `forge-app.ca/?src=instagram-story` |
| Per-reel (pin in a comment, or swap the bio link during a push) | `forge-app.ca/?src=ig-reel-<name>` |
| DMs | `forge-app.ca/?src=ig-dm` |

Test the bio link on your phone from inside Instagram — in-app browsers and
link-in-bio tools sometimes drop query strings. Pull the counts any time with
the KV read used on 2026-10-03 (`wrangler kv key list/get`, or
`GET /api/waitlist/export` with `ADMIN_TOKEN`).

## Content pillars

1. **Meet the dragon** (about 40%): stages, colours, moods. The art is the hook.
2. **Strength, kindly** (30%): consistency over intensity, rest is part of it,
   no leaderboards, any starting point. The audience (women 40+) is tired of
   gym-bro and shame; say the opposite out loud.
3. **Inside the beta** (30%): real screens, new features, testers' words (with
   permission), and the one-person build.

## Guardrails

- No weight-loss, body, or health claims. No before/after bodies. No promising
  an App Store date. Always say **iPhone only, private beta**.
- Only claim what the app does today: lifetime-volume stages (20k / 50k / 100k
  lbs), mood by training days in the last week (4+ fierce, 2–3 balanced,
  fewer gentle), kg/lbs, templates, share card, CSV export, no ads, no
  third-party tracking.
- Celebrate effort; never moralise about missed days.
- Ask before reposting any tester's words or screenshots.

## Weekly rhythm (about 3 posts + stories)

| Day | What |
|---|---|
| Tue | Reel |
| Thu | Carousel |
| Sat | Single image or reel |
| Mon/Wed/Fri | 1–3 stories: poll, a behind-the-scenes screen, the invite sticker |
| Daily, 10 min | Reply to every comment/DM; comment genuinely on 5–10 accounts in the strength-over-40 space |

## Measure

Check Insights and the signup counts weekly. Starting-guess targets (not
researched): **15 signups from Instagram in the first 4 weeks**, >3% of
profile visits tapping the link. If a post's reach is fine but nobody taps,
change the CTA; if reach is low, change the hook (first 2 seconds / first slide).

## Files

- `calendar.md` — 4-week plan with captions and CTAs
- `make_assets.py` → `assets/` — carousels, single post, story frame, profile picture
  (re-run to regenerate; dragon art is fetched from the CDN, not stored)
- Reels need screen footage: `scripts/record_reel.sh <sim-udid>` in the app repo
  records the scripted walk-through (demo account evolves the dragon); trim and
  caption it separately.
