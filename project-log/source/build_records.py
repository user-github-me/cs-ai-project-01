#!/usr/bin/env python3
"""Build authentic process records and Stage 2 submission drafts.

The personal logs retain existing student text. This program cannot
invent personal learning, attendance, feedback, scores, or human approval.
"""
from pathlib import Path
import hashlib
import html
import json
import re
import shutil
import subprocess
import zipfile
import xml.etree.ElementTree as ET

import fitz
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                               TableStyle, PageBreak, KeepTogether)

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / 'project-log'
PRIVATE = ROOT / 'private-submissions/stage2'
SOURCE = PUBLIC / 'source'
HISTORICAL_HEAD = '5ebb2bb'
PERIOD = '25 October–7 November 2026'
DATE = '7 November 2026'
def load_private_roster():
    """Load roster IDs from the assignment source instead of hard-coding them."""
    path = PRIVATE / 'source/roster.json'
    if path.exists():
        return json.loads(path.read_text())
    readme = subprocess.check_output(['git', 'show', f'{HISTORICAL_HEAD}:README.md'], cwd=ROOT, text=True)
    result = []
    for name, suffix in [('Nazif','NAZIF'),('Tian','TIAN'),('Edzel','EDZEL'),('Safa','SAFA'),('Danial','Danial')]:
        match = re.search(r'^\| '+name+r' \| ([^|]+) \| (\d+) \|', readme, re.M)
        if not match:
            raise RuntimeError('Missing private roster record for '+name)
        result.append([name,match.group(1).strip(),match.group(2),suffix])
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result


MEMBERS = load_private_roster()


def p(text): return {'type': 'p', 'text': text}
def h(text, level=1): return {'type': 'h', 'text': text, 'level': level}
def quote(text): return {'type': 'quote', 'text': text}
def bullet(text): return {'type': 'bullet', 'text': text}
def table(headers, rows, widths=None):
    return {'type': 'table', 'headers': headers, 'rows': rows, 'widths': widths}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def preserve_private_sources():
    dest = PRIVATE / 'source/original-personal-logs'
    dest.mkdir(parents=True, exist_ok=True)
    for _, _, _, suffix in MEMBERS:
        original = ROOT / f'Personal_logs/Personal_logs_{suffix}.md'
        target = dest / original.name
        if original.exists():
            shutil.copy2(original, target)
    return dest


