import os
import sys
import datetime
import subprocess
import time
import configparser
import timestamps

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)  # путь к папке exe
else:
    base_path = os.path.abspath(".")

config = configparser.ConfigParser()
config['Settings'] =    {'Codec': 'h264',
                         'Presset': 'fast'}

filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

config_path = os.path.join(base_path, "ffmty/settings.ini")
list_path = os.path.join(base_path, f"list_{filename}.txt")
mp3_output = os.path.join(base_path, f"output_{filename}.mp3")
video_output = os.path.join(base_path, f"output_{filename}.mp4")
image = os.path.join(base_path, "0.png")
timestamps_path = os.path.join(base_path, f"timestamps_{filename}.txt")

if os.path.isfile(config_path):
    print("Config file detected.")
else:
    print("No config file. Creating...")
    os.mkdir("ffmty")
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

    path = base_path

    if len(sys.argv) > 1:
        path = sys.argv[1]

    print("Directory:", path)

    directory = os.listdir(os.path.abspath(path))
    found = False
    print("\nFounded files:")
    for file in directory:
        if file.lower().endswith(".mp3"):
            mp3_files.append(file)
            #print(directory_files)

            print(file)
            found = True

    if found == False:
        print("There no .mp3 files.")
        a = input("Press Enter to exit...")
        if a:
            sys.exit(0)

def create_mp3():
    all_mp3_files()

    with open(list_path, "w", encoding="utf-8") as f:
        for file in mp3_files:
            f.write(f"file '{file}'\n")

    timestamps.create_timestamps(list_path, filename, base_path)

    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        mp3_output
    ], check=True)

def create_video(image):
    subprocess.run([
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", image,
        "-i", mp3_output,
        "-c:a", "copy",
        "-c:v", codec,
        "-preset", presset,
        "-shortest",
        video_output
    ], check=True)

    print(f"Video is done: {video_output}")


if __name__ == "__main__":
    create_mp3()
    usr_input = input("Do you want to make video now? \n1 - Yes\n2 - No\n")
    if usr_input == "1":
        if not os.path.exists(image):
            print("0.png is not found.")
            usr_input2 = input("Drag image cover here, then press enter.\n").strip()
            image = usr_input2
        else:
            print("0.png in this folder will be used as cover.")
            time.sleep(2)

        create_video(image)

    print("Done.")
