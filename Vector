import os
import numpy as np
from sentence_transformers import SentenceTransformer

# Khởi tạo mô hình Sentence Transformer
model = SentenceTransformer("all-MiniLM-L6-v2")  

# Đường dẫn thư mục chứa các file văn bản
folder_path = r"------------------------------"  # Thư mục mà các file(txt) mô tả của video được lưu trữ

# Danh sách lưu trữ nội dung câu và tên file
sentences = []
file_names = []

# Lặp qua tất cả các file trong thư mục
for file in os.listdir(folder_path):
    if file.endswith(".txt"):  # Chỉ xử lý các file .txt
        file_path = os.path.join(folder_path, file)
        
        # Đọc nội dung file và loại bỏ khoảng trắng dư thừa
        with open(file_path, "r", encoding="utf-8") as f:
            sentence = f.read().strip()
            sentences.append(sentence)
            file_names.append(file)  

# Mã hóa các câu thành vector nhúng (embeddings)
embeddings = np.array(model.encode(sentences), dtype=np.float32)

# Lưu embeddings và tên file vào các file .npy để sử dụng sau này
np.save("embeddings.npy", embeddings)
np.save("file_names.npy", np.array(file_names))

