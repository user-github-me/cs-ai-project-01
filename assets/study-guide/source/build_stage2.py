"""Build self-contained Markdown V2 and Study Guide/Test Bank V1 submissions.

Run after build_guide.py to create the original-art base. This script preserves
its first 96 pages and appends activities, resource introductions and feedback.
"""
from pathlib import Path
import sys,json,re,hashlib,shutil,subprocess,zipfile,tempfile
from collections import Counter
from html import escape
import fitz
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from guide_content import PAGES
from exercises import EXERCISES
from reference_content import TITLES,GOALS,TERMS
from stage2_learning import ANSWERS,CHECKS,MISSIONS,RESOURCES,CHAPTER_REFS
from stage2_testbank import TF,MC,OE
from stage2_documents import render_markdown

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'assets/study-guide'
CONTENT=ROOT/'content'
SUB=ROOT/'submissions/stage2'
MD=SUB/'markdown';SG=SUB/'study-guide'
REVIEW=BASE/'source/stage2-review'
for p in [MD,SG,REVIEW,CONTENT/'supporting']:p.mkdir(parents=True,exist_ok=True)
REPO='https://github.com/user-github-me/cs-ai-project-01'
DATE='7 November 2026 (UTC+8)'

def write(path,text):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text.strip()+'\n')

def table(headers,rows):
 clean=lambda v:str(v).replace('|','/').replace('\n',' ')
 return '\n'.join(['| '+' | '.join(map(clean,headers))+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(clean,row))+' |' for row in rows])

def resource_md(r,level=2):
 return ('#'*level+' '+r['id']+' — '+r['title']+'\n\n'+r['provider']+'.\n\n'+r['url']+'\n\n'+
 '\n\n'.join('**'+k+':** '+r[field] for k,field in [('Relevant section','section'),('Why use it','why'),('Learner task','task'),('Limits','limit'),('Offline alternative','fallback')])+\
 '\n\n**Access:** Optional public web resource; no account required to read the cited page. Signed-out HTTP access was checked on 7 November 2026. Availability on every campus network is not guaranteed. All essential task instructions and feedback are supplied locally.\n')

def mission_md(m,level=2):
 s='#'*level+' '+m['id']+' — '+m['title']+'\n\n**Chapter '+str(m['chapter'])+' — '+TITLES[m['chapter']]+'**\n\n'+m['hook']+'\n\n'
 for title,key in [('Goal','goal'),('Preparation','prep')]:s+='**'+title+':** '+m[key]+'\n\n'
 s+='**Task:**\n\n'+'\n'.join(str(i+1)+'. '+step for i,step in enumerate(m['steps']))+'\n\n'
 for title,key in [('Observe and record','observe'),('Reflect','reflect'),('Feedback — check after trying','feedback')]:s+='**'+title+':** '+m[key]+'\n\n'
 s+='**Optional resource:** '+m['resource']+' (full introduction and offline alternative follow).\n\n'
 return s

MODULE='''# Blue Impulse — Markdown Content V2.0

**Module:** Hardware, Networking and Behaviorist AI — How Machines Sense, Connect and Act  
**Team:** Blue Impulse  
**Version:** Stage 2, V2.0  
**Snapshot:** 7 November 2026, Beijing time

## Start here

A small campus delivery rover, Pip, must sense the world, choose useful actions and execute them on real hardware. The rover is fictional; its message identifier in the worked protocol examples is robot-7. Its problems connect the six chapters without claiming that every smart device learns or that a successful demo proves a safe deployment.

You need basic arithmetic and a willingness to record predictions. No programming experience, online account or paid tool is required. Paper versions contain every input and expected result. Optional code requires Python 3.9 or newer and uses only the standard library.

Read each chapter’s outcomes, then one topic at a time. Study the worked explanation, attempt its application checkpoint, compare the feedback and explain any difference. Complete the chapter mission before the exercises, then use the separate solutions to review your reasoning. Use the glossary when a term is unfamiliar. The separate Test Bank places all questions before the answer key.

## Learning route and outcomes

'''+table(['Chapter','Learning outcome','Mission'],[[str(c)+' — '+TITLES[c],GOALS[c],MISSIONS[c-1]['id']+' — '+MISSIONS[c-1]['title']] for c in range(1,7)])+'''

## What is included

Every chapter contains developed explanations, diagrams expressed as readable flows/tables, an application checkpoint with feedback for each topic, a substantial mission, a glossary, exercises, answers and specific references. Source notes distinguish textbook-derived material, technical standards, fictional examples, team-provided art and AI-assisted revision.

The original guide source supplied the existing developed explanations. On 7 November they were reconciled into this shared Markdown foundation; future edits should start here and update the guide, slides and tutorials. This is a documented repair of a missing Markdown foundation, not a claim that the earlier production already followed the desired sequence.

## Navigation

'''+ '\n'.join(f'- [Chapter {c}: {TITLES[c]}](chapter-{c:02d}/README.md)' for c in range(1,7))+'''
- [Curated resources and attribution](references.md)
- [Activity setup and expected results](supporting/README.md)
- [Review status and evidence](REVIEW.md)

## Review status

Automated checks and AI-assisted content review are recorded in the supplied evidence. A teammate must still independently attempt every Test Bank question and selected activities. No teacher feedback, learner test or student reflection has been invented. The remaining human review requirement is explicit in the submission report.
'''


