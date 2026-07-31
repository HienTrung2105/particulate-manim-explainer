# Scene 04 — Input và output của PARTICULATE

## Metadata

- Owner: Thành viên 1
- File: `scenes/scene04_input_output.py`
- Class: `Scene04InputOutput`
- Target duration: 120 giây; global `05:50–07:50`, local `00:00–02:00`
- Paper references: PDF trang 1, 3–5; Abstract, Problem Formulation và Figure 2
- Status: `outline`

## Mục tiêu

Khóa chính xác interface của bài toán trước khi giải thích kiến trúc: input là
một static 3D mesh; output cuối mô tả segmentation `S`, kinematic tree `K` và
motion constraints `M` trên cùng object.

## Handoff contract

- Handoff in: hai nhánh cuối Scene 3; nhánh feed-forward được giữ lại.
- Handoff out: diagram cô đọng
  `3D MESH → PARTICULATE → PARTS + KINEMATIC TREE + MOTION`.
- Shared components required: `create_pipeline_box()`,
  `create_cabinet_diagram()`, `create_kinematic_tree()`,
  `create_rotation_axis()`, `create_sliding_arrow()`.

## Beat sheet

| Time | Voice-over nháp | Visual state | Animation | Component/asset | Source check |
|---|---|---|---|---|---|
| 00:00–00:12 | “Ta giữ lại nhánh feed-forward. Ở đầu vào, PARTICULATE chỉ nhận một object 3D tĩnh.” | Nhánh cũ rời đi; `INPUT` và cabinet một màu còn lại. | Fade nhánh per-object; pipeline mới vào giữa frame. | Pipeline + cabinet | `paper-ok`: input 3D mesh. |
| 00:12–00:30 | “Mesh cho biết vertices và faces, tức hình học bề mặt ở một articulation state. Nó không đi kèm video chuyển động.” | Cabinet đổi sang wireframe giả; vertex/face cue hiện ngắn. | Trace edges; không dựng 3D phức tạp. | Cabinet geometry | `paper-ok`: `M=(V,F)`; input là static mesh. |
| 00:30–00:49 | “Đầu ra thứ nhất là articulated part segmentation: mỗi face của mesh được gán vào một part.” | Cabinet từ một màu thành body/door/drawer. | Màu lan theo face/point cluster rồi khóa. | Cabinet | `paper-ok`: segmentation `S:[F]→[P]`. |
| 00:49–01:08 | “Đầu ra thứ hai là kinematic structure: part nào là parent, part nào là child và base part nằm ở đâu.” | Tree `Body → Door, Drawer` xuất hiện. | Edge tạo tuần tự, cabinet part tương ứng sáng. | `create_kinematic_tree()` | `paper-ok`: `K` là arborescence rooted at base part. |
| 01:08–01:32 | “Đầu ra thứ ba là motion constraints: type, direction hoặc axis, cùng phạm vi chuyển động của từng part.” | Type labels, red axis, cyan direction và min/max range marks. | Cues xuất hiện từng lớp; door/drawer chỉ chuyển động ngắn. | Rotation/sliding components | `paper-ok`: `M=(Mtp,Mpd,Mra,Mpr,Mrr)`. |
| 01:32–01:47 | “Ghép ba lớp này lại, static mesh trở thành một articulated 3D model có thể chuyển sang các trạng thái hợp lệ.” | Cabinet chuyển từ closed sang two articulated states. | Door và drawer đổi trạng thái theo constraint. | Cabinet | `paper-ok`: Figure 2 output/articulated states. |
| 01:47–01:55 | “Output cuối có thể chuyển sang URDF để dùng trong physics simulator.” | Icon/file card `URDF` nối từ output. | Card xuất hiện nhỏ; không mở rộng thành phần ứng dụng. | File badge | `paper-ok`: Problem Formulation nói có thể chuyển sang URDF. |
| 01:55–02:00 | “Tiếp theo, ta mở chiếc hộp PARTICULATE để xem các prediction này được tạo ra như thế nào.” | Diagram thu về ba box chuẩn; model box được highlight. | Camera zoom vào model box; giữ frame. | Pipeline boxes | Câu chuyển Scene 5. |

## Text trên màn hình

```text
INPUT: STATIC 3D MESH
PART SEGMENTATION
KINEMATIC TREE
MOTION CONSTRAINTS
TYPE · AXIS / DIRECTION · RANGE
```

## Audio và subtitle

- Voice-over: `assets/audio/s04_input_output_vo_v01.wav`
- Subtitle: `subtitles/s04_input_output.vi.srt`
- Audio duration: `TODO(recording)`
- Intentional pauses: sau mỗi lớp output khoảng 0,4–0,6 giây.

## Review checklist

- [ ] Không nói input có animation/video/ground-truth articulation.
- [ ] Phân biệt output semantic của bài toán với tensor/raw network prediction.
- [ ] `S`, `K`, `M` chỉ hiện nếu voice-over giải thích được, không biến scene thành slide công thức.
- [ ] Handoff đúng diagram đầu Scene 5.
- [ ] Preview `-ql` render độc lập thành công.