def project_blocks():
    blocks = [
        {'type': 'title', 'text': 'Blue Impulse\nStage 2 Project Log'},
        p(f'Hardware, Networks & Behaviorist AI | {PERIOD}'),
        p('Evidence compilation prepared on 7 November 2026. Historical baseline: '
          'commit 5ebb2bb. This is a retrospective reconstruction from dated Git '
          'changes, existing records, recorded user requests, and saved checks. '
          'It does not replace missing contemporaneous meeting records.'),
        p('Status: documented work is supported below; team review, relative '
          'contribution scores, missing meeting details, and individual learning '
          'evidence are not completed by this AI-assisted compilation.'),
        h('Team and evidence boundaries'),
        p('Team: Blue Impulse. Module: Hardware, Networks & Behaviorist AI. '
          'Course: Foundations of CS & AI. Reporting period excludes work before '
          '25 October. Names are taken from the repository; class-roster spelling '
          'has not been independently checked. Safa’s Chinese name differs between '
          'the README and an existing personal log and needs roster confirmation.'),
    ]
    blocks.append(table(['Member', 'Recorded roster name', 'Student ID'],
                        [[a, b, c] for a, b, c, _ in MEMBERS]))
    blocks += [
        p('A Git author identifies who committed a change; it does not prove sole '
          'authorship, hours spent, personal understanding, or team approval. '
          'Existing author-to-member associations are based on repository records. '
          'Original student reflections are kept separately in the personal-log documents.'),
        h('29 October — early Stage 2 organization'),
        p('Recorded actor: Pichanyagan (Tian in the team records). Repository '
          'changes added visual-concept artwork, updated the task list, and created '
          'an AI-use note. The artifact record establishes those changes, not a meeting or review.'),
        table(['Commit / date', 'Actual change', 'What it supports'], [
            ['19c7a71 · 29 Oct', 'Added blueim1.png and blueim2.png under visual-concept.', 'Visual reference files were shared.'],
            ['d481f0c · 29 Oct', 'Updated task list to mark items complete.', 'A task-list change exists; each completion still needs substantive evidence.'],
            ['ed5576c · 29 Oct', 'Added significance-use-of-AI.md.', 'AI use was acknowledged, but the Stage 2 section was empty.'],
        ], [.22, .43, .35]),
        quote('Actual AI-note excerpt: “Use to create the README.md in the beginning '
              'and such folders like content, draft, and assets”; “Slide is AI based '
              'for ideas and templates, and later a lot of human intervention”. '
              'The same file’s Stage 2 section contains only a dash.'),
        p('Unresolved: the note lacks Stage 2 prompts, outputs, verification, and '
          'member-specific judgment. The fuller records below address Nazif’s '
          'available session evidence; they do not invent other members’ interactions.'),
        h('1 November — repository organization and visual assets'),
        p('Nazif requested recovery of the earlier Neogpt history, a “Learning and '
          'Development” folder, Stage 1 draft organization, and placement of the '
          'generated slides. Neogpt assisted with the file operations and the log. '
          'Tian separately maintained presentation folders and uploaded presentation assets.'),
        quote('Recorded request excerpt: “there’s a neogpt history for this repo, '
              'get that history … create a folder names ‘Learning and Development’ '
              'then log it in my nazif personal log.” The accompanying image instructed '
              'moving the draft Markdown files into a Stage 1 subfolder.'),
        table(['Evidence', 'Result'], [
            ['4cbc5cb · 1 Nov · Nazif', 'Created Learning and Development/, moved 12 draft Markdown files into drafts/stage 1/, added a Stage 1 PowerPoint draft, and updated links.'],
            ['e0902bb and 91c2da6 · 1 Nov · Tian', 'Presentation asset upload and final-presentation directory naming are recorded.'],
            ['35ec5c4 · 1 Nov · Safa', 'Updated Content_Outline.md.'],
        ], [.33, .67]),
        p('Outcome and limits: the repository changes are verifiable. A draft '
          'PowerPoint with placeholders is not evidence of a finished teaching deck. '
          'No new individual learning reflection is inferred from the organization work.'),
        h('2 November — chapter scope outline'),
        p('Recorded actor: SafaNadeem0508 (Safa). Commit ec245e7 created the '
          'chapter-finalization outline. It established six chapter headings and '
          'subtopics that later materials used as their structure.'),
        quote('Outline evidence: “Chapter 1: Intro--The Fundamentals”; “Chapter 2: '
              'Behaviorism and Behaviorist AI”; “Chapter 3: Hardware”; “Chapter 4: '
              'Networking”; “Chapter 5: Applications”; “Chapter 6: Strengths and Limitations”.'),
        p('An outline alone did not establish that every topic had complete '
          'explanations, activities, or checked answers. Later production and audit '
          'entries distinguish the content artifacts from that initial scope.'),
        h('3 November — slide outline and AI-assisted presentation draft'),
        p('Tian committed the Stage 2 slide outline (cfd8a53). Nazif supplied Mars '
          'visual references and asked Neogpt to make the new presentation from that '
          'outline. Commit ab18e00 added the editable 37-slide draft and design source. '
          'Safa added and revised chapter learning-outcome files.'),
        quote('Recorded request excerpt: “need to make new slide, this the info, '
              'prompt … assets/presentations/slides-draft/stage2-slide-outline.md” '
              'with color references and a PowerPoint Morph style reference.'),
        p('AI use — purpose and result: create an editable visual presentation '
          'matching the supplied outline. The existing record says the draft used '
          'Mars/NASA imagery, large text, and Morph transitions while leaving '
          'detailed explanations, debate, video, and game content for the team. '
          'This limitation is preserved rather than relabelled as completed content.'),
        table(['Selected evidence', 'Meaning'], [
            ['cfd8a53 · 3 Nov', '54 lines added to stage2-slide-outline.md by Tian’s recorded account.'],
            ['ab18e00 · 3 Nov', 'Editable Stage 2 Sojourner draft and design materials added by Nazif’s recorded account with Neogpt assistance.'],
            ['0af8fa2 / 10f6abb · 3 Nov', 'Chapter 3 / Chapter 2 learning-outcome files added by Safa’s recorded account.'],
        ], [.32, .68]),
        h('3 November — meeting record: whether Sojourner had AI', 2),
        quote('Actual user report: “also log in the personal log that, today we had '
              'meeting, and we discussed about is that sojourner had AI or not”.'),
        p('Date: 3 November, supported by the existing dated entry and commit '
          'b94beda. Purpose/discussion: whether Sojourner had AI. Time, location or '
          'platform, attendee list, absences, alternatives, final decision, action '
          'owners, and deadlines were not supplied. No outcome or attendance is invented.'),
        p('Follow-up evidence: rover research files were committed on 3–4 '
          'November, but the available record does not establish that this meeting '
          'assigned those tasks. Scientific clarification belongs in the checked '
          'learning content; it must not be presented as an unrecorded meeting decision.'),
        h('4 November — chapter folders and rover research'),
        p('Nazif asked for Chapters 4–6 to be added and logged. Neogpt created the '
          'folders using the existing README/draft/exercises/solutions layout '
          '(d5f7fc4; logged in e1b87c2). Safa continued learning-outcome files. '
          'Edzel and Danial’s recorded accounts uploaded rover research.'),
        quote('Recorded requests: “add chapter 4,5,6 folder in github repo”; '
              '“add this to my personal log too”.'),
        table(['Evidence', 'Recorded result / limit'], [
            ['d5f7fc4 · Nazif', 'Chapter 4–6 file structure added. A folder is not evidence of developed core content.'],
            ['a19c547 and 5a38faf · Edzel', 'ResearchRoverInfoEdzel.md added and formatted.'],
            ['d4050c1 · Bleedy0', 'ResearchRoverInfoDanial.docx uploaded (36,228 bytes); filename associates it with Danial.'],
            ['e0863af / febb796 / fdb8485 · Safa', 'Learning-outcome files for Chapters 6, 4, and 5 added.'],
        ], [.37, .63]),
        quote('Research excerpt from Edzel’s committed file: “Its navigation was '
              'not based on modern deep learning. Instead, it used sensor feedback '
              'and predefined reactive behaviours to avoid hazards while moving '
              'toward destinations selected by human operators.” This is a source '
              'excerpt, not proof that each student independently verified it.'),
        h('5 November — outcomes and key terminology'),
        p('Safa’s recorded account revised learning outcomes and added the six '
          'chapter key-term files. The repository shows dcfbc71 (Chapter 1), '
          'aeb6ced (2), 84cd2ba (3), 7ce917c (4), e87b4f5/50015be (5), and '
          '08b2955 (6). These changes establish vocabulary work across the module.'),
        p('Unresolved: the available records do not show a dated learner trial, '
          'peer approval, or each member’s explanation of the terms. Such learning '
          'evidence must come from the students and cannot be inferred from uploads.'),
        h('6 November — source chapters, exercises, and AI-use disclosures'),
        p('Safa updated exercises and UseOfAI.md in the chapter folders and '
          'uploaded six chapter PDFs. Edzel added activities.md with application '
          'tasks. The source upload was explicitly described as work in progress.'),
        quote('Commit 9a645d0 body: “The bone structures of the chapters i finished. '
              'Which are still a work in progress in terms of content but just to '
              'document work, I uploaded them here”.'),
        quote('Chapter 2 UseOfAI.md excerpt: “we largely used AI, specifically '
              'Gemini, from generating the learning outcomes, to the key terms, to '
              'creating the end of chapter exercises. It passed through multiple rounds”.'),
        p('AI evidence limit: the chapter disclosure names the tool and purpose '
          'but does not include the important prompts/outputs, round-by-round '
          'decisions, or verification results. That missing evidence remains a '
          'specific responsibility of the members involved; this log does not fabricate it.'),
        table(['Evidence', 'Actual material'], [
            ['9a645d0 · Safa', 'Six Bone Structures chapter PDFs uploaded.'],
            ['56c3ca9 / 6eae359 / 3edca73 and related 6 Nov commits · Safa', 'Chapter exercises revised; chapter-specific AI-use notes created.'],
            ['52bf6d2 · Edzel', '352-line activities.md added, including binary conversion, storage, computer components, logic gates, and AI applications.'],
        ], [.43, .57]),
        h('6 November — AI-assisted study guide and tutorial production'),
        p('Member directing the work: Nazif. Tool: Neogpt/Codex with local PDF, '
          'HyperFrames, FFmpeg, Python, and synthetic speech tooling. The user '
          'specified the order: ignore temporary source contents, finish the study '
          'guide from six chapters and supplied artwork, then produce five tutorial '
          'videos with documents and support files. The AI performed the drafting, '
          'rendering, and automated checks; this record does not attribute those '
          'operations to independent student execution.'),
        quote('Recorded prompt excerpt: “first of all, add the ‘temp contents’ '
              'folder in gitignore. then check the files, there are 6 chapters '
              'contents, and a md file about making the study guide. there is also '
              'a template for the study guide. follow all those then make a study '
              'guide pdf. and only then as task no. 2 …”'),
        quote('Video requirements excerpt: “This is not a seperate explanation '
              'but it’s a video of US tecahing the viewer using the book”; '
              '“CITE THE PAGES OR QUOTE FROM THE STUDY GUIDE”; '
              '“subtitles are mandatory”; “duration of the video 5-10min only”.'),
        quote('Important follow-up: when the original study guide art PDF was '
              'missing, the user replied “i have added that. check now”. The '
              'subsequent guide build used the supplied original artwork.'),
        p('Decisions and outcome: temporary material stayed ignored. The guide '
          'was completed before video production. Original cover/divider artwork '
          'was preserved. Commit b40933c added the 96-page guide; 238cf9e added '
          'five narrated tutorials, PDFs, timed scripts, subtitles, runnable '
          'demonstrations, and editable source. The old videos used guide screenshots '
          'and page citations, as requested then; the 7 November append below '
          'explicitly supersedes that visual requirement.'),
        table(['Saved guide verification', 'Result'], [
            ['source/verification.json', 'status: passed; 96 pages; 1,287 verified text items; 65 source exercises; 6 contents links.'],
            ['Artwork pages', 'Cover and six divider pages compared unchanged: guide pages 1, 5, 22, 34, 51, 71, 84.'],
            ['Guide SHA-256', '2af7695b50de6d32cdc3254b1a702b1ec09701c90677bc758d956f9476b7d3e4'],
        ], [.30, .70]),
        p('The following are saved verification results for the 6 November '
          'exports. They are not transferred automatically to replacement videos.'),
    ]
    media = []
    historical_media = json.loads((SOURCE / 'historical-video-verification.json').read_text())
    for d in historical_media['videos']:
        i = d['video']
        secs = round(d['duration_seconds'])
        media.append([f'{i:02}', f'{secs//60}:{secs%60:02}',
                      f"{d['bytes']/1000000:.2f} MB", str(d['frame_count']),
                      f"{d['sampled_ssim_against_render']:.6f}"])
    blocks += [
        table(['Video', 'Duration', 'Size', 'Decoded frames', 'Sampled SSIM'], media, [.12,.16,.22,.25,.25]),
        p('Saved final-review evidence: 1920 × 1080, 30 fps, H.264/AAC; all '
          '82,951 frames decoded without errors; audio unchanged by compression; '
          'all 456 spoken subtitle midpoint samples showed text and 12 silent '
          'samples had a clear caption band. Eighteen quotations were matched '
          'against the guide. Each tutorial PDF contained 13 pages, 65 combined. '
          'SSIM was sampled once per second, not on every frame. Runtime/layout '
          'checks had no errors; the optional automated motion pass was disabled.'),
        p('Meaningful technical correction recorded during production: captions '
          'could linger during seeking into silence. The caption child span was '
          'given explicit opacity changes at measured cue boundaries; the final '
          'caption and silence samples then passed. Compression reduced file '
          'size while preserving decoded audio. These are AI-assisted production '
          'findings, not claims about a student’s personal learning.'),
        h('6 November — repository/release delivery'),
        p('Nazif requested “push everything in github and log in my tasks in '
          'personal logs”. Commit 14c6ed1 records the final-presentation upload '
          'and deliverable documentation. The prior release is supplementary '
          'access, not evidence of a course-channel submission.'),
        quote('Saved package verification: BlueImpulse_Tutorial_Package.zip; '
              '369,127,764 bytes; 305 files; 0 CRC errors; 0 SHA-256 mismatches; '
              '5 videos; 6 tutorial PDFs. SHA-256: '
              '83cdedf69adf51ae9f3db3c8a9ca686927a852270b5f8a06d94fb6ca192fefdd.'),
        p('Shared-rule correction now required: earlier personal logs were '
          'published with project files. The 7 November audit identified the '
          'assignment’s privacy requirement. The user-directed access choice and the '
          'confirmed repository action are documented below when completed.'),
        h('7 November — chapter revision and printable tutorial documents'),
        p('Edzel revised the Chapter 3 outline in bc91f1e. Nazif requested PDFs '
          'of the tutorials and script/teaching-outline documents. Neogpt '
          'generated five printable script/outline PDFs, kept editable Markdown, '
          'and packaged the documents; commit 5ebb2bb records that work.'),
        quote('Actual content change in bc91f1e: removed “Computer Memory and '
              'Storage”, “Processing Devices and CPU Architecture”, “Parallel '
              'Processing and Computer Systems”, and “Logic Circuits and Boolean '
              'Algebra” from the Chapter 3 scope outline. “Input, Processing and '
              'Output Hardware” and “How Hardware enables AI” remain. This is '
              'scope-edit evidence, not proof that downstream resources were synchronized.'),
        quote('Recorded request: “make - pdf of tutorial - script/teaching '
              'outline for the tutorial videos.”'),
        p('Outcome: five Script_and_Teaching_Outline.pdf files and the source '
          'builders were committed. Their old screenshots/page references require '
          'revision under the later video append; keeping old files does not '
          'satisfy the new requirement by itself.'),
        h('7 November — Stage 2 rules audit and revised video direction'),
        p('Member directing work: Nazif. Tool: Neogpt/Codex. Purpose: apply the '
          'supplied Stage2_All_Instructions.md across the repository, revise video '
          'teaching and motion, prepare required formats, and record the work. '
          'This is active AI-assisted production; outcomes appear only when verified.'),
        quote('Current request excerpt: “rules/Stage2_All_Instructions.md follow '
              'this. and make whole repo follow this. make it it ready. log '
              'everything in my personal log.”'),
        quote('Current video append: “dont make it put screenshots or pg number '
              'of the study guide anymore, just cite the number and name of the '
              'chapter and the subtopic the video will explain”; “The key is '
              '‘story telling’”; “Keep the same color palette but the color must '
              'bemore vibrant”.'),
        quote('Motion/build excerpt: one typeface; at most three colors; '
              '115 BPM; “Everyshot is made out of previous one”; “no CSS '
              'animations, no timers, no state carried between frames”; '
              '60 fps with three subframes; inspect one frame per beat; '
              'sound effects must not overpower narration. The explicit banned '
              'list includes bouncy easing despite the earlier general request '
              'for bouncy energy.'),
        p('Production decisions recorded at the planning stage: keep the '
          'five teaching topics; use a fictional campus delivery rover, Pip '
          '(protocol identifier robot-7), to connect hook, example, demonstration, '
          'and recap. Cite chapter numbers, names, and subtopics instead of book '
          'screenshots/page numbers. Use the specific no-bouncy-easing constraint '
          'when interpreting the broad lively-motion request. Motion must remain '
          'readable during a sustained explanation; generated sound sits below voice.'),
        p('Rules audit result: separate editable Word test bank required; '
          'Markdown submission needs full rendered content and a report; video '
          'guide needs metadata, prerequisites, timestamps, resource connections, '
          'and scripts/outlines; individual MP4 files must be at most 250 MB; '
          'the assignment specifies private personal logs; project and combined personal logs each '
          'require a single Word/PDF document with adjacent evidence.'),
        h('7 November — checks actually repeated during record preparation', 2),
        p('The AI assistant read the complete shared rules and exact log '
          'submission requirements, inspected all five existing personal files '
          'and dated Git changes, and executed the existing demonstration script '
          'with --topic all. The observed outputs below are directly included so '
          'the evidence is readable without following a link.'),
        table(['Demonstration', 'Observed default result', 'Interpretation / limit'], [
            ['Q-learning', 'Target 4.6; new Q 3.3; terminal practice 1.5.', 'Future value is omitted for the terminal state.'],
            ['Pipeline', 'Completion cycles 4, 5, 6; 6 cycles total versus 12 sequential.', 'Four one-cycle stages, independent instructions, no stalls; one instruction still takes four stages.'],
            ['Delay distance', 'At 30 m/s: 500/50/5/200 ms → 15/1.5/0.15/6 m.', 'Distance travelled during delay only; not full stopping distance.'],
            ['Networked AI', 'ACCEPT, STALE, DUPLICATE / OLD SEQUENCE.', '200 ms policy limit; authenticated is a prior check result, not an authentication method.'],
            ['Program execution', 'ACC 3 → 7; memory[200] = 7; final PC = 104.', 'Invented teaching ISA, not a real processor implementation.'],
        ], [.19,.39,.42]),
        p('AI-use disclosure for these logs: Codex selected evidence, drafted '
          'the process prose, preserved available personal writing, and generated '
          'Word/PDF layouts. This is substantial AI assistance with the logs '
          'themselves. Nazif supplied the request and constraints. No personal '
          'learning, independent student checks, review approval, meeting details, '
          'or contribution scores were supplied by the model.'),
        p('Human evidence still required: student-written Stage 2 entries from '
          'Tian, Edzel, Safa, and Danial; Nazif’s own understanding and judgment '
          'where not recorded; specific wider-course learning; actual Stage 1 '
          'feedback if received; missing meeting details; team-agreed scores; '
          'each student’s review. These are flagged openly rather than claimed complete.'),
    ]
    updates = SOURCE / 'completion-updates.json'
    if updates.exists():
        blocks += json.loads(updates.read_text())
    blocks += [
        h('Follow-up and submission status'),
        table(['Owner', 'Required follow-up', 'Status / intended deadline'], [
            ['Nazif with AI production support', 'Finish the requested cross-resource revision and record new media/document/package checks.', 'See verified completion entries above; do not inherit old export checks.'],
            ['Each named student', 'Write and check their own Stage 2 personal section, including actual learning beyond the team module.', 'Missing where identified; before submission.'],
            ['All members / submission lead', 'Review evidence, agree contribution scores, confirm roster names, and verify course/teacher access.', 'Human confirmation not established in the inspected records.'],
            ['Submission lead', 'Submit actual assignment files through the course channel in the specified formats.', 'Repository upload is supplementary; course-channel receipt not available.'],
        ], [.25,.48,.27]),
        h('Stage 2 contribution table'),
        p('The following rows report available work evidence, not a ranking. '
          'The rules require the team to agree relative contribution scores, '
          'with the strongest contributor at 100. The AI cannot honestly assign '
          'those judgments from commit counts or generate the team’s agreement. '
          'Scores are therefore explicitly pending. Equal scores are permitted '
          'where the team judges contributions equally strong.'),
    ]
    contributions = [
        ['Nazif', 'Direction of AI-assisted repository organization, Stage 2 draft slides, study guide, five tutorials, documents, and requested compliance revision.', 'Team review required', '1, 3, 4, 6, 7 Nov entries; 4cbc5cb, ab18e00, d5f7fc4, b40933c, 238cf9e, 14c6ed1, 5ebb2bb.'],
        ['Tian', 'Visual-concept uploads, Stage 2 slide outline, presentation-folder organization, task-list and AI-use note updates.', 'Team review required', '29 Oct / 1 / 3 Nov; 19c7a71, d481f0c, ed5576c, e0902bb, cfd8a53.'],
        ['Edzel', 'Rover research, activity collection, chapter scope revisions, and four additional Chapter 3 Hardware topics in the finalization list.', 'Team review required', '4 / 6 / 7 Nov; a19c547, 5a38faf, 52bf6d2, bc91f1e, 8ab3108.'],
        ['Safa', 'Six-chapter scope, learning outcomes, key terms, exercises, AI-use disclosures, source chapter PDF uploads, and a rover-game AI prompt request (no implemented game evidenced).', 'Team review required', '1–7 Nov entries; ec245e7, outcome/key-term commits, 9a645d0, chapter exercise/AI-note changes, 4b51f77.'],
        ['Danial', 'Rover research document uploaded under his name.', 'Team review required', '4 Nov; d4050c1 added ResearchRoverInfoDanial.docx. Further research process/verification is not supplied.'],
    ]
    roster = {a: f'{a} / {b}\n{c}' for a,b,c,_ in MEMBERS}
    contributions = [[roster[row[0]], *row[1:]] for row in contributions]
    blocks.append(table(['Member / ID', 'Main evidenced Stage 2 work', 'Relative score', 'Evidence in this document'], contributions, [.16,.37,.18,.29]))
    return blocks


