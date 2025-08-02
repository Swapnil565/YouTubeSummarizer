# YouTube Summarizer with AI Chatbot

A powerful Python tool that automatically summarizes YouTube videos using AI and provides an intelligent chatbot for detailed Q&A about video content.

## 🚀 Features

- **Parallel Batch Processing**: 10x faster processing for long videos (1-4+ hours)
- **Smart Caching**: Automatic caching of transcripts and summaries for instant access
- **AI Chatbot**: Intelligent Q&A system for detailed explanations about video content
- **Multiple Summary Styles**: Casual, Academic, and Professional tone options
- **Automatic Chunking**: Intelligently splits long videos into manageable parts

## ⚡ Performance

- **Regular videos**: ~5-10 seconds
- **Long videos (1+ hours)**: ~7 seconds with parallel processing
- **Cached videos**: Instant loading

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Swapnil565/YouTubeSummarizer.git
cd YouTubeSummarizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```env
ROUTER_API_KEY=your_openrouter_api_key
base_url=https://openrouter.ai/api/v1/chat/completions
MODEL_NAME=google/gemini-2.5-pro-exp-03-25
```

## 🎯 Usage

### Basic Usage

```bash
python main.py
```

1. Enter a YouTube URL
2. Choose summary style (Casual/Academic/Professional)
3. Get instant summary
4. Optional: Chat with AI about video details

### Example

```
Enter YouTube URL: https://youtu.be/example
Choose style:
1. Casual (easy to read)
2. Academic (detailed)
3. Professional (structured)

Processing video...
Processing long video in 3 parts simultaneously...
Parallel processing completed in 5.29 seconds

VIDEO SUMMARY:
============================================================
[Your AI-generated summary appears here]
============================================================

Want to ask detailed questions about this video? (Y/n): y

Chat mode activated. Type 'quit' to exit.

You: What tools were mentioned in the video?
Bot: [Detailed AI response about tools mentioned]
```

## 🧠 AI Chatbot Features

The intelligent chatbot can answer detailed questions about:
- Specific topics mentioned in the video
- Tools and recommendations
- Step-by-step processes
- Technical explanations
- Key takeaways and insights

Simply ask natural questions like:
- "Explain the automation part"
- "What tools does he recommend?"
- "How does the system work?"
- "Tell me more about the lead generation"

## 📁 Project Structure

```
yt_summerizer/
├── main.py                 # Main application entry point
├── llm_endpoint.py         # AI processing with parallel batching
├── video_chatbot.py        # Intelligent Q&A chatbot
├── video_cache.py          # Caching system for persistence
├── tools/
│   └── yt_transcript.py    # YouTube transcript extraction
├── video_cache/            # Cache storage directory
├── .env                    # Environment variables
└── README.md              # This file
```

## 🔧 Technical Details

### Parallel Processing
- Automatically detects long videos (>3000 tokens)
- Splits into optimal chunks for parallel processing
- Merges results into coherent final summary
- 10x speed improvement over sequential processing

### Caching System
- Automatic caching of transcripts and summaries
- Persistent chat history storage
- Instant loading for previously processed videos
- Efficient hash-based storage

### AI Integration
- Uses OpenRouter API with Google Gemini 2.5 Pro
- Intelligent chunking with context preservation
- Smart prompt engineering for different summary styles
- Context-aware chatbot responses

## 🎛️ Configuration

### Summary Styles
- **Casual**: Easy-to-read, conversational summaries
- **Academic**: Detailed, structured analysis
- **Professional**: Business-focused, presentation-ready

### Environment Variables
- `ROUTER_API_KEY`: Your OpenRouter API key
- `base_url`: API endpoint URL
- `MODEL_NAME`: AI model to use (default: Google Gemini 2.5 Pro)

## 📊 Performance Metrics

- **Speed**: 10x faster than sequential processing
- **Accuracy**: Maintains context across chunked processing
- **Memory**: Efficient caching reduces redundant API calls
- **Cost**: Optimized token usage with smart chunking

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- YouTube Transcript API for transcript extraction
- OpenRouter for AI model access
- Google Gemini for powerful language processing

## 📧 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ by [Swapnil565](https://github.com/Swapnil565)**
# YouTube Summarizer with AI Chatbot

A powerful Python tool that automatically summarizes YouTube videos using AI and provides an intelligent chatbot for detailed Q&A about video content.

## 🚀 Features

- **Parallel Batch Processing**: 10x faster processing for long videos (1-4+ hours)
- **Smart Caching**: Automatic caching of transcripts and summaries for instant access
- **AI Chatbot**: Intelligent Q&A system for detailed explanations about video content
- **Multiple Summary Styles**: Casual, Academic, and Professional tone options
- **Automatic Chunking**: Intelligently splits long videos into manageable parts

## ⚡ Performance

- **Regular videos**: ~5-10 seconds
- **Long videos (1+ hours)**: ~7 seconds with parallel processing
- **Cached videos**: Instant loading

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Swapnil565/YouTubeSummarizer.git
cd YouTubeSummarizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```env
ROUTER_API_KEY=your_openrouter_api_key
base_url=https://openrouter.ai/api/v1/chat/completions
MODEL_NAME=google/gemini-2.5-pro-exp-03-25
```

## 🎯 Usage

### Basic Usage

```bash
python main.py
```

1. Enter a YouTube URL
2. Choose summary style (Casual/Academic/Professional)
3. Get instant summary
4. Optional: Chat with AI about video details

### Example

