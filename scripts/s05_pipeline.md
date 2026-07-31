# Scene 05 — Pipeline và Part Articulation Transformer

## Metadata

- Owner: Thành viên 1
- File: `scenes/scene05_pipeline.py`
- Class: `Scene05Pipeline`
- Target duration: 210 giây; global `07:50–11:20`, local `00:00–03:30`
- Paper references: PDF trang 3–5, Method, Figure 2 và Sections 3.2–3.3
- Status: `outline`

## Mục tiêu

Giải thích đường đi của thông tin qua PARTICULATE ở mức đủ sâu để người xem hiểu
vai trò của point tokens, learnable part queries, attention blocks và năm decoder
heads, nhưng không biến scene thành danh sách tensor hoặc công thức.

## Handoff contract

- Handoff in: diagram `3D Mesh → PARTICULATE → Parts + Tree + Motion`.
- Handoff out: Figure-2-inspired pipeline mở rộng; năm decoder head còn hiện;
  `Part Segmentation` được highlight.
- Shared components required: `create_pipeline_box()`,
  `create_cabinet_diagram()`, `create_footer_citation()`,
  `create_concept_token()`.
- Paper-derived asset: nếu dùng crop Figure 2, phải tạo
  `assets/paper/paper_fig02_pipeline_crop.png` và file `.source.md`; ưu tiên vẽ
  lại bằng geometry để transform được.

## Beat sheet

| Time | Voice-over nháp | Visual state | Animation | Component/asset | Source check |
|---|---|---|---|---|---|
| 00:00–00:18 | “Ta sẽ mở model box theo đúng luồng của Figure 2: chuẩn bị point cloud, tạo tokens, cho chúng tương tác và đọc ra nhiều đầu dự đoán.” | Model box nở thành bốn vùng: input features, PAT, heads, output. | Box mở ngang; các vùng chưa dùng được làm mờ. | Pipeline boxes | `paper-ok`: Figure 2 overview. |
| 00:18–00:42 | “Từ input mesh, model sample một point cloud trên bề mặt. Cách nhìn này biến object có topology khác nhau thành một tập điểm có cấu trúc thống nhất hơn cho network.” | Cabinet wireframe tan thành sampled points. | `TransformFromCopy` bề mặt thành dots; mesh outline vẫn mờ phía sau. | Cabinet + dots | `paper-ok`: model consumes point cloud sampled from mesh. |
| 00:42–01:08 | “Mỗi point mang ba nguồn thông tin: tọa độ XYZ, surface normal và semantic part feature lấy từ PartField.” | Ba feature card đi vào cùng một point. | XYZ, normal, PartField lần lượt cộng vào token; không hiện vector dài. | Feature cards | `paper-ok`: Section 3.2 Inputs. |
| 01:08–01:28 | “Các MLP riêng đưa ba feature về cùng dimension rồi cộng lại thành point token.” | Ba card co thành một capsule `POINT TOKEN`; cả cloud nhận token. | Merge animation; color chỉ biểu thị input, không tạo semantic mới. | Concept token | `paper-ok`: separate MLPs then sum. |
| 01:28–01:52 | “Song song với point tokens, model có một tập learnable part queries. Mỗi query là một ứng viên cho một part, vì số part thật chưa biết trước.” | Một hàng query token xuất hiện bên dưới point cloud; chỉ vài token đại diện. | Queries bật lên tuần tự; unused token giữ mờ. | Query tokens | `paper-ok`: `Pmax` learnable part queries; số part chưa biết. |
| 01:52–02:22 | “Trong mỗi attention block, queries trước tiên trao đổi thông tin với nhau bằng query self-attention, rồi đọc thông tin từ point tokens bằng query-to-point cross-attention.” | Hai bước attention được minh họa tuần tự. | Bước 1 chỉ nối query-query; bước 2 nối query tới points. | Lines/arrows | `paper-ok`: alternating query self-attention và query-to-point cross-attention. |
| 02:22–02:37 | “Model không chạy self-attention giữa toàn bộ points. Điều đó giúp tránh chi phí tăng mạnh khi point cloud lớn.” | Dense point-point graph thoáng hiện dưới dạng dấu gạch chéo rồi biến mất. | Không vẽ mạng dày thực sự; dùng icon/label `NO POINT SELF-ATTENTION`. | Text + point cloud | `paper-ok`: Section 3.2. |
| 02:37–03:03 | “Sau các block lặp lại, point tokens và part tokens đã mang thông tin articulation. Năm decoder head lần lượt đọc part segmentation, kinematic tree, articulation type, articulation axis và articulation range.” | Năm head mọc từ processed tokens đúng tên Figure 2. | Head xuất hiện tuần tự theo narration; không chạy đồng thời. | Pipeline boxes | `paper-ok`: Figure 2. |
| 03:03–03:20 | “Một số head đọc từng part token; segmentation và axis location còn cần quan hệ giữa point và part. Vì vậy output cuối không chỉ là năm nhãn độc lập.” | Heads nối về cabinet; axis head nhận thêm point-vote cue. | Connector lines; point votes hội tụ gần hinge. | Points + cabinet | `paper-ok`: Decoder Heads; revolute-axis over-parameterization. |
| 03:20–03:30 | “Ta sẽ bắt đầu từ prediction dễ nhìn nhất: các point được chia thành articulated parts như thế nào.” | Tất cả head mờ đi trừ `Part Segmentation`. | Camera zoom vào head segmentation; giữ handoff. | Pipeline head | Câu chuyển Scene 6. |

## Năm decoder head phải dùng đúng tên

```text
Part Segmentation
Kinematic Tree
Articulation Type
Articulation Axis
Articulation Range
```

Không thay Figure 2 bằng “five arbitrary neural networks”. Các head dùng point
và part tokens theo những cách khác nhau.

## Audio và subtitle

- Voice-over: `assets/audio/s05_pipeline_vo_v01.wav`
- Subtitle: `subtitles/s05_pipeline.vi.srt`
- Audio duration: `TODO(recording)`
- Intentional pauses: 0,8 giây sau khi merge input features; 1 giây sau khi năm
  head hoàn chỉnh.

## Review checklist

- [ ] Input features đúng: XYZ, normal, PartField.
- [ ] Attention đúng: query self-attention + query-to-point cross-attention.
- [ ] Không có dense point self-attention.
- [ ] Năm head đúng tên và đúng thứ tự visual.
- [ ] Figure/crop từ paper có citation và source sidecar nếu được dùng.
- [ ] Handoff highlight `Part Segmentation` cho Scene 6.
- [ ] Preview `-ql` render độc lập thành công.
