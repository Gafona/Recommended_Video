from duckduckgo_search import DDGS
import youtube_transcript_api
from groq import Groq

api_key = "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"
client = Groq(api_key=api_key)
model_name = "llama-3.3-70b-versatile"

system_prompt_before = """You are a tool that transforms customer requests into keywords or concise, well-structured content for searching videos on YouTube. Therefore, my request is for you to convert customer desires to meet these criteria and find the most relevant videos with 10 words."""
user_prompt_before = """Customer requests: {script}
DESCRIPTION:
"""

system_prompt_after = """You are an advanced video summary tool. Depend on what kind of languages of the video, you need to translate to its language, but if you don't recognize anything, please send nothing like "".Given a script extracted from a video, you are asked to generate a description as well as people read the description and they could know what the video discuss without watching whole video. However, words will be limit smaller than 100 words."""
user_prompt_after = """VIDEO SCRIPT: {script}
DESCRIPTION:
"""

def input_process(__input__):
    script = __input__[:600]
    chat_completion = client.chat.completions.create(
    messages=[
            {"role": "system", "content": system_prompt_before},
            {"role": "user", "content": user_prompt_before.format(script=script)},
    ],
        model=model_name,
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )  
    description = chat_completion.choices[0].message.content
    return description

def Translate_to_short_form(input_long_form):
    script = input_long_form[:600]
    chat_completion = client.chat.completions.create(
    messages=[
            {"role": "system", "content": system_prompt_after},
            {"role": "user", "content": user_prompt_after.format(script=script)},
    ],
        model=model_name,
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )  
    description = chat_completion.choices[0].message.content
    return description

def search_videos(keywords: str, max_results: int = 10):
    """
    Tìm kiếm video bằng DuckDuckGo.
    Trả về danh sách chứa tiêu đề, đường dẫn video và nội dung transcript.
    
    Args:
        keywords (str): Từ khóa tìm kiếm.
        max_results (int): Số lượng kết quả tối đa. Mặc định là 10.
    
    Returns:
        list[dict]: Danh sách chứa thông tin video (title, video_link, transcript).
    """
    results = DDGS().videos(keywords=keywords, max_results=max_results)
    
    video_list = []
    for video in results:
        video_id = video.get("content", "").split("v=")[-1]  # Lấy ID video từ URL
        transcript = get_video_transcript(video_id)
        
        video_info = {
            "title": video.get("title", "No title"),
            "video_link": video.get("content", "No link"),
            "transcript": transcript,
        }
        video_list.append(video_info)
    
    return video_list

def get_video_transcript(video_id: str):
    """Lấy transcript của video YouTube nếu có."""
    try:
        transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript])
    except Exception as e:
        return f"Transcript không khả dụng: {e}"

if __name__ == "__main__":
    keyword = input_process("Python tutorial")
    videos = search_videos(keyword, max_results=5)
    for idx, video in enumerate(videos, 1):
        print(f"{idx}. {video['title']}: {video['video_link']}")
        print(f"Transcript: {Translate_to_short_form(video['transcript'][:600])}...")  # Hiển thị 200 ký tự đầu
