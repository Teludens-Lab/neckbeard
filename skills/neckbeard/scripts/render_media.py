#!/usr/bin/env python3
"""Render reviewed, audio-first lesson segments to MP4, MP3, WebVTT and transcript.

Requires FFmpeg and FFprobe on PATH. Does not synthesize voices or invent footage.
Each lesson segment names an id, title, narration and timed captions; its sibling
<id>.png and <id>.mp3 supply the visual and audio. All inputs must pass media policy.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import governance


def run(args):
    return subprocess.check_output(args, stderr=subprocess.PIPE, text=True)


def duration(path):
    value = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                       '-of', 'default=noprint_wrappers=1:nokey=1', str(path)]))
    if not math.isfinite(value) or value <= 0:
        raise ValueError('Invalid audio duration: ' + str(path))
    return value


def timestamp(seconds):
    ms = round(seconds * 1000)
    hours, ms = divmod(ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return f'{hours:02}:{minutes:02}:{sec:02}.{ms:03}'


def validate_segments(lesson):
    if not isinstance(lesson.get('title'), str) or not lesson['title'].strip():
        raise ValueError('Lesson title required')
    segments = lesson.get('segments')
    if not isinstance(segments, list) or not segments:
        raise ValueError('At least one segment required')
    ids = set()
    for segment in segments:
        if not isinstance(segment, dict):
            raise ValueError('Each segment must be an object')
        sid = segment.get('id', '')
        if not isinstance(sid, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', sid) or sid in ids:
            raise ValueError('Unsafe or duplicate segment id')
        ids.add(sid)
        for key in ('title', 'narration'):
            if not isinstance(segment.get(key), str) or not segment[key].strip():
                raise ValueError('Segment ' + key + ' required')
        cues = segment.get('captions')
        if not isinstance(cues, list) or not cues:
            raise ValueError('Timed captions required; derive and check them against the audio')
        previous = 0
        for cue in cues:
            if not isinstance(cue, dict):
                raise ValueError('Each caption must be an object')
            start, end = cue.get('start'), cue.get('end')
            if (type(start) not in (int, float) or type(end) not in (int, float)
                    or not math.isfinite(start) or not math.isfinite(end)
                    or start < previous or end <= start):
                raise ValueError('Caption timing must be finite, ordered and non-overlapping')
            text = cue.get('text')
            if not isinstance(text, str) or not text.strip() or any(c in text for c in ('<', '>', '\n', '\r', '\x00')):
                raise ValueError('Caption text must be one plain-text line')
            previous = end
    return segments


def render(lesson_path, output, profile_path, record_path, root):
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            raise ValueError(tool + ' is required on PATH')
    lesson_path, root, output = lesson_path.resolve(), root.resolve(), output.resolve()
    lesson = governance.load(lesson_path)
    segments = validate_segments(lesson)
    inputs = [lesson_path]
    for segment in segments:
        inputs += [lesson_path.with_name(segment['id'] + suffix) for suffix in ('.png', '.mp3')]
    record = governance.load(record_path)
    inventory = {(root / a['path']).resolve(): a['id'] for a in record['media_assets']}
    if any(p not in inventory for p in inputs):
        raise ValueError('Inventory the lesson and every image/audio input before rendering')
    receipt = governance.gate(governance.load(profile_path), record, 'local-tools', 'render',
                              'offline', [inventory[p] for p in inputs], root)
    lengths = [duration(lesson_path.with_name(s['id'] + '.mp3')) for s in segments]
    for segment, length in zip(segments, lengths):
        if segment['captions'][-1]['end'] > length + 0.05:
            raise ValueError('Caption exceeds its audio: ' + segment['id'])
    suffixes = ('.mp4', '.mp3', '.vtt', '.transcript.md', '.render.json')
    destinations = [Path(str(output) + suffix) for suffix in suffixes]
    if any(p.exists() for p in destinations):
        raise ValueError('Output already exists; choose a new prefix or move the previous edition')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='neckbeard-render-', dir=output.parent) as temp:
        work = Path(temp)
        vtt, transcript, offset = ['WEBVTT\n'], ['# ' + lesson['title'], '', lesson.get('voice_disclosure', 'Narration transcript')], 0
        for i, (segment, length) in enumerate(zip(segments, lengths)):
            run(['ffmpeg', '-v', 'error', '-nostdin', '-loop', '1', '-framerate', '30',
                 '-i', str(lesson_path.with_name(segment['id'] + '.png')),
                 '-i', str(lesson_path.with_name(segment['id'] + '.mp3')),
                 '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p',
                 '-c:v', 'libx264', '-preset', 'fast', '-tune', 'stillimage', '-crf', '22',
                 '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-af', 'apad',
                 '-t', str(length), str(work / f'{i}.mp4')])
            # The encoded frame grid determines the actual next scene boundary.
            actual = duration(work / f'{i}.mp4')
            for cue in segment['captions']:
                vtt += [timestamp(offset + cue['start']) + ' --> ' + timestamp(offset + cue['end']), cue['text'], '']
            transcript += ['', '## ' + segment['title'], '', segment['narration']]
            offset += actual
        (work / 'clips.txt').write_text(''.join(f"file '{i}.mp4'\n" for i in range(len(segments))), encoding='utf-8')
        (work / 'lesson.vtt').write_bytes('\n'.join(vtt).encode('utf-8'))
        run(['ffmpeg', '-v', 'error', '-nostdin', '-f', 'concat', '-safe', '1', '-i', str(work / 'clips.txt'),
             '-i', str(work / 'lesson.vtt'), '-map', '0:v', '-map', '0:a', '-map', '1:0',
             '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
             '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:s', 'mov_text', '-metadata:s:s:0', 'language=eng',
             '-metadata', 'title=' + lesson['title'], '-movflags', '+faststart', str(work / 'lesson.mp4')])
        # This workflow requires audio-first narration: no visual-only instructions.
        run(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(work / 'lesson.mp4'), '-vn', '-c:a', 'libmp3lame',
             '-b:a', '160k', '-metadata', 'title=' + lesson['title'], str(work / 'lesson.mp3')])
        (work / 'lesson.transcript.md').write_bytes(('\n'.join(transcript) + '\n').encode('utf-8'))
        result = {'title': lesson['title'], 'duration_seconds': duration(work / 'lesson.mp4'),
                  'renderer': run(['ffmpeg', '-version']).splitlines()[0], 'gate': receipt,
                  'inputs': {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
                  'outputs': {s: hashlib.sha256((work / ('lesson' + s)).read_bytes()).hexdigest() for s in suffixes[:-1]},
                  'limits': 'Rendering verifies files and timing bounds, not pronunciation, caption accuracy, or learning effectiveness.'}
        (work / 'lesson.render.json').write_bytes((json.dumps(result, indent=2) + '\n').encode('utf-8'))
        for suffix, dest in zip(suffixes, destinations):
            shutil.move(str(work / ('lesson' + suffix)), dest)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lesson', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path, help='New output filename prefix, without extension')
    parser.add_argument('--profile', required=True, type=Path)
    parser.add_argument('--record', required=True, type=Path)
    parser.add_argument('--root', required=True, type=Path)
    args = parser.parse_args()
    try:
        result = render(args.lesson, args.out, args.profile, args.record, args.root)
        print(json.dumps({'created': str(args.out), 'duration_seconds': result['duration_seconds']}, indent=2))
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Render failed: {exc}\n' + (exc.stderr if isinstance(exc, subprocess.CalledProcessError) else ''))


if __name__ == '__main__':
    main()
