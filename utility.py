import yt_dlp.YoutubeDL as ydl
import glob
import os
import sys
from loguru import logger
import json 
from urllib import parse
from pathlib import Path



def check_url(url:str) -> bool:
    if parse.urlsplit(url).netloc == 'www.youtube.com':
        return True
    else:
        return False

def extract_info_for_online_media(logger, input_url=None) -> dict:
    extracted_info = {}
    
    logger.info(f"Extracting info for input_url: {input_url}")
    if input_url is not None:
        # If a URL is provided, use it to extract the metadata
        with ydl({"quiet": True}) as ydl_instance:
            extracted_info = ydl_instance.extract_info(input_url, download=False)

    return extracted_info

def get_info_artist_title(info:dict[str,str|int|list]) -> dict[str,str|int|list]:
    artist, song = info['title'].split('-')
    return {
        'name_artist':artist,
        'name_song':song,
        'full_title':info['categories'],
        'duration':info['duration'],
        'channel':info['channel'],
        'categories':info['categories'],
    }

def create_dirs(path:str):
    if not os.path.exists(path):
        os.makedirs(path)

def download_video(logger, url:str, path_folder:str, output_filename_no_extension:str):
    logger.debug(f"Downloading media from URL {url} to filename {output_filename_no_extension} + (as yet) unknown extension")
    folder_path = Path(path_folder).joinpath(output_filename_no_extension)
    full_path = folder_path.joinpath(output_filename_no_extension)
    create_dirs(folder_path)
    ydl_opts = {
        "quiet": True,
        "format": "bv*+ba/b",  # if a combined video + audio format is better than the best video-only format use the combined format
        "outtmpl": f"{full_path}.%(ext)s",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    }

    with ydl(ydl_opts) as ydl_instance:
        ydl_instance.download([url])

        # Search for the file with any extension
        downloaded_files = glob.glob( f"{full_path}.*")
        if downloaded_files:
            downloaded_file_name = downloaded_files[0]  # Assume the first match is the correct one
            logger.info(f"Download finished, returning downloaded filename: {downloaded_file_name}")
            return downloaded_file_name
        else:
            logger.error("No files found matching the download pattern.")
            return None


def convert_to_wav(logger, path_input_filename):
    """Convert input audio to WAV format, with input validation."""
    # Validate input file exists and is readable
    if not os.path.isfile(path_input_filename):
        raise Exception(f"Input audio file not found: {path_input_filename}")

    if os.path.getsize(path_input_filename) == 0:
        raise Exception(f"Input audio file is empty: {path_input_filename}")

    # Validate input file format using ffprobe
    probe_command = f'ffprobe -v error -show_entries stream=codec_type -of default=noprint_wrappers=1 "{path_input_filename}"'
    probe_output = os.popen(probe_command).read()
    logger.debug(probe_output)
    if "codec_type=audio" not in probe_output:
        raise Exception(f"No valid audio stream found in file: {path_input_filename}")

    path_output = f"{path_input_filename}" + ".wav"
    logger.info(f"Converting input media to audio WAV file")
    # Path to the Windows PyInstaller frozen bundled ffmpeg.exe, or the system-installed FFmpeg binary on Mac/Linux
    ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg.exe") if getattr(sys, "frozen", False) else "ffmpeg"
    ffmpeg_base_command = f"{ffmpeg_path} -hide_banner -nostats"
    ffmpeg_command = f'{ffmpeg_base_command} -n -i "{path_input_filename}" "{path_output}"'
    logger.debug(f"Running command: {ffmpeg_command}")
    os.system(ffmpeg_command)
    return path_output


def main():
    # pass
    url = "https://www.youtube.com/watch?v=WrpwegGf75Q"
    split_url = parse.urlsplit(url)
    print(split_url)
    

    # print(download_video(logger,'https://www.youtube.com/watch?v=WrpwegGf75Q','./db/audio/','Mitski - Washing machine heart (slowed)'))
    # print(Path("./db/audio"))
    convert_to_wav(logger,'db\\audio\Mitski - Washing machine heart (slowed)\Mitski - Washing machine heart (slowed).webm')
    # data = extract_info_for_online_media(logger,input_url='https://www.youtube.com/watch?v=WrpwegGf75Q')
    # print(get_info_artist_title(data))
    # json_string = json.dumps(data,indent=4)
    # print(json_string)
    # with open("data_artist.json", "w") as file:
    #     json.dump(data, file,indent=4)


if __name__ == "__main__":
    main()

