/* Editable Stage 2 deck. All visible type is at least 28 pt. */
const fs = require('fs');
const path = require('path');
const {createRequire} = require('module');
const req = createRequire(path.join(process.env.BLUE_IMPULSE_TOOLS || '/private/tmp/blue-impulse-stage2-tools','package.json'));
const pptxgen = req('pptxgenjs');
const sharp = req('sharp');
const fontkit = req('fontkit');
const {Resvg} = req('@resvg/resvg-js');
const BASE = path.resolve(__dirname,'..');
const ART = path.join(BASE,'art');
const OUT = path.resolve(BASE,'..');
const WORK = '/private/tmp/blue-impulse-stage2';
const PREVIEW = path.join(WORK,'previews');
fs.mkdirSync(PREVIEW,{recursive:true});
const C = {night:'180818',ink:'100B15',cream:'F9DEB5',gold:'FBB32A',orange:'E94E00',rose:'B34566',coral:'C76160',plum:'632644',purple:'3C0042',brown:'512317',muted:'D7A58B'};
const W=13.333333, H=7.5, PX=144;
const pptx = new pptxgen();
pptx.layout='LAYOUT_WIDE';
pptx.author='Blue Impulse / Nazif';
pptx.subject='Stage 2 visual structure: Sojourner, hardware, networks and behaviorist AI';
pptx.title='Blue Impulse — Sojourner';
pptx.company='Blue Impulse';
pptx.lang='en-GB';
pptx.theme={headFontFace:'Horizon Presentation',bodyFontFace:'Quicksand',lang:'en-GB'};
const fonts={Horizon:fontkit.openSync(path.join(WORK,'Horizon.ttf')),Quicksand:fontkit.openSync(path.join(BASE,'fonts/Quicksand-Medium.ttf'))};
const scenes=[];
const metadata=[];
let current;
let imageMeta={};
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');

