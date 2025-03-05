import moviepy.editor as mp 
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from groq import Groq

# Khởi tạo bộ nhận diện giọng nói
r = sr.Recognizer()

# Chuyển đổi file âm thanh thành văn bản

def transcribe_audio(path):
    """Nhận diện giọng nói từ file âm thanh."""
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        text = r.recognize_google(audio_listened)
    return text

def get_large_audio_transcription_on_silence(path):
    """Tách file âm thanh lớn thành các đoạn nhỏ dựa trên khoảng lặng và nhận diện giọng nói."""
    sound = AudioSegment.from_file(path)
    
    # Chia nhỏ âm thanh dựa trên khoảng lặng
    chunks = split_on_silence(sound,
        min_silence_len=500,
        silence_thresh=sound.dBFS - 14,
        keep_silence=500,
    )
    
    # Tạo thư mục lưu các đoạn âm thanh nhỏ
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    
    whole_text = ""
    
    # Xử lý từng đoạn âm thanh nhỏ
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        
        try:
            text = transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += text
    
    return whole_text

# Tạo mô tả video và lưu vào file

def Desciption_text(path, number):
    """Trích xuất âm thanh từ video, nhận diện nội dung, và tạo mô tả."""
    
    # Trích xuất âm thanh từ video
    video = mp.VideoFileClip(path)
    audio_file = video.audio
    audio_file.write_audiofile(f"sound_video_{number}.wav")
    
    r = sr.Recognizer()
    path = f"D:\Documents\AI_project\sound_video_{number}.wav"  # Địa chỉ lưu file âm thanh
    
    # Nhận diện giọng nói từ file âm thanh
    script = get_large_audio_transcription_on_silence(path)
    
    # Xóa file âm thanh sau khi xử lý
    if os.path.exists(path):  
        os.remove(path) 
    
    # Thiết lập API key cho Groq
    api_key = "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"
    client = Groq(api_key=api_key)
    
    # Thiết lập prompt cho AI
    system_prompt = """You are an advanced video description tool.
    Given a script extracted from a video, you are asked to generate a description as well as people read the description and they could know what the video discuss without watching whole video."""
    
    user_prompt = """VIDEO SCRIPT: {script}
    DESCRIPTION:
    """
    
    model_name = "llama-3.3-70b-versatile"
    
    # Gửi yêu cầu tạo mô tả đến AI
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
    
    prop_text = chat_completion.choices[0].message.content
    
    # Lưu kết quả mô tả vào file
    output_path = f"----------------------------------"  # Địa chỉ lưu file mô tả
    with open(output_path, "w") as file:
        file.write(prop_text)
    
