"""Scene 06: explain articulated-part segmentation from points to mesh faces."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    MoveToTarget,
    MovingCameraScene,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    Text,
    VGroup,
)

from common import (
    create_cabinet_diagram,
    create_footer_citation,
    create_kinematic_tree,
    create_part_label,
    create_pipeline_box,
    create_rotation_axis,
    create_scene_title,
)
from config import (
    ACCENT_COLOR,
    DEFAULT_FONT,
    FIXED_PART_COLOR,
    INPUT_COLOR,
    LABEL_FONT_SIZE,
    MUTED_TEXT_COLOR,
    OUTPUT_COLOR,
    PRISMATIC_JOINT_COLOR,
    REVOLUTE_JOINT_COLOR,
    TEXT_COLOR,
    apply_project_style,
)

apply_project_style()


class Scene06Segmentation(MovingCameraScene):
    """Turn point-query scores into articulation-aware mesh parts."""

    def _hold_until(self, target_time: float) -> None:
        remaining = target_time - self.time
        if remaining < -0.05:
            raise RuntimeError(f"Scene 06 exceeded {target_time:.2f}s at {self.time:.2f}s")
        if remaining > 0:
            self.wait(remaining)

    @staticmethod
    def _text(label: str, *, size: int = LABEL_FONT_SIZE, color: str = TEXT_COLOR) -> Text:
        return Text(label, font=DEFAULT_FONT, font_size=size, color=color)

    def _title(self, label: str, *, color: str = TEXT_COLOR) -> Text:
        return create_scene_title(label, color=color)

    @staticmethod
    def _point_cloud(*, colored: bool = False) -> VGroup:
        points = VGroup()
        for row, y_value in enumerate((-1.35, -0.95, -0.55, -0.15, 0.25, 0.65, 1.05, 1.35)):
            for column, x_value in enumerate((-1.05, -0.70, -0.35, 0.0, 0.35, 0.70, 1.05)):
                color = INPUT_COLOR
                if colored:
                    if column <= 2 and row >= 2:
                        color = REVOLUTE_JOINT_COLOR
                    elif column >= 3 and row <= 2:
                        color = PRISMATIC_JOINT_COLOR
                    else:
                        color = FIXED_PART_COLOR
                points.add(Dot(RIGHT * x_value + UP * y_value, radius=0.045, color=color))
        return points

    def construct(self) -> None:
        citation = create_footer_citation(
            "Li et al., PARTICULATE, CVPR 2026 — Sec. 3.3 & 3.5",
            max_width=11.6,
        ).to_edge(DOWN, buff=0.24)

        # 00:00–00:15 — recreate and enter Scene 5's highlighted head.
        heads = (
            VGroup(
                create_pipeline_box(
                    "PART SEGMENTATION", color=OUTPUT_COLOR, width=3.25, height=0.72
                ),
                create_pipeline_box("KINEMATIC TREE", color=OUTPUT_COLOR, width=3.25, height=0.72),
                create_pipeline_box(
                    "ARTICULATION TYPE", color=OUTPUT_COLOR, width=3.25, height=0.72
                ),
                create_pipeline_box(
                    "ARTICULATION AXIS", color=OUTPUT_COLOR, width=3.25, height=0.72
                ),
                create_pipeline_box(
                    "ARTICULATION RANGE", color=OUTPUT_COLOR, width=3.25, height=0.72
                ),
            )
            .arrange(DOWN, buff=0.18)
            .move_to(RIGHT * 2.7)
        )
        heads[1:].set_opacity(0.34)
        query_dots = (
            VGroup(*(Dot(radius=0.09, color=ACCENT_COLOR) for _ in range(5)))
            .arrange(RIGHT, buff=0.28)
            .move_to(LEFT * 3.0)
        )
        into_head = Arrow(
            query_dots.get_right(), heads[0].get_left(), buff=0.24, color=OUTPUT_COLOR
        )
        highlight = RoundedRectangle(
            width=heads[0].width + 0.22,
            height=heads[0].height + 0.18,
            corner_radius=0.14,
            color=OUTPUT_COLOR,
            stroke_width=4,
        ).move_to(heads[0])
        self.add(query_dots, heads, into_head, highlight, citation)
        self.wait(0.4)
        self.play(Indicate(heads[0], color=OUTPUT_COLOR), run_time=0.7)
        cloud = self._point_cloud().scale(0.9).move_to(LEFT * 2.7 + DOWN * 0.05)
        active_queries = query_dots.copy().arrange(DOWN, buff=0.30).move_to(RIGHT * 2.6)
        title = self._title("EACH POINT → ONE PART QUERY", color=OUTPUT_COLOR)
        self.play(
            FadeOut(VGroup(heads[1:], into_head, highlight)),
            ReplacementTransform(heads[0], title),
            ReplacementTransform(query_dots, active_queries),
            FadeIn(cloud),
            run_time=0.9,
        )
        self._hold_until(15)

        # 00:15–00:38 — representative N × Pmax score matrix.
        matrix_title = self._title("POINTS × PART QUERIES", color=ACCENT_COLOR)
        cells = VGroup()
        for row in range(5):
            for column in range(4):
                opacity = 0.65 if column == (row % 3) else 0.10
                cells.add(
                    Rectangle(
                        width=0.62,
                        height=0.54,
                        color=ACCENT_COLOR,
                        fill_color=ACCENT_COLOR,
                        fill_opacity=opacity,
                        stroke_opacity=0.45,
                    )
                )
        cells.arrange_in_grid(rows=5, cols=4, buff=0.08).move_to(RIGHT * 1.0 + DOWN * 0.10)
        row_label = self._text("POINTS", color=INPUT_COLOR).next_to(cells, LEFT, buff=0.40)
        col_label = self._text("PART QUERIES", color=ACCENT_COLOR).next_to(cells, UP, buff=0.26)
        sampled = VGroup(*[cloud[index].copy() for index in (3, 10, 22, 34, 47)])
        sampled.generate_target()
        sampled.target.arrange(DOWN, buff=0.33).next_to(cells, LEFT, buff=0.75)
        self.play(
            ReplacementTransform(title, matrix_title),
            FadeOut(active_queries),
            cloud.animate.set_opacity(0.24),
            sampled.animate.move_to(sampled.target),
            FadeIn(cells),
            FadeIn(row_label),
            FadeIn(col_label),
            run_time=1.0,
        )
        winner_boxes = VGroup(
            *[
                Rectangle(width=0.70, height=0.62, color=OUTPUT_COLOR, stroke_width=3).move_to(
                    cells[i * 4 + i % 3]
                )
                for i in range(5)
            ]
        )
        self.play(LaggedStart(*(Create(box) for box in winner_boxes), lag_ratio=0.18), run_time=1.0)
        self._hold_until(38)

        # 00:38–01:00 — argmax assignments form articulated clusters.
        cluster_title = self._title("POINT LABELS", color=OUTPUT_COLOR)
        colored_cloud = self._point_cloud(colored=True).scale(0.9).move_to(DOWN * 0.05)
        legend = (
            VGroup(
                create_part_label("Fixed body", color=FIXED_PART_COLOR),
                create_part_label("Door", color=REVOLUTE_JOINT_COLOR),
                create_part_label("Drawer", color=PRISMATIC_JOINT_COLOR),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            .move_to(RIGHT * 4.25)
        )
        self.play(
            FadeOut(VGroup(cells, row_label, col_label, sampled, winner_boxes, cloud)),
            ReplacementTransform(matrix_title, cluster_title),
            FadeIn(colored_cloud),
            run_time=0.9,
        )
        self.play(
            LaggedStart(*(FadeIn(item, shift=LEFT * 0.08) for item in legend), lag_ratio=0.22),
            run_time=0.9,
        )
        self.play(Indicate(colored_cloud, color=OUTPUT_COLOR, scale_factor=1.02), run_time=0.7)
        self._hold_until(60)

        # 01:00–01:20 — point predictions are lifted back to mesh faces.
        face_title = self._title("POINT LABELS → FACE LABELS", color=OUTPUT_COLOR)
        cabinet = create_cabinet_diagram(scale_factor=0.92).move_to(RIGHT * 2.65 + DOWN * 0.12)
        colored_cloud.generate_target()
        colored_cloud.target.scale(0.70).move_to(LEFT * 3.05 + DOWN * 0.12)
        map_arrow = Arrow(LEFT * 1.45, RIGHT * 1.30, color=OUTPUT_COLOR, stroke_width=4)
        self.play(
            ReplacementTransform(cluster_title, face_title),
            FadeOut(legend),
            colored_cloud.animate.move_to(colored_cloud.target),
            Create(map_arrow),
            FadeIn(cabinet),
            run_time=1.0,
        )
        self.play(Indicate(cabinet.door, color=REVOLUTE_JOINT_COLOR), run_time=0.6)
        self.play(Indicate(cabinet.drawer, color=PRISMATIC_JOINT_COLOR), run_time=0.6)
        self._hold_until(80)

        # 01:20–01:39 — majority vote on a representative face.
        vote_title = self._title("MAJORITY VOTE ON EACH FACE", color=ACCENT_COLOR)
        face = Rectangle(
            width=3.2,
            height=2.1,
            color=MUTED_TEXT_COLOR,
            fill_color=FIXED_PART_COLOR,
            fill_opacity=0.08,
        ).move_to(LEFT * 1.0)
        votes = VGroup(
            Dot(face.get_center() + LEFT * 0.65, radius=0.13, color=REVOLUTE_JOINT_COLOR),
            Dot(face.get_center() + UP * 0.48, radius=0.13, color=REVOLUTE_JOINT_COLOR),
            Dot(
                face.get_center() + RIGHT * 0.68 + DOWN * 0.30, radius=0.13, color=FIXED_PART_COLOR
            ),
        )
        result = create_part_label("Door wins: 2 / 3", color=REVOLUTE_JOINT_COLOR).move_to(
            RIGHT * 3.0
        )
        self.play(
            FadeOut(VGroup(colored_cloud, map_arrow, cabinet)),
            ReplacementTransform(face_title, vote_title),
            FadeIn(face),
            FadeIn(votes),
            run_time=0.8,
        )
        self.play(
            FadeIn(result, shift=LEFT * 0.10),
            face.animate.set_fill(REVOLUTE_JOINT_COLOR, opacity=0.28),
            run_time=0.8,
        )
        self._hold_until(99)

        # 01:39–01:59 — connected-component refinement is explicit post-processing.
        refine_title = self._title("CONNECTED-COMPONENT REFINEMENT", color=ACCENT_COLOR)
        refined = create_cabinet_diagram(scale_factor=0.96).move_to(DOWN * 0.12)
        noisy_patches = VGroup(
            Rectangle(width=0.28, height=0.28, color=PRISMATIC_JOINT_COLOR, fill_opacity=0.75),
            Rectangle(width=0.24, height=0.24, color=FIXED_PART_COLOR, fill_opacity=0.75),
        )
        noisy_patches[0].move_to(refined.door_panel.get_center() + UP * 0.25)
        noisy_patches[1].move_to(refined.drawer_panel.get_center() + LEFT * 0.22)
        note = self._text(
            "LARGEST SURFACE COVERAGE IN EACH COMPONENT", color=MUTED_TEXT_COLOR
        ).next_to(refined, DOWN, buff=0.38)
        self.play(
            FadeOut(VGroup(face, votes, result)),
            ReplacementTransform(vote_title, refine_title),
            FadeIn(refined),
            FadeIn(noisy_patches),
            FadeIn(note),
            run_time=0.9,
        )
        self.play(FadeOut(noisy_patches), Indicate(refined, color=OUTPUT_COLOR), run_time=0.8)
        self._hold_until(119)

        # 01:59–02:18 — parts are the substrate for structure and motion.
        structure_title = self._title("ARTICULATED PARTS, NOT SEMANTIC CLASSES", color=OUTPUT_COLOR)
        refined.generate_target()
        refined.target.scale(0.76).move_to(LEFT * 3.65 + DOWN * 0.05)
        tree = create_kinematic_tree().scale(0.62).move_to(RIGHT * 3.15 + UP * 0.48)
        axis = create_rotation_axis(length=1.55).scale(0.68).next_to(tree, DOWN, buff=0.28)
        connector = Arrow(
            refined.target.get_right(), tree.get_left(), buff=0.35, color=OUTPUT_COLOR
        )
        self.play(
            ReplacementTransform(refine_title, structure_title),
            FadeOut(note),
            MoveToTarget(refined),
            Create(connector),
            FadeIn(tree),
            FadeIn(axis),
            run_time=1.0,
        )
        self._hold_until(138)

        # 02:18–02:30 — clean segmented-cabinet handoff to Scene 7.
        final_cabinet = create_cabinet_diagram(scale_factor=1.10).move_to(DOWN * 0.05)
        final_title = self._title("THREE PARTS — WHAT JOINS THEM?", color=ACCENT_COLOR)
        self.play(
            FadeOut(VGroup(refined, tree, axis, connector, structure_title)),
            FadeIn(final_cabinet),
            FadeIn(final_title),
            run_time=0.9,
        )
        self._hold_until(149.0)
