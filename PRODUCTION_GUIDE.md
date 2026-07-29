# PARTICULATE — Production Guide

Tài liệu này là **production contract** cho cả hai thành viên. Nó chốt style,
tên scene, thời lượng, điểm nối, quy tắc asset/audio và gói bàn giao. Khi có mâu
thuẫn về nội dung kỹ thuật, thứ tự ưu tiên là:

1. Paper gốc.
2. Chỉ dẫn trực tiếp mới nhất của nhóm.
3. Tài liệu này.
4. File kế hoạch video ban đầu.

File kế hoạch là outline tốt nhưng không phải nguồn kỹ thuật thay cho paper.

## 1. Đánh giá trạng thái hiện tại

### Đã hợp lý

- Cấu trúc 10 scene tạo được mạch kể chuyện rõ: vấn đề → khái niệm → hạn chế cũ
  → input/output → kiến trúc → prediction → training → kết quả → kết luận.
- Chia scene 1–5 và 6–10 giúp hai người làm song song, ít đụng cùng file.
- Tủ là visual anchor tốt vì cùng lúc minh họa fixed, revolute và prismatic.
- Palette trong `config.py` có tương phản tốt trên nền tối và màu mang ý nghĩa
  ổn định.
- Segoe UI dễ đọc, trung tính và có sẵn trên cả máy hiện tại. Arial và DejaVu
  Sans là fallback phù hợp.
- Các cỡ chữ hiện tại phù hợp cho 1080p nếu text luôn ngắn. `LABEL_FONT_SIZE=24`
  là mức tối thiểu; không thu nhỏ label thêm để nhét nội dung dài.

### Chưa sẵn sàng để code toàn bộ

- Nội dung hiện mới là outline; chưa có voice-over cuối cùng và storyboard theo
  từng beat có timestamp.
- Chưa có handoff frame giữa các scene. Bảng ở mục 4 khóa các handoff này.
- Scene 3 không được nói chung rằng mọi phương pháp cũ mất 10–20 phút. Bảng 1
  của paper báo nhiều mức khác nhau, từ khoảng 10/30 giây đến 10–20 phút tùy
  phương pháp. Mọi con số hiện trên màn hình phải gắn đúng tên phương pháp.
- Scene 5 không được vẽ dense self-attention giữa mọi point. Paper nói PAT dùng
  query self-attention và query-to-point cross-attention; không áp dụng
  self-attention trên point tokens vì số point rất lớn.
- Scene 8 cần phân biệt network prediction và post-processing: inference còn
  dựng kinematic tree bằng maximum spanning arborescence và tổng hợp vote cho
  vị trí revolute axis.
- Scene 10 chỉ được gọi là “limitations của paper” đối với hai nhóm chính:
  kinematic structure quá khác dữ liệu train, và inter-part penetration do mesh
  sinh ra hoặc motion prediction chưa hoàn hảo. Các ý như robot chưa biết thao
  tác an toàn chỉ được ghi là bối cảnh mở rộng, không gán cho tác giả.

## 2. Nguyên tắc hình ảnh

Mục tiêu là học cách giải thích trực quan, không sao chép thiết kế, font, asset,
nhạc hoặc bố cục đặc trưng của 3Blue1Brown.

- Mỗi beat chỉ có một câu hỏi hoặc một thay đổi chính.
- Visual object tồn tại đủ lâu để người xem xây dựng “mental model”; ưu tiên
  transform object đang có thay vì liên tục cắt sang slide mới.
- Text chỉ đặt tên hoặc kết luận cho visual, không thay voice-over bằng đoạn văn.
- Màu chỉ xuất hiện khi mang thông tin; không đổi màu chỉ để trang trí.
- Camera đứng yên theo mặc định. Chỉ zoom/pan khi cần chuyển cấp độ giải thích.
- Sau một reveal quan trọng, giữ hình tối thiểu khoảng 0,8–1,2 giây.
- Không chạy quá hai animation cạnh tranh sự chú ý cùng lúc.
- Không dùng fade-to-black giữa các scene 1–9; dùng matched composition theo bảng
  handoff. Scene 10 mới được kết bằng end card/fade-out.
- Chừa vùng an toàn tối thiểu khoảng 0,5 Manim unit ở mép trên/dưới và 0,65 ở
  mép trái/phải.

