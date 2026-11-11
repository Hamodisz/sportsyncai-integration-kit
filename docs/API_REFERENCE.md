# Partner API — Reference

Public developer integration documentation. SportSyncAI's core implementation and intelligence remain proprietary — the scoring methodology, internal taxonomy, and reasoning process are private. Developers integrate through this documented API surface only: the systems described in full below. Nothing beyond what's documented here is ever exposed.

Systems: question catalog · identity · body reading · sport map · places · people · delete a user · usage.

Each system takes your user's data in and gives back its read. You receive the read, not the mechanism, and never any code.

## Question catalog

`GET /api/v1/integrate/questions` — no API key required.

Returns the question set you can ask your own users, so you know which `question_key` and `answer_text` values are valid for the request below. Never includes scoring internals — only question and option text.

The catalog currently returns 34 questions. Full guide: [sportsyncai.site/developers](https://sportsyncai.site/developers). Abbreviated response (real values, `q1` shown with all 5 of its options):

```json
{
  "success": true,
  "questions": [
    {
      "key": "q1",
      "question_en": "You've got a challenge in front of you, and the prize is the same no matter what you pick. Which one do you choose?",
      "question_ar": "عندك تحدي قدامك، والجايزة نفسها مهما اخترت. أي تحدي بتختار؟",
      "options": [
        {"text_en": "A mental puzzle — I solve it just by thinking", "text_ar": "لغز أو تحدي ذهني، أحله بالتفكير بس"},
        {"text_en": "A scary challenge, for real — heights, speed, real danger", "text_ar": "تحدي مخيف بصراحة — مرتفعات، سرعة، خطر حقيقي"},
        {"text_en": "A physical challenge — body against body, strength and speed", "text_ar": "تحدي بدني — جسد ضد جسد، قوة وسرعة"},
        {"text_en": "Whatever my friends pick — being together matters more", "text_ar": "اللي يختاره أصحابي — المهم نكون مع بعض"},
        {"text_en": "Depends on the moment — sometimes I think it through, sometimes I want the real thrill", "text_ar": "يعتمد على الموقف، أحياناً أفكر وأحياناً أبي إثارة حقيقية"}
      ]
    }
  ]
}
```

**`answer_text` must match an option's text exactly** as returned by this endpoint. Don't retype or paraphrase it — copy the string through from the catalog response, or you'll get `unrecognized_answers`. Always fetch the catalog rather than hardcoding these values; the wording can change.

## Authentication

Send your API key in the `X-API-Key` header. Keys are issued individually — email **partners@sportsyncai.site** to request one.

```
X-API-Key: ssai_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

This is a separate credential from any SportSyncAI end-user login — it identifies your integration, not a person.

## Request

```
POST /api/v1/integrate/identity
X-API-Key: <your key>
Content-Type: application/json

{
  "answers": [
    {"question_key": "q1", "answer_text": "A scary challenge, for real — heights, speed, real danger"},
    {"question_key": "q2", "answer_text": "Deep in thought, solving a problem no one else could figure out"}
  ],
  "language": "en"
}
```

- `answers` — required, non-empty. Each entry is `question_key` and `answer_text` — both taken from `GET /api/v1/integrate/questions` above.
- `language` — optional, `"en"` or `"ar"`. Defaults to `"en"`.
- `user_id` — optional. Your own id for this user (letters, digits, `_`, `-`, up to 64). When sent, we keep the answers under your account so body reading, sport map and people can use them without you sending them again. Never send an email or phone number as the id (`400 invalid_user_id`).
- Maximum 50 answers per request. Maximum request size 20KB.
- Rate limit: 30 requests per minute per API key.

## Response

`{"success": true, "category", "category_secondary", "identity", "narrative"}`

- `category` — one of `physical`, `adrenaline`, `mental`.
- `category_secondary` — a second category if the read is a genuine blend, otherwise `null`.
- `identity` — a short identity label.
- `narrative` — one to two sentences describing it.

There is no confidence score in this version — we'd rather omit one than return a number we can't stand behind.

## Errors

All errors return `{"success": false, "error": "<code>"}` with an appropriate HTTP status.

Checks run in this order: **API key → rate limit → request size → JSON parsing → answer validation.** The first failure is what you get back — so a request with both a bad key and a malformed body returns `401 invalid_api_key`, not `400 invalid_json`. Fix authentication first when debugging.

| Status | `error` | Meaning |
|---|---|---|
| 401 | `invalid_api_key` | Missing, wrong, or deactivated API key |
| 400 | `missing_answers` | `answers` was empty or absent |
| 400 | `malformed_answers` | Nothing in `answers` was a usable `{question_key, answer_text}` pair |
| 400 | `unrecognized_answers` | None of the submitted answers matched a real question/option |
| 400 | `too_many_answers` | More than 50 answers submitted |
| 400 | `invalid_json` | Request body wasn't valid JSON |
| 413 | `request_too_large` | Body exceeded 20KB |
| 429 | `rate_limited` | Too many requests this minute — see the `message` field for the current limit |

## Minimal example

Fetch the catalog (no key needed):

```bash
curl https://sportsyncai.site/api/v1/integrate/questions
```

Then send an answer (`answer_text` copied exactly from that response):

```bash
curl -X POST https://sportsyncai.site/api/v1/integrate/identity \
  -H "X-API-Key: ssai_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {"question_key": "q1", "answer_text": "A scary challenge, for real — heights, speed, real danger"}
    ],
    "language": "en"
  }'
