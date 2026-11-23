/* 신경망이 보는 법 연구실 — 계산(code/analysis.py와 같은 식)과 실험 패널 */
(function(){'use strict';
var D=JSON.parse(document.getElementById('nsee-data').textContent);
var NS=window.NS={};
var FO=D.forder, PO=D.porder;
function grid(rows){var m={'#':1,'+':0.5,'.':0};return rows.map(function(r){return r.split('').map(function(c){return m[c]})})}
function conv(img,k){var n=img.length-2,o=[];for(var r=0;r<n;r++){var row=[];for(var c=0;c<n;c++){var s=0;for(var i=0;i<3;i++)for(var j=0;j<3;j++)s+=img[r+i][c+j]*k[i][j];row.push(s)}o.push(row)}return o}
function relu(m){return m.map(function(r){return r.map(function(v){return Math.max(0,v)})})}
function pool(m,how){var n=Math.floor(m.length/2),o=[];for(var r=0;r<n;r++){var row=[];for(var c=0;c<n;c++){var v=[m[2*r][2*c],m[2*r][2*c+1],m[2*r+1][2*c],m[2*r+1][2*c+1]];row.push(how==='avg'?(v[0]+v[1]+v[2]+v[3])/4:Math.max.apply(null,v))}o.push(row)}return o}
function features(img,doPool){var o={};FO.forEach(function(f){var e=relu(conv(img,D.filters[f].k));o[f]=doPool===false?e:pool(e)});return o}
function flat(F){var a=[];FO.forEach(function(f){F[f].forEach(function(r){r.forEach(function(v){a.push(v)})})});return a}
function cosine(a,b){var d=0,na=0,nb=0;for(var i=0;i<a.length;i++){d+=a[i]*b[i];na+=a[i]*a[i];nb+=b[i]*b[i]}return na&&nb?d/Math.sqrt(na*nb):0}
function shift(img,dx,dy){var n=img.length;return img.map(function(r,ri){return r.map(function(_,ci){var y=ri-dy,x=ci-dx;return (y>=0&&y<n&&x>=0&&x<n)?img[y][x]:0})})}
function win(F,r,c){var a=[];FO.forEach(function(f){for(var i=0;i<2;i++)for(var j=0;j<3;j++)a.push(F[f][r+i][c+j])});return a}
var IM={};Object.keys(D.images).forEach(function(k){IM[k]=grid(D.images[k].rows)});
var CATF=features(IM.cat);var TPL={};PO.forEach(function(p){TPL[p]=win(CATF,D.parts[p].r,D.parts[p].c)});
function detect(F,th){var res={},n=F.v.length;PO.forEach(function(p){var b=[-1,0,0];for(var r=0;r<n-1;r++)for(var c=0;c<n-2;c++){var s=cosine(win(F,r,c),TPL[p]);if(s>b[0]+1e-9)b=[s,r,c]}res[p]={score:b[0],r:b[1],c:b[2],found:b[0]>=th}});return res}
function judge(d){var found=PO.filter(function(p){return d[p].found}).length;
  var ok=PO.every(function(p){return d[p].found})&&Math.max(d.ear_l.r,d.ear_r.r)<Math.min(d.eye_l.r,d.eye_r.r)&&Math.min(d.eye_l.r,d.eye_r.r)<d.mouth.r&&d.eye_l.c<d.mouth.c&&d.mouth.c<d.eye_r.c;
  return {found:found,count_rule:found>=4,place_rule:!!ok}}
NS.api={grid:grid,conv:conv,relu:relu,pool:pool,features:features,flat:flat,cosine:cosine,shift:shift,detect:detect,judge:judge,IM:IM,D:D};

/* ── 그리기 도우미 ── */
var INK='#16212b',RULE='#d5dbe2',MUTED='#5b6874';
function f1(v){return (Math.round(v*10)/10).toFixed(1).replace('-0.0','0.0')}
function shade(v){var g=Math.round(255-v*225);return 'rgb('+g+','+g+','+(g+6>255?255:g+6)+')'}
function signed(v,mx){mx=mx||4;var t=Math.min(1,Math.abs(v)/mx);if(v>0)return 'rgba(19,115,58,'+(0.12+0.8*t)+')';if(v<0)return 'rgba(201,48,44,'+(0.12+0.8*t)+')';return '#ffffff'}
function pos(v,mx,col){mx=mx||4;var t=Math.min(1,v/mx);if(v<=0)return '#ffffff';return col.replace('A',(0.15+0.8*t).toFixed(2))}
function drawMat(g,x,y,cs,m,fill,opt){opt=opt||{};var n=m.length;for(var r=0;r<n;r++)for(var c=0;c<m[r].length;c++){g.fillStyle=fill(m[r][c],r,c);g.fillRect(x+c*cs,y+r*cs,cs,cs);
  if(opt.nums&&cs>=17){g.fillStyle=opt.numCol?opt.numCol(m[r][c]):(m[r][c]>0.6?'#fff':INK);g.font=Math.max(9,Math.floor(cs*0.42))+'px IBM Plex Sans KR, sans-serif';g.textAlign='center';g.textBaseline='middle';g.fillText(opt.fmt?opt.fmt(m[r][c]):f1(m[r][c]),x+c*cs+cs/2,y+r*cs+cs/2+1)}}
  g.strokeStyle='rgba(22,33,43,.12)';g.lineWidth=1;for(var i=0;i<=n;i++){g.beginPath();g.moveTo(x,y+i*cs+.5);g.lineTo(x+n*cs,y+i*cs+.5);g.stroke();g.beginPath();g.moveTo(x+i*cs+.5,y);g.lineTo(x+i*cs+.5,y+n*cs);g.stroke()}
  g.strokeStyle=RULE;g.strokeRect(x+.5,y+.5,n*cs,n*cs)}
function label(g,t,x,y,col,size,align){g.fillStyle=col||MUTED;g.font=(size||13)+'px IBM Plex Sans KR, sans-serif';g.textAlign=align||'left';g.textBaseline='alphabetic';g.fillText(t,x,y)}
function box(g,x,y,w,h,col,lw){g.strokeStyle=col;g.lineWidth=lw||3;g.strokeRect(x,y,w,h);g.lineWidth=1}
function setKpi(id,v){var e=document.getElementById(id);if(e)e.textContent=v}
function btnGroup(sel,cb){var bs=$$(sel);bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.setAttribute('aria-pressed','false');x.classList.remove('on')});b.setAttribute('aria-pressed','true');b.classList.add('on');cb(b.getAttribute('data-v'))})})}

