"""Rebuild the explanatory slides from lesson.json; Pillow required.

Pass a local TrueType font path. These are instructional graphics, not Plenum UI.
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--font', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
lesson = json.loads((root/'lesson.json').read_text(encoding='utf-8'))
title_font = ImageFont.truetype(args.font, 86)
body_font = ImageFont.truetype(args.font, 44)
label_font = ImageFont.truetype(args.font, 28)
for number, segment in enumerate(lesson['segments'], 1):
    image = Image.new('RGB', (1920,1080), '#1e2b29')
    draw = ImageDraw.Draw(image)
    draw.text((120,80), 'Fractured Order / Blue Scribe', font=label_font, fill='#a9c5bb')
    words, lines, line = segment['title'].split(), [], ''
    for word in words:
        candidate = (line + ' ' + word).strip()
        if draw.textlength(candidate, font=title_font) > 1640:
            lines.append(line); line = word
        else:
            line = candidate
    lines.append(line)
    assert len(lines) <= 2, 'Title needs editorial shortening'
    for row, text in enumerate(lines):
        draw.text((120,180+row*105), text, font=title_font, fill='#eef0f2')
    for row, text in enumerate(segment['lines']):
        assert draw.textlength(text,font=body_font) <= 1640, 'Slide line needs shortening'
        y=475+row*135
        draw.line((120,y-28,1800,y-28),fill='#52615e',width=2)
        draw.text((120,y),text,font=body_font,fill='#eef0f2')
    draw.text((120,960),'Neckbeard  /  Source-based learning example',font=label_font,fill='#a9c5bb')
    draw.text((1640,960),f'{number} / {len(lesson["segments"])}',font=label_font,fill='#a9c5bb')
    image.save(root/(segment['id']+'.png'))
