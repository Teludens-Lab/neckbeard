---
{
  "owner": "unassigned",
  "source_revision": "06c8a7166fe7a6048c64dc59aa43318ff42185ea",
  "evidence_state": "source-supported",
  "reviewer": "unassigned",
  "review_by": "2026-12-11",
  "locale": "en",
  "review_state": "draft",
  "document_id": "proposal-practice"
}
---

# Practise submitting and recovering

**Goal:** Submit a different proposal, then recover from rejected input without help. Use the same local fixture, Python 3, and working directory as the [first task](first-task.md). All data below is synthetic.

## Guided attempt

1. Run `python3 app.py submit --role participant --text "Improve the library entrance"`.
2. Confirm `status` is `submitted`, `visible_to` lists `participant` and `facilitator`, and `final` is `false`.
3. Run `python3 app.py submit --role facilitator --text "Improve the library entrance"`.
4. Expect exit code 2 and `Only participants can submit`. Change the role to `participant` and retry; expect the successful JSON again.

## Independent task

Submit your own nonblank synthetic proposal about improving a public space. Then deliberately submit whitespace-only text and recover by supplying useful text. Use the first-task guide only if needed.

**Completion evidence:** Show a successful JSON response, a text rejection, and a corrected successful response. Explain why the result does not establish that a proposal was saved or shared.

**Reset:** Each invocation is independent; no application data or account state is saved. No cleanup command is provided or needed.

## Feedback after attempting

An example solution uses `--role participant --text "Add shaded seating at the bus stop"`. Whitespace-only text should produce `Proposal text is required` and exit code 2. Correct the text and rerun. Any nonblank text is accepted by this fixture.

Technical checks executed the guided success, wrong-role rejection, whitespace rejection, and the example solution. No learner has performed or been observed completing these exercises; learning effectiveness remains unverified.
