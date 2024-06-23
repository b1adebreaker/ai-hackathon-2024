import json
import os
from pytube import YouTube

SAVE_PATH = "downloaded_videos/"
OUTPUT_JSON = "video_paths.json"

# Ensure the save path directory exists
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

def download_video(youtube_url):
    """
    Downloads a video from a given YouTube URL and saves it to the specified directory.
    """
    try:
        yt = YouTube(youtube_url)
        video = yt.streams.filter(file_extension='mp4').first()
        if video:
            downloaded_file_path = video.download(output_path=SAVE_PATH)
            return downloaded_file_path
        else:
            print(f"No suitable mp4 stream found for {youtube_url}")
            return None
    except Exception as e:
        print(f"Error downloading video from {youtube_url}: {e}")
        return None

def process_json_data(data):
    """
    Processes the JSON data to extract YouTube links, download the videos, 
    and prepare the output data in the specified format.

    Input:
    Database dump.

    Returns:
    JSON array containing the primary key, company name, 
    YouTube URL, and relative path to the downloaded video file.
    """
    output_data = []

    for item in data:
        if item['model'] == 'ai_hackathon_api.company':
            company_name = item['fields']['name']
            youtube_url = item['fields']['youtube_url']
            pk = item['pk']
            
            video_path = download_video(youtube_url)
            if video_path:
                relative_video_path = os.path.relpath(video_path, start=os.getcwd())
                output_data.append({
                    "pk": pk,
                    "company_name": company_name,
                    "youtube_url": youtube_url,
                    "video_path": relative_video_path
                })

    return output_data

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(script_dir, '..', 'django', 'ai_hackathon', 'db_dump.json')
    relative_path = os.path.normpath(relative_path)  # normalizing path

    with open(relative_path, 'r') as file:
        data = json.load(file)
    
    output_data = process_json_data(data)
    
    with open(OUTPUT_JSON, 'w') as output_file:
        json.dump(output_data, output_file, indent=4)

if __name__ == "__main__":
    main()
