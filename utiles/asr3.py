import whisper
from whisper.utils import get_writer

filename = "antesdecristo.mp3"
input_directory  = "/tmp"
output_directory = "/tmp"
input_file = f"{input_directory}/{filename}"

model = whisper.load_model("medium") # or whatever model you prefer
result = model.transcribe(input_file)

# Save as a TXT file
txt_writer = get_writer("txt", output_directory)
txt_writer(result, input_file)

# Save as an SRT file
srt_writer = get_writer("srt", output_directory)
srt_writer(result, input_file)

# Save as an VTT file
vtt_writer = get_writer("vtt", output_directory)
vtt_writer(result, input_file)

# Save as a TSV file
tsv_writer = get_writer("tsv", output_directory)
tsv_writer(result, input_file)

# Save as a JSON file
json_writer = get_writer("json", output_directory)
json_writer(result, input_file)