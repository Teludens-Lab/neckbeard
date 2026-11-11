---
{
  "owner": "unassigned",
  "source_revision": "f81fd04b36c85d3c4236ba5e56222decd024807f",
  "evidence_state": "source-supported",
  "reviewer": "unassigned",
  "review_by": "2026-11-11",
  "locale": "en",
  "document_id": "approval-cli-tutorial-script"
}
---

# Submit one proposal with the CLI

Draft for CLI consumers using the small local fixture; not production training. Outcome: run one submission and recognize its JSON response. Requires Python 3, a terminal, and the fixture checkout. Estimated read-through: 90–120 seconds plus practice; unmeasured.

## Worked task

1. Open a terminal in the folder containing `app.py`.
2. Run the command with synthetic practice text:

```bash
python app.py submit --role participant --text "Repair the bridge"
```

3. Check the actual response:

```json
{"status": "submitted", "visible_to": ["participant", "facilitator"], "final": false}
```

`submitted` is the success checkpoint. The response declares participant and facilitator visibility and a nonfinal state. This fixture only prints JSON: it does not persist a proposal, authenticate people, enforce real visibility, or implement an approval service. No reset is needed; rerunning prints a fresh response. No editing or withdrawal command exists.

## Narration for live reading

**S01 — Orient.** “You’ll submit a sample proposal and check its response. This is a local learning fixture. It prints a result without saving a proposal. Open a terminal in the folder containing app dot py.”

**S02 — Demonstrate.** “Use the written command below. Run Python, app dot py, submit, with role participant and the text Repair the bridge in quotation marks. Pause while you enter the command.”

```bash
python app.py submit --role participant --text "Repair the bridge"
```

**S03 — Confirm.** “Look for status submitted. The response lists participant and facilitator in visible underscore to, and sets final to false. Those fields describe the response; this fixture does not provide an actual shared or saved record.”

**S04 — Recover.** “If you see Only participants can submit, use participant for this local practice command. A real application would require proper authorization. If you see Proposal text is required, replace empty or whitespace text with your sample proposal and run again. If Python cannot open app dot py, check that your terminal is in the fixture folder.”

**S05 — Practise and transfer.** “Try another synthetic proposal: Repair the library roof. Keep the participant role and check for submitted. Then choose your own sample text, run the command independently, and explain the three response fields. Pause here to practise.”

## Recovery and completion

The role and empty-text errors above were executed and returned exit code 2. The file-location recovery is a setup suggestion, not an executed failure test. If `python` is unavailable, check your Python installation; the local test used Python successfully. This CLI does not support automatic translation or bulk export. Completion means you can submit nonempty synthetic text and interpret the result independently; no learner observation has occurred.

## Spoken forms and accessibility

`CLI`: C L I; `JSON`: jay son; `app.py`: app dot pie; `--role`: dash dash role; `--text`: dash dash text; `visible_to`: visible underscore to. Keep literal commands in companion text; do not depend on spoken punctuation. This script is the transcript source with essential terminal context. Final captions require the actual spoken rendition and measured timing; no SRT is supplied with invented timestamps.
