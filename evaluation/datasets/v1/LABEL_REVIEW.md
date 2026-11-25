# NutriFit 100 case label review

Synthetic draft prepared November 25, 2026. All labels require human review before freezing the proposed test split.

For each case record: reviewer, accept or revise, and reason. Review the initial label before looking at any system prediction.

## complete_meal_01 — development

**Input:** I ate 3 slices of toast today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "toast", "quantity": 3, "unit": "slices"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "toast", "quantity": 3, "unit": "slices"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_02 — development

**Input:** I had two eggs today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "eggs", "quantity": 2, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "eggs", "quantity": 2, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_03 — development

**Input:** Yesterday I ate 1.5 cups of rice.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "rice", "quantity": 1.5, "unit": "cups"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "rice", "quantity": 1.5, "unit": "cups"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_04 — development

**Input:** I ate 180 grams of salmon today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "salmon", "quantity": 180, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "salmon", "quantity": 180, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_05 — development

**Input:** I ate 1 banana on 2026-11-23.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "banana", "quantity": 1, "unit": "count"}], "workouts": [], "date": "2026-11-23", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "banana", "quantity": 1, "unit": "count"}], "workouts": [], "date": "2026-11-23", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_06 — development

**Input:** Today I ate 2 apples and 3 eggs.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "apple", "quantity": 2, "unit": "count"}, {"name": "eggs", "quantity": 3, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "apple", "quantity": 2, "unit": "count"}, {"name": "eggs", "quantity": 3, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_07 — development

**Input:** I ate 120 g of chicken yesterday.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "chicken", "quantity": 120, "unit": "grams"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "chicken", "quantity": 120, "unit": "grams"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_08 — development

**Input:** I ate 2 slices of bread on November 20, 2026.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "bread", "quantity": 2, "unit": "slices"}], "workouts": [], "date": "2026-11-20", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "bread", "quantity": 2, "unit": "slices"}], "workouts": [], "date": "2026-11-20", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_01 — development

**Input:** I ate eggs today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "eggs", "quantity": null, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.quantity": "2 eggs"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "eggs", "quantity": 2, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_02 — development

**Input:** I ate 1 banana.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "banana", "quantity": 1, "unit": "count"}], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"date": "yesterday"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "banana", "quantity": 1, "unit": "count"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_03 — development

**Input:** I ate rice today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "rice", "quantity": null, "unit": null}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.quantity": "150 grams", "foods.0.unit": "grams"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "rice", "quantity": 150, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_04 — development

**Input:** I ate 2 slices of toast and eggs today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "toast", "quantity": 2, "unit": "slices"}, {"name": "eggs", "quantity": null, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.1.quantity": "3 eggs"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "toast", "quantity": 2, "unit": "slices"}, {"name": "eggs", "quantity": 3, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_05 — development

**Input:** I ate 200 of chicken today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "chicken", "quantity": 200, "unit": null}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.unit": "grams"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "chicken", "quantity": 200, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

The number is supplied, but its unit is not.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_06 — development

**Input:** I ate apples yesterday.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "apple", "quantity": null, "unit": "count"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.quantity": "2 apples"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "apple", "quantity": 2, "unit": "count"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_07 — development

**Input:** I ate 150 grams of salmon.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "salmon", "quantity": 150, "unit": "grams"}], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"date": "2026-11-21"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "salmon", "quantity": 150, "unit": "grams"}], "workouts": [], "date": "2026-11-21", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## workout_01 — development

**Input:** I ran for 30 minutes today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "running", "duration_minutes": 30}], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "running", "duration_minutes": 30}], "date": "2026-11-25", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_02 — development

**Input:** I walked yesterday.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "walking", "duration_minutes": null}], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{"workouts.0.duration_minutes": "25 minutes"}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "walking", "duration_minutes": 25}], "date": "2026-11-24", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_03 — development

