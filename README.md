# Neckbeard

Repository-grounded learning for end users, administrators, developers, support teams, and people adopting a release. A modular skill with auditable evidence, organization policy, and optional media production guidance.

## Start with one useful task

```text
Use $neckbeard to create participant onboarding for this repository.
Read our org-profile.yaml. Include a first-task tutorial, practice, recovery,
governance.json and the evidence you can actually verify.
```

Neckbeard inspects implementation, distinguishes runtime checks from code inspection, and creates a learning path. It does not certify usability or learning effectiveness without learner evidence. Audio/video production depends on separately available tools.

## Installation and managed lifecycle

GitHub publication is pending. Once this repository is published at the intended address:

```bash
git clone https://github.com/Seth-arc/neckbeard.git
cd neckbeard
python3 skills/neckbeard/scripts/checksums.py verify
python3 skills/neckbeard/scripts/install.py --target ~/.codex/skills --components end-user,practice
```

Omit `--components` for all eight components, or use `--components core`. On Windows PowerShell use `py -3` and `--target "$HOME/.codex/skills"`. Installation uses Python 3.9+ and its standard library. Install `skills/neckbeard/requirements.txt` for full YAML profile and document metadata support; JSON-compatible YAML is also supported without it.

```bash
# Run from a newly downloaded, checksum-verified full distribution.
python3 skills/neckbeard/scripts/install.py --target ~/.codex/skills --action upgrade
python3 skills/neckbeard/scripts/install.py --target ~/.codex/skills --action uninstall
```

Upgrades preserve the current component edition, agent choice, org-profile.yaml and glossary.json unless you explicitly choose another edition/agent. They refuse modifications to other managed files. Upgrade and uninstall move the complete previous directory into `.neckbeard-backups/` under the target. To restore, move the current directory aside, then move the chosen backup back to `neckbeard`. No backup is automatically deleted. Older installations without an ownership receipt require explicit `--adopt-legacy`. Source checksums detect changed or missing files; they do not authenticate the publisher. Do not regenerate them to bypass an unexplained mismatch.

### Other agents

Use `--agent claude`, `--agent cursor`, or `--agent generic` with an explicit target parent. Claude editions include CLAUDE.md; Cursor editions include neckbeard.mdc; generic editions include AGENTS.md. Each adapter delegates to the same SKILL.md and installed components. For Claude place the edition in the host's skills directory. For Cursor attach/import the provided rule in the host's rule configuration; for generic agents explicitly load the provided instruction file. These are portable instruction adapters, not installed plugins or guarantees of automatic discovery. Generated entry files and installer behavior are tested; live behavior in each host has not been certified. No adapter grants extra tool access.

## Components

| Component | Purpose |
|---|---|
| Core (required) | Evidence, orientation, task tutorials, governance and localization |
| `end-user` | Product onboarding and recovery |
| `admin` | Configuration, access, and operations |
| `developer` | Architecture, setup, and a first contribution |
| `practice` | Worked examples and independent performance |
| `maintenance` | Revision-aware learning updates and CI drift checks |
| `media` | Scripts, storyboards, approved-tool audio/video orchestration |
| `support` | Triage, safe reproduction, escalation, and support macros |
| `release-training` | What changed, migration, role impact, and transition practice |

## Organization profile

Copy the bundled `org-profile.yaml` and `glossary.json` into your project's `.neckbeard/` directory. The profile defaults to `configured: false`, no external tools, and confidential classification. Configure it deliberately; it is not evidence of organizational approval.

Step 1 reads an explicitly provided profile first, then `.neckbeard/org-profile.yaml`, then `org-profile.yaml`. It applies house style, terminology, documentation platform, required templates, approved tools, classification rules, mandatory reviewers, and review interval. With no configured project profile, outputs stay drafts and external media processing is blocked.

```bash
python3 skills/neckbeard/scripts/governance.py profile --profile .neckbeard/org-profile.yaml
```

## Document governance and audit

Every output carries an owner, exact primary source revision, evidence state, reviewer, review-by date, stable ID and locale. Markdown uses frontmatter; other formats use `<filename>.metadata.json`. Each document lists evidence IDs and repository/revision/path mappings. Multi-repository workflows retain a separate commit for each dependency. Reviewer approvals must apply to the full dependency snapshot. The example record at `skills/neckbeard/references/governance-example.json` is an unpopulated template, not evidence.

