# Scene 01 — Từ hình dạng tĩnh đến chuyển động

## Metadata

- Owner: Thành viên 1
- File: `scenes/scene01_hook.py`
- Class: `Scene01Hook`
- Target duration: 80 giây (`00:00–01:20`)
- Preview đã đo: khoảng 80,93 giây ở 480p/15 FPS
- Status: `visual-preview-ready`; voice-over và subtitle chưa thu
- Ngôn ngữ: voice-over/subtitle tiếng Việt; keyword ngắn trên màn hình bằng tiếng Anh
- Paper references:
  - Abstract, trang 1: input là một static 3D mesh; output gồm articulated parts, kinematic structure và motion constraints.
  - Introduction, trang 1: door và drawer của cabinet chuyển động theo hinge và sliding track; hiểu articulation hữu ích cho robot manipulation.

## Mục tiêu

Người xem cảm nhận được khoảng trống giữa **nhìn thấy hình dạng** và **hiểu cách
vật thể chuyển động**. Scene chưa giải thích kiến trúc mạng; ba khái niệm cần giữ
lại là `PART`, `JOINT` và `MOTION`.

## Handoff contract

- Handoff in: title paper bên trái và silhouette cabinet bên phải; robot chưa hiện.
- Handoff out: cabinet ở giữa/phải; door mở một phần, drawer kéo ra; token
  `STATIC 3D MESH` phía trên và `PART / JOINT / MOTION` ở đáy.
- Scene 2 phải dựng lại đúng composition này bằng component trong `common.py`.
- Shared components: `create_cabinet_diagram()`, `create_robot_diagram()`,
  `create_rotation_axis()`, `create_sliding_arrow()`, `create_concept_token()`,
  `create_section_title()`, `create_footer_citation()`.

## Beat sheet và voice-over nháp

| Time | Voice-over | Visual và chuyển động | Source check |
|---|---|---|---|
| 00:00–00:05 | “Một hình dạng tĩnh chưa cho ta biết vật thể có thể chuyển động thế nào.” | Tên paper hiện cạnh silhouette cabinet; luận điểm `STATIC SHAPE ≠ MOTION` xuất hiện bên dưới. | Diễn giải từ động lực của Abstract/Introduction. |
| 00:05–00:10 | “Hãy tưởng tượng một robot đang đứng trước chiếc tủ này.” | Title rời đi; chính cabinet intro sáng lên, robot xuất hiện và mặt sàn được dựng. Không cắt sang slide mới. | Visual analogy; động lực robotics trong Introduction. |
| 00:10–00:19 | “Từ bản quét 3D, nó có thể thấy rất rõ hình dạng bên ngoài: mặt tủ, cánh cửa và ngăn kéo.” | Scan đi qua cabinet. `STATIC 3D MESH` và `SHAPE: KNOWN` xuất hiện; từng bề mặt được nhấn nhẹ. | Abstract/Introduction: input là static 3D mesh. |
| 00:19–00:29 | “Nhưng mesh tĩnh không tự nói nên tác động ở đâu. Thân tủ, tay nắm cửa và tay nắm ngăn kéo tuân theo những quy luật khác nhau.” | `MOTION: UNKNOWN`. Tay robot thử lần lượt thân, cửa và drawer nhưng cabinet chưa chuyển động. | Diễn giải trực quan, không trình bày như thí nghiệm của paper. |
| 00:29–00:42 | “Thân tủ phải đứng yên. Cánh cửa xoay quanh bản lề. Ngăn kéo lại trượt theo một phương thẳng. Hiểu vật thể nghĩa là hiểu các ràng buộc này.” | Camera tiến gần. Door mở giả 3D quanh hinge; drawer trượt ra. Hai motion cue xuất hiện, rồi chuyển động lặp lại một lần để đọc rõ. | Introduction: rotational/translational motion constrained by hinges/sliding tracks. |
| 00:42–00:55 | “Ta cần tách đúng các bộ phận; xác định chúng nối với nhau bằng khớp nào; rồi dự đoán kiểu chuyển động, trục hoặc hướng và phạm vi chuyển động.” | `PART`, `JOINT`, `MOTION` lần lượt mọc ra từ geometry tương ứng; không hiện danh sách câu hỏi. | Abstract và Problem Definition. |
| 00:55–01:09 | “PARTICULATE giải bài toán đó theo hướng feed-forward: nhận một 3D mesh tĩnh và dự đoán các part, cấu trúc động học cùng ràng buộc chuyển động.” | Badge `PARTICULATE` kết nối tên phương pháp với ba token; citation ở footer. Không lặp lại title card đầy đủ. | Abstract, trang 1. `paper-ok`. |
| 01:09–01:20 | “Trước khi đi vào mô hình, ta sẽ làm rõ ba mảnh thông tin cốt lõi: part, joint và motion — ba thứ biến một hình dạng tĩnh thành vật thể có thể chuyển động.” | Badge/citation rời đi. Bốn token chuyển về handoff frame; ba token dưới đáy được nhấn tuần tự. | Câu chuyển tiếp sang Scene 2; không thêm technical claim. |

## Text trên màn hình

Chỉ dùng các nhãn ngắn sau:

```text
STATIC 3D MESH
SHAPE: KNOWN
MOTION: UNKNOWN
PART
JOINT
MOTION
PARTICULATE
Feed-Forward 3D Object Articulation
STATIC SHAPE ≠ MOTION
```

Màu vàng là accent dùng cho token khái niệm và trạng thái chưa biết; màu đỏ/cyan
chỉ lần lượt mang nghĩa revolute/prismatic. Không tô vàng một vài từ trong câu.

## Audio và subtitle

- Voice-over master dự kiến: `assets/audio/s01_hook_vo_v01.wav`
- Subtitle dự kiến: `subtitles/s01_hook.vi.srt`
- Thu WAV 48 kHz, mono; không nhúng BGM/SFX vào Manim ở vòng storyboard.
- Đọc thử toàn đoạn theo nhịp tự nhiên. Nếu voice-over lệch beat, ưu tiên chỉnh
  khoảng giữ trong code; không ép tốc độ đọc và không kéo im lặng giả tạo.
- `TODO(recording)`: thu voice-over, đo timestamp thật và cập nhật beat sheet/SRT.

## Review checklist

- [x] Mỗi beat có một thay đổi chính và dùng lại cùng visual anchor.
- [x] Door xoay và drawer trượt thật, không chỉ đổi màu.
- [x] Text ngắn, không nhỏ hơn `LABEL_FONT_SIZE`, không bị cắt ở preview.
- [x] Fixed/revolute/prismatic dùng đúng semantic palette.
- [x] Claim về input/output đã đối chiếu Abstract và Problem Definition.
- [x] Preview `-ql` render độc lập thành công, 80,93 giây.
- [ ] Thu voice-over và bấm giờ.
- [ ] Tạo subtitle cùng revision với voice-over.
- [ ] Owner Scene 2 xác nhận và dựng đúng handoff frame cuối.