function measure(text,face,size){return fonts[face].layout(text).glyphs.reduce((a,g)=>a+g.advanceWidth,0)/fonts[face].unitsPerEm*size/72;}
function fit(text,face,size,w){return Math.max(28,Math.min(size,size*w/Math.max(.01,measure(text,face,size))));}
function text(s,value,x,y,w,size=28,opt={}){
  const face=opt.face||'Quicksand';
  size=fit(value,face,size,w*.97);
  const h=opt.h||size/72*1.55;
  const config={x,y,w,h,fontFace:face==='Horizon'?'Horizon Presentation':face,fontSize:size,color:opt.color||C.cream,bold:face==='Horizon',margin:0,
    paraSpaceAfterPt:0,breakLine:false,vertAnchor:'top',valign:'top',align:opt.align||'left',
    isTextBox:true,objectName:opt.name||value,rotate:opt.rotate||0};
  s.addText(value,config);
  current.push({kind:'text',value,...config,logicalFont:face});
  return size;
}
function title(s,lines,opt={}){
  const x=opt.x??.72,y=opt.y??1.43,w=opt.w??11.9;
  const size=Math.min(...lines.map(t=>fit(t,'Horizon',opt.size||76,w*.97)));
  const step=opt.step||size/72*1.14;
  lines.forEach((t,i)=>text(s,t,x,y+i*step,w,size,{face:'Horizon',color:opt.color||C.cream,name:(opt.name||'Title')+' '+i}));
  return y+lines.length*step;
}
function shape(s,type,x,y,w,h,opt={}){
  const fill=opt.fill||C.cream;
  const transparency=opt.transparency??0;
  const line=opt.stroke?{color:opt.stroke,width:opt.width||1.5,transparency:opt.strokeTransparency||0}: {color:fill,transparency:100};
  s.addShape(type,{x,y,w,h,fill:{color:fill,transparency},line,rotate:opt.rotate||0,objectName:opt.name||type});
  current.push({kind:'shape',type,x,y,w,h,fill,transparency,...opt});
}
function line(s,x1,y1,x2,y2,opt={}){
  const x=Math.min(x1,x2),y=Math.min(y1,y2),w=Math.max(.001,Math.abs(x2-x1)),h=Math.max(.001,Math.abs(y2-y1));
  s.addShape(pptx.ShapeType.line,{x,y,w,h,flipH:x2<x1,flipV:y2<y1,
    line:{color:opt.color||C.gold,width:opt.width||2,transparency:opt.transparency||0,
      ...(opt.arrow?{endArrowType:'triangle'}:{})},objectName:opt.name||'Signal path'});
  current.push({kind:'line',x1,y1,x2,y2,...opt});
}
function img(s,file,x,y,w,h,opt={}){
  const p=path.join(ART,file),m=imageMeta[file];
  const factor=Math.min(w/m.width,h/m.height);
  const box=opt.fit==='cover'?{x,y,w,h,sizing:{type:'cover',w,h}}:{x:x+(w-m.width*factor)/2,y:y+(h-m.height*factor)/2,w:m.width*factor,h:m.height*factor};
  s.addImage({path:p,...box,rotate:opt.rotate||0,transparency:opt.transparency||0,
    objectName:opt.name||file,altText:opt.alt||file.replace(/[-_.]/g,' ')});
  current.push({kind:'image',file,x,y,w,h,...opt});
}
function bg(s,file='starfield.jpg'){img(s,file,0,0,W,H,{fit:'cover',name:'!!Background'});}
function footer(s,kicker){
  if(kicker)text(s,kicker,.74,.36,11.55,28,{color:C.muted,name:'Section label'});
  line(s,.75,1.06,1.22,1.06,{color:C.orange,width:4});
  text(s,String(scenes.length).padStart(2,'0'),11.88,6.78,.69,28,{align:'right',color:C.muted,name:'Slide number'});
}
function blank(s,x=.75,y=4.7,w=5.8,h=1.55,name='Future explanation'){
  s.addText('',{x,y,w,h,fontFace:'Quicksand',fontSize:32,margin:0,color:C.cream,isTextBox:true,objectName:name});
}
function slide(kicker,topic,notes='',transition='fade'){
  const s=pptx.addSlide();
  s.background={color:C.night};
  current=[]; scenes.push(current);
  metadata.push({number:scenes.length,topic,transition,notes});
  s.addNotes('VISUAL STRUCTURE ONLY — follow stage2-slide-outline.md.\n'+notes+'\nKeep all slide text at 28 pt or larger. Titles: Horizon. Body: Quicksand.\nNASA sources and the artwork process are listed in stage2-sojourner/README.md.');
  return s;
}
function planet(s,which,x,y,d,opt={}){
  if(opt.ring)shape(s,pptx.ShapeType.ellipse,x-.10,y-.10,d+.20,d+.20,{fill:opt.ring,name:'!!'+which+' ring'});
  img(s,which+'.png',x,y,d,d,{name:'!!'+which,alt:which==='earth'?'Earth, Apollo 17 NASA photograph':'Mars, NASA Viking mosaic'});
}
function rocket(s,x,y,w,h,rotation=0){img(s,'rocket.png',x,y,w,h,{rotate:rotation,name:'!!Rocket',alt:'Original symbolic retro rocket illustration'});}
function rover(s,x=7.05,y=1.35,w=5.4,h=5.35){img(s,'sojourner-cutout.png',x,y,w,h,{name:'!!Sojourner',alt:'Sojourner, cut out from NASA image PIA01122'});}
function picture(s,file,x=7.1,y=1.55,w=5.6,h=4.6){
  shape(s,pptx.ShapeType.rect,x-.13,y+.13,w,h,{fill:C.orange,rotate:2,name:'Photo backing'});
  img(s,file,x,y,w,h,{fit:'cover',name:'!!Photo'});
}
function splitTopic(kicker,topic,lines,opt={}){
  const s=slide(kicker,topic,opt.notes||'Leave the lower-left text area empty for the team to add content.',opt.transition||'morph');
  bg(s,opt.background||'starfield.jpg');
  if(opt.texture){img(s,'molten-ribbons.jpg',6.5,0,6.85,7.5,{fit:'cover',transparency:35,name:'!!Texture'});}
  footer(s,kicker);
  title(s,lines,{x:.74,y:1.44,w:opt.w||6.05,size:opt.size||65,step:opt.step});
  if(opt.label)text(s,opt.label,.77,opt.labelY||4.28,opt.labelW||6.0,28,{color:C.gold});
  if(opt.photo)picture(s,opt.photo,opt.px,opt.py,opt.pw,opt.ph);
  else if(opt.rover!==false)rover(s,opt.rx,opt.ry,opt.rw,opt.rh);
  blank(s,.78,opt.blankY||5.0,5.9,1.32);
  return s;
}
function divider(number,lines,kicker){
  const s=slide(kicker,kicker,'Chapter divider. No explanatory content is included.');
  bg(s,'molten-ribbons.jpg');
  shape(s,pptx.ShapeType.rect,0,0,8.5,H,{fill:C.night,transparency:18,name:'Title contrast'});
  text(s,number,8.1,3.3,4.7,240,{face:'Horizon',color:'A34139',name:'Chapter number'});
  footer(s,kicker);
  title(s,lines,{x:.72,y:1.7,w:11.45,size:76});
  return s;
}
function journey(label,phase,returning=false){
  const s=slide('MISSION / '+(returning?'RETURN':'OUTBOUND'),label,
    'Symbolic rocket journey, not a historical reconstruction of Pathfinder. Sojourner did not return to Earth. Advance through the adjacent slides in desktop PowerPoint to play the matched-object Morph movement.',phase===0?'fade':'morph');
  bg(s,'starfield.jpg'); footer(s,'MISSION / '+(returning?'RETURN':'OUTBOUND'));
  title(s,[label],{y:1.20,w:11.8,size:57});
  if(!returning){
    planet(s,'earth',.72,3.30,3.0);
    planet(s,'mars',9.05,2.43,3.5,{ring:C.orange});
    line(s,3.3,4.7,9.4,4.1,{color:C.plum,width:3});
    if(phase===0)rocket(s,2.5,2.42,1.4,3.0,37);
    if(phase===1)rocket(s,6.3,2.62,1.2,2.63,67);
    if(phase===2)rocket(s,9.95,2.4,1.0,2.35,0);
    text(s,'EARTH',1.12,6.3,2.3,30,{color:C.gold,name:'!!Earth label'});
    text(s,'MARS',9.86,6.3,2.3,30,{color:C.gold,name:'!!Mars label'});
  }else{
    planet(s,'mars',.75,3.15,3.15,{ring:C.orange});
    planet(s,'earth',9.05,2.56,3.5);
    line(s,3.8,4.65,9.25,4.22,{color:C.plum,width:3});
    rocket(s,phase===0?4.3:10.0,phase===0?2.6:2.54,1.05,2.4,phase===0?65:0);
    text(s,'MARS',1.12,6.3,2.3,30,{color:C.gold,name:'!!Mars label'});
    text(s,'EARTH',9.73,6.3,2.3,30,{color:C.gold,name:'!!Earth label'});
  }
  return s;
}
function pathNodes(s,signal,direction=1){
  planet(s,'earth',.82,3.62,2.2);
  shape(s,pptx.ShapeType.ellipse,5.58,3.64,2.10,2.10,{fill:C.brown,name:'!!Lander disc'});
  img(s,'pathfinder-lander.jpg',5.77,4.23,1.72,.81,{name:'!!Lander'});
  rover(s,10.02,3.52,2.6,2.62);
  line(s,direction===1?3.24:5.30,4.74,direction===1?5.30:3.24,4.74,{color:C.gold,width:2.5,arrow:true});
  line(s,direction===1?7.91:9.72,4.74,direction===1?9.72:7.91,4.74,{color:C.gold,width:2.5,arrow:true});
  text(s,'EARTH',.73,6.2,2.4,28,{align:'center',name:'!!Earth label'});
  text(s,'LANDER',5.32,6.2,2.6,28,{align:'center',name:'!!Lander label'});
  text(s,'SOJOURNER',9.62,6.2,3.15,28,{align:'center',name:'!!Rover label'});
  if(signal!=null)shape(s,pptx.ShapeType.ellipse,signal-.095,4.645,.19,.19,{fill:C.cream,name:'!!Signal'});
}

