Dưới đây là sơ đồ luồng hoạt động (Activity Workflow) của hệ thống Vina-Doctor-AI, được thiết kế để tối ưu hóa quy trình khám chữa bệnh tại Việt Nam, kết hợp sức mạnh của Qwen2.5-Audio và kiến trúc Full-stack hiện đại.

Sơ đồ hoạt động tổng quát (End-to-End Workflow)
Hệ thống hoạt động theo một vòng lặp khép kín gồm 4 giai đoạn chính:

Giai đoạn 1: Tiếp nhận âm thanh (Audio Ingestion)

1. Khởi tạo: Bác sĩ nhấn nút "Bắt đầu khám" trên Dashboard (Next.js).
2. Thu âm: Hệ thống ghi lại cuộc hội thoại giữa Bác sĩ và Bệnh nhân qua Microphone.
3. Tiền xử lý: \* Lọc nhiễu (Noise Suppression).

   * Nén audio (về định dạng .mp3 hoặc .m4a) để giảm độ trễ khi gửi lên Cloud.

Giai đoạn 2: Lớp xử lý AI (AI Processing Layer)

1. Audio-to-Insight (Qwen2.5-Audio):

   * Diarization: Tự động nhận diện ai là Bác sĩ, ai là Bệnh nhân.
   * Transcription: Chuyển lời nói (Tiếng Việt/Anh/Pháp) thành văn bản có cấu trúc.
2. Clinical Reasoning (Qwen Max):

   * Extraction: Bóc tách triệu chứng, tiền sử, chỉ số sinh tồn.
   * Mapping: Đối chiếu với từ điển y khoa và mã hóa ICD-10.
   * Formatting: Sắp xếp dữ liệu theo chuẩn SOAP.



Giai đoạn 3: Kiểm soát và Bảo mật (Security \& Validation)

1. Privacy Guard: Tự động ẩn danh (Anonymize) các thông tin cá nhân nhạy cảm (PII) trước khi lưu trữ.
2. Human-in-the-loop: Bác sĩ xem lại bản nháp trên Dashboard, chỉnh sửa hoặc bổ sung các chỉ định chuyên môn nếu AI trích xuất chưa đủ.



Giai đoạn 4: Xuất bản và Hành động (Output \& Actionability)

1. Đa ngôn ngữ: Tự động dịch báo cáo sang EN/FR/AR/VN cho các đối tượng bệnh nhân khác nhau.
2. Lưu trữ: Đẩy dữ liệu vào hồ sơ bệnh án điện tử (EMR) qua API.
3. Bệnh nhân: Xuất bản tóm tắt dễ hiểu và hướng dẫn dùng thuốc gửi về ứng dụng của bệnh nhân.



Bảng tóm tắt các bước kỹ thuật (Technical Flow)



|Bước|Thành Phần|Công nghệ sử dụng|Kết quả đầu ra|
|-|-|-|-|
|1|Frontend|Next.js + Web Audio API|File audio đã nén|
|2|Backend Gateway|FastAPI (Python)|Request có cấu trúc|
|3|AI Engine|Qwen2.5-Audio-Turbo|Raw Transcript + Diarization|
|4|Clinical Logic|Qwen2.5-72B / Gemini|JSON (SOAP, ICD-10, Meds)|
|5|Storage|PostgreSQL / Redis|Hồ sơ bệnh án số hóa|



Kết luận:

Tính liên tục (Seamlessness): Bác sĩ không cần thao tác tay trên màn hình khi khám. AI đóng vai trò "người thư ký vô hình".

Độ tin cậy (Reliability): Việc có bước "Bác sĩ kiểm duyệt" giúp hệ thống an toàn tuyệt đối trong môi trường y tế.

Tốc độ (Efficiency): Sử dụng các Model "Turbo" giúp bản báo cáo xuất hiện gần như ngay lập tức sau khi cuộc khám kết thúc.







