# Evaluation status

Run from this directory with `../backend/.venv/bin/python run.py`.

The 12 labelled cases are development smoke checks, including one food outside baseline vocabulary. They are not sufficient to support a final claim that one system outperforms another. The checked-in runner can run the four paired conditions; API-backed conditions require local credentials. Results are ignored by git because predictions can contain user-derived data in future datasets.

Current baseline smoke run: intent 11/12 in both conditions; frame exact match 7/12 without clarification and 11/12 with clarification. The baseline cannot extract salmon. Clarification helps fill missing slots, but these fixtures were also used during development. Do not report them as held-out results.

See the root README for the held-out evaluation plan and deadlines.

## 100 case annotation draft added November 25

`datasets/v1/` contains 100 synthetic AI-authored cases: 30 development cases and 70 proposed test cases. All are pending human label and near-duplicate review; the test split is not yet frozen or executed.

- `development.json`: runnable development cases.
- `test_candidate.json`: proposed held-out cases; do not use for prompt tuning.
- `LABEL_REVIEW.md`: all 100 inputs, initial labels, clarification answers, final targets, and reviewer spaces.
- `ANNOTATION_GUIDE.md`: label conventions, category counts, limits, and review/freeze procedure.
- `manifest.json`: version, review status, counts, and dataset hashes.

Each case has both `initial_expected` and `expected`. The existing metric uses the final `expected` target in both clarification conditions. Initial extraction accuracy is a separate analysis and must not be conflated with final recovery of missing information. Deliberately unanswerable and unknown-intent cases are not expected to become complete records.

```sh
# Run from evaluation/
../backend/.venv/bin/python validate_dataset.py
../backend/.venv/bin/python run.py --dataset datasets/v1/development.json --modes baseline --output results/dev_baseline_v1.json
```

Validation passed for schemas, counts, unique inputs/IDs, declared family separation, clarification answer keys, dates, and hashes. The baseline-only development check completed in both conditions. No Gemini calls were made and the proposed test cases were not evaluated. This work does not add full input-to-saved-record timing.
