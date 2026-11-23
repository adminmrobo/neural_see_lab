// 페이지의 nsee.js 계산이 code/analysis.py의 results.json과 같은지 맞춰 본다
const fs = require('fs'), path = require('path');
const ROOT = path.dirname(__dirname);
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const data = html.match(/<script type="application\/json" id="nsee-data">([\s\S]*?)<\/script>/)[1];
const R = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'results.json'), 'utf8'));
// 브라우저 흉내
const el = () => ({ addEventListener() {}, textContent: data, getContext() { return {}; } });
global.document = { getElementById: (id) => id === 'nsee-data' ? { textContent: data } : null, querySelector: () => null, querySelectorAll: () => [] };
global.window = {}; global.$ = () => null; global.$$ = () => []; global.Loop = { add() {} }; global.Duel = () => {};
eval(fs.readFileSync(path.join(__dirname, 'nsee.js'), 'utf8'));
const A = window.NS.api; let bad = 0;
const ok = (name, a, b) => { const g = Math.abs(a - b) < 1e-3; if (!g) bad++; console.log((g ? 'OK  ' : 'BAD ') + name, a, b); };
const cat = A.IM.cat;
for (const sh of ['right1', 'down1', 'right2']) {
  const m = { right1: [1, 0], down1: [0, 1], right2: [2, 0] }[sh]; const s = A.shift(cat, m[0], m[1]);
  ok('duel ' + sh + ' pool', A.cosine(A.flat(A.features(cat, true)), A.flat(A.features(s, true))), R.duel[sh].pool);
  ok('duel ' + sh + ' nopool', A.cosine(A.flat(A.features(cat, false)), A.flat(A.features(s, false))), R.duel[sh].nopool);
}
for (const k of Object.keys(R.detect)) {
  const d = A.detect(A.features(A.IM[k]), A.D.thresh), j = A.judge(d);
  ok('detect ' + k + ' found', j.found, R.detect[k].judge.found);
  ok('detect ' + k + ' count', +j.count_rule, +R.detect[k].judge.count_rule);
  ok('detect ' + k + ' place', +j.place_rule, +R.detect[k].judge.place_rule);
}
const E = A.conv(cat, A.D.filters.v.k);
for (const h of R.hand) ok('hand #' + h.no, E[h.r][h.c], h.sum);
ok('exam q2', A.conv(R.exam.q2_patch, A.D.filters.v.k)[0][0], 4);
ok('exam q3', JSON.stringify(A.pool(R.exam.q3_block)) === JSON.stringify([[3, 1], [1, 4]]) ? 1 : 0, 1);
console.log(bad ? '불일치 ' + bad + '건' : '숫자 검산: 모두 일치');
process.exit(bad ? 1 : 0);
