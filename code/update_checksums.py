"""SHA256SUMS.txt를 다시 만든다(코퍼스 없이 실행 가능).

저자명·저장소 주소처럼 공개 직전에 손으로 채우는 파일은 검사에서 뺀다.
데이터·집계·사전·코드 파일은 모두 지문으로 보증된다.
사용법: python code/update_checksums.py [저장소 경로]
"""
import hashlib, os, sys

EXCLUDE = {'SHA256SUMS.txt', 'README.md', 'CITATION.cff', 'LICENSE',
           'ontology/war_narrative.ttl'}
SKIP_DIRS = ('.git', '__pycache__', '.pytest_cache')

def write(R):
    out = []
    for root, dirs, fs in os.walk(R):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for fn in sorted(fs):
            rel = os.path.relpath(os.path.join(root, fn), R).replace(os.sep, '/')
            if rel in EXCLUDE: continue
            h = hashlib.sha256(open(os.path.join(root, fn), 'rb').read()).hexdigest()
            out.append(f"{h}  {rel}\n")
    with open(os.path.join(R, 'SHA256SUMS.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(sorted(out, key=lambda l: l.split('  ', 1)[1]))
    return len(out)

if __name__ == '__main__':
    R = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print('files:', write(R))