def clean_md(text):
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', text)
    return text.replace('`', '').replace('**', '')


def source_sections(path):
    text = path.read_text()
    sections = []
    pattern = re.compile(r'^### (.+? — (\d+) (November) (2026))\s*$', re.M)
    matches = list(pattern.finditer(text))
    for i,m in enumerate(matches):
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        body = text[m.end():end].split('\n## ')[0].strip()
        if 1 <= int(m.group(2)) <= 7:
            sections.append((int(m.group(2)), m.group(1), body))
    return sorted(sections, key=lambda x:x[0])


def personal_blocks(originals, only_nazif=False):
    selected = MEMBERS[:1] if only_nazif else MEMBERS
    blocks = [
        {'type': 'title', 'text': 'Blue Impulse\nStage 2 Personal Logs'},
        p(f'ASSIGNMENT DRAFT · PUBLIC AT THE USER’S REQUEST | {PERIOD}'),
        p('Submission filename: BlueImpulse_Stage2_PersonalLogs. Submit the '
          'completed single Word or PDF through the designated assignment channel '
          'without a ZIP. The user explicitly requested public repository access '
          'for the professor, including personal logs; this differs from the '
          'supplied assignment’s privacy instruction.'),
        p('This AI-assisted compilation preserves the available dated personal '
          'writing. It is not a claim that students have checked the compilation '
          'or demonstrated the missing learning. Each student must write and '
          'review their own section. Missing reflections remain explicitly missing.'),
        h('Contents'),
    ]
    for a,b,c,_ in selected:
        blocks.append(p(f'{a} / {b} · {c} — ' + ('existing dated entries plus labelled AI drafting' if a=='Nazif' else 'Stage 2 writing not supplied')))
    blocks.append(p('Navigation: each member starts on a new page. Word headings '
                    'and PDF headings identify the sections. Names/IDs come from '
                    'the repository; verify against the class roster, especially '
                    'the differing recorded Chinese spelling of Safa’s name.'))
    evidence = {
        'Repository organisation': ('4cbc5cb', 'Created Learning and Development/, reorganized 12 draft Markdown files, and added the Stage 1 draft presentation. Neogpt performed the requested file organization; no personal learning test is recorded.'),
        'Presentation design': ('ab18e00', '37-slide editable draft added from the supplied outline and references. The existing entry openly notes the content left blank; an editable design is not a complete teaching presentation.'),
        'Team meeting': ('b94beda', 'The only supplied meeting claim is that the team discussed whether Sojourner had AI. Attendees, time/location, final decision, and actions were not supplied.'),
        'Chapter folder setup': ('d5f7fc4 / e1b87c2', 'Added Chapters 4–6 with the existing four-file structure. This establishes organization, not completion of chapter explanations.'),
        'Study guide and tutorial': ('b40933c / 238cf9e', 'Saved AI-assisted checks report 96 guide pages, 65 source exercises, five 8:36–9:38 videos, 456 caption samples and 12 silence samples. These are automated production checks, not proof of Nazif’s independent subject understanding.'),
        'GitHub upload': ('14c6ed1', 'Final-presentation upload and delivery links recorded. Saved ZIP verification: 305 files, five MP4s, zero CRC/hash mismatches. This does not establish submission through the course channel.'),
        'Tutorial PDFs': ('5ebb2bb', 'Five printable script/outline PDFs, their source builders, and document-package links were added. The newer chapter/subtopic citation request supersedes old page-reference layouts.'),
    }
    for a,b,c,suffix in selected:
        blocks += [{'type':'pagebreak'}, h(f'{a} / {b}'), p(f'Student ID: {c} | Blue Impulse | {PERIOD}')]
        if a != 'Nazif':
            original = originals / f'Personal_logs_{suffix}.md'
            blocks += [
                h('Stage 2 entries — student writing required',2),
                p(f'The available {a} source contains Stage 1 material only' +
                  (' (Edzel’s stated reporting period is 21–24 October).' if a=='Edzel' else '.') +
                  ' It is not repeated or relabelled as Stage 2. The existence of '
                  'Git changes is team-process evidence; it cannot substitute '
                  'for this student’s own description, judgment, and reflection.'),
                p('Missing student-owned content: dated Stage 2 activities; '
                  'own contribution distinct from teammates/AI; adjacent outcome '
                  'evidence; subject understanding and how it was checked; '
                  'specific wider-course learning; significant AI interactions '
                  'and judgments; difficulties/feedback; next steps; own review.'),
                p('No entry, meeting attendance, contribution score, time spent, '
                  'learning outcome, or approval is invented in this section.'),
            ]
            continue
        blocks += [
            p('The entries below preserve the existing wording, including first '
              'person statements previously drafted with Neogpt. Added evidence '
              'notes identify which work/checks were AI-assisted. The 1 November '
              'entry was filed under a Stage 1 heading but falls within the '
              'required reporting period, so it is included by its date.'),
        ]
        for day,title,body in source_sections(originals / 'Personal_logs_NAZIF.md'):
            blocks.append(h(title,2))
            for line in body.splitlines():
                if not line.strip(): continue
                if line.startswith('- '): blocks.append(bullet(clean_md(line[2:])))
                else: blocks.append(p(clean_md(line)))
            for prefix,(commit,detail) in evidence.items():
                if title.startswith(prefix):
                    blocks.append(quote(f'Adjacent evidence note — {commit}: {detail}'))
                    break
        blocks += [
            h('7 November — Stage 2 audit and revised tutorials (AI-assisted draft)',2),
            p('Recorded personal action: I asked Neogpt to follow '
              'rules/Stage2_All_Instructions.md across the repository and to '
              'record the work. I supplied a new video direction: replace '
              'study-guide screenshots/page numbers with chapter and subtopic '
              'citations, use a story hook, make the existing palette more '
              'vibrant, and use readable dynamic motion with sound effects '
              'below the narration.'),
            quote('My recorded request: “rules/Stage2_All_Instructions.md follow '
                  'this. and make whole repo follow this. make it it ready. '
                  'log everything in my personal log.” Video follow-up: '
                  '“The key is ‘story telling’”.'),
            p('AI contribution: Codex inspected the rules and repository, '
              'planned the coordinated revision, checked existing evidence, '
              'and drafted the process records and this dated entry. Planned '
              'story: Pip, a fictional campus delivery rover, with robot-7 as '
              'its protocol identifier. The AI’s production/checking work is '
              'not presented as work I carried out independently.'),
            quote('Selected AI check output actually obtained during this '
                  'audit: Q target 4.6/new value 3.3; pipeline completions '
                  '4, 5, 6; at 30 m/s a 500 ms delay corresponds to 15 m '
                  '(delay distance only); packet checks ACCEPT, STALE, '
                  'DUPLICATE / OLD SEQUENCE; the toy program stores 7. '
                  'The assistant ran the existing Python examples; this is '
                  'not evidence that I solved or explained them unaided.'),
            p('Repository decision: after the rules audit, I explicitly '
              'clarified that the repository, personal logs, and submission '
              'materials should remain public for the professor. Neogpt '
              'restored and verified PUBLIC visibility and removed the broad '
              'personal-log/submission exclusions. This user-directed access '
              'choice differs from the assignment’s privacy instruction. '
              'The historical private-submissions folder name is not an '
              'access restriction.'),
            p('Own learning and judgment still to record: explain in my own '
              'words what I checked in the revised learning materials, show '
              'one independent worked check or prediction, and describe an '
              'actual wider-course learning activity. These were not '
              'provided in the recorded request, so no answer is invented.'),
            p('Next steps: review the generated learning materials and this '
              'log; correct anything that does not reflect my actual work; '
              'supply my own reflection and selected verification evidence; '
              'coordinate the combined submission with all members.'),
            p('AI-use disclosure: this new entry and the compilation were '
              'substantially drafted by Neogpt/Codex from actual requests '
              'and repository evidence. They have not been represented as '
              'student-approved or independently student-written.'),
        ]
        updates = PRIVATE / 'source/nazif-completion-updates.json'
        if updates.exists(): blocks += json.loads(updates.read_text())
    return blocks


