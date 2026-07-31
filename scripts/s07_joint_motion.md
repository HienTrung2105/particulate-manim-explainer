# Scene 07 — Kinematic tree, joint và motion constraints

## Metadata

- Owner: Thành viên 2
- File: `scenes/scene07_joint_motion.py`
- Class: `Scene07JointMotion`
- Target duration: 180 giây; global `13:50–16:50`, local `00:00–03:00`
- Paper references: PDF trang 3–5; Problem Formulation và Decoder Heads
- Status: `outline`

## Mục tiêu

Cho người xem hiểu output articulation sâu hơn Scene 2: tree được mô tả bằng
parent likelihood giữa part tokens; mỗi part có motion type, direction/axis và
range. Revolute axis phải thể hiện cả direction lẫn location.

## Handoff contract

- Handoff in: cabinet segmented cuối Scene 6.
- Handoff out: cabinet + kinematic tree + revolute axis + prismatic direction ở
  composition rõ nhất.
- Shared components required: `create_cabinet_diagram()`,
  `create_kinematic_tree()`, `create_rotation_axis()`,
  `create_sliding_arrow()`, `create_part_label()`.

## Beat sheet

| Time | Voice-over nháp | Visual state | Animation | Component/asset | Source check |
|---|---|---|---|---|---|
| 00:00–00:18 | “Segmentation cho ta ba part, nhưng chưa cho biết chúng ghép thành một cơ cấu như thế nào.” | Cabinet segmented; ba part token tách ra bên cạnh. | TransformFromCopy part thành token. | Cabinet + labels | `paper-ok`: segmentation `S` tách với kinematic `K`. |
| 00:18–00:44 | “Kinematic-tree head xét từng cặp part token và dự đoán log-probability rằng part này là parent của part kia.” | Ma trận pairwise nhỏ; một vài directed edge candidate xuất hiện. | Pair tokens nối theo hướng; score chỉ là thanh tương đối. | Token graph | `paper-ok`: `K̃_i,j = log P[i is parent of j]`. |
| 00:44–01:04 | “Sau cùng, tree có một base part làm root. Với cabinet, body là root; door và drawer là hai child.” | Candidate graph thu thành tree `Body → Door, Drawer`. | Edge sai mờ đi; tree đúng giữ lại. | `create_kinematic_tree()` | `paper-ok`: one base part, `K` is rooted arborescence. |
| 01:04–01:28 | “Mỗi child còn có một motion type trong bốn lựa chọn: fixed, prismatic, revolute hoặc both.” | Bốn type token; body/door/drawer lần lượt map vào fixed/rev/pri. | Token map tới part; `both` chỉ được giải thích bằng icon kết hợp. | Concept tokens | `paper-ok`: four motion types. |
| 01:28–01:52 | “Với prismatic motion, model dự đoán một unit direction và một range tịnh tiến tính theo articulation state của input mesh.” | Drawer direction vector + min/max tick. | Drawer trượt giữa hai tick; vector giữ hướng cố định. | `create_sliding_arrow()` | `paper-ok`: `Mpd` và `Mpr`. |
| 01:52–02:22 | “Với revolute motion, chỉ direction là chưa đủ. Ta còn cần biết axis đi qua đâu trong không gian.” | Hai axis song song cùng direction nhưng khác location; chỉ axis ở hinge mở đúng door. | Door thử quay quanh axis sai rồi trở lại; axis đúng sáng. | Rotation axes | `paper-ok`: revolute axis is direction plus 3D location. |
| 02:22–02:42 | “Paper dự đoán direction từ part token, còn các point thuộc part cùng vote cho axis location. Cách over-parameterize này giúp location ổn định hơn.” | Point votes hội tụ trên hinge line. | Mỗi point gửi projection/vote; line axis được fit trực quan. | Points + axis | `paper-ok`: revolute-axis over-parameterization. |
| 02:42–02:53 | “Range quay cho biết góc nhỏ nhất và lớn nhất so với trạng thái hiện tại của mesh.” | Arc có hai endpoint; door chuyển giữa endpoints. | Arc draw rồi door rotate một lần. | Rotation cue | `paper-ok`: revolute range `Mrr`. |
| 02:53–03:00 | “Đây là toàn bộ prediction ta cần ghép lại ở inference.” | Cabinet và tree cân bố cục; mọi motion cue còn hiện. | Thu nhỏ thành một `PREDICTION` card ở cuối nhịp. | Cabinet/tree | Câu chuyển Scene 8. |

## Quy tắc kỹ thuật

- Không dùng một arrow đơn lẻ để biểu diễn revolute axis; cần line direction và
  một point/location trên line.
- Range được định nghĩa tương đối với articulation state của input mesh.
- Việc chọn tree hợp lệ bằng Edmonds và aggregate axis votes được giải thích ở
  Scene 8, không trộn vào kinematic-tree decoder ở đầu scene.

## Audio và subtitle

- Voice-over: `assets/audio/s07_joint_motion_vo_v01.wav`
- Subtitle: `subtitles/s07_joint_motion.vi.srt`
- Audio duration: `TODO(recording)`
- Intentional pauses: khoảng 0,8 giây sau axis sai/đúng; 0,6 giây sau tree hoàn chỉnh.

## Review checklist

- [ ] Bốn motion type đúng paper.
- [ ] Tree có một root/base part.
- [ ] Revolute axis có direction và location.
- [ ] Prismatic/revolute range không bị gán đơn vị hoặc số tùy ý.
- [ ] Handoff giữ đầy đủ cabinet, tree và cues.
- [ ] Preview `-ql` render độc lập thành công.

