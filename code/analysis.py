# -*- coding: utf-8 -*-
"""신경망이 보는 법 연구실 — 모든 본문 숫자의 원본.

16×16 픽셀 그림(진하기 0·0.5·1)에 3×3 필터 4장을 대고(196군데), ReLU를 거친 뒤
2×2 최댓값 풀링(14×14 → 7×7)을 하고, 사람이 정한 부품 탐지기(귀·눈·입)로 얼굴을 판정한다.
페이지의 nsee.js가 같은 계산을 브라우저에서 다시 하고, build/check_numbers.js가 두 결과를 맞춰 본다.
"""
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# '#'=1 (검정), '+'=0.5 (회색), '.'=0 (흰색). 값은 '진하기'다.
CAT = [
    "................",
    "..##........##..",
    ".#+#........#+#.",
    ".#++#......#++#.",
    ".#..########..#.",
    ".#............#.",
    "#..............#",
    "#..##......##..#",
    "#..##......##..#",
    "#..............#",
    "#......++......#",
    "#.....####.....#",
    "#..............#",
    ".#............#.",
    "..############..",
    "................",
]
HOUSE = [
    "................",
    ".......##.......",
    "......#..#......",
    ".....#....#.....",
    "....#......#....",
    "...#........#...",
    "..############..",
    "..#..........#..",
    "..#.++....++.#..",
    "..#.++....++.#..",
    "..#..........#..",
    "..#....##....#..",
    "..#....##....#..",
    "..#....##....#..",
    "..############..",
    "................",
]
CUP = [
    "................",
    "................",
    "................",
    "..##########....",
    "..#........#....",
    "..#........####.",
    "..#........#..#.",
    "..#........#..#.",
    "..#........#..#.",
    "..#........####.",
    "..#........#....",
    "...#......#.....",
    "....######......",
    "................",
    ".##############.",
    "................",
]
# 뒤섞인 고양이: 귀 띠(0~5행)와 입 띠(10~15행)를 맞바꿨다. 부품은 그대로, 자리만 틀렸다.
SCRAMBLED = CAT[10:16] + CAT[6:10] + CAT[0:6]

IMAGES = {'cat': ('고양이', CAT), 'house': ('집', HOUSE), 'cup': ('컵', CUP), 'scrambled': ('뒤섞인 고양이', SCRAMBLED)}