def markdown(blocks):
    out=[]
    for b in blocks:
        typ=b['type']
        if typ=='title': out.append('# '+b['text'].replace('\n',' — '))
        elif typ=='h': out.append('#'*(b.get('level',1)+1)+' '+b['text'])
        elif typ=='p': out.append(b['text'])
        elif typ=='quote': out.append('> '+b['text'])
        elif typ=='bullet': out.append('- '+b['text'])
        elif typ=='pagebreak': out.append('<!-- new member page -->')
        elif typ=='table':
            rows=[b['headers'], *b['rows']]
            lines=['| '+' | '.join(str(x).replace('\n',' / ').replace('|','/') for x in rows[0])+' |',
                   '| '+' | '.join('---' for _ in rows[0])+' |']
            lines += ['| '+' | '.join(str(x).replace('\n',' / ').replace('|','/') for x in row)+' |' for row in rows[1:]]
            out.append('\n'.join(lines))
    return '\n\n'.join(out)+'\n'


def add_page_field(paragraph):
    run=paragraph.add_run()
    f=OxmlElement('w:fldSimple'); f.set(qn('w:instr'),'PAGE')
    run._r.addnext(f)


def build_docx(blocks,path,private):
    doc=Document()
    sec=doc.sections[0]
    sec.page_width=Inches(8.27);sec.page_height=Inches(11.69)
    sec.top_margin=Inches(.72);sec.bottom_margin=Inches(.72)
    sec.left_margin=Inches(.70);sec.right_margin=Inches(.70)
    for name in ['Normal','Body Text','List Bullet']:
        st=doc.styles[name];st.font.name='Arial';st.font.size=Pt(10.5)
        st.element.rPr.rFonts.set(qn('w:eastAsia'),'Arial Unicode MS')
        st.paragraph_format.space_after=Pt(6)
    for name,size in [('Title',25),('Heading 1',16),('Heading 2',12)]:
        st=doc.styles[name];st.font.name='Arial';st.font.size=Pt(size)
        st.font.color.rgb=RGBColor.from_string('172343')
        st.paragraph_format.keep_with_next=True
    header=sec.header.paragraphs[0]
    header.text='BLUE IMPULSE · STAGE 2 · '+('ASSIGNMENT COPY' if private else 'PROCESS RECORD')
    header.style=doc.styles['Caption']
    footer=sec.footer.paragraphs[0]
    footer.text=PERIOD+'  |  ';add_page_field(footer)
    footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    for b in blocks:
        typ=b['type']
        if typ=='title': doc.add_paragraph(b['text'],'Title')
        elif typ=='h': doc.add_heading(b['text'],level=b.get('level',1))
        elif typ in ('p','quote','bullet'):
            para=doc.add_paragraph(b['text'],'List Bullet' if typ=='bullet' else 'Normal')
            if typ=='quote':
                para.paragraph_format.left_indent=Inches(.15)
                para.paragraph_format.right_indent=Inches(.1)
                for run in para.runs:
                    run.font.size=Pt(9.5);run.font.color.rgb=RGBColor.from_string('354466')
        elif typ=='pagebreak': doc.add_page_break()
        elif typ=='table':
            t=doc.add_table(rows=1,cols=len(b['headers']));t.style='Light Shading Accent 1'
            for i,v in enumerate(b['headers']): t.rows[0].cells[i].text=str(v)
            trPr=t.rows[0]._tr.get_or_add_trPr();repeat=OxmlElement('w:tblHeader');trPr.append(repeat)
            for row in b['rows']:
                cells=t.add_row().cells
                for i,v in enumerate(row): cells[i].text=str(v)
            for row in t.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        para.paragraph_format.space_after=Pt(4)
                        for run in para.runs: run.font.size=Pt(8.5)
            doc.add_paragraph()
    doc.core_properties.title=path.stem.replace('_',' ')
    doc.core_properties.author='Blue Impulse — AI-assisted evidence compilation'
    doc.core_properties.comments='Student learning, approval, and missing evidence are not fabricated.'
    doc.save(path)


