# -*- coding: utf-8 -*-
"""신경망이 보는 법 연구실 — 페이지 조립 도구 (공용 블록·표지·스프라이트·데이터)"""
import json, os, re, subprocess, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PACK = os.environ.get('LAB_PACK', '/home/claude/ref/ahnboat_lab_explainer/packs/character/character_pack')
R = json.load(open(os.path.join(ROOT, 'data', 'results.json'), encoding='utf-8'))
NSEE = json.load(open(os.path.join(ROOT, 'data', 'nsee.json'), encoding='utf-8'))
SITE = 'https://adminmrobo.github.io/neural_see_lab/'
REPO = 'https://github.com/adminmrobo/neural_see_lab'
SERIES = '신경망이 보는 법 연구실 (neural_see_lab)'
AUTHOR_LINE = '글 · 안상선 (<a href="https://www.ahnboat.xyz">www.ahnboat.xyz</a>) · (주)M-Robo 대표'
NAMES = {'doc': '박사', 'asst': '조수 하루', 'fly': '초파리 연구원', 'robo': '주판봇', 'sia': '인턴1 시아', 'moa': '인턴2 모아',
         'x1': '교보재 담당 X1', 'x2': '교보재 담당 X2', 'x3': '교보재 담당 X3'}
SHORT = {'doc': '박사', 'asst': '하루', 'fly': '초파리', 'robo': '주판봇', 'sia': '시아', 'moa': '모아', 'x1': 'X1', 'x2': 'X2', 'x3': 'X3'}
USED = set()  # 페이지에서 쓴 표정 키


def img(who, mood, cls=''):
    USED.add(who + '_' + mood)
    return '<img%s data-who="%s" data-mood="%s" alt="" aria-hidden="true">' % (' class="%s"' % cls if cls else '', who, mood)


def say(who, mood, text, name=None):
    return '<div class="say" data-who="%s">%s<div><b class="name">%s</b><p>%s</p></div></div>' % (who, img(who, mood), name or NAMES[who], text)


def chat(lines):
    return '<div class="chat">' + ''.join(say(*l) for l in lines) + '</div>'


def talk(lines, label='식구 대화'):
    out = '<div class="talk" aria-label="%s">' % label
    for who, mood, text in lines:
        out += '<div class="line" data-who="%s">%s<b>%s</b><p>%s</p></div>' % (who, img(who, mood), SHORT.get(who, NAMES[who]), text)
    return out + '</div>'


def crowd(text, moods=('e15', 'e02', 'e04'), label='방청석'):
    """X1~X3 방청석 반응 — 긴장한 하루를 걱정한다 (진행 보조, 엑스트라)"""
    ims = ''.join(img('x%d' % (i + 1), m) for i, m in enumerate(moods))
    return '<div class="crowd" aria-label="%s 반응"><div class="ims">%s</div><p><b>%s · X1 X2 X3</b> %s</p></div>' % (label, ims, label, text)


def wrapup(text):
    return say('doc', 'judge', '<b>박사의 정리</b> ' + text)


def step(sid, no, title, tags, inner, small='단계'):
    tg = ''.join('<span class="lvtag%s">%s</span>' % (' g' if i == 0 else '', t) for i, t in enumerate(tags))
    return ('<section class="level" id="%s"><div class="wrap"><div class="lvhead"><div class="hexno">%s<small>%s</small></div>'
            '<div><h2>%s</h2><div class="sub">%s</div></div></div>%s</div></section>') % (sid, no, small, title, tg, inner)


def section(sid, title, inner, cls='level'):
    return '<section class="%s" id="%s"><div class="wrap"><h2>%s</h2>%s</div></section>' % (cls, sid, title, inner)


def why(items, easy, title='왜 이 방법을 쓰나'):
    lis = ''.join('<li><b>%s</b> %s</li>' % (a, b) for a, b in items)
    return '<div class="why"><h4>%s</h4><ol>%s</ol><p class="easy"><b>쉽게 말하면</b> %s</p></div>' % (title, lis, easy)


