# 표지 지시문 — 신경망이 보는 법 연구실 (neural_see_lab)

페이지 맨 위에 거는 표지 1장의 생성 지시문입니다. Genspark 등 이미지 생성 도구에 붙여 넣으세요.

- 그림체: **16비트 RPG풍 픽셀아트 (필수, 고정)** — 매끈한 일러스트·벡터·수채화·3D로 나오면 다시 받습니다.
- 배경: **낮의 연구실** (흰 벽, 큰 창으로 드는 자연광). 밤·네온은 쓰지 않습니다.
- 참고 이미지: GitHub `adminmrobo/fruitfly-lab-expressions`의 기본 그림 — 박사·조수·초파리·주판봇 `images/{doctor,haru,fruitfly,jupanbot}/E13_neutral.png`, 인턴 `images/{sia,moa}/E13_neutral.png`.
- X1~X3(미공개 식구)는 표지에 넣지 않습니다. 본문에서 교보재 담당으로만 나옵니다.
- 받은 그림은 픽셀아트 원래 격자(보통 생성 PNG를 4로 나눈 크기, 예 480×270)를 찾아 `NEAREST` 정수배로만 키운 무손실 WebP `img/cover_00.webp`(예 1920×1080)로 넣고 `python3 build/build_all.py`를 다시 돌리면 대체 표지 대신 보입니다. 같은 그림을 정수배로 잘라 `img/thumb_00.webp`, `img/og_00.webp`도 만듭니다.

| 키 | 페이지 | 장소 | 주제 은유 (글자 없이) |
|---|---|---|---|
| cover_00 | index.html | 낮의 연구실 강의실, 큰 창과 흰 칠판, 책상 위 교보재 상자 세 개 | 칠판에 붙인 16×16 픽셀 고양이 얼굴(글자 없음) 위에 파란 3×3 돋보기 창이 걸려 있고, 그 옆으로 초록·노랑 작은 사각형이 줄지어 선(경계)을 이룸. 인턴 둘이 앞줄에서 쪽지시험 대비 노트를 펼치고 하루가 칠판을 가리킴. 박사·초파리·주판봇은 뒤쪽 출제위원 책상에 앉아 있음 |

**공통 영어 묘사**

- doc: *chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie*
- asst: *girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans*
- fly: *anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings*
- robo: *boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus*
- sia: *young intern girl in a classic black-and-white maid-style uniform, straight black hair*
- moa: *young intern girl in a classic black-and-white maid-style uniform, wavy beige hair*

---

## cover_00 · 신경망은 고양이를 어떻게 "볼까" — 쪽지시험 대비반

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_00 · L (16:9, 1920 이상) |
| 장소 | 낮의 연구실 강의실, 큰 창과 흰 칠판, 책상 위 교보재 상자 세 개 |
| 등장 | 박사, 조수(하루), 인턴 시아, 인턴 모아, 초파리 연구원, 주판봇 |
| 대체 글 (alt) | 쪽지시험 전날, 하루가 픽셀 고양이 그림 앞에서 인턴 둘을 가르치고 출제위원 셋이 뒤에서 지켜보는 강의실 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- 비율 16:9, 가로 1920px 이상
- 그림체는 반드시 16비트 RPG풍 픽셀아트 (네모 픽셀이 보이게, 매끈한 일러스트·벡터·수채화·3D 금지)
- 첨부한 참고 이미지의 캐릭터를 같은 외형으로, 모두 픽셀아트로 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게
아래 영어 프롬프트를 그대로 써 줘.

Website top cover illustration, wide 16:9.
Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2-3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.
Match the characters' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style. Height ratio: doctor 1.00, girl 0.90, interns 0.85, robot 0.72, fruit fly 0.41.
Scene: bright daytime lab setting, white walls, big windows with natural light, small lavender, mint and pink accents. No night, no neon.
Characters:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, center back, calm guiding gesture;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, front center;
  young intern girl in a classic black-and-white maid-style uniform, straight black hair, seated on the left;
  young intern girl in a classic black-and-white maid-style uniform, wavy beige hair, seated next to her on the right;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, pointing with curiosity;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, holding a wooden abacus.
Visual metaphor of the topic: a big pixelated 16x16 cat face made of black and gray squares pinned on a white board, with a blue square magnifying frame covering a 3x3 patch of it; next to it, rows of small green and amber squares forming edge lines; two interns at the front desk open their study notebooks for a pop quiz, the girl researcher points at the board; behind them, the doctor, the fruit fly and the robot sit at a judges' desk with blank answer sheets.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain, bright and simple.
Mood: curious, warm, the nervous evening before a pop quiz turning into confidence.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```
