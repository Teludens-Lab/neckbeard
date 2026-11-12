---
{"document_id":"plenum-verification","owner":"repository-maintainer","source_revision":"2e9ace12438221a617126f1f3c63f67ace89411a","evidence_state":"source-supported","reviewer":"repository-maintainer","review_by":"2027-02-10","locale":"en"}
---

# Plenum case-study verification

## Source and scope

Repository: [Teludens-Lab/Plenum](https://github.com/Teludens-Lab/Plenum/tree/2e9ace12438221a617126f1f3c63f67ace89411a). Exact inspected revision: `2e9ace12438221a617126f1f3c63f67ace89411a`. Retrieved through the GitHub connector on 12 November 2026. [provenance.json](provenance.json) records paths, Git blob hashes, inspected ranges, claims, and limitations. Git blob hashes identify source objects; they are not the artifact SHA256 hashes used for approvals.

The traced path is the participant portal, its code/invitation/Seat HTTP routes, the server's admission and assignment policy, and the resulting role workspace. The UI supplies the labels; the server supplies the authoritative access rules. Product and journey documents establish intended audience and scope but do not prove runtime behavior. Existing test definitions corroborate intended checks and were not treated as passing execution results.

## Evidence boundaries

| Check | Status | Meaning |
|---|---|---|
| UI labels and state branches | Source inspected | The pinned participant portal implements the named controls and conditional paths. |
| Admission, Seat availability, and error conditions | Source inspected | Server handlers implement policy checks; no live database transaction was exercised here. |
| Workspace context and navigation | Source inspected | The pinned runtime exposes Session/role/Seat context and exit navigation. |
| Plenum browser tests | Definitions inspected, not run | Code-entry and invitation/Seat flows exist in test source. This case supplies no new Plenum test execution result. |
| Live sign-in and training Session walkthrough | Not run | No isolated Plenum instance, test identities, or disposable PostgreSQL database was provisioned for this case. |
| Human performance, accessibility, and retention | Not measured | The observation protocol and blank CSV are proposed instruments, not results. |

The case is `source-supported`. Passing Neckbeard's package validation does not change that evidence state to `runtime-verified`.

## Executed local checks — 12 November 2026

- On Windows with Python 3.11, the complete Neckbeard suite passed: 30 tests. This includes changed Markdown/HTML/binary bytes, missing approval hashes, linked failed evidence, empty release packages, interval boundaries, owner-only renewal, and the recorded Plenum package.
- Distribution checksum verification passed after regenerating the manifest for the inspected validator and governance-document changes.
- The public `validate --release` command accepted this package under the configured sole-owner policy. This validates local records and artifact integrity, not Plenum's runtime.
- The browser edition was shortened to a portfolio overview. Full instruction, rationale, and evaluation remain in downloadable Markdown. Its isolated stylesheet follows the owner-selected [UNIZULU 101 reference](https://seth-arc.github.io/projects/unizulu-101/): Geist type, #f3f4f5 canvas, #1d2125 text, #5c6570 secondary text, two-column narrative, fine dividers, and a rounded #1e2b29 media section. The shared Neckbeard homepage stylesheet is unchanged.
- Chromium checks at 1440 px and 375 px showed no page-level horizontal overflow. All local downloads returned HTTP 200 and all in-page destinations existed. The transcript opened without overflow. The 65-second video played past eight seconds, displayed the expected active caption, and loaded all eight English cues without media errors. The poster is an actual video frame. These checks do not certify full audio accuracy, screen-reader behavior, or WCAG conformance.
- The style detector flagged the reference's Geist font and treated the native video as a padded text container. The font is intentional; video controls retain browser-native rendering. The video fallback foreground is explicitly light. The actual page uses the reference's contrast-safe light and dark palettes.
- Media SHA256 values and origins are recorded in provenance.json and checked by the case-study test. The WebVTT captions preserve the supplied SRT's cue text and timings. No new reviewer step was introduced.

## Reproduce the local package checks

Run from the Neckbeard repository root. On Windows, replace `python3` with `py -3`.

```sh
python3 -m unittest discover -s tests -v
python3 skills/neckbeard/scripts/checksums.py verify
python3 skills/neckbeard/scripts/governance.py validate --release --profile .neckbeard/org-profile.yaml --record docs/case-studies/plenum/governance.json --root .
python3 -m http.server 8765 --bind 127.0.0.1 --directory docs
```

Open `http://127.0.0.1:8765/case-studies/plenum/`. Check the navigation, downloads, video playback and captions, transcript disclosure, keyboard focus, and narrow/zoomed layouts. The case-study unit test uses the recorded preparation date to validate the historical package reproducibly; the real release command uses today's date and must fail after the review deadline unless an authorized renewal is recorded.

The existing owner's profile names `repository-maintainer` as the only mandatory approver. Every case artifact uses the same owner and approver. Approval records explicitly cite the owner's instruction authorizing this work; they do not claim a separate manual review. No approval request or new review workflow is introduced.

## To collect runtime evidence later

Use an isolated Plenum environment and the pinned source, not a live simulation. The repository declares Node 24+ and an empty disposable PostgreSQL 18 database for browser tests. Inspect its setup scripts and arrange the appropriate test configuration before running them. Plenum's root package declares `npm run test:e2e:product`; the relevant source tests are PS-770-T00 and PS-770-T01/T02 in `tests/e2e/product/product-shell.spec.mjs`.

Record the actual command, source revision, environment, exit status, and sanitized output. Then walk through the participant guide in the configured training Sessions. Do not attribute a passing synthetic test to human learning effectiveness. Follow [evaluation.md](evaluation.md) to gather learner observations separately.

## Source drift and artifact integrity

With a trusted local Plenum checkout available, use:

```sh
python3 skills/neckbeard/scripts/governance.py stale --record docs/case-studies/plenum/governance.json --repo plenum=/path/to/Plenum
```

Mapped source changes, missing commits/checkouts, dirty worktrees, and overdue dates require attention. The command does not fetch repository URLs. All inspected paths and revisions are preserved in the ledger. Only mapped dependencies are covered.

Keep the written source and browser edition aligned when updating the guide. Finalize metadata before recording the exact file SHA256. Markdown, HTML, styles, provenance, and the blank observation template have separate entries; the governance ledger itself is the control record rather than an artifact that recursively approves itself. Text in this directory uses LF line endings so hashes survive Windows checkouts.

Old review decisions remain history. The latest effective authorized decision must match the current bytes and dependency snapshot and satisfy the profile's 90-day interval. This preserves the owner's single-approver workflow while preventing stale approval from silently applying to changed content.