def build_content():
 assert set(ANSWERS)==set(EXERCISES)
 assert set(CHECKS)=={p['key'] for p in PAGES}
 write(CONTENT/'README.md',MODULE)
 resources='# Blue Impulse — References and resource introductions\n\n'+\
 'The six team-supplied chapter PDFs defined the scope. Their notes credit Cambridge International AS & A Level Computer Science but do not identify a full edition or author bibliography; this remains a provenance limitation and no edition has been invented. The new activities, calculations and checkpoints are original AI-assisted teaching examples. The guide’s original artwork is user supplied and retains its own third-party rights.\n\n'+\
 'The resources below were inspected as optional extensions and reference support. No external link replaces an explanation, input, question or answer in this snapshot. No student-created website or external platform is required.\n\n'+ '\n'.join(resource_md(r) for r in RESOURCES)
 resources+='\n## Responsible AI-use record\n\nNeogpt/Codex assisted on 7 November 2026 with reconciling the guide into Markdown, developing activities and answers, drafting the Test Bank, generating PDFs/DOCX and verifying package structure. The user asked to follow rules/Stage2_All_Instructions.md. Calculations and supplied code outputs were checked locally; source/resource access and document checks are recorded in the submission evidence. These checks are not independent human peer review. Significant interaction excerpts belong in the project and personal logs.\n'
 write(CONTENT/'references.md',resources)
 all_sections=[MODULE]
 for ch in range(1,7):
  folder=CONTENT/f'chapter-{ch:02d}';pages=[p for p in PAGES if p['chapter']==ch]
  header=f'# Chapter {ch} — {TITLES[ch]}\n\n'
  readme=header+f'**Learning outcome:** {GOALS[ch]}\n\n'+\
   f'**Route:** Read the [developed chapter](draft.md), try [{MISSIONS[ch-1]["id"]}](activities.md), then answer [exercises](exercises.md) before opening [solutions](solutions.md). Keep the [glossary](Key_Terms_{ch}.md) nearby.\n\n'+\
   '## Topics\n\n'+'\n'.join('- '+p['title'] for p in pages)+'\n\n**Status:** All core sections contain learning content and feedback. Independent teammate review is pending; see ../REVIEW.md.\n'
  write(folder/'README.md',readme)
  draft=header+f'**Learning outcome:** {GOALS[ch]}\n\n'+\
   ('**Prerequisites:** Basic arithmetic; Chapter 1 supplies representation and execution foundations.\n\n' if ch==1 else f'**Prerequisites:** Read the relevant earlier chapters; this chapter connects those ideas to {TITLES[ch].lower()}.\n\n')
  for p in pages:
   draft+=f'## {p["title"]}\n\n'
   for b in p['blocks']:
    draft+=f'### {b["title"]}\n\n'
    if b['kind']=='text':draft+=b['text']+'\n\n'
    elif b['kind']=='table':draft+=table(b['headers'],b['rows'])+'\n\n'
    else:draft+=table(['Step / element','Meaning in the diagram'],[[str(i+1),label] for i,label in enumerate(b['labels'])])+'\n\n'+b.get('caption','')+'\n\n'
   q,a=CHECKS[p['key']]
   draft+='### Apply and check\n\n**Try before reading feedback:** '+q+'\n\n**Feedback:** '+a+'\n\n'
   draft+='**Practice connection:** Exercise '+p['exercise']+' in exercises.md; explained answer in solutions.md.\n\n'
  draft+='## Chapter review\n\nComplete '+MISSIONS[ch-1]['id']+' using the supplied mission instructions. Then choose two related terms and explain a mechanism using both; identify one limitation of the teaching model and one condition that could change the result.\n\n'
  draft+='## Reference support\n\n'+'\n'.join('- '+r['id']+': '+r['title']+' — '+r['section']+'. '+r['url'] for r in RESOURCES if r['id'] in CHAPTER_REFS[ch])+'\n\nFull resource introductions, optional tasks and access alternatives are in ../references.md.\n'
  write(folder/'draft.md',draft)
  goals=header+'## Learning outcomes\n\n'+GOALS[ch]+'\n\nBy the end, explain the chapter’s mechanisms, apply them to the mission, and justify a design decision using its constraints. Check learning by completing the application checkpoints and exercises without first reading feedback.\n'
  write(folder/f'Learning_Outcomes{ch}.md',goals)
  terms=header+'## Key terms\n\n'+table(['Term','Meaning'],TERMS[ch])
  write(folder/f'Key_Terms_{ch}.md',terms)
  exercise=header+'## Exercises\n\nWrite reasoning, units and intermediate steps. All necessary concepts are explained in draft.md; the answer key is in solutions.md. The numbering preserves the source questions used throughout the guide.\n\n'
  solutions=header+'## Explained answers\n\nThese are expected answers, not the only acceptable wording. Credit a correct alternative with clear assumptions and reasoning. Try the exercises before reading this section.\n\n'
  for key,val in EXERCISES.items():
   if int(key.split('.')[0])!=ch:continue
   exercise+=f'### Exercise {key}\n\n{val}\n\n'
   solutions+=f'### Answer {key}\n\n{ANSWERS[key]}\n\n'
  write(folder/'exercises.md',exercise);write(folder/'solutions.md',solutions)
  activity='# Chapter '+str(ch)+' — Mission and optional resource\n\n'+mission_md(MISSIONS[ch-1])+resource_md(next(r for r in RESOURCES if r['id']==MISSIONS[ch-1]['resource']))
  write(folder/'activities.md',activity)
  # Preserve historical AI notes while adding an explicit real revision record.
  ai=folder/'UseOfAI.md';old=ai.read_text() if ai.exists() else ''
  marker='## Stage 2 revision — 7 November 2026'
  old=old.split(marker)[0].rstrip()
  write(ai,old+'\n\n'+marker+'\n\nNeogpt/Codex assisted with importing the already developed guide explanations into Markdown, adding application checkpoints and feedback, the chapter mission, and explained answers. The request was to follow rules/Stage2_All_Instructions.md. Evidence includes checked calculations and executable demonstrations plus the Stage 2 review report. This records AI-assisted production, not a claim of independent student understanding or human peer review. Full user-specific evidence is kept in project and personal logs.\n')
  all_sections.extend([draft,activity,terms,exercise,solutions])
 all_sections.append(resources)
 write(CONTENT/'BlueImpulse_Complete_Content_V2.md','\n\n'.join(all_sections))
 source=CONTENT/'supporting/BlueImpulse_Demonstrations.py'
 setup='''# Blue Impulse — Offline activity setup

All six missions work with paper and the data in the chapter. For five optional demonstrations, use Python 3.9 or newer; no third-party package, account, internet connection or API key is required.

From this folder run:

```sh
python3 BlueImpulse_Demonstrations.py --topic all
python3 BlueImpulse_Demonstrations.py --topic execution --add 9
python3 BlueImpulse_Demonstrations.py --topic network --speed 2
```

The available topic values are `rl`, `hardware`, `network`, `networked-ai`, and `execution`. Output is JSON so a learner can compare exact intermediate states. `expected-results.json` records the default output; `modified-results.json` records the two changes above. The toy models are deliberately limited: no physical braking simulation, cryptographic authentication or real ISA is implemented. ACT-06 uses a supplied fictional design table and needs no code.
'''
 write(CONTENT/'supporting/README.md',setup)
 out=subprocess.check_output([sys.executable,str(source),'--topic','all'],text=True)
 write(CONTENT/'supporting/expected-results.json',out)
 changed={}
 for key,args in [('execution-add9',['--topic','execution','--add','9']),('network-speed2',['--topic','network','--speed','2'])]:
  changed[key]=json.loads(subprocess.check_output([sys.executable,str(source),*args],text=True))
 write(CONTENT/'supporting/modified-results.json',json.dumps(changed,indent=2))
 return resources


