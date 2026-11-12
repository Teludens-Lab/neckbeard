# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: repository maintainers and developers who use Codex (or Claude, Cursor, or a generic agent via adapters) and owe onboarding or learning docs for a product they ship. They want docs that match what the code actually does, without writing them from scratch.

Secondary audiences served by the skill's output (not the site's main visitor): end users, administrators, developers/contributors, support staff, and people adopting a release.

## Product Purpose

Neckbeard is a modular agent skill (v2.0.1) that reads a repository's implementation and produces repository-grounded learning material: orientation, first-task tutorials, practice, recovery/troubleshooting, and a verification record. Success is a learner who can complete a real task and recover from mistakes, and a maintainer who knows which claims were run versus only read in code.

## Positioning

It reads the code, not just the README, and keeps the difference between "ran it" and "read it in code" explicit in an auditable evidence ledger. When docs promise something the code doesn't do, it catches that.

## Operating Context

- Installed with a Python 3.9+ standard-library installer into a skills directory (`~/.codex/skills` by default); requires Git and an agent configured to load that directory.
- Output lands as plain files in the repo (Markdown/HTML/PDF, optionally MP4/MP3), reviewed and shipped like any other change.
- Governance: org-profile.yaml, glossary.json, governance.json with owners, revisions, evidence states, reviewers; `governance.py` validate/export/stale/gate.
- CI drift checks flag guides made stale by code changes.

## Capabilities and Constraints

- Components: Core (always), end-user, admin, developer, practice, maintenance, media, support, release-training.
- Media component gives direction and templates; recording/voice/editing tools are not bundled.
- Adapters for Claude/Cursor/generic are instruction entry points, not certified integrations.
- GitHub publication is pending: the clone command will not work until the repo is published. The site must keep saying so until then.
- No claim of learning effectiveness or usability without learner evidence.

## Brand Commitments

- Name: Neckbeard. Humor lives in the name and the voice; learner-facing instructions stay clear and respectful.
- Voice (site): lean in. An opinionated, funny voice through the marketing copy; install instructions, caveats, and limits stay straight and exact.
- The mascot/logo images are deliberately not used on the site.

## Evidence on Hand

- `docs/assets/neckbeard-overview.mp4` + `neckbeard-overview.srt`: 1-minute narrated overview with captions.
- README, SKILL.md, components.json, evals/ (fixtures, rubric, scored runs).
- No testimonials, customers, usage numbers, or learner outcome data exist. Do not invent them.

## Product Principles

1. Evidence over assertion: say what was run, what was read, and what is unknown.
2. Teach a real task, end to end, including recovery.
3. Start small; components are opt-in.
4. Honest limits are part of the product, not fine print.
