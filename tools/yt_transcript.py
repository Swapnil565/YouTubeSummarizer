from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url: str) -> str:
    
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
        return video_id
    
    if "youtube.com" in url:
        if "v=" in url:
            video_id = url.split("v=")[-1].split("&")[0]
            return video_id
        elif "embed/" in url:
            video_id = url.split("embed/")[-1].split("?")[0]
            return video_id
    
    # If no pattern matches, try to extract anything that looks like a video ID
    video_id_pattern = r'([a-zA-Z0-9_-]{11})'
    match = re.search(video_id_pattern, url)
    if match:
        return match.group(1)
    
    raise ValueError(f"Could not extract video ID from URL: {url}")

def get_transcript(link: str) -> str:
    
    try:
        video_id = extract_video_id(link)
        print(f"Extracted video ID: {video_id}")
        
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        full_text = " ".join([entry.text for entry in transcript])
        
        print(f"Transcript extracted: {len(full_text)} characters")
        return full_text
        
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

def get_transcript_simple(link: str) -> str:
    
    try:
        video_id = extract_video_id(link)
        
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        full_text = " ".join([entry.text for entry in transcript])
        
        return full_text
        
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"