**Input:** I cycled for 45 minutes.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "cycling", "duration_minutes": 45}], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"date": "today"}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "cycling", "duration_minutes": 45}], "date": "2026-11-25", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_04 — development

**Input:** I was running for 20 minutes on 2026-11-20.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "running", "duration_minutes": 20}], "date": "2026-11-20", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "running", "duration_minutes": 20}], "date": "2026-11-20", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_05 — development

**Input:** I went walking for 15 minutes today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "walking", "duration_minutes": 15}], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "walking", "duration_minutes": 15}], "date": "2026-11-25", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_06 — development

**Input:** I did cycling.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "cycling", "duration_minutes": null}], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"workouts.0.duration_minutes": "35 minutes", "date": "yesterday"}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "cycling", "duration_minutes": 35}], "date": "2026-11-24", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## history_01 — development

**Input:** Show nutrition yesterday.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-24", "end_date": "2026-11-24"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-24", "end_date": "2026-11-24"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_02 — development

**Input:** Show calories from 2026-11-01 to 2026-11-12.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-01", "end_date": "2026-11-12"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-01", "end_date": "2026-11-12"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_03 — development

**Input:** Show my protein today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-25", "end_date": "2026-11-25"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-25", "end_date": "2026-11-25"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_04 — development

**Input:** Show my nutrition history.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"date": "2026-11-20", "end_date": "2026-11-25"}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-20", "end_date": "2026-11-25"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_01 — development

**Input:** I did not eat eggs.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

Negated eating is not a completed log.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_02 — development

**Input:** I plan to eat rice.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

Future intention is not a completed log.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_03 — development

**Input:** I ate 2 eggs today—actually, make that 3 eggs.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "eggs", "quantity": 3, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "eggs", "quantity": 3, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

The explicit correction replaces 2; do not produce two egg items.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_04 — development

**Input:** I ate 1 apple and ran for 20 minutes today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

Mixed meal and workout is unsupported by the one-intent schema; ask to split, not choose one.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_05 — development

**Input:** How many calories should I eat each day?

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

Advice request, not history or a completed log.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_09 — test

**Input:** For lunch today, I finished 240 grams of chicken fried rice.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "chicken fried rice", "quantity": 240, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "chicken fried rice", "quantity": 240, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_10 — test

**Input:** My dinner yesterday was 175 grams of grilled tofu.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "grilled tofu", "quantity": 175, "unit": "grams"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "grilled tofu", "quantity": 175, "unit": "grams"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_11 — test

**Input:** This morning I ate 0.75 cups of oatmeal.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "oatmeal", "quantity": 0.75, "unit": "cups"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "oatmeal", "quantity": 0.75, "unit": "cups"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_12 — test

**Input:** On 2026-11-18, I ate 90 grams of steamed broccoli.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "steamed broccoli", "quantity": 90, "unit": "grams"}], "workouts": [], "date": "2026-11-18", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "steamed broccoli", "quantity": 90, "unit": "grams"}], "workouts": [], "date": "2026-11-18", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_13 — test

**Input:** Today I had 200 milliliters of orange juice.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "orange juice", "quantity": 200, "unit": "milliliters"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "orange juice", "quantity": 200, "unit": "milliliters"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_14 — test

**Input:** Yesterday I drank 250 ml of milk.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "milk", "quantity": 250, "unit": "milliliters"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "milk", "quantity": 250, "unit": "milliliters"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_15 — test

**Input:** For breakfast today: 160 grams of Greek yogurt and 40 grams of blueberries.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "Greek yogurt", "quantity": 160, "unit": "grams"}, {"name": "blueberries", "quantity": 40, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "Greek yogurt", "quantity": 160, "unit": "grams"}, {"name": "blueberries", "quantity": 40, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_16 — test

**Input:** I finished 1 cup of lentil soup at lunch today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "lentil soup", "quantity": 1, "unit": "cups"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "lentil soup", "quantity": 1, "unit": "cups"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_17 — test

**Input:** I ate 28 grams of almonds two days ago.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "almonds", "quantity": 28, "unit": "grams"}], "workouts": [], "date": "2026-11-23", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "almonds", "quantity": 28, "unit": "grams"}], "workouts": [], "date": "2026-11-23", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_18 — test

