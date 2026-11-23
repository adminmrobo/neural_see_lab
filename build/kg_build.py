# -*- coding: utf-8 -*-
"""페이지마다 kg.json · refs.json · meta.json을 만들고 retrofit.py로 #kg·#export를 붙인 뒤 check.py로 점검한다."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from lib import R, SERIES, SITE

DATE = '2026-11-23'
BB = os.path.join(HERE, 'backbone_ai.json')
V = lambda **k: dict({'title': True, 'author': True, 'year': True, 'container': True, 'pages': False, 'doi': False}, **k)
REFS = {
    'ahn2026nsee': {'type': 'dataset', 'title': '신경망이 보는 법 연구실 설명용 데이터 (16×16 픽셀 그림·필터·부품 탐지기)', 'author': [{'family': '안', 'given': '상선'}], 'publisher': '(주)M-Robo',
                    'URL': 'https://github.com/adminmrobo/neural_see_lab', 'year': 2026, 'role': 'data', 'verified': V(), 'checkedBy': '이 저장소 code/analysis.py', 'checkedSource': 'repo'},
    'hubel1959': {'type': 'article-journal', 'title': "Receptive fields of single neurones in the cat's striate cortex", 'author': [{'family': 'Hubel', 'given': 'David H.'}, {'family': 'Wiesel', 'given': 'Torsten N.'}],
                  'container-title': 'Journal of Physiology', 'volume': '148', 'issue': '3', 'page': '574-591', 'year': 1959, 'role': 'background', 'verified': V()},
    'maisak2013': {'type': 'article-journal', 'title': 'A directional tuning map of Drosophila elementary motion detectors', 'author': [{'family': 'Maisak', 'given': 'Matthew S.'}, {'family': 'Haag', 'given': 'Juergen'}, {'family': 'Borst', 'given': 'Alexander'}],
                   'container-title': 'Nature', 'volume': '500', 'page': '212-216', 'year': 2013, 'role': 'background', 'verified': V()},
    'fukushima1980': {'type': 'article-journal', 'title': 'Neocognitron: A self-organizing neural network model for a mechanism of pattern recognition unaffected by shift in position', 'author': [{'family': 'Fukushima', 'given': 'Kunihiko'}],
                      'container-title': 'Biological Cybernetics', 'volume': '36', 'issue': '4', 'page': '193-202', 'year': 1980, 'role': 'method', 'verified': V()},
    'lecun1998': {'type': 'article-journal', 'title': 'Gradient-based learning applied to document recognition', 'author': [{'family': 'LeCun', 'given': 'Yann'}, {'family': 'Bottou', 'given': 'Léon'}, {'family': 'Bengio', 'given': 'Yoshua'}, {'family': 'Haffner', 'given': 'Patrick'}],
                  'container-title': 'Proceedings of the IEEE', 'volume': '86', 'issue': '11', 'page': '2278-2324', 'year': 1998, 'role': 'method', 'verified': V()},
    'krizhevsky2012': {'type': 'paper-conference', 'title': 'ImageNet classification with deep convolutional neural networks', 'author': [{'family': 'Krizhevsky', 'given': 'Alex'}, {'family': 'Sutskever', 'given': 'Ilya'}, {'family': 'Hinton', 'given': 'Geoffrey E.'}],
                       'container-title': 'NeurIPS 2012', 'year': 2012, 'role': 'background', 'verified': V()},
    'zeiler2014': {'type': 'paper-conference', 'title': 'Visualizing and understanding convolutional networks', 'author': [{'family': 'Zeiler', 'given': 'Matthew D.'}, {'family': 'Fergus', 'given': 'Rob'}],
                   'container-title': 'ECCV 2014', 'year': 2014, 'role': 'background', 'verified': V()},
    'sabour2017': {'type': 'paper-conference', 'title': 'Dynamic routing between capsules', 'author': [{'family': 'Sabour', 'given': 'Sara'}, {'family': 'Frosst', 'given': 'Nicholas'}, {'family': 'Hinton', 'given': 'Geoffrey E.'}],
                   'container-title': 'NeurIPS 2017', 'year': 2017, 'role': 'background', 'verified': V()},
    'video_nnsees8': {'type': 'motion_picture', 'title': 'HOW A NEURAL NET SEES · PART 8 (짧은 영상, 사용자 제공)', 'author': [{'family': '제작자 표기 없음', 'given': ''}],
                      'role': 'background', 'verified': V(year=False, author=False, container=False), 'checkedBy': '사용자가 준 영상 파일을 직접 확인 (2026-11-23)', 'checkedSource': 'file'},
}


def ref(rid):
    r = dict(REFS[rid]); y = r.pop('year', None); role = r.pop('role', 'background')
    ver = r.pop('verified'); cb = r.pop('checkedBy', '페이지 참고문헌 목록에서 옮김 (외부 대조 안 함)'); cs = r.pop('checkedSource', 'page')
    o = {'id': rid}; o.update(r)
    if y: o['issued'] = {'date-parts': [[y]]}
    o['lab'] = {'work': 'lab:work/' + rid, 'role': role, 'supports': [], 'locs': [], 'verified': ver, 'checkedBy': cb, 'checkedSource': cs}
    return o


T = 'lab:topic/'
QMAP = {}


def build_page(slug, number, title, about, refs, nodes, edges, quiz=None, qanchor=None):
    N, E = [], []
    for t in nodes:
        nid, typ, ko, en, anchor, lvl, dfn = t[:7]
        n = {'id': nid, 'type': typ, 'label': {'ko': ko, 'en': en}, 'page': slug, 'anchor': anchor, 'level': lvl, 'status': 'known', 'confidence': 'high', 'coverage': 'explained', 'match': [], 'domain': ['ai']}
        if dfn: n['definition'] = {'ko': dfn}
        if len(t) > 7 and t[7]: n['source'] = [{'ref': t[7], 'loc': ''}]
        N.append(n)
    for rid in refs:
        a = REFS[rid]
        N.append({'id': 'lab:work/' + rid, 'type': 'Work', 'label': {'ko': '%s (%s) %s' % (a['author'][0]['family'] + (' 외' if len(a['author']) > 1 else ''), a.get('year') or 'n.d.', a.get('container-title') or a.get('publisher', '')), 'en': a['title']},
                  'page': slug, 'anchor': '#export', 'level': 2, 'status': 'known', 'confidence': 'high', 'coverage': 'explained', 'match': []})
    for s, p, o, anchor in edges:
        E.append({'s': s, 'p': 'lab:' + p, 'o': o, 'anchor': anchor, 'confidence': 'high'})
    cited = set()
    for n in N:
        for sr in n.get('source', []):
            E.append({'s': n['id'], 'p': 'lab:assertedIn', 'o': 'lab:work/' + sr['ref'], 'anchor': n['anchor'], 'confidence': 'high'}); cited.add(sr['ref'])
    for rid in refs:
        if rid not in cited:
            E.append({'s': about[0], 'p': 'lab:explainedIn', 'o': 'lab:work/' + rid, 'anchor': '#export', 'confidence': 'high'})
    if quiz:
        for qid, items in quiz.items():
            sec = qanchor(qid)
            for k, q in enumerate(items):
                nid = 'lab:quiz/nsee-%s-%s-%d' % (number, qid, k + 1)
                N.append({'id': nid, 'type': 'QuizItem', 'label': {'ko': q['q'][:60], 'en': 'Quiz %s %s-%d' % (number, qid, k + 1)}, 'page': slug, 'anchor': sec, 'level': 2,
                          'status': 'known', 'confidence': 'high', 'coverage': 'explained', 'match': []})
                E.append({'s': nid, 'p': 'lab:assesses', 'o': QMAP[qid], 'anchor': sec, 'confidence': 'high'})
    kg = {'version': '1.0', 'page': slug, 'nodes': N, 'edges': E}
    meta = {'title': title, 'number': number, 'series': SERIES, 'about': about, 'basedOn': refs, 'educationalLevel': '입문',
            'creator': [{'name': '안상선', 'role': 'author'}], 'contributor': [{'name': 'AI 보조 제작', 'role': 'assistant'}], 'date': DATE, 'version': '1.0',
            'language': ['ko'], 'license': '', 'url': SITE + slug + '.html', 'registry': 'KG_00_registry 0.2', 'learningResourceType': 'interactive explainer', 'seeAlso': '', 'domain': ['ai'],
            'suggestedCitation': '안상선 (2026). %s. %s %s, v1.0.' % (title, SERIES, number)}
    return kg, [ref(r) for r in refs], meta


def pages():
    P = {}
    import p00
    if not p00.QUIZ:
        p00.build_page()
    du = R['duel']['right1']; sc = R['detect']['scrambled']['judge']
    QMAP.update({'q1': 'lab:concept/pixel-grid', 'q2': 'lab:method/convolution-filter', 'q3': 'lab:method/max-pooling', 'q4': 'lab:concept/feature-hierarchy'})
    P['index'] = ('index', '0', '신경망은 고양이를 어떻게 "볼까" — 쪽지시험 대비반', ['lab:concept/cnn-vision-pipeline', 'lab:method/convolution-filter'],
                  ['ahn2026nsee', 'video_nnsees8', 'hubel1959', 'maisak2013', 'fukushima1980', 'lecun1998', 'krizhevsky2012', 'zeiler2014', 'sabour2017'], [
        ('lab:concept/cnn-vision-pipeline', 'Concept', '신경망이 그림을 보는 네 단계', 'How a CNN sees: four steps', '#map', 1, '숫자 격자 → 필터 → ReLU·풀링 → 깊은 층의 부품·전체', 'lecun1998'),
        ('lab:concept/pixel-grid', 'Concept', '픽셀 격자 (그림 = 숫자 표)', 'Image as a pixel grid', '#s1', 1, '픽셀마다 진하기 숫자 하나, 16×16 = 256개'),
        ('lab:bio/photoreceptor-ommatidium', 'BioAnalogue', '시각 세포·초파리 낱눈', 'Photoreceptors and ommatidia', '#s1', 2, '한 점의 밝기를 맡는 생물의 감각 단위'),
        ('lab:method/convolution-filter', 'Method', '3×3 필터 합성곱 (소벨 경계 필터)', 'Convolution with 3×3 edge filters', '#s2', 1, '필터 숫자 × 진하기를 아홉 번 더해 점수, 196곳', 'lecun1998'),
        ('lab:concept/edge-map', 'Concept', '경계 지도 (특징 지도)', 'Edge map (feature map)', '#s2', 2, '필터 점수를 자리마다 적은 14×14 표'),
        ('lab:bio/orientation-cell', 'BioAnalogue', '방향 선택 세포 (고양이 시각 피질), T4·T5 (초파리)', 'Orientation-selective cells; Drosophila T4/T5', '#s2', 2, '특정 방향의 경계에 크게 반응', 'hubel1959'),
        ('lab:claim/sign-is-direction', 'Claim', '필터 점수의 부호는 방향, 크기는 세기 (−3.0은 반대 방향의 강한 경계)', 'Sign encodes direction', '#s2', 2, ''),
        ('lab:method/relu', 'Method', 'ReLU (음수는 0)', 'ReLU', '#s3', 2, 'max(0, x)'),
        ('lab:method/max-pooling', 'Method', '2×2 최댓값 풀링 (14×14 → 7×7)', 'Max pooling', '#s3', 1, '2×2마다 가장 큰 값 하나', 'fukushima1980'),
        ('lab:bio/complex-cell', 'BioAnalogue', '복합 세포', 'Complex cells', '#s3', 2, '조금 넓은 범위 어디든 선이 있으면 반응', 'hubel1959'),
        ('lab:claim/pooling-shift', 'Claim', '1픽셀 옮긴 고양이의 지도 닮음: 풀링 %.1f%%, 풀링 안 함 %.1f%%' % (du['pool'] * 100, du['nopool'] * 100), 'Pooling tolerates small shifts', '#duel', 2, '', 'ahn2026nsee'),
        ('lab:limitation/pooling-loses-position', 'Limitation', '풀링은 정확한 자리를 흐린다', 'Pooling blurs position', '#s3', 2, ''),
        ('lab:concept/receptive-field', 'Concept', '보는 범위 (수용 영역) 3 → 4 → 8 → 10 → 18', 'Receptive field growth', '#s4', 2, '층을 쌓을수록 한 점이 원본에서 보는 범위가 넓어짐'),
        ('lab:concept/feature-hierarchy', 'Concept', '선 → 부품 → 전체 (특징의 위계)', 'Feature hierarchy', '#s4', 1, '깊은 층일수록 큰 모양에 반응', 'zeiler2014'),
        ('lab:claim/scrambled-fools-count', 'Claim', '뒤섞인 고양이: 부품 %d개를 모두 찾지만 자리 판정에서 탈락' % sc['found'], 'Part counting is fooled by scrambled faces', '#s4', 2, '', 'sabour2017'),
        ('lab:limitation/hand-set-filters', 'Limitation', '이 페이지의 필터·부품 탐지기는 사람이 정한 설명용 (실제는 학습)', 'Filters are hand-set here', '#sum', 2, '', 'krizhevsky2012'),
        ('lab:sim/nsee-filter-scan', 'Simulation', '필터 훑기 패널', 'Filter scan lab', '#s2', 2, ''),
        ('lab:sim/nsee-part-judge', 'Simulation', '부품 판정 패널 (개수 vs 자리)', 'Part judge lab', '#s4', 2, ''),
        ('lab:task/nsee-exam', 'Task', '쪽지시험 4문항 + 보너스', 'Quiz: four items plus bonus', '#exam', 2, ''),
        ('lab:question/what-did-it-see', 'Question', 'AI가 "고양이 99%"라고 할 때 무엇을 보고 그렇게 말했나?', 'What did the model look at?', '#s4', 2, '')], [
        ('lab:concept/cnn-vision-pipeline', 'broader', T + 'convolution', '#map'), ('lab:concept/pixel-grid', 'broader', T + 'linear-algebra', '#s1'),
        ('lab:method/convolution-filter', 'broader', T + 'convolution', '#s2'), ('lab:concept/edge-map', 'broader', T + 'convolution', '#s2'),
        ('lab:method/relu', 'broader', T + 'activation-function', '#s3'), ('lab:method/max-pooling', 'broader', T + 'pooling', '#s3'),
        ('lab:concept/receptive-field', 'broader', T + 'receptive-field', '#s4'), ('lab:concept/feature-hierarchy', 'broader', T + 'convolution', '#s4'),
        ('lab:bio/photoreceptor-ommatidium', 'broader', T + 'sensory-processing', '#s1'), ('lab:bio/orientation-cell', 'broader', T + 'sensory-processing', '#s2'),
        ('lab:bio/complex-cell', 'broader', T + 'sensory-processing', '#s3'), ('lab:limitation/hand-set-filters', 'broader', T + 'backpropagation', '#sum'),
        ('lab:question/what-did-it-see', 'broader', T + 'interpretability', '#s4'), ('lab:limitation/pooling-loses-position', 'broader', T + 'pooling', '#s3'),
        ('lab:concept/pixel-grid', 'prerequisiteOf', 'lab:method/convolution-filter', '#s1'), ('lab:method/convolution-filter', 'prerequisiteOf', 'lab:method/max-pooling', '#s2'),
        ('lab:method/max-pooling', 'prerequisiteOf', 'lab:concept/receptive-field', '#s3'),
        ('lab:bio/photoreceptor-ommatidium', 'bioAnalogueOf', 'lab:concept/pixel-grid', '#s1'), ('lab:bio/orientation-cell', 'bioAnalogueOf', 'lab:method/convolution-filter', '#s2'),
        ('lab:bio/complex-cell', 'bioAnalogueOf', 'lab:method/max-pooling', '#s3'), ('lab:method/convolution-filter', 'partOf', 'lab:concept/cnn-vision-pipeline', '#map'),
        ('lab:method/max-pooling', 'partOf', 'lab:concept/cnn-vision-pipeline', '#map'), ('lab:method/relu', 'partOf', 'lab:concept/cnn-vision-pipeline', '#map'),
        ('lab:concept/edge-map', 'partOf', 'lab:method/convolution-filter', '#s2'), ('lab:claim/sign-is-direction', 'supports', 'lab:concept/edge-map', '#s2'),
        ('lab:claim/pooling-shift', 'supports', 'lab:method/max-pooling', '#duel'), ('lab:method/max-pooling', 'hasLimitation', 'lab:limitation/pooling-loses-position', '#s3'),
        ('lab:limitation/pooling-loses-position', 'addressedBy', 'lab:concept/feature-hierarchy', '#s4'), ('lab:concept/receptive-field', 'prerequisiteOf', 'lab:concept/feature-hierarchy', '#s4'),
        ('lab:claim/scrambled-fools-count', 'supports', 'lab:limitation/pooling-loses-position', '#s4'), ('lab:concept/cnn-vision-pipeline', 'hasLimitation', 'lab:limitation/hand-set-filters', '#sum'),
        ('lab:sim/nsee-filter-scan', 'demonstratedBy', 'lab:method/convolution-filter', '#s2'), ('lab:sim/nsee-part-judge', 'demonstratedBy', 'lab:concept/feature-hierarchy', '#s4'),
        ('lab:task/nsee-exam', 'assesses', 'lab:concept/cnn-vision-pipeline', '#exam'), ('lab:question/what-did-it-see', 'addressedBy', 'lab:sim/nsee-part-judge', '#s4')],
        (p00.QUIZ, lambda q: '#s' + q[1]))
    return P


def main():
    P = pages()
    report, newids = [], {}
    for key, (slug, number, title, about, refs, nodes, edges, qz) in P.items():
        quiz, qa = (qz if qz else (None, None))
        kg, rf, meta = build_page(slug, number, title, about, refs, nodes, edges, quiz, qa)
        if slug == 'practice/index': meta['url'] = SITE + 'practice/'
        if slug == 'index': meta['url'] = SITE
        for n in kg['nodes']:
            if n['type'] not in ('Work', 'QuizItem') and n['id'] not in newids:
                newids[n['id']] = {'label': n['label'], 'type': n['type'], 'first_page': slug}
        d = os.path.join(ROOT, 'kg', slug.replace('/index', '') if slug != 'index' else 'index')
        os.makedirs(d, exist_ok=True)
        for n, o in (('kg.json', kg), ('refs.json', rf), ('meta.json', meta)):
            json.dump(o, open(os.path.join(d, n), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        html = os.path.join(ROOT, slug + '.html'); orig = html + '.orig'
        open(orig, 'w', encoding='utf-8').write(open(html, encoding='utf-8').read())
        subprocess.check_call(['python3', os.path.join(HERE, 'retrofit.py'), orig, '--kg', os.path.join(d, 'kg.json'), '--refs', os.path.join(d, 'refs.json'),
                               '--meta', os.path.join(d, 'meta.json'), '--backbone', BB, '-o', html])
        rep = os.path.join(d, 'check_report.md')
        subprocess.call(['python3', os.path.join(HERE, 'check.py'), orig, html, '--backbone', BB, '--report', rep])
        os.remove(orig)
        report.append((slug, open(rep, encoding='utf-8').read()))
    json.dump({'series': 'neural_see_lab', 'date': DATE, 'new_ids': newids}, open(os.path.join(ROOT, 'KG_new_ids.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for s, r in report:
        print('=====', s); print(r[:900])


if __name__ == '__main__':
    main()