def mathbox(ask, school, eq, rows, trial, comment, title='수학 수식을 어려워하는 조수가 대신 물어봅니다'):
    tb = ''
    if rows:
        tb = '<div class="tw"><table class="tb"><tr><th>식 조각</th><th>읽는 법</th><th>뜻</th></tr>' + ''.join(
            '<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>' % r for r in rows) + '</table></div>'
    return ('<div class="mathbox"><h4>%s</h4><div class="ask">%s<p><b>하루</b> %s</p></div>'
            '<p class="school">학교 수학으로 보면: %s</p><div class="eqbig">%s</div>%s'
            '<div class="try"><b>숫자로 한 번 해 보기</b> %s</div>'
            '<div class="ask" style="margin-top:10px">%s<p><b>하루</b> %s</p></div></div>') % (
        title, img('asst', 'shock'), ask, school, eq, tb, trial, img('asst', 'spark'), comment)


def duo(a, b):
    return '<div class="duo">%s%s</div>' % (a, b)


def pair(lt, ltext, rt, rtext):
    return ('<div class="pair"><div><span class="tag fly">%s</span><p>%s</p></div>'
            '<div><span class="tag nn">%s</span><p>%s</p></div></div>') % (lt, ltext, rt, rtext)


def kit(x, mood, title, text):
    """X1~X3가 들고 오는 교보재 상자 (진행 보조)"""
    return ('<div class="kit" data-who="%s">%s<div><span class="lab">%s · 교보재</span><b>%s</b><p>%s</p></div></div>') % (
        x, img(x, mood), x.upper(), title, text)


def mock(who, mood, q, ans, fix_mood, fix):
    """모의 문제: 인턴이 답하고 하루가 처방한다"""
    return ('<div class="mock"><span class="lab">모의 문제</span><p class="mq">%s</p>%s%s</div>') % (
        q, say(who, mood, ans), say('asst', fix_mood, fix, name='조수 하루의 처방'))


def panel(pid, title, stamp, inner, real=False):
    return '<div class="panel" id="%s"><h3>%s <span class="stamp%s">%s</span></h3>%s</div>' % (pid, title, ' real' if real else '', stamp, inner)


def canvas(cid, h, label, wide=False):
    return '<div class="cwrap"><canvas id="%s" data-h="%d"%s aria-label="%s" role="img"></canvas></div>' % (cid, h, ' class="wide"' if wide else '', label)


def explain(items, lim, title='풀이'):
    lis = ''.join('<li>%s</li>' % x for x in items)
    return '<div class="explain"><h4>%s</h4><ol>%s</ol><p class="lim"><b>이 단계의 한계</b> %s</p></div>' % (title, lis, lim)


def codefold(rows, title='실제 도구의 코드로 보면 (몰라도 됩니다)'):
    body = ''.join('<div class="codeline"><div class="code">%s</div><p>%s</p></div>' % (H.escape(c), m) for c, m in rows)
    return '<details class="codefold"><summary>%s</summary>%s</details>' % (title, body)


def quiz(qid):
    return '<div class="quiz" data-quiz="%s"></div>' % qid


def aicheck(title, inner):
    return '<div class="ai-check"><h4>AI 판단 코너 · %s</h4>%s</div>' % (title, inner)


def recap(title, inner):
    return '<div class="recap"><h4>30초 복습 · %s</h4>%s</div>' % (title, inner)


def bridge(kind, title, text, lim):
    return '<div class="bridge %s"><h4>%s</h4><p>%s</p><p class="lim">비유의 한계: %s</p></div>' % (kind, title, text, lim)


def note(text, warn=False):
    return '<p class="note%s">%s</p>' % (' warn' if warn else '', text)


