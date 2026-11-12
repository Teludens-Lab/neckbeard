---
{"document_id":"plenum-evaluation","owner":"repository-maintainer","source_revision":"2e9ace12438221a617126f1f3c63f67ace89411a","evidence_state":"source-supported","reviewer":"repository-maintainer","review_by":"2027-02-10","locale":"en"}
---

# Observe participant entry and recovery

**Status: protocol prepared, not executed.** There are no recorded learners or measured outcomes. This is formative evaluation of a learning intervention, not another reviewer approval step. The project owner already authorizes the package.

## Questions to answer

Can a newcomer distinguish finding a Session from admission and assignment? Can they enter the intended role and recognize a situation that requires an Operator? Does the job aid help without creating new confusion or unnecessary steps?

## Setup for the simulation team

Use the pinned Plenum implementation or record the exact replacement revision. Provide an isolated, working deployment, synthetic authorized accounts, and two training Sessions. Arrange these with an Operator using supported administration procedures; this protocol does not claim that a deployment or seeded Sessions have already been created.

| Scenario | Required starting state | Expected performance |
|---|---|---|
| A — first entry | Signed-in newcomer; valid code; open Seat selection; intended team/role available | Find the correct Session, select the intended choice, enter its role link, confirm context. |
| B — transfer and recovery | Different title and labels; invitation or code; waiting room; Operator-managed assignment | Recognize waiting, request the appropriate Operator action, refresh after admission/assignment, enter the intended role without inventing a Seat-selection step. |

Have the Operator rehearse both setups before recruiting participants. Verify the expected labels and states in the actual deployment. If the service, assignment, or policy is broken, log a setup failure separately and fix it before judging the instruction. Never ask a learner to provoke a conflict in a live Session.

Invite representative first-time participants, including differing browser confidence and relevant access needs. A proposed first round of 5–8 people is for finding usability problems, not estimating a reliable success rate. Record prior experience and group allocation. Participation should be voluntary; use pseudonymous IDs. Do not put names, account identifiers, codes, tokens, or confidential screenshots in the public repository.

## Session script

1. Explain: “We are testing the instructions, not you. You can stop at any time.” Establish permission for note-taking; recording is optional and not part of this package.
2. Give the participant the Session title, intended team/Seat and role, and the supplied entry method. Confirm prerequisites without demonstrating the task.
3. Ask: “Enter the training Session in the role on your brief. Tell me when you believe you are ready to begin.” Start active task timing. Record pauses caused by the Operator or infrastructure separately.
4. Observe without supplying the next click. If the learner requests help, ask a neutral question such as “What do you think this message means?” Record each prompt. Stop and assist before an unintended or consequential action.
5. At their declared finish, ask them to identify the Session, Seat/team and role, and explain what **Found** established. Record the observed state and their explanation.
6. Run scenario B with different labels and policy. Provide the aid under the assigned condition, but do not coach the branch decision. Distinguish required Operator work from instructional prompting.
7. Ask what was unclear and what information was missing at the moment they needed it. Record an observation separately from your interpretation.

## Performance criteria

| Criterion | Independent | Assisted | Incomplete / critical issue |
|---|---|---|---|
| Correct Session | Selects the Session matching the brief | Needs a prompt to compare the title | Continues in the wrong Session |
| Policy decision | Chooses the visible invitation, waiting, assignment, or selection path correctly | Needs a prompt to interpret the state | Attempts to bypass access or assumes lookup equals admission |
| Correct context | Enters and identifies the intended team/Seat and role | Needs help checking context | Begins work in an unintended role |
| Recovery | Waits, refreshes, or contacts the Operator as the state requires | Needs a recovery prompt | Repeats an unsafe/irrelevant action or cannot recover |
| Transfer | Applies the distinctions in scenario B | Needs the previous steps re-explained | Repeats scenario A's path despite different policy |

Call the task independently complete only when all applicable criteria are independent and no critical issue occurred. Operator admission or assignment is not a failure; coaching the learner to recognize that need is assistance. This is a task-based decision rule, not an arbitrary percentage score or proof of lasting learning.

Use [observations.csv](observations.csv) for one row per participant and scenario. Keep an empty result empty; never encode “not observed” as zero. Durations are seconds. Describe each assistance prompt and critical error without identifying the participant. Store consent and any identifying contact details separately under the owner's data policy.

## Comparison and interpretation

Where feasible, give one group the onboarding material normally available and a comparable group this job aid, using matched Session conditions and the same neutral script. Retain the baseline material and record its version. Record prior experience, group size, and exclusions. If the same people must try both, vary the scenarios and report the practice effect; do not label the difference causal.

Report counts with denominators, task and transfer completion, assistance, critical errors, and active time separately from Operator waiting. Explain setup failures and missing observations. Small samples should be presented descriptively with examples, not as statistically established improvement. A later return to the task would be needed to assess retention.

## Revision decisions

- Wrong Session or role: inspect the context-check step and the interface labels before adding more prose.
- **Found** mistaken for admission: revise the explanation at the lookup checkpoint and retest that decision.
- Correct recognition but delayed Operator action: treat this as an operational dependency, not a learning failure.
- Repeated confusion from misleading interface feedback: file a product finding separately; instruction cannot correct authorization or state behavior.
- Successful guided attempt but failed transfer: reduce repeated procedural cues and practise deciding from the current state.

Retain the initial version, observations, revision rationale, and revised version. Record the new artifact hashes when authorized updates are made. No observed findings or improvements are supplied in advance.