/* ── 1단계: 픽셀 격자판 (X1) ── */
(function(){var cv=$('#cv1');if(!cv)return;var img=IM.cat.map(function(r){return r.slice()}),showNum=true,key='cat',L={};
  function draw(){var o=fit(cv),g=o.c,W=o.W;var cs=Math.max(12,Math.min(26,Math.floor((W-40)/2/16)));var two=W>=cs*32+60;
    if(!two)cs=Math.max(12,Math.min(24,Math.floor((W-20)/16)));
    var H=two?cs*16+50:cs*32+90;if(Math.abs(o.H-H)>1){cv.setAttribute('data-h',H);o=fit(cv,H);g=o.c}
    g.clearRect(0,0,W,o.H);var x0=10,y0=30;label(g,'사람이 보는 그림',x0,20,INK,14);
    drawMat(g,x0,y0,cs,img,function(v){return shade(v)});
    var x1=two?x0+cs*16+30:x0,y1=two?y0:y0+cs*16+40;label(g,'신경망이 받는 숫자 (진하기)',x1,y1-10,INK,14);
    drawMat(g,x1,y1,cs,img,function(v){return v>0?(v>=1?'#e6eefb':'#f3f6fd'):'#fff'},{nums:showNum&&cs>=17,fmt:function(v){return v===0?'0':(v===1?'1':'.5')},numCol:function(v){return v>0?'#1e55c8':'#b7c0ca'}});
    L={x0:x0,y0:y0,cs:cs};
    var dark=0,gray=0;img.forEach(function(r){r.forEach(function(v){if(v===1)dark++;else if(v===0.5)gray++})});
    setKpi('k1a','256개');setKpi('k1b',dark+'개');setKpi('k1c',gray+'개');setKpi('k1d',(256-dark-gray)+'개');
    var ins=$('#ins1');if(ins)ins.innerHTML='<p class="g">그림 '+D.images[key].name+': 숫자 256개 중 1(검정) '+dark+'개, 0.5(회색) '+gray+'개, 0(흰색) '+(256-dark-gray)+'개입니다. 신경망에게는 오른쪽 숫자판이 전부예요.</p>';}
  cv.addEventListener('click',function(e){var r=cv.getBoundingClientRect(),x=e.clientX-r.left-L.x0,y=e.clientY-r.top-L.y0;var c=Math.floor(x/L.cs),rr=Math.floor(y/L.cs);if(c<0||c>15||rr<0||rr>15)return;var v=img[rr][c];img[rr][c]=v===0?0.5:(v===0.5?1:0);draw()});
  btnGroup('#p1 .imgsel',function(v){key=v;img=IM[v].map(function(r){return r.slice()});draw()});
  $('#p1 .numtg').addEventListener('click',function(){showNum=!showNum;this.setAttribute('aria-pressed',showNum?'true':'false');this.textContent=showNum?'숫자 숨기기':'숫자 보기';draw()});
  Loop.add(cv,function(dt,force){if(dt===0)draw()});
})();

