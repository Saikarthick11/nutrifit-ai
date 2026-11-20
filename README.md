# NutriFit AI

A conversational nutrition and activity journal for **CS 678 Advanced NLP**. NutriFit uses a pretrained Gemini API model to extract structured food, workout, quantity, and date information, asks about missing details, and saves entries only after confirmation. No model training or fine-tuning is used.

## Features

- Meal and workout logging through a multi-turn chatbot, with Pydantic validation.
- Automatic USDA food search, reviewed food matches and portions, and deterministic nutrition calculations.
- Nutrition-label OCR with image validation and user review before saving.
- Corrections to pending and saved entries, including explicit fractional portion changes.
- Saved usual meals, user-defined daily goals, and historical nutrition queries.
- Daily dashboard, weekly comparisons, and an editable journal.
- A separate research view and controlled evaluation runner for rule-based versus LLM extraction, with and without clarification.
- Responsive React and TypeScript frontend; FastAPI and PostgreSQL backend.

This is a **local, single-user research prototype**, not a production service. It has no authentication. Publishing the source does not make it suitable for public hosting. API keys, personal records, databases, and evaluation outputs are not included.

## Architecture

```text
React + TypeScript → FastAPI → Gemini structured extraction
                           → dialogue state and validation
                           → USDA retrieval / reviewed nutrition labels
                           → portion calculation → user confirmation → PostgreSQL
```

Nutrition comes from USDA records or reviewed package labels, not generated nutritional estimates. Unknown nutrient values remain unknown. The selected Gemini model is `gemini-3.5-flash-lite`; configure access through your own API account. The adapter does not silently substitute a different model.

## Local setup

Install Python 3.14 (the tested version), Node.js 22.6 or newer, and Docker Desktop. Start Docker Desktop before starting the database. macOS has been tested; Windows PowerShell commands are also included.

### 1 Clone and configure

```sh
git clone https://github.com/Saikarthick11/nutrifit-ai.git
cd nutrifit-ai
cp .env.example .env
cp backend/.env.example backend/.env
```

In PowerShell, use `Copy-Item` instead of `cp` if needed. If you already have environment files, edit them rather than overwriting them.

- In the root `.env`, replace `POSTGRES_PASSWORD` with your own local database password.
- In `backend/.env`, use the same password in `DATABASE_URL`. The Docker host port is **5433**; PostgreSQL inside the container uses 5432.
- Add your own `GEMINI_API_KEY` and `USDA_API_KEY` to `backend/.env`. Keep credentials on the backend; never use `VITE_` variables for secrets.
- If the password contains URL-reserved characters, URL-encode it in `DATABASE_URL`.

