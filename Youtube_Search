from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq
from langdetect import detect  # type: ignore

# API key và cấu hình Groq
api_key = "---------------------------------------------------" #Có thể lấy API key của Grop từ trang web https://groq.com/
client = Groq(api_key=api_key)
model_name = "llama-3.3-70b-versatile"

# Prompt hệ thống để hướng dẫn AI cách tạo mô tả video
system_prompt = """You are an advanced video summary tool.
Depend on what kind of languages of the video, you need to translate to its language, but if you don't recognize anything, please send nothing like "".
Given a script extracted from a video, you are asked to generate a description as well as people read the description and they could know what the video discuss without watching whole video. However, words will be limit smaller than 100 words."""

# Prompt dành cho người dùng
user_prompt = """VIDEO SCRIPT: {script}
DESCRIPTION:
"""

def is_english(text):
    """Kiểm tra xem văn bản có phải tiếng Anh không."""
    try:
        return detect(text) == "en"
    except:
        return False  # Nếu lỗi xảy ra, giả định không phải tiếng Anh

def search_youtube(query):
    """Tìm kiếm 5 video trên YouTube theo truy vấn đầu vào."""
    ydl_opts = {"quiet": True, "default_search": "ytsearch5"}
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
        videos = [
            {"title": entry["title"], "videoId": entry["id"]}
            for entry in result["entries"]
        ]
    return videos

def display_videos(videos):
    """Trả về danh sách tiêu đề và đường dẫn của các video tìm được."""
    title_list = []
    link_list = []
    
    for i, video in enumerate(videos, start=1):
        title_list.append(f"{video['title']}")
        link_list.append(f"https://www.youtube.com/watch?v={video['videoId']}")
    
    return title_list, link_list

def link_and_tittle(input):
    """Tìm video và trả về tiêu đề cùng liên kết của chúng."""
    videos = search_youtube(input)
    return display_videos(videos)

def get_transcript(video_id):
    """Lấy phụ đề từ video nếu có."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print("Transcript not available:", str(e))
        return None

def split_transcript_into_chunks(transcript, chunk_duration=30):
    """Chia nhỏ phụ đề thành các đoạn có thời lượng tối đa 30 giây."""
    if not transcript:  
        return []  # Bỏ qua nếu không có phụ đề
    
    chunks = []
    current_chunk = []
    chunk_start = 0
    
    for entry in transcript:
        current_time = entry['start']
        current_chunk.append(entry['text'])
        
        # Khi thời gian vượt quá chunk_duration, lưu lại đoạn hiện tại
        if current_time - chunk_start >= chunk_duration:
            chunks.append({"text": " ".join(current_chunk), "start": chunk_start, "end": current_time})
            current_chunk = []
            chunk_start = current_time
    
    # Thêm đoạn cuối cùng nếu có
    if current_chunk:
        chunks.append({"text": " ".join(current_chunk), "start": chunk_start, "end": current_time})
    
    return chunks

def format_transcript_chunks(chunks):
    """Định dạng các đoạn phụ đề để dễ xử lý hơn."""
    formatted_chunks = []
    
    for chunk in chunks:
        formatted_chunks.append(f"[{chunk['start']}s - {chunk['end']}s] {chunk['text']}")
    
    return "\n".join(formatted_chunks)

def decription_youtube_video(input):
    """Tạo mô tả cho 5 video đầu tiên tìm thấy từ YouTube."""
    videos = search_youtube(input)
    description_list = []
    
    for i in range(5):
        video_id = videos[i]["videoId"]
        transcript = get_transcript(video_id)
        chunks = split_transcript_into_chunks(transcript)
        script = format_transcript_chunks(chunks)[:600]  # Giới hạn độ dài script
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt.format(script=script)},
            ],
            model=model_name,
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        
        description = chat_completion.choices[0].message.content
        description_list.append(description)
    
    return description_list
