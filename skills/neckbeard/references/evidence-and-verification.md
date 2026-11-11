# Evidence and verification

## Evidence states

| State | Meaning | Permitted wording |
|---|---|---|
| Runtime verified | Executed the specified action and observed the relevant outcome | Verified in the stated environment |
| Source supported | Traced reachable implementation and configuration, without executing the behavior | Supported by implementation; runtime unverified |
| Documentation only | Existing documentation claims it; implementation not corroborated | Existing documentation states; confirmation needed |
| Unknown or conflicting | Evidence is missing or disagrees | Unresolved; specify the missing evidence |

Do not collapse these states into a blanket verified badge. A test verifies only its scope. A mock-backed test does not establish a production integration works.

## Evidence ledger

Record one row per consequential claim or procedure:

| Claim/task | Source path and symbol | Evidence state | Check and result | Environment/revision | Limitation |
|---|---|---|---|---|---|

Use accurate relative source links in repository documentation. Add line anchors only when actually inspected and useful. Record commands and concise sanitized results, not sensitive raw logs.

## Repository investigation

- Inspect entry points, routes, commands, role definitions, feature flags, schemas, error handling, and task-specific tests.
- Check whether a route or action is enabled for the intended role.
- Trace validation and authoritative enforcement rather than relying only on interface hints.
- Use fixtures to understand examples; label them as fixtures.
- Identify setup requirements from manifests, environment samples, and executable scripts. Never print secrets or paste private values into guides.
- Determine whether apparent integrations are real, mocked, optional, or unavailable.

## Verification matrix

Check what is relevant: clean setup, valid task, missing prerequisite, denied permission, invalid input, refresh/retry, saved outcome, and safe recovery. Do not execute every case mechanically when it adds no value.

Run commands in isolated environments where feasible. Avoid invoking publish/deploy hooks inadvertently. Explain blockers precisely: missing credentials, unavailable services, inaccessible UI, or unsupported environment. Do not fabricate logs or silently treat skipped checks as passed.

## Maintenance

Map document sections to relevant source paths and configuration. For a diff, inspect both direct changes and workflow dependencies. List affected guides, update them, and verify changed examples. Treat the mapping as an aid, not proof that all downstream effects were found.
