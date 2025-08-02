import re
from typing import List, Dict, Any, Optional
from llm_endpoint import call_model_single
from video_cache import VideoCache

class VideoDetailBot:
    
    def __init__(self):
        self.cache = VideoCache()
        self.current_video_data = None
        self.chat_history = []
        
        self.detail_triggers = [
            "explain", "detail", "more about", "elaborate", "tell me about",
            "what does", "how does", "why", "expand on", "clarify",
            "describe", "breakdown", "go deeper", "more info"
        ]
        
        self.part_indicators = [
            "beginning", "start", "intro", "introduction",
            "middle", "end", "conclusion", "summary",
            "first part", "second part", "last part",
            "when they talk about", "the section about",
            "minute", "timestamp", "time"
        ]
    
    def load_video(self, video_url: str, transcript: str = None, summary: str = None, chunks: List[str] = None):
        
        cached_data = self.cache.load_video_data(video_url)
        
        if cached_data:
            self.current_video_data = cached_data
            self.chat_history = self.cache.load_chat_history(video_url)
            print("Video loaded from cache. You can now ask detailed questions!")
        else:
            if transcript and summary:
                self.current_video_data = {
                    "url": video_url,
                    "transcript": transcript,
                    "summary": summary,
                    "chunks": chunks or [],
                    "transcript_length": len(transcript)
                }
                self.cache.save_video_data(video_url, transcript, summary, chunks)
                self.chat_history = []
                print("Video cached. You can now ask detailed questions!")
            else:
                print("No video data available")
                return False
        
        return True
    
    def should_activate_ai(self, user_input: str) -> bool:
        
        user_input_lower = user_input.lower()
        
        has_detail_trigger = any(trigger in user_input_lower for trigger in self.detail_triggers)
        
        question_starters = ["what", "how", "why", "when", "where", "who", "which"]
        starts_with_question = any(user_input_lower.startswith(q) for q in question_starters)
        
        has_question_mark = "?" in user_input
        
        return has_detail_trigger or starts_with_question or has_question_mark
    
    def find_relevant_parts(self, query: str) -> str:
        
        if not self.current_video_data:
            return "No video loaded"
        
        transcript = self.current_video_data["transcript"]
        chunks = self.current_video_data.get("chunks", [])
        
        query_words = query.lower().split()
        relevant_sections = []
        
        search_sections = chunks if chunks else [transcript]
        
        for i, section in enumerate(search_sections):
            section_lower = section.lower()
            
            matches = sum(1 for word in query_words if word in section_lower)
            
            if matches > 0:
                relevant_sections.append({
                    "section": section,
                    "matches": matches,
                    "index": i
                })
        
        relevant_sections.sort(key=lambda x: x["matches"], reverse=True)
        
        if relevant_sections:
            top_sections = relevant_sections[:3]
            context = "\\n\\n".join([f"Section {s['index'] + 1}: {s['section']}" for s in top_sections])
            return context
        else:
            summary = self.current_video_data["summary"]
            transcript_preview = transcript[:2000] + "..." if len(transcript) > 2000 else transcript
            return f"Summary: {summary}\\n\\nTranscript Preview: {transcript_preview}"
    
    def get_detailed_explanation(self, user_query: str) -> str:
        
        if not self.current_video_data:
            return "Please load a video first before asking questions."
        
        relevant_context = self.find_relevant_parts(user_query)
        
        system_prompt = f"""
You are a helpful assistant that provides detailed explanations about YouTube videos.

The user is asking about a specific part or topic from a video. Here's the relevant context from the video:

{relevant_context}

User's question: {user_query}

Provide a detailed, helpful explanation that directly answers their question based on the video content.
If the question is about something not covered in the video, say so clearly.
Be conversational and helpful, but stick to what's actually in the video.
"""
        
        result = call_model_single(user_query, system_prompt)
        
        if "error" in result:
            return f"Sorry, I couldn't process your question: {result['error']}"
        
        if "choices" in result and len(result["choices"]) > 0:
            response = result["choices"][0]["message"]["content"]
            
            self.chat_history.append({
                "user": user_query,
                "assistant": response,
                "timestamp": str(datetime.now())
            })
            
            if self.current_video_data:
                self.cache.save_chat_history(self.current_video_data["url"], self.chat_history)
            
            return response
        else:
            return "Sorry, I couldn't generate a response."
    
    def handle_user_input(self, user_input: str) -> str:
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            return "chat_exit"
        
        return self.get_detailed_explanation(user_input)
    
from datetime import datetime
