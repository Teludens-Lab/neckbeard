---
{"document_id":"plenum-case-study","owner":"repository-maintainer","source_revision":"2e9ace12438221a617126f1f3c63f67ace89411a","evidence_state":"source-supported","reviewer":"repository-maintainer","review_by":"2027-02-10","locale":"en"}
---

# Plenum: from a Session invitation to the right role

An implementation-grounded learning-design case study using Neckbeard. Prepared 12 November 2026. **Design and source inspection are complete; participant walkthroughs and learner outcomes have not been observed.**

## The design brief

Help a first-time Plenum participant enter the intended simulation Session and recognize the correct role context before starting work. Plenum is a role-governed simulation platform: finding a Session, gaining admission, receiving a Seat, and entering a role workspace are different events. A successful code lookup alone is not the learning outcome.

The product's own journey J-PAR-01 ends when an allowed Seat/role is entered and the Session, Seat, and Active Role Context are explicit. That gives this case a concrete performance target rather than a tour of the platform. [Journey definition, lines 13–15](https://github.com/Teludens-Lab/Plenum/blob/2e9ace12438221a617126f1f3c63f67ace89411a/docs/design/journeys.md#L13-L15)

**Audience:** participants who already have an authorized account and a simulation-team invitation or Session code. They can use a browser but need not know Plenum's internal identifiers, API, or repository. Signing in and provisioning accounts are prerequisites, not tasks taught by this guide.

**Design hypothesis:** first-time participants may confuse “Session found,” admission, and role assignment. This is inferred from the implementation's distinct states, not from interviews, support tickets, or observed learner errors. The proposed business benefit is fewer avoidable entry interruptions for Operators; no reduction has been measured.

## Scope and constraints

- One participant journey: identify the Session, follow the available entry path, enter the intended role, and recognize when an Operator must act.
- Use an isolated training Session with synthetic identities and a seat brief supplied by the simulation team. No live exercise, production account changes, or invented working access codes.
- Match Plenum's supported desktop-browser context. The product specifies a 1024 × 768 desktop acceptance floor, zoom, keyboard, reduced-motion, forced-color, and assistive-technology support; those are requirements, not certification established by this case. [Product contract](https://github.com/Teludens-Lab/Plenum/blob/2e9ace12438221a617126f1f3c63f67ace89411a/PRODUCT.md)
- Session policy controls invitation, code, waiting-room, open-selection, and assigned-role paths. The guide must branch on what the participant actually sees.
- Existing Plenum application permissions remain authoritative. The owner's approval of this learning package does not grant participants access or bypass a waiting room.
- The project owner commissioned and approved this package. The existing governance record uses `repository-maintainer` as both owner and sole approver. There is no additional reviewer or approval step.

## What implementation inspection changed

An initial linear outline—“enter code, choose role, begin”—would be incomplete. Inspection produced these design corrections before publication; they are source-driven revisions, not results of a learner study.

| Implementation evidence | Consequence for the learning design |
|---|---|
| The portal handles invitations, waiting rooms, assignment-pending states, eligible Seats, and assigned-role links separately. | Replace the linear outline with a short decision table. Keep the successful path visible and put exceptional states next to the decision. |
| Code lookup is scoped to the authenticated person's Organization and configured code-entry policy. | Treat account access and a valid code as separate prerequisites. Do not teach guessing codes or treating the code as an account credential. |
| Seat claims require admission and open Seat selection; occupancy can change before a claim completes. | Teach waiting and refreshing as legitimate recovery, and escalate an unavailable intended Seat rather than choosing an arbitrary one. |
| The workspace exposes the Session, role, and Seat context; role switching is limited to available assignments. | Define completion as checking the intended context, not clicking “Join.” |
| A transient success message is followed by a reload of server state. | Use the stable assigned-role link and resulting workspace as evidence, not a notification alone. |

