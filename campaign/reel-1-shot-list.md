# Reel 1 — "One workout. One hatch." (evolve version: "One workout. One evolution.")

**Length:** 20–25 s final cut · **Format:** 9:16 (1080×1920), H.264, captions burned in
(most people watch muted) · **Voice:** the dragon — no voice-over needed.
**Source footage:** the scripted run in the app repo (`scripts/record_reel.sh`),
which drives the DEBUG demo account on a simulator.

> **Two takes are available.** The app repo's `scripts/record_reel.sh` now
> records either demo account:
>
> | Take | Command | Starts as | Ends as |
> |---|---|---|---|
> | **Hatch** (Week 1 reel) | `scripts/record_reel.sh <udid> reel-hatch.mp4 hatch` | new egg, 19,400 lbs | Hatchling |
> | **Evolve** (Week 4 reel) | `scripts/record_reel.sh <udid> reel-evolve.mp4 evolve` | fledgling, 97,400 lbs | Mature |
>
> The shot list below is the same for both; swap the text where marked. Use the
> **hatch** take for Week 1 ("the egg stirs" in `calendar.md`) and save the
> **evolve** take for Week 4.

## What the footage already contains (script order)

| Raw step | What's on screen | Script pause |
|---|---|---|
| 1 | Home: the fledgling, "Log Workout" | 3.5 s |
| 2 | Log Workout sheet: title "Leg Day", types "dead", picks *Barbell Deadlift* | ~3 s |
| 3 | Three sets of 185 lbs × 5, each ticked off | ~7 s |
| 4 | **Finish Workout → full-screen evolution to Mature** | 5 s hold |
| 5 | "Keep going" → Progress tab → the new workout expands | ~8 s |

Total raw ≈ 45 s. Login is in the first seconds of the take; cut it.

## Shot list (final cut)

| # | Time | Picture | On-screen text | Notes |
|---|---|---|---|---|
| 1 | 0:00–0:02 | Home, the egg (evolve take: the fledgling), slow push-in | **One workout.** | Hook. Hold on the dragon, not the UI. |
| 2 | 0:02–0:05 | Tap *Log Workout*; title "Leg Day" typed | **Log a lift.** | Speed up typing 1.5×. |
| 3 | 0:05–0:09 | "dead" → *Barbell Deadlift* suggestion appears and is tapped | Quick search | Shows the exercise catalog. |
| 4 | 0:09–0:14 | Three sets filled 185 × 5, checkmarks land one by one | **Tick off your sets.** | Cut between sets to keep it moving. |
| 5 | 0:14–0:15 | Tap *Finish Workout* | | Hard cut on the tap. |
| 6 | 0:15–0:21 | **Celebration:** the new dragon lands ("You reached Hatchling"; evolve take: Mature) | **Your dragon hatched.** (evolve take: **Your dragon evolved.**) | Hold the full 5 s. This is the cover frame and the payoff. Slight zoom in. |
| 7 | 0:21–0:24 | Progress tab, the workout card expands | **Every set counts.** | Optional; cut if over 25 s. |
| 8 | 0:24–0:26 | End card: egg on cream (reuse `assets/` style) | **Forge · private beta · iPhone** / **Request an invite — link in bio** | Brand colours; 2 s is enough. |

Text style: Avenir Next Bold, charcoal `#2c3e50` on a cream `#f5f1e8` pill, or
cream on dark footage — whichever reads. Keep text out of the top 250 px and
bottom 340 px, where Instagram's UI covers it.

## First cut (automated)

`python3 campaign/edit_reel.py` turns `footage/reel-hatch-raw.mp4` into
`footage/reel-hatch-cut.mp4`: 1080×1920, 30 fps, ~25 s, silent, with the
speed-ups, cream background, rounded phone frame, caption pills, "Demo account"
tag and the end card. The segment times at the top of the script are read off a
specific take, so re-check them against `footage/reel-hatch-30fps.mp4` after any
re-recording. Add music or audio in Instagram, then use the caption below.

## Run the recording

```bash
# Developer Mode must be on (DevToolsSecurity -status), or UI automation stalls.
xcrun simctl list devices booted         # get the simulator UDID
cd ~/git_repos/forge
scripts/record_reel.sh <udid> reel-hatch.mp4 hatch    # or: evolve
```

Pre-flight:
- Use a recent iPhone simulator in **light mode**, network on (dragon art loads from the CDN).
- The script overrides the status bar to 9:41, full battery and signal.
- It uninstalls the app first so the demo starts clean.
- Check the raw clip: the login screen should only be in the first seconds,
  and the keyboard should never cover the set fields.

## Edit

1. Trim login; cut to the shot list; ease speed-ups on typing only.
2. The simulator is taller than 9:16: scale to fit the width and put a flat
   cream (`#f5f1e8`) background behind, or crop the status bar area. No gradients,
   per the brand style.
3. Add the text overlays above. Add **"Demo account"** in small text in the
   corner — the numbers are fixtures, not a real user's lifting.
4. Audio: Instagram's music library is limited for business accounts (commercial
   use). Use a library track marked as available for business, or no music.
5. Export 1080×1920, 30 fps, under 90 s (this is ~25 s).

## Post

- **Cover:** frame from shot 6 (the new dragon), with the title safe-area in view.
- **Caption:** *Log a set. Tick it off. Watch your egg hatch. 🐉 Every workout feeds your dragon, and the first one starts it all. Private beta for iPhone: request an invite, link in bio.* (Evolve take: "…This is what 100,000 lbs looks like, one workout at a time.")
- **Alt text:** "A screen recording of the Forge app: a workout is logged and the dragon egg hatches (evolve take: the dragon grows to its mature form)."
- **Hashtags** (5–8): #strengthtrainingforwomen #womenwholift #liftingover40 #gamifiedfitness #indieapp #betatesters
- **Link/label:** bio link `?src=instagram-bio` (swap to `?src=ig-reel-evolve` while the reel is fresh, then change back).
- **Story follow-up the same day:** share the reel + the invite frame
  (`assets/story/request-invite.png`) with a link sticker → `?src=instagram-story`.

## Don't

- Don't show the login or "Dev login (skip Apple)" screen.
- Don't imply the lifting numbers belong to a real person — keep "Demo account" visible.
- Don't claim fitness outcomes; the reel shows a game mechanic, nothing more.
