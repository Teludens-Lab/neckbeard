---
{
  "owner": "unassigned",
  "source_revision": "06c8a7166fe7a6048c64dc59aa43318ff42185ea",
  "evidence_state": "source-supported",
  "reviewer": "unassigned",
  "review_by": "2026-12-11",
  "locale": "en",
  "review_state": "draft",
  "document_id": "proposal-first-task"
}
---

# Submit your first proposal

**Outcome:** Receive `status: submitted` with `visible_to: [participant, facilitator]` and `final: false`.

**Before you begin:** Use a local copy of the supplied Proposal tool fixture and Python 3. No third-party Python packages, account, credentials, or network service are needed. You need access to `app.py` and a terminal; examples use a POSIX shell and synthetic text. This guide applies to the source revision recorded in its metadata.

1. Open a terminal in the directory containing `app.py`. In the inspected environment that directory is `/workspace/scratch/9b38bf47b721/neckbeard/evals/fixtures/approval-product`.
2. Check Python availability with `python3 --version`. If unavailable, use an environment with Python 3 before continuing.
3. Run:

   ```sh
   python3 app.py submit --role participant --text "Repair the bridge"
   ```

   Keep the text in quotes so it is passed as one argument. `participant` is the only accepted submission role.
4. Check the returned JSON:

   ```json
   {"status": "submitted", "visible_to": ["participant", "facilitator"], "final": false}
   ```

**Recognize success:** All three fields match this result and the process exits successfully. The response does not include your proposal text or a saved proposal ID. `final: false` does not establish a later editing or approval workflow: neither is implemented.

**Recover:** For a role or text error, correct the argument and rerun the command. No submission is stored, so there is no rollback or deletion step. If Python cannot find `app.py`, return to its directory. See [exact errors and recovery](troubleshooting.md).

**Next:** Complete [guided practice and an independent task](practice.md).
