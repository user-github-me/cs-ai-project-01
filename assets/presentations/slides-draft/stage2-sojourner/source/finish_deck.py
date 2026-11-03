"""Embed the permitted fonts, add native Morph, and deduplicate the PowerPoint media."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import posixpath
import struct
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont

BASE = Path(__file__).resolve().parents[1]
WORK = Path('/private/tmp/blue-impulse-stage2')
DEST = BASE.parent/'BlueImpulse_Stage2_Sojourner.pptx'
NS = {
    'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'mc':'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'p14':'http://schemas.microsoft.com/office/powerpoint/2010/main',
    'p159':'http://schemas.microsoft.com/office/powerpoint/2015/09/main',
}
REL='http://schemas.openxmlformats.org/package/2006/relationships'
CT='http://schemas.openxmlformats.org/package/2006/content-types'
for key,val in NS.items(): ET.register_namespace(key,val)


def xml(root):
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)


def eot(path, family='Quicksand', style='Medium'):
    data=path.read_bytes()
    f=TTFont(path); os2=f['OS/2']; head=f['head']
    assert os2.fsType==0, 'Only installable-embedding fonts are used.'
    panose=bytes(getattr(os2.panose,key) for key in ['bFamilyType','bSerifStyle','bWeight','bProportion','bContrast','bStrokeVariation','bArmStyle','bLetterForm','bMidline','bXHeight'])
    b=struct.pack('<4I',0,len(data),0x00020001,0)+panose
    b+=struct.pack('<BBIHH',1,0,os2.usWeightClass,os2.fsType,0x504C)
    b+=struct.pack('<4I',*[getattr(os2,'ulUnicodeRange'+str(i),0) for i in range(1,5)])
    b+=struct.pack('<2I',getattr(os2,'ulCodePageRange1',0),getattr(os2,'ulCodePageRange2',0))
    b+=struct.pack('<5I',head.checkSumAdjustment,0,0,0,0)
    for name in [family,style,'Version 1.0',family+' '+style]:
        value=name.encode('utf-16le'); b+=struct.pack('<HH',0,len(value))+value
    b+=struct.pack('<HH',0,0)
    output=bytearray(b+data)
    struct.pack_into('<I',output,0,len(output))
    return bytes(output)


with ZipFile(WORK/'BlueImpulse_Stage2_Sojourner.unpatched.pptx') as archive:
    files={name:archive.read(name) for name in archive.namelist() if not name.endswith('/')}
slides=json.loads((BASE/'source/slides.json').read_text())
for item in slides:
    name=f'ppt/slides/slide{item["number"]}.xml'
    root=ET.fromstring(files[name])
    position=next((i+1 for i,n in enumerate(root) if n.tag==f'{{{NS["p"]}}}clrMapOvr'),1)
    duration='1500' if item['transition']=='morph' else '600'
    if item['transition']=='morph':
        alternate=ET.Element(f'{{{NS["mc"]}}}AlternateContent')
        choice=ET.SubElement(alternate,f'{{{NS["mc"]}}}Choice',{'Requires':'p159'})
        transition=ET.SubElement(choice,f'{{{NS["p"]}}}transition',{'spd':'slow','advClick':'1',f'{{{NS["p14"]}}}dur':duration})
        ET.SubElement(transition,f'{{{NS["p159"]}}}morph',{'option':'byObject'})
        fallback=ET.SubElement(alternate,f'{{{NS["mc"]}}}Fallback')
        ft=ET.SubElement(fallback,f'{{{NS["p"]}}}transition',{'spd':'slow','advClick':'1'})
        ET.SubElement(ft,f'{{{NS["p"]}}}fade')
        root.insert(position,alternate)
    else:
        transition=ET.Element(f'{{{NS["p"]}}}transition',{'spd':'med','advClick':'1'})
        ET.SubElement(transition,f'{{{NS["p"]}}}fade')
        root.insert(position,transition)
    files[name]=xml(root)

presentation=ET.fromstring(files['ppt/presentation.xml'])
presentation.set('embedTrueTypeFonts','1')
presentation.set('saveSubsetFonts','0')
fontlist=ET.Element(f'{{{NS["p"]}}}embeddedFontLst')
rels=ET.fromstring(files['ppt/_rels/presentation.xml.rels'])
new_id=max(int(n.get('Id')[3:]) for n in rels if n.get('Id','').startswith('rId'))+1
for offset,(family,data) in enumerate([
    ('Horizon Presentation',eot(WORK/'Horizon.ttf','Horizon Presentation','Bold')),
    ('Quicksand',eot(BASE/'fonts/Quicksand-Medium.ttf')),
]):
    rid=f'rId{new_id+offset}'
    part=f'fonts/font{offset+1}.fntdata'
    files['ppt/'+part]=data
    entry=ET.SubElement(fontlist,f'{{{NS["p"]}}}embeddedFont')
    ET.SubElement(entry,f'{{{NS["p"]}}}font',{'typeface':family,'charset':'0'})
    for font_style in (['regular','bold'] if family=='Horizon Presentation' else ['regular']):
        ET.SubElement(entry,f'{{{NS["p"]}}}{font_style}',{f'{{{NS["r"]}}}id':rid})
    ET.SubElement(rels,f'{{{REL}}}Relationship',{'Id':rid,'Type':NS['r']+'/font','Target':part})
position=next((i for i,n in enumerate(presentation) if n.tag==f'{{{NS["p"]}}}defaultTextStyle'),len(presentation))
presentation.insert(position,fontlist)
files['ppt/presentation.xml']=xml(presentation)
files['ppt/_rels/presentation.xml.rels']=xml(rels)
ct=ET.fromstring(files['[Content_Types].xml'])
if not any(n.get('Extension')=='fntdata' for n in ct):
    ET.SubElement(ct,f'{{{CT}}}Default',{'Extension':'fntdata','ContentType':'application/x-fontdata'})
files['[Content_Types].xml']=xml(ct)

# PptxGenJS repeats assets across slides. Keep one copy of each identical media file.
canonical={}; replacements={}
for name,data in sorted(files.items()):
    if name.startswith('ppt/media/'):
        digest=hashlib.sha256(data).hexdigest()
        if digest in canonical: replacements[name]=canonical[digest]
        else: canonical[digest]=name
for name,data in list(files.items()):
    if not name.endswith('.rels'): continue
    root=ET.fromstring(data); modified=False
    folder=posixpath.dirname(posixpath.dirname(name))
    for rel in root:
        if rel.get('TargetMode')=='External':continue
        target=posixpath.normpath(posixpath.join(folder,rel.get('Target','')))
        if target in replacements:
            rel.set('Target',posixpath.relpath(replacements[target],folder));modified=True
    if modified:files[name]=xml(root)
for name in replacements:del files[name]

with ZipFile(DEST,'w',ZIP_DEFLATED,compresslevel=8) as archive:
    for name,data in files.items():archive.writestr(name,data)

visible=[]; morph_count=0; rel_errors=[]
for item in slides:
    root=ET.fromstring(files[f'ppt/slides/slide{item["number"]}.xml'])
    morph_count+=len(root.findall('.//p159:morph',NS))
    for run in root.findall('.//a:r',NS):
        node=run.find('a:t',NS)
        if node is not None and node.text:
            prop=run.find('a:rPr',NS)
            size=int(prop.get('sz','0'))/100
            assert size>=28, (item['number'],node.text,size)
            visible.append(size)
for name,data in files.items():
    if name.endswith('.xml') or name.endswith('.rels'):ET.fromstring(data)
    if not name.endswith('.rels'):continue
    base=posixpath.dirname(posixpath.dirname(name))
    if name=='_rels/.rels':base=''
    for rel in ET.fromstring(data):
        if rel.get('TargetMode')=='External':continue
        target=posixpath.normpath(posixpath.join(base,rel.get('Target','')))
        if target not in files:rel_errors.append((name,target))
assert not rel_errors,rel_errors
with ZipFile(DEST) as archive:assert archive.testzip() is None
print(json.dumps({'slides':len(slides),'min_visible_font_pt':min(visible),'morph_transitions':morph_count,'embedded_fonts':['Horizon Presentation','Quicksand'],'deduplicated_media':len(replacements),'bytes':DEST.stat().st_size,'file':str(DEST)},indent=2))