async function main(){
  // Every SVG also has a PNG representation for older presentation software.
  const rocketData=fs.readFileSync(path.join(ART,'rocket.svg'));
  await sharp(new Resvg(rocketData).render().asPng()).png().toFile(path.join(ART,'rocket.png'));
  for(const file of fs.readdirSync(ART)){
    if(/\.(png|jpg|jpeg)$/i.test(file))imageMeta[file]=await sharp(path.join(ART,file)).metadata();
  }
  let s;
  s=slide('', 'Blue Impulse','Opening title. The rocket is an original illustration; the planets are NASA photographs.');
  bg(s,'mars-landscape.jpg');
  planet(s,'mars',8.48,.43,4.57,{ring:C.orange});
  text(s,'BLUE',.65,1.38,7.55,120,{face:'Horizon',name:'Opening BLUE'});
  text(s,'IMPULSE',.65,3.13,11.9,120,{face:'Horizon',name:'Opening IMPULSE'});
  rocket(s,10.23,3.27,1.58,3.65,28);
  text(s,'SOJOURNER',.75,6.35,6,32,{color:C.gold});
  text(s,'A JOURNEY TO MARS',.74,.38,9.8,28,{color:C.muted});

  s=slide('OUR MISSION','Meet Sojourner','Introduce Sojourner and its connection to the three chapter topics. Leave detailed claims for the next content pass.','morph');
  bg(s,'starfield.jpg'); footer(s,'OUR MISSION');
  shape(s,pptx.ShapeType.ellipse,7.05,1.8,5.1,5.1,{fill:C.orange,name:'Sojourner halo'});
  title(s,['MEET','SOJOURNER'],{w:10.8,size:87,y:1.25});
  rover(s,7.14,1.95,5.06,4.93);
  text(s,'Hardware',.76,4.37,5.2,32,{color:C.gold});
  text(s,'Networks',.76,5.04,5.2,32,{color:C.gold});
  text(s,'Behaviorist AI',.76,5.71,5.5,32,{color:C.gold});

  journey('LEAVING EARTH',0);
  journey('NEXT STOP: MARS',1);
  journey('TOUCHDOWN',2);

  divider('01',['WHAT MAKES','SOJOURNER','WORK?'],'01 / HARDWARE');
  splitTopic('01 / HARDWARE','Sojourner overall body',['THE','ROVER'],{texture:true,label:'SOJOURNER’S OVERALL BODY',labelY:4.42});
  splitTopic('01 / HARDWARE','Information collection',['COLLECTING','INFORMATION'],{size:58,w:8.8,rx:8.25,ry:3.18,rw:4.25,rh:3.32,blankY:4.78});
  splitTopic('01 / HARDWARE','The lander',['MEET THE','LANDER'],{photo:'pathfinder-lander.jpg',px:6.83,py:4.0,pw:5.73,ph:2.65,w:9.6,size:80,blankY:4.65});

  s=slide('01 / HARDWARE','Lander hardware','The three instrument headings come directly from the outline. Do not add specifications yet.','morph');
  bg(s,'starfield.jpg');footer(s,'01 / HARDWARE');title(s,['LANDER','HARDWARE'],{w:10.4,size:85,y:1.32});
  text(s,'Stereoscopic camera',.79,4.27,7,32,{color:C.gold});
  text(s,'IMP filters',.79,5.0,7,32,{color:C.gold});
  text(s,'ASI / MET',.79,5.73,7,32,{color:C.gold});
  picture(s,'pathfinder-lander.jpg',8.0,4.15,4.38,2.05);

  splitTopic('01 / HARDWARE','Cameras',['CAMERAS'],{w:10.5,size:102,photo:'sojourner-on-mars.jpg',px:7.35,py:2.74,pw:4.92,ph:3.54,blankY:3.7});
  splitTopic('01 / HARDWARE','The rear: APXS',['AT THE','REAR'],{size:87,w:7.5,label:'APXS',labelY:4.31,photo:'sojourner-rear.jpg',px:7.08,py:2.8,pw:5.30,ph:3.97,blankY:5.16});
  splitTopic('01 / HARDWARE','Wheels and wheel abrasion experiment',['WHEELS','AT WORK'],{size:70,label:'WHEEL ABRASION EXPERIMENT',labelW:8.2,labelY:4.14,rx:7.44,ry:2.62,rw:4.85,rh:4.30,blankY:5.03});
  s=splitTopic('01 / HARDWARE','Antenna and UHF radio',['ANTENNA','+ UHF RADIO'],{size:63,w:9.4,rx:8.56,ry:3.28,rw:3.65,rh:3.59,blankY:4.8});
  [0,1,2].forEach(i=>shape(s,pptx.ShapeType.ellipse,8.05-i*.43,2.15-i*.23,3.15+i*.86,3.15+i*.46,{fill:C.night,transparency:100,stroke:C.plum,width:1.2,name:'Radio ring '+i}));

  divider('02',['HOW DOES','SOJOURNER','COMMUNICATE?'],'02 / NETWORKS');
  s=slide('02 / NETWORKS','Communication path','Communication-path structure only. Future explanatory text belongs in the notes or the blank area, at 28 pt or larger.');
  bg(s);footer(s,'02 / NETWORKS');title(s,['THE CONNECTION'],{size:77,y:1.3,w:11.8});pathNodes(s,null);

  for(const direction of [1,-1]){
    for(const part of [1,2]){
      const outbound=direction===1;
      s=slide('02 / NETWORKS',`${outbound?'Earth to Sojourner':'Sojourner to Earth'} (${part})`,
        `Part ${part} of a two-slide communication sequence. The moving point is a visual cue only; add transmission details later.`,'morph');
      bg(s);footer(s,'02 / NETWORKS');
      title(s,[outbound?'EARTH TO':'SOJOURNER TO',outbound?'SOJOURNER':'EARTH'],{w:10.3,size:57,y:1.24,step:.93});
      text(s,`${part} / 2`,11.07,1.38,1.35,28,{color:C.gold,align:'right'});
      const sig=outbound?(part===1?4.08:8.76):(part===1?8.76:4.08);
      pathNodes(s,sig,direction);
    }
  }
  splitTopic('02 / NETWORKS','UHF radio link',['THE','UHF LINK'],{size:86,w:8.1,texture:true,rx:7.32,ry:2.18,rw:5.1,rh:4.77});

  s=slide('02 / NETWORKS','Half-duplex','Two directional visual lanes. Leave detailed explanation blank.','morph');
  bg(s);footer(s,'02 / NETWORKS');title(s,['HALF-','DUPLEX'],{w:9.3,size:110,y:1.36,step:1.53});
  line(s,7.83,4.72,12.18,4.72,{color:C.orange,width:13,arrow:true});
  line(s,12.18,5.52,7.83,5.52,{color:C.plum,width:13,arrow:true});blank(s,.77,5.04,6.3,1.53);

  s=slide('02 / NETWORKS','Heartbeat and communication checks','Heartbeat motif only. The intended checks and details remain to be added.','morph');
  bg(s);footer(s,'02 / NETWORKS');title(s,['STILL','CONNECTED?'],{w:10.9,size:89,y:1.4});
  text(s,'HEARTBEAT & COMMUNICATION CHECKS',.78,4.62,11.8,28,{color:C.gold});
  const pts=[[.8,6.1],[3.8,6.1],[4.27,5.78],[4.7,6.40],[5.18,5.51],[5.73,6.1],[12.1,6.1]];
  for(let i=1;i<pts.length;i++)line(s,...pts[i-1],...pts[i],{color:C.orange,width:3.5});

  splitTopic('02 / NETWORKS','Communication limitations',['WORKING','WITH LIMITS'],{size:72,w:10.3,label:'MEMORY / COMMUNICATION',labelW:9,labelY:4.35,rx:9.08,ry:3.56,rw:3.2,rh:3.03,blankY:5.15});
  splitTopic('02 / NETWORKS','How Sojourner made decisions',['WHEN TO','DECIDE'],{size:90,w:8.9,texture:true,rx:7.95,ry:2.67,rw:4.2,rh:4.0,notes:'Transition into the behaviorist-AI discussion. Do not assert that Sojourner used reinforcement learning.'});

  divider('03',['HOW','SOJOURNER','DECIDES'],'03 / BEHAVIORIST AI');

  s=slide('03 / BEHAVIORIST AI','Can Sojourner be an example for behaviorist AI?','This is deliberately a question, not an assertion that Sojourner learned using reinforcement learning.');
  bg(s,'mars-landscape.jpg');footer(s,'03 / BEHAVIORIST AI');
  text(s,'CAN SOJOURNER BE AN EXAMPLE?',.77,1.53,11.6,32,{color:C.gold});
  title(s,['BEHAVIORIST','AI?'],{w:11.8,size:85,y:2.42});
  rover(s,9.9,4.49,2.4,2.33);

  s=slide('03 / BEHAVIORIST AI','Safa vs Nazif','Introduce Safa and Nazif’s argument, points and claims. The two text areas are intentionally empty. No position has been invented for either person.');
  bg(s,'molten-ribbons.jpg');
  shape(s,pptx.ShapeType.rect,0,0,6.68,H,{fill:C.plum,transparency:16,name:'Safa half'});
  shape(s,pptx.ShapeType.rect,6.68,0,6.66,H,{fill:'7D250E',transparency:24,name:'Nazif half'});
  text(s,'THE ARGUMENT',.74,.4,11.2,28,{color:C.cream});
  text(s,'SAFA',.74,2.03,5.65,102,{face:'Horizon'});
  text(s,'NAZIF',7.12,2.03,5.49,102,{face:'Horizon'});
  text(s,'vs',5.95,3.66,1.48,40,{align:'center',color:C.gold});
  blank(s,.77,4.72,5.18,1.60,'Safa argument');blank(s,7.26,4.72,5.12,1.6,'Nazif argument');
  text(s,String(scenes.length).padStart(2,'0'),11.88,6.78,.69,28,{align:'right',color:C.cream});

  for(const part of [1,2]){
    s=slide('03 / BEHAVIORIST AI',`Stimulus and response (${part})`,'Leave the stimulus and response examples blank for the content pass.','morph');
    bg(s);footer(s,'03 / BEHAVIORIST AI');
    title(s,['STIMULUS','RESPONSE'],{w:10.4,size:91,y:1.38,step:1.32});
    text(s,`${part} / 2`,11.12,1.44,1.26,28,{align:'right',color:C.gold});
    line(s,6.80,5.58,10.86,5.58,{color:C.plum,width:3,arrow:true});
    shape(s,pptx.ShapeType.ellipse,part===1?7.0:10.2,5.43,.3,.3,{fill:C.orange,name:'!!Response cue'});
    blank(s,.76,4.79,5.7,1.5,'Stimulus / response example');
  }

  s=slide('03 / BEHAVIORIST AI','Rover behavior video','Video placeholder only. No video has been fabricated or embedded. Replace the empty video frame with the selected real rover clip.');
  bg(s);footer(s,'03 / BEHAVIORIST AI');title(s,['WATCH IT HAPPEN'],{w:11.7,size:69,y:1.35});
  shape(s,pptx.ShapeType.rect,.8,3.0,11.64,3.25,{fill:'21131E',stroke:C.plum,width:1,name:'Replace with rover video'});
  shape(s,pptx.ShapeType.ellipse,5.79,3.74,1.5,1.5,{fill:C.orange,name:'Video placeholder button'});
  shape(s,pptx.ShapeType.triangle,6.33,4.14,.49,.64,{fill:C.cream,rotate:90,name:'Video placeholder play mark'});

  s=slide('03 / BEHAVIORIST AI','Comparison with Curiosity and Perseverance','Comparison headings only. The right-side NASA photo shows engineering models of Curiosity and Perseverance, not Sojourner. Do not add comparative claims yet.');
  bg(s,'starfield.jpg');footer(s,'03 / BEHAVIORIST AI');title(s,['WHY','SOJOURNER?'],{w:11.5,size:95,y:1.32});
  rover(s,1.08,4.14,2.46,2.31);
  text(s,'Curiosity',4.51,4.72,4.2,32,{color:C.gold});
  text(s,'Perseverance',4.51,5.47,4.2,32,{color:C.gold});
  picture(s,'curiosity-perseverance.jpg',9.96,3.93,2.16,2.85);

  s=slide('CONCLUSION','How everything comes together','Structural integration diagram: Input → Process → Output, with Networking and Decision Making. The arrows are organisational scaffolding, not a detailed architecture.');
  bg(s,'molten-ribbons.jpg');footer(s,'CONCLUSION');title(s,['ONE CONNECTED','SYSTEM'],{w:11.65,size:64,y:1.39});
  const nodes=[{t:'INPUT',x:1.0},{t:'PROCESS',x:5.05},{t:'OUTPUT',x:9.26}];
  nodes.forEach(n=>text(s,n.t,n.x,4.5,3.06,38,{face:'Quicksand',color:C.cream,align:'center'}));
  line(s,3.9,4.88,4.85,4.88,{color:C.gold,width:3,arrow:true});line(s,8.2,4.88,9.0,4.88,{color:C.gold,width:3,arrow:true});
  text(s,'NETWORKING',.97,6.03,4.4,30,{color:C.gold});text(s,'DECISION MAKING',7.48,6.03,4.9,30,{color:C.gold,align:'right'});

  s=slide('YOUR TURN','Game','Intentionally blank game slide. Add the game only after its content is agreed.');
  bg(s,'starfield.jpg');footer(s,'YOUR TURN');title(s,['GAME'],{w:11.8,size:160,y:1.68});blank(s,.79,4.14,11.7,2.2,'Game placeholder — intentionally empty');

  journey('HOMEWARD BOUND',0,true);
  journey('BACK TO EARTH',1,true);

  s=slide('','Thank you','Closing slide. The return rocket is a storytelling device; Sojourner remained on Mars.','morph');
  bg(s,'molten-ribbons.jpg');
  planet(s,'earth',8.7,2.95,3.86);
  title(s,['THANK','YOU'],{x:.74,y:1.53,w:10.9,size:132,step:1.82});
  text(s,'BLUE IMPULSE',.79,6.36,6.8,32,{color:C.gold});
  rocket(s,10.16,2.50,.93,2.23,0);

  const raw=path.join(WORK,'BlueImpulse_Stage2_Sojourner.unpatched.pptx');
  await pptx.writeFile({fileName:raw,compression:true});
  fs.writeFileSync(path.join(BASE,'source/slides.json'),JSON.stringify(metadata,null,2)+'\n');
  fs.writeFileSync(path.join(WORK,'scenes.json'),JSON.stringify(scenes));
  await renderPreviews();
  console.log(JSON.stringify({slides:scenes.length,raw,previews:PREVIEW}));
}