def build_pdf(blocks,path,private):
    font=Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
    pdfmetrics.registerFont(TTFont('RecordsUnicode',str(font)))
    pdfmetrics.registerFont(TTFont('RecordsBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle('RBody',fontName='RecordsUnicode',fontSize=10,leading=14,spaceAfter=7,textColor=colors.HexColor('#182340'),splitLongWords=True))
    styles.add(ParagraphStyle('RQuote',parent=styles['RBody'],fontSize=9,leading=12,leftIndent=10,rightIndent=6,spaceBefore=3,spaceAfter=9,textColor=colors.HexColor('#354466'),backColor=colors.HexColor('#f0f3f9'),borderPadding=7))
    styles.add(ParagraphStyle('RTitle',parent=styles['RBody'],fontSize=25,leading=30,spaceAfter=15))
    styles.add(ParagraphStyle('RH1',parent=styles['RBody'],fontSize=15,leading=19,spaceBefore=12,spaceAfter=8,keepWithNext=True))
    styles.add(ParagraphStyle('RH2',parent=styles['RH1'],fontSize=12,leading=16,spaceBefore=9))
    styles.add(ParagraphStyle('RCell',parent=styles['RBody'],fontSize=8.5,leading=11,spaceAfter=0))
    styles.add(ParagraphStyle('RHead',parent=styles['RCell'],textColor=colors.white))
    page=(210*mm,297*mm);width=174*mm
    story=[]
    esc=lambda t:html.escape(str(t)).replace('\n','<br/>')
    for b in blocks:
        typ=b['type']
        if typ=='pagebreak':story.append(PageBreak())
        elif typ=='table':
            data=[[Paragraph(esc(v),styles['RHead']) for v in b['headers']]]
            data += [[Paragraph(esc(v),styles['RCell']) for v in row] for row in b['rows']]
            weights=b.get('widths') or [1/len(b['headers'])]*len(b['headers'])
            t=Table(data,colWidths=[width*w for w in weights],repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#172343')),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f3f9')]),
                ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),
                ('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),
                ('BOTTOMPADDING',(0,0),(-1,-1),7),
                ('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#f12a8e')),
            ]));story += [t,Spacer(1,9)]
        else:
            sty={'title':'RTitle','p':'RBody','quote':'RQuote','bullet':'RBody'}.get(typ)
            if typ=='h':sty='RH1' if b.get('level',1)==1 else 'RH2'
            text=esc(b['text'])
            if typ=='bullet':text='• '+text
            story.append(Paragraph(text,styles[sty]))
    def decorate(c,doc):
        c.saveState();c.setFont('RecordsUnicode',8)
        c.setFillColor(colors.HexColor('#59667f'))
        c.drawString(18*mm,284*mm,'BLUE IMPULSE · STAGE 2 · '+('ASSIGNMENT COPY' if private else 'PROCESS RECORD'))
        c.drawString(18*mm,13*mm,PERIOD)
        c.drawRightString(192*mm,13*mm,str(doc.page))
        c.restoreState()
    doc=SimpleDocTemplate(str(path),pagesize=page,rightMargin=18*mm,leftMargin=18*mm,topMargin=21*mm,bottomMargin=22*mm,title=path.stem.replace('_',' '),author='Blue Impulse — AI-assisted evidence compilation')
    doc.build(story,onFirstPage=decorate,onLaterPages=decorate)


