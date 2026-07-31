# PARTICULATE — Tổng quan 10 scene

File này là **story map chung** của video. Hai thành viên dùng nó để kiểm tra mạch
kể chuyện, phạm vi từng phần và điểm nối trước khi viết storyboard chi tiết.

- Đây không phải voice-over hoàn chỉnh.
- Đây không thay thế paper hoặc `PRODUCTION_GUIDE.md`.
- Các file `scripts/s01_...md` đến `scripts/s10_...md` là storyboard draft tạo
  từ `SCENE_TEMPLATE.md`; owner phải review paper và đọc thử voice-over trước khi code.
- Scene 1 đã có visual preview. Scene 2–10 mới có storyboard draft, chưa có
  animation production và chưa được tự suy diễn thêm claim, số liệu hoặc limitation.

## 1. Mạch kể chuyện toàn video

```text
Hình dạng tĩnh chưa cho biết chuyển động
                ↓
Part — Joint — Motion là gì?
                ↓
Vì sao các cách trước đây còn bất tiện?
                ↓
PARTICULATE nhận gì và dự đoán gì?
                ↓
Mạng xử lý object như thế nào?
                ↓
Part segmentation
                ↓
Kinematic tree + joint + motion constraints
                ↓
Training, prediction và post-processing
                ↓
Kết quả, khả năng generalization và ứng dụng
                ↓
Limitations của paper + kết luận
```

Cabinet là visual anchor xuyên suốt. Object chỉ được thay bằng ví dụ khác khi
ví dụ đó làm rõ một ý mà cabinet không thể hiện tốt.

## 2. Timeline, class và owner

| # | Scene | Class | Owner | Mốc | Target | Trạng thái |
|---:|---|---|---|---|---:|---|
| 1 | Hook | `Scene01Hook` | Thành viên 1 | 00:00–01:20 | 80 s | Preview đã render |
| 2 | Articulation | `Scene02Articulation` | Thành viên 1 | 01:20–03:20 | 120 s | Storyboard draft |
| 3 | Old methods | `Scene03OldMethods` | Thành viên 1 | 03:20–05:50 | 150 s | Storyboard draft |
| 4 | Input / output | `Scene04InputOutput` | Thành viên 1 | 05:50–07:50 | 120 s | Storyboard draft |
| 5 | Pipeline | `Scene05Pipeline` | Thành viên 1 | 07:50–11:20 | 210 s | Storyboard draft |
| 6 | Segmentation | `Scene06Segmentation` | Thành viên 2 | 11:20–13:50 | 150 s | Storyboard draft |
| 7 | Joint and motion | `Scene07JointMotion` | Thành viên 2 | 13:50–16:50 | 180 s | Storyboard draft |
| 8 | Training / inference | `Scene08TrainingInference` | Thành viên 2 | 16:50–18:50 | 120 s | Storyboard draft |
| 9 | Results / applications | `Scene09ResultsApplications` | Thành viên 2 | 18:50–22:20 | 210 s | Storyboard draft |
| 10 | Conclusion | `Scene10Conclusion` | Thành viên 2 | 22:20–24:50 | 150 s | Storyboard draft |

Tổng target: **24 phút 50 giây**. Thời lượng chỉ được khóa sau khi đọc voice-over
thành tiếng; sai số storyboard ban đầu cho mỗi scene là ±10%.

## 3. Scene 01 — Hook: hình dạng chưa phải chuyển động

**Câu hỏi trung tâm:** Robot nhìn thấy hình dạng chiếc tủ, nhưng làm sao biết bộ
phận nào có thể chuyển động và chuyển động theo cách nào?

- Nội dung: static 3D mesh cho biết geometry nhưng chưa trực tiếp cung cấp
  articulation; dẫn tới ba khái niệm `PART`, `JOINT`, `MOTION`.
- Visual chính: title paper → cabinet silhouette → robot quét mesh → thử tương
  tác → door xoay, drawer trượt → ba concept token.
- Paper anchor: Abstract và Introduction.
- Handoff in: title paper bên trái, cabinet silhouette bên phải.
- Handoff out: cabinet đã mở một phần; `STATIC 3D MESH` ở trên;
  `PART / JOINT / MOTION` ở đáy.
