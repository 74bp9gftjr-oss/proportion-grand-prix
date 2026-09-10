# Proportion Grand Prix — teacher notes

**Year 8 · Autumn · Block 2 — Proportion and scale**

A kart race where the fuel comes from maths. Drive, pit, answer, pick a weapon, race on.

---

## The four files

| File | What it is |
|---|---|
| `Proportion Grand Prix.html` | The whole game. One file, no installs, works offline. |
| `race_server.py` | Lets the class race each other in one room. |
| `Start Race Server.command` | Double-click this to run the server on a Mac. |
| `Stop Race Server.command` | Double-click to stop a server you left running. |
| `Teacher notes.md` | This file. |

---

## Quick start: 8 students racing each other

1. Double-click **Start Race Server.command**. A black window opens, prints an address
   like `http://192.168.1.92:8000`, and opens that page in your browser.

   > **Leave that window open for the whole lesson.** It *is* the race server. If you
   > close it, everyone is dropped and the address stops working. If a browser says
   > *"refused to connect"* or *ERR_CONNECTION_REFUSED*, that almost always means this
   > window is not open. Double-click the launcher again.

2. **Write that address on the board.** It is different every lesson — always read it off
   the black window, never from a note.
3. Each student gets there one of two ways, whichever is easier:
   - type the address straight into Safari or Chrome; **or**
   - open the game file they already have and type the address into the
     **Play with your class** box, then tap **Go to the class race**.
4. One person (you, or a student) taps **New room** and reads out the 4-letter code.
   Everyone else types that code and taps **Join room**.
5. Watch the grid fill up. When all 9 of you are listed, the host picks circuit, laps and
   fuel, then taps **Start race**.

The black window prints a live **`DEVICES CONNECTED:`** count. If a student's phone will
not join, that line tells you whether they are reaching your Mac at all — see
*If a phone will not connect* below.

Everyone must be on the **same wi-fi**, and the black window must stay open.

---

## Sending it to students

`Proportion Grand Prix.html` is **one self-contained file**. No fonts, no libraries, no
internet, nothing to install. Send that single file, they open it, they play. Everything
below is optional.

**The one catch is how it gets opened.** Most places you might send it from will *preview*
an HTML file rather than run it, and a preview shows a blank page. Tell students to
**download or save the file first, then open it** — not to tap it inside the app.

| How you send it | What to tell them |
|---|---|
| School VLE / shared drive | "Download it, then open the downloaded file." Best option. |
| Email | Some mail systems strip `.html` attachments. If it does not arrive, zip it or use the VLE. |
| Teams / Google Drive / OneDrive | Tapping it previews it. They must press **Download** first. |
| AirDrop to an iPad | Choose to open it in **Safari** (or save to Files, then tap it there). |
| USB stick | Just double-click it. |

Once it is open they can use it offline forever — on a plane, with wi-fi off, anywhere.

**On an iPad or phone, hold the device sideways.** The game says so if you do not.

If a pupil's browser blocks storage for local files, the game still runs perfectly — it
just forgets their name, kart design and coins when they close it. Nothing breaks.

---

## Running it

The class race needs the server below; solo does not. Students who open the file on their
own get a **Play with your class** box where they can type your address — so the one file
covers both cases.

> **If you do want a class race:** double-clicking the HTML opens a **solo-only** copy, so
> there is nothing for other devices to connect to. For a class race **nobody opens the
> file, including you.** Everyone goes to the web address the server prints. The
> class-race panel only appears when the page is actually being served, so students who
> just open the file never see anything they cannot use.

### Solo — zero setup

Send students the HTML file or put it on the shared drive. They double-click it and get
two choices:

- **Solo Grand Prix** — a five-race championship, one race on each circuit, against the
  same five rivals throughout, with points (10-8-6-4-3-2) and a running table after every
  race. About fifteen minutes end to end.
- **Or just one circuit** — pick any of the five and race it on its own.

Everything works offline — questions, fuel, weapons, ramps, coins, the shop.

### Class race — up to 32 in one room

1. Double-click **Start Race Server.command**. A black window opens, prints an address
   like `http://192.168.1.24:8000`, and **opens that page in your own browser for you**.
   That browser tab is the one you race in.
2. Put the address on the board. Students type it into Safari or Chrome. They must be on
   the **same wi-fi** as your computer. Nothing leaves the school network.

   > **The address is not the same every lesson.** It changes whenever the Mac rejoins
   > wi-fi — it was `192.168.1.13` this morning and `192.168.1.92` this afternoon. Always
   > read it off the black window, never from a note or from memory. Typing yesterday's
   > address is the most common reason a phone "cannot connect".