def save_document(blocks,dest,stem,private=False):
    dest.mkdir(parents=True,exist_ok=True)
    (dest/(stem+'.md')).write_text(markdown(blocks))
    (dest/(stem+'.json')).write_text(json.dumps(blocks,ensure_ascii=False,indent=2)+'\n')
    build_docx(blocks,dest/(stem+'.docx'),private)
    build_pdf(blocks,dest/(stem+'.pdf'),private)
    pdf=fitz.open(dest/(stem+'.pdf'))
    bounds=[]
    for i,page in enumerate(pdf):
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    x0,y0,x1,y1=span['bbox']
                    if x0 < 12 or x1 > page.rect.width-12 or y0 < 5 or y1 > page.rect.height-5:
                        bounds.append({'page':i+1,'text':span['text'],'bbox':span['bbox']})
    text='\n'.join(page.get_text() for page in pdf)
    docx_path=dest/(stem+'.docx')
    pdf_path=dest/(stem+'.pdf')
    with zipfile.ZipFile(docx_path) as z:
        assert z.testzip() is None
        xml=z.read('word/document.xml').decode()
        ET.fromstring(xml)
        assert 'Stage 2' in xml
    Document(docx_path)
    expected=MEMBERS[:1] if 'NAZIF' in stem else MEMBERS
    missing_members=[a for a,_,_,_ in expected if a not in text or a not in xml]
    missing_ids=[a for a,_,c,_ in expected if c not in text or c not in xml]
    invalid_text=[code for code in ['\ufffd','\x00','(cid:'] if code in text]
    empty_pages=[i+1 for i,page in enumerate(pdf) if len(page.get_text().strip())<20]
    result={
        'file':str(pdf_path.relative_to(ROOT)), 'pages':len(pdf),
        'bytes':pdf_path.stat().st_size,
        'sha256':hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
        'docx_file':str(docx_path.relative_to(ROOT)),
        'docx_bytes':docx_path.stat().st_size,
        'docx_sha256':hashlib.sha256(docx_path.read_bytes()).hexdigest(),
        'out_of_page_spans':bounds,'docx_crc_errors':0,
        'docx_xml_parse':'passed','docx_reopen':'passed',
        'extracted_pdf_characters':len(text),
        'all_member_names_present':not missing_members,
        'all_recorded_student_ids_present':not missing_ids,
        'missing_member_names':missing_members,'missing_student_ids_for':missing_ids,
        'invalid_extracted_text_markers':invalid_text,'empty_pages':empty_pages,
    }
    pdf.close()
    if bounds or missing_members or missing_ids or invalid_text or empty_pages:
        raise RuntimeError(result)
    return result