/* ── 2단계: 필터 훑기 (X2) ── */
(function(){var cv=$('#cv2');if(!cv)return;var f='v',key='cat',p=0,play=false,acc=0,speed=6,img=IM.cat,E=conv(img,D.filters.v.k);
  function upd(){E=conv(img,D.filters[f].k)}
  function draw(){var o=fit(cv),g=o.c,W=o.W;var narrow=W<700;var cs=narrow?Math.max(11,Math.floor((W-20)/16)):Math.min(22,Math.floor((W-260)/30));cs=Math.max(10,cs);
    var H=narrow?cs*16+cs*14+170:cs*16+60;if(Math.abs(o.H-H)>1){o=fit(cv,H);g=o.c}g.clearRect(0,0,W,o.H);
    var r=Math.floor(p/14),c=p%14,x0=10,y0=26;label(g,'그림 (16×16)',x0,18,INK,13);
    drawMat(g,x0,y0,cs,img,function(v){return shade(v)});box(g,x0+c*cs,y0+r*cs,cs*3,cs*3,'#1e55c8',3);
    var fx=narrow?x0:x0+cs*16+20,fy=narrow?y0+cs*16+16:y0;var k=D.filters[f].k,ks=26;
    label(g,'필터',fx,fy+10,INK,13);
    for(var i=0;i<3;i++)for(var j=0;j<3;j++){var v=k[i][j];g.fillStyle=v>0?'#e7f5ec':(v<0?'#fcebea':'#f6f8fa');g.fillRect(fx+j*ks,fy+16+i*ks,ks-2,ks-2);g.fillStyle=v>0?'#13733a':(v<0?'#c9302c':MUTED);g.font='13px IBM Plex Sans KR';g.textAlign='center';g.textBaseline='middle';g.fillText((v>0?'+':'')+v,fx+j*ks+ks/2-1,fy+16+i*ks+ks/2)}
    var s=E[r][c];label(g,'합 '+f1(s),fx,fy+16+3*ks+20,INK,15);label(g,'ReLU '+f1(Math.max(0,s)),fx,fy+16+3*ks+42,s>0?'#13733a':MUTED,15);
    var mx=narrow?x0:fx+110,my=narrow?fy+16+3*ks+60:y0;var ms=narrow?cs:Math.max(8,Math.min(cs,Math.floor((W-mx-10)/14)));
    label(g,'경계 지도 (14×14) · 자리 '+(p+1)+'/196',mx,my-8,INK,13);
    drawMat(g,mx,my,ms,E.map(function(row,ri){return row.map(function(v,ci){return (ri*14+ci)<=p?v:NaN})}),function(v){return isNaN(v)?'#fbfcfd':signed(v)});
    box(g,mx+c*ms,my+r*ms,ms,ms,'#1e55c8',2);
    // 곱셈 풀이
    var patch=[0,1,2].map(function(i){return img[r+i].slice(c,c+3)});var terms=[];for(var i2=0;i2<3;i2++)for(var j2=0;j2<3;j2++)if(k[i2][j2]!==0)terms.push('('+k[i2][j2]+'×'+(patch[i2][j2]===0.5?'0.5':patch[i2][j2])+')');
    var eq=$('#eq2');if(eq)eq.innerHTML='합 = '+terms.join(' + ')+' = <b>'+f1(s)+'</b> → ReLU: <b>'+f1(Math.max(0,s))+'</b>';
    setKpi('k2a',(p+1)+' / 196');setKpi('k2b',f1(s));setKpi('k2c',f1(Math.max(0,s)));
    var done=E.reduce(function(a,row,ri){return a+row.filter(function(v,ci){return ri*14+ci<=p&&v>0}).length},0);setKpi('k2d',done+'곳');
    var ins=$('#ins2');if(ins)ins.innerHTML=s>0.01?'<p class="g">점수 '+f1(s)+': 이 자리에 이 필터가 찾는 경계('+D.filters[f].name+')가 있어요. 초록으로 칠합니다.</p>':(s<-0.01?'<p class="r">점수 '+f1(s)+': 경계는 있는데 <b>방향이 반대</b>예요. 빨강으로 칠하고, ReLU를 거치면 0이 됩니다. 반대 방향은 다른 필터가 맡아요.</p>':'<p class="a">점수 0: 3×3 안의 왼쪽과 오른쪽(또는 위와 아래) 진하기가 같아요. 찾을 경계가 없습니다.</p>');
    var sl=$('#p2 .pos');if(sl&&+sl.value!==p+1)sl.value=p+1;$('#p2 .posv').textContent=(p+1);}
  Loop.add(cv,function(dt,force){if(play&&!window.REDUCED){acc+=dt*speed;if(acc>=1){p=(p+Math.floor(acc))%196;acc=acc%1;draw()}}else if(dt===0||force)draw()});
  $('#p2 .play').addEventListener('click',function(){play=!play;this.setAttribute('aria-pressed',play?'true':'false');this.textContent=play?'멈춤':'훑기 재생';if(window.REDUCED&&play){p=Math.min(195,p+14);play=false;this.textContent='훑기 재생';this.setAttribute('aria-pressed','false');draw()}});
  $('#p2 .prev').addEventListener('click',function(){p=(p+195)%196;draw()});$('#p2 .next').addEventListener('click',function(){p=(p+1)%196;draw()});
  $('#p2 .pos').addEventListener('input',function(){p=+this.value-1;draw()});
  $('#p2 .spd').addEventListener('input',function(){speed=+this.value;$('#p2 .spdv').textContent='초당 '+speed+'곳'});
  $('#p2 .jump').addEventListener('click',function(){p=195;draw()});
  btnGroup('#p2 .fsel',function(v){f=v;upd();draw()});btnGroup('#p2 .imgsel',function(v){key=v;img=IM[v];upd();draw()});
  NS.s2={set:function(ff,pp){f=ff;p=pp;upd();draw()}};
})();

