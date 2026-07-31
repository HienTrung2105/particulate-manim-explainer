# Scene 03 — Vì sao cần một phương pháp feed-forward?

## Metadata

- Owner: Thành viên 1
- File: `scenes/scene03_old_methods.py`
- Class: `Scene03OldMethods`
- Target duration: 150 giây; global `03:20–05:50`, local `00:00–02:30`
- Paper references: PDF trang 1–3, Introduction, Related Work và Table 1
- Status: `outline`

## Mục tiêu

Giải thích nhu cầu của một model feed-forward mà không dựng “phương pháp cũ”
thành một nhóm đồng nhất. Các baseline khác nhau về input, output, prior và
runtime; mọi so sánh cụ thể phải giữ đúng điều kiện của Table 1.

## Handoff contract

- Handoff in: cabinet phân màu cùng tree, rotation axis và sliding arrow từ
  Scene 2.
- Handoff out: hai nhánh so sánh còn hiện: `PER-OBJECT PROCESS` và
  `ONE FEED-FORWARD PASS`.
- Shared components required: `create_pipeline_box()`,
  `create_cabinet_diagram()`, `create_footer_citation()`.

## Beat sheet

| Time | Voice-over nháp | Visual state | Animation | Component/asset | Source check |
|---|---|---|---|---|---|
| 00:00–00:18 | “Bây giờ giả sử ta không chỉ có một chiếc tủ, mà là hàng nghìn object rất khác nhau. Ta cần một quy trình có thể chạy lại trên từng object mới.” | Cabinet thu nhỏ; laptop, vali và faucet hình học xuất hiện thành hàng. | Object mới mọc từ cabinet bằng `TransformFromCopy`. | Geometry tự tạo | Động lực từ Introduction; không phải benchmark claim. |
| 00:18–00:42 | “Các nghiên cứu trước không giải đúng một bài toán duy nhất. Có hướng chỉ tách part, có hướng dựng articulated object từ ảnh hoặc video, và có hướng cần thêm prior hay prompt.” | Ba lane: `Segmentation only`, `Images / video`, `Extra prior / prompt`. | Từng lane hiện tuần tự; không gắn tất cả nhược điểm cho một method. | Pipeline boxes | `paper-ok`: Related Work và Table 1 phân biệt input/output/prior. |
| 00:42–01:06 | “Một số phương pháp reconstruct theo từng object bằng optimization ở test time. Khi object thay đổi, quá trình xử lý phải chạy lại.” | Ba object đi qua ba progress ring riêng. | Ring chạy tuần tự, không dùng đồng hồ với số phút chưa khóa. | Custom 2D geometry | `paper-ok` ở mức nhóm phương pháp; `TODO(paper-check)` tên method nếu hiện trên màn hình. |
| 01:06–01:30 | “Ngay cả runtime cũng không thể gom thành một con số. Table 1 báo từ khoảng vài chục giây đến nhiều phút, và một số paper không công bố thời gian.” | Dải thời gian không số cụ thể; nhãn `reported runtime varies`, `N/A`. | Scale line mở rộng; citation Table 1. | Footer citation | `paper-ok`; mọi số cụ thể để `TODO(paper-check)` trước production. |
| 01:30–01:52 | “Vấn đề lớn hơn là tính không đồng nhất: input khác nhau, giả định khác nhau và có method chỉ dự đoán một phần của articulated structure.” | Các lane cũ không ghép được thành một output đầy đủ. | Missing blocks trong output lần lượt hiện viền đứt. | Pipeline boxes | `paper-ok`: Table 1. |
| 01:52–02:12 | “PARTICULATE chọn một mục tiêu rõ hơn: nhận trực tiếp static 3D mesh và dự đoán toàn bộ articulation trong một forward pass.” | Nhiều object hội tụ vào một model box rồi tạo articulated output. | `ReplacementTransform` các lane thành một pipeline. | `create_pipeline_box()` | `paper-ok`: Abstract/Introduction. |
| 02:12–02:24 | “Feed-forward không có nghĩa mọi object đều hoàn hảo. Nó có nghĩa model không phải tối ưu lại từ đầu cho từng object khi inference.” | Dòng `NO PER-OBJECT OPTIMIZATION` xuất hiện dưới nhánh mới; dấu cảnh báo nhỏ giữ lại. | Highlight một lần, không flash. | Text + badge | `paper-ok`; tránh biến thành claim tuyệt đối về accuracy. |
| 02:24–02:30 | “Vậy input và output của forward pass này chính xác là gì?” | Hai nhánh xếp cạnh nhau, nhánh feed-forward sáng hơn. | Giữ handoff; camera tiến về nhánh mới. | Pipeline boxes | Câu chuyển Scene 4. |

## Các claim chưa được phép khóa số

- `TODO(paper-check)`: nếu hiện runtime của từng method, chép đúng tên method,
  input setting và ô Table 1; không dùng một đồng hồ `10–20 min` cho tất cả.
- `TODO(paper-check)`: nếu nêu method cần GT part count, point prompt hoặc known
  category, gắn đúng method và đúng evaluation setting.
- Không dùng “old methods are slow and inaccurate” như kết luận chung.

## Audio và subtitle

- Voice-over: `assets/audio/s03_old_methods_vo_v01.wav`
- Subtitle: `subtitles/s03_old_methods.vi.srt`
- Audio duration: `TODO(recording)`
- Intentional pauses: 0,6 giây sau khi ba lane xuất hiện; 0,8 giây trước khi ba
  lane transform thành feed-forward pipeline.

## Review checklist

- [ ] Mỗi nhược điểm gắn đúng nhóm/method.
- [ ] Số liệu runtime đã đối chiếu Table 1 hoặc không xuất hiện.
- [ ] Citation Table 1 đọc được.
- [ ] Không trình bày feed-forward như bảo đảm luôn đúng.
- [ ] Handoff đúng nhánh so sánh cho Scene 4.
- [ ] Preview `-ql` render độc lập thành công.

