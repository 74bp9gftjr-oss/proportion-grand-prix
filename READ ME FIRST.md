# Proportion Grand Prix — the two-minute version

## If you just want them playing on their own

Send them **`Proportion Grand Prix.html`**. They open it, they play. Nothing else needed,
works offline. They get a five-race championship across all five circuits.

*(Tell them to **download/save it first, then open it** — tapping it inside Teams, Drive or
Mail only shows a preview, which looks blank.)*

---

## If you want them racing each other

### You need ONE thing open

Double-click **`Start Race Server.command`**.

A black window opens. **Leave it open for the whole lesson.** That window *is* the race.
Close it and everyone is dropped.

That's it. Nothing else. Don't open the game file yourself — use the link below like
everyone else.

### The link to send them

```
http://MacBook-Air-2.local:8000
```

This is your Mac's name, so **it stays the same every lesson**. Safe to put in ClassDojo
or your VLE once and reuse.

If a device can't open that name, the black window also prints a numbers version like
`http://192.168.1.92:8000`. That one **changes every lesson**, so only read it off the
window, never from a note.

### Then, in the game

1. One person taps **New room** and reads out the 4-letter code.
2. Everyone else types that code and taps **Join room**.
3. When everyone's on the grid, the host picks circuit/laps/fuel and taps **Start race**.

Everyone must be on the **same wi-fi** as your Mac. Up to 32 in a room.

---

## When it goes wrong

| What you see | What it means |
|---|---|
| "Refused to connect" / ERR_CONNECTION_REFUSED | The black window isn't open. Start it again. |
| The page never loads at all | Phone is on mobile data or a different wi-fi. |
| `DEVICES CONNECTED: 0` stays at 0 | Nothing is reaching your Mac — check the address and the wi-fi. |
| Works at home, not at school | School wi-fi is blocking devices from talking to each other. Use the single-file version instead. |

The black window prints **`DEVICES CONNECTED:`** as each device arrives — that tells you
instantly whether they're getting through.

**Before a lesson**: start the server and load the link on one phone. If the counter goes
to 1, you're fine.

---

Full detail is in `Teacher notes.md`.