const dataCache=new Map();
function imageUri(file){
  if(!dataCache.has(file))dataCache.set(file,'data:image/'+(file.endsWith('.png')?'png':'jpeg')+';base64,'+fs.readFileSync(path.join(ART,file)).toString('base64'));
  return dataCache.get(file);
}
function textPath(item){
  const f=fonts[item.logicalFont||item.fontFace],run=f.layout(item.value),scale=item.fontSize*2/f.unitsPerEm;
  const advance=run.positions.reduce((a,p)=>a+p.xAdvance,0)*scale;
  let x=item.x*PX;
  if(item.align==='center')x+=(item.w*PX-advance)/2;
  if(item.align==='right')x+=item.w*PX-advance;
  const baseline=item.y*PX+f.ascent*scale;
  let offset=0,out='';
  run.glyphs.forEach((g,i)=>{
    const p=run.positions[i];
    out+=`<path d="${g.path.toSVG()}" transform="translate(${x+(offset+p.xOffset)*scale},${baseline-p.yOffset*scale}) scale(${scale},${-scale})"/>`;
    offset+=p.xAdvance;
  });
  return `<g fill="#${item.color}">${out}</g>`;
}
async function renderPreviews(){
  for(let index=0;index<scenes.length;index++){
    let parts=[];
    scenes[index].forEach((o,i)=>{
      if(o.kind==='text'){parts.push(textPath(o));return;}
      if(o.kind==='image'){
        const x=o.x*PX,y=o.y*PX,w=o.w*PX,h=o.h*PX;
        const rot=o.rotate?` transform="rotate(${o.rotate} ${x+w/2} ${y+h/2})"`:'';
        parts.push(`<g${rot} opacity="${1-(o.transparency||0)/100}"><svg x="${x}" y="${y}" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" overflow="hidden"><image width="${w}" height="${h}" href="${imageUri(o.file)}" preserveAspectRatio="xMidYMid ${o.fit==='cover'?'slice':'meet'}"/></svg></g>`);return;
      }
      if(o.kind==='line'){
        const stroke=o.color||C.gold,sw=(o.width||2)*2;
        parts.push(`<line x1="${o.x1*PX}" y1="${o.y1*PX}" x2="${o.x2*PX}" y2="${o.y2*PX}" stroke="#${stroke}" stroke-width="${sw}" opacity="${1-(o.transparency||0)/100}"/>`);
        if(o.arrow){
          const a=Math.atan2(o.y2-o.y1,o.x2-o.x1),x=o.x2*PX,y=o.y2*PX,l=Math.max(14,sw*2),r=Math.max(7,sw);
          parts.push(`<path d="M${x},${y} L${x-l*Math.cos(a)+r*Math.sin(a)},${y-l*Math.sin(a)-r*Math.cos(a)} L${x-l*Math.cos(a)-r*Math.sin(a)},${y-l*Math.sin(a)+r*Math.cos(a)} Z" fill="#${stroke}"/>`);
        }return;
      }
      const x=o.x*PX,y=o.y*PX,w=o.w*PX,h=o.h*PX;
      const sty=`fill="#${o.fill}" fill-opacity="${1-o.transparency/100}" stroke="${o.stroke?'#'+o.stroke:'none'}" stroke-width="${(o.width||1.5)*2}"`;
      const rot=o.rotate?` transform="rotate(${o.rotate} ${x+w/2} ${y+h/2})"`:'';
      if(o.type===pptx.ShapeType.ellipse)parts.push(`<ellipse cx="${x+w/2}" cy="${y+h/2}" rx="${w/2}" ry="${h/2}" ${sty}${rot}/>`);
      else if(o.type===pptx.ShapeType.triangle)parts.push(`<path d="M${x+w/2},${y} L${x+w},${y+h} L${x},${y+h} Z" ${sty}${rot}/>`);
      else parts.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" ${sty}${rot}/>`);
    });
    const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><rect width="1920" height="1080" fill="#${C.night}"/>${parts.join('')}</svg>`;
    const buffer=new Resvg(svg).render().asPng();
    await sharp(buffer).jpeg({quality:91}).toFile(path.join(PREVIEW,`slide-${String(index+1).padStart(2,'0')}.jpg`));
  }
  const thumbs=[];
  for(let i=0;i<scenes.length;i++){
    const b=await sharp(path.join(PREVIEW,`slide-${String(i+1).padStart(2,'0')}.jpg`)).resize(384,216).toBuffer();
    thumbs.push({input:b,left:(i%5)*400+8,top:Math.floor(i/5)*232+8});
  }
  await sharp({create:{width:2000,height:Math.ceil(scenes.length/5)*232,channels:3,background:'#F4E5D5'}}).composite(thumbs).jpeg({quality:94}).toFile(path.join(OUT,'BlueImpulse_Stage2_Overview.jpg'));
  fs.copyFileSync(path.join(PREVIEW,'slide-01.jpg'),path.join(BASE,'cover.jpg'));
}
main().catch(error=>{console.error(error);process.exit(1);});