/* ── 3단계: ReLU와 풀링 (X3) ── */
(function(){var cv=$('#cv3');if(!cv)return;var f='v',useRelu=true,how='max',sel=[2,1],key='cat',L={};
  function draw(){var o=fit(cv),g=o.c,W=o.W;var narrow=W<720;var cs=narrow?Math.max(10,Math.floor((W-24)/14)):Math.max(10,Math.min(24,Math.floor((W-60)/(14+14))));
    var E=conv(IM[key],D.filters[f].k),Rm=useRelu?relu(E):E,P=pool(Rm,how);var ps=cs*2;
    var H=narrow?cs*14+ps*7+90:cs*14+60;if(Math.abs(o.H-H)>1){o=fit(cv,H);g=o.c}g.clearRect(0,0,W,o.H);
    var x0=10,y0=28;label(g,(useRelu?'ReLU 뒤':'ReLU 전')+' 경계 지도 14×14',x0,18,INK,13);
    drawMat(g,x0,y0,cs,Rm,function(v){return signed(v)},{nums:cs>=22,fmt:function(v){return v===0?'':f1(v)},numCol:function(){return INK}});
    box(g,x0+sel[1]*2*cs,y0+sel[0]*2*cs,cs*2,cs*2,'#a35c00',3);
    var x1=narrow?x0:x0+cs*14+40,y1=narrow?y0+cs*14+40:y0;label(g,(how==='max'?'최댓값':'평균')+' 풀링 7×7',x1,y1-10,INK,13);
    drawMat(g,x1,y1,ps,P,function(v){return signed(v)},{nums:ps>=20,fmt:function(v){return v===0?'':f1(v)},numCol:function(){return INK}});
    box(g,x1+sel[1]*ps,y1+sel[0]*ps,ps,ps,'#a35c00',3);
    if(!narrow){g.strokeStyle='#a35c00';g.setLineDash([4,4]);g.beginPath();g.moveTo(x0+sel[1]*2*cs+cs*2,y0+sel[0]*2*cs+cs);g.lineTo(x1+sel[1]*ps,y1+sel[0]*ps+ps/2);g.stroke();g.setLineDash([])}
    L={x1:x1,y1:y1,ps:ps,x0:x0,y0:y0,cs:cs};
    var kept=Rm.reduce(function(a,r){return a+r.filter(function(v){return v>0}).length},0),neg=E.reduce(function(a,r){return a+r.filter(function(v){return v<0}).length},0);
    setKpi('k3a',useRelu?(neg+'개 → 0'):'0개 (끔)');setKpi('k3b',kept+'개');setKpi('k3c','196 → 49');
    var b=[Rm[2*sel[0]][2*sel[1]],Rm[2*sel[0]][2*sel[1]+1],Rm[2*sel[0]+1][2*sel[1]],Rm[2*sel[0]+1][2*sel[1]+1]];
    var eq=$('#eq3');if(eq)eq.innerHTML='고른 2×2: '+b.map(f1).join(', ')+' → '+(how==='max'?'가장 큰 값 <b>'+f1(Math.max.apply(null,b))+'</b>':'평균 <b>'+f1((b[0]+b[1]+b[2]+b[3])/4)+'</b>');
    var ins=$('#ins3');if(ins)ins.innerHTML=(!useRelu?'<p class="r">ReLU를 껐어요. 빨간 음수가 남아 있어 풀링 결과가 들쭉날쭉합니다. 최댓값 풀링은 음수를 무시하기 쉬워 정보가 섞여요.</p>':'')+
      (how==='max'?'<p class="g">최댓값 풀링: 2×2 안에서 가장 센 신호 하나만 남겨요. "이 근처 어딘가에 경계가 있다"는 사실은 남고, 정확한 자리는 흐려집니다.</p>':'<p class="a">평균 풀링: 2×2를 고르게 섞어요. 약한 신호가 강한 신호를 희석해 선이 옅어집니다.</p>');}
  cv.addEventListener('click',function(e){var r=cv.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;var c=Math.floor((x-L.x1)/L.ps),rr=Math.floor((y-L.y1)/L.ps);
    if(c>=0&&c<7&&rr>=0&&rr<7){sel=[rr,c];draw();return}c=Math.floor((x-L.x0)/(L.cs*2));rr=Math.floor((y-L.y0)/(L.cs*2));if(c>=0&&c<7&&rr>=0&&rr<7){sel=[rr,c];draw()}});
  $('#p3 .relutg').addEventListener('click',function(){useRelu=!useRelu;this.setAttribute('aria-pressed',useRelu?'true':'false');this.textContent=useRelu?'ReLU 켜짐':'ReLU 꺼짐';draw()});
  btnGroup('#p3 .how',function(v){how=v;draw()});btnGroup('#p3 .fsel',function(v){f=v;draw()});btnGroup('#p3 .imgsel',function(v){key=v;draw()});
  Loop.add(cv,function(dt,force){if(dt===0)draw()});
})();