def testbank_markdown():
 s='''# Blue Impulse — Stage 2 Test Bank V1.0

**Module:** Hardware, Networking and Behaviorist AI  
**Version/date:** V1.0 — 7 November 2026  
**Coverage:** Six chapters; 24 True/False, 24 single-answer Multiple Choice and 6 open-ended tasks.

## Instructions

Attempt the questions before reading the answer key. For True/False, correct any false statement. For multiple choice, select exactly one answer. Open responses require developed reasoning: normally at least 120 words (150 for OE06), or an equivalent labelled diagram, decision matrix, calculations or worked trace with explanations. Every question includes its own required numerical data; no online platform is needed. Suggested self-assessment: 1 mark for each T/F decision plus 1 for reasoning; 1 mark for each MC choice plus 1 for reasoning; 10 marks for each open response. Total 156 marks. This is a practice allocation, not a teacher-issued grading scheme.

'''
 s+='## Questions — True/False\n\n'
 for i,(ch,topic,q,answer,why) in enumerate(TF,1):s+=f'### TF{i:02d} — Chapter {ch}: {TITLES[ch]} / {topic}\n\n{q}\n\n'
 s+='## Questions — Multiple Choice\n\n'
 for i,(ch,topic,q,options,answer,why) in enumerate(MC,1):
  s+=f'### MC{i:02d} — Chapter {ch}: {TITLES[ch]} / {topic}\n\n{q}\n\n'+ '\n\n'.join(f'{chr(65+j)}. {v}' for j,v in enumerate(options))+'\n\n'
 s+='## Questions — Open-ended\n\n'
 for i,(ch,topic,q,points,sample) in enumerate(OE,1):s+=f'### OE{i:02d} — Chapter {ch}: {TITLES[ch]} / {topic}\n\n{q}\n\n'
 s+='# Answer key — read after attempting all questions\n\n## True/False answers and corrections\n\n'
 for i,(ch,topic,q,a,why) in enumerate(TF,1):s+=f'### TF{i:02d}: {"True" if a else "False"}\n\n{why}\n\n'
 s+='## Multiple-choice answers and reasoning\n\n'
 for i,(ch,topic,q,opts,a,why) in enumerate(MC,1):s+=f'### MC{i:02d}: {a}\n\n{why}\n\n'
 s+='## Open-ended expected points and sample responses\n\nValid alternatives receive credit when justified with correct assumptions and evidence. These sample responses demonstrate one acceptable line of reasoning.\n\n'
 for i,(ch,topic,q,points,sample) in enumerate(OE,1):
  s+=f'### OE{i:02d} — expected points (10 marks)\n\n'+'\n'.join('- '+x for x in points)+'\n\n**Sample response:** '+sample+'\n\n'
 s+='## Review and provenance\n\nThis question set was AI-assisted and checked for coverage, arithmetic, answer alignment and document completeness on 7 November 2026. It has not been recorded as independently attempted by another team member. That mandatory human review remains pending and must be documented honestly. Questions are original teaching material based on the module; chapter references and resource attribution are included in the complete Study Guide and Markdown snapshot.\n'
 return s