### Typography và màu đã khóa

| Vai trò | Giá trị |
|---|---|
| Final render | 1920×1080, 30 FPS |
| Font | Segoe UI → Arial → DejaVu Sans |
| Title | 54 |
| Section | 42 |
| Body | 30 |
| Label | 24, không nhỏ hơn |
| Citation | 19, chỉ ở footer; ưu tiên dạng rút gọn để không phải scale |
| Fixed part | `#8B95A7` |
| Revolute joint | `#FF5A67` |
| Prismatic joint | `#35C2D8` |
| Input | `#F4F7FB` |
| Output | `#69D58C` |
| Accent | `#F2C14E` |

Không tạo màu semantic mới trong scene. Nếu thật sự cần, cập nhật `config.py`
sau khi cả hai thống nhất.

## 3. Tên class, owner và thời lượng

Tên class dưới đây là contract. Mỗi file chỉ định nghĩa một production scene.

| # | File | Class | Owner | Mốc | Target |
|---:|---|---|---|---|---:|
| 1 | `scene01_hook.py` | `Scene01Hook` | Thành viên 1 | 00:00–01:20 | 80 s |
| 2 | `scene02_articulation.py` | `Scene02Articulation` | Thành viên 1 | 01:20–03:20 | 120 s |
| 3 | `scene03_old_methods.py` | `Scene03OldMethods` | Thành viên 1 | 03:20–05:50 | 150 s |
| 4 | `scene04_input_output.py` | `Scene04InputOutput` | Thành viên 1 | 05:50–07:50 | 120 s |
| 5 | `scene05_pipeline.py` | `Scene05Pipeline` | Thành viên 1 | 07:50–11:20 | 210 s |
| 6 | `scene06_segmentation.py` | `Scene06Segmentation` | Thành viên 2 | 11:20–13:50 | 150 s |
| 7 | `scene07_joint_motion.py` | `Scene07JointMotion` | Thành viên 2 | 13:50–16:50 | 180 s |
| 8 | `scene08_training_inference.py` | `Scene08TrainingInference` | Thành viên 2 | 16:50–18:50 | 120 s |
| 9 | `scene09_results_applications.py` | `Scene09ResultsApplications` | Thành viên 2 | 18:50–22:20 | 210 s |
| 10 | `scene10_conclusion.py` | `Scene10Conclusion` | Thành viên 2 | 22:20–24:50 | 150 s |

Tổng target là 1490 giây, tức 24 phút 50 giây. Sai số chấp nhận ban đầu cho mỗi scene là
±10%; chỉ khóa chính xác sau khi có voice-over.

## 4. Handoff giữa các scene

Mỗi scene phải tự dựng lại `handoff_in` bằng component trong `common.py`, không
import object sống từ scene trước. Scene trước giữ `handoff_out` khoảng 0,25–0,4
giây; scene sau bắt đầu từ composition tương ứng rồi biến đổi tiếp.

| Scene | Handoff in | Handoff out / scene sau bắt đầu từ |
|---:|---|---|
| 1 | Không gian tối, robot và tủ tĩnh | Tủ ở giữa/phải; door mở một phần, drawer kéo ra; token `STATIC 3D MESH` phía trên và `PART / JOINT / MOTION` ở đáy |
| 2 | Dựng lại đúng tủ và bốn token cuối scene 1 | Tủ đã phân màu: body fixed, door revolute, drawer prismatic; axis và sliding arrow còn hiện |
| 3 | Cùng tủ đã phân màu, sau đó thu nhỏ sang trái | So sánh cuối còn hai nhánh: per-object process và one feed-forward pass |
| 4 | Giữ nhánh feed-forward của scene 3, bỏ nhánh cũ | Diagram cô đọng `3D Mesh → PARTICULATE → Parts + Kinematic Tree + Motion` |
| 5 | Đúng diagram cuối scene 4 | Pipeline Figure 2 đã mở rộng; năm decoder output còn hiện, `Part Segmentation` được highlight |
| 6 | Zoom vào `Part Segmentation` từ scene 5 | Point/face segmentation đã map về cùng cabinet nhiều màu |
| 7 | Cùng cabinet đã segmented từ scene 6 | Cabinet + kinematic tree + revolute axis + prismatic direction ở trạng thái rõ nhất |
| 8 | Cabinet/tree của scene 7 thu nhỏ thành một `Prediction` card | Nhánh inference kết ở articulated object; nhãn `Output` còn hiện |
| 9 | Articulated object output từ scene 8 | Chuỗi ứng dụng kết ở `Static 3D → PARTICULATE → Articulated 3D`, object cuối còn hiện |
| 10 | Cùng articulated object của scene 9 | Quay lại cabinet scene 1, lần này cửa mở đúng; end card rồi fade-out |