/* ── 4단계 ①: 보는 범위가 넓어진다 ── */
(function(){var cv=$('#cv4a');if(!cv)return;var RF=[[1,1,'원본 픽셀 하나'],[3,1,'1층 필터 3×3'],[4,2,'1층 풀링 2×2'],[8,2,'2층 필터 3×3'],[10,4,'2층 풀링 2×2'],[18,4,'3층 필터 3×3']],L=1;
  function draw(){var o=fit(cv),g=o.c,W=o.W;var cs=Math.max(12,Math.min(24,Math.floor((Math.min(W,520)-30)/16)));var H=cs*16+50;if(Math.abs(o.H-H)>1){o=fit(cv,H);g=o.c}g.clearRect(0,0,W,o.H);
    var x0=10,y0=30;drawMat(g,x0,y0,cs,IM.cat,function(v){return shade(v)});var rf=RF[L][0];var cx=8,cy=8;
    var a=Math.max(0,cx-Math.floor(rf/2)),b=Math.min(16,a+rf);var a2=Math.max(0,cy-Math.floor(rf/2)),b2=Math.min(16,a2+rf);
    for(var i=1;i<=L;i++){var q=RF[i][0];var s0=Math.max(0,cx-Math.floor(q/2)),s1=Math.min(16,s0+q);g.fillStyle='rgba(155,63,181,'+(0.06+0.03*i)+')';g.fillRect(x0+s0*cs,y0+s0*cs,(s1-s0)*cs,(s1-s0)*cs)}
    box(g,x0+a*cs,y0+a2*cs,(b-a)*cs,(b2-a2)*cs,'#9b3fb5',3);
    label(g,RF[L][2]+' 뒤 · 한 점이 보는 범위 '+rf+'×'+rf+(rf>16?' (그림 16×16 전체를 넘음)':''),x0,20,INK,14);
    setKpi('k4a',rf+'×'+rf);setKpi('k4b',Math.min(100,Math.round(Math.min(rf,16)*Math.min(rf,16)/256*100))+'%');
    var ins=$('#ins4a');if(ins)ins.innerHTML=L<=1?'<p class="a">1층의 점 하나는 3×3, 픽셀 9개만 봐요. 이 정도로는 "선 한 토막"밖에 알 수 없습니다.</p>':(rf<16?'<p class="m">층을 쌓을수록 점 하나가 보는 범위가 넓어져요. 지금은 '+rf+'×'+rf+'. 눈 하나, 귀 하나 정도가 들어갑니다.</p>':'<p class="g">3층 필터의 점 하나는 '+rf+'×'+rf+' 범위를 봐요. 16×16 그림 전체가 들어가므로 "귀와 눈과 입이 어떻게 놓였나"를 한 번에 볼 수 있습니다.</p>');}
  $('#p4a .lv').addEventListener('input',function(){L=+this.value;$('#p4a .lvv').textContent=RF[L][2];draw()});
  Loop.add(cv,function(dt){if(dt===0)draw()});
})();

