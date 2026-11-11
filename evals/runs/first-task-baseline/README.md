---
{
  "document_id": "onboarding",
  "owner": "unassigned \u2014 draft authoring only",
  "source_revision": "f81fd04b36c85d3c4236ba5e56222decd024807f",
  "evidence_state": "source-supported",
  "reviewer": "unassigned \u2014 organization must designate",
  "review_by": "2026-12-11",
  "locale": "en"
}
---

# Proposal tool onboarding — draft

For CLI consumers using the supplied learning fixture. This is not a production approval system. Your first outcome is a successful local proposal response.

1. Follow [Submit your first proposal](first-task.md).
2. Complete [Practice and independent task](practice.md).
3. Use [Troubleshooting](troubleshooting.md) when a command fails.

The tool supports one action, `submit`. It reports `submitted`, visibility labels and finality in JSON. It has no storage, retrieval, editing, approval, translation or export workflow. The role is a command argument, not authenticated access. Do not infer actual sharing or a saved record from the response.

The instructions assume a terminal, Python 3 available as `python3`, and read access to the fixture. No packages, account or credentials are needed. The absolute source location below is specific to this evaluation environment; elsewhere, use your actual path to `app.py`.

All materials are drafts: no organization profile or independent review is available. Technical verification and source dependencies are recorded in [Verification](verification.md).
