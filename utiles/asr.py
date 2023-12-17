#
# Install with pip install git+https://github.com/openai/whisper.git 
#
import whisper
import os
from whisper.utils import get_writer
from typing import Iterator, TextIO
import torch

print('Torch cuda available:', torch.cuda.is_available() )

# Model options:
# Size      Params   vRAM   Relative Speed
#
# tiny      39M      1Gb    32x
# base      74M      1Gb    16x
# small     244M     2Gb     6x
# medium    769M     5Gb     2x
# large-v3  1550M    10Gb    1x

#With GPU capable
model  = whisper.load_model("medium", device="cuda:0")

#Without CPU capable
#model  = whisper.load_model("tiny")

filename   = 'EP12'
language   = 'es'

#Linux
fileloc    = '/mnt/c/Temp/R2_EPISODIO_43_CULTO_LOST_IN_TRANSLATION.mp3'
output_dir = '/mnt/c/Temp'

def srt_format_timestamp(seconds: float):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    return (f"{hours}:") + f"{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def write_srt(transcript: Iterator[dict], file: TextIO):
    count = 0
    for segment in transcript:
        count +=1
        print(
            f"{count}\n"
            f"{srt_format_timestamp(segment['start'])} --> {srt_format_timestamp(segment['end'])}\n"
            f"{segment['text'].replace('-->', '->').strip()}\n",
            file=file,
            flush=True,
        )
        
#Linux
result = model.transcribe(fileloc, verbose=True, language=language)

#Windows CPU
#result = model.transcribe(fileloc, verbose=True, language=language, fp16=False)

# save TXT
# with open(os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt"), "w") as txt:
#       print(result["text"], file=txt)

# save VTT
# with open(os.path.join(output_dir, os.path.splitext(filename)[0] + ".vtt"), "w") as vtt:
#       write_vtt(result["segments"], file=vtt)

# save SRT
with open(os.path.join(output_dir, os.path.splitext(filename)[0] + f".{language}.srt"), "w") as srt:
        write_srt(result["segments"], file=srt)