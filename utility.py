from sqlalchemy import Engine
from sqlmodel import SQLModel, Session
import yt_dlp.YoutubeDL as ydl
import glob
import os
import sys
from loguru import logger
import json 
from urllib import parse
from pathlib import Path

from models.audio import Audio



def check_url(url:str) -> bool:
    if parse.urlsplit(url).netloc == 'www.youtube.com':
        return True
    else:
        return False

def extract_info_for_online_media(input_url) -> dict|None:
    extracted_info = None
    
    with ydl({"quiet": True}) as ydl_instance:
        extracted_info = ydl_instance.extract_info(input_url, download=False)

    return extracted_info

def get_info(info:dict[str,str|int|list]) -> dict[str,str|int|list]:
    
    title = info['title'].split('-')
    artist = None 
    song = None 

    if(len(title) == 2):
        artist, song = title
    
    return {
        'url': info['webpage_url'],
        'name_artist':artist.strip() if artist else None,
        'name_song':song.strip() if song else None,
        'full_title':info['title'],
        'duration':info['duration'],
        'channel':info['channel'],
        # 'categories':info['categories'],
    }

def create_dirs(path:str|Path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_video(logger, url:str, path_folder:str, output_filename_no_extension:str) -> str|None:
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

def convert_to_wav(logger, path_input_filename) -> Path|None:
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
    path_file = Path(path_input_filename)
    path_output = f"{(path_file.parent).joinpath(path_file.stem)}" + ".wav"
    logger.info(f"Converting input media to audio WAV file")
    # Path to the Windows PyInstaller frozen bundled ffmpeg.exe, or the system-installed FFmpeg binary on Mac/Linux
    ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg.exe") if getattr(sys, "frozen", False) else "ffmpeg"
    ffmpeg_base_command = f"{ffmpeg_path} -hide_banner -nostats"
    ffmpeg_command = f'{ffmpeg_base_command} -n -i "{path_input_filename}" "{path_output}"'
    logger.debug(f"Running command: {ffmpeg_command}")
    os.system(ffmpeg_command)
    return Path(path_output)

def init_db(engine, name_file, DATABASE_URL:str):
    # Check if the database file exists
    db_exists = os.path.exists(name_file)

    # Create tables only if they don't exist
    if not db_exists:
        logger.info("Initializing database...")
        SQLModel.metadata.create_all(engine)

        path_file = Path('./db/audio/Mitski - Washing machine heart (slowed)/Mitski - Washing machine heart (slowed).wav')

        audio_data = Audio(
            id=1,
            name_artist="Mitski",
            name_song="Washing machine heart (slowed)",
            full_title="Mitski - Washing machine heart (slowed)",
            duration=157,
            channel="Kawwko",
            url="https://www.youtube.com/watch?v=WrpwegGf75Q",
            file_path=str(path_file),
        )

        with Session(engine) as session:
            session.add(audio_data)
            session.commit()
    else:
        logger.info("Database already exists, skipping initialization.")

def get_audio_info(url) -> Audio:
    extracted_info = extract_info_for_online_media(url)
    audio_info = get_info(extracted_info)
    audio = Audio(**audio_info)
    return audio

def download_audio(logger, url:str, path_to_folder:Path, output_filename_no_extension:str) -> Path:
    create_dirs(path_to_folder)
    path_or_name = download_video(logger,url,path_to_folder,output_filename_no_extension)
    return Path(path_or_name)


def main():
    url = "https://www.youtube.com/watch?v=3Ngzk9h247I"
    
    if(check_url(url)):
        logger.debug(f"Download Info from url: {url}")
        audio = get_audio_info(url)
        
        path_downloaded_file = download_audio(logger,url,Path("./tmp/dumps/audio"), audio.full_title)
        path_file = convert_to_wav(logger,path_downloaded_file)
        logger.debug(f"Path-audio {path_file}")

    #     audio_info = get_info(extracted_info)
    #     audio = Audio(**audio_info)
    # print(audio)

    # split_url = parse.urlsplit(url)
    # print(split_url)
    
    # urls = [
    #     'https://www.youtube.com/watch?v=D4jguVJ2ldY',
    #     'https://www.youtube.com/watch?v=UD4jRK5j2Ow',
    #     'https://www.youtube.com/watch?v=8FSpGs7W5wY',
    #     'https://www.youtube.com/watch?v=2Kt8HP1VEPU',
    #     'https://www.youtube.com/watch?v=-loJ3JJ6hIA'
    # ]

    # for url in urls:
    #     if check_url(url):
    #         data = extract_info_for_online_media(logger,url)
    #         audio_info = get_info(data)




if __name__ == "__main__":
    main()

