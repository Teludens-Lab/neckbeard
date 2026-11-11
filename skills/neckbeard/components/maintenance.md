# Documentation maintenance

Inspect the requested revision range, existing documents, and affected workflow dependencies. Map source changes to tutorials, screenshots, examples, permissions, reference tables, and practice exercises. Update affected material and rerun relevant checks. Report stale instructions and product gaps separately. Preserve accurate content. Never claim full coverage from a changed-files-only review. Record revision, checks, unresolved questions, and the source-to-document mapping.

Read references/governance.md for CI mode. Run scripts/governance.py stale with governance.json and explicit --repo ID=CHECKOUT entries for every source repository. Flag changes, expired reviews and unavailable evidence as JSON; do not automatically declare documents current. Include translated artifacts, media shots and multi-repository workflows in mappings. Use the consuming-project workflow shipped in the standalone repository.
