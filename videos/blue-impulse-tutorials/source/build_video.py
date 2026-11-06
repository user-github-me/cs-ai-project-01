"""Build editable HyperFrames films from measured narration and exact guide excerpts."""
from pathlib import Path
import json
import html
import re
import textwrap
from lesson_content import LESSONS

ROOT=Path(__file__).resolve().parents[1]
CUSTOM={"q-demo","pipeline-demo","latency-demo","message-demo","cpu-demo"}
FONT_CSS='''
@font-face{font-family:Anta;src:url('assets/fonts/Anta-Regular.ttf')}
@font-face{font-family:Inter;src:url('assets/fonts/Inter-400.woff2');font-weight:400}
@font-face{font-family:Inter;src:url('assets/fonts/Inter-700.woff2');font-weight:700}
@font-face{font-family:Mono;src:url('assets/fonts/JetBrainsMono-400.woff2')}
@font-face{font-family:'JetBrains Mono';src:url('assets/fonts/JetBrainsMono-400.woff2')}
'''

def e(t): return html.escape(str(t),quote=True)
def num(n): return f'{n:.6f}'.rstrip('0').rstrip('.')
def tag(id,cls,body,style=''):
    return f'<div id="{id}" class="{cls}" style="{style}">{body}</div>'

def enter(selector,t,x=60):
    return f'''tl.fromTo({json.dumps(selector)},{{opacity:0,x:{x}}},{{opacity:1,x:{x+12 if x>=0 else x-12},duration:0.1,ease:'power1.in',immediateRender:false}},{num(t)});
tl.to({json.dumps(selector)},{{x:0,duration:0.5,ease:'power3.out'}},{num(t+.1)});'''

def svg_hook(kind):
    base='fill="none" stroke="#E6E4E5" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"'
    pink='fill="none" stroke="#E15B83" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"'
    if kind=='rover':
        paths=''.join(f'<path d="M{x} 60 V500 M60 {x} H500" {base} opacity=".16"/>' for x in range(60,501,88))
        paths+=f'<path d="M104 456 V368 H280 V192 H456 V104" {pink}/><rect x="58" y="407" width="90" height="54" rx="12" {base}/><circle cx="78" cy="469" r="13" fill="#E15B83"/><circle cx="130" cy="469" r="13" fill="#E15B83"/><path d="M104 404 V380 M104 380 L124 365" {base}/><circle cx="456" cy="104" r="26" {pink}/>'
    elif kind=='hardware':
        paths=f'<rect x="36" y="140" width="126" height="106" rx="15" {base}/><circle cx="99" cy="193" r="31" {pink}/><rect x="226" y="146" width="126" height="126" rx="8" {base}/><path d="M244 125 V145 M274 125 V145 M304 125 V145 M334 125 V145 M244 272 V292 M274 272 V292 M304 272 V292 M334 272 V292 M170 193 H213 M360 207 H416" {base}/><circle cx="462" cy="208" r="52" {pink}/><path d="M462 208 L491 181 M462 260 V359 H101 V250" {base}/>'
    elif kind=='cpu':
        paths=f'<rect x="250" y="133" width="248" height="265" rx="18" {base}/><path d="M275 103 V133 M320 103 V133 M365 103 V133 M410 103 V133 M455 103 V133 M275 398 V428 M320 398 V428 M365 398 V428 M410 398 V428 M455 398 V428" {base}/>'
        paths+='<text x="374" y="288" text-anchor="middle" fill="#E15B83" font-family="Anta" font-size="76">3 + 4</text>'
        paths+=f'<path d="M30 172 H181 M30 236 H181 M30 300 H181 M30 364 H181 M192 267 H246" {pink}/>'
    else:
        paths=f'<rect x="26" y="180" width="140" height="116" rx="10" {base}/><path d="M98 296 V323 M62 323 H134 M202 240 H380" {base}/><rect x="405" y="114" width="129" height="92" rx="10" {base}/><rect x="405" y="226" width="129" height="92" rx="10" {base}/><rect x="405" y="338" width="129" height="92" rx="10" {base}/><path d="M253 213 L280 240 L253 267 M315 213 L342 240 L315 267" {pink}/>'
    return f'<svg viewBox="0 0 560 560" width="100%" height="100%" aria-hidden="true">{paths}</svg>'

