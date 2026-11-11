---
{
  "document_id": "troubleshooting",
  "owner": "unassigned \u2014 draft authoring only",
  "source_revision": "f81fd04b36c85d3c4236ba5e56222decd024807f",
  "evidence_state": "source-supported",
  "reviewer": "unassigned \u2014 organization must designate",
  "review_by": "2026-12-11",
  "locale": "en"
}
---

# Recover from command errors — draft

Use this reference after the [first task](first-task.md). Diagnose the exact message, correct the command, and rerun it with synthetic text. Success means exit code 0 and the expected JSON.

| Symptom | Confirmed meaning or likely cause | Recovery |
|---|---|---|
| `Only participants can submit` | The role argument is not exactly `participant`. | Use `--role participant`; this does not grant authenticated permissions. |
| `Proposal text is required` | Text is empty or whitespace only. | Supply a nonblank quoted sentence. |
| `the following arguments are required: --text` | Required text flag is missing. | Add `--text "Your illustrative proposal"`. |
| `invalid choice: 'export'` | `export` is not an action. | Use `submit`; no export workaround is implemented. |
| Python reports it cannot open the file | Likely wrong or inaccessible source path; not reproduced. | Confirm where your copy of `app.py` is stored and that you can read it. |
| Shell cannot find `python3` | Likely missing Python or PATH entry; not reproduced. | Arrange a Python 3 installation/environment and retry the version check. |

Run `python3 -B /workspace/scratch/9b38bf47b721/neckbeard/evals/fixtures/approval-product/app.py --help` for supported syntax (verified). Error usage also lists required arguments. `--role` and `--text` are both mandatory.

A successful response does not create a retrievable proposal. There is no edit, undo, approve, publish or finalize action; correcting an input means rerunning the command. Translation and bulk export are roadmap items, not working features. If a corrected command still fails, provide the person responsible for your local fixture with the Python version, command using synthetic text, exit code and error. No support endpoint is supplied.