**Input:** Today I ate half a cup of chickpeas.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "chickpeas", "quantity": 0.5, "unit": "cups"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "chickpeas", "quantity": 0.5, "unit": "cups"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_19 — test

**Input:** Yesterday I ate a quarter cup of raisins.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "raisins", "quantity": 0.25, "unit": "cups"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "raisins", "quantity": 0.25, "unit": "cups"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_20 — test

**Input:** I ate 6 ounces of baked cod today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "baked cod", "quantity": 6, "unit": "ounces"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "baked cod", "quantity": 6, "unit": "ounces"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_21 — test

**Input:** On November 22, 2026, I ate 1 pear and 2 kiwis.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "pear", "quantity": 1, "unit": "count"}, {"name": "kiwi", "quantity": 2, "unit": "count"}], "workouts": [], "date": "2026-11-22", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "pear", "quantity": 1, "unit": "count"}, {"name": "kiwi", "quantity": 2, "unit": "count"}], "workouts": [], "date": "2026-11-22", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_22 — test

**Input:** I ate 100 grams of pasta and 60 grams of tomato sauce yesterday.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "pasta", "quantity": 100, "unit": "grams"}, {"name": "tomato sauce", "quantity": 60, "unit": "grams"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "pasta", "quantity": 100, "unit": "grams"}, {"name": "tomato sauce", "quantity": 60, "unit": "grams"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_23 — test

**Input:** Today I ate 1 tablespoon of peanut butter.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "peanut butter", "quantity": 1, "unit": "tablespoons"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "peanut butter", "quantity": 1, "unit": "tablespoons"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_24 — test

**Input:** I ate 2 teaspoons of honey today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "honey", "quantity": 2, "unit": "teaspoons"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "honey", "quantity": 2, "unit": "teaspoons"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## complete_meal_25 — test

**Input:** I had 1 small bowl of vegetable curry for dinner yesterday.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "vegetable curry", "quantity": 1, "unit": "small bowl"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "vegetable curry", "quantity": 1, "unit": "small bowl"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Preserve stated preparation and household unit; do not infer ingredients or gram equivalents.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_08 — test

**Input:** Lunch today was chicken fried rice.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "chicken fried rice", "quantity": null, "unit": null}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.quantity": "220 grams", "foods.0.unit": "grams"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "chicken fried rice", "quantity": 220, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_09 — test

**Input:** I had Greek yogurt for breakfast.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "Greek yogurt", "quantity": null, "unit": null}], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.quantity": "170 grams", "foods.0.unit": "grams", "date": "yesterday"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "Greek yogurt", "quantity": 170, "unit": "grams"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_10 — test

