"""Embed licensed Inter regular and bold fonts in the editable deck."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import struct
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
B=Path(__file__).resolve().parents[1]
P='http://schemas.openxmlformats.org/presentationml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL='http://schemas.openxmlformats.org/package/2006/relationships'
CT='http://schemas.openxmlformats.org/package/2006/content-types'
for name,uri in [('p',P),('r',R)]:ET.register_namespace(name,uri)
def eot(file,style):
    data=file.read_bytes();f=TTFont(file);o=f['OS/2'];assert o.fsType==0
    panose=bytes(getattr(o.panose,k) for k in ['bFamilyType','bSerifStyle','bWeight','bProportion','bContrast','bStrokeVariation','bArmStyle','bLetterForm','bMidline','bXHeight'])
    b=struct.pack('<4I',0,len(data),0x00020001,0)+panose
    b+=struct.pack('<BBIHH',1,0,o.usWeightClass,o.fsType,0x504C)
    b+=struct.pack('<4I',*[getattr(o,'ulUnicodeRange'+str(i),0) for i in range(1,5)])
    b+=struct.pack('<2I',getattr(o,'ulCodePageRange1',0),getattr(o,'ulCodePageRange2',0))
    b+=struct.pack('<5I',f['head'].checkSumAdjustment,0,0,0,0)
    for name in ['Inter',style,'Version 1.0','Inter '+style]:
        v=name.encode('utf-16le');b+=struct.pack('<HH',0,len(v))+v
    b+=struct.pack('<HH',0,0);output=bytearray(b+data);struct.pack_into('<I',output,0,len(output));return bytes(output)
dest=B/'BlueImpulse_Stage2_PPT_V1.pptx'
with ZipFile(dest) as z:files={n:z.read(n) for n in z.namelist() if not n.endswith('/')}
pres=ET.fromstring(files['ppt/presentation.xml']);pres.set('embedTrueTypeFonts','1');pres.set('saveSubsetFonts','0')
old=pres.find('{'+P+'}embeddedFontLst')
if old is not None:pres.remove(old)
fl=ET.Element('{'+P+'}embeddedFontLst');entry=ET.SubElement(fl,'{'+P+'}embeddedFont');ET.SubElement(entry,'{'+P+'}font',{'typeface':'Inter','charset':'0'})
rels=ET.fromstring(files['ppt/_rels/presentation.xml.rels'])
for e in list(rels):
    if e.get('Type')==R+'/font':rels.remove(e)
rid=max(int(n.get('Id')[3:]) for n in rels if n.get('Id','').startswith('rId'))+1
for i,(sty,tag) in enumerate([('Regular','regular'),('Bold','bold')]):
    f=f'fonts/inter-{sty.lower()}.fntdata';id='rId'+str(rid+i);files['ppt/'+f]=eot(B/'fonts'/f'Inter-{sty}.ttf',sty)
    ET.SubElement(entry,'{'+P+'}'+tag,{'{'+R+'}id':id})
    ET.SubElement(rels,'{'+REL+'}Relationship',{'Id':id,'Type':R+'/font','Target':f})
idx=next((i for i,n in enumerate(pres) if n.tag=='{'+P+'}defaultTextStyle'),len(pres));pres.insert(idx,fl)
ct=ET.fromstring(files['[Content_Types].xml'])
if not any(n.get('Extension')=='fntdata' for n in ct):ET.SubElement(ct,'{'+CT+'}Default',{'Extension':'fntdata','ContentType':'application/x-fontdata'})
for fn,x in [('ppt/presentation.xml',pres),('ppt/_rels/presentation.xml.rels',rels),('[Content_Types].xml',ct)]:files[fn]=ET.tostring(x,encoding='utf-8',xml_declaration=True)
with ZipFile(dest,'w',ZIP_DEFLATED) as z:
    for n,b in files.items():z.writestr(n,b)
print('Embedded Inter regular and bold; editable text and native notes preserved.')