def kpis(items):
    return '<section class="kpis" aria-label="숫자 요약">' + ''.join('<div class="kpi %s"><b>%s</b><span>%s</span></div>' % (c, v, l) for v, l, c in items) + '</section>'


def three(items, note_text='', abbr=None, title='처음 오신 분께 — 이 장을 3줄로'):
    lis = ''.join('<li><b>%s</b> %s</li>' % (a, b) for a, b in items)
    ab = ''
    if abbr:
        ab = '<details><summary>이 장에 나오는 영어 약어 풀이</summary><dl class="abbr">' + ''.join('<dt>%s</dt><dd>%s</dd>' % x for x in abbr) + '</dl></details>'
    return ('<section class="level" id="first" style="padding-top:28px"><div class="wrap"><div class="three"><h2>%s</h2><ol>%s</ol>'
            '<p class="note">%s</p>%s</div></div></section>') % (title, lis, note_text, ab)


def cast_cards(items, hidden=True):
    out = '<div class="cast">' + ''.join(
        '<div class="c" data-who="%s">%s<div><b style="color:var(--who)">%s</b><span>%s</span></div></div>' % (w, img(w, m), NAMES[w], t)
        for w, m, t in items) + '</div>'
    if hidden:
        out += ('<p><button class="bt" data-toggle-hidden="#hc" aria-pressed="false">미공개 식구 보기 (No.007~009)</button></p>'
                '<div class="hiddencast" id="hc"><div class="cast">' + ''.join(
                    '<div class="c" data-who="x%d">%s<div><b style="color:var(--who)">%s</b><span>%s</span></div></div>' % (
                        i, img('x%d' % i, 'e13'), NAMES['x%d' % i], t) for i, t in ((1, '픽셀 격자판을 들고 옵니다 (1단계). 시험 날에는 답안지를 나눠 줍니다.'), (2, '필터 카드 네 장을 들고 옵니다 (2단계). 시험 시간을 잽니다.'), (3, '풀링 체와 부품 스티커를 들고 옵니다 (3·4단계). 채점표를 모읍니다.'))) + '</div></div>')
    return out


def duel(did, question, fly_pick, robo_pick, fly_line, robo_line, metric):
    return ('<section class="level" id="duel"><div class="wrap"><div class="lvhead"><div class="hexno">VS<small>대결</small></div><div><h2>대결 · %s</h2>'
            '<div class="sub"><span class="lvtag g">판정 기준: %s</span><span class="lvtag">숫자는 이 페이지가 직접 계산</span></div></div></div>'
            '<div class="duel" id="%s"><div class="vs"><div class="side fly" data-who="fly">%s<div><b style="color:var(--c-fly)">초파리 연구원</b><p>%s</p><p class="small muted">고른 쪽: %s</p></div></div>'
            '<div class="mid">VS</div><div class="side robo" data-who="robo">%s<div><b style="color:var(--c-robo)">주판봇</b><p>%s</p><p class="small muted">고른 쪽: %s</p></div></div></div>'
            '<div class="ctrl"><div class="group"><span class="glabel">먼저 맞혀 보기</span><button class="bt guess" data-side="fly" aria-pressed="false">초파리가 이길 것 같다</button>'
            '<button class="bt guess" data-side="robo" aria-pressed="false">주판봇이 이길 것 같다</button></div>'
            '<div class="group"><button class="bt primary run">결과 보기</button><button class="bt reset">다시 닫기</button></div></div>'
            '<div class="bars"><div class="bar f"><span>초파리 쪽</span><div class="track"><div class="fill"></div></div><span class="v">?</span></div>'
            '<div class="bar r"><span>주판봇 쪽</span><div class="track"><div class="fill"></div></div><span class="v">?</span></div></div>'
            '<div class="verdict" aria-live="polite"><p class="gtext small muted"></p>'
            '<div class="say" data-who="asst">%s<div><b class="name">조수 하루</b><p class="vreport"></p></div></div>'
            '<div class="say" data-who="doc">%s<div><b class="name">박사</b><p class="vtext"></p></div></div></div></div></div></section>') % (
        question, metric, did, img('fly', 'point'), fly_line, fly_pick, img('robo', 'coin'), robo_line, robo_pick,
        img('asst', 'report'), img('doc', 'judge'))


