"""Local narration with exact, measured caption-cue boundaries and an original quiet bed."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import subprocess
import textwrap
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
from lesson_content import LESSONS

ROOT = Path(__file__).resolve().parents[1]
SR = 24000
FPS = 30
VOICE = "am_michael"
SPEED = 0.92

def caption_chunks(text, maximum=112):
    """Split long spoken lines at clause boundaries before synthesis, not after timing."""
    if len(text) <= maximum:
        return [text]
    middle = len(text)/2
    candidates = [m.end() for m in re.finditer(r"[,;:] | (?=and |while |because |rather |then |so )", text)]
    candidates = [i for i in candidates if 25 < i < len(text)-25]
    if not candidates:
        candidates = [m.end() for m in re.finditer(" ", text) if 35 < m.end() < len(text)-35]
    split = min(candidates, key=lambda n:abs(n-middle))
    return caption_chunks(text[:split].strip(),maximum)+caption_chunks(text[split:].strip(),maximum)

def timestamp(t, vtt=False):
    ms = round(t*1000)
    return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}{'.' if vtt else ','}{ms%1000:03}"

def ambient(seconds):
    """Original sparse four-chord pad, no external recordings or musical quotations."""
    t = np.arange(round(seconds*SR),dtype=np.float64)/SR
    out = np.zeros(len(t),dtype=np.float64)
    chords = [(130.8128,164.8138,195.9977),(110.0,130.8128,164.8138),(87.3071,110.0,130.8128),(97.9989,123.4708,146.8324)]
    for start in np.arange(0,seconds,8):
        idx = int(start/8)%4
        mask = (t>=start)&(t<start+10)
        u = t[mask]-start
        env = np.minimum(u/1.7,1)*np.minimum((10-u)/3.0,1)
        wave = sum(np.sin(2*np.pi*f*u)*(1+0.08*np.sin(2*np.pi*0.11*u)) for f in chords[idx])/3
        out[mask] += wave*env*0.004
    out *= np.minimum(t/2,1)*np.minimum((seconds-t)/3,1)
    return out.astype(np.float32)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--only',type=int);parser.add_argument('--start',type=int,default=1);parser.add_argument('--models',default='/private/tmp/blue-impulse-voice-models')
    args=parser.parse_args()
    model=Path(args.models)
    kokoro=Kokoro(str(model/'kokoro-v1.0.onnx'),str(model/'voices-v1.0.bin'))
    cue_dir=ROOT/'assets/voice/cues';cue_dir.mkdir(parents=True,exist_ok=True)
    out_dir=ROOT/'assets/voice';sub_dir=ROOT/'subtitles';sub_dir.mkdir(exist_ok=True)
    build=ROOT/'build';build.mkdir(exist_ok=True)
    lessons=[]
    for lesson in LESSONS:
        if (args.only and lesson['number'] != args.only) or lesson['number'] < args.start: continue
        n=lesson['number']; data=json.loads(json.dumps(lesson)); samples=[]; pos=0; captions=[]
        def silence(seconds):
            nonlocal pos
            count=round(seconds*SR);samples.append(np.zeros(count,dtype=np.float32));pos+=count
        for si,sc in enumerate(data['scenes']):
            scene_start=pos/SR
            sc['start']=scene_start;sc['beats']=[]
            silence(0.30)
            for ci,text in enumerate(sc['cues']):
                beat_start=pos/SR
                for pi,part in enumerate(caption_chunks(text)):
                    digest=hashlib.sha256(f'{VOICE}|{SPEED}|{part}'.encode()).hexdigest()[:16]
                    path=cue_dir/f'{digest}.wav'
                    if path.exists():
                        a,sr=sf.read(path,dtype='float32')
                    else:
                        a,sr=kokoro.create(part,voice=VOICE,speed=SPEED,lang='en-us',trim=True)
                        assert sr==SR
                        sf.write(path,a,sr,subtype='PCM_16')
                    assert len(a)>SR*0.25 and float(np.max(np.abs(a)))>0.001, f'Empty narration: {part}'
                    start=pos/SR;samples.append(a);pos+=len(a);end=pos/SR
                    captions.append(dict(id=f'v{n:02}-s{si:02}-c{ci:02}-{pi}',text=part,start=round(start,6),end=round(end,6),scene=si,beat=ci,audio=f'assets/voice/cues/{path.name}'))
                    silence(0.11 if pi < len(caption_chunks(text))-1 else 0.17)
                beat_end=pos/SR
                sc['beats'].append(dict(index=ci,start=round(beat_start-scene_start,6),end=round(beat_end-scene_start,6),text=text))
                if sc.get('pause_after')==ci:
                    sc['question_pause']={"start":round(pos/SR-scene_start,6),"duration":sc['pause']}
                    silence(sc['pause'])
            silence(1.6 if sc['kind']=='credits' else 0.65)
            silence((math.ceil(pos/SR*FPS)/FPS)-(pos/SR))
            sc['duration']=round(pos/SR-scene_start,6)
            print(f'Video {n:02} / {sc["key"]}: {sc["duration"]:.1f}s (total {pos/SR:.1f}s)',flush=True)
        duration=pos/SR
        assert 300<=duration<=600, f'Video {n} duration {duration:.2f} is outside user request.'
        voice=np.concatenate(samples)
        assert len(voice)==pos
        sf.write(out_dir/f'video-{n:02}-narration.wav',voice,SR,subtype='PCM_16')
        # Preserve a clean narration stem, and mix a quiet bed plus scene-entry ticks.
        bed=ambient(duration)
        for sc in data['scenes']:
            start=round((sc['start']+0.1)*SR)
            u=np.arange(round(0.085*SR))/SR
            tick=0.008*np.sin(2*np.pi*880*u)*np.exp(-u*65)
            bed[start:start+len(tick)]+=tick[:max(0,min(len(tick),len(bed)-start))]
        sf.write(build/f'video-{n:02}-bed.wav',bed,SR)
        sf.write(build/f'video-{n:02}-premix.wav',voice+bed,SR)
        for src,output in [(out_dir/f'video-{n:02}-narration.wav',out_dir/f'video-{n:02}-narration.m4a'),(build/f'video-{n:02}-premix.wav',out_dir/f'video-{n:02}-mix.m4a')]:
            subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-af','loudnorm=I=-16:TP=-1.5:LRA=9','-ar','48000','-c:a','aac','-b:a','160k',str(output)],check=True)
        data.update(duration=round(duration,6),fps=FPS,voice=VOICE,speed=SPEED,captions=captions,audio=f'assets/voice/video-{n:02}-mix.m4a')
        (ROOT/f'lesson-{n:02}.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
        stem=f'BlueImpulse_Video{n:02}_{lesson["slug"]}'
        srt=[];vtt=['WEBVTT','']
        for i,c in enumerate(captions,1):
            lines=textwrap.wrap(c['text'],width=64,break_long_words=False,break_on_hyphens=False)
            assert len(lines)<=2,(c['text'],lines)
            srt.extend([str(i),f'{timestamp(c["start"])} --> {timestamp(c["end"])}','\n'.join(lines),''])
            vtt.extend([f'{timestamp(c["start"],True)} --> {timestamp(c["end"],True)}','\n'.join(lines),''])
        (sub_dir/f'{stem}.srt').write_text('\n'.join(srt))
        (sub_dir/f'{stem}.vtt').write_text('\n'.join(vtt))
        print(f'FINISHED VIDEO {n:02}: {duration:.2f}s, {len(captions)} measured caption cues',flush=True)
        lessons.append(dict(number=n,duration=duration,cues=len(captions)))
    (build/'audio-summary.json').write_text(json.dumps(lessons,indent=2)+'\n')

if __name__=='__main__':main()
