---
{
  "owner": "unassigned",
  "source_revision": "06c8a7166fe7a6048c64dc59aa43318ff42185ea",
  "evidence_state": "source-supported",
  "reviewer": "unassigned",
  "review_by": "2026-12-11",
  "locale": "en",
  "review_state": "draft",
  "document_id": "proposal-troubleshooting"
}
---

# Recover from a failed submission

Use a terminal, Python 3, and the local fixture. Run commands from the directory containing `app.py`. For each error, apply the correction and rerun the [first-task command](first-task.md); success is the three-field JSON shown there.

| Symptom | Cause | Recovery |
|---|---|---|
| `Only participants can submit` | Role is not exactly `participant` | Set `--role participant`; this is an argument correction, not an account permission change. |
| `Proposal text is required` | Text contains no non-whitespace characters | Pass nonblank quoted text using `--text`. |
| `the following arguments are required: --text` | Required option omitted | Add `--text "Repair the bridge"`. |
| `invalid choice: 'export' (choose from 'submit')` | Unsupported action | Use `submit`; bulk export is not implemented. |
| Python cannot open `app.py` | Likely wrong working directory or missing source file | Locate the supplied `app.py`, then open the terminal in its directory. This environment error was not executed. |
| `python3` command unavailable | Python 3 is absent or unavailable on PATH | Use an environment with Python 3; installation is outside this fixture's documented setup. This condition was not executed. |

The first four cases were executed. Error prefixes, usage text, and paths may vary with Python version; the messages shown are the relevant excerpts. `python3 app.py --help` lists the command and options.

If correct arguments still fail, retain the exit code and sanitized error text for the person maintaining your local copy. No support endpoint is supplied. Do not infer successful persistence, collaboration, translation, or approval from a successful JSON response.
