"""Scene 07: assemble the kinematic tree and motion constraints."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arc,
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
    Rotate,
    Text,
    TransformFromCopy,
    VGroup,
)

from common import (
    create_cabinet_diagram,
    create_concept_token,
    create_footer_citation,
    create_kinematic_tree,
    create_part_label,
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


class Scene07JointMotion(MovingCameraScene):
    """Explain parent relations, joint types, axes, and relative ranges."""

    def _hold_until(self, target_time: float) -> None:
        remaining = target_time - self.time
        if remaining < -0.05:
            raise RuntimeError(f"Scene 07 exceeded {target_time:.2f}s at {self.time:.2f}s")
        if remaining > 0:
            self.wait(remaining)

    @staticmethod
    def _text(label: str, *, size: int = LABEL_FONT_SIZE, color: str = TEXT_COLOR) -> Text:
        return Text(label, font=DEFAULT_FONT, font_size=size, color=color)

    def _title(self, label: str, *, color: str = TEXT_COLOR) -> Text:
        return create_scene_title(label, color=color)

    def construct(self) -> None:
        citation = create_footer_citation(
            "Li et al., PARTICULATE, CVPR 2026 — Sec. 3.1 & 3.3",
            max_width=11.6,
        ).to_edge(DOWN, buff=0.24)
        cabinet = create_cabinet_diagram(scale_factor=1.10).move_to(DOWN * 0.05)
        self.add(cabinet, citation)

        # 00:00–00:18 — segmentation provides parts, not connectivity.
        title = self._title("PARTS ARE NOT YET A MECHANISM", color=ACCENT_COLOR)
        labels = (
            VGroup(
                create_part_label("Fixed body", color=FIXED_PART_COLOR),
                create_part_label("Door", color=REVOLUTE_JOINT_COLOR),
                create_part_label("Drawer", color=PRISMATIC_JOINT_COLOR),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            .move_to(RIGHT * 4.35)
        )
        self.play(FadeIn(title), run_time=0.6)
        self.play(
            LaggedStart(
                TransformFromCopy(cabinet.fixed_body, labels[0]),
                TransformFromCopy(cabinet.door, labels[1]),
                TransformFromCopy(cabinet.drawer, labels[2]),
                lag_ratio=0.25,
            ),
            cabinet.animate.shift(LEFT * 2.0),
            run_time=1.2,
        )
        self._hold_until(18)

        # 00:18–00:44 — pairwise parent likelihoods.
        pair_title = self._title("PAIRWISE PARENT LIKELIHOODS", color=OUTPUT_COLOR)
        tokens = (
            VGroup(
                create_concept_token("BODY", color=FIXED_PART_COLOR),
                create_concept_token("DOOR", color=REVOLUTE_JOINT_COLOR),
                create_concept_token("DRAWER", color=PRISMATIC_JOINT_COLOR),
            )
            .arrange(RIGHT, buff=0.70)
            .move_to(UP * 0.75)
        )
        candidates = VGroup(
            Arrow(
                tokens[0].get_bottom(),
                tokens[1].get_bottom(),
                buff=0.20,
                color=REVOLUTE_JOINT_COLOR,
            ),
            Arrow(
                tokens[0].get_bottom(),
                tokens[2].get_bottom(),
                buff=0.20,
                color=PRISMATIC_JOINT_COLOR,
            ),
            Arrow(tokens[1].get_top(), tokens[2].get_top(), buff=0.20, color=MUTED_TEXT_COLOR),
            Arrow(tokens[2].get_top(), tokens[1].get_top(), buff=0.20, color=MUTED_TEXT_COLOR),
        )
        scores = VGroup(
            self._text("high", color=REVOLUTE_JOINT_COLOR),
            self._text("high", color=PRISMATIC_JOINT_COLOR),
            self._text("low", color=MUTED_TEXT_COLOR),
            self._text("low", color=MUTED_TEXT_COLOR),
        )
        for score, arrow in zip(scores, candidates, strict=True):
            score.next_to(arrow, DOWN, buff=0.08)
        self.play(
            FadeOut(VGroup(cabinet, labels)),
            ReplacementTransform(title, pair_title),
            FadeIn(tokens),
            run_time=0.8,
        )
        self.play(LaggedStart(*(Create(edge) for edge in candidates), lag_ratio=0.20), run_time=1.1)
        self.play(FadeIn(scores), run_time=0.5)
        self._hold_until(44)

        # 00:44–01:04 — a rooted arborescence for the cabinet.
        tree_title = self._title("ONE BASE PART → ROOTED TREE", color=OUTPUT_COLOR)
        tree = create_kinematic_tree().scale(0.90).move_to(DOWN * 0.05)
        self.play(
            FadeOut(VGroup(candidates, scores)),
            ReplacementTransform(pair_title, tree_title),
            ReplacementTransform(tokens, tree),
            run_time=1.0,
        )
        self.play(Indicate(tree[1], color=FIXED_PART_COLOR), run_time=0.65)
        self.play(
            Indicate(tree[2][0], color=REVOLUTE_JOINT_COLOR),
            Indicate(tree[2][1], color=PRISMATIC_JOINT_COLOR),
            run_time=0.7,
        )
        self._hold_until(64)

        # 01:04–01:28 — four motion types supported by the representation.
        type_title = self._title("MOTION TYPE PER PART", color=ACCENT_COLOR)
        types = (
            VGroup(
                create_concept_token("FIXED", color=FIXED_PART_COLOR),
                create_concept_token("PRISMATIC", color=PRISMATIC_JOINT_COLOR),
                create_concept_token("REVOLUTE", color=REVOLUTE_JOINT_COLOR),
                create_concept_token("BOTH", color=ACCENT_COLOR),
            )
            .arrange(RIGHT, buff=0.38)
            .move_to(UP * 0.65)
        )
        mapped = VGroup(
            self._text("BODY", color=FIXED_PART_COLOR),
            self._text("DRAWER", color=PRISMATIC_JOINT_COLOR),
            self._text("DOOR", color=REVOLUTE_JOINT_COLOR),
            self._text("COMBINED", color=ACCENT_COLOR),
        )
        for label, token in zip(mapped, types, strict=True):
            label.next_to(token, DOWN, buff=0.35)
        self.play(
            FadeOut(tree), ReplacementTransform(tree_title, type_title), FadeIn(types), run_time=0.9
        )
        self.play(
            LaggedStart(*(FadeIn(label, shift=UP * 0.06) for label in mapped), lag_ratio=0.20),
            run_time=0.9,
        )
        self._hold_until(88)

        # 01:28–01:52 — prismatic direction plus range relative to input state.
        prism_title = self._title("PRISMATIC: UNIT DIRECTION + RANGE", color=PRISMATIC_JOINT_COLOR)
        prism_cabinet = create_cabinet_diagram(scale_factor=1.0).move_to(LEFT * 2.0 + DOWN * 0.10)
        slider = create_sliding_arrow(length=2.7).move_to(RIGHT * 2.9 + DOWN * 0.15)
        ticks = VGroup(
            Line(DOWN * 0.28, UP * 0.28, color=PRISMATIC_JOINT_COLOR).move_to(slider.get_left()),
            Line(DOWN * 0.28, UP * 0.28, color=PRISMATIC_JOINT_COLOR).move_to(slider.get_right()),
        )
        range_label = self._text("RANGE RELATIVE TO INPUT STATE", color=MUTED_TEXT_COLOR).next_to(
            slider, DOWN, buff=0.42
        )
        self.play(
            FadeOut(VGroup(types, mapped)),
            ReplacementTransform(type_title, prism_title),
            FadeIn(prism_cabinet),
            FadeIn(slider),
            FadeIn(ticks),
            FadeIn(range_label),
            run_time=0.9,
        )
        self.play(prism_cabinet.drawer.animate.shift(RIGHT * 0.65), run_time=0.8)
        self.play(prism_cabinet.drawer.animate.shift(LEFT * 0.65), run_time=0.8)
        self._hold_until(112)

        # 01:52–02:22 — same direction, different axis location.
        rev_title = self._title("REVOLUTE AXIS = DIRECTION + LOCATION", color=REVOLUTE_JOINT_COLOR)
        rev_cabinet = create_cabinet_diagram(scale_factor=1.0).move_to(RIGHT * 2.15 + DOWN * 0.08)
        correct_axis = DashedLine(
            DOWN * 1.35, UP * 1.35, color=REVOLUTE_JOINT_COLOR, stroke_width=4
        )
        correct_axis.move_to(rev_cabinet.hinge_axis)
        wrong_axis = correct_axis.copy().shift(RIGHT * 1.35).set_color(MUTED_TEXT_COLOR)
        direction = Arrow(
            LEFT * 4.9 + DOWN * 0.9, LEFT * 4.9 + UP * 0.9, buff=0, color=REVOLUTE_JOINT_COLOR
        )
        direction_label = self._text("SAME DIRECTION", color=MUTED_TEXT_COLOR).next_to(
            direction, RIGHT, buff=0.25
        )
        location_dots = VGroup(
            Dot(correct_axis.get_center(), radius=0.10, color=REVOLUTE_JOINT_COLOR),
            Dot(wrong_axis.get_center(), radius=0.10, color=MUTED_TEXT_COLOR),
        )
        self.play(
            FadeOut(VGroup(prism_cabinet, slider, ticks, range_label)),
            ReplacementTransform(prism_title, rev_title),
            FadeIn(rev_cabinet),
            FadeIn(correct_axis),
            FadeIn(wrong_axis),
            FadeIn(direction),
            FadeIn(direction_label),
            FadeIn(location_dots),
            run_time=1.0,
        )
        self.play(Indicate(wrong_axis, color=MUTED_TEXT_COLOR), run_time=0.65)
        self.play(Indicate(correct_axis, color=REVOLUTE_JOINT_COLOR), run_time=0.65)
        self.play(
            Rotate(rev_cabinet.door, angle=-0.32, about_point=correct_axis.get_center()),
            run_time=0.85,
        )
        self.play(
            Rotate(rev_cabinet.door, angle=0.32, about_point=correct_axis.get_center()),
            run_time=0.85,
        )
        self._hold_until(142)

        # 02:22–02:42 — part points vote for the axis location.
        vote_title = self._title("POINT VOTES FOR AXIS LOCATION", color=REVOLUTE_JOINT_COLOR)
        target = correct_axis.get_center()
        vote_points = VGroup(
            *[
                Dot(target + LEFT * offset + UP * height, radius=0.07, color=REVOLUTE_JOINT_COLOR)
                for offset, height in ((1.6, 0.9), (1.8, 0.3), (1.5, -0.35), (1.7, -0.9))
            ]
        )
        vote_lines = VGroup(
            *[
                Line(
                    point.get_center(),
                    target + UP * (0.25 * index - 0.38),
                    color=REVOLUTE_JOINT_COLOR,
                    stroke_width=2,
                )
                for index, point in enumerate(vote_points)
            ]
        )
        self.play(
            FadeOut(VGroup(wrong_axis, direction, direction_label, location_dots)),
            ReplacementTransform(rev_title, vote_title),
            FadeIn(vote_points),
            run_time=0.8,
        )
        self.play(LaggedStart(*(Create(line) for line in vote_lines), lag_ratio=0.18), run_time=1.0)
        self.play(Indicate(correct_axis, color=REVOLUTE_JOINT_COLOR), run_time=0.7)
        self._hold_until(162)

        # 02:42–02:53 — revolute range endpoints.
        range_title = self._title("REVOLUTE RANGE", color=REVOLUTE_JOINT_COLOR)
        arc = Arc(
            radius=1.25,
            start_angle=-0.20 * PI,
            angle=0.60 * PI,
            color=REVOLUTE_JOINT_COLOR,
            stroke_width=4,
        )
        arc.add_tip(tip_length=0.16).move_to(LEFT * 2.8)
        endpoint_ticks = VGroup(
            Dot(arc.get_start(), radius=0.09, color=REVOLUTE_JOINT_COLOR),
            Dot(arc.get_end(), radius=0.09, color=REVOLUTE_JOINT_COLOR),
        )
        self.play(
            FadeOut(VGroup(vote_points, vote_lines)),
            ReplacementTransform(vote_title, range_title),
            Create(arc),
            FadeIn(endpoint_ticks),
            run_time=0.9,
        )
        self.play(
            Rotate(rev_cabinet.door, angle=-0.40, about_point=correct_axis.get_center()),
            run_time=0.8,
        )
        self._hold_until(173)

        # 02:53–03:00 — full prediction handoff.
        final_title = self._title("PREDICTION", color=OUTPUT_COLOR)
        final_cabinet = create_cabinet_diagram(scale_factor=0.82).move_to(LEFT * 3.4 + DOWN * 0.10)
        final_tree = create_kinematic_tree().scale(0.72).move_to(RIGHT * 2.55 + UP * 0.35)
        final_axis = create_rotation_axis(length=1.70).scale(0.72).move_to(LEFT * 1.78 + UP * 0.10)
        final_slider = (
            create_sliding_arrow(length=1.75).scale(0.75).move_to(LEFT * 2.85 + DOWN * 1.65)
        )
        self.play(
            FadeOut(VGroup(rev_cabinet, correct_axis, arc, endpoint_ticks, range_title)),
            FadeIn(final_title),
            FadeIn(final_cabinet),
            FadeIn(final_tree),
            FadeIn(final_axis),
            FadeIn(final_slider),
            run_time=0.9,
        )
        self._hold_until(179.0)
