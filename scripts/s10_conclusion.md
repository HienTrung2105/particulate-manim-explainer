# Scene 10 — Limitations và kết luận

## Metadata

- Owner: Thành viên 2
- File: `scenes/scene10_conclusion.py`
- Class: `Scene10Conclusion`
- Target duration: 150 giây; global `22:20–24:50`, local `00:00–02:30`
- Paper references: PDF trang 8, Conclusion và Limitations
- Status: `outline`

## Mục tiêu

Kết thúc video bằng một recap ngắn, hai limitation đúng paper và callback về
robot/cabinet. Không thêm limitation suy đoán rồi gán cho tác giả.

## Handoff contract

- Handoff in: articulated object cuối chuỗi ứng dụng Scene 9, warning marker nhỏ.
- Handoff out: robot mở đúng door cabinet; end card + citation rồi fade-out.
- Shared components required: `create_cabinet_diagram()`,
  `create_robot_diagram()`, `create_concept_token()`,
  `create_footer_citation()`.
- Paper-derived failure images: chỉ dùng khi crop có source sidecar và citation;
  có thể redraw bằng geometry để tránh phụ thuộc asset.

## Beat sheet

| Time | Voice-over nháp | Visual state | Animation | Component/asset | Source check |
|---|---|---|---|---|---|
| 00:00–00:18 | “PARTICULATE cho thấy một static mesh có thể được phân tích thành parts, kinematic tree và motion constraints trong một feed-forward pass.” | Object cuối Scene 9; ba layer `PARTS / TREE / MOTION` tách ra rồi ghép lại. | Layer peel/reassemble. | Concept tokens | `paper-ok`: contributions/conclusion. |
| 00:18–00:38 | “Thiết kế dùng point features và part queries giúp model dự đoán toàn bộ articulated structure, thay vì chỉ một output riêng lẻ.” | Mini pipeline point tokens + queries → five heads → object. | Pipeline recap nhanh, không lặp Scene 5 đầy đủ. | Pipeline geometry | `paper-ok`: Method/Conclusion. |
| 00:38–01:03 | “Limitation thứ nhất: nếu object có kinematic structure rất khác những cấu trúc đã thấy khi training, model có thể không recover đúng articulation.” | Cabinet đúng ở trái; cơ cấu lạ có branching khác ở phải với tree prediction sai. | Tree đúng/khác morph; warning chỉ xuất hiện bên failure. | Original geometry | `paper-ok`: Limitations, first limitation. |
| 01:03–01:28 | “Limitation thứ hai xuất hiện ở generated meshes: các parts có thể xuyên vào nhau do artifact của mesh hoặc do motion prediction chưa hoàn hảo.” | Hai part giả 3D overlap; vùng penetration đỏ nhẹ. | Part chuyển state và giao nhau; highlight vùng overlap. | Original geometry | `paper-ok`: Limitations, inter-part penetration. |
| 01:28–01:43 | “Tăng physical plausibility của articulated assets là hướng tiếp theo, đặc biệt nếu muốn dùng chúng cho large-scale sim-to-real robotics training.” | Overlap được tách; physics/sim icon xuất hiện dưới dạng future direction. | Constraint barrier xuất hiện; icon nhỏ, không hứa đã giải quyết. | Geometry + badge | `paper-ok`: future direction in Limitations. |
| 01:43–02:02 | “Dù vậy, đóng góp cốt lõi vẫn rất rõ: AI không chỉ nhìn object như một hình dạng, mà còn suy ra cấu trúc và khả năng chuyển động của nó.” | Callback `STATIC SHAPE ≠ MOTION`; dấu `≠` transform thành arrow qua PARTICULATE. | Matched transform từ intro Scene 1. | Intro tokens | Paraphrase conclusion; không thêm metric. |
| 02:02–02:20 | “Quay lại chiếc tủ ban đầu: lần này robot biết door là part nào, hinge ở đâu và phải xoay quanh axis nào.” | Robot và cabinet Scene 1 trở lại; cues sáng tuần tự. | Robot chạm handle; door mở đúng quanh hinge. | Robot + cabinet | Visual callback; ứng dụng minh họa, không phải robot experiment của paper. |
| 02:20–02:30 | “Từ static 3D object đến articulated 3D object — đó là ý tưởng chính của PARTICULATE.” | End card: title paper, nhóm thực hiện, citation. | Hold 1,5–2 giây rồi fade-out. | Section title + citation | `paper-ok`; end card. |

## Chỉ được gọi là limitation của paper đối với hai ý

1. Kinematic structures rất khác training distribution.
2. Inter-part penetration do generated mesh artifacts hoặc imperfect motion predictions.

Các ý như “robot chưa biết thao tác an toàn”, “part nhỏ luôn bị bỏ sót” hoặc
“model cần video” không được gán cho phần Limitations nếu không có nguồn khác và
không được tác giả phát biểu.

## Audio và subtitle

- Voice-over: `assets/audio/s10_conclusion_vo_v01.wav`
- Subtitle: `subtitles/s10_conclusion.vi.srt`
- Audio duration: `TODO(recording)`
- Intentional pauses: 0,8 giây sau mỗi limitation; 1 giây trước callback cabinet;
  end card giữ tối thiểu 1,5 giây sau câu cuối.

## Review checklist

- [ ] Chỉ dùng hai limitation đúng paper.
- [ ] Future work được nói như hướng tiếp theo, không như tính năng đã có.
- [ ] Robot opening được ghi nhận là visual analogy.
- [ ] End card có title, tác giả/paper citation và tên nhóm nếu nhóm chốt.
- [ ] Fade-out chỉ xảy ra ở scene cuối.
- [ ] Preview `-ql` render độc lập thành công.
