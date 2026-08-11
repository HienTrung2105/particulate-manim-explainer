# Scene 08 — Training và inference assembly

## Metadata

- Owner: Thành viên 2
- File: `scenes/scene08_training_inference.py`
- Class: `Scene08TrainingInference`
- Target duration: 120 giây; global `16:50–18:50`, local `00:00–02:00`
- Paper references: PDF trang 5–6; Sections 3.4, 3.5 và 4.1
- Status: `coding`

## Mục tiêu

Phân biệt ba việc: model học nhiều prediction chung trong training; network tạo
raw predictions ở inference; các prediction sau đó được ghép/refine thành một
articulated mesh hợp lệ.

## Handoff contract

- Handoff in: cabinet/tree/motion cuối Scene 7 thu nhỏ thành `PREDICTION` card.
- Handoff out: articulated object output với nhãn `OUTPUT` còn hiện.
- Shared components required: `create_pipeline_box()`,
  `create_cabinet_diagram()`, `create_kinematic_tree()`.

## Beat sheet

| Time | Voice-over nháp | Visual state | Animation | Component/asset | Source check |
|---|---|---|---|---|---|
| 00:00–00:13 | “Những output vừa xem không được học tách rời. PARTICULATE được train end-to-end với nhiều supervision trong cùng một hệ thống.” | Prediction card tách thành `TRAINING` bên trái, `INFERENCE` bên phải. | Split composition; chỉ nhánh training sáng trước. | Pipeline boxes | `paper-ok`: Section 3.4 multi-task training. |
| 00:13–00:34 | “Mỗi training object có ground-truth part segmentation, kinematic tree và motion constraints.” | Input point cloud, GT cabinet/tree/cues. | GT layers xuất hiện tuần tự. | Cabinet/tree | `paper-ok`: training tuple `S, K, M`. |
| 00:34–00:52 | “Vì part queries không có thứ tự cố định, model phải match predicted parts với ground-truth parts trước khi tính loss.” | Query tokens và GT parts nối bằng assignment lines. | Crossing lines sắp lại thành one-to-one matching. | Tokens + lines | `paper-ok`: Hungarian matching in Section 3.4. |
| 00:52–01:07 | “Sau matching, các loss cho segmentation, tree, motion type, direction, axis và range được tối ưu cùng nhau.” | Các loss card gom thành `MULTI-TASK LOSS`. | Cards xuất hiện ngắn rồi cộng vào một meter. | Cards | `paper-ok`; không cần hiện toàn bộ công thức. |
| 01:07–01:19 | “Paper train trên PartNet-Mobility và GRScenes, với nhiều articulated states được sample trong quá trình training.” | Hai dataset badges + cabinet ở hai state. | Badge xuất hiện; cabinet đổi state. | Dataset badges | `paper-ok`: Section 4.1. |
| 01:19–01:35 | “Khi inference, raw segmentation trên points được map lại original mesh; chỉ các part thực sự xuất hiện mới được giữ.” | Nhánh inference sáng; point labels → face labels → present part tokens. | Reuse visual rút gọn Scene 6. | Cabinet + tokens | `paper-ok`: Section 3.5. |
| 01:35–01:49 | “Pairwise parent scores chưa tự tạo thành một tree hợp lệ. Paper chạy Edmonds để lấy maximum spanning arborescence trên các part hiện diện.” | Candidate directed graph biến thành một rooted tree. | Edge thấp mờ; tree hợp lệ giữ lại. | Graph/tree | `paper-ok`: Edmonds MSA. |
| 01:49–01:57 | “Với revolute axis, mỗi point vote cho location; coordinate-wise median của các vote cho vị trí cuối.” | Các point vote hội tụ; median marker đặt trên hinge. | Vote dots → median → axis line. | Points + axis | `paper-ok`: Eq. 9 / Section 3.5. |
| 01:57–02:00 | “Kết quả là một articulated 3D object hoàn chỉnh.” | Cabinet/tree/cues ghép vào card `OUTPUT`. | Snap assembly; giữ handoff. | Output card | `paper-ok`; câu chuyển Scene 9. |

## Text trên màn hình

```text
TRAINING
GROUND TRUTH
HUNGARIAN MATCHING
MULTI-TASK LOSS
INFERENCE
EDMONDS MSA
MEDIAN AXIS VOTE
OUTPUT
```

## Audio và subtitle

- Voice-over: `assets/audio/s08_training_inference_vo_v01.wav`
- Subtitle: `subtitles/s08_training_inference.vi.srt`
- Audio duration: `TODO(recording)`
- Intentional pauses: rất ngắn; scene này dày thông tin, cần đọc thử và có thể
  cắt bớt dataset details thay vì tăng tốc narration.

## Review checklist

- [ ] Hungarian matching chỉ xuất hiện ở training.
- [ ] Edmonds MSA và median vote chỉ xuất hiện ở inference assembly.
- [ ] Không gọi post-processing là decoder head.
- [ ] Không đọc toàn bộ loss formula.
- [ ] Output frame nối được Scene 9.
- [ ] Preview `-ql` render độc lập thành công.
