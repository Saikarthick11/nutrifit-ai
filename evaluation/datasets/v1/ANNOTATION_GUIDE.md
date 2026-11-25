# NutriFit evaluation annotation guide

## Dataset status

100 synthetic, AI-authored cases: 30 development and 70 proposed test cases. This is a draft for two-person label review, not an independently collected or frozen benchmark. The proposed test cases have not been run against either extractor. Existing smoke cases remain separate; several familiar smoke patterns intentionally occur in development.

| Category | Development | Proposed test | Total |
|---|---:|---:|---:|
| Complete meals | 8 | 17 | 25 |
| Meals missing details | 7 | 18 | 25 |
| Workouts | 6 | 14 | 20 |
| History queries | 4 | 11 | 15 |
| Corrections and other challenges | 5 | 10 | 15 |
| Total | 30 | 70 | 100 |

The JSON files are the runnable source of truth. LABEL_REVIEW.md presents every input, initial label, scripted answer, and final label for review. manifest.json records file hashes. Do not combine these 100 cases with the 12 smoke cases and describe them as 112 independent test examples.

## Label contract

- Reference date is Wednesday, November 25, 2026, interpreted in the application timezone. Dates are explicit ISO calendar dates in labels. Today is November 25; yesterday is November 24; two days ago is November 23.
- Weeks begin Monday. This week means Monday through the reference date. Last week means the previous complete Monday–Sunday week. Last seven days includes today. This month so far ends today; previous calendar month covers the full prior month.
- `initial_expected` contains only information available in the original input. Missing values are null, never guessed. `expected` is the intended final target after available clarification answers. Cases without answers can legitimately remain incomplete.
- `answers` maps a missing-slot path to a scripted user response. Quantity responses can include a unit. A separate unit answer is available if the system still asks for it. No answer is provided to rescue an incorrect intent, entity list or invented entity. The runner stops if it cannot answer the requested slot.
- The runner scores the same final target in both clarification conditions. Thus missing-slot cases measure successful recovery of information, not just correctness on the initially available evidence. Use `initial_expected` separately if analyzing initial extraction accuracy. The current runner does not score that additional metric automatically.
- Food order follows first mention. Countable foods explicitly numbered or preceded by “a/an” use count. An unspecified mass food has quantity and unit null. Eggs normalize to “eggs”; singularize other explicitly counted fruits as shown in the labels. Never turn “some” or “a few” into a number.
- Canonical units: grams, cups, slices, count, milliliters, ounces, tablespoons, teaspoons, bowls. Preserve explicitly qualified units such as small bowl. Normalize g→grams and ml→milliliters. Do not convert these units to mass or infer a standard serving.
- Keep preparation and dish identity when stated (e.g. chicken fried rice is one dish, not chicken plus rice). Do not add ingredients. Food-name spelling in JSON is the exact-match convention; semantically equivalent alternative names should be flagged in human error analysis rather than silently treated as medically different foods.
- Workout labels use the activity names in JSON, with running/walking/cycling/swimming as normalized activity forms. Convert explicit hours/seconds to minutes. Distance does not imply a duration. Weight training and strength training remain as separately named activities, reflecting wording; document equivalent-name errors separately.
- History labels contain intent and inclusive date bounds only. The current schema does not encode requested nutrients or record-kind filters. This dataset cannot establish correctness of returned history answers or filtering.
- Completed meal intent with an unknown food uses an empty foods list, not a fabricated food named “something” or “it”. Unavailable dates/quantities remain missing when the user explicitly cannot remember them.
- A wholly negated event, a future plan, or a generic advice/information request has intent unknown and empty/null slots. Local negation can instead reject a particular amount while retaining an actual completed meal.
- Mixed meal/workout requests are unknown under the current single-intent contract. Do not select one event or merge schemas.
- Correction cases include their original value and correction in the same input. They test interpretation of corrections, not a separate multi-turn correction or saved-record editing benchmark.

## Split and review procedure

1. Each teammate independently reviews the labels in LABEL_REVIEW.md. Record disagreements before discussing them; then reconcile and document each revision.
2. Check near-duplicates and template overlap with both development.json and the existing smoke set. Exact duplicates are prohibited within the new 100 cases. `family_id` groups identified close variants into one split; automated checks do not establish semantic independence. Move related variants together or replace them before freezing.
3. Check whether strict name/unit conventions require an agreed normalization layer. Decide this using development examples only. Do not change the application prompt based on test predictions.
4. Revise JSON first and regenerate the review sheet and manifest if labels change. Keep this draft and record a versioned revision history. Do not call the proposed test set “human-labelled” until actual human review is complete.
5. Freeze the reviewed test file and its SHA-256 before evaluating. Run the same fixed cases in all four conditions. Do not tune prompts or baseline rules after seeing test outputs and then reuse the same set as unseen evidence.
6. Report full-frame match, intent accuracy, slot accuracy, and completeness by category as well as overall. Unknown requests and deliberately unanswerable logs should not be expected to become complete records. Separate safe rejection from log-completion metrics.

## Running

From the evaluation directory:

```sh
../backend/.venv/bin/python validate_dataset.py
../backend/.venv/bin/python run.py --dataset datasets/v1/development.json --modes baseline --output results/dev_baseline.json
```

After human review, freeze and explicitly choose the test file for final runs. Adding `llm` to `--modes` calls Gemini and can incur charges. The default runner dataset remains the original smoke set.

No evaluation is executed by dataset validation. Timing instrumentation, live API experiments, USDA matching, portion accuracy, OCR accuracy, persistence, and human response time are outside this dataset-preparation task.
