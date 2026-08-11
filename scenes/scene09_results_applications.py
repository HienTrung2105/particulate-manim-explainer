"""Scene 09: summarize evaluation evidence and supported applications."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    MovingCameraScene,
    Rectangle,
    ReplacementTransform,
    Text,
    VGroup,
)

from common import (
    create_cabinet_diagram,
    create_concept_token,
    create_footer_citation,
    create_kinematic_tree,
    create_pipeline_box,
    create_rotation_axis,
    create_scene_title,
    create_sliding_arrow,
)
from config import (
    ACCENT_COLOR,
    DEFAULT_FONT,
    FIXED_PART_COLOR,
    INPUT_COLOR,
    LABEL_FONT_SIZE,
    MUTED_TEXT_COLOR,
    OUTPUT_COLOR,
    REVOLUTE_JOINT_COLOR,
    TEXT_COLOR,
    apply_project_style,
)

apply_project_style()


class Scene09ResultsApplications(MovingCameraScene):
    """Present reported comparisons without reproducing dense paper tables."""

    def _hold_until(self, target_time: float) -> None:
        remaining = target_time - self.time
        if remaining < -0.05:
            raise RuntimeError(f"Scene 09 exceeded {target_time:.2f}s at {self.time:.2f}s")
        if remaining > 0:
            self.wait(remaining)

    @staticmethod
    def _text(label: str, *, size: int = LABEL_FONT_SIZE, color: str = TEXT_COLOR) -> Text:
        return Text(label, font=DEFAULT_FONT, font_size=size, color=color)

    def _title(self, label: str, *, color: str = TEXT_COLOR) -> Text:
        return create_scene_title(label, color=color)

    @staticmethod
    def _output_object(*, scale_factor: float = 1.0) -> VGroup:
        cabinet = create_cabinet_diagram(scale_factor=0.72).move_to(LEFT * 1.45)
        tree = create_kinematic_tree().scale(0.50).move_to(RIGHT * 1.55 + UP * 0.25)
        axis = create_rotation_axis(length=1.35).scale(0.55).move_to(LEFT * 0.65)
        slider = create_sliding_arrow(length=1.30).scale(0.58).move_to(LEFT * 1.30 + DOWN * 1.15)
        return VGroup(cabinet, tree, axis, slider).scale(scale_factor)

    def _comparison_chart(self, *, full: bool = False) -> VGroup:
        labels = ("gIoU", "PC ↓", "OC ↓") if full else ("gIoU", "PC ↓", "mIoU")
        baseline = (0.50, 0.58, 0.52) if full else (0.52, 0.62, 0.55)
        ours = (0.88, 0.82, 0.86)
        rows = VGroup()
        for index, (label, old_value, our_value) in enumerate(
            zip(labels, baseline, ours, strict=True)
        ):
            metric = self._text(label, color=MUTED_TEXT_COLOR).move_to(
                LEFT * 4.6 + UP * (1.0 - index)
            )
            old = Rectangle(
                width=old_value * 4.2,
                height=0.30,
                color=FIXED_PART_COLOR,
                fill_color=FIXED_PART_COLOR,
                fill_opacity=0.55,
                stroke_width=0,
            ).next_to(metric, RIGHT, buff=0.35)
            ours_bar = Rectangle(
                width=our_value * 4.2,
                height=0.30,
                color=OUTPUT_COLOR,
                fill_color=OUTPUT_COLOR,
                fill_opacity=0.85,
                stroke_width=0,
            ).next_to(old, DOWN, buff=0.12, aligned_edge=LEFT)
            rows.add(VGroup(metric, old, ours_bar))
        legend = (
            VGroup(
                self._text("BEST BASELINE", color=FIXED_PART_COLOR),
                self._text("PARTICULATE", color=OUTPUT_COLOR),
            )
            .arrange(RIGHT, buff=0.65)
            .next_to(rows, DOWN, buff=0.42)
        )
        return VGroup(rows, legend).move_to(DOWN * 0.10)

    def construct(self) -> None:
        citation = create_footer_citation(
            "Li et al., PARTICULATE, CVPR 2026 — Sec. 4; Tables 2–4",
            max_width=11.6,
        ).to_edge(DOWN, buff=0.24)
        output = self._output_object(scale_factor=1.05).move_to(DOWN * 0.05)
        output_title = self._title("OUTPUT", color=OUTPUT_COLOR)
        self.add(output_title, output, citation)

        # 00:00–00:18 — split evaluation into its two reported subtasks.
        eval_title = self._title("DOES THE WHOLE ARTICULATION HOLD UP?", color=ACCENT_COLOR)
        lanes = (
            VGroup(
                create_pipeline_box(
                    "PART SEGMENTATION", color=OUTPUT_COLOR, width=3.5, height=1.05
                ),
                create_pipeline_box(
                    "FULL ARTICULATION", color=OUTPUT_COLOR, width=3.5, height=1.05
                ),
            )
            .arrange(RIGHT, buff=0.85)
            .move_to(DOWN * 0.05)
        )
        self.play(
            FadeOut(output),
            ReplacementTransform(output_title, eval_title),
            LaggedStart(*(FadeIn(lane) for lane in lanes), lag_ratio=0.25),
            run_time=1.0,
        )
        self._hold_until(18)

        # 00:18–00:42 — evaluation sets and their verified scope.
        data_title = self._title("TWO EVALUATION SETS", color=ACCENT_COLOR)
        datasets = (
            VGroup(
                create_pipeline_box(
                    "PARTNET-MOBILITY\n7 CATEGORIES", color=ACCENT_COLOR, width=4.1, height=1.45
                ),
                create_pipeline_box(
                    "LIGHTWHEEL\n243 OBJECTS · 14 CATEGORIES",
                    color=ACCENT_COLOR,
                    width=4.8,
                    height=1.45,
                ),
            )
            .arrange(RIGHT, buff=0.55)
            .move_to(DOWN * 0.05)
        )
        license_note = self._text("Lightwheel: CC BY-NC", color=MUTED_TEXT_COLOR).next_to(
            datasets[1], DOWN, buff=0.28
        )
        self.play(
            FadeOut(lanes),
            ReplacementTransform(eval_title, data_title),
            FadeIn(datasets[0]),
            run_time=0.8,
        )
        self.play(FadeIn(datasets[1]), FadeIn(license_note), run_time=0.8)
        self._hold_until(42)

        # 00:42–01:08 — redraw only the ranking conveyed by Table 2.
        seg_title = self._title("PART SEGMENTATION — BEST ON BOTH SETS", color=OUTPUT_COLOR)
        seg_chart = self._comparison_chart()
        method_line = self._text(
            "Naive · PartField · P3SAM · SINGAPO · Articulate AnyMesh",
            color=MUTED_TEXT_COLOR,
        ).next_to(seg_chart, UP, buff=0.28)
        self.play(
            FadeOut(VGroup(datasets, license_note)),
            ReplacementTransform(data_title, seg_title),
            FadeIn(method_line),
            LaggedStart(*(Create(row[1]) for row in seg_chart[0]), lag_ratio=0.15),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*(Create(row[2]) for row in seg_chart[0]), lag_ratio=0.15),
            FadeIn(seg_chart[1]),
            run_time=1.0,
        )
        self._hold_until(68)

        # 01:08–01:24 — surface privileged inputs used by selected baselines.
        condition_title = self._title("READ THE TEST CONDITIONS", color=ACCENT_COLOR)
        badges = (
            VGroup(
                create_concept_token("PARTFIELD: GT PART COUNT", color=ACCENT_COLOR),
                create_concept_token("P3SAM: GT PART COUNT + POINT PROMPTS", color=ACCENT_COLOR),
            )
            .arrange(DOWN, buff=0.42)
            .move_to(DOWN * 0.05)
        )
        self.play(
            FadeOut(VGroup(seg_chart, method_line)),
            ReplacementTransform(seg_title, condition_title),
            LaggedStart(*(FadeIn(badge, shift=LEFT * 0.10) for badge in badges), lag_ratio=0.30),
            run_time=0.9,
        )
        self._hold_until(84)

        # 01:24–01:50 — full articulation comparisons use moved geometries.
        full_title = self._title("FULL ARTICULATION — BEST ACROSS ALL METRICS", color=OUTPUT_COLOR)
        full_chart = self._comparison_chart(full=True)
        layers = (
            VGroup(
                create_concept_token("PARTS", color=OUTPUT_COLOR),
                create_concept_token("TREE", color=FIXED_PART_COLOR),
                create_concept_token("MOTION", color=REVOLUTE_JOINT_COLOR),
            )
            .arrange(RIGHT, buff=0.32)
            .next_to(full_chart, UP, buff=0.30)
        )
        self.play(
            FadeOut(badges),
            ReplacementTransform(condition_title, full_title),
            FadeIn(layers),
            LaggedStart(*(Create(row[1]) for row in full_chart[0]), lag_ratio=0.12),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*(Create(row[2]) for row in full_chart[0]), lag_ratio=0.12),
            FadeIn(full_chart[1]),
            run_time=0.9,
        )
        self._hold_until(110)

        # 01:50–02:10 — preserve the GT-range caveat for AnyMesh.
        range_title = self._title("A CRITICAL COMPARISON DETAIL", color=ACCENT_COLOR)
        anymesh = create_pipeline_box(
            "ARTICULATE ANYMESH", color=FIXED_PART_COLOR, width=4.1, height=1.0
        )
        range_badge = create_concept_token("GIVEN GT MOTION RANGE", color=ACCENT_COLOR)
        caveat = VGroup(anymesh, range_badge).arrange(DOWN, buff=0.42).move_to(DOWN * 0.05)
        self.play(
            FadeOut(VGroup(full_chart, layers)),
            ReplacementTransform(full_title, range_title),
            FadeIn(anymesh),
            run_time=0.8,
        )
        self.play(
            FadeIn(range_badge, shift=UP * 0.10),
            Indicate(range_badge, color=ACCENT_COLOR),
            run_time=0.9,
        )
        self._hold_until(130)

        # 02:10–02:37 — original geometry stands in for reported Hunyuan3D examples.
        gen_title = self._title("GENERALIZATION TO AI-GENERATED MESHES", color=OUTPUT_COLOR)
        static = (
            create_cabinet_diagram(scale_factor=0.58).set_color(INPUT_COLOR).move_to(LEFT * 4.2)
        )
        segmented = create_cabinet_diagram(scale_factor=0.58).move_to(DOWN * 0.05)
        articulated = create_cabinet_diagram(scale_factor=0.58).move_to(RIGHT * 4.2)
        articulated.door.rotate(-0.28, about_point=articulated.hinge_axis.get_center())
        articulated.drawer.shift(RIGHT * 0.42)
        gen_flow = VGroup(
            Arrow(static.get_right(), segmented.get_left(), buff=0.28, color=OUTPUT_COLOR),
            Arrow(segmented.get_right(), articulated.get_left(), buff=0.28, color=OUTPUT_COLOR),
        )
        gen_labels = VGroup(
            self._text("GENERATED MESH", color=INPUT_COLOR).next_to(static, DOWN, buff=0.28),
            self._text("PREDICTED PARTS", color=OUTPUT_COLOR).next_to(segmented, DOWN, buff=0.28),
            self._text("TWO STATES", color=OUTPUT_COLOR).next_to(articulated, DOWN, buff=0.28),
        )
        self.play(
            FadeOut(caveat),
            ReplacementTransform(range_title, gen_title),
            FadeIn(static),
            run_time=0.8,
        )
        self.play(Create(gen_flow[0]), FadeIn(segmented), run_time=0.8)
        self.play(Create(gen_flow[1]), FadeIn(articulated), FadeIn(gen_labels), run_time=0.9)
        self._hold_until(157)

        # 02:37–02:56 — report the two validated ablation findings qualitatively.
        ablation_title = self._title("WHAT MAKES THE MODEL STRONGER?", color=ACCENT_COLOR)
        toggles = (
            VGroup(
                create_pipeline_box(
                    "AXIS POINT VOTES\nIMPROVE AXIS ESTIMATION",
                    color=REVOLUTE_JOINT_COLOR,
                    width=4.5,
                    height=1.25,
                ),
                create_pipeline_box(
                    "PARTFIELD FEATURES\nADD GLOBAL + SEMANTIC CONTEXT",
                    color=ACCENT_COLOR,
                    width=4.8,
                    height=1.25,
                ),
            )
            .arrange(DOWN, buff=0.38)
            .move_to(DOWN * 0.05)
        )
        self.play(
            FadeOut(VGroup(static, segmented, articulated, gen_flow, gen_labels)),
            ReplacementTransform(gen_title, ablation_title),
            FadeIn(toggles[0]),
            run_time=0.8,
        )
        self.play(FadeIn(toggles[1]), run_time=0.8)
        self._hold_until(176)

        # 02:56–03:16 — supported composition with an off-the-shelf 3D generator.
        app_title = self._title("FROM IMAGE OR TEXT TO A SIMULATOR ASSET", color=OUTPUT_COLOR)
        pipeline = (
            VGroup(
                create_pipeline_box("IMAGE / TEXT", color=INPUT_COLOR, width=2.15, height=0.92),
                create_pipeline_box("3D GENERATOR", color=ACCENT_COLOR, width=2.25, height=0.92),
                create_pipeline_box("STATIC 3D", color=INPUT_COLOR, width=2.05, height=0.92),
                create_pipeline_box("PARTICULATE", color=OUTPUT_COLOR, width=2.25, height=0.92),
                create_pipeline_box("PHYSICS ASSET", color=OUTPUT_COLOR, width=2.35, height=0.92),
            )
            .arrange(RIGHT, buff=0.34)
            .move_to(DOWN * 0.05)
        )
        app_arrows = VGroup(
            *[
                Arrow(
                    pipeline[index].get_right(),
                    pipeline[index + 1].get_left(),
                    buff=0.08,
                    color=OUTPUT_COLOR,
                )
                for index in range(len(pipeline) - 1)
            ]
        )
        self.play(
            FadeOut(toggles),
            ReplacementTransform(ablation_title, app_title),
            LaggedStart(*(FadeIn(box) for box in pipeline), lag_ratio=0.14),
            LaggedStart(*(Create(arrow) for arrow in app_arrows), lag_ratio=0.14),
            run_time=1.2,
        )
        self._hold_until(196)

        # 03:16–03:30 — retain the articulated object for Scene 10.
        final_title = self._title("ARTICULATED 3D", color=OUTPUT_COLOR)
        final_object = self._output_object(scale_factor=1.12).move_to(DOWN * 0.05)
        self.play(
            FadeOut(VGroup(pipeline, app_arrows)),
            ReplacementTransform(app_title, final_title),
            FadeIn(final_object),
            run_time=0.9,
        )
        self._hold_until(209.0)