def make_docx(text,path):
 d=Document();sec=d.sections[0];sec.top_margin=Inches(.7);sec.bottom_margin=Inches(.7)
 normal=d.styles['Normal'];normal.font.name='Aptos';normal.font.size=Pt(10.5)
 normal.paragraph_format.space_after=Pt(6)
 for name in ['Title','Heading 1','Heading 2','Heading 3']:
  d.styles[name].font.name='Aptos Display';d.styles[name].font.color.rgb=RGBColor.from_string('162144')
 first=True
 for line in text.splitlines():
  if not line.strip():continue
  line=line.replace('**','').replace('  ',' ')
  if line.startswith('# '):
   if not first:d.add_page_break()
   d.add_heading(line[2:],0);first=False
  elif line.startswith('## '):d.add_heading(line[3:],1)
  elif line.startswith('### '):d.add_heading(line[4:],2)
  elif line.startswith('- '):d.add_paragraph(line[2:],'List Bullet')
  else:d.add_paragraph(line)
 footer=sec.footer.paragraphs[0];footer.alignment=2
 footer.add_run('Blue Impulse | Stage 2 Test Bank | ')
 field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
 d.core_properties.title='Blue Impulse Stage 2 Test Bank V1.0';d.core_properties.author='Blue Impulse';d.save(path)


