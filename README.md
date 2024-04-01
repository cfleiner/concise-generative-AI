# Concise Generative AI
This repository contains a collection of code snippets to demonstrate simple applications of popular libraries and projects of generative AI.

The target audience of this repository are Windows users who want to try out different genAI techniques, but are overwhelmed by GUIs with dozens of manual configuration inputs.

- [Concise Generative AI](#concise-generative-ai)
  - [Technical Setup](#technical-setup)
    - [Hardware](#hardware)
    - [Software](#software)
  - [General Preparation](#general-preparation)
  - [Applications](#applications)
    - [Text-To-Speech with Single Speaker Model](#text-to-speech-with-single-speaker-model)
    - [Text-To-Speech with Cloned Voice](#text-to-speech-with-cloned-voice)
    - [Swap Voices](#swap-voices)
    - [Swap Voices (in Songs)](#swap-voices-in-songs)
    - [Animate Speaker](#animate-speaker)
      - [Troubleshooting](#troubleshooting)
  - [References](#references)

## Technical Setup
The code was tested with the technical setup listed below. I might not be able to help out, if errors are raised in a deviating setup.

### Hardware
* Intel(R) Core(TM) i5-8400 CPU @ 2.80GHz
* RAM 12 GB
* 25 GB free space on SSD hard drive
* NVIDIA GeForce GTX 1060 6GB / Driver Version: 535.98

### Software
* Windows 11 Home / Version: 23H2
* Python 3.10.6
* Pip 24.0
* Wheel 0.43.0
* PyTorch 2.2.2+cu121


## General Preparation
0. Open your preferred console. I am using Powershell 5.1 (press WIN + R and type "powershell").
   
1. Download the project as archive or via git:
```
git clone https://github.com/cfleiner/concise-generative-AI.git genAI
```

2. Download the FFmpeg Essential Build Archive from the [download site](https://www.gyan.dev/ffmpeg/builds/). Unzip the archive and move _ffmpeg.exe_ and _ffprobe.exe_ to the project folder. FFmpeg is the open-source tool of choice when it comes to video and audio editing and is required by many genAI projects. It will also come in handy to prepare your input files.

3. Change the directory of your console to the project folder and create a virtual environment for Python. After creation, activate it.
```
cd genAI
python -m venv venv
venv/scripts/activate
```

4. Install PyTorch with CUDA support
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

5. Install Coqui.ai's [TTS](https://github.com/coqui-ai/TTS) library for advanced Text-to-Speech generation
```
pip install TTS
```

In case the Pypi package is outdated and raises unexpected errors you are not able to solve, you can also download the library directly from GitHub:
```
pip install https://github.com/coqui-ai/TTS/archive/refs/heads/dev.zip
```

## Applications

### Text-To-Speech with Single Speaker Model
The TTS library references many pre-trained speech models that can be used out of the box to synthesize utterances from text. The code snippet is in file _tts.py_. Change the value of global variable ```TEXT``` to your needs. Single speaker models support only one language. If you want an utterance other than in English, you need to use another model. Note that models must be downloaded first and are not contained in the library itself. The program automatically downloads the model after you have agreed to the non-commercial license. Models are stored in folder ```TTS```.

```
python tts.py
```
The file is saved in folder ```output``` with the filename pattern ```tts_{language}_{timestamp}```.

### Text-To-Speech with Cloned Voice
Text-To-Speech with a cloned voice means that you define text that must be uttered (equal to tts.py), but additionally you must also provide a voice recording as input. Record your voice or take an existing recording, copy it to the input folder, and change the global variables ```TEXT, LANG, INPUTFILE``` in file _tts_clone.py_ accordingly. The code snippet uses a multilingual model. The utterances from the voice recording do not have to be in the same language as you defined in ```LANG```.  

```
python tts_clone.py
```
The file is saved in folder ```output``` with the filename pattern ```tts_clone_{language}_{timestamp}```.

Voice recordings between 5 and 30 seconds are enough and the model will not overwhelm the GPU. You can use FFmpeg to extract an audio slice from a longer recording. The following example extracts a 15 seconds audio slice from ```long_recording.wav``` and saves it as ```output.wav```.
```
./ffmpeg.exe -i {long_recording.wav} -ss {00:30} -to {00:45} -c:a copy {output.wav}
```

Note that not all languages are directly supported. To use Japanese, you need to install a dictionary and a Romaji parser. 
```
pip install cutlet
pip install fugashi[unidic]
python -m unidic download
```

### Swap Voices
Another form of voice cloning is to swap the voice in an audio file with the voice of another recording. The utterance remains the same of the source recording (```CURRENT_VOICE_FILE```), but the habit of speech of the utterance will be from the target recording (```NEW_VOICE_FILE```). Change the global variables accordingly in file _swap_voice.py_.

```
python swap_voice.py
```
The file is saved in folder ```output``` with the filename pattern ```swap_voice_{timestamp}```.

### Swap Voices (in Songs)
The simple form of voice swapping considers recordings without background noise/music. Swapping the singer's voice in a music song follows the same principle, but voice and background must be separated and at the end merged. A popular library to achieve this is [Spleeter](https://github.com/deezer/spleeter). Spleeter uses TensorFlow instead of PyTorch. Thus, you should not use Spleeter in this project, but you can create a new one for that. A great alternative is the [Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui).

After you have separated the singer's voice from the background music, you can swap voices. After you have your swap voiced file, you can merge it with the background music using FFmpeg.

```
./ffmpeg.exe -i {background_music.wav} -i {swapped_voice.wav} -c:a copy {output.wav}
```

### Animate Speaker
After we have considered all audio scenarios, it is time to move to visual manipulations. We will use [SadTalker](https://github.com/OpenTalker/SadTalker) to generate head and lip movements from a portrait image that adapts to the utterances of a voice recording. First, we need to download the repository and install missing packages.

```
cd genAI
git clone https://github.com/OpenTalker/SadTalker.git
pip install -r SadTalker/requirements.txt
```

Change the global variables in file _animate_speaker.py_ before you start. The program will first download required models which will be saved in folder _checkpoints_ and _gfpgan_. Make also sure to use a short ```SOURCE_AUDIO``` file because the computation time is quite longer compared to the programs before.

```
python animate_speaker.py
```
The file is saved in folder ```output``` with the filename pattern ```{dotted timestamp}.mp4```.

#### Troubleshooting
ML projects in general are quite sensitive when it comes to package versions they use. As a result, it is sometimes not trivial, if we want to having multiple third-party ML projects in the same virtual environment. Also in this case, we need to make some tweaks to make it work:
* Dependency issues of graphical packages like Gradio can be ignored because we will not use the GUI
* _No module named 'torchvision.transforms.functional\_tensor'_ can be solved by renaming the line _from torchvision.transforms.functional\_tensor import rgb\_to\_grayscale_ to _from torchvision.transforms.functional import rgb\_to\_grayscale_.
* _FileNotFoundError: [Errno 2] No such file or directory: '{UUID}.mp4'_ is caused by a missing FFmpeg.exe file.
* _OpenCV: FFMPEG: tag 0x5634504d/'MP4V' is not supported with codec id 12 and format 'mp4 / MP4 (MPEG-4 Part 14)'_ can be solved by replacing _cv2.VideoWriter\_fourcc(*'mp4v')_ with _cv2.VideoWriter\_fourcc('m', 'p', '4', 'v')_.
* _Invalid SOS parameters for sequential JPEG_ can be ignored. It seems to be an issue with Samsung photos, but does not effect the program outcome.




## References
At last, you might wondering why I did not include a text-to-image generation code snippet with StableDiffusion. The reason is that generated images need always post-processing using a canvas feature or iterations in general. Using a GUI for that is imperative. In the following, I will reference some great GUIs for genAI applications:
* Automatic1111's [Stable Diffusion web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) is a great tool that supports many plugins. For instance, a plugin for [SadTalker](https://github.com/OpenTalker/SadTalker) is provided. However, also here some tweaks must be done to make SadTalker work.
* [XTTS-2-UI](https://github.com/BoltzmannEntropy/xtts2-ui) provides a simple GUI for the xtts2 model that we have used to clone voices.
* [Text generation web UI](https://github.com/oobabooga/text-generation-webui) aims to be a central GUI for text generation with plugin support.
* [SoftVC VITS Singing Voice Conversion Fork](https://github.com/voicepaw/so-vits-svc-fork) supports real-time voice conversion.
* [Ultimate Vocal Remover GUI v5.6](https://github.com/Anjok07/ultimatevocalremovergui) can be used to separate the vocal track from the instrumental track of any song. 
