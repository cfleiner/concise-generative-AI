import os
import urllib.request
from typing import List

SCRIPT = 'SadTalker/scripts/download_models.sh'

def download_models():
    content = get_lines()
    valids = keep_valids(content)
    for v in valids:
        items = v.split()
        if items[0] == 'mkdir':
            make_dir(items[-1])
            continue
        download_model(items[2], items[4])

def make_dir(path: str) -> None:
    if os.path.isdir(path): return
    os.makedirs(path)

def download_model(source: str, target: str) -> None:
    if os.path.isfile(target): return
    print(f'Downloading "{source}" ...', end='\r')
    urllib.request.urlretrieve(source, target)
    print(f'Downloading "{source}"   \u2713')

def keep_valids(lines: List[str]) -> List[str]:
    return [l for l in lines if l.startswith(('mkdir', 'wget'))]

def get_lines() -> List[str]:
    with open(SCRIPT, 'r') as f:
        return f.read().split('\n')

if __name__ == '__main__':
    download_models()