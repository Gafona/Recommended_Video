from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer
import re
import os
import cv2
import pandas as pd

model = SentenceTransformer("all-MiniLM-L6-v2")

file_names = np.load("file_names.npy")
embeddings = np.load("embeddings.npy")

def find_x(filename):
    match = re.search(r'Grop_(\d+)', filename, re.IGNORECASE)
    if match:
        n = int(match.group(1))
        return n
def sentence_similarity(promp):
    n_list = []
    similarity_rate_list = []
    query_embedding = np.array(model.encode([promp]), dtype=np.float32).reshape(1, -1)
    similarities = cosine_similarity(query_embedding, embeddings)
    similarities_list = similarities.flatten()
    matching_indices = np.where(similarities_list >= 0.3)[0] 
    if len(matching_indices) > 0:
        for idx in matching_indices:
            n = find_x(str(np.str_(file_names[idx])))
            n_list.append(n)
            num = np.float32(similarities_list[idx])*100
            similarity_rate_list.append(num)
    else:
        return 0
    return n_list, similarity_rate_list
def compare(input): 
    result = sentence_similarity(input)
    if result != 0:
        n_list, similarity_rate_list = sentence_similarity(input)
        return n_list, similarity_rate_list
    else: 
        return 0
def extract_thumbnail(video_path, frame_time=1):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, frame_time * 1000)  # Lấy frame ở 1s
    success, frame = cap.read()
    cap.release()
    if success:
        return frame
    return None
def read_grop_file(grop_path):
    if os.path.exists(grop_path):
        with open(grop_path, "r", encoding="utf-8") as f:
            content = f.read(250) + "..."  # Lấy 100 ký tự đầu
        return content
    return "File not found"
def get_video_thumbnail(video_path):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    cap.release()
    if success:
        thumbnail_path = video_path.replace(".mp4", "_thumbnail.jpg")
        cv2.imwrite(thumbnail_path, frame)
        return thumbnail_path
    return None
