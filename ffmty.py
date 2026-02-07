import os
import sys
import datetime
import subprocess
import time
import configparser
import timestamps
import subprocess
from tk_file_dialog import  CreateFileDialog_Open, CreateFileDialog_OpenFolder, CreateFileDialog_SaveToFolder

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.abspath(".")

config = configparser.ConfigParser()
config['Settings'] =    {'Codec': 'h264',
                         'Presset': 'fast'}


#usr_path = input("Enter path there:\n")
def check_ffmpeg():
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True
        )
        print("FFmpeg detected:", result.stdout.splitlines()[0])
    except FileNotFoundError:
        print("FFmpeg is not found. Exit")
        sys.exit(0)

check_ffmpeg()

usr_path = CreateFileDialog_OpenFolder()

if not usr_path:
    print("Folder selection cancelled.")
    sys.exit(0)

usr_path = os.path.abspath(usr_path)
selected_folder = os.path.basename(usr_path)

filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

output_folder = os.path.join(base_path, "ffmty/output")
render_folder = os.path.join(base_path, "ffmty/render")

os.makedirs(output_folder, exist_ok=True)
os.makedirs(render_folder, exist_ok=True)

config_path = os.path.join(base_path, "ffmty/settings.ini")
list_path = os.path.join(base_path, f"ffmty/output/list_{selected_folder}_{filename}.txt")
mp3_output = os.path.join(base_path, f"ffmty/render/{selected_folder}_{filename}.mp3")
video_output = os.path.join(base_path, f"ffmty/render/{selected_folder}_{filename}.mp4")
timestamps_path = os.path.join(base_path, f"ffmty/output/timestamps_{selected_folder}_{filename}.txt")
image = os.path.join(base_path, "ffmty/0.png")


if os.path.isfile(config_path):
    print("Config file detected.")
else:
    print("No config file. Creating...")
    with open(config_path, "w") as configfile:
        configfile.write("# Image in execute folder with name 0.png will be used as image cover if you want this.\n")
        configfile.write("# Codecs: h264 h265 h264_nvenc h265_nvenc mpeg4 av1\n")
        configfile.write("# Pressets: ultrafast fast medium slow veryslow\n")
        config.write(configfile)

config.read(config_path)

codec_ = config.get("Settings", "Codec")
presset_ = config.get("Settings", "Presset")
mp3_files = []

codec = "h264"
presset = "fast"

if codec_ is not None:
    codec = codec_
    presset = presset_

print(f"\nCodec: {codec}\nPresset: {presset}")

def all_mp3_files():

    path = usr_path

    if len(sys.argv) > 1:
        path = sys.argv[1]

    print("Directory:", path)

    directory = os.listdir(os.path.abspath(path))
    found = False
    print("\nFounded files:")
    for file in directory:
        if file.lower().endswith(".mp3"):
            mp3_files.append(file)

            print(file)
            found = True

    if found == False:
        print("There no .mp3 files.\n")
        a = input("Press Enter to exit...")
        if a:
            sys.exit(0)

def create_mp3():
    all_mp3_files()
    #list_path = os.path.join(usr_path, f"list_{filename}.txt")
    with open(list_path, "w", encoding="utf-8") as f:
        for file in mp3_files:
            nf = os.path.join(usr_path, file)
            f.write(f"file '{os.path.abspath(nf)}'\n")

    timestamps.create_timestamps(list_path, filename, base_path, timestamps_path)
    time.sleep(2)
    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        mp3_output
    ], encoding="utf-8", check=True)

def create_video(image):
    max_seconds = 12 * 3599

    total_seconds = int(timestamps.overall_duration)
    #print(total_seconds)

    parts = (total_seconds + max_seconds - 1) // max_seconds
    if parts > 1:
        print("Video is longer than 12 hours. Separating into two parts")

    for i in range(parts):
        start = i * max_seconds
        duration = min(max_seconds, total_seconds - start)

        output = video_output.replace(".mp4", f"_part{i+1}.mp4")
    #    print(duration, parts)

        subprocess.run([
            "ffmpeg",
            "-y",
            "-ss", str(start),
            "-t", str(duration),
            "-loop", "1",
            "-i", image,
            "-i", mp3_output,
            "-c:a", "copy",
            "-c:v", codec,
            "-preset", presset,
            "-shortest",
            "-vf",
            "scale=1920:1080:force_original_aspect_ratio=decrease,"
            "pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
            output
        ], encoding="utf-8", check=True)

        print(f"Video part {i+1} done: {output}")
    print(f"Video is done.")


if __name__ == "__main__":
    create_mp3()
    usr_input = input("Do you want to make video now? \n1/y - Yes\n2/n - No\n")
    if usr_input == "1" or "y":
        if not os.path.exists(image):
            print("0.png is not found. Please select image.")
            time.sleep(2)
            #usr_input2 = input("Drag image cover here, then press enter.\n").strip()
            usr_input2 = CreateFileDialog_Open()
            image = usr_input2
        else:
            print("0.png in this folder will be used as cover.")
            time.sleep(2)

        create_video(image)

    print("Done.")