def outro(lines, scene_alt, extra=''):
    """lines: [(who,mood,text)] 박사 먼저, 조수 마지막"""
    return ('<section class="level" id="outro"><div class="wrap"><h2>아웃트로</h2>'
            '<div class="scene" data-img="sc_outro" role="img" aria-label="%s">%s</div>%s%s</div></section>') % (
        scene_alt, ''.join(img(w, m) for w, m, _ in lines), chat([(w, m, t) for w, m, t in lines]), extra)


def footer(sources, examples, prev=None, nxt=None, depth=0):
    up = '../' * depth
    rows = ''.join('<tr><td>%s</td><td>%s</td></tr>' % s for s in sources)
    pg = '<div class="pager">'
    if prev:
        pg += '<a class="prev" href="%s%s"><small>← 앞 장</small>%s</a>' % (up, prev[0], prev[1])
    if nxt:
        pg += '<a class="next" href="%s%s"><small>다음 장 →</small>%s</a>' % (up, nxt[0], nxt[1])
    pg += '</div>'
    ex = ''.join('<li>%s</li>' % e for e in examples)
    return ('<footer><div class="wrap">%s<h4>출처</h4><div class="tw"><table class="tb"><tr><th>무엇</th><th>출처</th></tr>%s</table></div>'
            '<h4>예시값·설명용 모형인 것</h4><ul>%s</ul>'
            '<p>%s</p><p class="small">캐릭터(박사·조수 하루·초파리 연구원·주판봇·인턴 시아·인턴 모아·X1~X3)의 이름·설정·그림 저작권은 안상선에게 있으며 허락 없이 쓸 수 없습니다. '
            '영화·리뷰·SNS 글·랩플릭스 안내 문서는 이 연구실이 만든 가상 데이터이며 실제 작품·서비스와 관계없습니다.</p></div></footer>') % (pg, rows, ex, AUTHOR_LINE)


