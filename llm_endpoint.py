import requests
import aiohttp
import asyncio
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import math
import time

load_dotenv()

API_KEY = os.getenv("ROUTER_API_KEY")         
API_URL = os.getenv("base_url")
MODEL_NAME = os.getenv("MODEL_NAME", "google/gemini-2.5-pro-exp-03-25")  

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def chunk_transcript(transcript: str, max_tokens: int = 3000) -> List[str]:
    
    chars_per_token = 4
    max_chars = max_tokens * chars_per_token
    
    sentences = transcript.split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 2 > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
        else:
            current_chunk += sentence + ". "
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

async def call_model_async(session: aiohttp.ClientSession, content: str, system_prompt: str) -> Dict[str, Any]:
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ],
        "temperature": 0.5,
        "max_tokens": 2048,
        "model": MODEL_NAME
    }

    try:
        async with session.post(API_URL, headers=headers, json=payload, timeout=60) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                return {"error": f"HTTP Error: {response.status} - {error_text}"}

    except asyncio.TimeoutError:
        return {"error": "Request timed out."}
    except Exception as e:
        return {"error": str(e)}

def call_model_single(content: str, system_prompt: str) -> Dict[str, Any]:
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ],
        "temperature": 0.5,
        "max_tokens": 2048,
        "model": MODEL_NAME
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        return {"error": "Request timed out."}

    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP Error: {e.response.status_code} - {e.response.text}"}

    except Exception as e:
        return {"error": str(e)}

def call_model(transcript: str, tone: str = "student notes", use_batching: bool = True) -> Dict[str, Any]:
    
    estimated_tokens = len(transcript) // 4
    
    if not use_batching or estimated_tokens < 3000:
        return process_single_transcript(transcript, tone)
    else:
        return process_batched_transcript(transcript, tone)

def process_single_transcript(transcript: str, tone: str) -> Dict[str, Any]:
    
    system_prompt = f"""
You are a helpful assistant that summarizes YouTube videos. Write a natural, detailed summary that a human would write.

User prefers: "{tone}" style.

Write a comprehensive summary that covers:
1. What the video is about
2. The main points discussed
3. Important details and examples
4. Key takeaways

Write in a natural, conversational way. Don't use JSON format or bullet points. Just write a flowing, detailed summary that someone could read to understand what the video was about.
"""
    
    return call_model_single(transcript, system_prompt)

async def process_batched_transcript_async(transcript: str, tone: str) -> Dict[str, Any]:
    
    chunks = chunk_transcript(transcript, max_tokens=3000)
    
    print(f"Processing long video in {len(chunks)} parts simultaneously...")
    start_time = time.time()
    
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        
        tasks = []
        for i, chunk in enumerate(chunks):
            batch_system_prompt = f"""
You are summarizing part {i+1} of {len(chunks)} from a long video transcript.

User prefers: "{tone}" style.

Write a natural summary of this segment covering the key points discussed. Don't use JSON or bullet points. 
Write in a flowing, conversational way that captures what this part of the video covered.
"""
            
            task = call_model_async(session, chunk, batch_system_prompt)
            tasks.append((i + 1, task))
        
        print("Running parallel processing...")
        results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        batch_summaries = []
        for i, result in enumerate(results):
            batch_num = tasks[i][0]
            
            if isinstance(result, Exception):
                print(f"Error processing part {batch_num}: {str(result)}")
            elif "error" in result:
                print(f"Error processing part {batch_num}: {result['error']}")
            else:
                batch_summaries.append({
                    "batch_number": batch_num,
                    "result": result
                })
    
    end_time = time.time()
    processing_time = end_time - start_time
    print(f"Parallel processing completed in {processing_time:.2f} seconds")
    
    return await merge_batch_results_async(batch_summaries, tone, len(chunks))

def process_batched_transcript(transcript: str, tone: str) -> Dict[str, Any]:
    
    return asyncio.run(process_batched_transcript_async(transcript, tone))

async def merge_batch_results_async(batch_summaries: List[Dict], tone: str, total_batches: int) -> Dict[str, Any]:
    
    if not batch_summaries:
        return {"error": "No successful batch processing results to merge"}
    
    combined_content = f"Here are summaries from {total_batches} parts of a long video:\n\n"
    
    for batch in batch_summaries:
        batch_num = batch["batch_number"]
        result = batch["result"]
        
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            combined_content += f"Part {batch_num}:\n{content}\n\n"
    
    final_system_prompt = f"""
You have summaries from {total_batches} parts of a long video.

User prefers: "{tone}" style.

Write a comprehensive, detailed summary that combines all the parts into one flowing narrative. 
Write it like a human would - naturally and conversationally. Cover all the main points from the entire video.
Don't use JSON, bullet points, or structured formats. Just write a complete, detailed summary that captures everything important from the video.
"""
    
    print("Creating final merged summary...")
    
    connector = aiohttp.TCPConnector(limit=1)
    async with aiohttp.ClientSession(connector=connector) as session:
        final_result = await call_model_async(session, combined_content, final_system_prompt)
    
    if "error" in final_result:
        return final_result
    
    if "choices" in final_result and len(final_result["choices"]) > 0:
        final_result["processing_info"] = {
            "total_batches": total_batches,
            "successful_batches": len(batch_summaries),
            "processing_method": "parallel_batched"
        }
    
    return final_result

def merge_batch_results(batch_summaries: List[Dict], tone: str, total_batches: int) -> Dict[str, Any]:
    
    if not batch_summaries:
        return {"error": "No successful batch processing results to merge"}
    
    combined_content = f"Here are summaries from {total_batches} parts of a long video:\n\n"
    
    for batch in batch_summaries:
        batch_num = batch["batch_number"]
        result = batch["result"]
        
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            combined_content += f"Part {batch_num}:\n{content}\n\n"
    
    final_system_prompt = f"""
You have summaries from {total_batches} parts of a long video.

User prefers: "{tone}" style.

Write a comprehensive, detailed summary that combines all the parts into one flowing narrative. 
Write it like a human would - naturally and conversationally. Cover all the main points from the entire video.
Don't use JSON, bullet points, or structured formats. Just write a complete, detailed summary that captures everything important from the video.
"""
    
    final_result = call_model_single(combined_content, final_system_prompt)
    
    if "error" in final_result:
        return final_result
    
    if "choices" in final_result and len(final_result["choices"]) > 0:
        final_result["processing_info"] = {
            "total_batches": total_batches,
            "successful_batches": len(batch_summaries),
            "processing_method": "batched"
        }
    
    return final_result
