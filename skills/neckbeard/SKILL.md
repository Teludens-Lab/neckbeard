---
name: neckbeard
description: Create and maintain repository-grounded learning documentation for the product a repository powers and for the repository itself. Use for end-user onboarding, role-based learning paths, first-task tutorials, administrator training, contributor onboarding, contextual help, practice exercises, documentation updates after code changes, and tutorial scripts, audio walkthroughs, video production packages, support staff training, release/change learning, organizational governance, and localized learning materials. Inspect implementation and verify workflows rather than generating generic documentation. Do not use for ordinary code explanation without a learning deliverable or for a general code audit.
---

# Neckbeard

Turn a repository into a path from first access to independent performance. Treat end users as a first-class audience. Use implementation as evidence; organize instruction around what people need to accomplish.

## Components and branding

Read `components.json` to discover installed components. Core orientation, evidence checks, and task tutorials are always available. Load a component's instructions only when its audience or deliverable is requested. If a requested component is absent, explain that it is not installed; do not imply its bundled resources are available. Select component behavior from the manifest, not from stale references to files excluded during installation.

Use the supplied Neckbeard identity for skill presentation. Keep humor in the mascot and name; write learner-facing instructions clearly and respectfully. Preserve the destination project's visual and documentation conventions unless branded output is requested. The supplied vector identity is assets/neckbeard.svg. Preserve its proportions.

For portable Codex installation, run `python3 scripts/install.py --target <skills-directory> --components end-user,admin,developer,practice,maintenance,media,support,release-training` from this skill folder. Omit `--components` to install all available components; use `--components core` for the minimal edition. The installer creates a `neckbeard` folder, refuses accidental overwrite, and supports explicit --action upgrade or uninstall with backups and managed-file checks. Use --agent codex|claude|cursor|generic for adapters; these are instruction entry points, not tested integrations with every host version. It copies only selected optional components. It does not install into ChatGPT. Adapter entry points require the host’s own loading and tool configuration. Use the personal skill manager for ChatGPT installation and updates.

## 1. Establish the learning contract

Read references/governance.md. Resolve the project organization profile before inspecting sensitive material; validate it with scripts/governance.py. Apply its house style, glossary, platform, required templates, approved tools, classifications, and mandatory reviewers. Use the bundled org-profile.yaml only as a template. With no configured profile, generate drafts only and block external media processing.


- Read applicable AGENTS.md, existing documentation, package manifests, and repository structure. Reuse the project's documentation conventions and framework.
- Identify audience, role, goal, prerequisites, environment, and definition of successful independent performance from the request and available evidence.
- When unspecified, default to end users and one central, supported workflow. For a library or CLI, treat its consumers as end users. Do not default every repository to developer onboarding.
- State material assumptions briefly. Ask only when a missing choice prevents useful work; otherwise proceed with the best-supported scope.
- Distinguish product use, administration, operations, and contribution. Create separate paths only for requested or evidenced roles. Do not invent product roles.
- For small requests, deliver one complete tutorial. For broad requests, produce an orientation, sequenced path, one complete first-task tutorial per requested audience, relevant reference/troubleshooting, and a verification record. Avoid generating empty stubs for every feature.

## 2. Map the actual system

Trace the chosen task through entry points, interface labels, permissions, business rules, state transitions, persistence, integrations, and observable outcomes as relevant. Use targeted searches; do not ingest an entire repository indiscriminately.

Read references/evidence-and-verification.md before investigating behavior. Build a compact evidence ledger with source paths/symbols, supported claims, verification method, result, and limitations. Record the revision when available. Treat existing documentation as a claim to check, not proof.

Separate implemented behavior from plans, fixtures, mocks, disabled features, and release-specific behavior. Check the path selected by the active configuration. A component's existence does not establish that users can reach it.

If no repository is accessible, request its location or link. Offer a clearly labeled provisional structure only; never imply an inspection occurred.

## 3. Design the learning route

Read references/learning-design.md. Work backward from an observable task outcome:

1. Define what the learner will do and how they will recognize success.
2. Identify essential prerequisites and consequential concepts.
3. Sequence tasks by dependency and increasing independence.
4. Provide a worked first task, guided practice, and a transfer task where useful.
5. Place detailed reference and optional explanations beside the relevant task rather than ahead of it.

Explain decisions and consequences where learners need to choose. Keep internal architecture out of end-user guidance unless it helps a user act or recover. Provide deeper technical explanations for administrators and developers as needed.

Never use knowledge quizzes as substitutes for demonstrating a task. Never claim learning effectiveness or usability has been established without learner evidence.

## 4. Write usable documentation

Read references/delivery-formats.md before choosing outputs. Complete tutorials default to actual MD, HTML, PDF, MP4 and MP3 files unless the user narrows scope. Written technical documents default to MD, HTML and PDF. Load media for complete tutorials; clearly report unavailable components/tools and missing deliverables. Use references/rendering-workflow.md for the bundled PDF/HTML exporter and MP3/MP4 assembler. Scripts and storyboards do not count as finished audio or video.


Read references/output-patterns.md and references/production-standards.md and select only the needed patterns. Apply the shared writing, document, and tutorial standards to all learning deliverables. For audio, video, scripts, or storyboards, load the installed media component; establish tool capabilities before promising rendered media.

- Use exact, verified interface labels, commands, fields, and statuses. Specify relevant version/environment assumptions.
- Give each procedure a goal, prerequisites, numbered actions, expected outcome, and recovery path.
- Include realistic sanitized examples. Mark illustrative data and placeholders; do not invent working credentials, endpoints, settings, or capabilities.
- Explain who can see information, which actions become final, and how to reverse mistakes when the implementation establishes those facts.
- Capture screenshots only from an actual accessible build. Do not manufacture interface screenshots or describe screenshot placeholders as completed assets. Use supported browser tools when available.
- Write accessible text alternatives and meaningful link labels. Never make color or screenshot position the only instruction.
- Label practice resources and reset instructions. Use isolated local or test environments; do not have learners perform destructive exercises in production.
- Put implementation citations and detailed verification in a maintainer-facing record so end-user instructions remain readable.

## 5. Verify and revise

Verify commands, examples, links, and workflows using available tools and the repository's supported setup. Inspect scripts before running them. Do not send communications, incur charges, mutate production, or expose secrets as part of verification without explicit authorization.

Re-run relevant checks after corrections. Report what was executed, what was inferred from code, and what remains unverified. If runtime access is blocked, deliver a source-grounded guide with specific limits rather than claiming a successful walkthrough.

Check prerequisite completeness, role access, reachable states, expected results, failure recovery, relative links, and consistency with the inspected revision. Report product defects separately with reproducible evidence; do not silently modify application behavior to make a tutorial work.

For updates, inspect the relevant diff and affected dependencies. Revise impacted paths and examples; preserve accurate content. Do not claim complete documentation coverage from a changed-files-only review.

Give every generated artifact the metadata in references/governed-document.md. Emit governance.json with document ownership, review state, evidence ledger, and multi-repository source mapping; export JSON/CSV and prose audit using scripts/governance.py. Validate before handoff and require --release before claiming publication readiness. Apply the shared glossary and locale rules in references/governance.md.

Save documentation in the repository when working on an existing project, following its conventions. For standalone files, use the environment's required durable artifact workflow. A chat-only request needs no file. Summarize deliverables, verification, and material limitations with usable links.
