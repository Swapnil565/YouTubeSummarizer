import pickle
import os
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime

class VideoCache:
    
    def __init__(self, cache_dir: str = "video_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_video_hash(self, video_url: str) -> str:
        return hashlib.md5(video_url.encode()).hexdigest()
    
    def _get_cache_path(self, video_hash: str, cache_type: str) -> str:
        return os.path.join(self.cache_dir, f"{video_hash}_{cache_type}.pkl")
    
    def save_video_data(self, video_url: str, transcript: str, summary: str, chunks: List[str] = None):
        video_hash = self._get_video_hash(video_url)
        
        video_data = {
            "url": video_url,
            "transcript": transcript,
            "summary": summary,
            "chunks": chunks or [],
            "timestamp": datetime.now().isoformat(),
            "transcript_length": len(transcript)
        }
        
        cache_path = self._get_cache_path(video_hash, "data")
        with open(cache_path, 'wb') as f:
            pickle.dump(video_data, f)
    
    def load_video_data(self, video_url: str) -> Optional[Dict]:
        video_hash = self._get_video_hash(video_url)
        cache_path = self._get_cache_path(video_hash, "data")
        
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        return None
    
    def save_chat_history(self, video_url: str, chat_history: List[Dict]):
        video_hash = self._get_video_hash(video_url)
        cache_path = self._get_cache_path(video_hash, "chat")
        
        with open(cache_path, 'wb') as f:
            pickle.dump(chat_history, f)
    
    def load_chat_history(self, video_url: str) -> List[Dict]:
        video_hash = self._get_video_hash(video_url)
        cache_path = self._get_cache_path(video_hash, "chat")
        
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        return []
    
    def is_cached(self, video_url: str) -> bool:
        return self.load_video_data(video_url) is not None
    
    def list_cached_videos(self) -> List[Dict]:
        cached_videos = []
        
        for filename in os.listdir(self.cache_dir):
            if filename.endswith("_data.pkl"):
                cache_path = os.path.join(self.cache_dir, filename)
                with open(cache_path, 'rb') as f:
                    video_data = pickle.load(f)
                    cached_videos.append({
                        "url": video_data["url"],
                        "timestamp": video_data["timestamp"],
                        "length": video_data["transcript_length"]
                    })
        
        return sorted(cached_videos, key=lambda x: x["timestamp"], reverse=True)
