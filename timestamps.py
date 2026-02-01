# timestamps.py
from mutagen.mp3 import MP3
from datetime import timedelta
import os

def create_timestamps(list_path, filename, base_path):
    concat_file = list_path
    timestamps_path = os.path.join(base_path, f"timestamps_{filename}.txt")
    overall_duration = 0

    with open(concat_file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    mp3_files = []
    for line in lines:
        line = line.strip()
        if line.startswith("file '") and line.endswith("'"):
            mp3_files.append(line[6:-1])
        elif line.startswith('file '):
            mp3_files.append(line[5:].strip("'\""))
    print("\nTimestamps: ")
    with open(timestamps_path, "w", encoding="utf-8") as f:
        current_time = 0.0
        for mp3 in mp3_files:
            full_path = os.path.join(base_path, mp3)
            if not os.path.isfile(full_path):
                print(f"File not found: {mp3}")
                continue
            audio = MP3(full_path)
            duration = audio.info.length
            start = str(timedelta(seconds=int(current_time)))
            f.write(f"{start} {os.path.splitext(os.path.basename(mp3))[0]}\n")
            print(f"{start} {os.path.splitext(os.path.basename(mp3))[0]}")
            current_time += duration
            overall_duration += duration

    minutes = int(overall_duration // 60)
    seconds = int(overall_duration % 60)
    print(f"\nOvearall duration: {minutes} min {seconds} sec.\n")
    print(f"Timestamps list path: {timestamps_path}\n")
