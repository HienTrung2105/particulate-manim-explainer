"""Scene 08: distinguish training supervision from inference assembly."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MovingCameraScene,
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
    LABEL_FONT_SIZE,
    MUTED_TEXT_COLOR,
    OUTPUT_COLOR,
    PRISMATIC_JOINT_COLOR,
    REVOLUTE_JOINT_COLOR,
    TEXT_COLOR,
    apply_project_style,
)

apply_project_style()


class Scene08TrainingInference(MovingCameraScene):
    """Show query matching, multi-task learning, and inference post-processing."""

    def _hold_until(self, target_time: float) -> None:
        remaining = target_time - self.time
        if remaining < -0.05:
            raise RuntimeError(f"Scene 08 exceeded {target_time:.2f}s at {self.time:.2f}s")
        if remaining > 0:
            self.wait(remaining)

    @staticmethod
    def _text(label: str, *, size: int = LABEL_FONT_SIZE, color: str = TEXT_COLOR) -> Text:
        return Text(label, font=DEFAULT_FONT, font_size=size, color=color)

    def _title(self, label: str, *, color: str = TEXT_COLOR) -> Text:
        return create_scene_title(label, color=color)

    @staticmethod
    def _prediction_group() -> VGroup:
        cabinet = create_cabinet_diagram(scale_factor=0.58).move_to(LEFT * 1.6)
        tree = create_kinematic_tree().scale(0.48).move_to(RIGHT * 1.45 + UP * 0.2)
        axis = create_rotation_axis(length=1.3).scale(0.55).move_to(LEFT * 0.8)
        slider = create_sliding_arrow(length=1.25).scale(0.60).move_to(LEFT * 1.4 + DOWN * 1.0)
        return VGroup(cabinet, tree, axis, slider)

    def construct(self) -> None:
        citation = create_footer_citation(
            "Li et al., PARTICULATE, CVPR 2026 — Sec. 3.4–3.5; Sec. 4.1",
            max_width=11.6,
        ).to_edge(DOWN, buff=0.24)
        prediction = self._prediction_group()
        prediction_card = create_pipeline_box(
            "PREDICTION", color=OUTPUT_COLOR, width=7.1, height=4.25
        )
        prediction.move_to(prediction_card)
        self.add(prediction_card[0], prediction, citation)

        # 00:00–00:13 — the same system has training and inference phases.
        training = create_pipeline_box(
            "TRAINING", color=ACCENT_COLOR, width=3.2, height=1.15
        ).move_to(LEFT * 2.6)
        inference = create_pipeline_box(
            "INFERENCE", color=OUTPUT_COLOR, width=3.2, height=1.15
        ).move_to(RIGHT * 2.6)
        split_title = self._title("LEARN TOGETHER — ASSEMBLE AT TEST TIME", color=TEXT_COLOR)
        self.play(
            FadeOut(VGroup(prediction_card[0], prediction)),
            FadeIn(split_title),
            FadeIn(training, shift=RIGHT * 0.08),
            FadeIn(inference, shift=LEFT * 0.08),
            run_time=0.9,
        )
        self.play(Indicate(training, color=ACCENT_COLOR), run_time=0.65)
        self._hold_until(13)

        # 00:13–00:34 — supervised tuple S, K, M.
        gt_title = self._title("GROUND TRUTH: SEGMENTATION + TREE + MOTION", color=ACCENT_COLOR)
        gt_cabinet = create_cabinet_diagram(scale_factor=0.72).move_to(LEFT * 3.4 + DOWN * 0.1)
        gt_tree = create_kinematic_tree().scale(0.58).move_to(RIGHT * 0.15 + UP * 0.15)
        gt_motion = (
            VGroup(
                create_rotation_axis(length=1.5).scale(0.62),
                create_sliding_arrow(length=1.55).scale(0.65),
            )
            .arrange(DOWN, buff=0.55)
            .move_to(RIGHT * 4.15)
        )
        self.play(
            FadeOut(VGroup(training, inference)),
            ReplacementTransform(split_title, gt_title),
            FadeIn(gt_cabinet),
            run_time=0.8,
        )
        self.play(FadeIn(gt_tree), run_time=0.65)
        self.play(FadeIn(gt_motion), run_time=0.65)
        self._hold_until(34)

        # 00:34–00:52 — Hungarian query-to-part matching during training.
        match_title = self._title("HUNGARIAN MATCHING", color=ACCENT_COLOR)
        queries = (
            VGroup(*[create_concept_token(f"Q{i}", color=ACCENT_COLOR) for i in range(1, 5)])
            .arrange(DOWN, buff=0.24)
            .move_to(LEFT * 3.0)
        )
        gt_parts = (
            VGroup(
                create_concept_token("BODY", color=FIXED_PART_COLOR),
                create_concept_token("DOOR", color=REVOLUTE_JOINT_COLOR),
                create_concept_token("DRAWER", color=PRISMATIC_JOINT_COLOR),
            )
            .arrange(DOWN, buff=0.35)
            .move_to(RIGHT * 3.0)
        )
        crossing = VGroup(
            DashedLine(queries[0].get_right(), gt_parts[2].get_left(), color=MUTED_TEXT_COLOR),
            DashedLine(queries[1].get_right(), gt_parts[0].get_left(), color=MUTED_TEXT_COLOR),
            DashedLine(queries[2].get_right(), gt_parts[1].get_left(), color=MUTED_TEXT_COLOR),
        )
        matched = VGroup(
            Arrow(
                queries[0].get_right(), gt_parts[0].get_left(), buff=0.16, color=FIXED_PART_COLOR
            ),
            Arrow(
                queries[1].get_right(),
                gt_parts[1].get_left(),
                buff=0.16,
                color=REVOLUTE_JOINT_COLOR,
            ),
            Arrow(
                queries[2].get_right(),
                gt_parts[2].get_left(),
                buff=0.16,
                color=PRISMATIC_JOINT_COLOR,
            ),
        )
        self.play(
            FadeOut(VGroup(gt_cabinet, gt_tree, gt_motion)),
            ReplacementTransform(gt_title, match_title),
            FadeIn(queries),
            FadeIn(gt_parts),
            Create(crossing),
            run_time=0.9,
        )
        self.play(ReplacementTransform(crossing, matched), run_time=0.9)
        self._hold_until(52)

        # 00:52–01:07 — compact multi-task loss view.
        loss_title = self._title("MULTI-TASK LOSS", color=ACCENT_COLOR)
        losses = (
            VGroup(
                *[
                    create_pipeline_box(label, color=color, width=2.55, height=0.70)
                    for label, color in (
                        ("SEGMENTATION", OUTPUT_COLOR),
                        ("KINEMATIC TREE", FIXED_PART_COLOR),
                        ("MOTION TYPE", ACCENT_COLOR),
                        ("AXIS + RANGE", REVOLUTE_JOINT_COLOR),
                    )
                ]
            )
            .arrange_in_grid(rows=2, cols=2, buff=0.45)
            .move_to(DOWN * 0.05)
        )
        total = create_pipeline_box(
            "JOINT OPTIMIZATION", color=ACCENT_COLOR, width=3.4, height=0.78
        ).next_to(losses, DOWN, buff=0.35)
        arrows = VGroup(
            *[
                Arrow(loss.get_bottom(), total.get_top(), buff=0.10, color=ACCENT_COLOR)
                for loss in losses
            ]
        )
        self.play(
            FadeOut(VGroup(queries, gt_parts, matched)),
            ReplacementTransform(match_title, loss_title),
            LaggedStart(*(FadeIn(loss) for loss in losses), lag_ratio=0.18),
            run_time=0.9,
        )
        self.play(Create(arrows), FadeIn(total), run_time=0.75)
        self._hold_until(67)

        # 01:07–01:19 — datasets and sampled articulated states.
        data_title = self._title("TRAINING DATA", color=ACCENT_COLOR)
        datasets = (
            VGroup(
                create_pipeline_box("PARTNET-MOBILITY", color=ACCENT_COLOR, width=3.2, height=0.90),
                create_pipeline_box("GRSCENES", color=ACCENT_COLOR, width=3.2, height=0.90),
            )
            .arrange(RIGHT, buff=0.75)
            .move_to(UP * 0.75)
        )
        state_cabinet = create_cabinet_diagram(scale_factor=0.58).move_to(DOWN * 1.0)
        state_label = self._text("RANDOM ARTICULATED STATE", color=MUTED_TEXT_COLOR).next_to(
            state_cabinet, RIGHT, buff=0.45
        )
        self.play(
            FadeOut(VGroup(losses, arrows, total)),
            ReplacementTransform(loss_title, data_title),
            FadeIn(datasets),
            FadeIn(state_cabinet),
            FadeIn(state_label),
            run_time=0.85,
        )
        self.play(state_cabinet.drawer.animate.shift(RIGHT * 0.45), run_time=0.65)
        self._hold_until(79)

        # 01:19–01:35 — point labels become face labels; retain active parts only.
        infer_title = self._title("INFERENCE: RAW PREDICTIONS → PRESENT PARTS", color=OUTPUT_COLOR)
        point_tokens = (
            VGroup(
                *(
                    Dot(radius=0.07, color=color)
                    for color in (
                        FIXED_PART_COLOR,
                        REVOLUTE_JOINT_COLOR,
                        PRISMATIC_JOINT_COLOR,
                        FIXED_PART_COLOR,
                        REVOLUTE_JOINT_COLOR,
                        PRISMATIC_JOINT_COLOR,
                    )
                )
            )
            .arrange_in_grid(rows=2, cols=3, buff=0.30)
            .move_to(LEFT * 4.1)
        )
        face_cabinet = create_cabinet_diagram(scale_factor=0.55).move_to(DOWN * 0.05)
        present = (
            VGroup(
                create_concept_token("BODY", color=FIXED_PART_COLOR),
                create_concept_token("DOOR", color=REVOLUTE_JOINT_COLOR),
                create_concept_token("DRAWER", color=PRISMATIC_JOINT_COLOR),
            )
            .arrange(DOWN, buff=0.20)
            .move_to(RIGHT * 4.0)
        )
        flow = VGroup(
            Arrow(point_tokens.get_right(), face_cabinet.get_left(), buff=0.25, color=OUTPUT_COLOR),
            Arrow(face_cabinet.get_right(), present.get_left(), buff=0.25, color=OUTPUT_COLOR),
        )
        self.play(
            FadeOut(VGroup(datasets, state_cabinet, state_label)),
            ReplacementTransform(data_title, infer_title),
            FadeIn(point_tokens),
            Create(flow[0]),
            FadeIn(face_cabinet),
            Create(flow[1]),
            FadeIn(present),
            run_time=1.0,
        )
        self._hold_until(95)

        # 01:35–01:49 — Edmonds extracts the maximum spanning arborescence.
        tree_title = self._title("EDMONDS: MAXIMUM SPANNING ARBORESCENCE", color=OUTPUT_COLOR)
        candidate_nodes = (
            VGroup(
                create_concept_token("BODY", color=FIXED_PART_COLOR),
                create_concept_token("DOOR", color=REVOLUTE_JOINT_COLOR),
                create_concept_token("DRAWER", color=PRISMATIC_JOINT_COLOR),
            )
            .arrange(RIGHT, buff=0.80)
            .move_to(UP * 0.55)
        )
        candidate_edges = VGroup(
            Arrow(
                candidate_nodes[0].get_bottom(),
                candidate_nodes[1].get_bottom(),
                buff=0.15,
                color=REVOLUTE_JOINT_COLOR,
            ),
            Arrow(
                candidate_nodes[0].get_bottom(),
                candidate_nodes[2].get_bottom(),
                buff=0.15,
                color=PRISMATIC_JOINT_COLOR,
            ),
            Arrow(
                candidate_nodes[2].get_top(),
                candidate_nodes[1].get_top(),
                buff=0.15,
                color=MUTED_TEXT_COLOR,
            ),
        )
        valid_tree = create_kinematic_tree().scale(0.82).move_to(DOWN * 0.30)
        self.play(
            FadeOut(VGroup(point_tokens, face_cabinet, present, flow)),
            ReplacementTransform(infer_title, tree_title),
            FadeIn(candidate_nodes),
            Create(candidate_edges),
            run_time=0.85,
        )
        self.play(
            ReplacementTransform(VGroup(candidate_nodes, candidate_edges), valid_tree), run_time=0.8
        )
        self._hold_until(109)

        # 01:49–01:57 — coordinate-wise median aggregates axis-location votes.
        median_title = self._title("MEDIAN AXIS VOTE", color=REVOLUTE_JOINT_COLOR)
        votes = VGroup(
            *[
                Dot(
                    LEFT * 2.2 + UP * y_value + RIGHT * x_value,
                    radius=0.08,
                    color=REVOLUTE_JOINT_COLOR,
                )
                for x_value, y_value in (
                    (0.0, -0.9),
                    (0.25, -0.4),
                    (-0.15, 0.0),
                    (0.12, 0.45),
                    (-0.05, 0.9),
                )
            ]
        )
        median = Dot(RIGHT * 1.1, radius=0.13, color=ACCENT_COLOR)
        vote_lines = VGroup(
            *(
                Line(vote.get_center(), median.get_center(), color=REVOLUTE_JOINT_COLOR)
                for vote in votes
            )
        )
        axis = create_rotation_axis(length=2.1).scale(0.8).move_to(RIGHT * 2.5)
        self.play(
            FadeOut(valid_tree),
            ReplacementTransform(tree_title, median_title),
            FadeIn(votes),
            Create(vote_lines),
            FadeIn(median),
            FadeIn(axis),
            run_time=0.9,
        )
        self._hold_until(117)

        # 01:57–02:00 — assembled articulated output handoff.
        output_title = self._title("OUTPUT", color=OUTPUT_COLOR)
        output = self._prediction_group().scale(1.05).move_to(DOWN * 0.10)
        self.play(
            FadeOut(VGroup(votes, vote_lines, median, axis, median_title)),
            FadeIn(output_title),
            FadeIn(output),
            run_time=0.8,
        )
        self._hold_until(119.0)