def guide_appendix(resources):
 s='''# Active learning route and feedback

**Blue Impulse Study Guide V1.0 — Stage 2 complete edition, 7 November 2026**

This complete edition preserves the original cover, chapter dividers and developed teaching pages, then adds the active learning missions, optional resource introductions and explained exercise answers. The story follows Pip, a fictional campus delivery rover; robot-7 is its identifier in the packet exercise. Fictional model measurements are labelled and are not research results.

## How to use the complete guide

Start with the learning goals and core explanations. In every chapter, pause at the exercise and make a prediction before reading feedback. Use the matching chapter mission below to apply the ideas, record the result and explain why it happens. Then compare the expected answer and try a changed input. The answer key is placed after all six missions so learners can attempt the questions first.

Prerequisites are basic arithmetic and the earlier chapters in sequence. Paper and a calculator are sufficient. Optional code is supplied in the submission’s supporting folder and needs Python 3.9 or newer, with no extra packages or account. The separate editable Test Bank provides 54 balanced questions for review; its questions come before its answer key. Human peer review remains pending, as documented in the package’s review record.

## Complete edition navigation

The original six-chapter contents and bookmarks remain usable. Additional PDF bookmarks open each mission, resource introduction and explained-answer section. The teaching topics remain named consistently across Markdown, slides and videos; revised videos cite chapter number, chapter name and subtopic rather than page numbers.

'''
 for m in MISSIONS:
  s+='# Mission '+str(m['chapter'])+' — '+m['title']+'\n\n'+mission_md(m,2)+resource_md(next(r for r in RESOURCES if r['id']==m['resource']))+'\n'
 s+='# Exercise answer key\n\nAttempt the original guide exercises first. Match each question number with the explained answer below. Equivalent correct explanations and clearly stated alternative assumptions are acceptable.\n\n'
 for ch in range(1,7):
  s+=f'## Chapter {ch} — {TITLES[ch]}\n\n'
  for key,val in ANSWERS.items():
   if int(key.split('.')[0])==ch:s+=f'### Answer {key}\n\n{val}\n\n'
 s+='# Sources, access and revision notes\n\n'+resources.split('\n',1)[1]
 return s


def append_guide(resources):
 appmd=guide_appendix(resources);write(BASE/'BlueImpulse_Active_Learning_and_Feedback.md',appmd)
 apppdf=REVIEW/'guide-appendix.pdf';render_markdown(appmd,apppdf,'Blue Impulse — Active learning and feedback','Study Guide V1.0 • Activity and answer section',page_offset=96)
 original=fitz.open(BASE/'BlueImpulse_Study_Guide.pdf');assert len(original)>=96
 final=fitz.open();final.insert_pdf(original,from_page=0,to_page=95)
 app=fitz.open(apppdf);final.insert_pdf(app)
 toc=[x for x in original.get_toc() if x[2]<=96]
 for lev,title,number in app.get_toc():toc.append([1,title,number+96])
 final.set_toc(toc)
 final.set_metadata({'title':'Blue Impulse Study Guide V1.0 — How Machines Sense, Connect and Act','author':'Blue Impulse','subject':'Stage 2 complete guide with activities, resources and explained answers','creator':'Blue Impulse / Neogpt-Codex; ReportLab and PyMuPDF'})
 tmp=BASE/'study-guide-stage2.tmp.pdf';final.save(tmp,garbage=4,deflate=True);final.close();original.close();app.close();tmp.replace(BASE/'BlueImpulse_Study_Guide.pdf')
 manifest=json.loads((BASE/'manifest.json').read_text());manifest.update(version='Stage 2 V1.0 complete',pages=len(fitz.open(BASE/'BlueImpulse_Study_Guide.pdf')),base_pages=96,appendix_start=97,sha256=hashlib.sha256((BASE/'BlueImpulse_Study_Guide.pdf').read_bytes()).hexdigest())
 write(BASE/'manifest.json',json.dumps(manifest,indent=2))
 return manifest


