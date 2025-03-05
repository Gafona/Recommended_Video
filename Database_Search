from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer
import re
import os
import cv2
import pandas as pd

# Khởi tạo mô hình Sentence Transformer
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load danh sách tên file và embeddings đã lưu
file_names = np.load("file_names.npy")
embeddings = np.load("embeddings.npy")

def find_x(filename):
    """Tìm số thứ tự từ tên file theo mẫu 'Grop_X'."""
    match = re.search(r'Grop_(\d+)', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def sentence_similarity(promp):
    """Tính độ tương đồng giữa input và các embeddings đã lưu."""
    n_list = []
    similarity_rate_list = []
    
    # Mã hóa câu nhập vào thành vector
    query_embedding = np.array(model.encode([promp]), dtype=np.float32).reshape(1, -1)
    
    # Tính toán độ tương đồng cosine
    similarities = cosine_similarity(query_embedding, embeddings)
    similarities_list = similarities.flatten()
    
    # Lấy các chỉ mục có độ tương đồng >= 0.3
    matching_indices = np.where(similarities_list >= 0.3)[0] 
    
    if len(matching_indices) > 0:
        for idx in matching_indices:
            n = find_x(str(np.str_(file_names[idx])))
            n_list.append(n)
            num = np.float32(similarities_list[idx]) * 100  # Chuyển thành %
            similarity_rate_list.append(num)
    else:
        return 0
    
    return n_list, similarity_rate_list

def compare(input): 
    """So sánh câu input với các embeddings và trả về kết quả nếu có."""
    result = sentence_similarity(input)
    if result != 0:
        return list(result)  # Chuyển kết quả thành danh sách
    return 0

def extract_thumbnail(video_path, frame_time=1):
    """Trích xuất ảnh thumbnail từ video tại thời điểm 1 giây."""
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, frame_time * 1000)  # Lấy frame ở 1s
    success, frame = cap.read()
    cap.release()
    
    if success:
        return frame
    return None

def read_grop_file(grop_path):
    """Đọc nội dung file Grop, lấy 250 ký tự đầu tiên."""
    if os.path.exists(grop_path):
        with open(grop_path, "r", encoding="utf-8") as f:
            content = f.read(250) + "..."  # Giới hạn ký tự hiển thị
        return content
    return "File not found"