```
Enter YouTube URL: https://youtu.be/example
Choose style:
1. Casual (easy to read)
2. Academic (detailed)
3. Professional (structured)

Processing video...
Processing long video in 3 parts simultaneously...
Parallel processing completed in 5.29 seconds

VIDEO SUMMARY:
============================================================
[Your AI-generated summary appears here]
============================================================

Want to ask detailed questions about this video? (Y/n): y

Chat mode activated. Type 'quit' to exit.

You: What tools were mentioned in the video?
Bot: [Detailed AI response about tools mentioned]
```

## 🧠 AI Chatbot Features

The intelligent chatbot can answer detailed questions about:
- Specific topics mentioned in the video
- Tools and recommendations
- Step-by-step processes
- Technical explanations
- Key takeaways and insights

Simply ask natural questions like:
- "Explain the automation part"
- "What tools does he recommend?"
- "How does the system work?"
- "Tell me more about the lead generation"

## � Project Structure

```
yt_summerizer/
├── main.py                 # Main application entry point
├── llm_endpoint.py         # AI processing with parallel batching
├── video_chatbot.py        # Intelligent Q&A chatbot
├── video_cache.py          # Caching system for persistence
├── tools/
│   └── yt_transcript.py    # YouTube transcript extraction
├── video_cache/            # Cache storage directory
├── .env                    # Environment variables
└── README.md              # This file
```

## 🔧 Technical Details

### Parallel Processing
- Automatically detects long videos (>3000 tokens)
- Splits into optimal chunks for parallel processing
- Merges results into coherent final summary
- 10x speed improvement over sequential processing

### Caching System
- Automatic caching of transcripts and summaries
- Persistent chat history storage
- Instant loading for previously processed videos
- Efficient hash-based storage

### AI Integration
- Uses OpenRouter API with Google Gemini 2.5 Pro
- Intelligent chunking with context preservation
- Smart prompt engineering for different summary styles
- Context-aware chatbot responses

## 🎛️ Configuration

### Summary Styles
- **Casual**: Easy-to-read, conversational summaries
- **Academic**: Detailed, structured analysis
- **Professional**: Business-focused, presentation-ready

### Environment Variables
- `ROUTER_API_KEY`: Your OpenRouter API key
- `base_url`: API endpoint URL
- `MODEL_NAME`: AI model to use (default: Google Gemini 2.5 Pro)

## 📊 Performance Metrics

- **Speed**: 10x faster than sequential processing
- **Accuracy**: Maintains context across chunked processing
- **Memory**: Efficient caching reduces redundant API calls
- **Cost**: Optimized token usage with smart chunking

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- YouTube Transcript API for transcript extraction
- OpenRouter for AI model access
- Google Gemini for powerful language processing

## 📧 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ by [Swapnil565](https://github.com/Swapnil565)**

## 📋 Prerequisites

- Python 3.11+
- OpenAI API key (or compatible API)
- Internet connection

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd yt_summerizer
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API credentials
```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
API_KEY=your_openai_api_key_here
API_URL=https://api.openai.com/v1/chat/completions
MODEL_NAME=gpt-3.5-turbo
```

## 🎯 Usage

### Interactive CLI
```bash
python main.py
```

### Programmatic Usage
```python
from main import process_youtube_url

result = process_youtube_url(
    url="https://www.youtube.com/watch?v=VIDEO_ID",
    tone="student notes",  # or "presentation points", "casual recap"
    use_batching=True
)

if result["success"]:
    summary = result["summary"]
    print(summary)
else:
    print(f"Error: {result['error']}")
```

## 📊 Output Format

The summarizer provides structured output in three layers:

### 1. TL;DR
A concise one-sentence summary of the entire video.

### 2. Key Takeaways
5-7 bullet points highlighting the most important information.

### 3. Detailed Outline
Chapter-style breakdown showing the video's structure and flow.

## 🔧 Batch Processing Logic

- **Short videos** (<3000 tokens): Processed in a single API call
- **Long videos** (≥3000 tokens): 
  - Split into contextual chunks at sentence boundaries
  - Each chunk processed individually
  - Results merged into comprehensive summary
  - Progress tracking throughout the process

## 📈 Performance

- **1-hour videos**: ~30 seconds processing time
- **3-4 hour videos**: ~2-3 minutes with batch processing
- **Token efficiency**: Smart chunking minimizes API costs
- **Context preservation**: Sentence-boundary splitting maintains coherence

## 🎨 Tone Options

- **Student Notes**: Detailed, academic style with comprehensive coverage
- **Presentation Points**: Structured, professional format ideal for business use
- **Casual Recap**: Conversational, easy-to-read summary for general audiences

## 🛡️ Error Handling

- Network timeout protection
- API rate limit handling
- Invalid URL detection
- Transcript extraction failures
- Graceful batch processing fallbacks

## 📝 Example Output

```json
{
  "tldr": "This video explains advanced machine learning concepts...",
  "key_takeaways": [
    "Neural networks require careful hyperparameter tuning",
    "Batch normalization significantly improves training stability",
    "..."
  ],
  "detailed_outline": [
    "Introduction to Deep Learning Fundamentals",
    "Architecture Design Principles",
    "..."
  ]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check your `.env` configuration
2. Verify your API key and URL
3. Ensure the YouTube URL is valid and has transcripts available
4. Check the console output for detailed error messages

For long videos, batch processing is automatically enabled and may take several minutes to complete.
=======
# YouTubeSummarizer
>>>>>>> 37619350b5b510714baeb44eaa218e6aac65a61f
