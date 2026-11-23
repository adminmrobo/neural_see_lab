# -*- coding: utf-8 -*-
"""표지 지시문(16비트 RPG 픽셀아트), 이미지 제작 명세서, cover_manifest.json 만들기 — neural_see_lab"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)

CH = {
    'doc': 'chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie',
    'asst': 'girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans',
    'fly': 'anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings',
    'robo': 'boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus',
    'sia': 'young intern girl in a classic black-and-white maid-style uniform, straight black hair',
    'moa': 'young intern girl in a classic black-and-white maid-style uniform, wavy beige hair',
}
COVERS = [
    ('cover_00', 'index.html', '신경망은 고양이를 어떻게 "볼까" — 쪽지시험 대비반', '낮의 연구실 강의실, 큰 창과 흰 칠판, 책상 위 교보재 상자 세 개', 'ko',
     ['doc', 'asst', 'sia', 'moa', 'fly', 'robo'],
     '칠판에 붙인 16×16 픽셀 고양이 얼굴(글자 없음) 위에 파란 3×3 돋보기 창이 걸려 있고, 그 옆으로 초록·노랑 작은 사각형이 줄지어 선(경계)을 이룸. 인턴 둘이 앞줄에서 쪽지시험 대비 노트를 펼치고 하루가 칠판을 가리킴. 박사·초파리·주판봇은 뒤쪽 출제위원 책상에 앉아 있음',
     'a big pixelated 16x16 cat face made of black and gray squares pinned on a white board, with a blue square magnifying frame covering a 3x3 patch of it; next to it, rows of small green and amber squares forming edge lines; two interns at the front desk open their study notebooks for a pop quiz, the girl researcher points at the board; behind them, the doctor, the fruit fly and the robot sit at a judges\' desk with blank answer sheets',
     '쪽지시험 전날, 하루가 픽셀 고양이 그림 앞에서 인턴 둘을 가르치고 출제위원 셋이 뒤에서 지켜보는 강의실'),
]
POSE = {'doc': 'center back, calm guiding gesture', 'asst': 'front center', 'fly': 'on the left facing right, pointing with curiosity',
        'robo': 'on the right facing left, holding a wooden abacus', 'sia': 'seated on the left', 'moa': 'seated next to her on the right'}


def prompt(c):
    key, page, title, place, _, chars, meta_ko, meta_en, alt = c
    who = ';\n  '.join('%s, %s' % (CH[w], POSE[w]) for w in chars)
    return ('웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.\n- 비율 16:9, 가로 1920px 이상\n- 그림체는 반드시 16비트 RPG풍 픽셀아트 (네모 픽셀이 보이게, 매끈한 일러스트·벡터·수채화·3D 금지)\n'
            '- 첨부한 참고 이미지의 캐릭터를 같은 외형으로, 모두 픽셀아트로 등장\n- 그림 안에 글자·숫자·로고를 넣지 말 것\n- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게\n아래 영어 프롬프트를 그대로 써 줘.\n\n'
            'Website top cover illustration, wide 16:9.\nArt style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2-3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.\n'
            'Match the characters\' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style. Height ratio: doctor 1.00, girl 0.90, interns 0.85, robot 0.72, fruit fly 0.41.\n'
            'Scene: bright daytime lab setting, white walls, big windows with natural light, small lavender, mint and pink accents. No night, no neon.\n'
            'Characters:\n  %s.\nVisual metaphor of the topic: %s.\n'
            'Composition: keep every face and hand inside the central safe area (12%% margin left and right, 10%% top, 18%% bottom); keep the bottom-left corner plain, bright and simple.\n'
            'Mood: curious, warm, the nervous evening before a pop quiz turning into confidence.\nNo text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.') % (who, meta_en)


def main():
    c = COVERS[0]
    md = ['# 표지 지시문 — 신경망이 보는 법 연구실 (neural_see_lab)', '',
          '페이지 맨 위에 거는 표지 1장의 생성 지시문입니다. Genspark 등 이미지 생성 도구에 붙여 넣으세요.', '',
          '- 그림체: **16비트 RPG풍 픽셀아트 (필수, 고정)** — 매끈한 일러스트·벡터·수채화·3D로 나오면 다시 받습니다.',
          '- 배경: **낮의 연구실** (흰 벽, 큰 창으로 드는 자연광). 밤·네온은 쓰지 않습니다.',
          '- 참고 이미지: GitHub `adminmrobo/fruitfly-lab-expressions`의 기본 그림 — 박사·조수·초파리·주판봇 `images/{doctor,haru,fruitfly,jupanbot}/E13_neutral.png`, 인턴 `images/{sia,moa}/E13_neutral.png`.',
          '- X1~X3(미공개 식구)는 표지에 넣지 않습니다. 본문에서 교보재 담당으로만 나옵니다.',
          '- 받은 그림은 픽셀아트 원래 격자(보통 생성 PNG를 4로 나눈 크기, 예 480×270)를 찾아 `NEAREST` 정수배로만 키운 무손실 WebP `img/cover_00.webp`(예 1920×1080)로 넣고 `python3 build/build_all.py`를 다시 돌리면 대체 표지 대신 보입니다. 같은 그림을 정수배로 잘라 `img/thumb_00.webp`, `img/og_00.webp`도 만듭니다.', '',
          '| 키 | 페이지 | 장소 | 주제 은유 (글자 없이) |', '|---|---|---|---|', '| %s | %s | %s | %s |' % (c[0], c[1], c[3], c[6]),
          '', '**공통 영어 묘사**', ''] + ['- %s: *%s*' % (k, v) for k, v in CH.items()] + ['', '---', '',
          '## %s · %s' % (c[0], c[2]), '', '| 항목 | 내용 |', '|---|---|', '| 키 · 판 | %s · L (16:9, 1920 이상) |' % c[0], '| 장소 | %s |' % c[3],
          '| 등장 | 박사, 조수(하루), 인턴 시아, 인턴 모아, 초파리 연구원, 주판봇 |', '| 대체 글 (alt) | %s |' % c[8], '', '**Genspark에 붙여 넣기 ↓**', '```', prompt(c), '```', '']
    os.makedirs(os.path.join(ROOT, 'docs'), exist_ok=True)
    open(os.path.join(ROOT, 'docs', 'COVER_PROMPTS_neural_see_lab.md'), 'w', encoding='utf-8').write('\n'.join(md))

    img = ['# 신경망이 보는 법 연구실 — 이미지 제작 명세서', '', '## 1. 그림체와 고정 외형', '',
           '- 그림체: 16비트 RPG풍 픽셀아트 (굵은 어두운 외곽선, 2~3단계 명암, 작은 반사광). 캐릭터 팩 `CHAR_lab4`를 따릅니다.',
           '- 장면 조명: 낮의 연구실. 흰 벽, 큰 창의 자연광, 연보라·민트·분홍 소품. 밤·어둠·네온은 쓰지 않습니다.',
           '- 고정 외형: 박사·조수(하루)·초파리 연구원·주판봇 v2·인턴 시아·인턴 모아. X1~X3는 본문 교보재 담당으로만 나오고 표지에는 넣지 않습니다.',
           '- 그림 안 글자·숫자·로고 금지.', '', '## 2. 필요한 그림 전체', '',
           '| 키 | 판 | 상태 | 쓰는 곳 | 만드는 법 |', '|---|---|---|---|---|',
           '| cover_00 | L (16:9) | 새로 그림 (지금은 대체 표지: 픽셀 고양이 + 파란 3×3 창) | 페이지 맨 위 표지 | `COVER_PROMPTS_neural_see_lab.md` |',
           '| thumb_00 | 3:2 | 표지에서 자름 | ahnboat.xyz 카드·현황판 | 표지 가운데 기준, 정수배 |',
           '| og_00 | 1200×630 | 표지에서 자름 | 공유 미리보기(og:image) | 표지 가운데 기준 |',
           '| sc_00_outro | E (3:2) | 선택 | 아웃트로 장면 자리 | 지금은 캐릭터 팩 표정 그림을 한 줄로 세워 대신합니다 |',
           '| 캐릭터 표정 | A (96px) | 캐릭터 팩 재사용 | 말풍선·대화·대결·교보재 상자 | `build_character_pack.py --pick` (쓰는 키만) |',
           '| 픽셀 그림 4장 (고양이·집·컵·뒤섞인 고양이) | 16×16 | 코드로 그림 | 실험 패널 | `code/analysis.py`의 문자열 그림 |', '',
           '## 3. 일관성 지침', '', '- 표지는 시험 전날 장면입니다. 아웃트로(합격)의 표정을 미리 쓰지 않습니다. 시아는 살짝 긴장, 모아는 생각하는 얼굴, 하루는 단단한 얼굴.',
           '- 초파리는 왼쪽에서 오른쪽을, 주판봇은 오른쪽에서 왼쪽을 봅니다.', '- 칠판의 고양이는 이 페이지의 16×16 고양이와 같은 모양(뾰족한 귀 둘, 네모 눈 둘, 회색 코와 입)으로 그립니다.', '']
    open(os.path.join(ROOT, 'docs', 'IMG_neural_see_lab.md'), 'w', encoding='utf-8').write('\n'.join(img))

    items = []
    chars = ['jupanbot' if w == 'robo' else w for w in c[5]]
    items.append({'id': 'cover_00', 'role': 'cover', 'page': 'index.html', 'path': 'img/cover_00.webp', 'size': [1920, 1080], 'characters': chars, 'robot': 'jupanbot-v2',
                  'prompt_en': 'see docs/COVER_PROMPTS_neural_see_lab.md#cover_00', 'source_of': None, 'status': 'ok' if os.path.exists(os.path.join(ROOT, 'img', 'cover_00.webp')) else 'missing', 'alt_ko': c[8]})
    for role, size in (('thumb', [1200, 800]), ('og', [1200, 630])):
        items.append({'id': '%s_00' % role, 'role': role, 'path': 'img/%s_00.webp' % role, 'size': size, 'characters': chars, 'robot': 'jupanbot-v2',
                      'prompt_en': None, 'source_of': 'cover_00', 'status': 'ok' if os.path.exists(os.path.join(ROOT, 'img', '%s_00.webp' % role)) else 'missing'})
    man = {'series_ko': 'AI 기초 · 컴퓨터 비전 (CNN)', 'title_ko': '신경망이 보는 법 연구실 (neural_see_lab) — 신경망은 고양이를 어떻게 "볼까"', 'site_title': '신경망은 고양이를 어떻게 "볼까" — 쪽지시험 대비반',
           'site_url': 'https://adminmrobo.github.io/neural_see_lab/',
           'ontology': {'pages': [{'path': 'index.html', 'kg': True, 'export': True}], 'files': ['kg/index/kg.json']},
           'i18n': {'langs': ['ko'], 'pages': {'ko': 1}, 'readme_langs': ['ko']}, 'languages': ['ko'], 'items': items, 'updated': '2026-11-23'}
    json.dump(man, open(os.path.join(ROOT, 'cover_manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('docs ok', len(items))


if __name__ == '__main__':
    main()
