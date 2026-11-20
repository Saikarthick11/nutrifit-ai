# Evaluation status

Run from this directory with `../backend/.venv/bin/python run.py`.

The 12 labelled cases are development smoke checks, including one food outside baseline vocabulary. They are not sufficient to support a final claim that one system outperforms another. The checked-in runner can run the four paired conditions; API-backed conditions require local credentials. Results are ignored by git because predictions can contain user-derived data in future datasets.

Current baseline smoke run: intent 11/12 in both conditions; frame exact match 7/12 without clarification and 11/12 with clarification. The baseline cannot extract salmon. Clarification helps fill missing slots, but these fixtures were also used during development. Do not report them as held-out results.

See the root README for the held-out evaluation plan and deadlines.
