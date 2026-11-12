import copy
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]/'skills/neckbeard/scripts'
sys.path.insert(0, str(SCRIPTS))
import render_document
import render_media


class RenderTests(unittest.TestCase):
    def lesson(self):
        return {'title':'Entry guide','segments':[{'id':'enter','title':'Enter','narration':'Check your role.',
                'captions':[{'start':0,'end':1.5,'text':'Check your role.'}]}]}

    def test_caption_timing_rejects_overlap_nonfinite_and_reversed_bounds(self):
        for cue in ({'start':1,'end':.5}, {'start':float('nan'),'end':2}, {'start':0,'end':float('inf')}, {'start':True,'end':2}):
            with self.subTest(cue=cue):
                lesson=self.lesson(); lesson['segments'][0]['captions']=[dict(cue,text='Caption')]
                with self.assertRaises(ValueError): render_media.validate_segments(lesson)
        lesson=self.lesson();lesson['segments'][0]['captions'].append({'start':1,'end':3,'text':'Overlapping'})
        with self.assertRaises(ValueError):render_media.validate_segments(lesson)

    def test_paths_duplicate_ids_and_caption_markup_rejected(self):
        for sid in ('../escape','C:/escape','-option'):
            lesson=self.lesson();lesson['segments'][0]['id']=sid
            with self.assertRaises(ValueError):render_media.validate_segments(lesson)
        lesson=self.lesson();lesson['segments']*=2
        with self.assertRaises(ValueError):render_media.validate_segments(lesson)
        lesson=self.lesson();lesson['segments'][0]['captions'][0]['text']='<script>'
        with self.assertRaises(ValueError):render_media.validate_segments(lesson)

    def test_caption_timestamp_carry_and_valid_lesson(self):
        self.assertEqual(render_media.timestamp(59.9999),'00:01:00.000')
        self.assertEqual(len(render_media.validate_segments(self.lesson())),1)

    def test_frontmatter_is_removed_without_removing_body(self):
        self.assertEqual(render_document.document_body('---\n{}\n---\n\n# Guide\n---\nEnd'),'# Guide\n---\nEnd')
        with self.assertRaises(ValueError):render_document.document_body('---\n{}')

    @unittest.skipUnless(importlib.util.find_spec('markdown') and importlib.util.find_spec('reportlab'), 'Optional PDF dependencies not installed')
    def test_real_document_preserves_numbered_restart_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'guide.md';out=root/'guide'
            source.write_text('# Guide\n\n1. Find\n\nText between steps.\n\n4. Verify\n5. Finish\n',encoding='utf-8')
            html,pdf=render_document.render(source,out,'Guide')
            self.assertIn('<ol start="4">',html.read_text(encoding='utf-8'))
            self.assertTrue(pdf.read_bytes().startswith(b'%PDF-'))
            original=pdf.read_bytes()
            with self.assertRaises(ValueError):render_document.render(source,out,'Guide')
            self.assertEqual(pdf.read_bytes(),original)

    @unittest.skipUnless(importlib.util.find_spec('markdown') and importlib.util.find_spec('reportlab'), 'Optional PDF dependencies not installed')
    def test_pdf_keeps_short_instruction_and_heading_on_same_page(self):
        from reportlab.platypus import Paragraph
        draw = Paragraph.draw
        for prefix in ('', '1. '):
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as temp:
                root=Path(temp);source=root/'guide.md'
                source.write_text('```\n' + 'Filler\n'*57 + '```\n\n## Practise\n\n'
                                  + prefix + 'First line.<br/>Second line.<br/>Third line.<br/>Final line.\n', encoding='utf-8')
                drawn=[]
                def capture(paragraph):
                    lines = sum(any(getattr(word, 'text', '').strip() for word in line.words)
                                for line in paragraph.blPara.lines) if paragraph.blPara.kind else len(paragraph.blPara.lines)
                    drawn.append((paragraph.style.name, paragraph.canv.getPageNumber(), lines))
                    return draw(paragraph)
                with patch.object(Paragraph, 'draw', capture):
                    render_document.render(source,root/'guide','Pagination check')
                self.assertEqual(drawn, [('Heading2', 2, 1), ('Normal', 2, 4)])

    @unittest.skipUnless(importlib.util.find_spec('markdown') and importlib.util.find_spec('reportlab'), 'Optional PDF dependencies not installed')
    def test_pdf_long_paragraph_still_splits_without_single_line_fragments(self):
        from reportlab.platypus import Paragraph
        draw = Paragraph.draw
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'guide.md'
            source.write_text('<br/>'.join(f'Line {i}.' for i in range(95)), encoding='utf-8')
            drawn=[]
            def capture(paragraph):
                lines = sum(any(getattr(word, 'text', '').strip() for word in line.words)
                            for line in paragraph.blPara.lines)
                drawn.append((paragraph.canv.getPageNumber(), lines))
                return draw(paragraph)
            with patch.object(Paragraph, 'draw', capture):
                render_document.render(source,root/'guide','Long paragraph')
            self.assertGreater(len(drawn), 1)
            self.assertEqual(sum(lines for _,lines in drawn), 95)
            self.assertTrue(all(lines >= 2 for _,lines in drawn), drawn)

    @unittest.skipUnless(importlib.util.find_spec('markdown') and importlib.util.find_spec('reportlab'), 'Optional PDF dependencies not installed')
    def test_unsupported_active_html_fails_without_deliverables(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'bad.md';out=root/'bad'
            source.write_text('<script>alert(1)</script>',encoding='utf-8')
            with self.assertRaises(ValueError):render_document.render(source,out,'Bad')
            self.assertFalse(out.with_suffix('.pdf').exists())
            self.assertFalse(out.with_suffix('.html').exists())