FILTERS = {
    'v': ('세로 경계 (오른쪽이 진함)', [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
    'h': ('가로 경계 (아래쪽이 진함)', [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
    'vr': ('세로 경계 (왼쪽이 진함)', [[1, 0, -1], [2, 0, -2], [1, 0, -1]]),
    'hr': ('가로 경계 (위쪽이 진함)', [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]),
}
FORDER = ['v', 'h', 'vr', 'hr']


def grid(rows):
    m = {'#': 1.0, '+': 0.5, '.': 0.0}
    return [[m[c] for c in r] for r in rows]


def conv(img, k):
    n = len(img) - 2
    return [[sum(img[r + i][c + j] * k[i][j] for i in range(3) for j in range(3)) for c in range(n)] for r in range(n)]


def relu(m):
    return [[max(0.0, v) for v in row] for row in m]


def pool(m, how='max'):
    n = len(m) // 2
    out = []
    for r in range(n):
        row = []
        for c in range(n):
            v = [m[2 * r][2 * c], m[2 * r][2 * c + 1], m[2 * r + 1][2 * c], m[2 * r + 1][2 * c + 1]]
            row.append(max(v) if how == 'max' else sum(v) / 4)
        out.append(row)
    return out


def features(img, do_pool=True):
    out = {}
    for f in FORDER:
        e = relu(conv(img, FILTERS[f][1]))
        out[f] = pool(e) if do_pool else e
    return out


def flat(feat):
    return [v for f in FORDER for row in feat[f] for v in row]


def cosine(a, b):
    d = sum(x * y for x, y in zip(a, b)); na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(y * y for y in b))
    return d / (na * nb) if na and nb else 0.0


def shift(img, dx, dy):
    n = len(img)
    return [[img[r - dy][c - dx] if 0 <= r - dy < n and 0 <= c - dx < n else 0.0 for c in range(n)] for r in range(n)]


# ── 부품 탐지기 (사람이 정한 설명용, 실제 신경망은 학습으로 만든다) ──
# 고양이 그림의 풀링 지도(7×7, 4장)에서 부품 자리를 3×3 창으로 떼어 '본보기'로 삼는다.
PARTS = {'ear_l': ('왼쪽 귀', 0, 0), 'ear_r': ('오른쪽 귀', 0, 4), 'eye_l': ('왼쪽 눈', 3, 0), 'eye_r': ('오른쪽 눈', 3, 4), 'mouth': ('입', 4, 2)}
PORDER = ['ear_l', 'ear_r', 'eye_l', 'eye_r', 'mouth']
THRESH = 0.80  # 부품을 찾았다고 보는 닮음 문턱 (코사인)


def window(feat, r, c, h=2, w=3):
    return [feat[f][r + i][c + j] for f in FORDER for i in range(h) for j in range(w)]


def part_templates(catfeat):
    T = {}
    for p in PORDER:
        _, r, c = PARTS[p]
        T[p] = window(catfeat, r, c)
    return T


def detect(feat, T):
    res = {}
    n = len(feat['v'])
    for p in PORDER:
        best = (-1, 0, 0)
        for r in range(n - 1):
            for c in range(n - 2):
                s = cosine(window(feat, r, c), T[p])
                if s > best[0] + 1e-9:
                    best = (s, r, c)
        res[p] = {'score': round(best[0], 4), 'r': best[1], 'c': best[2], 'found': best[0] >= THRESH}
    return res


def judge(det):
    found = sum(1 for p in PORDER if det[p]['found'])
    count_rule = found >= 4  # 부품 개수만 세기
    ok_place = (det['ear_l']['found'] and det['ear_r']['found'] and det['eye_l']['found'] and det['eye_r']['found'] and det['mouth']['found']
                and max(det['ear_l']['r'], det['ear_r']['r']) < min(det['eye_l']['r'], det['eye_r']['r']) < det['mouth']['r']
                and det['eye_l']['c'] < det['mouth']['c'] < det['eye_r']['c'])
    return {'found': found, 'count_rule': count_rule, 'place_rule': bool(ok_place)}


def receptive():
    """층마다 한 점이 원본에서 보는 범위 (가로 = 세로)"""
    layers = [('1층 필터 3×3', 3, 1), ('1층 풀링 2×2', 2, 2), ('2층 필터 3×3', 3, 1), ('2층 풀링 2×2', 2, 2), ('3층 필터 3×3', 3, 1)]
    rf, jump, out = 1, 1, []
    for name, k, s in layers:
        rf = rf + (k - 1) * jump
        jump *= s
        out.append({'layer': name, 'rf': rf, 'jump': jump})
    return out


def r3(m):
    return [[round(v, 3) for v in row] for row in m]


def main():
    imgs = {k: grid(v[1]) for k, v in IMAGES.items()}
    cat = imgs['cat']
    R = {'n': {'img': 16, 'map': 14, 'patches': 14 * 14, 'pooled': 7}}

    # 2단계: 영상에 나온 자리 번호 예시와 손계산 예 (세로 경계)
    edge = {f: conv(cat, FILTERS[f][1]) for f in FORDER}
    R['edge_raw'] = {f: r3(edge[f]) for f in FORDER}
    R['edge_stats'] = {f: {'pos': sum(1 for row in edge[f] for v in row if v > 0), 'neg': sum(1 for row in edge[f] for v in row if v < 0),
                           'max': max(v for row in edge[f] for v in row), 'min': min(v for row in edge[f] for v in row)} for f in FORDER}
    # 손계산 예: 왼쪽 위 귀 바깥 (r=1,c=0) 패치
    hand = []
    for (r, c) in [(1, 0), (5, 0), (2, 2)]:
        patch = [row[c:c + 3] for row in cat[r:r + 3]]
        s = sum(patch[i][j] * FILTERS['v'][1][i][j] for i in range(3) for j in range(3))
        hand.append({'r': r, 'c': c, 'no': r * 14 + c + 1, 'patch': patch, 'sum': s, 'relu': max(0, s)})
    R['hand'] = hand

    # 3단계: ReLU와 풀링
    relu_v = relu(edge['v'])
    R['relu_kept'] = {f: sum(1 for row in relu(edge[f]) for v in row if v > 0) for f in FORDER}
    R['pool_v'] = r3(pool(relu_v))
    R['pool_avg_v'] = r3(pool(relu_v, 'avg'))
    # 풀링 손계산 예 (4×4 → 2×2)
    blk = [row[0:4] for row in relu_v[4:8]]
    R['pool_hand'] = {'block': r3(blk), 'max': r3(pool(blk)), 'avg': r3(pool(blk, 'avg'))}

    # 대결: 1픽셀 옮긴 고양이 — 풀링 전(14×14)과 후(7×7)의 닮음
    duel = {}
    for name, (dx, dy) in {'right1': (1, 0), 'down1': (0, 1), 'right2': (2, 0)}.items():
        s = shift(cat, dx, dy)
        a0, b0 = flat(features(cat, False)), flat(features(s, False))
        a1, b1 = flat(features(cat, True)), flat(features(s, True))
        duel[name] = {'nopool': round(cosine(a0, b0), 4), 'pool': round(cosine(a1, b1), 4)}
    R['duel'] = duel

    # 4단계: 보는 범위와 부품 판정
    R['receptive'] = receptive()
    T = part_templates(features(cat))
    det = {}
    for k in IMAGES:
        d = detect(features(imgs[k]), T)
        det[k] = {'parts': d, 'judge': judge(d)}
    R['detect'] = det
    R['thresh'] = THRESH

    # 쪽지시험 정답 (손계산 문제)
    q2 = [[1, 0, 0], [1, 0.5, 0], [0, 0, 1]]
    R['exam'] = {'q2_patch': q2, 'q2_sum': sum(q2[i][j] * FILTERS['v'][1][i][j] for i in range(3) for j in range(3)),
                 'q3_block': [[0, 2, 1, 0], [3, 1, 0, 0], [0, 0, 4, 2], [1, 0, 0, 0]]}
    R['exam']['q3_max'] = pool(R['exam']['q3_block'])

    data = {'images': {k: {'name': v[0], 'rows': v[1]} for k, v in IMAGES.items()},
            'filters': {k: {'name': v[0], 'k': v[1]} for k, v in FILTERS.items()}, 'forder': FORDER,
            'parts': {k: {'name': PARTS[k][0], 'r': PARTS[k][1], 'c': PARTS[k][2]} for k in PORDER}, 'porder': PORDER, 'thresh': THRESH}
    os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
    json.dump(data, open(os.path.join(ROOT, 'data', 'nsee.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(R, open(os.path.join(ROOT, 'data', 'results.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return R


if __name__ == '__main__':
    R = main()
    print(json.dumps({k: R[k] for k in ('hand', 'relu_kept', 'edge_stats', 'pool_hand', 'duel', 'receptive', 'exam')}, ensure_ascii=False))
    for k, v in R['detect'].items():
        print(k, v['judge'], {p: (x['score'], x['r'], x['c']) for p, x in v['parts'].items()})
