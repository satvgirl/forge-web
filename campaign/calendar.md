# 4-week content calendar

Three feed posts a week plus stories. Voice is the dragon: warm, direct, no
shame. **CTA on every post:** "Private beta, iPhone only. Request an invite —
link in bio." Images marked ✅ already exist in `assets/`; reels need
screen footage (`scripts/record_reel.sh` in the app repo).

Suggested hashtags (use 5–8 per post, rotate): #strengthtrainingforwomen
#womenwholift #liftingover40 #strongover40 #midlifefitness #gamifiedfitness
#habittracker #indieapp #betatesters

---

## Week 1 — Meet the dragon

**Tue · Reel: "Your workouts hatch a dragon"** (15–20s)
- Footage: the scripted reel — log a set, the egg stirs, the dragon evolves. Text on screen: "Log a lift." / "Watch it grow." / "That's Forge."
- Caption: *Every set you log feeds a dragon. It starts as an egg. It doesn't get impatient. 🐉 Private beta for iPhone — request an invite, link in bio.*
- Link/label: bio (`ig-reel-hatch` if you swap it)

**Thu · Carousel: "Four stages"** ✅ `assets/carousel-four-stages/` (6 slides)
- Caption: *Egg → Hatchling → Fledgling → Mature. It grows with your lifetime lifting: 20,000 lbs to hatch, 50,000 to find its stride, 100,000 to take command. No rush. It's a long game, and so is strength. Which stage would you like to meet first? 👇*
- CTA: link in bio.

**Sat · Single: "No leaderboards. No shame."** ✅ `assets/single/no-leaderboards-no-shame.png`
- Caption: *No leaderboards. No streak-shaming. No one to compare yourself to but you. Just your progress, made visible. Request an invite — link in bio.*

**Stories (2–3):** (1) poll "Which dragon colour would you pick?" copper / sage / gold / charcoal; (2) behind the scenes: the hatchling art; (3) ✅ `assets/story/request-invite.png` with a link sticker → `?src=instagram-story`.

---

## Week 2 — Strength, kindly

**Tue · Carousel: "Your dragon notices how you show up"** ✅ `assets/carousel-moods/` (5 slides)
- Caption: *Gentle, balanced, fierce. Your dragon's mood follows how many days you trained in the last week: fewer than two, it rests with you; two or three, it's steady; four or more, it's on a roll. And when life gets in the way, it just waits. No guilt, no lecture.*

**Thu · Reel: "A rest week isn't failure"** (10–15s)
- Footage ✅ record with `scripts/record_reel.sh <udid> out.mp4 rest` (app repo), cut with `python3 campaign/edit_reel.py rest` → `footage/reel-rest-cut.mp4` (~15 s, captions: "A quiet week." / "Your dragon rests with you." / "No guilt. No lecture." / "Come back when you're ready." + end card). The app has no rest-week message, so keep the wording to what the gentle mood actually does.
- Caption: *Missed a week? Your dragon didn't notice, or at least didn't mind. Come back when you're ready. 🌿*

**Sat · Single: "Pick your dragon"** ✅ `assets/single/pick-your-dragon.png` (2×2 of the four colours)
- Caption: *Copper, sage, gold or charcoal. Which one's yours? Tell me below. In Forge you pick at the start, and it's yours.*

**Stories:** poll results from week 1; a question box "What would make you stick with strength training?" (real insight for the app).

---

## Week 3 — Inside the beta

**Tue · Reel: "Log a set in seconds"** (15s)
- Footage: start a workout from a template, tick off sets, switch an exercise to kg.
- Caption: *Same simple logging you'd do on paper, only faster. Templates for your usual days, pounds or kilograms per exercise. Private beta, iPhone — link in bio.*

**Thu · Carousel: "What's new in the beta"** — make screenshots of: kg/lbs menu, share card, CSV export, post-workout card.
- Caption: *Fresh in the beta: kilograms or pounds (even mixed in one workout), a card to share your dragon, and export of all your data to a spreadsheet. Your data is yours. No ads, no third-party tracking.*

**Sat · Single or story-to-post: "Beta notes"** — a genuine tester quote (ask permission) or a "you asked, we built" note from the question box.
- Caption: *You said it. We built it. Keep it coming.*

**Stories:** the share card as a story; "this or that" poll on feature ideas.

---

## Week 4 — The invitation

**Tue · Reel: "The moment it evolves"** (10–15s)
- Footage: the full-screen evolution celebration (debug session `Long-press dragon` triggers it for recording only).
- Caption: *100,000 lbs, lifted a set at a time. This is the moment it all adds up. 🐉*

**Thu · Carousel: "How to join the beta"** ✅ `assets/carousel-how-to-join/` (6 slides: request an invite → TestFlight invite → hatch your egg → what to expect → link in bio).
- Caption: *We're looking for early testers on iPhone. Three steps, no payment. You'll shape what Forge becomes.*

**Sat · Single: "Built by one person"** — the egg + "Made in Ontario by one person. No ads. No tracking."
- Caption: *Forge is one person's project, not a company's. If you want strength training to feel kinder, come help build it.*

**Stories:** countdown or "last call" for the current invite batch; recap of the month's best questions.

---

## After week 4

Review which format and which hook got the most link taps (not likes), keep
the top two formats, and drop the rest. Re-check `?src=` counts before
deciding whether to spend money on ads (don't, until the invite flow is
smooth and at least one organic post is clearly converting).