Get API credentials from [Google AI Studio](https://aistudio.google.com/apikey) and [USDA FoodData Central](https://fdc.nal.usda.gov/api-key-signup/). Model availability, quotas, and charges depend on your API account. A chat subscription does not supply an API key.

### 2 Start PostgreSQL

From the project root:

```sh
docker compose up -d --wait db
docker compose ps
```

The backend creates its tables on startup. Docker stores the database in a persistent volume. `docker compose stop db` preserves it; **`docker compose down -v` deletes it**. Changing the environment password after initialization does not change an existing database user's password.

### 3 Start the backend

macOS or Linux, from the project root:

```sh
cd backend
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --reload
```

Windows PowerShell, from the project root:

```powershell
cd backend
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Keep the terminal running. Check [health](http://localhost:8000/health) for `{"status":"ok"}`. Open [API documentation](http://localhost:8000/docs) to explore endpoints. Restart the backend after changing environment settings.

### 4 Start the frontend

In a separate terminal, from the project root:

```sh
cd frontend
npm ci
npm run dev
```

Open [NutriFit](http://localhost:5173). Vite proxies `/api` requests to the local backend. Both services bind locally by default. A phone cannot access the computer through its own `localhost` address.

SQLite is an optional local development backend: set `DATABASE_URL=sqlite:///nutrifit.db`. The normal setup above uses PostgreSQL. Do not commit either database files or database dumps.

## Try the app

1. In Chat, enter `I ate 2 slices of toast and eggs today`.
2. Reply with the egg quantity when asked. Review the suggested USDA foods, preparation, and measured grams or listed serving.
3. Confirm and save. Only confirmed entries affect the journal and totals.
4. For corrections, try `Actually, I ate half of that rice` in a rice draft. For an existing entry, first select **Edit this entry** in My journal.
5. Expand a saved meal and choose **Save as usual meal**, using a name such as `breakfast`. In a new chat, enter `I had my usual breakfast today` and confirm the reused portions.
6. On the dashboard, select **Set goals** to enter your own targets.
7. Ask `Compare my protein intake this week and last week` in a fresh chat. This compares week-to-date with the same elapsed weekdays of the previous week. The dashboard compares two complete seven-day windows ending on the selected date.
8. Log a workout with `I walked for 30 minutes today`.

The Research view exposes a limited rule-based baseline without Gemini. Normal Chat uses Gemini. USDA credentials are needed for food retrieval. No fabricated nutrition fallback is used when a provider fails.

## Nutrition and OCR behavior

USDA nutrients are calculated as `nutrient per 100 g × reviewed grams / 100`. Household portions use the gram weight for the complete selected USDA portion row. Counts and cups are not assumed to have a particular weight. Users review the food, preparation, quantity, and portion before confirmation.

Label scanning accepts JPEG, PNG, or WebP images up to 6 MB and 12 megapixels. The read action sends a metadata-stripped image to Gemini; image bytes are not persisted by NutriFit. Users review the extracted label, choose per-serving or per-100-g values, specify how much they consumed and the date, and confirm the entry. Label corrections use the review form. This feature does not recognize meals on a plate or estimate hidden ingredients.

LLM requests send the current draft and dialogue context to Gemini. USDA receives food search terms. Provider handling follows the respective account terms. Conversations and confirmed records are stored locally. Use synthetic examples for research and public issue reports.

## Tests

From `backend`:

```sh
.venv/bin/python -m pytest -q
# Optional PostgreSQL integration checks in temporary schemas:
NUTRIFIT_TEST_POSTGRES_ENV=.env .venv/bin/python -m pytest -q
```

The default tests use isolated SQLite databases. PostgreSQL checks create and remove isolated test schemas. Run integration tests with a local development database and an account permitted to create schemas.

From `frontend`:

```sh
npm run build
node --experimental-strip-types --test tests/data.test.mjs
```

The tests cover dialogue, confirmation, editing conflicts, nutrition arithmetic, label validation, usual meals, goals, weekly comparisons, and frontend aggregation/date helpers. Automated provider responses are mocked; passing tests is not a claim of live model accuracy.

## Evaluation

From `evaluation`:

```sh
../backend/.venv/bin/python run.py --modes baseline --output results/baseline.json
# Calls Gemini and may incur API charges:
../backend/.venv/bin/python run.py --modes baseline llm --output results/paired.json
```

The runner compares baseline/LLM × clarification off/on using identical cases and a fixed reference date. It records schema validity, intent accuracy, frame exact match, slot accuracy, completeness, turns, latency, failures, and dataset/prompt identifiers. Scripted clarification answers simulate users; this is not a human user study.

The included 12 examples are **synthetic development smoke cases**, not a held-out benchmark. Final evaluation remains pending. Freeze a separately labelled test set before reporting comparative performance, and evaluate retrieval/portion accuracy separately from extraction. See [evaluation notes](evaluation/README.md).

## Scope and limitations

One meal or workout per conversation; mixed-event logging is unsupported. Workout duration is recorded, not estimated calorie burn. Shortcuts snapshot previously reviewed portions and do not automatically follow edits to their source meal. Goals are user-defined tracking targets, not prescribed recommendations. Weekly summaries describe recorded totals; missing logs do not mean zero intake.

Authentication, multi-user deployment, Apple Watch integration, and model training are outside the current implementation. SQLAlchemy creates tables; versioned database migrations are not implemented. The SQLite migration helper is for the original conversations/records schema, not a full migration of newer favorites/preferences.

## References

- [Gemini structured outputs](https://ai.google.dev/gemini-api/docs/structured-output)
- [USDA API guide](https://fdc.nal.usda.gov/api-guide/)
- [USDA Foundation Foods documentation](https://fdc.nal.usda.gov/Foundation_Foods_Documentation/)
