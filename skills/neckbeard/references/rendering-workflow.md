# Produce actual learning artifacts

Choose outputs from the learning contract. The bundled helpers supply document export and local media assembly; voice generation, recording, and illustration still use available approved tools. They do not add a voice subscription or install a recorder. Keep evidence claims about the product separate from checks of the exported files.

## Written guide: Markdown to HTML and PDF

Install optional rendering dependencies into the host's chosen virtual environment:

```sh
python3 -m pip install Markdown reportlab==4.5.1
python3 scripts/render_document.py --source learning/participant-guide.md --out learning/participant-guide --title "Participant guide"
```

This creates actual `.html` and `.pdf` files and refuses existing output paths. JSON/YAML frontmatter is omitted from the visible document. Supported content is headings, paragraphs, lists (including numbering restarts), tables, emphasis, links and code. Unsupported HTML fails rather than disappearing. It executes no HTML and fetches no assets. The PDF's core fonts support Western European text; for other scripts, images, advanced layouts, or tagged PDF requirements use the host's PDF/document workflow with appropriate fonts. This exporter does not claim PDF/UA conformance.

Inspect every PDF page, check selectable text and metadata, and compare content against Markdown. Relative links remain in the HTML; the PDF shows their link text without creating unreliable local-file hyperlinks. Supply absolute approved links where click-through matters. The generated HTML is a functional reading edition; the destination site can provide its own stylesheet.

## Audio and video: prepare, then assemble

1. Adapt the guide for listening: exact labels, spoken checkpoints, pauses, and recovery. Avoid instructions that require seeing the frame. If video needs visual-only narration, author a separate standalone audio script instead of using this shared-track workflow.
2. Select an available approved speech tool. For example, a connected voice generator can synthesize public narration; a configured local or hosted TTS engine can supply the same MP3 inputs. Gate the exact narration before any external call. Owner authorization can satisfy the existing sole-owner policy; do not invent a second reviewer.
3. Divide the lesson into short instructional segments. Keep the actual voice files, transcript, and tool/voice identification. If a provider returns a preview, verify that it contains the entire requested segment; a truncated preview is not a finished input.
4. Supply a PNG visual and MP3 narration for each segment. Use authentic captures for product demonstrations. A text-and-diagram explainer is valid when clearly identified; it must not be described as a recorded application walkthrough.
5. Transcribe or align the real narration to obtain caption times. Check the text against the approved script, especially names and controls. Do not estimate all timing from word counts. Keep cues readable and within the corresponding audio duration.
6. Inventory the lesson JSON, images, and audio in the existing governance record. The renderer runs the `local-tools` / `render` / `offline` gate itself. The operating environment must supply actual network isolation if required; a receipt alone is not a sandbox.

The lesson JSON uses this shape; timings below are illustrative, not production captions:

```json
{
  "title": "Participant entry",
  "segments": [{
    "id": "01-orient",
    "title": "Check your context",
    "narration": "Check the Session and role against your brief.",
    "captions": [{"start": 0.2, "end": 3.1, "text": "Check the Session and role against your brief."}]
  }]
}
```

Place `01-orient.png` and `01-orient.mp3` beside that JSON. IDs are unique lowercase letters, numbers and hyphens. Install FFmpeg and FFprobe on PATH, then run:

```sh
python3 scripts/render_media.py --lesson learning/production/lesson.json --out learning/participant-entry --profile .neckbeard/org-profile.yaml --record learning/governance.json --root .
```

The helper creates H.264/AAC MP4 with an English subtitle track, MP3, WebVTT, a transcript, and a render receipt containing input hashes and measured duration. Captions are timed to the encoded segment boundaries. It refuses missing tools, unapproved or changed inputs, invalid/overlapping captions, and existing output names. It does not synthesize narration, capture screens, judge pronunciation, or certify learning effectiveness. The current helper uses 1080p/30fps and English captions; use the host editor for other production specifications.

## Handoff

Check codecs, complete playback, audibility, captions, page layout, and download links. Record checks that were not performed honestly. Add separate governed entries and metadata companions for the PDF, HTML, MP3, MP4, transcript, and captions. Preserve `edition_of` and shared source dependencies. Update approvals under the owner's existing authorization only after final bytes exist. Present direct downloads and accessible native players on the learning page; retain editable sources without making the learner read production records.

The repository's `docs/case-studies/fractured-order/production/` package is a worked example using local Kokoro narration and token-timed captions. It is not copied into installed skill editions and is not required by the helpers.