3. One person taps **New room** and reads out the 4-letter code; everyone else types it
   and taps **Join room**.
4. The host picks circuit, laps, fuel and topics, then **Start race**. Fewer than six
   humans and CPU karts fill the grid.

Positions are merged and broadcast ten times a second rather than passed player-to-player,
which is what makes 32 devices possible. Measured with 30 clients: about 33 KB/s to each
device, 1 MB/s out of your laptop. Fine on normal wi-fi; on an old access point, run two
rooms instead.

**If you end up on the solo-only screen**, it says so, gives you the three steps, and — if
the server is already running on that computer — offers an **Open the class race page**
button that jumps you to the right address.

To stop the server, press `Ctrl+C` in the black window or close it.

### If a phone will not connect

The black window prints a live **`DEVICES CONNECTED:`** count. That one line tells you
which half of the problem you have:

- **"Refused to connect" / ERR_CONNECTION_REFUSED** → the server is not running. That
  error means the Mac was found but nothing was listening. Double-click
  **Start Race Server.command** and leave the window open.
- **The number goes up when the phone loads the page** → the phone is reaching the Mac.
  Any remaining trouble is in the game, not the network.
- **It stays at 0** → the phone is not getting to the Mac at all. In order of likelihood:
  1. The address is stale or mistyped. Re-read it off the window; include `http://` and
     the `:8000` on the end.
  2. The phone is on mobile data, or a different wi-fi (guest vs staff network).
  3. The window was closed — that stops the server.
  4. The wi-fi blocks devices from talking to each other. Many school and guest networks
     do this deliberately. **Test the same phone on your home wi-fi**: if it works there
     and not at school, it is the school network, and no change to the game can fix it —
     you would need the network team to allow it, or use Solo mode instead.

---

## How the maths works

**Fuel is the engine of the whole thing.** The tank does not last a lap, so nobody gets
round without stopping. Five pit pads sit on the shoulder of each lap. Drive onto one and
your kart parks:

- **Right first time** → full tank, choose one of three rewards, **+12 coins**.
- **Wrong** → the option you picked is named and explained, then the worked method, then
  **a new question on the same topic with different numbers**. Keep going until it is
  right; that one pays **+5 coins**.

**The only penalty for a wrong answer is time.** While you are parked everyone else is
racing — the header shows `PARKED 12.4s · 3rd` ticking over and your position slipping.
A pupil who needs three attempts still leaves with a full tank.

Ignore the pits and you run dry, coast to a halt and get a question anyway — but only half
a tank and no reward.

### How much maths per race

Set this with **Fuel tank** in the lobby. Measured over full six-kart races, averaged
across all five circuits:

| Laps | Fuel | Questions each | Winner finishes | Last kart |
|---|---|---|---|---|
| 2 | Steady  | ~3   | 1:51 | 2:34 |
| 2 | **Normal** | **~5** | **2:17** | **2:52** |
| 2 | Thirsty | ~7   | 2:36 | 3:05 |
| 3 | Steady  | ~5   | 2:52 | 3:47 |
| 3 | Normal  | ~7–8 | 3:27 | 4:16 |
| 3 | Thirsty | ~10  | 3:55 | 4:40 |

**2 laps on Normal is the default** — about three minutes and five questions each, which
fits repeated rounds in a lesson. 3 laps + Thirsty gives ten questions for a longer
consolidation run.

### The six topics

All six steps of the block, matching your worksheets. Switch any off in the lobby if you
have only taught the first two.

