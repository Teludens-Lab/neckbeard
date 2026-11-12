---
{"document_id":"plenum-participant-guide","owner":"repository-maintainer","source_revision":"2e9ace12438221a617126f1f3c63f67ace89411a","evidence_state":"source-supported","reviewer":"repository-maintainer","review_by":"2027-02-10","locale":"en"}
---

# Enter the right Plenum Session and role

**Outcome:** open your assigned training workspace and confirm the Session, team/Seat, and role match your brief. Explain whether you can continue or need an Operator to act.

This guide follows inspected implementation. It has not yet been exercised with a running Plenum deployment or observed with learners.

## Before you begin

- Use a desktop browser and the Plenum address supplied by your simulation team. Sign in with the authorized account they identify. This guide begins after sign-in.
- Have your training Session's title, intended team/Seat and role, and either its Session code or an invitation. Ask the simulation team for anything missing; no working code is supplied here.
- Practise in an isolated training Session with synthetic information. Joining claims or uses actual Session access; do not experiment in a live exercise.
- Know how to contact that Session's Operator. The Operator manages admission and assignment. Selecting a different role is not a substitute for correcting access.

**Three useful distinctions:** a Session is the exercise you are entering; a Seat is the place assigned or offered to you; a role determines the workspace context available to you. Finding the Session does not prove all three are ready.

## Complete your first entry

1. Open **Your Sessions**. Check the displayed account name. If it is not the account your simulation team instructed you to use, stop and correct sign-in before continuing.
2. Find the intended Session. If it is already listed, select its entry and compare its title with your brief. Otherwise enter the supplied **Session code** and select **Find session**. Wait for the lookup to finish. A **Found** indicator means the lookup succeeded; it does not by itself establish admission or a role assignment.
3. Follow the state you see:

   | What you see | Your next action |
   |---|---|
   | **Accept invitation** | Check the Session title, then accept. Continue according to the new state; acceptance alone does not guarantee a role workspace. |
   | **Waiting for an Operator to admit you. Refresh after admission.** | Tell the Operator which training Session you are joining. Wait for admission, then select **Refresh Sessions**. |
   | **Access is confirmed. An Operator must assign your seat before you can enter.** | Ask the Operator for your intended assignment. After it is made, select **Refresh Sessions**. |
   | **Available team and role** | Compare the offered **Team** and **Role** with your brief. When multiple choices exist, select the intended ones. A single choice may be displayed without a selector. Select **Join as [role]**, where the role is the actual label shown. |
   | **Your assigned roles** | Use the link for the intended team and role. Do not claim another Seat merely because one is offered elsewhere. |

4. After a Seat claim, wait for the page to update. Under **Your assigned roles**, select the intended role link to enter its workspace. If the request is rejected, follow the recovery table below before trying again.
5. Confirm the workspace context. Read the Session title and open the role control labelled **Role: [role]**. Check its role context and **Seat:** detail against your brief. If the sidebar is visible, its Session and Role details provide an additional check. Do not begin simulation work in an unintended context.

## Recognize success

You can show the intended Session workspace, identify the assigned role and Seat/team, and explain why a successful lookup alone was insufficient. A banner or notification on its own is not the completion evidence. Reaching a workspace does not mean the simulation has started or that every module is available to your role.

If the context is wrong, use **All your Sessions** in the Session menu or **Exit Session** in the role menu to leave the workspace, then contact the Operator. These links navigate away; do not assume they release your Seat or revoke your assignment.

## Recover safely

| Symptom or message | Supported next step |
|---|---|
| The browser will not submit a short or empty code | Enter the complete supplied code. The field requires 6–100 characters; do not invent a replacement. |
| **The Session code is invalid or unavailable for this account.** | Check the supplied code and the signed-in account. Ask the Operator to confirm access and the permitted entry method. Do not assume a typo is the only cause. |
| No Sessions are linked yet | Use the supplied code or wait for the simulation team's invitation. A missing entry does not establish a system failure. |
| Waiting for admission or assignment | Wait for the Operator's action, then use **Refresh Sessions**. Repeatedly submitting the same code does not grant authority. |
| **The Seat is already occupied.** | Refresh the offered choices and tell the Operator the intended Seat is unavailable. Choose an alternative only if your training brief or Operator authorizes it. |
| **The Seat cannot be claimed now.** or **Open Seat selection is not enabled.** | Ask the Operator to check Session state and assignment policy. The guide cannot enable that action. |
| Loading or a network error persists | Wait for connectivity, then reload or use **Refresh Sessions** if available. Inspect the resulting assigned roles before submitting again. An error does not prove that an earlier request had no effect. |
| Workspace context does not match the brief | Stop before doing simulation work. Return to your Sessions and ask the Operator to correct the assignment. Do not edit a URL or attempt an unoffered role. |

## Guided practice

Use a separate training Session prepared for open Seat selection. With the guide available, identify your account, find the Session with the supplied code, choose the intended team/role, enter the workspace, and explain the final context. The observer may point you to a section of the guide but records that as assistance.

The names and code come from your actual training brief. “Blue Scribe” appears in Plenum's existing test source, but it is not a universal role or an instruction to choose that role in your Session.

## Independent transfer

Use a second training Session with a different title and labels, prepared with a waiting room and Operator assignment. Starting from an invitation or supplied code, reach the intended role workspace. Decide when to wait, when to refresh, and when to request help. Do not follow the earlier open-selection path if the controls are not offered.

**Completion evidence:** show the correct Session and role context, explain the waiting/assignment distinction, and recover without entering an unintended role. An Operator's required admission action is part of the scenario, not instructional assistance; prompting you to recognize that you need it is assistance.

**Reset:** the Operator resets or replaces the training setup between attempts using their established administration procedures. This guide supplies no deletion or reset command. Exiting the workspace is not a reset.

## Feedback after attempting

- **Found** confirms lookup, not completion.
- An invitation can still lead to a waiting room or pending assignment.
- Offered choices reflect policy and availability; they are not a menu of interchangeable roles.
- Completion requires the intended workspace context, not simply a successful click.

Implementation links, limitations, and validation commands are kept in the [verification record](verification.md). The [evaluation protocol](evaluation.md) supplies the observation criteria.
