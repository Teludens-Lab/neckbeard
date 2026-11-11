---
{
  "owner": "unassigned",
  "source_revision": "06c8a7166fe7a6048c64dc59aa43318ff42185ea",
  "evidence_state": "source-supported",
  "reviewer": "unassigned",
  "review_by": "2026-12-11",
  "locale": "en",
  "review_state": "draft",
  "document_id": "proposal-verification"
}
---

# Verification and maintenance record

Scope: end-user CLI onboarding for `evals/fixtures/approval-product` only. Source root: `/workspace/scratch/9b38bf47b721/neckbeard`. Revision: `06c8a7166fe7a6048c64dc59aa43318ff42185ea`. The two inspected input files are tracked and unchanged relative to that commit. No other eval directories or prior answers were inspected. Source was read-only; all generated outputs and subprocess working directories were confined to this package.

No applicable AGENTS.md or organizational profile was found at the explicitly checked ancestor/profile locations. Outputs remain drafts. The included profile is the supplied restrictive unconfigured template, with no approved media tools; it is not organizational approval. Owner and reviewer are unassigned, review decisions are empty, and the proposed review-by date is 2026-12-11. Assign accountable people and configure actual policy before release. External media processing is blocked; no media was produced.

## Executed verification

Using the local Python interpreter, ran the CLI through subprocesses for the first task, guided success, transfer example, wrong role, whitespace text, missing text, unsupported action, and help. Exit codes and successful JSON fields were asserted. Exact arguments and sanitized stdout/stderr are in [runtime checks](runtime-checks.json).

Source inspection of `app.py:submit` and `main` establishes a single reachable `submit` action, role and text validation, and fixed response fields. There is no persistence, authentication, actual visibility enforcement, finalization, edit/delete, or integration code in this fixture. The README corroborates the command and explicitly labels translation/export as unimplemented roadmap items. Returned visibility is metadata, not observed sharing.

## Limits and acceptance

Technical CLI behavior was checked locally; Python installation, other platforms, missing-file recovery, learner usability, and production integration were not verified. This fixture explicitly is not a production approval system. No product defect was discovered within the exercised scope. Missing production capabilities are scope boundaries, not features to imply in onboarding.

All learner documents map to the two inspected files in governance.json. Maintain these guides when either file changes. Only the mapped sources are covered. A schema/content validation and export are recorded separately; they do not establish independent review or publication readiness. Publication is blocked until a configured profile, assigned owner/reviewer, actual approvals, and a successful `--release` validation exist.