| Topic | What comes up | The mistake the wrong answers are built from |
|---|---|---|
| Direct proportion | unit cost, boxes, constant speed, recipes, rope | scaling the total instead of finding one first |
| Conversion graphs | read a drawn line both ways, then beyond the axis | reading the graph the wrong way round (Nijah's mistake, L02) |
| Currency | £ ↔ 10 real currencies, and which is better value | dividing when you should multiply |
| Proportion graphs | find *k* from a point, spot the proportional graph | using *a ÷ b* instead of *b ÷ a*; adding instead of multiplying |
| Similar shapes | scale factor, missing side, which one is similar | **adding the difference instead of multiplying** — the big one |
| Metric units | mm/cm/m/km, ml/l, g/kg, two-step, true/false | ×1000 instead of ÷1000 (Mo's mistake, Step 6) |

Every question is generated fresh, so "try a new one" genuinely is a new one and no two
pupils get the same numbers. Answers are four-option multiple choice — **each wrong option
is a specific misconception with its own feedback line**, so a wrong tap tells you
something rather than just costing a mark.

---

## The five circuits

| Circuit | Lap | Road | Hills | Notes |
|---|---|---|---|---|
| Unit Circuit  | 34s | widest | flat | the forgiving one — start here |
| Graph Glen    | 32s | wide   | gentle | fast and flowing |
| Scale Ridge   | 38s | medium | strong | hairpins and climbs |
| Exchange Bay  | 37s | medium | mild | long sweepers |
| Summit Pass   | 36s | tightest | steepest | the hard one |

About five karts fit across the road. Each lap has **5 pit pads, 5 ramps, ~78 coins,
12 magic boxes** and around 20 cones and barrels.

## What is on the track

- **Coins** — trails you can line up and sweep through. They are the other half of the
  economy; the maths pays better.
- **Ramps** — hit one with pace and you take off. In the air you fly straight over cones,
  barrels and oil, so a ramp is an escape as well as a shortcut.
- **Hills** — the road climbs and drops. Climbing costs you speed, dropping gives it back.
- **Magic boxes** — a random weapon, no question asked. The only free items; fuel still
  only ever comes from a pit stop.
- **Boost chevrons** — a free kick of speed for the right line.
- **Cones** (lose two thirds of your speed) and **barrels** (bounce and spin you).
- **Sand traps** on the outside of corners — slower than grass.

## Drifting

Hold **Shift** (or the blue **DRIFT** pad) while turning and the kart slides. Sparks build
white → **blue** → **orange**. Let go and you get a boost: about one second from blue,
nearly two from orange. It is the main skill gap in the game and worth pointing out.

## Coins and the garage

Coins carry over between races and are spent on the results screen. Four upgrades, five
levels each, deliberately small so a pupil who has played more cannot simply out-run one
who has not:

| | Effect per level | Max |
|---|---|---|
| 🔧 Engine | +2% top speed | +10% |
| 🌀 Grip | +3% cornering | +15% |
| ⛽ Tank | +8% fuel | +40% |
| ⚡ Turbo | +10% boost length | +50% |

Upgrades live on that pupil's device only. To reset a class, clear the browser's site data
for the game's address.

## Rewards (choose one per pit stop)

| | |
|---|---|
| ⚡ **Turbo** | 2.6 seconds of extra speed |
| 🎯 **Homing bolt** | stops a rival for 3 seconds |
| 🛢️ **Oil slick** | dropped behind you; spins whoever hits it |
| 🛡️ **Shield** | blocks the next hit |
| ⛽ **Spare can** | a second full tank, saved for later |

---

## Customising the kart

**12 body colours, 6 designs** (plain, stripe, flame, check, spots, bolt) and **8 drivers**.
Everyone in the room sees your choices; they are remembered on that device.

Two settings sit under the garage:

- **View: 3rd person / Top-down.** 3rd person puts the camera behind and above the kart
  looking up the road, with a horizon. Top-down looks straight down at the map. Some
  pupils read one far more easily — let them pick. The minimap works in both.
- **Sound: On / Off.** Engine note that follows your speed, plus hits, crashes, pickups,
  jumps, drift, the countdown and the answer jingles.

---

## What you get back

The results screen shows a **podium for the top three**, then each pupil's **pit stops,
questions answered, percentage right first time, and a bar per topic**. Ask them to read
out their weakest bar — that is your plenary, and it points straight at which worksheet to
revisit.

---

## Controls

- **Computer** — arrows or A/D steer, S or ↓ brakes, **Shift** drifts, **space** fires
  your item. Throttle is automatic. Keys **1–4** answer a question.
- **iPad / phone** — hold it **sideways**. Steering pads bottom left; BRAKE, DRIFT and
  fire bottom right. Tap an answer.

---

## Worth knowing

- **The graph really is the answer.** Conversion-graph questions render a proper labelled
  graph with the read-off drawn on. Pupils should read it, not calculate it.
- **Latecomers** can join the next race — after a race the host taps *Race again*, which
  reopens the room.
- **If the host leaves mid-race**, the CPU karts they were driving stop moving. Human
  racers are unaffected; finish the race and start a new one.
- **The 3rd-person view costs about 1.2 ms a frame** against 0.3 ms for top-down. Both are
  far inside a 60 fps budget, but if an old iPad struggles, switch that pupil to Top-down.
- **Nothing leaves your network.** No accounts, no data collection; names, kart designs,
  coins and upgrades live in that device's own browser storage.

## Checking it works

Open the game, press **F12** (or ⌥⌘I on a Mac) for the console, and type:

```
__QA()
```

It runs 27 checks — 3000 generated questions, every circuit, a full six-kart race on each,
every screen, and the weapon logic — and prints a pass/fail list.

---

*Content follows White Rose Education Y8 Autumn Block 2, Steps 1–6.*
