"""Rebuild local Kokoro narration and token-timed captions; no external calls.

Requires Kokoro 0.9.4, its English phonemizer, NumPy and SoundFile. Supply the
pinned Kokoro-82M model directory; outputs remain beside this lesson manifest.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--model-dir',required=True,type=Path)
args=parser.parse_args()
os.environ['HF_HUB_OFFLINE']='1'
os.environ['TRANSFORMERS_OFFLINE']='1'
print('Loading local speech dependencies',flush=True)
import numpy as np
import soundfile as sf
from kokoro import KModel, KPipeline
import torch
torch.set_num_threads(4)
print('Speech dependencies loaded',flush=True)

root=Path(__file__).resolve().parent
model_dir=args.model_dir.resolve()
model_path=model_dir/'kokoro-v1_0.pth'
expected='496dba118d1a58f5f3db2efc88dbdc216e0483fc89fe6e47ee1f2c53f18ad1e4'
if hashlib.sha256(model_path.read_bytes()).hexdigest()!=expected:
    raise ValueError('Pinned model checksum mismatch')
lesson=json.loads((root/'lesson.json').read_text(encoding='utf-8'))
if any((root/(s['id']+'.mp3')).exists() for s in lesson['segments']):
    raise ValueError('Narration exists; move the previous edition before rebuilding')
print('Loading checksum-verified model',flush=True)
model=KModel(repo_id='hexgrad/Kokoro-82M',config=str(model_dir/'config.json'),model=str(model_path)).to('cpu').eval()
pipeline=KPipeline(lang_code='a',repo_id='hexgrad/Kokoro-82M',model=model,device='cpu')
for segment in lesson['segments']:
    results=[r for r in pipeline(segment['narration'],voice=str(model_dir/'voices/af_heart.pt'),speed=.95) if r.audio is not None]
    samples=[];cues=[];offset=0.0
    for i,result in enumerate(results):
        if i: samples.append(np.zeros(3840,dtype=np.float32));offset+=.16
        audio=result.audio.detach().cpu().numpy().astype(np.float32)
        group=[]
        for token in result.tokens or []:
            if token.start_ts is None or token.end_ts is None or not token.text:continue
            group.append(token)
            if len(group)>=9 or token.text.endswith(('.', '?', '!', ';', ':')):
                cues.append(dict(start=round(offset+group[0].start_ts,3),end=round(offset+group[-1].end_ts,3),text=''.join(t.text+(t.whitespace or '') for t in group).strip()))
                group=[]
        if group:cues.append(dict(start=round(offset+group[0].start_ts,3),end=round(offset+group[-1].end_ts,3),text=''.join(t.text+(t.whitespace or '') for t in group).strip()))
        samples.append(audio);offset+=len(audio)/24000
    if not samples or not cues:raise ValueError('Speech or timing missing: '+segment['id'])
    sf.write(root/(segment['id']+'.mp3'),np.concatenate(samples),24000,format='MP3',subtype='MPEG_LAYER_III')
    segment['captions']=cues
    print(segment['id'],round(offset,2),flush=True)
lesson['generation']={'engine':'Kokoro 0.9.4','voice':'af_heart','speed':.95,'sample_rate':24000,'model_revision':'8542409da2986c0ab5d41b3cf0411f7a58caab38','model_sha256':expected,'caption_timing':'Kokoro synthesis token timestamps','network':'HF_HUB_OFFLINE=1; TRANSFORMERS_OFFLINE=1'}
(root/'lesson.json').write_bytes((json.dumps(lesson,indent=2)+'\n').encode())