**Input:** I finished 2 bowls of vegetable soup.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "vegetable soup", "quantity": 2, "unit": "bowls"}], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"date": "2026-11-22"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "vegetable soup", "quantity": 2, "unit": "bowls"}], "workouts": [], "date": "2026-11-22", "end_date": null}
```

Bowls are a stated unit; physical gram conversion is a later nutrition task.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_11 — test

**Input:** I drank milk today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "milk", "quantity": null, "unit": null}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.quantity": "200 milliliters", "foods.0.unit": "milliliters"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "milk", "quantity": 200, "unit": "milliliters"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_12 — test

**Input:** I ate 80 of almonds yesterday.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "almonds", "quantity": 80, "unit": null}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.unit": "grams"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "almonds", "quantity": 80, "unit": "grams"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_13 — test

**Input:** For dinner today I ate tofu and 100 grams of spinach.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "tofu", "quantity": null, "unit": null}, {"name": "spinach", "quantity": 100, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.quantity": "160 grams", "foods.0.unit": "grams"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "tofu", "quantity": 160, "unit": "grams"}, {"name": "spinach", "quantity": 100, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_14 — test

**Input:** Today I ate 1 pear and some grapes.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "pear", "quantity": 1, "unit": "count"}, {"name": "grapes", "quantity": null, "unit": null}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.1.quantity": "75 grams", "foods.1.unit": "grams"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "pear", "quantity": 1, "unit": "count"}, {"name": "grapes", "quantity": 75, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Some is not a numeric portion; do not default grapes to a serving.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_15 — test

**Input:** Yesterday I ate bowls of lentil stew.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "lentil stew", "quantity": null, "unit": "bowls"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.quantity": "2 bowls"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "lentil stew", "quantity": 2, "unit": "bowls"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Bowls specifies the unit, but not how many.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_16 — test

**Input:** I had oatmeal.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "oatmeal", "quantity": null, "unit": null}], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.quantity": "half a cup", "foods.0.unit": "cups", "date": "today"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "oatmeal", "quantity": 0.5, "unit": "cups"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_17 — test

**Input:** I ate 3 slices of pizza.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "pizza", "quantity": 3, "unit": "slices"}], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"date": "2026-11-19"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "pizza", "quantity": 3, "unit": "slices"}], "workouts": [], "date": "2026-11-19", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_18 — test

**Input:** I finished 1.5 of pasta today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "pasta", "quantity": 1.5, "unit": null}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.unit": "cups"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "pasta", "quantity": 1.5, "unit": "cups"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_19 — test

**Input:** Today I had soup, but I did not measure the amount.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "soup", "quantity": null, "unit": null}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "soup", "quantity": null, "unit": null}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Unanswerable quantity: keep unknown and incomplete; no simulated answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_20 — test

**Input:** I ate 30 grams of cheese and crackers yesterday.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "cheese", "quantity": 30, "unit": "grams"}, {"name": "crackers", "quantity": null, "unit": null}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.1.quantity": "20 grams", "foods.1.unit": "grams"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "cheese", "quantity": 30, "unit": "grams"}, {"name": "crackers", "quantity": 20, "unit": "grams"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

30 grams modifies cheese only; crackers need their own amount.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_21 — test

**Input:** I drank orange juice and ate a muffin today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "orange juice", "quantity": null, "unit": null}, {"name": "muffin", "quantity": 1, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.quantity": "180 milliliters", "foods.0.unit": "milliliters"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "orange juice", "quantity": 180, "unit": "milliliters"}, {"name": "muffin", "quantity": 1, "unit": "count"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_22 — test

**Input:** I ate a few strawberries yesterday.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "strawberries", "quantity": null, "unit": null}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.quantity": "60 grams", "foods.0.unit": "grams"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "strawberries", "quantity": 60, "unit": "grams"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

A few has no exact numerical quantity; do not invent a count.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_23 — test

**Input:** I ate 2 tablespoons of hummus, but I cannot remember the date.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "hummus", "quantity": 2, "unit": "tablespoons"}], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "hummus", "quantity": 2, "unit": "tablespoons"}], "workouts": [], "date": null, "end_date": null}
```

Unanswerable date: do not default to reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_24 — test

**Input:** I ate 120 grams of beans and 1 cup of quinoa.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "beans", "quantity": 120, "unit": "grams"}, {"name": "quinoa", "quantity": 1, "unit": "cups"}], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"date": "two days ago"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "beans", "quantity": 120, "unit": "grams"}, {"name": "quinoa", "quantity": 1, "unit": "cups"}], "workouts": [], "date": "2026-11-23", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## missing_meal_25 — test

**Input:** I had 250 of vegetable curry.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "vegetable curry", "quantity": 250, "unit": null}], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"foods.0.unit": "grams", "date": "yesterday"}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "vegetable curry", "quantity": 250, "unit": "grams"}], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Extract only explicitly stated information; normalize units using the annotation guide.