- File chi tiết: `scripts/s01_hook.md`.
- Không mở rộng sang kiến trúc model trong scene này.

## 4. Scene 02 — Object articulation là gì?

**Câu hỏi trung tâm:** `Part`, `joint` và `motion` mô tả một articulated object
như thế nào?

- Nội dung: phân biệt fixed part, revolute joint và prismatic joint; giải thích
  quan hệ giữa part cha/con và chuyển động được phép.
- Visual chính: dựng lại frame cuối Scene 1; tách cabinet thành fixed body, door
  và drawer; gắn rotation axis cho door và sliding direction cho drawer.
- Paper anchor: Problem Definition/Problem Formulation và phần mô tả output.
- Handoff in: đúng bốn token và cabinet cuối Scene 1.
- Handoff out: cabinet đã phân màu; rotation axis và sliding arrow còn hiện.
- File chi tiết: `scripts/s02_articulation.md`.
- Không nói `fixed`, `revolute`, `prismatic` là toàn bộ mọi cơ chế có thể tồn tại
  trong thế giới; chỉ trình bày chúng theo phạm vi biểu diễn của paper.

## 5. Scene 03 — Vì sao cần một phương pháp feed-forward?

**Câu hỏi trung tâm:** Các hướng tiếp cận trước đây gây khó khăn gì khi phải xử
lý nhiều object mới?

- Nội dung: đặt các nhóm phương pháp liên quan cạnh nhau theo đúng mô tả của
  paper; nhấn mạnh sự khác nhau giữa quy trình riêng cho từng object và một mô
  hình feed-forward.
- Visual chính: nhiều object đi qua nhánh xử lý/optimization riêng, sau đó thu
  gọn thành so sánh với một feed-forward pass.
- Paper anchor: Related Work, Introduction và bảng runtime/kết quả liên quan.
- Handoff in: cabinet đã articulated từ Scene 2 thu nhỏ sang trái.
- Handoff out: hai nhánh `per-object process` và `one feed-forward pass`.
- `TODO(paper-check)`: tên phương pháp, điều kiện đánh giá và mọi con số runtime
  phải được chép đúng bảng tương ứng.
- Không nói chung rằng tất cả phương pháp cũ đều mất 10–20 phút.
- File chi tiết: `scripts/s03_old_methods.md`.

## 6. Scene 04 — Input và output của PARTICULATE

**Câu hỏi trung tâm:** Mô hình nhận chính xác dữ liệu gì và phải dự đoán những
thành phần nào?

- Nội dung: input là một static 3D mesh; output mô tả articulated parts,
  kinematic structure và motion constraints.
- Visual chính: `3D Mesh → PARTICULATE → Parts + Kinematic Tree + Motion`;
  output được xây từng lớp trên cùng một cabinet.
- Paper anchor: Abstract, Problem Formulation và overview của phương pháp.
- Handoff in: giữ nhánh feed-forward từ Scene 3.
- Handoff out: diagram input/model/output cô đọng.
- Không trộn output trực tiếp của network với các bước post-processing; phần đó
  được làm rõ ở Scene 8.
- File chi tiết: `scripts/s04_input_output.md`.

## 7. Scene 05 — Pipeline và Part Articulation Transformer

**Câu hỏi trung tâm:** Từ mesh tĩnh, thông tin đi qua model theo đường nào để tạo
ra các prediction?

- Nội dung: sampling point cloud, semantic features, point tokens, learnable
  part queries, Part Articulation Transformer và các prediction heads.
- Visual chính: mở rộng diagram Scene 4 theo Figure 2; zoom từ mesh sang points,
  sau đó cho part queries tương tác với point tokens và tách thành output heads.
- Paper anchor: Method và Figure 2.
- Handoff in: diagram cuối Scene 4.
- Handoff out: pipeline mở rộng; các output head còn hiện; `Part Segmentation`
  được highlight để dẫn sang Scene 6.
- PAT dùng query self-attention và query-to-point cross-attention.
- Không vẽ dense self-attention giữa toàn bộ point tokens; paper chủ động tránh
  cách đó vì số point lớn.
- `TODO(paper-check)`: khóa đúng tên và số lượng prediction heads theo Figure 2
  trước khi viết storyboard chi tiết.
