# Identity API — External Integration

SportSyncAI is a closed-core service: the scoring methodology, internal taxonomy, and reasoning process are private. Partners integrate through this documented API surface only — two endpoints, described in full below. Nothing beyond what's documented here is ever exposed.

`GET /api/v1/integrate/questions` · `POST /api/v1/integrate/identity`

Send structured answers about a person. Get back a synthesized identity read. Nothing else.

## What it does

Runs a set of answers through SportSyncAI's identity engine and returns a category, an identity label, and a short narrative. You receive the result, not the mechanism.

## Question catalog

`GET /api/v1/integrate/questions` — no API key required.

Returns the question set you can ask your own users, so you know which `question_key` and `answer_text` values are valid for the request below. Never includes scoring internals — only question and option text.

```json
{
  "success": true,
  "questions": [
    {
      "key": "q1",
      "question_en": "You're facing a challenge, and the reward is the same either way. Which do you choose?",
      "question_ar": "قدامك تحدي، والجائزة نفس الشيء. أي تحدي تختار؟",
      "options": [
        {"text_en": "A mental puzzle — I beat it with thinking alone", "text_ar": "لغز أو تحدي ذهني — أتغلب عليه بالتفكير فقط"},
        {"text_en": "A real, scary challenge — heights, speed, genuine danger", "text_ar": "تحدي حقيقي مخيف — مرتفعات، سرعة، خطر حقيقي"}
      ]
    }
  ]
}
```

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
    {"question_key": "q1", "answer_text": "A real, scary challenge — heights, speed, genuine danger"},
    {"question_key": "q2", "answer_text": "With friends"}
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

```bash
curl -X POST https://sportsyncai.site/api/v1/integrate/identity \
  -H "X-API-Key: ssai_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {"question_key": "q1", "answer_text": "A real, scary challenge — heights, speed, genuine danger"}
    ],
    "language": "en"
  }'
```