Reviewer: ___  Decision: ___  Notes: ___

## workout_07 — test

**Input:** I swam for half an hour this morning.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "swimming", "duration_minutes": 30}], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "swimming", "duration_minutes": 30}], "date": "2026-11-25", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_08 — test

**Input:** Yesterday I did yoga for 40 minutes.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "yoga", "duration_minutes": 40}], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "yoga", "duration_minutes": 40}], "date": "2026-11-24", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_09 — test

**Input:** I lifted weights for 1 hour today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "weight training", "duration_minutes": 60}], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "weight training", "duration_minutes": 60}], "date": "2026-11-25", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_10 — test

**Input:** I hiked for 90 minutes two days ago.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "hiking", "duration_minutes": 90}], "date": "2026-11-23", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "hiking", "duration_minutes": 90}], "date": "2026-11-23", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_11 — test

**Input:** On 2026-11-17 I rowed for 22 minutes.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "rowing", "duration_minutes": 22}], "date": "2026-11-17", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "rowing", "duration_minutes": 22}], "date": "2026-11-17", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_12 — test

**Input:** Today I danced for 12.5 minutes.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "dancing", "duration_minutes": 12.5}], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "dancing", "duration_minutes": 12.5}], "date": "2026-11-25", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_13 — test

**Input:** I did Pilates yesterday.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "Pilates", "duration_minutes": null}], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{"workouts.0.duration_minutes": "50 minutes"}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "Pilates", "duration_minutes": 50}], "date": "2026-11-24", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_14 — test

**Input:** I went swimming for 35 minutes.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "swimming", "duration_minutes": 35}], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"date": "2026-11-21"}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "swimming", "duration_minutes": 35}], "date": "2026-11-21", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_15 — test

**Input:** I finished a strength training session.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "strength training", "duration_minutes": null}], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"workouts.0.duration_minutes": "45 minutes", "date": "today"}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "strength training", "duration_minutes": 45}], "date": "2026-11-25", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_16 — test

**Input:** I played basketball today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "basketball", "duration_minutes": null}], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"workouts.0.duration_minutes": "one hour"}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "basketball", "duration_minutes": 60}], "date": "2026-11-25", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_17 — test

**Input:** Yesterday I jogged for 1 hour and 15 minutes.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "jogging", "duration_minutes": 75}], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "jogging", "duration_minutes": 75}], "date": "2026-11-24", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_18 — test

**Input:** I stretched for 600 seconds today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "stretching", "duration_minutes": 10}], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "stretching", "duration_minutes": 10}], "date": "2026-11-25", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_19 — test

**Input:** I cycled 10 kilometers today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "cycling", "duration_minutes": null}], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{"workouts.0.duration_minutes": "32 minutes"}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "cycling", "duration_minutes": 32}], "date": "2026-11-25", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## workout_20 — test

