/* Editable native PowerPoint shapes/text. No linked media or network dependencies. */
const fs=require('fs'),path=require('path'),{createRequire}=require('module');
const depRoot=process.env.BLUE_IMPULSE_TOOLS||(fs.existsSync(path.join(__dirname,'node_modules'))?__dirname:'/private/tmp/blue-impulse-stage2-tools');
const req=createRequire(path.join(depRoot,'package.json')); 
const PptxGenJS=req('pptxgenjs'),fontkit=req('fontkit');
const B=path.resolve(__dirname,'..'),S=JSON.parse(fs.readFileSync(path.join(__dirname,'slides.json')));
const pptx=new PptxGenJS();pptx.layout='LAYOUT_WIDE';pptx.author='Blue Impulse';pptx.company='Blue Impulse';
pptx.title='Blue Impulse | Hardware, Networking and Behaviorist AI | Stage 2 PPT V1.0';
pptx.subject='Complete six-chapter classroom teaching module';pptx.lang='en-GB';
pptx.theme={headFontFace:'Inter',bodyFontFace:'Inter',lang:'en-GB'};
const C={bg:'111936',white:'FFF6FA',pink:'FF4385'};
const F={regular:fontkit.openSync(path.join(B,'fonts/Inter-Regular.ttf')),bold:fontkit.openSync(path.join(B,'fonts/Inter-Bold.ttf'))};
const W=13.333333,H=7.5,A=[];let shapes=[],cur;
function width(t,size,bold=false){const f=F[bold?'bold':'regular'];return f.layout(String(t)).glyphs.reduce((n,g)=>n+g.advanceWidth,0)/f.unitsPerEm*size/72;}
function wrap(t,size,w,bold=false){let out=[];for(const line of String(t).split('\n')){let acc='';for(const word of line.split(' ')){const next=acc?acc+' '+word:word;if(acc&&width(next,size,bold)>w){out.push(acc);acc=word;}else acc=next;}out.push(acc);}return out;}
function text(s,t,x,y,w,h,size=30,opt={}){t=String(t).replaceAll('→','to');const lines=wrap(t,size,w-.06,opt.bold),need=lines.length*size/72*1.15;
 if(need>h+.025)throw Error(`Slide ${cur.number}: text too high (${need.toFixed(2)} > ${h}) ${t}`);
 if(lines.some(l=>width(l,size,opt.bold)>w+.005))throw Error(`Slide ${cur.number}: text too wide ${t}`);
 s.addText(lines.join('\n'),{x,y,w,h,fontFace:'Inter',fontSize:size,bold:opt.bold||false,color:opt.color||C.white,margin:0,
 breakLine:false,paraSpaceAfterPt:0,lineSpacingMultiple:1.0,valign:opt.valign||'mid',align:opt.align||'left',objectName:String(t).slice(0,80)});
 shapes.push({kind:'text',text:t,x,y,w,h,size,lines:lines.length});
}
function rect(s,x,y,w,h,fill=C.bg,stroke=C.white,round=false){s.addShape(round?pptx.ShapeType.roundRect:pptx.ShapeType.rect,{x,y,w,h,rectRadius:.12,fill:{color:fill},line:{color:stroke,width:2},radius:.12});shapes.push({kind:'rect',x,y,w,h});}
function line(s,x1,y1,x2,y2,color=C.pink,arrow=false,width=2.5){s.addShape(pptx.ShapeType.line,{x:Math.min(x1,x2),y:Math.min(y1,y2),w:Math.max(.001,Math.abs(x2-x1)),h:Math.max(.001,Math.abs(y2-y1)),flipH:x1>x2,flipV:y1>y2,line:{color,width,...(arrow?{endArrowType:'triangle'}:{})}});}
function dot(s,x,y,r=.10,color=C.pink){s.addShape(pptx.ShapeType.ellipse,{x:x-r,y:y-r,w:r*2,h:r*2,fill:{color},line:{color,transparency:100}});}
function card(s,t,x,y,w,h,opt={}){rect(s,x,y,w,h,opt.fill||C.bg,opt.stroke||C.pink);text(s,t,x+.23,y+.1,w-.46,h-.2,opt.size||32,{bold:opt.bold,...opt});}
function headers(s,d){
 text(s,`CHAPTER ${d.chapter} · ${['','THE FUNDAMENTALS','BEHAVIORISM & BEHAVIORIST AI','HARDWARE','NETWORKING','APPLICATIONS','STRENGTHS & LIMITATIONS'][d.chapter]}`,.65,.36,12.0,.48,28,{color:C.pink,bold:true});
 let size=42;if(wrap(d.title,size,12.0,true).length>2)size=38;
 text(s,d.title,.65,1.06,12.0,1.34,size,{bold:true});
 text(s,String(d.number).padStart(2,'0'),11.91,6.91,.75,.44,28,{align:'right'});
 if(d.activity){const seconds=(d.activity.match(/\d+ seconds/)||['DISCUSS'])[0].toUpperCase();text(s,`YOUR TURN · ${seconds}`,.65,6.69,10.8,.52,28,{color:C.pink,bold:true});}
}
function table(s,rows,head,x=.7,y=2.57,w=11.95,h=3.64){const n=rows.length+(head?1:0),rh=h/n,cols=rows[0].length,cw=w/cols;
 (head?[head,...rows]:rows).forEach((r,i)=>{for(let j=0;j<cols;j++){rect(s,x+j*cw,y+i*rh,cw,rh,i===0&&head?C.pink:C.bg,i===0&&head?C.pink:C.white);text(s,String(r[j]),x+j*cw+.13,y+i*rh+.025,cw-.26,rh-.05,28,{color:i===0&&head?C.bg:C.white,bold:i===0&&!!head});}});
}
function flow(s,items){const n=items.length,w=(11.95-(n-1)*.45)/n;items.forEach((v,i)=>{const x=.7+i*(w+.45);card(s,v,x,2.80,w,2.42,{size:n>3?28:31,align:'center',bold:true});if(i<n-1)line(s,x+w+.04,4,x+w+.40,4,C.pink,true);});}
for(const d of S){cur=d;shapes=[];const s=pptx.addSlide();s.background={color:C.bg};headers(s,d);let items=d.items;
 switch(d.kind){
 case 'hook':
   // Fictional Pip rover; original geometry, not borrowed art.
   rect(s,.85,3.38,2.36,1.28,C.pink,C.pink);dot(s,1.37,4.81,.25,C.white);dot(s,2.69,4.81,.25,C.white);dot(s,2.92,3.69,.095,C.bg);
   line(s,3.6,4.06,7.65,4.06,C.white,true,3);rect(s,7.95,3.25,1.6,1.8,C.bg,C.pink);line(s,9.82,3.2,9.82,5.1,C.pink,false,4);
   text(s,'PIP',1.06,5.18,2.05,.55,32,{bold:true});text(s,'A BOX IN THE PATH',6.60,5.40,5.95,.6,30,{bold:true});
   text(s,'Detection is not the same as action.',.7,2.54,12,.58,32,{color:C.pink});break;
 case 'cards':case 'roadmap':case 'recap':case 'next_steps':case 'credits':
   items.forEach((t,i)=>{const gap=.17,h=(3.68-gap*(items.length-1))/items.length,y=2.55+i*(h+gap);rect(s,.7,y,.08,h,C.pink,C.pink);text(s,t,1.04,y+.025,11.24,h-.05,d.kind==='credits'?30:32,{bold:i===0&&d.kind==='recap'});});break;
 case 'question':
   items.forEach((t,i)=>{const y=2.66+i*1.07;text(s,t,.78,y,11.82,.99,i===items.length-1?36:32,{bold:i===items.length-1,color:i===items.length-1?C.pink:C.white});});break;
 case 'answer':
   items.forEach((t,i)=>card(s,t,.7,2.65+i*1.72,11.95,1.46,{size:30}));break;
 case 'equation':
   items.forEach((t,i)=>text(s,t,.78,2.53+i*1.22,11.82,1.16,i===items.length-1?34:30,{bold:i===items.length-1,color:i===items.length-1?C.pink:C.white}));break;
 case 'flow':flow(s,items);break;
 case 'comparison':
   items.forEach((r,i)=>{const h=items.length===3?1.03:1.5,y=2.62+i*(h+.20);rect(s,.7,y,11.95,h,C.bg,C.white);text(s,r[0],.93,y+.07,4.25,h-.14,28,{color:C.pink,bold:true});text(s,r[1],5.48,y+.07,6.92,h-.14,30);});break;
 case 'layers':
   items.forEach((t,i)=>{const h=items.length===4?.72:.92,y=2.65+i*(h+.21);card(s,t,.9+i*.23,y,11.2-i*.46,h,{size:30,bold:true,align:'center'});});break;
 case 'architecture':
   card(s,'MEMORY\ninstructions + data',4.37,2.48,4.6,1.2,{size:30,align:'center'});
   card(s,'INPUT',.7,4.10,2.5,1.25,{size:32,align:'center'});card(s,'CPU\nALU + control\nregisters',4.37,4.10,4.6,1.6,{size:28,align:'center'});card(s,'OUTPUT',10.15,4.10,2.5,1.25,{size:31,align:'center'});
   line(s,3.3,4.7,4.25,4.7,C.pink,true);line(s,9.1,4.7,10.03,4.7,C.pink,true);line(s,6.49,3.77,6.49,3.98,C.pink,true);line(s,6.86,3.98,6.86,3.77,C.pink,true);break;
 case 'program':table(s,items,['Address','Instruction']);break;
 case 'trace':case 'logic':case 'question_table':case 'packet':table(s,items,d.headers||null);if(d.kind==='question_table')text(s,'Start at sequence 41 · age limit 200 ms',.73,6.25,11.9,.45,28,{color:C.pink});break;
 case 'rl_loop':
   card(s,'AGENT\nchooses an action',.9,2.9,4.25,1.35,{size:31,align:'center'});card(s,'ENVIRONMENT\nreturns feedback',8.17,2.9,4.25,1.35,{size:29,align:'center'});
   line(s,5.35,3.48,7.98,3.48,C.pink,true);text(s,'ACTION',5.47,2.65,2.37,.52,28,{align:'center',color:C.pink,bold:true});
   line(s,10.3,4.49,10.3,5.50,C.white);line(s,10.3,5.50,3.1,5.50,C.white);line(s,3.1,5.50,3.1,4.49,C.white,true);
   text(s,'REWARD + NEXT OBSERVATION',3.78,5.70,7.46,.50,28,{align:'center'});break;
 case 'memory':
   items.forEach((t,i)=>{const w=4.35+i*1.92;card(s,t,(W-w)/2,2.52+i*.84,w,.68,{size:28,align:'center',bold:true});});
   text(s,'Closer: lower latency · farther: more capacity',.75,6.10,11.85,.51,28,{color:C.pink,align:'center'});break;
 case 'pipeline':{
   const rows=[['I1','F','D','E','W','—','—'],['I2','—','F','D','E','W','—'],['I3','—','—','F','D','E','W']];
   table(s,rows,['Cycle','1','2','3','4','5','6'],.7,2.63,11.95,2.76);
   text(s,'F Fetch · D Decode · E Execute · W Write',.74,5.56,11.85,.61,28,{color:C.pink});break;}
 case 'network_path':flow(s,items);text(s,'Local hop → network boundary → remote service',.7,5.50,11.9,.70,30,{color:C.pink,align:'center'});break;
 case 'queue':
   items.forEach((t,i)=>card(s,t,.85+i*2.80,3.26,2.43,1.43,{size:29,align:'center',bold:true}));
   line(s,9.25,3.02,9.25,4.9,C.pink,false,5);line(s,9.70,4,12.3,4,C.white,true,3);text(s,'ONE SHARED LINK',8.7,5.31,3.94,.95,28,{color:C.pink,align:'center'});break;
 case 'bars':
   items.forEach(([label,value],i)=>{const y=2.63+i*.82;text(s,label,.73,y,2.10,.59,30);rect(s,3.0,y+.04,8.0*(value/15),.48,C.pink,C.pink);text(s,`${value} m`,11.12,y,1.5,.58,28,{bold:true});});
   text(s,'At 30 m/s · distance during delay only',.73,6.09,11.9,.52,28,{color:C.pink});break;
 case 'integrated':
   card(s,'LOCAL\nSense · validate\nDecide · act',.7,2.61,5.56,2.58,{size:31,bold:true});
   card(s,'REMOTE\nTrain · coordinate\nReview',7.07,2.61,5.56,2.58,{size:31,bold:true});
   line(s,6.40,3.55,6.94,3.55,C.pink,true);line(s,6.94,4.12,6.40,4.12,C.pink,true);card(s,'UPDATE GATE · freshness + identity + version',.7,5.5,11.95,.79,{size:28,align:'center'});break;
 default:throw Error('Unknown slide type '+d.kind);
 }
 const notes=`BLUE IMPULSE — STAGE 2 PPT V1.0\nSlide ${d.number}: ${d.title}\nChapter ${d.chapter}: ${['','The Fundamentals','Behaviorism & Behaviorist AI','Hardware','Networking','Applications','Strengths & Limitations'][d.chapter]}\nSubtopic: ${d.subtopic}\nSuggested time: ${d.minutes} minute(s), subject to human rehearsal.\n\nTEACHING GUIDANCE\n${d.notes}\n${d.activity?'\nAUDIENCE TASK\n'+d.activity+'\n':''}${d.answer?'\nEXPECTED ANSWER / DEBRIEF\n'+d.answer+'\n':''}\nSOURCES\n${d.source}. Full details in supporting/Sources.md.\n\nRELATED RESOURCES\nLearning_Resource_Map.md gives matching chapter sections, practice and tutorial filenames.\n`;
 s.addNotes(notes);A.push({number:d.number,title:d.title,notes,shapes});
}
fs.writeFileSync(path.join(B,'review/layout-audit.json'),JSON.stringify(A,null,2));
pptx.writeFile({fileName:path.join(B,'BlueImpulse_Stage2_PPT_V1.pptx')}).then(()=>console.log(`Wrote ${S.length} editable slides`));