def common_scene(lesson,sc,idx,book):
    cid=f'v{lesson["number"]:02}-s{idx:02}'
    duration=sc['duration'];kind=sc['kind'];beats=[b['start'] for b in sc['beats']]
    T=lambda n:beats[min(n,len(beats)-1)]
    motion=[]
    body=[]
    title=sc['title']
    body.append(tag(f'{cid}-eyebrow','eyebrow',f'BLUE IMPULSE · BOOK TUTORIAL {lesson["number"]:02}'))
    body.append(tag(f'{cid}-title','title motion',e(title)))
    motion.append(enter(f'#{cid}-title',.05))
    body.append(tag(f'{cid}-cite','cite',f'Blue Impulse study guide · p. {sc["page"]}'))
    if kind=='hook':
        body[1]=tag(f'{cid}-title','hook-title motion',e(title))
        body.append(tag(f'{cid}-hero','hook-art motion',svg_hook(sc.get('diagram','rover'))))
        body.append(tag(f'{cid}-sub','hook-sub motion',e(sc.get('hero',''))))
        body.append(tag(f'{cid}-bookprompt','book-prompt motion',f'Open your guide at page <b>{sc["page"]}</b>'))
        motion += [enter(f'#{cid}-hero',.2),enter(f'#{cid}-sub',T(1)),enter(f'#{cid}-bookprompt',T(3))]
    elif kind=='objectives':
        for i,objective in enumerate(lesson['objectives']):
            body.append(tag(f'{cid}-objective-{i}','learning-row motion',f'<span class="number">{i+1}</span><span>{e(objective)}</span>',f'top:{315+i*114}px'))
            motion.append(enter(f'#{cid}-objective-{i}',T(min(i,1))+.1*i))
        body.append(tag(f'{cid}-welcome','welcome motion','Welcome to the tutorial<br><b>by Blue Impulse</b>'))
        motion.append(enter(f'#{cid}-welcome',T(2)))
    elif kind=='book':
        page=book['pages'][str(sc['page'])];block=min(sc.get('block',0),len(page['excerpts'])-1)
        crop=page['excerpts'][block]
        body.append(tag(f'{cid}-page','book-page motion',f'<img src="{page["full"]}" alt="Study guide page {sc["page"]}">'))
        body.append(tag(f'{cid}-excerpt','excerpt motion',f'<img src="{crop["path"]}" alt="Exact excerpt: {e(crop["title"])}">'))
        body.append(tag(f'{cid}-excerpt-label','excerpt-label motion',e(crop['title'])))
        quote=sc.get('quote','')
        body.append(tag(f'{cid}-quote','quote motion',f'“{e(quote)}”<small>Guide p. {sc.get("quote_page",sc["page"])}</small>'))
        motion += [enter(f'#{cid}-page',.15,-60),enter(f'#{cid}-excerpt',T(1)),enter(f'#{cid}-excerpt-label',T(1)+.1),enter(f'#{cid}-quote',T(3))]
        # A quiet opposite-direction anticipation precedes the book/excerpt focus move.
        at=T(3)
        motion += [f"tl.to('#{cid}-excerpt',{{y:8,duration:.1,ease:'power1.in'}},{num(at)});",
                   f"tl.to('#{cid}-excerpt',{{y:-25,duration:.5,ease:'power3.out'}},{num(at+.1)});"]
    elif kind in ['compare','recap']:
        labels=sc['labels'];gap=min(105,450/max(1,len(labels)-1))
        for i,label in enumerate(labels):
            body.append(tag(f'{cid}-row-{i}','compare-row motion',f'<span class="square"></span><span>{e(label)}</span>',f'top:{310+i*gap}px'))
            motion.append(enter(f'#{cid}-row-{i}',T(i)+.1))
        body.append(tag(f'{cid}-mini-page','mini-page motion',f'<img src="assets/book/page-{sc["page"]:03}.jpg" alt="Guide page {sc["page"]}">'))
        motion.append(enter(f'#{cid}-mini-page',.1))
    elif kind=='diagram':
        labels=sc['labels'];count=len(labels);gap=1500/count;xs=[212+i*gap for i in range(count)];w=gap-62
        for i,label in enumerate(labels):
            body.append(tag(f'{cid}-node-{i}','diagram-node motion',e(label),f'left:{xs[i]}px;width:{w}px;top:{410+(i%2)*30}px'))
            motion.append(enter(f'#{cid}-node-{i}',T(i)+.1))
            if i:
                x=xs[i-1]+w+6;y=465+(i%2)*15
                body.append(tag(f'{cid}-arrow-{i}','diagram-arrow motion','→',f'left:{x}px;top:{y}px'))
                motion.append(enter(f'#{cid}-arrow-{i}',T(i),-20))
        body.append(tag(f'{cid}-return','diagram-return motion','<svg viewBox="0 0 1450 150"><path d="M1370 15 V90 H50 V15" fill="none" stroke="#E15B83" stroke-width="4"/><path d="M34 32 L50 15 L66 32" fill="none" stroke="#E15B83" stroke-width="4"/></svg>'))
        final='Feedback closes the loop' if lesson['number']==2 else 'Context connects the steps'
        body.append(tag(f'{cid}-diagram-note','diagram-note motion',e(final)))
        motion += [enter(f'#{cid}-return',T(4)),enter(f'#{cid}-diagram-note',T(4)+.1)]
    elif kind=='question':
        body.append(tag(f'{cid}-prompt','question-prompt motion',e(sc['prompt'])))
        motion.append(enter(f'#{cid}-prompt',.1))
        pause=sc['question_pause'];start=pause['start'];end=start+pause['duration']
        body.append(f'<div id="{cid}-count-label" class="clip countdown" data-start="{num(start)}" data-duration="{num(pause["duration"])}" data-track-index="2"><span>PAUSE &amp; THINK ·</span></div>')
        for i in range(pause['duration']):
            body.append(f'<div id="{cid}-count-{i}" class="clip countdown" style="left:500px;width:80px" data-start="{num(start+i)}" data-duration="1" data-track-index="2"><span>{pause["duration"]-i}</span></div>')
        body.append(tag(f'{cid}-answer','answer motion',e(sc['answer'])))
        motion.append(enter(f'#{cid}-answer',end))
        body.append(tag(f'{cid}-pause-hint','pause-hint motion','Pause the video for more time.'))
        motion.append(enter(f'#{cid}-pause-hint',start))
        motion.append(f"tl.to('#{cid}-pause-hint',{{opacity:0,duration:.15}},{num(end-.15)});")
    elif kind=='credits':
        # Replace the normal heading with a book-sized closing credit.
        body=[body[0],tag(f'{cid}-title','credit-title motion','Blue Impulse<br>study guide')]
        body.append(tag(f'{cid}-cover','credit-cover motion','<img src="assets/book/cover.png" alt="Original Blue Impulse study guide cover">'))
        body.append(tag(f'{cid}-credit-pages','credit-pages motion','Read · pause · practise<br><span>Guide pages '+', '.join(map(str,lesson['pages']))+'</span>'))
        body.append(tag(f'{cid}-credit-end','credit-end motion','Tutorial PDF · Scripts · Subtitles · Demonstration'))
        motion += [enter(f'#{cid}-cover',.15),enter(f'#{cid}-credit-pages',T(1)),enter(f'#{cid}-credit-end',T(2))]
    else:
        raise ValueError(kind)
    style=f'''
#root{{position:relative;width:1920px;height:1080px;overflow:hidden;color:#E6E4E5;font-family:Inter,sans-serif;container-type:size}}
#{cid}-background{{position:absolute;inset:0;background:#212C4A}}
#{cid}-content{{position:absolute;inset:0}}
#{cid}-content .motion{{opacity:0}}
#{cid}-content img{{display:block;width:100%;height:100%;object-fit:contain}}
#{cid}-content .eyebrow{{position:absolute;left:192px;top:108px;font-size:28px;letter-spacing:3px;color:#E15B83}}
#{cid}-content .title{{position:absolute;left:192px;top:158px;width:1536px;font:64px/1.12 Anta;max-height:150px}}
#{cid}-content .cite{{position:absolute;left:192px;top:818px;font-size:28px;color:#E6E4E5}}
#{cid}-content .hook-title{{position:absolute;left:192px;top:278px;width:780px;font:78px/1.12 Anta}}
#{cid}-content .hook-art{{position:absolute;left:1090px;top:244px;width:560px;height:560px}}
#{cid}-content .hook-sub{{position:absolute;left:192px;top:614px;width:850px;color:#E15B83;font-size:38px;line-height:1.25}}
#{cid}-content .book-prompt{{position:absolute;left:192px;top:729px;font-size:34px}}
#{cid}-content b{{font-weight:700}}
#{cid}-content .learning-row{{position:absolute;left:214px;width:1480px;display:flex;gap:36px;align-items:center;font-size:43px;line-height:1.3}}
#{cid}-content .number{{font:58px Anta;color:#E15B83;width:60px;flex-shrink:0}}
#{cid}-content .welcome{{position:absolute;left:310px;top:670px;font:34px/1.4 Inter;color:#E6E4E5}}
#{cid}-content .welcome b{{color:#E15B83}}
#{cid}-content .book-page{{position:absolute;left:192px;top:310px;width:294px;height:416px}}
#{cid}-content .excerpt{{position:absolute;left:560px;top:374px;width:1166px;height:310px;display:flex;align-items:flex-start}}
#{cid}-content .excerpt img{{object-position:top left}}
#{cid}-content .excerpt-label{{position:absolute;left:560px;top:311px;width:1166px;font:34px/1.2 Anta;color:#E15B83}}
#{cid}-content .quote{{position:absolute;left:560px;top:670px;width:1166px;font:32px/1.18 Inter;color:#E6E4E5}}
#{cid}-content .quote small{{display:block;font:28px/1.4 Inter;color:#E15B83;margin-top:8px}}
#{cid}-content .compare-row{{position:absolute;left:212px;width:1080px;display:flex;gap:26px;align-items:center;font-size:38px;line-height:1.24}}
#{cid}-content .square{{display:block;width:16px;height:16px;flex-shrink:0;background:#E15B83}}
#{cid}-content .mini-page{{position:absolute;left:1396px;top:350px;width:275px;height:389px}}
#{cid}-content .diagram-node{{position:absolute;min-height:150px;padding:22px 14px;border:3px solid #E15B83;border-radius:16px;text-align:center;display:flex;align-items:center;justify-content:center;font:35px/1.2 Anta}}
#{cid}-content .diagram-arrow{{position:absolute;font:60px/1 Inter;color:#E15B83}}
#{cid}-content .diagram-return{{position:absolute;left:214px;top:612px;width:1445px;height:150px}}
#{cid}-content .diagram-note{{position:absolute;left:370px;top:756px;width:1160px;font-size:34px;text-align:center}}
#{cid}-content .question-prompt{{position:absolute;left:214px;top:342px;width:1490px;font:55px/1.24 Anta}}
#{cid}-content .countdown{{position:absolute;left:214px;top:592px;width:1490px;height:60px;font:34px/1.3 Inter;color:#E15B83}}
#{cid}-content .answer{{position:absolute;left:214px;top:652px;width:1490px;font:45px/1.22 Anta;color:#E15B83}}
#{cid}-content .pause-hint{{position:absolute;left:214px;top:708px;font-size:30px}}
#{cid}-content .credit-title{{position:absolute;left:192px;top:306px;width:885px;font:91px/1.1 Anta}}
#{cid}-content .credit-cover{{position:absolute;left:1206px;top:181px;width:402px;height:569px}}
#{cid}-content .credit-pages{{position:absolute;left:192px;top:554px;width:934px;font:39px/1.6 Inter;color:#E15B83}}
#{cid}-content .credit-pages span{{font-size:30px;color:#E6E4E5}}
#{cid}-content .credit-end{{position:absolute;left:192px;top:768px;width:1470px;font-size:30px}}
'''
    return f'''<template>
<style>{style}</style>
<div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{num(duration)}">
<div id="{cid}-background" class="clip" data-start="0" data-duration="{num(duration)}" data-track-index="0"></div>
<div id="{cid}-content" class="clip" data-start="0" data-duration="{num(duration)}" data-track-index="1">{''.join(body)}</div>
</div>
<script>
(function(){{const tl=gsap.timeline({{paused:true}});{''.join(motion)}
window.__timelines=window.__timelines||{{}};window.__timelines['{cid}']=tl;}})();
</script>
</template>'''