```bash
python3 skills/neckbeard/scripts/governance.py validate --profile .neckbeard/org-profile.yaml --record .neckbeard/governance.json --root .
python3 skills/neckbeard/scripts/governance.py export --record .neckbeard/governance.json --out /tmp/learning-audit
# Require current mandatory approvals before claiming release readiness:
python3 skills/neckbeard/scripts/governance.py validate --release --profile .neckbeard/org-profile.yaml --record .neckbeard/governance.json --root .
```

Exports include governance.json, documents.csv, evidence.csv, mapping.csv, media-gate.csv and audit.md. CSV cells that could be interpreted as spreadsheet formulas are escaped; raw values remain in JSON. Validation checks structure and claims against the recorded evidence, not reviewer identity. Audit records do not replace access controls or an approval system.

## Continuous maintenance

```bash
python3 skills/neckbeard/scripts/governance.py stale --record .neckbeard/governance.json --repo product=/checkout/product --repo api=/checkout/api
```

The command emits JSON and exits 1 for stale/missing/overdue dependencies, 2 for invalid input, 0 for no detected drift. It compares actual Git changes to mapped paths, flags dirty checkouts and unavailable commits, and includes deletions/renames. It never silently fetches record-supplied URLs. Only mapped dependencies are covered.

`.github/workflows/neckbeard-maintenance.yml` checks this repository on pull requests. `templates/multi-repository-ci.yml` shows explicit dependency checkouts for consuming projects; configure each repository, ref and read-only credential. A code-only change can make a guide stale even if the guide itself is unchanged. Refresh revisions only after reviewing affected learning content and evidence. CI flags work; it does not automatically certify rewritten content.

## Media data handling and offline mode

Inventory every screenshot, demo dataset, narration, caption and render input in `media_assets`. Record classification, personal-data status, sanitization, reviewer, review status, and SHA256 of the reviewed bytes. Use synthetic data wherever possible. Sanitization does not automatically declassify an asset.

```bash
python3 skills/neckbeard/scripts/governance.py gate --profile .neckbeard/org-profile.yaml --record .neckbeard/governance.json --root . --tool local-tools --operation voice --mode offline --assets narration-01
```

Only exact approved tools, operations, modes and asset classifications pass. Unreviewed inputs, changed file bytes, unknown tools, disallowed personal data, and external transmission of offline-only data fail. Capture the JSON receipt with the audit package. Re-run for every changed tool, input or policy. No external calls are made by the gate. Offline mode is a preflight requirement; actual network isolation must be supplied by the execution environment. The script cannot intercept arbitrary agent/tool traffic.

## Localization

Use shared glossary IDs and approved translations. Preserve literal UI labels, commands, identifiers and placeholders. Translated outputs have their own metadata and `translation_of`, while retaining the source dependencies so maintenance catches drift. Release validation flags missing glossary translations for used locales. Human language review, RTL rendering and caption timing remain explicit checks.

## Evaluations and checksums

```bash
python3 -m pip install -r skills/neckbeard/requirements.txt
python3 -m unittest discover -s tests -v
python3 skills/neckbeard/scripts/checksums.py verify
```

`evals/` contains runnable product/service fixtures, five behavioral cases, a weighted scoring rubric, a submission scorer and evaluation instructions. Automatic tests check the fixture behavior and governance/distribution mechanisms. Fresh-agent artifacts and scores are separate evidence; no human learning outcomes are inferred from passing code tests.

Each skill distribution includes CHECKSUMS.json. The release workflow produces a source ZIP and SHA256SUMS artifact on tags or manual dispatch. It has not run on GitHub while publication is pending. MIT licensing is in LICENSE and included in installed editions.

## Website

`docs/` contains the buildless GitHub Pages site. Preview with `python3 -m http.server 8765 --directory docs`. After publication set Settings → Pages → Source → GitHub Actions. The Pages workflow deploys on changes to docs. Remove the publication-pending notice only after the repository is available. The site includes component selection, platform-specific commands, saved preferences, keyboard navigation, and reduced-motion support.

## Tutorial delivery formats

Complete tutorials default to actual `.md`, `.html`, `.pdf`, `.mp4` and `.mp3` files unless the user narrows the scope. Written technical guides use Markdown, HTML and PDF. Scripts and storyboards are supporting assets; unavailable production tools leave the corresponding media explicitly incomplete. See `skills/neckbeard/references/delivery-formats.md` for rendering, review and cross-format governance requirements.
