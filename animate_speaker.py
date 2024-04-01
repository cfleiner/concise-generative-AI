import subprocess
import sys

from download_models import download_models
from etc import time_it

SOURCE_AUDIO = 'input/your_source_audio.wav'
SOURCE_IMG   = 'input/your_source_image.jpg'
SADTALKER_FOLDER = 'SadTalker'
SCRIPT = f'{SADTALKER_FOLDER}/scripts/download_models.sh'
VENV_PYTHON = 'venv/Scripts/python.exe'

@time_it
def animate_speaker() -> str:
    cmd = ' '.join([VENV_PYTHON, 
            f'{SADTALKER_FOLDER}/inference.py',
            '--driven_audio', SOURCE_AUDIO,
            '--source_image', SOURCE_IMG,
            '--result_dir', './output',
            '--checkpoint_dir', './checkpoints',
            '--bfm_folder', './checkpoints/BFM_Fitting/',
            '--still',
            '--preprocess', 'full',
            '--enhancer', 'gfpgan'])
    run_subprocess(cmd)

def run_subprocess(cmd: str) -> None:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for c in iter(lambda: process.stdout.read(1), b""):
        sys.stdout.buffer.write(c)

if __name__ == '__main__':
    download_models()
    animate_speaker()