def reports(manifest):
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 hist=subprocess.check_output(['git','log','-8','--format=%h | %ad | %s','--date=short'],cwd=ROOT,text=True).strip()
 review='''# Blue Impulse — Stage 2 content review

**Date:** 7 November 2026. **Review type:** automated checks and AI-assisted content review, not independent student review.

## Completed and evidenced

- All 67 guide topics have developed Markdown explanations and a specific application checkpoint with feedback.
- All 65 retained source exercise IDs have explained answers.
- Six missions specify goals, preparation, steps, observations, reflection and expected outcomes; they run on paper without an external service.
- Five optional standard-library Python demonstrations were run, including changed program and speed inputs. Exact JSON outputs are bundled with the source.
- The Test Bank contains 24 T/F, 24 single-answer MCQ and six substantive open tasks: exactly 4/4/1 per chapter. All questions precede the answer key. Each open task has explicit expected points totalling 10 marks and a developed sample response.
- Resource pages R1–R6 returned HTTP 200 in signed-out requests. Their identity and relevant subject matter were inspected. External resources are optional and every task has a complete offline explanation or trace.
- Original cover and all six dividers are retained without overlays. The complete guide adds activities and answer feedback after the existing core.
- Final PDFs are checked for readable selectable text and page bounds; packages are extracted and compared by SHA-256.

## Required human evidence still unavailable

The rules require a different team member to attempt every Test Bank question and selected learning activities. No such attempt or learner feedback has been supplied in this session. The assistant cannot stand in for an independent student. A reviewer must record their name, actual answers/results, confusion, revisions and date in the project and personal logs. Teacher feedback specific to the six-chapter content was not available; this revision therefore records observed repository gaps and the user’s instructions instead of inventing feedback.

The team must also confirm that every member has read and understood their contribution, and complete authentic contribution/learning records. These are submission-process gaps, not hidden content placeholders. No unperformed meeting, learner test, rehearsal or reflection is claimed.
'''
 write(CONTENT/'REVIEW.md',review)
 mapping=[]
 videos={1:'Video 05 — Program Execution',2:'Video 01 — Basic Reinforcement Learning',3:'Video 02 — How Hardware Enables AI; Video 05 pipeline link',4:'Video 03 — Network Challenges',5:'Video 04 — Networking for Behaviorist AI; Video 03 deadline link',6:'Not selected as a standalone video; limitations integrated across tutorials'}
 for ch in range(1,7):mapping.append([f'content/chapter-{ch:02d}/draft.md — {TITLES[ch]}',f'Guide chapter {ch}; ACT-{ch:02d}; TF{(ch-1)*4+1:02d}–TF{ch*4:02d}, MC{(ch-1)*4+1:02d}–MC{ch*4:02d}, OE{ch:02d}',f'Six-chapter classroom teaching deck — Chapter {ch} {TITLES[ch]}',videos[ch]])
 report=f'''# Blue Impulse — Markdown V2.0 submission report

**Team:** Blue Impulse  
**Module:** Hardware, Networking and Behaviorist AI  
**Snapshot date:** {DATE}  
**Repository (supplementary):** {REPO}  
**Historical repository baseline (HEAD before the uncommitted snapshot changes):** {commit}

This package includes the complete updated Markdown source and supporting assets, the full rendered content PDF and this report. The files contain uncommitted Stage 2 revisions made after the identified baseline; the SHA-256 manifest fixes the submitted snapshot independently of a later upload commit. GitHub links are supplementary; current access settings are recorded in the repository README. The supplied PDF and snapshot contain the required learning content directly.

## Revision summary

'''+table(['Observed problem / instruction','Change and reason','Location'],[
 ['Chapter draft/readme files contained placeholders such as “put your draft here la!!!!!”.','Reconciled all 67 developed guide topics into substantive Markdown, adding application and feedback checkpoints.','content/chapter-01…06/draft.md; content/topic-map.json'],
 ['Chapter solutions were placeholders and the guide explicitly omitted the answer key.','Added 65 explained answers with matching preserved IDs; appended feedback to the complete guide.','content/chapter-01…06/solutions.md; guide answer appendix'],
 ['Activities lacked a consistent goal/task/observation/feedback sequence.','Created ACT-01…06 with a fictional Pip story, full inputs, predictions, reflection and offline feedback.','content/chapter-01…06/activities.md'],
 ['No separate minimum-compliant editable Test Bank.','Added 24 T/F, 24 MCQ and 6 open tasks, balanced equally across six chapters, with questions first and explanatory key later.','BlueImpulse_Stage2_TestBank_V1.docx and matching Markdown/PDF'],
 ['Sources in supplied PDFs lacked a complete textbook bibliography.','Documented the limitation and added six traceable optional resources with section guidance, tasks, access notes and fallbacks.','content/references.md; mission resource introductions'],
 ['New user direction removes guide screenshots/page citations from tutorials.','Preserved stable chapter names/subtopic titles and added a machine-readable topic map for all resources.','content/topic-map.json; resource mapping below'],
 ['Required independent human checks have no available evidence.','Marked the requirement pending rather than fabricating peer attempts, feedback or learning.','content/REVIEW.md; package verification record']])+\
 '\n\n## Review results\n\n'+review.split('## Completed and evidenced')[1].split('## Required human evidence')[0]+\
 '\n## Resource mapping\n\n'+table(['Markdown topic','Study Guide / Test Bank','PPT use','Video use'],mapping)+\
 '\n\nThe slides/videos adapt this foundation for their media; not every paragraph appears in every resource. Topic references use the canonical chapter number/name/subtopic. The visual and narration revision is coordinated in the project repository; package-specific media checks belong to the video and slides submissions.\n\n## Selected development evidence\n\nThe following actual commit history is reproduced so the report does not rely on a web link:\n\n```text\n'+hist+'\n```\n\n'+\
 'The earlier study-guide and video commits demonstrate prior production. The current revision repairs the missing shared Markdown source and feedback. For example, content/chapter-03/draft.md previously contained “put your draft here la!!!!!”; it now develops thirteen hardware topics. The new pipeline checkpoint asks for five instructions in four ideal stages and explains 4 + 5 − 1 = 8 cycles. The original solutions file’s request for future answers is replaced by worked answers, including exact binary, image-size, Q-update and network-delay calculations.\n\n'+\
 'The guide and paper mission now agree that a 200 ms delay at 30 m/s contributes 6 m of delay distance, not complete stopping distance. ACT-05 records ACCEPT / STALE / DUPLICATE with accepted sequence state 42 / 42 / 42, matching the executable demonstration. These are concrete revisions and results rather than a count of commits.\n\n'+\
 '## Remaining process gaps and next steps\n\n'+review.split('## Required human evidence still unavailable')[1]+'\n\nThe development history is preserved honestly: the initial guide was produced before this complete Markdown reconstruction. The present package is the reconciled V2 foundation for subsequent revision, not a backdated claim of workflow compliance.\n'
 write(MD/'BlueImpulse_Stage2_Markdown_Submission_Report.md',report)
 render_markdown(report,MD/'BlueImpulse_Stage2_Markdown_Submission_Report.pdf','Blue Impulse Markdown V2 submission report','Snapshot and review evidence')
 write(SG/'REVIEW.md',review)
 return report


