# Visual QA cho production scene

Tài liệu này là checklist thao tác ngắn để phát hiện layer chồng nhau trước khi
render 1080p. Production contract vẫn nằm ở `PRODUCTION_GUIDE.md`.

## Thứ tự đọc một frame

Một frame đạt yêu cầu khi người xem nhận ra theo thứ tự:

1. Câu hỏi hoặc kết luận của beat ở title band.
2. Object/quan hệ chính trong content band.
3. Chú giải màu hoặc nhãn phụ.
4. Nguồn paper ở footer band.

Nếu hai mục cùng tranh vị trí hoặc cùng có độ nổi bật cao, giảm bớt layer phụ.
Không giải quyết bằng cách thu nhỏ chữ.

## Các lỗi phải kiểm tra

- Title bị cắt, xuống dòng ngoài ý muốn hoặc chạm diagram.
- Label nằm trên cabinet, tree node hoặc motion cue.
- Arrow/connector chạy xuyên qua chữ hay kết thúc giữa một object.
- Object cũ chưa fade hết trước khi camera pan/zoom, tạo mảnh hình ở mép frame.
- Citation đụng caption hoặc bị scale nhỏ đến mức không đọc được.
- Handoff giữ thêm ký hiệu không có ý nghĩa ở scene kế tiếp.
- Diagram nhiều layer nhưng không có thứ tự đọc trái sang phải hoặc trên xuống.

## Quy trình review

1. Render scene độc lập bằng chất lượng thấp.
2. Lấy một frame giữa mỗi cue trong file `subtitles/sNN_*.vi.srt`.
3. Ghép frame thành contact sheet và đọc theo thứ tự beat.
4. Xem lại video ở tốc độ bàn giao để kiểm tra layer trong lúc transform.
5. Chỉ sau khi contact sheet và transition đều sạch mới render 1080p.

## Quy ước sửa

- Dùng `create_scene_title()` cho title một dòng.
- Dùng component trong `common.py` trước khi tạo object tương đương trong scene.
- Dùng constant trong `config.py` cho safe area; không thêm magic number lặp lại.
- Sửa layout ở source scene rồi render lại; không crop hoặc che lỗi ở bước ghép.
- Nếu thay đổi handoff, cập nhật storyboard của cả hai scene liên quan.
