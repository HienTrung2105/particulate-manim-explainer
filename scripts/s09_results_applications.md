# Scene 09 — Kết quả và ứng dụng

## Metadata

- Owner: Thành viên 2
- File: `scenes/scene09_results_applications.py`
- Class: `Scene09ResultsApplications`
- Target duration: 210 giây; global `18:50–22:20`, local `00:00–03:30`
- Paper references: PDF trang 1, 6–8; Figures 3–4, Tables 2–4 và Section 4
- Status: `coding`

## Mục tiêu

Trình bày bằng chứng paper báo cáo mà không biến scene thành đọc bảng: phạm vi
evaluation, kết quả part segmentation, kết quả full articulation, qualitative
generalization lên AI-generated meshes và ứng dụng được paper hỗ trợ.

## Handoff contract

- Handoff in: articulated object output card từ Scene 8.
- Handoff out: chuỗi `STATIC 3D → PARTICULATE → ARTICULATED 3D`; object cuối
  còn hiện để Scene 10 bắt đầu.
- Shared components required: `create_pipeline_box()`,
  `create_footer_citation()`, `create_rotation_axis()`,
  `create_sliding_arrow()`.
- Paper-derived assets: Figure 3/4 hoặc table crop chỉ dùng với citation + source
  sidecar; ưu tiên redraw chart/table có chọn lọc.

## Beat sheet

| Time | Voice-over nháp | Visual state | Animation | Component/asset | Source check |
|---|---|---|---|---|---|
| 00:00–00:18 | “Một articulated output nhìn hợp lý chưa đủ. Paper đánh giá riêng part segmentation và toàn bộ articulation prediction.” | Output card tách thành hai evaluation lane. | `PART SEGMENTATION` và `FULL ARTICULATION` hiện cạnh nhau. | Pipeline boxes | `paper-ok`: Section 4 evaluation subtasks. |
| 00:18–00:42 | “Evaluation dùng test split PartNet-Mobility với bảy category phổ biến, cùng benchmark Lightwheel mới gồm 243 object chất lượng cao trên 14 category.” | Hai dataset card; số `7`, `243`, `14` xuất hiện rõ nhưng không phóng đại. | Dataset cards hiện tuần tự; citation. | Cards + footer | `paper-ok`: Section 4.1. |
| 00:42–01:08 | “Ở part segmentation, paper so sánh với Naive Baseline, PartField, P3SAM, SINGAPO và Articulate AnyMesh. PARTICULATE đứng đầu trên cả hai dataset theo các metric được báo cáo.” | Simplified ranking/chart; metric labels nhỏ gọn. | Bars grow; ours highlight output green. | Redrawn chart | `paper-ok`: Table 2; exact cells require review before production. |
| 01:08–01:24 | “Một số baseline còn nhận privileged information như số ground-truth parts hoặc point prompts, nên điều kiện này phải được giữ khi đọc bảng.” | Badge `GT PART COUNT` / `POINT PROMPTS` gắn đúng lane. | Badge xuất hiện cạnh method liên quan. | Method cards | `paper-ok`: Section 4.2.2. |
| 01:24–01:50 | “Với full articulation, evaluation xét cả segmentation, tree và motion. Paper báo PARTICULATE vượt các baseline trên toàn bộ metric ở cả hai dataset.” | Ba layer score hợp thành one result; simplified Table 3 chart. | Layers stack; ours remains highest. | Redrawn chart | `paper-ok`: Table 3 and accompanying text. |
| 01:50–02:10 | “Ngay cả Articulate AnyMesh trong comparison này được cấp ground-truth motion range cho từng predicted part.” | Range badge gắn đúng method; ours không nhận badge đó. | Callout ngắn, sau đó trở về chart. | Method card | `paper-ok`: Section 4.2.3. |
| 02:10–02:37 | “Qualitative results còn cho thấy model xử lý meshes do Hunyuan3D tạo ra, dù training chỉ dùng artist-created assets.” | Một vài object silhouette tự vẽ theo category, không copy Figure 3 nếu chưa tạo source. | Static mesh → predicted parts → two states. | Original geometry | `paper-ok`: Figure 3 / Section 4.2.1. |
| 02:37–02:56 | “Ablation cho thấy point-voting over-parameterization cải thiện revolute-axis estimation, và pretrained PartField features đóng góp đáng kể.” | Hai ablation switch `Axis votes` và `PartField features`. | Toggle off/on, quality meter thay đổi tương đối. | Toggle cards | `paper-ok`: Table 4; không hiện số trước khi kiểm tra cells. |
| 02:56–03:16 | “Khi kết hợp với image-to-3D hoặc text-to-3D model, PARTICULATE tạo articulated assets có thể chuyển sang physics simulator.” | `Image/Text → 3D Generator → Static Mesh → PARTICULATE → URDF/Simulator`. | Pipeline dựng từ trái sang phải. | Pipeline boxes | `paper-ok`: Abstract, Conclusion và contributions. |
| 03:16–03:30 | “Nhưng generalization tốt không có nghĩa model không thất bại. Ta kết thúc bằng đúng những limitation mà tác giả nêu.” | Application pipeline thu lại; articulated object cuối ở giữa, cạnh có warning marker. | Fade các box trung gian; giữ object. | Output object | Câu chuyển Scene 10. |

## Số liệu đã xác nhận nhưng vẫn phải kiểm tra khi dựng chart

- Lightwheel benchmark: 243 articulated objects, 14 categories.
- PartNet-Mobility evaluation split: 7 common categories.
- Table 2: paper nói PARTICULATE consistently outperforms all baselines on both datasets.
- Table 3: paper nói PARTICULATE outperforms all baselines across all metrics on both datasets.
- Các cell của Tables 2–4 đã được đối chiếu với PDF gốc. Production chart chỉ
  thể hiện thứ hạng tương đối, không chép số, để tránh biến scene thành đọc bảng.

## Audio và subtitle

- Voice-over: `assets/audio/s09_results_applications_vo_v01.wav`
- Subtitle: `subtitles/s09_results_applications.vi.srt`
- Audio duration: `TODO(recording)`
- Intentional pauses: 0,8 giây sau mỗi chart; 1 giây khi qualitative object đổi state.

## Review checklist

- [ ] Dataset sizes và category counts đúng paper.
- [ ] Method conditions/privileged input được giữ khi so sánh.
- [ ] Không biến potential application thành kết quả đã benchmark.
- [ ] Paper figure/table crop có citation và sidecar.
- [ ] Chart redraw không làm sai thứ hạng hoặc metric direction.
- [ ] Preview `-ql` render độc lập thành công.
