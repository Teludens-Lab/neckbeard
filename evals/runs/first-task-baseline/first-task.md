---
{
  "document_id": "first-task",
  "owner": "unassigned \u2014 draft authoring only",
  "source_revision": "f81fd04b36c85d3c4236ba5e56222decd024807f",
  "evidence_state": "source-supported",
  "reviewer": "unassigned \u2014 organization must designate",
  "review_by": "2026-12-11",
  "locale": "en"
}
---

# Submit your first proposal — draft

**Outcome:** Produce JSON with `status` equal to `submitted` for a nonblank proposal.

**Before you begin:** Open a terminal with Python 3 and read access to `/workspace/scratch/9b38bf47b721/neckbeard/evals/fixtures/approval-product/app.py`. Use synthetic text. No installation or login is required. This local fixture only prints a result; it does not persist or transmit a proposal.

1. Check Python: `python3 --version`. A Python 3 version should appear. If unavailable, arrange a supported Python 3 environment before proceeding.
2. Submit this illustrative proposal:

   ```sh
   python3 -B /workspace/scratch/9b38bf47b721/neckbeard/evals/fixtures/approval-product/app.py submit --role participant --text "Repair the bridge"
   ```

   Use the exact role `participant`. Quotation marks keep the sentence together as one argument. Text must contain at least one non-whitespace character.
3. Inspect the response:

   ```json
   {"status": "submitted", "visible_to": ["participant", "facilitator"], "final": false}
   ```

**Check your result:** The command exits successfully (code 0) and prints this JSON. `visible_to` lists the participant and facilitator labels; `final: false` reports that the result is not final. The fixture has no sharing or finalization mechanism. It does not echo or retain the text, so the JSON cannot establish which text was submitted or provide a durable receipt.

**Recovery:** An error exits with code 2. Check the exact role, nonblank text, quotation marks and required flags, then run the corrected command. A rerun prints a new response; it does not edit an earlier proposal. See [Troubleshooting](troubleshooting.md).

**Next:** Complete [Practice](practice.md).