- File chi tiết: `scripts/s05_pipeline.md`.

## 8. Scene 06 — Articulated part segmentation

**Câu hỏi trung tâm:** Các điểm hoặc mặt trên mesh được gom thành những bộ phận
có khả năng chuyển động độc lập như thế nào?

- Nội dung: giải thích trực giác part queries tạo mask/assignment cho các phần;
  prediction trên point được ánh xạ lại để hiển thị trên mesh.
- Visual chính: point cloud một màu → các cụm part → cabinet segmented; fixed
  body, door và drawer giữ màu semantic nhất quán.
- Paper anchor: nhánh part segmentation trong Method/Figure 2 và phần training
  supervision tương ứng.
- Handoff in: zoom vào `Part Segmentation` từ Scene 5.
- Handoff out: cabinet segmented hoàn chỉnh.
- Không gọi đây đơn thuần là semantic segmentation; part trong bài toán gắn với
  cấu trúc articulation.
- Khi mô tả connected-component refinement: trong mỗi component, tất cả faces
  được gán về part có predicted surface coverage lớn nhất trong component đó.
- File chi tiết: `scripts/s06_segmentation.md`.

## 9. Scene 07 — Kinematic tree, joint và motion constraints

**Câu hỏi trung tâm:** Sau khi có parts, model biểu diễn quan hệ và chuyển động
giữa chúng ra sao?

- Nội dung: parent/child relations, kinematic tree, motion type, revolute axis,
  prismatic direction và motion range.
- Visual chính: tree xuất hiện cạnh cabinet; chọn edge nào thì part/joint tương
  ứng sáng lên; door xoay và drawer trượt theo constraint đã dự đoán.
- Paper anchor: Problem Formulation và các decoder/prediction heads trong Method.
- Handoff in: cabinet segmented cuối Scene 6.
- Handoff out: cabinet + kinematic tree + revolute axis + prismatic direction ở
  composition rõ nhất.
- Không giản lược axis thành chỉ một mũi tên nếu paper cần cả direction và
  location; vị trí axis phải được thể hiện riêng.
- `TODO(paper-check)`: khóa representation và loss của từng motion parameter
  trong storyboard chi tiết.
- File chi tiết: `scripts/s07_joint_motion.md`.

## 10. Scene 08 — Training, prediction và inference assembly

**Câu hỏi trung tâm:** Những prediction riêng lẻ được học và ghép thành một
articulated object hợp lệ như thế nào?

- Nội dung: training supervision ở mức tổng quan; khi inference, phân biệt rõ
  network predictions với bước dựng cấu trúc đầu ra.
- Visual chính: hai nhánh `Training` và `Inference`; prediction card được ghép
  thành segmentation, tree và motion parameters.
- Paper anchor: Training/Inference trong Method và supplementary details nếu cần.
- Handoff in: cabinet/tree cuối Scene 7 thu nhỏ thành `Prediction` card.
- Handoff out: articulated object output với nhãn `Output`.
- Inference còn dựng kinematic tree bằng maximum spanning arborescence
  (Edmonds) và tổng hợp vote cho vị trí revolute axis.
- Không nói mọi thứ trên output cuối đều xuất hiện trực tiếp từ một decoder duy
  nhất; phải tách network prediction và post-processing.
- `TODO(paper-check)`: xác nhận loss terms và chỉ chọn các term thực sự cần cho
  lời giải thích trực quan.
- File chi tiết: `scripts/s08_training_inference.md`.

## 11. Scene 09 — Kết quả và ứng dụng

**Câu hỏi trung tâm:** Phương pháp hoạt động tốt ở đâu, generalize ra sao và đầu
ra có thể dùng vào việc gì?

- Nội dung: trình bày kết quả định lượng/định tính được paper báo cáo; minh họa
  khả năng xử lý object mới và generated 3D assets nếu paper có bằng chứng.
- Visual chính: kết quả trên một vài loại object; bảng/biểu đồ chỉ giữ metric cần
  thiết; kết thúc bằng `Static 3D → PARTICULATE → Articulated 3D`.
