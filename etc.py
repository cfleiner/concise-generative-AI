import os
from datetime import datetime, timedelta
from typing import List

def get_filename(name: str) -> str:
    now = datetime.now()
    return f'output/{name}{now.strftime("_%Y%m%d_%H%M%S")}.wav'

def time_it(func):
    def time_wrapper():
        start_time = datetime.now()
        func()
        diff  = datetime.now() - start_time
        diff -= timedelta(microseconds=diff.microseconds)
        print(f'Program has finished after "{diff}"!')
    set_environ()
    return time_wrapper

def set_environ() -> None:
    os.environ["TTS_HOME"] = '.'
    os.environ["XDG_DATA_HOME"] = '.'