# ── 표지 (그림이 오기 전 대체 표지, 18-14-5) ──
def cover(key, kicker, title, chars=(('doc', 'front'), ('asst', 'e15'), ('fly', 'point'), ('robo', 'coin')), band=False, depth=0):
    import random
    rnd = random.Random(sum(map(ord, key)))
    up = '../' * depth
    cat = NSEE['images']['cat']['rows']
    px = ''.join('<rect x="%d" y="%d" width="26" height="26" fill="%s"/>' % (980 + c * 28, 150 + r * 28, '#16212b' if ch == '#' else '#8a94a0')
                 for r, row in enumerate(cat) for c, ch in enumerate(row) if ch != '.')
    frame = '<rect x="972" y="142" width="456" height="456" fill="none" stroke="#9aa6b2" stroke-width="6"/>'
    lens = '<rect x="1036" y="178" width="92" height="92" fill="rgba(30,85,200,.18)" stroke="#1e55c8" stroke-width="8"/>'
    edges = ''.join('<rect x="%d" y="%d" width="18" height="18" fill="%s" opacity=".85"/>' % (150 + (i % 9) * 22, 170 + (i // 9) * 22, ['#13733a', '#a35c00', '#9b3fb5'][(i * 7 + rnd.randint(0, 2)) % 3])
                    for i in range(63) if rnd.random() < .55)
    tiles = ''.join('<rect x="%d" y="760" width="40" height="40" fill="%s"/>' % (x, '#eef2f8' if (x // 40) % 2 == 0 else '#e6edf5') for x in range(0, 1600, 40))
    svg = ('<svg viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true" shape-rendering="crispEdges" style="width:100%%;height:100%%;display:block">'
           '<defs><linearGradient id="g%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7f9fc"/><stop offset="1" stop-color="#e8eef6"/></linearGradient></defs>'
           '<rect width="1600" height="900" fill="url(#g%s)"/>%s%s%s%s<rect x="0" y="800" width="1600" height="100" fill="#e9eef5"/>%s</svg>') % (key, key, edges, frame, px, lens, tiles)
    row = '<div class="pxrow" aria-hidden="true">' + ''.join(img(w, m) for w, m in chars) + '</div>'
    src = up + 'img/' + key + '.webp' if os.path.exists(os.path.join(ROOT, 'img', key + '.webp')) else ''  # 그림이 있을 때만 불러온다 (없으면 404를 내지 않음)
    return ('<!-- lab-cover --><div class="cover%s" data-img="%s" role="img" aria-label="%s 표지"><div class="fallback">%s%s</div>'
            '<img class="cimg" data-cover="%s" data-src="%s" alt="%s" hidden>'
            '<div class="ctitle"><b>%s</b><span>%s</span></div></div><!-- /lab-cover -->') % (
        ' band' if band else '', key, H.escape(title), svg, row, key, src, H.escape(title) + ' 표지 그림', kicker, title)


# ── 데이터·스프라이트 ──
def nsee_data():
    return '<script type="application/json" id="nsee-data">%s</script>' % json.dumps(NSEE, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def sprites(keys, size=96):
    em = json.load(open(os.path.join(PACK, 'expression_map.json'), encoding='utf-8'))
    pick = []
    for k in sorted(keys):
        if k in em or re.match(r'^[a-z0-9]+_e\d\d$', k):
            pick.append(k)
    for base in ['doc_front', 'asst_smile', 'fly_clip', 'robo_smile', 'moa_smile', 'sia_smile', 'x1_hint', 'x2_hint', 'x3_hint']:
        if base.split('_')[0] in {k.split('_')[0] for k in keys} and base not in pick:
            pick.append(base)
    out = subprocess.check_output(['python3', os.path.join(PACK, 'build_character_pack.py'), '--pack', PACK, '--pick', ','.join(pick), '--size', str(size)]).decode()
    return out


def read(name):
    return open(os.path.join(HERE, name), encoding='utf-8').read()


EXTRA_CSS = '''
/* 신경망이 보는 법 연구실 추가분 */
.cover img.cimg[hidden]{display:none}
.cover .fallback .pxrow{max-width:100%;overflow:hidden}
@media (max-width:560px){.cover.band .fallback .pxrow img{width:56px!important;height:56px!important}}
.ctrl .group{max-width:100%;min-width:0;flex-wrap:wrap}.sel{max-width:100%}
.supbox{display:flex;gap:12px;align-items:flex-start;border:1px solid #e3cf9a;background:#fffaf0;border-left:4px solid var(--c-moa);border-radius:14px;padding:12px 14px;margin:18px 0}
.supbox>img{width:56px;height:56px;object-fit:contain;flex:none;image-rendering:pixelated}
.supbox .lab{font-size:13px;font-weight:700;color:var(--c-moa)}
.supbox .sgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:6px}
.supbox .sgrid>div{background:#fff;border:1px solid var(--rule);border-radius:10px;padding:9px 12px}
.supbox .sgrid b{font-size:13.5px}.supbox .s1 b{color:var(--muted)}.supbox .s2 b{color:var(--info)}
.supbox .sgrid p{margin:.2em 0 0;font-size:15px}
@media (max-width:760px){.supbox .sgrid{grid-template-columns:1fr}}
.crowd{display:flex;gap:10px;align-items:center;border:1px dashed var(--rule);background:#fbfcfd;border-radius:12px;padding:6px 12px;margin:10px 0}
.crowd .ims{display:flex;flex:none}.crowd .ims img{width:40px;height:40px;object-fit:contain;image-rendering:pixelated;margin-right:-6px}
.crowd p{margin:0;font-size:14.5px;color:#3a3f5c}.crowd b{color:var(--c-x);font-size:13px;margin-right:4px}
.scene{display:flex;gap:14px;justify-content:center;align-items:flex-end;flex-wrap:wrap;background:linear-gradient(#f7f9fc,#eaf0f7);border:1px solid var(--rule);border-radius:16px;padding:16px;margin:10px 0 6px}
.scene img{width:96px;height:96px;object-fit:contain;image-rendering:pixelated}
.scene.scimg{padding:0;overflow:hidden;display:block}
.scene.scimg img{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;display:block}
@media (max-width:520px){.scene img{width:56px;height:56px}}
.codefold .codeline p{margin:0;font-size:14.5px}
.mini-table td,.mini-table th{padding:4px 8px}
.mapbar{display:flex;gap:4px;align-items:center;flex-wrap:wrap;margin:8px 0}
.mapbar span{background:#fff;border:1px solid var(--rule);border-radius:10px;padding:5px 10px;font-size:14px}
.mapbar span.on{border-color:var(--info);background:var(--info-soft);color:var(--info);font-weight:700}
.mapbar i{font-style:normal;color:var(--muted)}
.vbars{display:grid;gap:6px;margin:8px 0}
.vbars .vb{display:grid;grid-template-columns:96px 1fr 52px;gap:8px;align-items:center;font-size:14px}
.vbars .tr{height:14px;background:var(--panel2);border-radius:7px;overflow:hidden}
.vbars .fl{height:100%;border-radius:7px;background:var(--info);transition:width .4s}
.vbars .fl.neg{background:var(--eye)}
.vbars .v{text-align:right;font-variant-numeric:tabular-nums}
.mission{border:1px solid var(--rule);border-radius:12px;background:#fff;padding:8px 12px;margin:6px 0;display:flex;gap:10px;align-items:flex-start}
.mission .st{flex:none;font-weight:700;font-size:13px;border-radius:99px;padding:1px 10px;background:var(--panel2);color:var(--muted)}
.mission.ok .st{background:var(--gfp-soft);color:var(--gfp)}
.mission p{margin:0}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0}
.ctl-env{border-left:4px solid var(--gfp);padding-left:10px}
.ctl-me{border-left:4px solid var(--info);padding-left:10px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media (max-width:860px){.grid2{grid-template-columns:1fr}}

@media (min-width:761px){.cover .fallback .pxrow{width:50%}.cover .fallback .pxrow img{width:15.5%}}
.say[hidden]{display:none!important}
.kit{display:flex;gap:12px;align-items:flex-start;border:1px solid var(--rule);background:#fbfcfd;border-left:4px solid var(--c-x);border-radius:14px;padding:10px 14px;margin:14px 0}
.kit>img{width:56px;height:56px;object-fit:contain;flex:none;image-rendering:pixelated}
.kit .lab{display:block;font-size:12.5px;font-weight:700;color:var(--c-x)}
.kit b{font-size:15.5px}.kit p{margin:.2em 0 0;font-size:15px}
.mock{border:1px solid #e3cf9a;background:#fffaf0;border-radius:14px;padding:12px 14px;margin:18px 0}
.mock .lab{font-size:12.5px;font-weight:700;color:var(--amber)}
.mock .mq{font-weight:700;margin:.2em 0 .4em}
.guide{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0}
@media (max-width:860px){.guide{grid-template-columns:1fr}}
.guide>div{border:1px solid var(--rule);border-top:4px solid var(--who);border-radius:14px;background:#fff;padding:12px 14px}
.guide .gh{display:flex;gap:10px;align-items:center}.guide .gh img{width:52px;height:52px;object-fit:contain;image-rendering:pixelated}
.guide .gh b{color:var(--who)}.guide p{margin:.4em 0;font-size:15px}.guide .ex{background:var(--panel);border-radius:10px;padding:8px 10px;font-size:14.5px}
.interns{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0}
@media (max-width:760px){.interns{grid-template-columns:1fr}}
.interns>div{display:flex;gap:10px;align-items:flex-start;border:1px solid var(--rule);border-left:4px solid var(--who);border-radius:14px;padding:10px 12px;background:#fff}
.interns img{width:64px;height:64px;object-fit:contain;image-rendering:pixelated;flex:none}.interns b{color:var(--who)}.interns p{margin:.2em 0;font-size:15px}
.exam{border:2px solid var(--info);border-radius:18px;padding:18px 20px;background:#fff}
.exam fieldset{border:1px solid var(--rule);border-radius:12px;padding:10px 14px;margin:12px 0}
.exam legend{font-weight:700;padding:0 6px}
.exam label{display:block;margin:4px 0;cursor:pointer}
.exam input[type=text]{width:84px;font:inherit;padding:4px 8px;border:1px solid var(--rule);border-radius:8px}
.exam .mini{display:inline-grid;grid-template-columns:repeat(4,30px);gap:2px;margin:6px 0;font-variant-numeric:tabular-nums}
.exam .mini span{background:var(--panel2);text-align:center;border-radius:4px;font-size:14px}
.exam .mini.f span.p{background:var(--gfp-soft);color:var(--gfp)}.exam .mini.f span.n{background:var(--eye-soft);color:var(--eye)}
.exam .mini3{grid-template-columns:repeat(3,34px)}
.exam .score{font-size:20px}.exam .pair2{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-start}
.mapflow{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:10px 0}
.mapflow span{border:1px solid var(--rule);border-radius:10px;padding:6px 10px;background:#fff;font-size:14.5px}
.mapflow span.on{border-color:var(--info);background:var(--info-soft);color:var(--info);font-weight:700}
.mapflow i{font-style:normal;color:var(--muted)}
.vb span:first-child{font-size:14px}
mark{background:#fff1a8;border-radius:3px;padding:0 1px}
mark.flip{background:#fcd9d6;text-decoration:underline wavy #c9302c}
.res{list-style:none;padding:0;margin:8px 0;display:grid;gap:6px}
.res li{border:1px solid var(--rule);border-radius:10px;padding:7px 11px;background:#fff;font-size:15px;line-height:1.6}
.res li.ok{border-left:4px solid var(--gfp)}.res li.no{border-left:4px solid var(--eye)}.res li.nt{border-left:4px solid var(--rule)}
.res li small{color:var(--muted);display:block;font-size:12.5px}
.res li .sc{float:right;font-variant-numeric:tabular-nums;color:var(--info);font-weight:700;margin-left:8px}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
@media (max-width:860px){.cols3{grid-template-columns:1fr}}
.cols3>div{background:var(--panel);border:1px solid var(--rule);border-radius:12px;padding:10px 12px}
.cols3 h4{font-size:15px;margin:0 0 4px}
.sqlbox{font-family:ui-monospace,Menlo,Consolas,monospace;background:#0f1720;color:#e6edf3;border-radius:10px;padding:10px 14px;font-size:14px;line-height:1.6;white-space:pre-wrap;word-break:break-all;margin:8px 0}
.sqlbox .k{color:#7cc4ff}.sqlbox .s{color:#ffd479}
.prompt{font-family:ui-monospace,Menlo,Consolas,monospace;background:#f6f8fa;border:1px solid var(--rule);border-radius:10px;padding:10px 14px;font-size:13.5px;line-height:1.6;white-space:pre-wrap;word-break:break-all;margin:8px 0;max-height:260px;overflow:auto}
.flowsteps{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0}
.flowsteps span{border:1px solid var(--rule);border-radius:10px;padding:5px 10px;font-size:14px;background:#fff}
.flowsteps span.on{background:var(--info-soft);border-color:var(--info);color:var(--info);font-weight:700}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}
.chips .bt{font-size:14px;padding:5px 10px}
input[type=text].wide{width:100%;max-width:520px}
.ansbox{border:2px solid var(--info);border-radius:12px;padding:10px 14px;background:var(--info-soft);margin:8px 0}
.ansbox.none{border-color:var(--amber);background:var(--amber-soft)}
.ansbox.bad{border-color:var(--eye);background:var(--eye-soft)}
'''


def build(path, *, title, desc, nav, cover_html, hero, body, gloss, quizzes, page_js, data_js=True, depth=0, og=None):
    """한 페이지 HTML을 조립해 path에 쓴다 (지식 색인·꾸러미는 다음 단계 kg_build.py가 붙인다)"""
    css = read('base.css') + EXTRA_CSS
    navh = '<nav class="top" aria-label="이 페이지 목차"><a class="logo" href="%sindex.html">신경망이 보는 법 연구실</a>%s</nav>' % (
        '../' * depth, ''.join('<a href="%s">%s</a>' % (h, t) for h, t in nav))
    og = og or 'og_00'
    url = SITE + path
    head = ('<!DOCTYPE html><html lang="ko"><head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n'
            '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n'
            '<meta property="og:url" content="%s">\n<meta property="og:type" content="website">\n'
            '<meta property="og:image" content="%simg/%s.webp">\n<meta name="author" content="안상선">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">\n'
            '<style>%s</style>\n</head><body>\n<div id="prog" aria-hidden="true"></div>\n') % (
        H.escape(title), H.escape(desc), H.escape(title), H.escape(desc), url, SITE, og, css)
    scripts = ''
    if data_js:
        scripts += nsee_data() + '\n'
    scripts += '<script>\n' + sprites(USED) + '\n</script>\n'
    scripts += '<script>\n' + read('common.js') + '\n' + read('study.js') + '\n' + read('nsee.js') + '\n</script>\n'
    scripts += ('<script>\n(function(){"use strict";\nGloss(%s);\nQuiz(%s);\n%s\nCast.fill();LoopStart();\n})();\n</script>\n') % (
        json.dumps(gloss, ensure_ascii=False), json.dumps(quizzes, ensure_ascii=False), page_js)
    doc = head + navh + cover_html + hero + '<main id="top">' + body + '</main>\n' + scripts + '</body></html>\n'
    doc = doc.replace('data-img="sc_outro"', 'data-img="sc_%s_outro"' % og[3:])
    # 아웃트로 장면 그림(img/sc_XX_outro.webp)이 있으면 표정 그림 줄 대신 그 그림을 건다
    sc_key = 'sc_%s_outro' % og[3:]
    if os.path.exists(os.path.join(ROOT, 'img', sc_key + '.webp')):
        doc = re.sub(r'(<div class="scene" data-img="%s" role="img" aria-label="([^"]*)">).*?(</div>)' % sc_key,
                     lambda m: '<div class="scene scimg" data-img="%s" role="img" aria-label="%s"><img src="%simg/%s.webp" alt="" loading="lazy" decoding="async"></div>' % (
                         sc_key, m.group(2), '../' * depth, sc_key), doc, count=1, flags=re.S)
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(doc)
    USED.clear()
    return out


def hero(kicker, h1, q, lead, kp, chat_lines, crowd_html=''):
    return ('<header class="hero"><div class="wrap"><p class="kicker">%s</p><h1>%s</h1><p class="q">핵심 질문: %s</p><p class="lead">%s</p>%s%s%s</div></header>') % (
        kicker, h1, q, lead, kpis(kp), chat(chat_lines), crowd_html)


def pct(v, d=1):
    return ('%.' + str(d) + 'f%%') % (v * 100)


def num(v, d=0):
    return ('{:,.%df}' % d).format(v)
