from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
from pytubefix.exceptions import RegexMatchError


def VideoDownload():
    url = input("Enter the YouTube video URL: ")

    # Exiting if no URL is provided
    if not url:
        exit()

    # Checking URL validity
    try:
        yt = YouTube(url, on_progress_callback = on_progress) # Displays the progress bar
    except RegexMatchError:
        print("Invalid YouTube URL. Please check the URL and try again.")
        exit()


    # Listing available streams
    print("Available streams:")
    counter = 1
    streams_list = []
    for stream in yt.streams:
        if stream.codecs == ["vp9"]: # Filtring codecs
            print(f"{counter}: {stream.resolution} - {stream.filesize / (1024 * 1024):.2f} MB")
            streams_list.append(stream)
            counter += 1

    # Getting chosen stream
    stream_index = int(input("Enter the stream number to download: ")) - 1 # Minus 1 because 0-index sucks
    selected_stream = streams_list[stream_index]
    path = input("Enter the download path (leave empty for current directory): ")
    # Checking if path is empty
    if not path:
        path = "."

    # Downloading the video
    print("Downloading...")
    selected_stream.download(output_path=path)
    print("Download completed!")


def PlaylistDownload():
    url = input("Enter the YouTube playlist URL: ")

    # Exiting if no URL provided
    if not url:
        exit()

    # Checking URL validity
    try:
        pl = Playlist(url)
    except RegexMatchError:
        print("Invalid YouTube playlist URL. Please check the URL and try again.")
        exit()

    print("Choose quality:")
    print("1. 1080p")
    print("2. 720p")
    print("3. 480p")
    print("4. 360p")
    quality_choice = input("Enter your choice [1-4]: ")
    quality_map = {
        "1": "1080p",
        "2": "720p",
        "3": "480p",
        "4": "360p"
    }
    if quality_choice not in quality_map:
        print("Invalid choice. Please enter a number between 1 and 4.")
        exit()
    else:
        selected_quality = quality_map[quality_choice]

    total_size = 0
    stream_list = []
    for video_url in pl.video_urls:
        video = YouTube(video_url)
        print(video_url)
        for stream in video.streams:
            if stream.resolution == selected_quality and stream.codecs == ["vp9"]:
                total_size += stream.filesize
                stream_list.append(stream)
                break
        else:
            print(f"No availabe stream found for \"{video.title}\" in {selected_quality} resolution")
    print(f"Total size of the playlist: {total_size / (1024 * 1024):.2f} MB")
    print("Confirm download? (yes/no)")
    confirmation = input().strip().lower()
    if confirmation == "yes":
        print("Download will proceed")
    elif confirmation == "no":
        print("Download cancelled.")
        exit()
    else:
        print("Invalid choice")
        exit()

    path = input("Enter the download path (leave empty for current directory): ")
    # Checking if path is empty
    if not path:
        path = "."
    
    counter = 1
    for stream in stream_list:
        print(f"downloading video {counter} of {len(stream_list)}")
        try:
            stream.download(output_path=path)
        except Exception as e:
            print(f"Error downloading video {counter}: {e}")
            continue
        counter += 1
    else:
        print("Your videos are ready!")


print("Welcome to the YouTube Video Downloader!")
print("Choose an option:")
print("1. Download a single video")
print("2. Download a playlist")
selection = input("Enter your choice [1/2]: ")

if selection == "1":
    VideoDownload()
elif selection == "2":
    PlaylistDownload()
else:
    print("Invalid selection. Please enter 1 or 2.")
    exit()