```


---

# The other systems

Same rules as identity: `X-API-Key` on every call, the same rate limit (30 requests per minute per key, shared across all systems), and errors as `{"success": false, "error": "<code>"}`. The days-based systems accept bodies up to 1 MB; everything else 20KB.

`user_id` is your own id for the user: letters, digits, `_` and `-`, up to 64 characters. Data is kept per partner — the same `user_id` sent by two partners is two different people.

## Watch days (input format)

Used by body reading, sport map and people. Up to 14 days per call; each date once. Days you sent before are kept (up to 365 days) and the newest 14 are read together.

| Field | Required | Meaning |
|---|---|---|
| `date` | yes | `YYYY-MM-DD` |
| `sleep` | no | hours slept, 0–24 |
| `sleep_mid_min` | no | minutes from the previous noon to the middle of the night's sleep, 0–1440 |
| `move_center_min` | no | the step-weighted minute of the day the user moved (minutes from midnight), 0–1440 |
| `resting_hr` | no | resting heart rate, 20–250 |
| `steps` | no | steps that day, 0–200000 |
| `context` | no | what kind of day it was: `work`, `off_day`, `personal`, `physical`, `excitement`, `sick`, `private`. `personal`, `sick` and `private` days are left out of the read. |
| `hr_by_minute` | no | up to 1440 heart-rate values, one per minute from midnight (`null` for no reading) |
| `steps_by_minute` | no | up to 1440 step counts, one per minute from midnight |

Day errors (400): `missing_days`, `too_many_days`, `malformed_days`, `invalid_user_id`.

## Body reading

`POST /api/v1/integrate/body-reading` — body `{"user_id", "days", "answers"?, "language"?}`

Reads how the user actually lives from the watch, in words.

Response fields:
- `ready` — whether there is enough data for a read.
- `days_used` — how many days went into the read.
- `confidence` — `initial`, `early`, `building`, `solid`, or `null`.
- `traits` — list of `{trait, lean}`: the trait name and which way this user leans, in words.
- `facts` — the middle value of your own data: `resting_hr`, `sleep_hours`, `steps`, `sleep_midpoint`.
- `disagrees_with_answers` — only when answers are known: the traits where the body says something different from the answers.

## Sport map

`POST /api/v1/integrate/sport-map` — body `{"user_id", "answers"?, "days"?, "language"?}`

Maps the user to up to three sports — one per world — that run on the same drivers. It is a map, not a ranking: the entry with `"yours": true` is the user's own world, the others are other doors into the same room.

Response fields: `world`, `map` (list of `{world, sport, yours}`), `based_on` (`answers`, `watch`). When there is not enough to map, `map` is empty and `reason` is `need_answers_or_more_traits`.

Errors: `400 missing_input` (no answers and no days, sent or stored).

## Places

`GET /api/v1/integrate/places?sport=<sport>&city=<city>&language=en|ar`

Real venues and groups for one sport in one city, from SportSyncAI's own places data.

Response fields: `sport`, `city`, `count`, `places` (each: `kind` (`venue` or `community`), `id`, `name`, `sport`, `district`, `rating`, `rating_count`, `gender_category`, `world`, and `beginner_friendly` for groups), `browse_url` (where your user can see contacts and booking on sportsyncai.site). Contact details, booking links and coordinates are never returned.

Errors: `400 missing_sport_or_city`, `400 unknown_sport`, `400 unknown_city`, `503 places_unavailable` (with `"retryable": true` — try again later; not counted).

## People

Matches **your own users** with each other. Never with another partner's users, never with SportSyncAI's own users. **Men are matched only with men and women only with women** — enforced on our side; a user with no gender is never matched.

- `PUT /api/v1/integrate/people/{user_id}` — body `{"gender": "male"|"female", "matching": true|false, "answers"?, "days"?, "interests"? (up to 10, 30 characters each), "city"? (40 characters)}`. Set `matching: true` only for users who agreed to be shown to other users. Response: `user_id`, `matching`, `world`, `sports`. Errors: `400 invalid_gender`, `400 gender_required` (matching on without a gender).
- `GET /api/v1/integrate/people/{user_id}/matches` — up to 30 users. Each: `user_id`, `world`, `sports`, `interests`, `city`, `in_common`, `plays_alike` (one line, in words). Trait values are never returned. Errors: `404 not_found`, `400 matching_off`.
- `POST /api/v1/integrate/people/{user_id}/block/{other_id}` — the two never see each other again. Response: `user_id`, `blocked`.

## Delete a user

`DELETE /api/v1/integrate/users/{user_id}` — erases every answer, watch day, people profile and block stored for that user under your account. Response: `user_id`, `deleted`. Free.

## Usage

`GET /api/v1/integrate/usage?month=YYYYMM` (defaults to this month, UTC) — your successful calls per system: `month`, `calls` (per system), `total_calls`, `price_per_call_usd`, `amount_usd`. Free. Error: `400 invalid_month`.

## Billing

Each successful call (HTTP 200) to identity, body reading, sport map, places or people is counted once. Errors, `usage` and `delete` are not counted. Prices are agreed per partner; until yours are set, `price_per_call_usd` is `"not_set"` and `amount_usd` is `null`.
