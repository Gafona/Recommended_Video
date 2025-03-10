# 🎬 Recommended Videos 🔍  

Dự án này giúp tìm kiếm video dựa trên mô tả của người dùng bằng hai phương pháp:  
1. **YouTube Search** – Tìm video trực tiếp trên YouTube dựa trên mô tả.  
2. **Database Search** – Tìm video trong cơ sở dữ liệu bằng cách so sánh vector mô tả.  

## 🚀 Tính năng chính  
✅ Tìm kiếm video theo mô tả người dùng.  
✅ Hỗ trợ tìm kiếm trên YouTube và Database.  
✅ Chuyển video thành văn bản, tạo vector và so sánh mô tả.  
✅ Dựa trên mức độ giống nhau của mô tả với video mà gợi ý cho người dùng.  

## 🔍 Hướng dẫn sử dụng
1️⃣ Tìm kiếm trên YouTube
- Chỉ cần nhập mô tả video, Youtube.Search sẽ tìm kiếm và chuyển đổi cách video tìm được trên Youtuber thành các mô tả để trả về danh sách video phù hợp, mô tả, hình ảnh của video.

🔥Lưu ý: Youtube.Search.py chỉ hoạt động với những video nói bằng ngôn ngữ Tiếng Anh, và phải có tiếng nói (các video không tiếng, ngôn ngữ khác, người nói nói không rõ ràng đều sẽ bị bỏ qua).

2️⃣ Tìm kiếm trong Database
Chỉ cần nhập mô tả video, hệ thống sẽ tìm kiếm và trả về danh sách video phù hợp.
- sử dụng Transfer_video_to_decripsion.py để chuyển hóa các video thành các dạng mô tả.
- Tiếp theo đó là sử dụng vector.py để chuyển đổi tất cả các file mô tả trên thành danh sách tên và tỉ lệ để phục vụ so sánh.
- Cuối cùng là sử dung Database_Search.py để người nhập mô tả vào rồi so sánh và trả lại nhưng video có phần trăm tương thích cao (>30%).
  
🔥Lưu ý: Trong những file.py trên vẫn còn nhiều chỗ yêu cầu người dùng phải sửa lại địa chỉ hay API key để có thể sử dụng được, nên vui lòng đọc kĩ và thay đổi trước khi sử dụng nha.

## 📦 Các thư viện đã sử dụng
- duckduckgo_search để tìm kiếm video trên YouTube.
- moviepy, speech_recognition để trích xuất nội dung từ video.
- sentence_transformers, numpy để tạo vector từ văn bản.
- sklearn.metrics.pairwise để so sánh độ tương đồng giữa mô tả và video.

## 🤝 Đóng góp
Mọi đóng góp đều được hoan nghênh! Hãy fork repo, tạo pull request hoặc mở issue nếu có đề xuất cải thiện.  ❤️ ❤️ ❤️ 