**Input:** I exercised on the elliptical yesterday, but I do not know for how long.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "elliptical", "duration_minutes": null}], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "elliptical", "duration_minutes": null}], "date": "2026-11-24", "end_date": null}
```

Normalize explicit durations to minutes. Distance does not imply duration. Preserve unknowns when no answer is available.

Reviewer: ___  Decision: ___  Notes: ___

## history_05 — test

**Input:** How much protein did I log on November 18, 2026?

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-18", "end_date": "2026-11-18"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-18", "end_date": "2026-11-18"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_06 — test

**Input:** Give me my nutrition totals for the last 7 days.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-19", "end_date": "2026-11-25"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-19", "end_date": "2026-11-25"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_07 — test

**Input:** Show my logged calories this week.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-23", "end_date": "2026-11-25"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-23", "end_date": "2026-11-25"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_08 — test

**Input:** What were my nutrition totals last week?

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-16", "end_date": "2026-11-22"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-16", "end_date": "2026-11-22"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_09 — test

**Input:** Show my meal history for this month so far.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-01", "end_date": "2026-11-25"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-01", "end_date": "2026-11-25"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_10 — test

**Input:** How much fat did I log two days ago?

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-23", "end_date": "2026-11-23"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-23", "end_date": "2026-11-23"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_11 — test

**Input:** List the workouts I logged on 2026-11-17.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-17", "end_date": "2026-11-17"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-17", "end_date": "2026-11-17"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_12 — test

**Input:** Summarize my logged carbs from November 5 through November 9, 2026.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-05", "end_date": "2026-11-09"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-05", "end_date": "2026-11-09"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_13 — test

**Input:** Show my meal records for the previous calendar month.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-10-01", "end_date": "2026-10-31"}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-10-01", "end_date": "2026-10-31"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_14 — test

**Input:** Show my nutrition totals for a date range; I have not told you the dates yet.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{"date": "2026-11-10", "end_date": "2026-11-15"}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": "2026-11-10", "end_date": "2026-11-15"}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## history_15 — test

**Input:** Show my calorie history, but I cannot remember which dates I mean.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "history", "foods": [], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "history", "foods": [], "workouts": [], "date": null, "end_date": null}
```

History extracts dates and intent only, not requested nutrient filters. Weeks start Monday; ranges are inclusive; current week/month ends at reference_date.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_06 — test

**Input:** I had 300 grams of vegetable curry today. Correction: I ate only half of that amount.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "vegetable curry", "quantity": 150, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "vegetable curry", "quantity": 150, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Explicit relative correction: 300 × 0.5 = 150 grams. No nutrient arithmetic is tested.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_07 — test

**Input:** I swam for 50 minutes today; sorry, it was 35 minutes.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "swimming", "duration_minutes": 35}], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "workout_log", "foods": [], "workouts": [{"name": "swimming", "duration_minutes": 35}], "date": "2026-11-25", "end_date": null}
```

Use the corrected duration, retaining the date.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_08 — test

**Input:** I ate 140 grams of tofu yesterday. Correction: it was today.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "tofu", "quantity": 140, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "tofu", "quantity": 140, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Explicit date correction retains the food amount.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_09 — test

**Input:** I was going to eat a muffin but never did.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

Unrealized intention must not become a meal log.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_10 — test

**Input:** I did not go swimming.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

Negated workout must not become a workout log.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_11 — test

**Input:** Tomorrow I will do yoga for 30 minutes.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

Future workout planning is outside completed-log intent; keep all slots empty.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_12 — test

**Input:** What is the protein content of tofu?

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "unknown", "foods": [], "workouts": [], "date": null, "end_date": null}
```

Generic food-information question is not personal history or meal logging.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_13 — test

**Input:** I ate something today, but I cannot remember what it was.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Completed meal intent and date are known; foods remain empty and clarification cannot be answered.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_14 — test

**Input:** I ate 2 portions of it yesterday, but I have not named the food.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [], "workouts": [], "date": "2026-11-24", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [], "workouts": [], "date": "2026-11-24", "end_date": null}
```

Do not invent a food called it. Food list is empty because schema has no unnamed-food entity.

Reviewer: ___  Decision: ___  Notes: ___

## challenge_15 — test

**Input:** I ate 100 grams of chickpeas today, not 200 grams.

**Reference date:** 2026-11-25

**Initial expected extraction**
```json
{"intent": "meal_log", "foods": [{"name": "chickpeas", "quantity": 100, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

**Scripted clarification answers**
```json
{}
```

**Final target**
```json
{"intent": "meal_log", "foods": [{"name": "chickpeas", "quantity": 100, "unit": "grams"}], "workouts": [], "date": "2026-11-25", "end_date": null}
```

Local negation rejects 200 grams; it does not negate the completed meal.

Reviewer: ___  Decision: ___  Notes: ___
