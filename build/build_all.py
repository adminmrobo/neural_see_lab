# 전체 다시 만들기: 숫자(results.json) → 페이지 → 지식 색인·꾸러미 붙이기·점검 → 표지 지시문·현황 파일
import subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(H)
subprocess.check_call([sys.executable, os.path.join(ROOT, 'code', 'analysis.py')], stdout=subprocess.DEVNULL)
subprocess.check_call([sys.executable, os.path.join(H, 'p00.py')])
subprocess.check_call([sys.executable, os.path.join(H, 'kg_build.py')], stdout=subprocess.DEVNULL)
subprocess.check_call([sys.executable, os.path.join(H, 'make_docs.py')])
subprocess.check_call(['node', os.path.join(H, 'check_numbers.js')])
