# 쪽지시험 채점·대결·자리 71번 단추가 실제로 동작하는지 브라우저에서 확인한다
import asyncio, os
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await (await b.new_context(viewport={'width': 1280, 'height': 900})).new_page()
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.route('**/fonts.g*/**', lambda r: r.abort())
        await pg.goto('file://' + os.path.join(ROOT, 'index.html')); await pg.wait_for_timeout(600)
        bad = 0
        # 제출 전에는 결과가 비어 있어야 한다
        assert await pg.inner_text('#examres') == ''
        # 정답
        await pg.check('input[name=eq1][value=b]'); await pg.fill('#ex2', '−2'); 
        for k, v in zip('abcd', '3114'): await pg.fill('#ex3' + k, v)
        await pg.check('input[name=eq4][value=c]'); await pg.check('input[name=eq5][value=a]')
        await pg.click('#examgo'); s1 = await pg.inner_text('#examres .score')
        print('정답 제출:', s1); bad += '4 / 4' not in s1 or '보너스 1' not in s1
        # 흔한 오답 (가운데 0.5를 더함 → 4.5, 평균 풀링)
        await pg.click('#examreset'); await pg.fill('#ex2', '4.5')
        for k, v in zip('abcd', ['1.5', '0.25', '0.25', '1.5']): await pg.fill('#ex3' + k, v)
        await pg.click('#examgo'); s2 = await pg.inner_text('#examres .score'); t2 = await pg.inner_text('#examres')
        print('오답 제출:', s2); bad += '0 / 4' not in s2 or '흔한 실수' not in t2
        print('박사:', await pg.inner_text('#examsay p'))
        # 대결
        await pg.click('#duelbox .run'); v = await pg.inner_text('#duelbox .vtext'); print('대결:', v[:30]); bad += '초파리' not in v
        await pg.click('#duel .shsel[data-v=right2]'); await pg.click('#duelbox .run'); print('대결 2픽셀:', await pg.inner_text('#duelbox .vreport'))
        # 자리 71번
        await pg.click('#go71'); await pg.wait_for_timeout(500); k = await pg.inner_text('#k2b'); print('자리 71번 합:', k); bad += k != '-3.0'
        # 부품 판정: 뒤섞인 고양이
        await pg.click('#p4b .imgsel[data-v=scrambled]'); a, c = await pg.inner_text('#k4d'), await pg.inner_text('#k4e'); print('뒤섞인 고양이:', a, c); bad += not (a == '고양이!' and c == '아님')
        print('페이지 오류:', errs); bad += len(errs)
        await b.close()
        print('결과:', '통과' if not bad else '실패 %d' % bad)
        raise SystemExit(1 if bad else 0)

asyncio.run(main())
