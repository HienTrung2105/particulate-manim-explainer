# PARTICULATE video — Manim project foundation

Project này là nền tảng cho video giải thích paper *Particulate: Feed-Forward 3D
Object Articulation*. Hiện có `SmokeTestScene` và production `Scene01Hook`;
scene 2–10 vẫn là khung trống có TODO và chưa chứa animation.

Trước khi viết scene production, đọc `PRODUCTION_GUIDE.md`. File này khóa tên
class, thời lượng, handoff giữa scene, naming asset/audio và gói bàn giao. Tạo
script/storyboard mới từ `scripts/SCENE_TEMPLATE.md`.

## 1. Tạo virtual environment trên Windows

Mở PowerShell tại thư mục project:

```powershell
cd D:\videoAI_MANIMM\particulate_video
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Nếu PowerShell chặn activation, có thể gọi Python trong venv trực tiếp:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Project hỗ trợ Python 3.11–3.14 và đang pin Manim Community `0.20.1` để hai máy
dùng cùng một API/render behavior.

## 2. Render một scene ở chất lượng thấp

Sau khi activate `.venv`:

```powershell
python -m manim -ql --renderer=cairo --media_dir output/manim scenes/smoke_test.py SmokeTestScene
```

Video nằm dưới `output/manim/videos/`.

Render riêng Scene 1 production hiện tại:

```powershell
python -m manim -ql --renderer=cairo --media_dir output/manim scenes/scene01_hook.py Scene01Hook
```

## 3. Render final 1080p, 30 FPS

```powershell
python -m manim -qh -r 1920,1080 --fps 30 --renderer=cairo --media_dir output/manim scenes/smoke_test.py SmokeTestScene
```

Đổi file/class ở cuối lệnh để render Scene 1:

```powershell
python -m manim -qh -r 1920,1080 --fps 30 --renderer=cairo --media_dir output/manim scenes/scene01_hook.py Scene01Hook
```

## 4. Render toàn bộ scene đã được triển khai

Trong giai đoạn hiện tại, lệnh sau render `Scene01Hook` và smoke test:

```powershell
python render_all.py --quality low
```

Chỉ render production scene đã triển khai, không render smoke test:

```powershell
python render_all.py --quality low --exclude-smoke
```

Khi scene 1–10 đã có lớp Manim thật, render production 1080p và bỏ smoke test:

```powershell
python render_all.py --quality final --exclude-smoke
```

`render_all.py` đọc AST thay vì import các file scene, sắp xếp theo tên file rồi
tên class, và chỉ render lớp kế thừa `Scene`, `MovingCameraScene`, `ThreeDScene`
hoặc `ZoomedScene`.

## 5. Ghép scene

Sau khi cài FFmpeg CLI và mọi scene được render cùng resolution/FPS/codec:

```powershell
python render_all.py --quality final --exclude-smoke --concat --output-file output/particulate_final.mp4
```

Script tạo `output/concat.txt` theo đúng thứ tự render và gọi FFmpeg concat demuxer
với `-c copy`, nên không encode lại video.

## 6. Trạng thái dependency trên máy kiểm tra (2026-07-29)

- OS: Windows x64, build `26200.8875`.
- `python`: Miniconda Python 3.13.5, 64-bit.
- Python Launcher: `py -3.13` là 3.13.1 (được dùng cho `.venv`) và còn có Python 3.14.
- Manim: chưa có ở môi trường global; project dùng `.venv` riêng.
- FFmpeg CLI/FFprobe: chưa có trên `PATH`.
- LaTeX (`latex`, `pdflatex`, `xelatex`) và `dvisvgm`: chưa có.
- Font có sẵn: Segoe UI và Arial; code còn fallback sang DejaVu Sans.

Manim 0.20.1 dùng PyAV nên không cần executable `ffmpeg` để render scene cơ bản.
FFmpeg CLI vẫn cần cho bước ghép. LaTeX là tùy chọn; smoke test chỉ dùng `Text`,
không dùng `Tex`/`MathTex`.

### Cài FFmpeg CLI (cần cho ghép video)

```powershell
winget install --id Gyan.FFmpeg -e
```

Mở terminal mới rồi kiểm tra:

```powershell
ffmpeg -version
ffprobe -version
```

### Cài LaTeX (chỉ cần khi scene dùng công thức)

Manim Community khuyến nghị MiKTeX trên Windows:

```powershell
winget install --id MiKTeX.MiKTeX -e
```

Trong MiKTeX Console, bật tự động cài package còn thiếu. Mở terminal mới và kiểm tra:

```powershell
latex --version
dvisvgm --version
```

## 7. Kiến trúc ngắn gọn

- `config.py`: resolution/FPS final, font fallback, cỡ chữ, spacing, palette ngữ nghĩa.
- `common.py`: component hình học và typography dùng lại giữa các scene.
- `PRODUCTION_GUIDE.md`: production contract cho style, scene, transition và naming.
- `scripts/SCENE_TEMPLATE.md`: template beat-by-beat cho narration/storyboard.
- `scenes/`: một file cho mỗi scene; `smoke_test.py` tách khỏi 10 scene production.
- `assets/`: paper-derived crops, ảnh, SVG và audio có nguồn rõ ràng.
- `subtitles/`: phụ đề theo scene.
- `render_all.py`: render tuần tự và tùy chọn ghép video.
- `output/`: toàn bộ artifact render; không đặt source code tại đây.

Không dùng hình/thiết kế sao chép từ 3Blue1Brown. Chỉ học cách ưu tiên trực giác,
nhịp giải thích và hình học rõ ràng.
