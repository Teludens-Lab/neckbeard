---
{"document_id":"fo-case-study","owner":"repository-maintainer","source_revision":"10647dd33143fa0ffaea4b4f84c2f2fdbcbb1469","evidence_state":"source-supported","reviewer":"repository-maintainer","review_by":"2027-02-10","locale":"en"}
---

# Fractured Order: from a team decision to a verified handoff

Fractured Order is an economic statecraft seminar simulation delivered through Plenum. The selected first task is deliberately narrow: a Blue Scribe records Strategic Orientation and hands it to the Facilitator. The learning package comprises a written job aid, printable PDF, browser edition, audio walkthrough, narrated video, captions, and a performance-observation protocol.

## The performance problem

The implementation separates authoring, handoff, submission to White Cell, and review. A newcomer can complete a form yet misread what has happened next. Blue's own orientation and its forecast of Red also occupy different fields. The learning hypothesis is that explicit role boundaries and success checks can reduce these errors. Their frequency and any learning benefit have not been established with learners.

## The design decision

Teach one complete role task rather than tour every feature. The job aid uses the deployment's visible labels: Session Code, Display Name, Blue, Scribe, Strategic Orientation, and Record Strategic Orientation. It does not import the invitation/admission workflow from the separate Teludens-Lab Plenum repository.

The three-part form becomes a task table: own choice, forecast, expected action. The completion check deliberately extends beyond a toast to the saved card and the receiving Facilitator. A second brief changes the choices while preserving the underlying decision, so a learner must transfer the distinction instead of repeat sample values.

## Why several formats

The HTML and PDF contain the complete job aid. Audio is written for a listener who cannot see the frame: exact control names, checkpoints, and responsibility boundaries are spoken. The video pairs that narration with clearly identified instructional graphics. It is an explainer, not footage of the hosted deployment. Captions and a transcript preserve an alternative to listening; the Markdown remains editable.

## Ownership and evidence

The owner selected the deployment and authorized the work. Codex used Neckbeard to inspect the implementation, author the materials, render the files, and check them. The clean local checkout is pinned to `10647dd33143fa0ffaea4b4f84c2f2fdbcbb1469`. The supplied GitHub repository was not accessible through the connector, so remote HEAD and the hosted deployment are not independently confirmed.

The local rehearsal, where executed, uses the real application with its deterministic synthetic backend. It does not establish production Supabase permissions, hosted reliability, or learner performance. Exact execution results belong in [verification.md](verification.md); [provenance.json](provenance.json) maps the source files. No learner success rate, time saving, or reduction in support demand is claimed.
