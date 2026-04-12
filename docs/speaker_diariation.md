

Qwen2.5-Audio có thể làm được Speaker Diarization, nhưng theo một cách tiếp cận khác biệt và "thông minh" hơn so với các thư viện truyền thống.

Thông thường, các công cụ cũ tách biệt hai bước: (1) Phân đoạn ai nói gì - Diarization và (2) Chuyển âm thanh thành chữ - Transcription. Với Qwen2.5-Audio, nó thực hiện theo cơ chế End-to-End.

1. Cơ chế Diarization của Qwen2.5-Audio:
Qwen không chỉ trả về các nhãn vô hồn như Speaker 0, Speaker 1. Nó sử dụng khả năng Reasoning (Suy luận) để định danh nhân vật dựa trên nội dung hội thoại:

Nhận diện qua ngữ cảnh: Nếu trong audio có câu "Chào bác sĩ, tôi bị đau bụng", Qwen sẽ tự hiểu người nói là Patient và người phản hồi là Doctor.
Gán nhãn trực tiếp trong bản dịch: Khi bạn Prompt đúng cách, Qwen sẽ trả về văn bản có cấu trúc:

Doctor: Chào anh, anh bị đau từ bao giờ?
Patient: Dạ từ sáng nay bác sĩ ạ.

Kết luận: Tự nhận diện ai là bác sĩ/ bệnh nhân, phân biệt 2 giọng nói rất tốt, độ phức tạp thấp (Chỉ cần 1 API call), tốc độ nhanh (phù hợp Hackathon)

2. Cách tối ưu Prompt để Qwen làm Diarization tốt nhất, không phức tạp
Để Qwen không bị nhầm lẫn giữa các vai trong phòng khám, chúng ta nên sử dụng một kỹ thuật gọi là Guided Diarization trong Master Prompt như sau:

"Listen to the audio carefully. There are two speakers: a Doctor and a Patient. Please transcribe the conversation and prefix each turn with 'Doctor:' or 'Patient:' based on the context and voice characteristics. Then, extract the medical data into JSON."

Tùy chỉnh giai đoạn scale: Pyannote.audio ở Backend để xử lý các ca có từ 3 người nói trở lên (ví dụ: Bác sĩ + Bệnh nhân + Người nhà) để tăng độ chính xác của Timestamp.

3. Những cải tiến đáng chú ý của Qwen2.5-Audio:
Native Audio Understanding: Nó không chỉ "nghe rồi chép" (ASR) mà nó "hiểu" trực tiếp sóng âm. Điều này giúp nó nhận diện được sắc thái biểu cảm của bệnh nhân (đau đớn, lo âu) tốt hơn nhiều so với việc chỉ đọc văn bản transcript.

Hỗ trợ tiếng Việt sâu hơn: Bản 2.5 được huấn luyện trên tập dữ liệu đa ngôn ngữ mới nhất, giúp giảm thiểu lỗi sai khi bệnh nhân nói tiếng bồi hoặc dùng từ địa phương Việt Nam.

Context Window mở rộng: Khả năng ghi nhớ thông tin từ đầu file audio đến cuối file audio tốt hơn, giúp bản tóm tắt (Summary) không bị mất ý.


4. Các phiên bản Qwen 2.5 Audio: Mô hình âm thanh mới nhất và mạnh mẽ nhất từ Alibaba Cloud
Qwen2.5-Audio-7B-Instruct: Nó được tối ưu hóa để hiểu các câu lệnh (instructions) cực kỳ tốt. Với kích thước 7 tỷ tham số, nó đủ nhẹ để chạy với độ trễ thấp nhưng đủ thông minh để xử lý các thuật ngữ y khoa chuyên sâu cho Challenge.
Qwen2.5-Audio-Turbo: Đây là phiên bản tối ưu riêng cho tốc độ trên Cloud. Nếu bạn làm Demo cần tính thời gian thực (Real-time), đây là lựa chọn số 1 trên DashScope API.

5. Kiểm tra bản cập nhật mới nhất trên DashScope (Alibaba Cloud)
    1. Truy cập DashScope Console.
    2. Tìm mục Model Library.
    3. Chọn tab Audio Analysis.
    4. Tại đây, chúng ta sẽ thấy danh sách các model đang hoạt động. Hãy ưu tiên các model có nhãn -latest hoặc phiên bản cao nhất (ví dụ: v2.5).

Trong file cấu trúc thư mục  đã chuẩn bị, tại phần ai_engine/processors/audio.py, bạn nên thiết lập model là một biến môi trường (ENV) để khi Qwen ra bản Qwen3-Audio (nếu có vào cuối năm), bạn chỉ cần đổi tên model mà không cần sửa code logic.

# Ví dụ cấu hình trong .env
AUDIO_MODEL_NAME="qwen2.5-audio-turbo"




Tech Stack:

1. Use of AI:

Smart Diarization: Qwen đã tự định danh là Doctor và Patient dựa trên ngữ cảnh câu chào hỏi và chuyên môn y tế.


2. Solution Quality:

Tiêu chuẩn SOAP: Dữ liệu được bóc tách theo đúng chuẩn y tế quốc tế, giúp bác sĩ không phải mất công sắp xếp lại ý tưởng.
Mã hóa ICD-10: Việc tự động gắn mã E11.9 chứng minh AI có "kiến thức chuyên sâu", không chỉ là một trình chuyển đổi văn bản.

3. Execution:

Ready-to-Consume: Với một Full-stack Dev, cấu trúc này là "vàng". Chúng ta chỉ cần data.transcript.map() là có ngay giao diện chat, và data.multilingual_summary[selectedLang] để đổi ngôn ngữ báo cáo trong 1 nốt nhạc.
Actionability: Phần severity_level và action_items giúp hệ thống của bạn mang tính hành động cao, hỗ trợ bác sĩ đưa ra quyết định nhanh.