def package(folder,name,paths):
 zpath=folder/name;entries=[]
 for src,relative in paths:
  if src.is_dir():
   for file in sorted(src.rglob('*')):
    if file.is_file() and '__pycache__' not in file.parts and file.name!='.DS_Store':entries.append((file,Path(relative)/file.relative_to(src)))
  else:entries.append((src,Path(relative)))
 records={str(dst):{'bytes':src.stat().st_size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()} for src,dst in entries}
 assert len(records)==len(entries)
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for src,dst in entries:z.write(src,str(dst))
  z.writestr('MANIFEST.json',json.dumps({'snapshot':DATE,'files':records},indent=2))
 with tempfile.TemporaryDirectory(prefix='blue-impulse-stage2-extract-') as tmp:
  with zipfile.ZipFile(zpath) as z:
   assert z.testzip() is None;z.extractall(tmp)
  for rel,rec in records.items():assert hashlib.sha256((Path(tmp)/rel).read_bytes()).hexdigest()==rec['sha256'],rel
  for p in Path(tmp).rglob('*.pdf'):
   d=fitz.open(p);assert len(d)>0;d[0].get_pixmap(matrix=fitz.Matrix(.2,.2));d.close()
  for p in Path(tmp).rglob('*.docx'):assert len(Document(p).paragraphs)>0
 return {'file':str(zpath.relative_to(ROOT)),'bytes':zpath.stat().st_size,'sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'files':len(records),'extracted_and_hash_checked':True}


def main():
 resources=build_content()
 bank=testbank_markdown();write(CONTENT/'BlueImpulse_Stage2_TestBank_V1.md',bank)
 make_docx(bank,BASE/'BlueImpulse_Stage2_TestBank_V1.docx')
 render_markdown(bank,BASE/'BlueImpulse_Stage2_TestBank_V1.pdf','Blue Impulse Stage 2 Test Bank V1','Questions first • Explanatory answer key later')
 # The complete content PDF deliberately includes the full separate test bank too.
 allmd=(CONTENT/'BlueImpulse_Complete_Content_V2.md').read_text()+'\n\n'+bank
 render_markdown(allmd,MD/'BlueImpulse_Stage2_Markdown_V2_Content.pdf','Blue Impulse Complete Markdown Content V2','Six chapters • Activities • Answers • Test Bank')
 manifest=append_guide(resources)
 reports(manifest)
 shutil.copy2(BASE/'BlueImpulse_Study_Guide.pdf',SG/'BlueImpulse_Stage2_StudyGuide_V1.pdf')
 for ext in ['docx','pdf']:shutil.copy2(BASE/f'BlueImpulse_Stage2_TestBank_V1.{ext}',SG/f'BlueImpulse_Stage2_TestBank_V1.{ext}')
 shutil.copytree(CONTENT/'supporting',SG/'supporting',dirs_exist_ok=True)
 write(SG/'README.md',f'''# Blue Impulse — Study Guide and Test Bank V1

Open BlueImpulse_Stage2_StudyGuide_V1.pdf ({manifest['pages']} pages) for the complete guide, then BlueImpulse_Stage2_TestBank_V1.docx for an editable 54-question bank with explained answers. A PDF copy of the bank is included. Supporting code and exact expected results are in supporting/; every activity also works offline on paper. See REVIEW.md for verified checks and the required independent human review that remains pending. The original compressed PDF made by the user was not modified.
''')
 # Required snapshot includes the current repository README and working content structure.
 snapshot=MD/'source-snapshot'
 if snapshot.exists():shutil.rmtree(snapshot)
 snapshot.mkdir();shutil.copytree(CONTENT,snapshot/'content')
 (snapshot/'rules').mkdir();shutil.copy2(ROOT/'rules/Stage2_All_Instructions.md',snapshot/'rules/Stage2_All_Instructions.md')
 if (ROOT/'task.md').exists():shutil.copy2(ROOT/'task.md',snapshot/'task.md')
 current_readme=(ROOT/'README.md').read_text()
 shutil.copy2(ROOT/'README.md',snapshot/'REPOSITORY_README_ORIGINAL.txt')
 from urllib.parse import unquote,quote
 def snapshot_link(match):
  label,target=match.group(1),match.group(2)
  if target.startswith(('http:','https:','#','mailto:')):return match.group(0)
  local=unquote(target.split('#')[0].strip('<>'))
  if local and (snapshot/local).exists():return match.group(0)
  kind='tree' if (ROOT/local).is_dir() else 'blob'
  return '['+label+']('+REPO+'/'+kind+'/main/'+quote(target,safe='/%#')+')'
 linked=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',snapshot_link,current_readme)
 write(snapshot/'README.md',linked)
 if (ROOT/'task.md').exists():
  shutil.copy2(ROOT/'task.md',snapshot/'TASK_ORIGINAL.txt')
  write(snapshot/'task.md',re.sub(r'\[([^\]]+)\]\(([^)]+)\)',snapshot_link,(ROOT/'task.md').read_text()))

 write(snapshot/'SNAPSHOT_README.md','''# Snapshot navigation

The current repository README text is included in README.md. Links to files outside this Markdown snapshot have been made explicit supplementary GitHub URLs, while content/ and the included task.md and rules/ links remain local. REPOSITORY_README_ORIGINAL.txt preserves the exact original Markdown bytes for development evidence. The complete learning foundation is content/README.md; every content-relative link and optional activity file is included in its working structure. The rendered content PDF includes every core explanation, activity and answer offline. The original art is embedded in the separately submitted complete Study Guide PDF; this Markdown content uses native tables/flows and does not require the ignored raw art inputs.
''')
 packages=[package(MD,'BlueImpulse_Stage2_Markdown_V2.zip',[(snapshot,'source-snapshot'),(MD/'BlueImpulse_Stage2_Markdown_V2_Content.pdf','BlueImpulse_Stage2_Markdown_V2_Content.pdf'),(MD/'BlueImpulse_Stage2_Markdown_Submission_Report.pdf','BlueImpulse_Stage2_Markdown_Submission_Report.pdf')]),package(SG,'BlueImpulse_Stage2_StudyGuide_TestBank_V1.zip',[(SG/'BlueImpulse_Stage2_StudyGuide_V1.pdf','BlueImpulse_Stage2_StudyGuide_V1.pdf'),(SG/'BlueImpulse_Stage2_TestBank_V1.docx','BlueImpulse_Stage2_TestBank_V1.docx'),(SG/'BlueImpulse_Stage2_TestBank_V1.pdf','BlueImpulse_Stage2_TestBank_V1.pdf'),(SG/'supporting','supporting'),(SG/'README.md','README.md'),(SG/'REVIEW.md','REVIEW.md')])]
 result={'date':DATE,'topics':len(PAGES),'checkpoint_answers':len(CHECKS),'exercises_and_answers':len(ANSWERS),'missions':len(MISSIONS),'test_bank':{'true_false':len(TF),'multiple_choice':len(MC),'open_ended':len(OE),'distribution':{str(ch):{'tf':sum(q[0]==ch for q in TF),'mc':sum(q[0]==ch for q in MC),'oe':sum(q[0]==ch for q in OE)} for ch in range(1,7)}},'guide':manifest,'packages':packages,'independent_human_peer_review':'pending — no evidence supplied'}
 write(REVIEW/'build-verification.json',json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
