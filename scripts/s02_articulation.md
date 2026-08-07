# Scene 02 — Object articulation là gì?

## Metadata

- Owner: Thành viên 1
- File: `scenes/scene02_articulation.py`
- Class: `Scene02Articulation`
- Target duration: 120 giây; global `01:20–03:20`, local `00:00–02:00`
- Paper references: PDF trang 3–4, Problem Formulation và Figure 2
- Status: `preview-rendered`

## Mục tiêu

Giúp người xem hiểu `part`, `joint` và `motion` bằng chính cabinet của Scene 1.
Kết thúc scene, người xem phải phân biệt được fixed, revolute và prismatic, đồng
thời biết representation của paper còn hỗ trợ motion type `both`.

## Handoff contract

- Handoff in: cabinet mở một phần; `STATIC 3D MESH` ở trên;
  `PART / JOINT / MOTION` ở đáy.
- Handoff out: cabinet phân màu; fixed body, revolute door, prismatic drawer;
  rotation axis và sliding arrow còn hiện.
- Shared components required: `create_cabinet_diagram()`,
  `create_concept_token()`, `create_part_label()`, `create_rotation_axis()`,
  `create_sliding_arrow()`, `create_kinematic_tree()`.

## Beat sheet

| Time | Voice-over nháp | Visual state | Animation | Component/asset | Source check |
|---|---|---|---|---|---|
| 00:00–00:12 | “Ba từ ở cuối phần trước mô tả ba lớp thông tin khác nhau của cùng một vật thể.” | Dựng đúng handoff Scene 1. Ba token dịch lên cạnh cabinet. | Matched composition; không fade-to-black. | Cabinet + concept tokens | `paper-ok`: articulation được tham số hóa bằng parts, kinematic structure và motion constraints. |
| 00:12–00:30 | “Part là một bộ phận có vai trò riêng trong cấu trúc chuyển động. Với chiếc tủ này, ta có thân tủ, cánh cửa và ngăn kéo.” | Cabinet tách nhẹ thành ba lớp; nhãn ngắn gắn vào từng phần. | Door và drawer dịch ra vài pixel rồi trở lại; label xuất hiện tuần tự. | `create_part_label()` | `paper-ok`: articulated part segmentation `S`. |
| 00:30–00:47 | “Thân tủ là base part. Nó làm gốc cho cấu trúc và trong ví dụ này được giữ cố định.” | Body xám giữ nguyên; door/drawer mờ. Token `FIXED`. | Indicate body một lần; không rung hoặc chuyển động giả. | Cabinet | `paper-ok`: paper giả định một base part; motion type có `fixed`. |
| 00:47–01:08 | “Cánh cửa nối với thân bằng một khớp quay. Chuyển động được phép là xoay quanh một trục, nên loại này gọi là revolute.” | Door đỏ; axis đỏ dọc bản lề; arc xuất hiện. | Axis được `Create`, door xoay đóng–mở một lần. | `create_rotation_axis()` | `paper-ok`: revolute cho phép rotation quanh một axis. |
| 01:08–01:29 | “Ngăn kéo lại không xoay. Nó trượt dọc theo một hướng thẳng, tương ứng với prismatic motion.” | Drawer cyan; direction arrow chạy theo ray. | Drawer trượt ra–vào một lần; arrow giữ lại. | `create_sliding_arrow()` | `paper-ok`: prismatic cho phép linear sliding; paper dự đoán direction và range. |
| 01:29–01:43 | “Trong biểu diễn của paper còn có loại both, dành cho part có cả chuyển động tịnh tiến và quay. Cabinet này chỉ cần ba trường hợp dễ thấy: fixed, revolute và prismatic.” | Legend bốn type hiện ngắn; `both` chỉ là token, không tự dựng cơ chế mới. | Ba type của cabinet sáng; `BOTH` xuất hiện trung tính rồi thu nhỏ. | Concept tokens | `paper-ok`: `Mtp ∈ {fixed, pri, rev, both}`. |
| 01:43–01:54 | “Joint còn cho biết part nào là cha, part nào là con. Toàn bộ các quan hệ đó tạo thành một kinematic tree.” | Tree `Body → Door, Drawer` xuất hiện cạnh cabinet. | Edge tree mọc từ body đến hai child; joint tương ứng sáng. | `create_kinematic_tree()` | `paper-ok`: `K` là arborescence rooted at the base part. |
| 01:54–02:00 | “Khi đã biết parts, quan hệ và motion, ta mới có một articulated object thay vì chỉ một mesh tĩnh.” | Token biến mất; cabinet + tree + cues thành frame cuối. | Camera lùi nhẹ; giữ handoff tối thiểu 0,4 giây. | Shared cabinet/tree | `paper-ok`; câu chuyển Scene 3. |

## Text trên màn hình

```text
PART
JOINT
MOTION
FIXED
REVOLUTE
PRISMATIC
BOTH
KINEMATIC TREE
```

## Audio và subtitle

- Voice-over: `assets/audio/s02_articulation_vo_v01.wav`
- Subtitle: `subtitles/s02_articulation.vi.srt`
- Audio duration: `TODO(recording)`
- Intentional pauses: sau lần door xoay và sau lần drawer trượt, mỗi lần khoảng
  0,5 giây để người xem đọc motion cue.

## Review checklist

- [ ] Dựng đúng frame cuối Scene 1.
- [ ] Không bỏ quên motion type `both` nhưng cũng không làm nó lấn át ví dụ chính.
- [ ] Fixed/revolute/prismatic dùng đúng màu semantic.
- [ ] Tree thể hiện đúng base/parent/child.
- [ ] Voice-over được đọc thử đủ 120 giây.
- [ ] Preview `-ql` render độc lập thành công.
