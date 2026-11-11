---
{
  "document_id": "maintainer-first-task",
  "owner": "repository-maintainer",
  "source_revision": "7586d226115ba2ef89d22f79a99b0ac467ee8674",
  "evidence_state": "runtime-verified",
  "reviewer": "repository-maintainer",
  "review_by": "2027-02-09",
  "locale": "en"
}
---

# Verify a Neckbeard edition — draft for maintainer review

## Outcome
Verify the distribution and run the checks before changing or distributing an edition.

## Before you begin
Use a checkout of this repository, Python 3.9 or newer, and a disposable local directory for installation trials. These commands do not contact production systems. Dependency installation needs access to your approved package source.

## Complete the task
1. From the repository root, install YAML support: `python3 -m pip install -r skills/neckbeard/requirements.txt`.
2. Verify the shipped source: `python3 skills/neckbeard/scripts/checksums.py verify`. Expected: `Checksums verify passed`.
3. Run `python3 -m unittest discover -s tests -v`. Expected: all checks pass. The checks create temporary installations and fixture repositories, exercise governance and media denial paths, and clean up their temporary files.
4. Run `python3 skills/neckbeard/scripts/governance.py validate --profile .neckbeard/org-profile.yaml --record .neckbeard/governance.json --root .`. Expected: JSON with `valid: true`.
5. Run `python3 skills/neckbeard/scripts/governance.py stale --record .neckbeard/governance.json --repo neckbeard=.` from a clean checkout. Expected: `stale: false` if no mapped source has changed since this guide's evidence revision.

## Recover
A checksum mismatch means the distribution differs from its manifest. Investigate the diff; do not regenerate checksums merely to silence the failure. Failed tests print the affected case. Stale sources require checking the guide against the affected implementation, then refreshing source/evidence revisions and obtaining review. Missing repositories or commits require explicit checkouts with sufficient history. A dirty checkout is flagged even when the edits seem unrelated.

## Practice
In a temporary branch, change a mapped installer file and run the drift check. Confirm it reports the affected guide. Restore your change and rerun. Do not modify the distribution used by other people during practice.

## Verification and review
The code and fixture checks were executed during development; this is not independent reviewer approval or learner validation. The machine record records the source snapshot and empty review decisions. Release readiness remains pending.