def build():
    book=json.loads((ROOT/'assets/book/provenance.json').read_text())
    comps=ROOT/'compositions/lessons';comps.mkdir(parents=True,exist_ok=True)
    frames=ROOT/'compositions/frames';frames.mkdir(exist_ok=True)
    entries=ROOT/'entries';entries.mkdir(exist_ok=True)
    outputs=[]
    for path in sorted(ROOT.glob('lesson-??.json')):
        lesson=json.loads(path.read_text());n=lesson['number'];duration=lesson['duration'];hosts=[];missing=[]
        for i,sc in enumerate(lesson['scenes']):
            if sc['kind'] in CUSTOM:
                source=frames/(sc['kind']+'.html')
                if not source.exists():missing.append(str(source));continue
                text=source.read_text()
                # Re-synchronize only explicit constants and full-duration layer attributes.
                text=re.sub(r'const\s+BEATS\s*=\s*\[[^\]]*\]\s*;', 'const BEATS = '+json.dumps([b['start'] for b in sc['beats']])+';',text)
                scene_captions=[dict(start=round(c['start']-sc['start'],6),
                                     end=round(c['end']-sc['start'],6),text=c['text'])
                                for c in lesson['captions']
                                if sc['start']-.00001 <= c['start'] < sc['start']+sc['duration']-.00001]
                text=re.sub(r'const\s+CAPTIONS\s*=\s*\[\s*\]\s*;',
                            lambda match: 'const CAPTIONS = '+json.dumps(scene_captions)+';',text)
                text=re.sub(r'const\s+DURATION\s*=\s*[0-9.]+\s*;', 'const DURATION = '+num(sc['duration'])+';',text)
                text=re.sub(r'data-duration=["\']60["\']',f'data-duration="{num(sc["duration"])}"',text)
                target=comps/f'v{n:02}-{i:02}-{sc["kind"]}.html';target.write_text(text)
                cid=sc['kind']
            else:
                target=comps/f'v{n:02}-{i:02}-{sc["key"]}.html';target.write_text(common_scene(lesson,sc,i,book));cid=f'v{n:02}-s{i:02}'
            hosts.append(f'<div id="host-{n:02}-{i:02}" class="clip" data-composition-src="compositions/lessons/{target.name}" data-composition-id="{cid}" data-start="{num(sc["start"])}" data-duration="{num(sc["duration"])}" data-track-index="1" data-track-kind="graphics"></div>')
        if missing:
            print(f'Video {n:02}: awaiting custom frame {missing}');continue
        capid=f'captions-{n:02}'
        capnodes=[]
        capmotion=[]
        for j,c in enumerate(lesson['captions']):
            lines=textwrap.wrap(c['text'],width=64,break_long_words=False,break_on_hyphens=False)
            if len(lines)>2:
                # Caption layout uses measured full cue duration; never invent word times.
                width=max(64,(len(c['text'])+1)//2+5);lines=textwrap.wrap(c['text'],width=width,break_long_words=False,break_on_hyphens=False)
            capnodes.append(f'<div id="caption-{n:02}-{j:03}" class="clip cuebox" data-start="{num(c["start"])}" data-duration="{num(c["end"]-c["start"])}" data-track-index="0"><span>'+ '<br>'.join(e(line) for line in lines)+'</span></div>')
            selector=f'#caption-{n:02}-{j:03} span'
            # Explicit child visibility also clears captions when seeking into a silent gap.
            capmotion.append(f"tl.fromTo('{selector}',{{opacity:0}},{{opacity:1,duration:.00001,immediateRender:false}},{num(c['start'])});")
            capmotion.append(f"tl.to('{selector}',{{opacity:0,duration:.00001}},{num(c['end'])});")
        (comps/f'{capid}.html').write_text(f'''<template><style>#root{{position:relative;width:1920px;height:1080px}}.cuebox{{position:absolute;left:196px;top:872px;width:1528px;height:100px;display:flex;align-items:center;justify-content:center;text-align:center;font:42px/48px Inter;color:#E6E4E5}}.cuebox span{{background:#212C4A;padding:2px 16px;opacity:0}}</style><div id="root" data-composition-id="{capid}" data-width="1920" data-height="1080" data-duration="{num(duration)}">{''.join(capnodes)}</div><script>(function(){{const tl=gsap.timeline({{paused:true}});{''.join(capmotion)}window.__timelines=window.__timelines||{{}};window.__timelines['{capid}']=tl;}})();</script></template>''')
        hosts.append(f'<div id="host-captions-{n:02}" class="clip" data-composition-src="compositions/lessons/{capid}.html" data-composition-id="{capid}" data-start="0" data-duration="{num(duration)}" data-track-index="3" data-track-kind="captions" style="z-index:20;pointer-events:none"></div>')
        hosts.append(f'<audio id="voice-{n:02}" class="clip" src="{lesson["audio"]}" data-start="0" data-duration="{num(duration)}" data-track-index="4" data-volume="1"></audio>')
        root=f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920,height=1080"><title>Blue Impulse — {e(lesson['title'])}</title><script src="assets/gsap.min.js"></script><style>{FONT_CSS}*{{box-sizing:border-box;margin:0}}html,body{{width:1920px;height:1080px;overflow:hidden;background:#212C4A}}#root{{position:relative;width:100%;height:100%;background:#212C4A}}.clip{{position:absolute}}</style></head><body><div id="root" data-composition-id="main-{n:02}" data-start="0" data-duration="{num(duration)}" data-width="1920" data-height="1080" data-fps="30">{''.join(hosts)}</div><script>(function(){{const tl=gsap.timeline({{paused:true}});window.__timelines=window.__timelines||{{}};window.__timelines['main-{n:02}']=tl;}})();</script></body></html>'''
        out=entries/(f'video-{n:02}.html.in');out.write_text(root)
        if n==1:(ROOT/'index.html').write_text(root)
        old=ROOT/(f'video-{n:02}.html')
        if old.exists():old.unlink()
        outputs.append(dict(number=n,file=out.name,duration=duration,scenes=len(lesson['scenes']),captions=len(lesson['captions'])))
        print(f'Video {n:02}: built {len(lesson["scenes"])} scenes, {len(lesson["captions"])} captions, {duration:.2f}s')
    (ROOT/'build/video-build.json').write_text(json.dumps(outputs,indent=2)+'\n')

if __name__=='__main__':build()
