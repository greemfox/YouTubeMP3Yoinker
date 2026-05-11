from pytubefix import Stream, YouTube
from pydub import AudioSegment
import os
import shutil


def read_urls():
    urls = []
    try:
        with open("urls.txt", "r") as f:
            for line in f:
                urls.append(line)
    except FileNotFoundError:
        print("Error: urls.txt was not found")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return urls


def download_progress(stream, _, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Download: {round(pct_completed, 2)}% complete")


def convert_audio(input_path, output_path):
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="mp3")
        print("Successfully converted m4a to mp3")
    except Exception as e:
        print(f"Error converting audio: {e}")


def download_and_convert(urls: list[str]):
    if urls:
        for url in urls:
            vid = YouTube(url, on_progress_callback=download_progress)
            vid_title = vid.title
            print(f"Title: {vid_title}")

            audio_track: Stream = vid.streams.filter(only_audio=True).last()
            print(f"Audio track found!\nSize: {audio_track.filesize_approx}")
            m4a_path = audio_track.download(output_path="m4a")
            if m4a_path:
                os.makedirs(name="mp3", exist_ok=True)
                mp3_path = m4a_path.replace("m4a", "mp3")
                convert_audio(m4a_path, mp3_path)
            else:
                print(f"{audio_track.title} download skipped or failed")
    else:
        print("Check urls.txt again")


def main():
    download_and_convert(read_urls())
    shutil.rmtree("m4a")
    with open("urls.txt", "w") as f:
        f.write("")
    os.startfile("mp3")


if __name__ == "__main__":
    main()
