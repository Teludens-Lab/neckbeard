# Required delivery formats

For a complete tutorial, deliver actual files in these five formats unless the user explicitly narrows the request:

| File | Purpose |
|---|---|
| `tutorial.md` | Editable canonical written tutorial |
| `tutorial.html` | Responsive, accessible browser-readable edition |
| `tutorial.pdf` | Rendered print/download edition |
| `tutorial.mp4` | Finished narrated video tutorial |
| `tutorial.mp3` | Finished standalone audio walkthrough |

For technical documents and written guides, produce Markdown, HTML and PDF. For standalone audio or video requests, deliver MP3 or MP4 respectively. Small contextual-help snippets and audit records retain their appropriate native formats; do not create five files for a tooltip or JSON ledger. Scripts, storyboards, captions, transcripts and editable masters are supporting assets, not replacements for the requested finished formats. A WAV master may accompany the MP3; it does not replace it.

## Consistent editions
Author and verify the Markdown first. Derive the HTML and PDF from the same content and keep task IDs, control labels, examples, prerequisites and success criteria consistent. Use the shared production standards and organization templates. Include semantic headings, meaningful links, alt text, language metadata, keyboard-readable navigation and mobile layouts in HTML. Prefer self-contained HTML with bundled/local assets and no required network connection. Resolve links appropriately for each edition; do not leave Markdown-only links broken in exported files.

Generate PDF with supported document/PDF tools. Render and inspect pages for clipping, table and code wrapping, font support, pagination and readable text. Verify that the PDF contains selectable text and document metadata; never rename HTML or Markdown to .pdf. HTML and PDF metadata companions must match the source document's owner, source revision, evidence state, reviewer, review-by date and locale. Register all editions separately in governance.json with common workflow/source dependencies and an edition_of relationship. Updating the source makes every affected edition subject to maintenance review.

## Finished media
Load the installed media component for a complete tutorial. Capture the real supported workflow and use reviewed narration as described in components/media.md. MP4 is the delivery container; prefer H.264 video and AAC audio where supported. MP3 is the standalone listening format; adapt narration for audio-only navigation rather than blindly stripping the video soundtrack. Preserve an editable script, transcript, reviewed captions and production brief. Check actual codecs, duration, intelligibility, sync and captions with available inspection/playback tools. A file extension alone does not establish successful media production.

Before any capture, synthesis or external processing apply the organization profile and data-handling gate. Use approved tools only. Installing the skill supplies instructions, not voice, recording or rendering engines. Discover available production tools and use the appropriate PDF/document/media workflows. If the media component or a required tool is unavailable, produce supported actual files and report the missing formats with the precise blocker. Do not call the complete tutorial package finished until all requested formats have been produced and checked. A script is never an MP3; a storyboard or screenshot sequence is never an MP4. Never fabricate tool execution, encode silence as narration, or substitute generated UI footage for authentic product demonstration.
