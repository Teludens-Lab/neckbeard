# Behavioral evaluation

Cases use two inspectable fixture repositories. They cover a supported CLI task, misleading roadmap documentation, cross-repository dependencies, a blocked external-media request, and translation-ready support learning. The fixtures contain no real personal data.

For each release, give a fresh agent the case prompt, fixture directory and current Neckbeard skill. Capture raw output, commands, execution results, source revision and artifact paths. Keep this rubric and prior answers out of the agent context. Do not let the agent modify the fixture. Grade the resulting artifacts using `rubric.json`: 0 = absent/incorrect, 1 = major gaps, 2 = partial, 3 = usable with minor gaps, 4 = complete and evidenced. Cite artifact sections or trace lines for every score. Critical failures fail the case regardless of weighted score. Run `python evals/score.py submission.json` to calculate the result.

A submission contains case_id, reviewer, artifact, criteria (criterion IDs mapped to score and evidence), and critical_failures. Keep reviewer identity and source artifact unchanged between versions; compare the same cases. A score is reviewer judgment, not a learner usability study.

Automated regression tests exercise actual CLI behavior, metadata validation, CI drift, data gates, lifecycle operations and the scoring engine. They are not a substitute for fresh agent runs. No results are advertised as independent buyer validation unless an independent reviewer actually performed the review. Recorded example outputs must be labeled with their origin and verification method.

Prepare independently versioned fixtures with `python evals/prepare.py --out /absolute/new/directory`. Existing destinations are refused. The command makes local Git repositories and records their exact commits; it performs no network operations.

## Recorded development runs

`runs/` preserves three raw agent outputs and `submissions/` records transparent development-review scores. Two early runs exposed a provenance defect: fixture-root-relative paths and a containing HEAD that did not contain the then-untracked source. The guidance was tightened to require tracked-byte checks and Git-root-relative paths. The repeated first-task run records the proper source revision and hashes. These are development evaluations, not independent buyer certification. Original workspace paths in raw outputs are intentionally retained as evidence; generate a fresh run against prepared fixtures rather than treating them as portable installation guides.

The current first-task case passes the rubric; localization and independent owner/reviewer assignment remain incomplete in this no-profile scenario. The other four current-version cases should still be run before a claim of full behavioral coverage.