/* ── 4단계 ②: 부품 판정 ── */
(function(){var cv=$('#cv4b');if(!cv)return;var key='cat',th=D.thresh,COL={ear_l:'#c42a6e',ear_r:'#c42a6e',eye_l:'#1e55c8',eye_r:'#1e55c8',mouth:'#a35c00'};
  function draw(){var o=fit(cv),g=o.c,W=o.W;var cs=Math.max(12,Math.min(24,Math.floor((Math.min(W,520)-30)/16)));var H=cs*16+50;if(Math.abs(o.H-H)>1){o=fit(cv,H);g=o.c}g.clearRect(0,0,W,o.H);
    var x0=10,y0=30;label(g,D.images[key].name+' · 부품 탐지기가 찾은 곳',x0,20,INK,14);drawMat(g,x0,y0,cs,IM[key],function(v){return shade(v)});
    var d=detect(features(IM[key]),th),j=judge(d);
    PO.forEach(function(p){var q=d[p];if(!q.found)return;var x=x0+(q.c*2+1)*cs,y=y0+(q.r*2+1)*cs;g.strokeStyle=COL[p];g.lineWidth=3;g.setLineDash(p==='mouth'?[]:[6,3]);g.strokeRect(x+2,y+2,cs*6-4,cs*4-4);g.setLineDash([]);g.lineWidth=1;
      g.fillStyle=COL[p];g.font='bold 12px IBM Plex Sans KR';g.textAlign='left';g.fillText(D.parts[p].name,x+4,y+14)});
    var rows=PO.map(function(p){var q=d[p];return '<div class="vb"><span>'+D.parts[p].name+'</span><div class="tr"><div class="fl'+(q.found?'':' neg')+'" style="width:'+Math.max(0,q.score*100)+'%"></div></div><span class="v">'+Math.round(q.score*100)+'%</span></div>'}).join('');
    $('#bars4').innerHTML=rows;
    setKpi('k4c',j.found+' / 5');setKpi('k4d',j.count_rule?'고양이!':'아님');setKpi('k4e',j.place_rule?'고양이!':'아님');
    $('#k4d').parentNode.className='kpi '+(j.count_rule?'g':'r');$('#k4e').parentNode.className='kpi '+(j.place_rule?'g':'r');
    var ins=$('#ins4b'),t='';
    if(key==='scrambled'&&j.count_rule&&!j.place_rule)t='<p class="r">부품 다섯 개를 모두 찾았어요. <b>개수만 세는 판정기</b>는 "고양이"라고 속지만, <b>자리까지 보는 판정기</b>는 입이 귀 위에 있으니 고양이가 아니라고 합니다.</p>';
    else if(key==='house')t='<p class="a">지붕의 비스듬한 선이 귀와 닮아 "귀"를 찾았다고 나올 수 있어요. 그래도 눈과 입이 맞지 않아 고양이는 아닙니다.</p>';
    else if(key==='cat')t='<p class="g">귀 둘이 위, 눈 둘이 가운데, 입이 아래 가운데. 개수도 자리도 맞아 두 판정기 모두 고양이라고 합니다.</p>';
    else t='<p class="a">부품이 거의 안 보여요. 두 판정기 모두 고양이가 아니라고 합니다.</p>';
    if(Math.abs(th-D.thresh)>0.001)t+='<p class="m">문턱을 '+Math.round(th*100)+'%로 바꿨어요. 문턱이 낮으면 아무거나 부품으로 보고, 높으면 진짜 부품도 놓칩니다.</p>';
    ins.innerHTML=t;}
  btnGroup('#p4b .imgsel',function(v){key=v;draw()});
  $('#p4b .th').addEventListener('input',function(){th=+this.value/100;$('#p4b .thv').textContent=this.value+'%';draw()});
  Loop.add(cv,function(dt){if(dt===0)draw()});
})();

