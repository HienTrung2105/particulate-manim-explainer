# Quy tắc cộng tác lâu dài

Các quy tắc này áp dụng cho toàn bộ project `particulate_video/`.

Trước khi triển khai scene production, phải đọc `PRODUCTION_GUIDE.md` và dùng
`scripts/SCENE_TEMPLATE.md` cho script/storyboard. Tên class, thời lượng target,
handoff và naming convention trong guide là production contract của hai thành viên.

## Độ chính xác nội dung

- Mọi nội dung kỹ thuật phải bám đúng paper *Particulate: Feed-Forward 3D Object Articulation*.
- Trước khi viết lời giải thích, số liệu, so sánh hoặc hạn chế, phải đối chiếu paper gốc. File kế hoạch là định hướng sản xuất, không thay thế paper như nguồn kỹ thuật.
- Nếu chưa chắc thông tin, ghi `TODO(paper-check): ...` thay vì đoán hoặc tự hoàn thiện ý.
- Không thêm claim, kết quả, limitation hay ứng dụng mà paper không hỗ trợ.
- Hình lấy trực tiếp từ paper phải có citation dễ đọc. Không dùng asset có vấn đề bản quyền hoặc không rõ giấy phép.

## Tổ chức code

- Mỗi scene production nằm trong đúng một file riêng dưới `scenes/`.
- Tên class production phải đúng bảng trong `PRODUCTION_GUIDE.md`.
- Component dùng lại phải đặt trong `common.py`; hằng số style và render đặt trong `config.py`.
- Không copy-paste các object giống nhau giữa nhiều scene. Mở rộng component chung hoặc thêm tham số cấu hình.
- Code phải rõ ràng, có type hints; chỉ comment những phần khó, quyết định hình học hoặc logic không hiển nhiên.
- Text trên màn hình phải ngắn, dễ đọc và chỉ trình bày 1–2 ý chính tại một thời điểm.
- Không dùng animation dư thừa. Mỗi chuyển động phải hỗ trợ việc giải thích.
- Ưu tiên hình học 2D hoặc giả 3D đơn giản; chỉ dùng 3D thật khi nó làm ý tưởng rõ hơn.
- Mỗi scene phải render độc lập từ thư mục gốc project.

## Phối hợp hai thành viên

- Thành viên 1 có thể phụ trách scene 1–5; thành viên 2 có thể phụ trách scene 6–10.
- Owner phải bàn giao code, storyboard, voice-over, subtitle và preview theo checklist
  trong `PRODUCTION_GUIDE.md`; người ghép cuối không tự sửa timing của cả mười scene.
- Không sửa scene của thành viên khác nếu chưa thật sự cần thiết. Nếu cần sửa, trao đổi trước và giữ thay đổi nhỏ, có mục đích rõ ràng.
- Thay đổi trong `common.py` hoặc `config.py` phải giữ tương thích với cả hai nhóm scene.
- Không thực hiện `git commit`, `git push`, tạo tag hoặc sửa lịch sử Git nếu chưa được yêu cầu rõ ràng.

## Kiểm tra trước khi bàn giao

- Render riêng scene đã sửa ở chất lượng thấp trước.
- Kiểm tra chữ không bị cắt, màu giữ đúng ý nghĩa, tốc độ đủ đọc và citation hiện rõ.
- Chỉ render 1080p sau khi preview đã đạt yêu cầu.