Sources: [participant portal](https://github.com/Teludens-Lab/Plenum/blob/2e9ace12438221a617126f1f3c63f67ace89411a/apps/runtime-web/src/product/ParticipantPortal.tsx), [entry projection](https://github.com/Teludens-Lab/Plenum/blob/2e9ace12438221a617126f1f3c63f67ace89411a/apps/server/src/runtime/access/participant-entry.ts#L151-L248), [admission and Seat commands](https://github.com/Teludens-Lab/Plenum/blob/2e9ace12438221a617126f1f3c63f67ace89411a/apps/server/src/runtime/access/onboarding.ts#L327-L430), [runtime context](https://github.com/Teludens-Lab/Plenum/blob/2e9ace12438221a617126f1f3c63f67ace89411a/apps/runtime-web/src/App.tsx#L1569-L1625).

## Why this learning intervention

| Decision | Reason and tradeoff |
|---|---|
| A concise job aid with guided and independent practice | Entry is a short, consequential task. Learners need to decide what to do from their current state. They can keep the aid open beside the application. |
| One worked path, with branches for waiting and assignment | Gives a clear starting point without implying that every participant has the same permissions or controls. |
| Exact interface labels, flexible team/role names | “Your Sessions” and “Find session” are stable labels in the inspected code. Team and role names come from the Session's Release and must not be invented as universal labels. |
| Written, searchable instruction | Operators can update changed labels and policy branches quickly. The full instruction is in Markdown; the browser overview includes the existing Neckbeard introduction video, rather than a Plenum walkthrough. |
| Performance criteria rather than a knowledge quiz | Opening the right workspace and choosing a safe recovery demonstrate the target behavior. Recalling definitions alone would not. |
| A planned transfer scenario with different labels and access policy | Changing only a name would test repetition. Changing the entry condition tests whether the participant can select the correct next action. |

Training does not repair missing permission, a full Seat, or a service outage. Those require an Operator or product action. The guide's job is to help a participant distinguish that boundary and communicate the problem accurately. If observation shows that the interface itself misleads people, record a product issue rather than expanding the guide to compensate indefinitely.

## The learning package

1. [Participant guide](participant-guide.md): prerequisites, a complete first task, state-based recovery, guided practice, and an independent transfer exercise.
2. [Evaluation protocol](evaluation.md): Operator setup, observable criteria, neutral assistance rules, and a baseline comparison plan.
3. [Observation sheet](observations.csv): an empty template; it contains no fabricated learner records.
4. [Verification record](verification.md): inspected implementation, evidence boundaries, and reproducible governance checks.
5. [Browser edition](index.html): a concise case overview, the Neckbeard introduction video with captions and transcript, and downloads of the complete learning materials.

## What is demonstrated today

The package shows how Neckbeard translates a real repository's permissions and state transitions into an instructional sequence, then preserves source provenance and exact artifact integrity. The guide distinguishes what a participant can do from what only an Operator can resolve. Its governance record is tied to the inspected commit and to the final file bytes.

No participant success rate, completion time, support reduction, accessibility certification, or learning gain is claimed. Plenum's relevant browser-test source was inspected; those tests were not executed during this case. No interface screenshot has been manufactured or presented as runtime evidence.

## Evaluation and iteration

The next evidence is a formative observation of representative newcomers using a training Session. Record independent completion, assistance, incorrect-context attempts, recovery, and active task time separately from Operator wait time. Use a second scenario to check transfer. Compare the job aid with the onboarding material normally available, using separate comparable participants where possible; repeating the same task with the same person introduces practice effects.

The [protocol](evaluation.md) specifies critical errors and revision decisions in advance. A small formative sample identifies problems; it does not establish a population-wide improvement. After observation, retain the initial guide, the anonymized observations, the revised guide, and the reason for each change. Until then, outcomes remain **not measured**.

## Authorship and accountability

The project owner selected Plenum and authorized the work and its approval. Codex used Neckbeard's instructional guidance to inspect the pinned source, draft the case and learning materials, and run local package checks. No user interviews, independent reviews, or learner sessions were performed by the agent. Owner authorization is recorded as authorization, not evidence that a human completed the task.

## Maintenance

Inspected Plenum revision: `2e9ace12438221a617126f1f3c63f67ace89411a`. The machine ledger maps the portal, runtime context, entry projection, admission/Seat commands, HTTP routes, product/journey contracts, package setup, and existing browser tests. A change to a mapped source triggers inspection of the affected steps. Content changes invalidate the old artifact hash. Revalidate under the owner's existing authorization policy; a second person is not required.
