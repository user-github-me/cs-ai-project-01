"""Open the actual PowerPoint with Keynote and export the supplementary PDF.

Does not save or change the PPTX. Installs only these licensed project fonts if
absent. This is an application import/export check, not a human rehearsal.
"""
from pathlib import Path
import shutil,subprocess
B=Path(__file__).resolve().parents[1]
fonts=Path.home()/'Library/Fonts';fonts.mkdir(exist_ok=True)
for name in ['Regular','Bold']:
    f=fonts/f'BlueImpulseTeaching-Inter-{name}.ttf'
    if not f.exists():shutil.copy2(B/'fonts'/f'Inter-{name}.ttf',f)
def q(s):return '"'+str(s).replace('\\','\\\\').replace('"','\\"')+'"'
src=B/'BlueImpulse_Stage2_PPT_V1.pptx';out=B/'BlueImpulse_Stage2_PPT_V1.pdf'
subprocess.run(['open','-a','Keynote',str(src)],check=True)
script=f'''with timeout of 300 seconds
tell application "Keynote"
set teachingDeck to open (POSIX file {q(src)})
delay 3
export teachingDeck to (POSIX file {q(out)}) as PDF
close teachingDeck saving no
end tell
end timeout'''
subprocess.run(['osascript','-e',script],check=True)
print(out)
