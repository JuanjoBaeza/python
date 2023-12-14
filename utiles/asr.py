import whisper
from whisper.utils import get_writer
import os

#model = whisper.load_model("large-v3")
model = whisper.load_model("base")

output_dir = '/mnt/c/Temp'
filename   = 'EP09'
language   = 'es'
fileloc    = 'https://www.cumlingus.com/wp-content/uploads/podcasts/R2_EPISODIO_09_MONOGRAFICO_CINE_RURAL_CONTEMPORANEO_ESPAÑOL.mp3'

from typing import Iterator, TextIO

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

result = model.transcribe(fileloc, verbose=True, language=language)
  
# save SRT
with open(os.path.join(output_dir, os.path.splitext(filename)[0] + f".{language}.srt"), "w") as srt:
        write_srt(result["segments"], file=srt)