def main():
    SOURCE.mkdir(parents=True,exist_ok=True)
    originals=preserve_private_sources()
    complete=project_blocks()
    (SOURCE/'project-records.json').write_text(json.dumps(complete,ensure_ascii=False,indent=2)+'\n')
    results=[save_document(complete,PUBLIC,'BlueImpulse_Stage2_ProjectLog',True)]
    results.append(save_document(complete,PRIVATE,'BlueImpulse_Stage2_ProjectLog',True))
    results.append(save_document(personal_blocks(originals),PRIVATE,'BlueImpulse_Stage2_PersonalLogs',True))
    results.append(save_document(personal_blocks(originals,True),PRIVATE,'BlueImpulse_Stage2_PersonalLog_NAZIF',True))
    (PRIVATE/'README.md').write_text('''# Stage 2 assignment drafts\n\nThe user explicitly requested a public repository including personal logs and submission materials. The historical folder name `private-submissions` is not an access restriction. This public access choice differs from the supplied assignment privacy instruction and is recorded in the project log.\n\n- `BlueImpulse_Stage2_ProjectLog.docx` / `.pdf`: complete roster-ID assignment copy of the project log.\n- `BlueImpulse_Stage2_PersonalLogs.docx` / `.pdf`: required combined five-member draft; only Nazif has available dated Stage 2 writing.\n- `BlueImpulse_Stage2_PersonalLog_NAZIF.docx` / `.pdf`: Nazif-only review copy; it does not replace the required combined submission.\n- `.md` / `.json`: editable document source; original personal files are preserved under `source/original-personal-logs/`.\n\nEach student must write/check their own learning and work record. Four missing Stage 2 logs, member review, authentic personal reflections, meeting details and team-agreed contribution scores remain human requirements. No experiences, attendance, feedback, learning, or scores have been fabricated. Submit the completed combined personal document through the designated course channel without a ZIP; a repository link remains supplementary under the supplied instructions.\n''')
    stem='BlueImpulse_Stage2_ProjectLog'
    assert (PUBLIC/(stem+'.json')).read_bytes()==(PRIVATE/(stem+'.json')).read_bytes()
    with zipfile.ZipFile(PUBLIC/(stem+'.docx')) as a, zipfile.ZipFile(PRIVATE/(stem+'.docx')) as b:
        assert a.read('word/document.xml')==b.read('word/document.xml')
    with fitz.open(PUBLIC/(stem+'.pdf')) as a,fitz.open(PRIVATE/(stem+'.pdf')) as b:
        assert [p.get_text() for p in a]==[p.get_text() for p in b]
    report={
        'status':'passed','date':DATE,'historical_baseline':HISTORICAL_HEAD,
        'documents':results,'main_and_retained_project_log_content_identical':True,
        'original_personal_log_copies_match_current_files':all(
            (PRIVATE/'source/original-personal-logs'/p.name).read_bytes()==p.read_bytes()
            for p in (ROOT/'Personal_logs').glob('*.md')),
        'verification_scope':'PDF text-page bounds, member names and recorded IDs, extracted-text markers, empty pages, Word ZIP/XML/reopen, document hashes, equivalent project-log copies and refreshed original logs. These are automated artifact checks; no human review or approval is claimed.',
    }
    assert report['original_personal_log_copies_match_current_files']
    (SOURCE/'document-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
