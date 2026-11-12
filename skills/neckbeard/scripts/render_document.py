#!/usr/bin/env python3
"""Render a Markdown guide to HTML and PDF. Requires Markdown and ReportLab.

Supports headings, paragraphs, lists, tables, links, emphasis, and code. Unsupported
HTML fails explicitly. This renderer does not execute HTML or fetch external assets.
"""
import argparse
from html import escape
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def document_body(text):
    if text.startswith('---\n'):
        pieces = text.split('---\n', 2)
        if len(pieces) != 3:
            raise ValueError('Unclosed document metadata')
        return pieces[2].lstrip()
    return text


def render(source, output, title):
    import markdown
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, KeepTogether
    html_path, pdf_path = Path(str(output) + '.html'), Path(str(output) + '.pdf')
    if html_path.exists() or pdf_path.exists():
        raise ValueError('Output exists; choose a new prefix or move the previous edition')
    body = markdown.markdown(document_body(source.read_text(encoding='utf-8-sig')),
                             extensions=['tables', 'fenced_code', 'sane_lists'], output_format='xhtml')
    tree = ET.fromstring('<root>' + body + '</root>')
    allowed = {'root', 'h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li', 'table', 'thead', 'tbody',
               'tr', 'th', 'td', 'strong', 'em', 'a', 'code', 'pre', 'br', 'hr', 'blockquote'}
    for node in tree.iter():
        if node.tag not in allowed or any(k not in {'href', 'start'} for k in node.attrib):
            raise ValueError('Unsupported HTML: ' + node.tag)
        if node.tag == 'a' and re.match(r'\s*(?:javascript|data|file):', node.get('href', ''), re.I):
            raise ValueError('Unsafe document link')
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'Helvetica'
    styles['Normal'].fontSize, styles['Normal'].leading = 10, 15
    styles['Normal'].spaceAfter = 9
    styles['Normal'].allowWidows = styles['Normal'].allowOrphans = 0
    styles['Normal'].textColor = colors.HexColor('#35413e')
    for name, size in [('Title', 25), ('Heading2', 16), ('Heading3', 12)]:
        styles[name].keepWithNext = 1
        styles[name].fontName = 'Helvetica-Bold'
        styles[name].fontSize, styles[name].leading = size, size * 1.25
        styles[name].textColor = colors.HexColor('#1e2b29')
        styles[name].spaceBefore, styles[name].spaceAfter = 16, 9
    cell_style = ParagraphStyle('Cell', parent=styles['Normal'], fontSize=9, leading=13, spaceAfter=0)
    code_style = ParagraphStyle('Code', fontName='Courier', fontSize=8, leading=11)

    def inline(node):
        text = escape(node.text or '')
        for child in node:
            content = inline(child)
            tag = {'strong': 'b', 'em': 'i', 'code': 'font'}.get(child.tag, child.tag)
            if tag == 'a':
                href = child.get('href', '')
                text += f'<a href="{escape(href, quote=True)}" color="#2f5d50">{content}</a>' if href.startswith(('https://', 'http://')) else content
            elif tag == 'font':
                text += '<font name="Courier">' + content + '</font>'
            elif tag == 'br':
                text += '<br/>'
            elif tag in ('b', 'i'):
                text += f'<{tag}>{content}</{tag}>'
            else:
                text += content
            text += escape(child.tail or '')
        # Core PDF fonts cover the guide's Latin text; fail unsupported scripts below.
        text = text.replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', ' - ')
        text.encode('cp1252')
        return text

    flow = []
    def blocks(parent):
        for node in parent:
            tag = node.tag
            if tag in ('h1', 'h2', 'h3', 'h4', 'p', 'blockquote'):
                style = styles[{'h1': 'Title', 'h2': 'Heading2', 'h3': 'Heading3', 'h4': 'Heading3'}.get(tag, 'Normal')]
                flow.append(Paragraph(inline(node), style))
            elif tag in ('ul', 'ol'):
                for number, item in enumerate(node, int(node.get('start', '1'))):
                    label = f'{number}. ' if tag == 'ol' else '\u2022 '
                    if len(item) and item[0].tag == 'p':
                        flow.append(Paragraph(label + inline(item[0]), styles['Normal']))
                        holder = ET.Element('root'); holder.extend(list(item)[1:]); blocks(holder)
                    else:
                        flow.append(Paragraph(label + inline(item), styles['Normal']))
            elif tag == 'table':
                rows = [[Paragraph(inline(cell), cell_style) for cell in row] for row in node.iter('tr')]
                columns = len(rows[0])
                if any(len(row) != columns for row in rows):
                    raise ValueError('Table rows have different column counts')
                table = Table(rows, colWidths=[475 / columns] * columns, repeatRows=1, hAlign='LEFT')
                table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e8eeeb')),
                    ('LINEBELOW', (0,0), (-1,-1), .4, colors.HexColor('#d2dcd6')),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING',(0,0),(-1,-1),8),
                    ('BOTTOMPADDING',(0,0),(-1,-1),8), ('LEFTPADDING',(0,0),(-1,-1),8), ('RIGHTPADDING',(0,0),(-1,-1),8)]))
                flow.extend([table, Spacer(1,12)])
            elif tag == 'pre':
                text = ''.join(node.itertext())
                if max(map(len, text.splitlines()), default=0) > 90:
                    raise ValueError('Code line too wide for PDF; wrap the source before rendering')
                flow.append(Preformatted(text, code_style))
            elif tag == 'hr':
                flow.append(Spacer(1,12))
            else:
                raise ValueError('Unsupported block: ' + tag)
    blocks(tree)
    # Keep instructions intact when they fit a page; oversized paragraphs can still split.
    grouped, pending = [], []
    for item in flow:
        if isinstance(item, Paragraph):
            pending.append(item)
            if item.getKeepWithNext():
                continue
            grouped.append(KeepTogether(pending))
        else:
            grouped.extend(pending)
            grouped.append(item)
        pending = []
    flow = grouped + pending
    output.parent.mkdir(parents=True, exist_ok=True)
    def footer(canvas, doc):
        canvas.setFont('Helvetica',8); canvas.setFillColor(colors.HexColor('#5c6570'))
        canvas.drawString(60,32,title[:65])
        canvas.drawRightString(535,32,str(doc.page))
    SimpleDocTemplate(str(pdf_path), pagesize=(595,842), rightMargin=60, leftMargin=60,
                      topMargin=48, bottomMargin=55, title=title, author='Neckbeard',
                      subject='Source-grounded learning guide').build(flow, onFirstPage=footer, onLaterPages=footer)
    css = 'body{font:17px/1.6 system-ui,sans-serif;max-width:75ch;margin:auto;padding:40px 24px;color:#1e2b29;background:#f3f4f5}h1,h2,h3{line-height:1.2}h2{margin-top:2em}table{border-collapse:collapse;width:100%;font-size:15px}th,td{text-align:left;padding:12px;border-bottom:1px solid #ccd5cf;vertical-align:top}th{background:#e8eeeb}a{color:#2f5d50}pre{overflow:auto}a:focus-visible{outline:3px solid #2f5d50;outline-offset:3px}@media print{body{padding:0;background:white}}'
    html_path.write_bytes(('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+escape(title)+'</title><style>'+css+'</style></head><body><main>'+body+'</main></body></html>\n').encode('utf-8'))
    return html_path, pdf_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--title', required=True)
    args = parser.parse_args()
    try:
        for path in render(args.source, args.out, args.title):
            print(path)
    except (ImportError, OSError, ValueError, ET.ParseError) as exc:
        parser.exit(1, f'Document render failed: {exc}\n')


if __name__ == '__main__':
    main()
