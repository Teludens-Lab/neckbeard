---
{
  "document_id": "practice",
  "owner": "unassigned \u2014 draft authoring only",
  "source_revision": "f81fd04b36c85d3c4236ba5e56222decd024807f",
  "evidence_state": "source-supported",
  "reviewer": "unassigned \u2014 organization must designate",
  "review_by": "2026-12-11",
  "locale": "en"
}
---

# Practice and independent task — draft

**Goal:** Run a valid submission and recover from invalid input without assistance. Use the same Python 3 environment and source path as the [first task](first-task.md). All example text is synthetic. These example commands were technically executed; no human learning assessment has occurred.

## Guided attempt

1. Run:

   ```sh
   python3 -B /workspace/scratch/9b38bf47b721/neckbeard/evals/fixtures/approval-product/app.py submit --role participant --text "Add lighting at the bus stop"
   ```
2. Confirm exit code 0 and the same JSON as the worked example.
3. Replace the text value with `"   "` and rerun. Expect exit code 2 and `Proposal text is required` in the error.
4. Restore nonblank text and rerun successfully. If another error occurs, use [Troubleshooting](troubleshooting.md).

## Independent task

In a new terminal command, propose a public drinking fountain using synthetic text. Choose the supported action and role yourself. Then deliberately try the facilitator role, explain the error, and recover with a valid command.

Completion evidence: a successful response containing `submitted`, the two visibility labels and `final: false`; a denied facilitator attempt; and a successful corrected attempt. No point score substitutes for completing these actions.

## Check after attempting

A valid example uses `submit --role participant --text "Install a public drinking fountain"`. The facilitator attempt fails with `Only participants can submit` (exit 2). Changing back to `participant` recovers. All successful inputs return the same JSON, so inspect the command you ran as well as the output.

**Reset:** No proposal data is stored by this fixture. No deletion or reset command is needed. Retained terminal output is outside the application's control.
