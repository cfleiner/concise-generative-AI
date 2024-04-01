import torch
from TTS.api import TTS

from etc import get_filename, time_it

TEXT, LANG  = "A multilingual model is used for voice cloning!", 'en'
INPUT_FILE  = 'input/your_input_file.wav'
MODEL       = 'tts_models/multilingual/multi-dataset/xtts_v2'

@time_it
def text_to_speech_cloned() -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model_name=MODEL).to(device)
    tts.tts_to_file(text=TEXT, 
                    speaker_wav=INPUT_FILE, 
                    language=LANG, 
                    file_path=get_filename('tts_clone_' + LANG))
    
if __name__ == '__main__':
    text_to_speech_cloned()