/* ── 대결 ── */
(function(){var el=$('#duelbox');if(!el)return;var sh='right1';
  btnGroup('#duel .shsel',function(v){sh=v});
  Duel({el:'#duelbox',scale:1,fmt:function(v){return Math.round(v*1000)/10+'%'},drawMargin:0.005,bigGap:0.15,
    run:function(){var m={right1:[1,0],down1:[0,1],right2:[2,0]}[sh];var s=shift(IM.cat,m[0],m[1]);
      return {fly:cosine(flat(features(IM.cat,true)),flat(features(s,true))),robo:cosine(flat(features(IM.cat,false)),flat(features(s,false)))}},
    report:function(r){var nm={right1:'오른쪽으로 1픽셀',down1:'아래로 1픽셀',right2:'오른쪽으로 2픽셀'}[sh];return '고양이를 '+nm+' 옮긴 뒤 원래 고양이와의 닮음(코사인)입니다. 풀링한 7×7 지도: <b>'+(Math.round(r.fly*1000)/10)+'%</b>, 풀링 안 한 14×14 지도: <b>'+(Math.round(r.robo*1000)/10)+'%</b>.'},
    verdict:{fly:'초파리 연구원 승. 최댓값 풀링은 "2×2 안 어딘가에 있으면 된다"고 보기 때문에 조금 옮겨도 같은 값이 남아요. 단, 풀링은 정확한 자리를 버립니다. 그래서 4단계에서 자리를 따로 확인해야 했죠.',
      robo:'주판봇 승. 이번 조건에서는 풀링 안 한 지도가 더 닮았어요.',draw:'비겼습니다.'}});
})();