- Paper anchor: Experiments, tables, qualitative figures và phần applications.
- Handoff in: articulated object output từ Scene 8.
- Handoff out: object articulated cuối chuỗi ứng dụng.
- `TODO(paper-check)`: mọi metric, baseline, runtime, tên dataset và claim
  generalization phải được kiểm tra lại từng dòng trong paper.
- Phân biệt rõ kết quả paper chứng minh với ứng dụng tiềm năng do nhóm minh họa.
- File chi tiết: `scripts/s09_results_applications.md`.

## 12. Scene 10 — Limitations và kết luận

**Câu hỏi trung tâm:** PARTICULATE đóng góp điều gì, còn thất bại trong trường
hợp nào và người xem nên nhớ câu nào sau cùng?

- Nội dung: tóm lại đường đi `static shape → parts → joints → motion`; trình bày
  đúng limitations tác giả nêu; quay lại robot/cabinet ở đầu video.
- Visual chính: hai failure case được đặt cạnh kết quả đúng; sau đó robot mở đúng
  cửa cabinet và video kết bằng end card.
- Paper anchor: Limitations, Conclusion và failure-case discussion.
- Handoff in: articulated object cuối Scene 9.
- Handoff out: cabinet Scene 1, lần này door mở đúng; end card rồi fade-out.
- Hai limitation chính đã xác nhận:
  1. Kinematic structure quá khác dữ liệu training có thể làm model thất bại.
  2. Inter-part penetration có thể xuất hiện do generated mesh hoặc prediction
     chưa hoàn hảo.
- Không tự gán cho paper các limitation như “robot chưa biết thao tác an toàn”
  nếu tác giả không phát biểu điều đó.
- File chi tiết: `scripts/s10_conclusion.md`.

## 13. Contract chuyển tiếp nhanh

| Từ → sang | Object phải được giữ lại |
|---|---|
| 1 → 2 | Cabinet mở một phần + `STATIC 3D MESH` + `PART/JOINT/MOTION` |
| 2 → 3 | Cabinet phân màu + axis + sliding arrow |
| 3 → 4 | Hai nhánh old/per-object và feed-forward |
| 4 → 5 | Diagram `Mesh → PARTICULATE → Outputs` |
| 5 → 6 | Pipeline với `Part Segmentation` được highlight |
| 6 → 7 | Cabinet segmented |
| 7 → 8 | Cabinet + kinematic tree + motion constraints |
| 8 → 9 | Articulated output card |
| 9 → 10 | Articulated object cuối application chain |

Mỗi scene tự dựng lại frame đầu bằng component trong `common.py`; không import
mobject sống từ scene trước.

## 14. Checklist trước khi một owner bắt đầu code

- [ ] Đọc paper anchor của scene.
- [ ] Tạo file `scripts/sNN_slug.md` từ `SCENE_TEMPLATE.md`.
- [ ] Viết voice-over nháp và đọc thành tiếng.
- [ ] Chia beat có timestamp; mỗi beat chỉ có một thay đổi chính.
- [ ] Đối chiếu mọi số liệu/claim; chỗ chưa chắc ghi `TODO(paper-check)`.
- [ ] Xác nhận `handoff_in` và `handoff_out` với owner scene bên cạnh.
- [ ] Liệt kê component dùng lại; chỉ sửa `common.py` khi thực sự dùng chung.
- [ ] Render độc lập ở `-ql` trước khi tạo preview bàn giao.

## 15. Phân việc hiện tại

### Thành viên 1 — Scene 1–5

Tập trung vào vấn đề, định nghĩa articulation, related approaches, input/output
và kiến trúc tổng quan. Scene 1 đã có preview; storyboard draft Scene 2–5 cần
owner và thành viên còn lại review trước khi code.

### Thành viên 2 — Scene 6–10

Tập trung vào segmentation, joint/motion, training/inference, experiments và
limitations. Storyboard draft Scene 6–10 đã có nhưng vẫn phải đọc
Method/Experiments/Limitations trực tiếp; không dựa riêng vào mô tả tổng quát.

### Người ghép cuối

Chỉ ghép các scene đã được owner căn voice-over/subtitle và bàn giao đúng frame.
Người ghép không chịu trách nhiệm kéo giãn hoặc sửa timing của cả mười scene.
