# Learning design

## Audience and scope

| Audience | Typical performance | Useful detail |
|---|---|---|
| End user | Complete a product task and recover from a mistake | Visible controls, decisions, statuses, permissions, outcomes |
| Administrator | Configure access and product behavior | Dependencies, settings, role effects, safe rollback |
| Operator | Diagnose and restore service | Signals, dependencies, runbooks, escalation |
| Developer | Make and validate a change | Architecture, setup, execution flow, conventions, tests |
| API/library consumer | Integrate a supported capability | Authentication, inputs, outputs, errors, lifecycle |

Do not merge these audiences into one long guide. Offer a shared orientation only where their conceptual model overlaps.

## Path design

For each path, define:
- Entry conditions: access, prior knowledge, environment, sample resources.
- Outcome: an observable action and its success criterion.
- Dependencies: which earlier tasks or concepts are necessary.
- Sequence: orientation → worked task → guided practice → independent transfer.
- Recovery: common mistakes, safe correction, and escalation.
- Completion: evidence the learner can inspect or produce.

Scale to the task. A small feature may need a five-minute walkthrough, not a curriculum. Estimate time only with a stated basis; do not present guesses as measured completion times.

## Cognitive load

Introduce concepts just before use. Keep one primary goal per tutorial. Separate mandatory steps from optional exploration. Explain consequences before irreversible actions. Use progressive disclosure for background material. Define terms once and use them consistently.

## Practice

Use a realistic problem and a checkable result. Give enough scaffolding for the first attempt, then remove guidance for a second, different case. Include reset/cleanup only when supported. Distinguish a suggested exercise from one actually executed. If no safe practice environment exists, provide an explicitly unexecuted scenario or observation task.

## Evaluation

Review technical correctness separately from learner effectiveness. A successful agent walkthrough establishes that a path worked in that environment; it does not prove a novice can follow it. Suggest learner observation when appropriate, recording task success, intervention needed, recovery, and points of confusion. Avoid arbitrary pass scores or invented assessment evidence.
