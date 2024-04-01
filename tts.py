import torch
from TTS.api import TTS

from etc import get_filename, time_it

TEXT  = "The single speaker model supports only one language!"
MODEL = 'tts_models/en/ljspeech/tacotron2-DDC'
LANG  = MODEL.split('/')[1]

@time_it
def text_to_speech_single() -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model_name=MODEL).to(device)
    tts.tts_to_file(text=TEXT,
                    file_path=get_filename('tts_' + LANG))
    
if __name__ == '__main__':
    text_to_speech_single()