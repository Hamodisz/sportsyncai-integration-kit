# Beyond identity: the compatibility direction

**Places and People are now live systems** — see the [API reference](API_REFERENCE.md). Experiences is still a direction, not a capability. This page exists so a partner evaluating the
[Identity API](API_REFERENCE.md) can see where the underlying signal is headed
and plan accordingly — the same reason [What the Identity API
enables](WHAT_IT_ENABLES.md) publishes its "honest boundaries" table instead of
staying silent about gaps.

---

## The question one step past identity

The Identity API answers *who someone is* — a category, a named identity, a
narrative. The natural next question is *who or what they fit with*. That
question splits into three directions:

```
             IDENTITY  (what this API returns today)
                 │
                 ▼
          COMPATIBILITY  (the direction below)
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
   PEOPLE      PLACES     EXPERIENCES
  training    venues,      events,
  partners,   groups,     activities,
  collabs,   communities   adventures
  networking
```

All three would draw on the same identity read this API already returns —
they are not three separate systems bolted together, they are the same
signal pointed at three different questions. That is a direction, not a
promise of a date.

---

## Where each direction actually stands today

| Direction | Status today | What that means for you |
|---|---|---|
| **Places** — venues, groups, communities | Live: `GET /api/v1/integrate/places`. | Real venues and groups for a sport in a city, without contacts. |
| **People** — training partners | Live: `/api/v1/integrate/people/…`, within your own users, same gender only, opt-in per user. | Your users who agreed to be matched can find each other. |
| **Experiences** — events, activities, adventures | Concept stage. | Named here for completeness, not availability. |

---

## Why People is a different kind of problem than Places or Experiences

Worth stating plainly, because it changes what "done" would even mean: matching
a person to a venue or an event only requires their consent. Matching a person
to *another person* requires both sides to agree before either one is
revealed to the other — otherwise it isn't matching, it's one person being
served up to a stranger without a say in it. In the live People system, a user is only shown when you set `matching: true`
for them — set it only for users who agreed — and either side can block the other. Mentioned here so it's clear this isn't being treated as a
smaller version of the same problem.

---

## If this is relevant to you

If any of these three directions is the actual reason you're evaluating the
Identity API — say so when you [request a
key](../README.md#getting-a-key). It's a more useful conversation to have
before integrating than to have after.
