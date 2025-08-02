import json
from tools.yt_transcript import get_transcript_simple
from llm_endpoint import call_model, chunk_transcript
from video_chatbot import VideoDetailBot
from video_cache import VideoCache

def summarize_youtube_video(url: str, tone: str = "casual recap", use_batching: bool = True) -> tuple:
    
    print("Getting video transcript...")
    transcript = get_transcript_simple(url)
    
    if transcript.startswith("Error"):
        return f"Sorry, couldn't get the transcript: {transcript}", None, None
    
    print("Creating summary...")
    result = call_model(transcript, tone=tone, use_batching=use_batching)
    
    if "error" in result:
        return f"Sorry, couldn't create summary: {result['error']}", None, None
    
    if "choices" in result and len(result["choices"]) > 0:
        summary = result["choices"][0]["message"]["content"]
        
        chunks = None
        if use_batching and len(transcript) // 4 >= 3000:
            chunks = chunk_transcript(transcript, max_tokens=3000)
        
        return summary, transcript, chunks
    else:
        return "Sorry, couldn't understand the AI response.", None, None

def chat_with_video(bot: VideoDetailBot):
    
    print("\nChat mode activated. Type 'quit' to exit.")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            response = bot.handle_user_input(user_input)
            
            if response == "chat_exit":
                print("\nExiting chat...")
                break
            
            print(f"\nBot: {response}")
            
        except KeyboardInterrupt:
            print("\nChat interrupted. Exiting...")
            break

def main():
    print("YouTube Video Summarizer with Detail Bot")
    print("=" * 50)
    
    cache = VideoCache()
    bot = VideoDetailBot()
    
    url = input("\nEnter YouTube URL: ").strip()
    
    if not url or ('youtube.com' not in url and 'youtu.be' not in url):
        print("Please enter a valid YouTube URL")
        return
    
    if cache.is_cached(url):
        bot.load_video(url)
        cached_data = cache.load_video_data(url)
        
        print("\n" + "=" * 60)
        print("VIDEO SUMMARY:")
        print("=" * 60)
        print(cached_data["summary"])
        print("=" * 60)
        
        chat_choice = input("\nWant to ask detailed questions about this video? (Y/n): ").strip().lower()
        if chat_choice != 'n':
            chat_with_video(bot)
        return
    
    print("\nChoose style:")
    print("1. Casual (easy to read)")
    print("2. Academic (detailed)")
    print("3. Professional (structured)")
    
    choice = input("Pick 1, 2, or 3 (or press Enter for casual): ").strip()
    
    tone_map = {
        "1": "casual recap",
        "2": "student notes", 
        "3": "presentation points"
    }
    tone = tone_map.get(choice, "casual recap")
    
    print(f"\nProcessing video...")
    summary, transcript, chunks = summarize_youtube_video(url, tone, use_batching=True)
    
    print("\n" + "=" * 60)
    print("VIDEO SUMMARY:")
    print("=" * 60)
    print(summary)
    print("=" * 60)
    
    if transcript:
        bot.load_video(url, transcript, summary, chunks)
        
        chat_choice = input("\nWant to ask detailed questions about this video? (Y/n): ").strip().lower()
        if chat_choice != 'n':
            chat_with_video(bot)

if __name__ == "__main__":
    main()
