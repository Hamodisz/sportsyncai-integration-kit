# Identity API — External Integration

Public developer integration documentation. SportSyncAI's core implementation and intelligence remain proprietary — the scoring methodology, internal taxonomy, and reasoning process are private. Developers integrate through this documented API surface only: two endpoints, described in full below. Nothing beyond what's documented here is ever exposed.

`GET /api/v1/integrate/questions` · `POST /api/v1/integrate/identity`

Send structured answers about a person. Get back a synthesized identity read. Nothing else.

## What it does

Runs a set of answers through SportSyncAI's identity engine and returns a category, an identity label, and a short narrative. You receive the result, not the mechanism.

## Question catalog

`GET /api/v1/integrate/questions` — no API key required.

Returns the question set you can ask your own users, so you know which `question_key` and `answer_text` values are valid for the request below. Never includes scoring internals — only question and option text.

The catalog currently returns 31 questions. Abbreviated response (real values, `q1` shown with all 5 of its options):

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

Send your API key in the `X-API-Key` header. Keys are issued individually — contact SportSyncAI to get one.

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
- Maximum 50 answers per request. Maximum request size 20KB.
- Rate limit: 30 requests per minute per API key.

## Response

```json
{
  "success": true,
  "category": "adrenaline",
  "category_secondary": null,
  "identity": "The Edge-Seeker",
  "narrative": "Calm bores you. You come alive at the edge — where the stakes are real and most people step back."
}
```

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
