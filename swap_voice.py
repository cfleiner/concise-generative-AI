import torch
from TTS.api import TTS

from etc import get_filename, time_it

CURRENT_VOICE_FILE  = 'input/your_source_recording.wav'
NEW_VOICE_FILE      = 'input/your_target_recording.wav'
MODEL = 'voice_conversion_models/multilingual/vctk/freevc24'

@time_it
def swap_voice() -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS(model_name=MODEL).to(device)
    tts.voice_conversion_to_file(source_wav=CURRENT_VOICE_FILE,
                                 target_wav=NEW_VOICE_FILE, 
                                 file_path=get_filename('swap_voice'))

if __name__ == '__main__':
    swap_voice()