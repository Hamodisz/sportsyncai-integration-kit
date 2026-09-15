# What the Identity API enables

The [API reference](API_REFERENCE.md) describes *how* to call the service. This
page describes *what it does for your business* once it's wired in.

One sentence: **you send structured answers about a person and get back who they
are in sport — an identity, not a score — so your product can route them to the
right thing the first time.**

---

## The problem it removes

Most sports and fitness products ask people what they *want*. Preference is a
weak predictor. Someone can genuinely enjoy an activity and still stop doing it,
because the environment doesn't fit how they're built — they need structure and
the format is loose, they need solitude and the format is social, they need real
stakes and the format is comfortable.

That mismatch shows up in your metrics as churn, low activation, and a
cross-sell offer nobody accepts. It doesn't look like a matching problem — it
looks like a motivation problem — so it usually gets addressed with reminders
and discounts, which don't fix it.

The Identity API gives you the missing variable: **the kind of environment this
specific person stays in.**

---

## What you can build with it

Each of these uses only what the API already returns — `category`,
`category_secondary`, `identity`, `narrative`.

### Onboarding that isn't cold
A new signup is an anonymous row until they do something. Ask a handful of
questions during signup, call the API once, and the account starts with a real
identity attached — a named type and a short narrative you can show back to
them. The first screen after signup can be specific instead of generic.

### Routing across a multi-activity catalogue
If you sell more than one thing — a chain with several formats, a marketplace, a
booking platform, a club with multiple programmes — the identity tells you which
part of your own catalogue to put in front of this person. You already have the
inventory; this decides the order.

### Retention interventions aimed at the real cause
When someone lapses, the identity distinguishes "wrong activity for them" from
"right activity, life got busy." Those need opposite responses. Today most
systems can't tell them apart, so they send the same nudge to both.

### Segmentation that isn't demographics
`category` and `identity` are behavioural, not demographic. They give you
message and offer segments that correspond to how people actually behave, which
is usually a better split than age or location.

### A differentiator you don't have to build
The behavioural modelling behind the result is years of work and is not
something you'd spin up to ship one feature. You integrate the outcome of it
over HTTPS and keep your roadmap on your own product.

---

## What you are NOT taking on

This matters as much as the capability:

- **No ML team, no data pipeline, no model to maintain.** One HTTPS call. The
  methodology stays on our side and improves without you redeploying anything.
- **No hardware or app-architecture change.** It's a request and a response.
- **No data custody burden from us.** The identity endpoint is stateless — it
  creates no account, stores no end-user record, and returns no identifier that
  tracks a person. Your users stay yours.
- **No lock-in through your data.** You keep every input you collected and every
  result you received.

---

## Honest boundaries

Things this API does **not** do today, stated plainly so you can plan around
them rather than discover them mid-integration:

| Not included | What that means for you |
|---|---|
| Wearable / health-platform ingestion | The API reads the answers you send. It does not connect to a device stream. |
| Booking or transactions | It returns an identity. Acting on it happens in your product. |
| A learning loop from your outcomes | Results do not currently get better from the outcomes your users produce. |
| User accounts or auth for your users | Your API key identifies *your integration*, never an individual person. |
| Venue or facility data | Not part of this endpoint. |

If a roadmap item above is the reason you're evaluating this, say so when you
request a key — it's a different conversation, and a more useful one than
discovering the gap in week three.

---

## What a first integration usually looks like

1. Call `GET /api/v1/integrate/questions` and render the questions in your own
   UI, with your own styling. There is no SportSyncAI branding in the response.
2. Send the answers to `POST /api/v1/integrate/identity` from your backend.
3. Store `category` / `identity` / `narrative` on your own user record.
4. Use it to decide what that person sees next.

Steps 1–3 are a day of work; the [runnable example](../examples/example.py) is
about fifty lines. Step 4 is where the value is, and it's entirely yours to
design — you know your catalogue and your funnel better than we do.

---

## Commercial terms

Deliberately not published here. Terms depend on volume, category and market,
and are agreed per partner — email **partners@sportsyncai.site** and we'll walk
through what fits your integration.

No open-source license is granted; SportSyncAI's implementation and
intelligence remain proprietary.
