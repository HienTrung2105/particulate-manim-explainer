# Scene 06 — Articulated part segmentation

## Metadata

- Owner: Thành viên 2
- File: `scenes/scene06_segmentation.py`
- Class: `Scene06Segmentation`
- Target duration: 150 giây; global `11:20–13:50`, local `00:00–02:30`
- Paper references: PDF trang 4–7; Sections 3.3, 3.5, 4.2.2 và Figures 2, 4
- Status: `coding`

## Mục tiêu

Giải thích part segmentation như một prediction gắn với articulation: part
queries chia sampled points thành các bộ phận, sau đó prediction được đưa về
faces của mesh và có thể được refine bằng connected components.

## Handoff contract

- Handoff in: pipeline Scene 5 với head `Part Segmentation` được highlight.
- Handoff out: cabinet segmented hoàn chỉnh bằng màu semantic nhất quán.
- Shared components required: `create_cabinet_diagram()`,
  `create_concept_token()`, `create_part_label()`.
- Paper-derived asset: Figure 4 chỉ dùng nếu có crop + source sidecar + citation.

## Beat sheet

| Time | Voice-over nháp | Visual state | Animation | Component/asset | Source check |
|---|---|---|---|---|---|
| 00:00–00:15 | “Ta zoom vào head đầu tiên. Nhiệm vụ của nó là quyết định mỗi sampled point thuộc part query nào.” | Head segmentation nở ra; processed point cloud và query tokens còn lại. | Camera zoom; các head khác mờ đi. | Pipeline + tokens | `paper-ok`: part segmentation head. |
| 00:15–00:38 | “Với mỗi point và mỗi part query, model tạo một score. Có thể hình dung chúng thành một ma trận: hàng là points, cột là các part ứng viên.” | Ma trận nhỏ đại diện, không hiển thị hàng nghìn phần tử. | Một vài point chạy vào rows; query chạy vào columns. | Grid geometry | `paper-ok`: mask logits `S̃ ∈ R^(N×Pmax)`. |
| 00:38–01:00 | “Query nào có score cao nhất sẽ nhận point đó. Dần dần, những vùng cùng thuộc door, drawer hay fixed body tạo thành các cụm rõ ràng.” | Point cloud một màu chuyển thành ba cluster. | Màu lan theo nhóm; không random sparkle. | Dots + semantic colors | `paper-ok`: inference assigns point labels from logits. |
| 01:00–01:20 | “Prediction ban đầu nằm trên sampled points, còn output cần nằm trên original mesh. Vì vậy mỗi face nhận nhãn theo các sampled points thuộc face đó.” | Points rơi trở lại mesh faces; face đổi màu. | Point-to-face connectors ngắn; majority cue xuất hiện. | Cabinet mesh | `paper-ok`: Section 3.5 maps point predictions back to faces. |
| 01:20–01:39 | “Nếu một face có nhiều sampled point, nhãn chiếm đa số được dùng. Bước này biến point segmentation thành face-part segmentation.” | Một face phóng to với ba dot vote; hai cùng màu thắng. | Vote dots hội tụ; face nhận màu kết quả. | Zoomed inset | `paper-ok`: majority over points sampled on the face. |
| 01:39–01:59 | “Mesh thủ công thường có connected components khá rõ. Trong mỗi component, paper gán tất cả faces về part có predicted surface coverage lớn nhất ngay trong component đó.” | Một vài patch sai màu trên cabinet; connected regions được sửa. | Trong từng component, coverage theo part được so sánh rồi toàn bộ faces nhận part thắng. | Cabinet patches | `paper-ok`: connected-component refinement in Section 3.5. |
| 01:59–02:18 | “Điểm quan trọng là đây không chỉ là gọi tên vùng bề mặt. Các part được dùng tiếp để dựng parent-child relation và gắn motion constraints.” | Segmented cabinet nối tới icon tree và axis. | Part colors giữ nguyên; tree/axis preview xuất hiện mờ. | Cabinet + tree preview | `paper-ok`: output parts feed articulated structure. |
| 02:18–02:30 | “Giờ ta giữ nguyên ba part này và hỏi: chúng nối với nhau bằng joint nào, và mỗi joint cho phép chuyển động gì?” | Point cloud biến mất; cabinet segmented chiếm giữa frame. | Clean-up; giữ handoff tối thiểu 0,4 giây. | Cabinet | Câu chuyển Scene 7. |

## Text trên màn hình

```text
POINTS × PART QUERIES
POINT LABELS
FACE LABELS
CONNECTED-COMPONENT REFINEMENT
```

## Audio và subtitle

- Voice-over: `assets/audio/s06_segmentation_vo_v01.wav`
- Subtitle: `subtitles/s06_segmentation.vi.srt`
- Audio duration: `TODO(recording)`
- Intentional pauses: sau khi point clusters hoàn chỉnh và sau point-to-face
  mapping, mỗi lần khoảng 0,7 giây.

## Review checklist

- [ ] Phân biệt sampled point prediction và face segmentation output.
- [ ] Connected-component refinement không bị mô tả như decoder neural riêng.
- [ ] Không gọi đây đơn thuần là semantic class segmentation.
- [ ] Nếu dùng Figure 4 phải có citation và source sidecar.
- [ ] Frame cuối đúng cabinet đầu Scene 7.
- [ ] Preview `-ql` render độc lập thành công.
