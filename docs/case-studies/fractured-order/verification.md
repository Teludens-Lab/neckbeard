---
{"document_id":"fo-verification","owner":"repository-maintainer","source_revision":"10647dd33143fa0ffaea4b4f84c2f2fdbcbb1469","evidence_state":"source-supported","reviewer":"repository-maintainer","review_by":"2027-02-10","locale":"en"}
---

# Fractured Order learning package: verification

## Source and scope

Source: `ssgwm25/Fractured-Order`, clean local checkout at `10647dd33143fa0ffaea4b4f84c2f2fdbcbb1469`, inspected on 12 November 2026. The GitHub connector returned 404 for the supplied repository, so remote HEAD and deployed commit were not independently established. A Git archive of that exact local commit was used for the isolated build and rehearsal; no `.env.local`, live identities, or production data were copied.

The task is Blue Scribe Strategic Orientation and handoff. The guide uses the visible semantic role labels. Legacy routes named `facilitator.html` implement the Scribe surface; that implementation detail is deliberately excluded from participant instructions. Blue's three required inputs and its explicit handoff are traced through the form profile, controller, lifecycle projection, and existing rehearsal helper.

## Evidence boundaries

- Source inspection supports the required fields, control names, role ownership, and handoff meaning.
- Local synthetic rehearsal exercises the real application against its deterministic mock backend. It is not evidence of hosted Supabase/RLS policy, live configuration, or a live exercise.
- The PDF, HTML, MP3, MP4, captions, and transcript are learning artifacts. The video is a narrated graphic explainer, not a hosted application recording.
- No learner study has run. Effectiveness, transfer success rate, time saving, and support reduction remain unmeasured. The observation sheet is blank.

## Production

The written job aid is the full instruction. The six-scene listening adaptation preserves the task and control names while removing dependence on visual position. Video pairs that same deliberately audio-first script with instructional graphics. The existing Neckbeard overview remains separately labeled on the case page.

Narration uses the locally executed Kokoro 0.9.4 engine, `af_heart` voice, and the checksum-verified model revision `8542409da2986c0ab5d41b3cf0411f7a58caab38`. No Fractured Order narration or repository material is sent to a hosted voice service. Captions use synthesis-token timestamps and the same spoken script. The production directory preserves the lesson manifest, source text, generated segments, visuals, scoped policy, and gate receipts.

The owner has explicitly approved this work and requested no separate reviewer approval step. Records use the existing sole-owner policy. That standing authorization is not represented as an independent human review or a completed listen-through. Full human pronunciation/listening review, assistive-technology testing, and PDF/UA conformance are not established by file or codec checks.

## Executed checks - 12 November 2026

- The isolated Fractured Order production build passed. Vite reported bundle-size and mixed-import warnings; these are not claims of a performance audit.
- The existing `session-smoke.e2e.js` passed: one test, no skips, no retries, no recorded browser errors, approximately 1.5 minutes. The initial attempt lacked the matching browser executable; after installing it in the workspace, the test ran successfully. Its machine summary is in `production/rehearsal-result.json`.
- All pages of the two-page PDF were rendered and visually inspected. The document has selectable text, metadata, readable tables, and intact role instructions. The earlier document-export check also caught and fixed numbering restarts across a table.
- The MP4 renderer completed at 137.788 seconds. Input hashes, the local render preflight, and output hashes are preserved in `blue-scribe.render.json`.
- Full-file FFmpeg decode completed without errors. FFprobe identified 1920 x 1080 H.264 video, 48 kHz AAC audio and an embedded English subtitle stream. The 160 kbps MP3 measured -16.57 LUFS integrated and -1.93 dBTP. Measurement does not substitute for human listening.
- All 57 caption cues preserve the narration's words, with timing supplied by the synthesis engine. Chromium loaded the audio and video, advanced video playback, and displayed the expected active caption. At 375 px and 1440 px the case page had no horizontal overflow.

## Reproduction commands

Optional Python document dependencies: Markdown and ReportLab. Media assembly requires FFmpeg and FFprobe on PATH. The local speech generator additionally uses Kokoro, its English phonemizer, NumPy, SoundFile, and the pinned model files. Existing output names are protected; move the previous edition or choose a new prefix.

```sh
python3 skills/neckbeard/scripts/render_document.py --source docs/case-studies/fractured-order/participant-guide.md --out /tmp/fo-guide --title "Fractured Order: Blue Scribe first handoff"
python3 skills/neckbeard/scripts/render_media.py --lesson docs/case-studies/fractured-order/production/lesson.json --out /tmp/fo-blue-scribe --profile docs/case-studies/fractured-order/production/profile.json --record docs/case-studies/fractured-order/governance.json --root .
python3 -m unittest discover -s tests -v
python3 skills/neckbeard/scripts/checksums.py verify
python3 skills/neckbeard/scripts/governance.py validate --release --profile .neckbeard/org-profile.yaml --record docs/case-studies/fractured-order/governance.json --root .
```

Run the Fractured Order rehearsal only in an isolated checkout. Inspect its scripts and use `npm ci --ignore-scripts`, `npm run build`, then the existing Playwright `tests/e2e/session-smoke.e2e.js` with a local base URL and its mock backend. Do not point that synthetic test at a live hosted Session.