/* ── 쪽지시험 ── */
(function(){var ex=$('#examform');if(!ex)return;
  function num(id){var v=($('#'+id).value||'').trim().replace(',','.');return v===''?NaN:+v}
  $('#examgo').addEventListener('click',function(){var sc=0,fb=[];
    var q1=$('input[name=eq1]:checked',ex);var ok1=q1&&q1.value==='b';sc+=ok1?1:0;fb.push([ok1,'1번',ok1?'맞아요. 픽셀마다 진하기 숫자 하나, 16×16이면 숫자 256개입니다.':'신경망은 그림을 "모양"으로 받지 않아요. 픽셀마다 숫자 하나, 숫자판 전체를 받습니다. (1단계)']);
    var a2=num('ex2');var ok2=Math.abs(a2-4)<0.01;sc+=ok2?1:0;fb.push([ok2,'2번',ok2?'맞아요. 오른쪽 열 (1×1)+(2×1)+(1×1)=4, 가운데 열은 필터가 0이라 빠지고, 왼쪽 열은 진하기 0이라 0입니다.':'초파리의 흔한 실수: 가운데 0.5를 더하는 것. 필터 가운데 열은 0이라 곱하면 0이에요. 오른쪽 열만 (1×1)+(2×1)+(1×1)=4. (2단계)']);
    var a3=[num('ex3a'),num('ex3b'),num('ex3c'),num('ex3d')],t3=[3,1,1,4];var ok3=a3.every(function(v,i){return Math.abs(v-t3[i])<0.01});sc+=ok3?1:0;
    fb.push([ok3,'3번',ok3?'맞아요. 2×2마다 가장 큰 값: 3, 1, 1, 4.':'2×2 네 묶음마다 가장 큰 값만 남겨요. 왼쪽 위 (0,2,3,1) → 3, 오른쪽 위 (1,0,0,0) → 1, 왼쪽 아래 (0,0,1,0) → 1, 오른쪽 아래 (4,2,0,0) → 4. 평균을 내면 틀려요. (3단계)']);
    var q4=$('input[name=eq4]:checked',ex);var ok4=q4&&q4.value==='c';sc+=ok4?1:0;fb.push([ok4,'4번',ok4?'맞아요. 부품의 개수만이 아니라 놓인 자리(귀는 위, 입은 아래)까지 봐야 해요.':'뒤섞인 고양이도 귀·눈·입은 다 있어요. 빠진 것은 "자리"입니다. (4단계)']);
    var q5=$('input[name=eq5]:checked',ex);var ok5=q5&&q5.value==='a';var bonus=ok5?1:0;fb.push([ok5,'보너스',ok5?'맞아요. 이 페이지는 설명하려고 필터를 사람이 정했지만, 실제 신경망은 정답을 맞히도록 학습하면서 필터 숫자를 스스로 정합니다.':'박사의 함정 문제였어요. 이 페이지의 필터는 설명용으로 사람이 정했어요. 실제 신경망은 학습(역전파)으로 필터 숫자를 스스로 정합니다.']);
    var out='<p class="score">본 문항 <b>'+sc+' / 4</b> · 보너스 '+bonus+' / 1</p><ul class="res">'+fb.map(function(x){return '<li class="'+(x[0]?'ok':'no')+'"><b>'+x[1]+'</b> '+x[2]+'</li>'}).join('')+'</ul>';
    $('#examres').innerHTML=out;
    var who=sc>=3?['doc','verdict','박사','합격입니다. '+(sc===4?'만점이에요. ':'')+'틀린 문항은 표시된 단계로 돌아가 한 번 더 보세요.']:['doc','think','박사','아직 70%가 안 됩니다. 괜찮아요. 처음엔 다들 여기서 오래 봅니다. 틀린 문항 옆에 적힌 단계로 돌아가 실험을 한 번 더 돌려 보세요.'];
    var face=sc>=3?'proud':'sigh';Cast.set($('#examsay img'),who[0],who[1]);$('#examsay .name').textContent=who[2];$('#examsay p').textContent=who[3];$('#examsay').hidden=false;
    Cast.set($('#examhelp img'),'asst',sc>=3?'proud':'firm');$('#examhelp p').textContent=sc>=3?'두 분 다 수고했어요. 시아 씨는 숫자를, 모아 씨는 이유를 말로 할 수 있게 됐어요.':'제가 같이 볼게요. 숫자 문제는 X2의 필터 카드를, 풀링 문제는 X3의 체를 다시 꺼내 볼까요?';$('#examhelp').hidden=false;
    ex.setAttribute('data-score',sc);
  });
  $('#examreset').addEventListener('click',function(){ex.reset();$('#examres').innerHTML='';$('#examsay').hidden=true;$('#examhelp').hidden=true});
})();
})();