Nếu thay đổi handoff, người sửa phải cập nhật đồng thời hai dòng scene liên quan
và báo cho owner của scene bên cạnh.

## 5. Quy tắc đặt tên file

Tất cả tên file dùng ASCII, `lower_snake_case`, không dấu, không khoảng trắng.
`NN` luôn là số scene hai chữ số.

### Script và storyboard

```text
scripts/s01_hook.md
scripts/s02_articulation.md
...
scripts/s10_conclusion.md
```

Mỗi file dùng template `scripts/SCENE_TEMPLATE.md` và phải có paper reference,
handoff in/out, narration, visual, animation và duration theo beat.

### Visual assets

```text
assets/images/s09_laptop_articulated_v01.png
assets/svg/s02_cabinet_closed_v01.svg
assets/svg/shared_robot_v01.svg
assets/paper/paper_fig02_pipeline_crop.png
assets/paper/paper_fig02_pipeline_crop.source.md
```

- Prefix `shared_` chỉ dành cho asset thật sự dùng từ hai scene trở lên.
- Asset riêng phải có prefix `sNN_`.
- Crop từ paper dùng prefix `paper_figNN_` và file `.source.md` ghi tên paper,
  figure/page, cách crop và citation phải hiện trong video.
- Không ghi đè version đã dùng trong render review; tăng `v01` → `v02`.

### Audio

```text
assets/audio/s01_hook_vo_v01.wav
assets/audio/s01_hook_sfx_door_v01.wav
assets/audio/shared_bgm_main_v01.wav
```

- Mỗi scene có đúng một voice-over master `_vo_` để bàn giao.
- Voice-over master: WAV, 48 kHz, mono, ưu tiên 24-bit; không dùng MP3 làm master.
- Chừa khoảng 0,2–0,3 giây đầu và 0,3–0,5 giây cuối để tránh cắt âm.
- BGM/SFX không được nhúng cứng vào scene khi chưa khóa mix cuối.

### Subtitle và render

```text
subtitles/s01_hook.vi.srt
subtitles/s02_articulation.vi.srt
output/review/s01_hook_preview.mp4
```

- SRT lưu UTF-8, tối đa hai dòng/cue, ưu tiên câu ngắn trùng nhịp nói.
- Preview và final không đặt ngược vào `assets/`.

## 6. Gói bàn giao bắt buộc của mỗi scene

Owner chỉ đánh dấu scene “ready to merge” khi có đủ:

```text
scenes/sceneNN_slug.py
scripts/sNN_slug.md
assets/audio/sNN_slug_vo_vNN.wav
subtitles/sNN_slug.vi.srt
output/review/sNN_slug_preview.mp4
```

Checklist:

- Render độc lập thành công ở `-ql`.
- Duration lệch không quá ±10% target hoặc đã báo lại người ghép.
- Frame đầu/cuối đúng handoff contract.
- Không có claim chưa đối chiếu paper.
- Không có text nhỏ hơn label size hoặc bị cắt.
- Asset có nguồn/license; hình paper có citation.
- Voice-over và subtitle cùng revision với code.

## 7. Quy trình thay đổi file chung

- Owner chỉ sửa scene và script mình phụ trách.
- Trước khi sửa `common.py`, `config.py` hoặc handoff, báo người còn lại và nêu
  component/constant nào thay đổi.
- Sau thay đổi file chung, cả hai render lại ít nhất một scene đại diện của mình.
- Một người chạy final render/concat, nhưng mỗi owner phải tự bàn giao scene đã
  căn voice-over và subtitle. Người ghép không chịu trách nhiệm sửa timing của
  cả mười scene.
