"""Scene 10: paper-supported limitations, callback, and conclusion."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    Cross,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    MovingCameraScene,
    Rectangle,
    ReplacementTransform,
    Rotate,
    Text,
    VGroup,
)

from common import (
    create_cabinet_diagram,
    create_concept_token,
    create_footer_citation,
    create_kinematic_tree,
    create_pipeline_box,
    create_robot_diagram,
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
    TITLE_FONT_SIZE,
    apply_project_style,
)

apply_project_style()


class Scene10Conclusion(MovingCameraScene):
    """Close with the paper's two limitations and the cabinet callback."""

    def _hold_until(self, target_time: float) -> None:
        remaining = target_time - self.time
        if remaining < -0.05:
            raise RuntimeError(f"Scene 10 exceeded {target_time:.2f}s at {self.time:.2f}s")
        if remaining > 0:
            self.wait(remaining)

    @staticmethod
    def _text(label: str, *, size: int = LABEL_FONT_SIZE, color: str = TEXT_COLOR) -> Text:
        return Text(label, font=DEFAULT_FONT, font_size=size, color=color)

    def _title(self, label: str, *, color: str = TEXT_COLOR) -> Text:
        return create_scene_title(label, color=color)

    @staticmethod
    def _articulated_object(*, scale_factor: float = 1.0) -> VGroup:
        cabinet = create_cabinet_diagram(scale_factor=0.72).move_to(LEFT * 1.45)
        tree = create_kinematic_tree().scale(0.50).move_to(RIGHT * 1.55 + UP * 0.25)
        axis = create_rotation_axis(length=1.35).scale(0.55).move_to(LEFT * 0.65)
        return VGroup(cabinet, tree, axis).scale(scale_factor)

    def construct(self) -> None:
        citation = create_footer_citation(
            "Li et al., PARTICULATE: Feed-Forward 3D Object Articulation, CVPR 2026",
            max_width=11.6,
        ).to_edge(DOWN, buff=0.24)
        final_object = self._articulated_object(scale_factor=1.12).move_to(DOWN * 0.05)
        self.add(self._title("ARTICULATED 3D", color=OUTPUT_COLOR), final_object, citation)

        # 00:00–00:18 — peel the output into the three predicted components.
        recap_title = self._title("ONE PASS — THREE LINKED OUTPUTS", color=OUTPUT_COLOR)
        tokens = (
            VGroup(
                create_concept_token("PARTS", color=OUTPUT_COLOR),
                create_concept_token("TREE", color=FIXED_PART_COLOR),
                create_concept_token("MOTION", color=REVOLUTE_JOINT_COLOR),
            )
            .arrange(RIGHT, buff=0.52)
            .move_to(DOWN * 0.05)
        )
        old_title = self.mobjects[0]
        self.play(
            FadeOut(final_object),
            ReplacementTransform(old_title, recap_title),
            LaggedStart(*(FadeIn(token, shift=UP * 0.08) for token in tokens), lag_ratio=0.24),
            run_time=1.0,
        )
        self._hold_until(18)

        # 00:18–00:38 — compact architecture recap.
        model_title = self._title("POINT FEATURES + PART QUERIES", color=ACCENT_COLOR)
        points = (
            VGroup(*(Dot(radius=0.065, color=INPUT_COLOR) for _ in range(8)))
            .arrange_in_grid(rows=2, cols=4, buff=0.22)
            .move_to(LEFT * 4.3)
        )
        queries = (
            VGroup(*(Dot(radius=0.10, color=ACCENT_COLOR) for _ in range(4)))
            .arrange(DOWN, buff=0.25)
            .move_to(LEFT * 2.4)
        )
        model = create_pipeline_box("PAT", color=ACCENT_COLOR, width=1.65, height=1.0)
        heads = (
            VGroup(
                *[
                    create_pipeline_box(label, color=OUTPUT_COLOR, width=1.75, height=0.60)
                    for label in ("PARTS", "TREE", "TYPE", "AXIS", "RANGE")
                ]
            )
            .arrange(DOWN, buff=0.12)
            .move_to(RIGHT * 2.1)
        )
        object_out = create_cabinet_diagram(scale_factor=0.43).move_to(RIGHT * 5.0)
        flow = VGroup(
            Arrow(points.get_right(), model.get_left(), buff=0.18, color=INPUT_COLOR),
            Arrow(queries.get_right(), model.get_left(), buff=0.18, color=ACCENT_COLOR),
            Arrow(model.get_right(), heads.get_left(), buff=0.18, color=OUTPUT_COLOR),
            Arrow(heads.get_right(), object_out.get_left(), buff=0.18, color=OUTPUT_COLOR),
        )
        self.play(
            FadeOut(tokens),
            ReplacementTransform(recap_title, model_title),
            FadeIn(points),
            FadeIn(queries),
            FadeIn(model),
            Create(flow[0]),
            Create(flow[1]),
            run_time=0.9,
        )
        self.play(Create(flow[2]), FadeIn(heads), Create(flow[3]), FadeIn(object_out), run_time=1.0)
        self._hold_until(38)

        # 00:38–01:03 — limitation 1: out-of-distribution kinematic structures.
        limit_one_title = self._title("LIMITATION 1 — UNFAMILIAR KINEMATICS", color=ACCENT_COLOR)
        familiar = create_kinematic_tree().scale(0.72).move_to(LEFT * 3.2 + DOWN * 0.05)
        root = create_concept_token("BASE", color=FIXED_PART_COLOR).move_to(RIGHT * 2.8 + UP * 1.25)
        branch_a = create_concept_token("A", color=REVOLUTE_JOINT_COLOR).move_to(
            RIGHT * 1.4 + DOWN * 0.65
        )
        branch_b = create_concept_token("B", color=PRISMATIC_JOINT_COLOR).move_to(
            RIGHT * 4.2 + DOWN * 0.65
        )
        branch_c = create_concept_token("C", color=ACCENT_COLOR).move_to(RIGHT * 2.8 + DOWN * 1.75)
        unfamiliar_edges = VGroup(
            Arrow(root.get_bottom(), branch_a.get_top(), buff=0.10, color=MUTED_TEXT_COLOR),
            Arrow(root.get_bottom(), branch_b.get_top(), buff=0.10, color=MUTED_TEXT_COLOR),
            Arrow(branch_a.get_right(), branch_c.get_left(), buff=0.12, color=ACCENT_COLOR),
            Arrow(branch_b.get_left(), branch_c.get_right(), buff=0.12, color=ACCENT_COLOR),
        )
        unfamiliar = VGroup(root, branch_a, branch_b, branch_c, unfamiliar_edges)
        fail_mark = Cross(unfamiliar, stroke_color=REVOLUTE_JOINT_COLOR, stroke_width=5).scale(0.42)
        labels = VGroup(
            self._text("SEEN-LIKE", color=OUTPUT_COLOR).next_to(familiar, DOWN, buff=0.28),
            self._text("VERY DIFFERENT", color=ACCENT_COLOR).next_to(unfamiliar, DOWN, buff=0.28),
        )
        self.play(
            FadeOut(VGroup(points, queries, model, heads, object_out, flow)),
            ReplacementTransform(model_title, limit_one_title),
            FadeIn(familiar),
            FadeIn(unfamiliar),
            FadeIn(labels),
            run_time=1.0,
        )
        self.play(Create(fail_mark), run_time=0.7)
        self._hold_until(63)

        # 01:03–01:28 — limitation 2: inter-part penetration.
        limit_two_title = self._title("LIMITATION 2 — INTER-PART PENETRATION", color=ACCENT_COLOR)
        part_a = (
            Rectangle(
                width=4.2,
                height=1.35,
                color=FIXED_PART_COLOR,
                fill_color=FIXED_PART_COLOR,
                fill_opacity=0.35,
            )
            .rotate(0.12)
            .move_to(LEFT * 0.55)
        )
        part_b = (
            Rectangle(
                width=3.2,
                height=1.15,
                color=REVOLUTE_JOINT_COLOR,
                fill_color=REVOLUTE_JOINT_COLOR,
                fill_opacity=0.40,
            )
            .rotate(-0.28)
            .move_to(RIGHT * 0.65)
        )
        overlap = Circle(
            radius=0.62,
            color=REVOLUTE_JOINT_COLOR,
            fill_color=REVOLUTE_JOINT_COLOR,
            fill_opacity=0.38,
            stroke_width=4,
        ).move_to(DOWN * 0.05)
        causes = (
            VGroup(
                create_concept_token("GENERATED-MESH ARTIFACT", color=ACCENT_COLOR),
                create_concept_token("IMPERFECT MOTION", color=ACCENT_COLOR),
            )
            .arrange(RIGHT, buff=0.45)
            .move_to(DOWN * 1.9)
        )
        self.play(
            FadeOut(VGroup(familiar, unfamiliar, fail_mark, labels)),
            ReplacementTransform(limit_one_title, limit_two_title),
            FadeIn(part_a),
            FadeIn(part_b),
            run_time=0.9,
        )
        self.play(FadeIn(overlap), Indicate(overlap, color=REVOLUTE_JOINT_COLOR), run_time=0.8)
        self.play(FadeIn(causes), run_time=0.7)
        self._hold_until(88)

        # 01:28–01:43 — explicitly frame physical plausibility as future work.
        future_title = self._title("FUTURE: MORE PHYSICALLY PLAUSIBLE ASSETS", color=OUTPUT_COLOR)
        barrier = DashedLine(DOWN * 1.15, UP * 1.15, color=OUTPUT_COLOR, stroke_width=4)
        simulator = create_pipeline_box(
            "SIM-TO-REAL ROBOTICS", color=OUTPUT_COLOR, width=4.1, height=1.0
        ).move_to(RIGHT * 3.25)
        self.play(
            FadeOut(VGroup(overlap, causes)),
            ReplacementTransform(limit_two_title, future_title),
            part_a.animate.shift(LEFT * 1.0),
            part_b.animate.shift(RIGHT * 1.0),
            Create(barrier),
            run_time=0.9,
        )
        self.play(FadeOut(VGroup(part_a, part_b, barrier)), FadeIn(simulator), run_time=0.8)
        self._hold_until(103)

        # 01:43–02:02 — return to the central conceptual contribution.
        idea_title = self._title("SHAPE → STRUCTURE → MOTION", color=OUTPUT_COLOR)
        shape = create_concept_token("STATIC SHAPE", color=INPUT_COLOR)
        particulate = create_pipeline_box("PARTICULATE", color=ACCENT_COLOR, width=2.65, height=1.0)
        motion = create_concept_token("ARTICULATED 3D", color=OUTPUT_COLOR)
        idea = VGroup(shape, particulate, motion).arrange(RIGHT, buff=1.0).move_to(DOWN * 0.05)
        idea_arrows = VGroup(
            Arrow(shape.get_right(), particulate.get_left(), buff=0.15, color=ACCENT_COLOR),
            Arrow(particulate.get_right(), motion.get_left(), buff=0.15, color=OUTPUT_COLOR),
        )
        self.play(
            FadeOut(simulator),
            ReplacementTransform(future_title, idea_title),
            FadeIn(shape),
            Create(idea_arrows[0]),
            FadeIn(particulate),
            Create(idea_arrows[1]),
            FadeIn(motion),
            run_time=1.1,
        )
        self._hold_until(122)

        # 02:02–02:20 — visual analogy: the robot now opens the correct door.
        callback_title = self._title("PART · HINGE · AXIS", color=OUTPUT_COLOR)
        cabinet = create_cabinet_diagram(scale_factor=0.88).move_to(RIGHT * 2.1 + DOWN * 0.10)
        robot = create_robot_diagram(scale_factor=0.72).move_to(LEFT * 3.0 + DOWN * 0.65)
        axis = create_rotation_axis(length=1.75).scale(0.78).move_to(cabinet.hinge_axis)
        self.play(
            FadeOut(VGroup(idea, idea_arrows)),
            ReplacementTransform(idea_title, callback_title),
            FadeIn(robot),
            FadeIn(cabinet),
            run_time=0.9,
        )
        self.play(FadeIn(axis), Indicate(cabinet.door, color=REVOLUTE_JOINT_COLOR), run_time=0.8)
        self.play(
            Rotate(cabinet.door, angle=-0.42 * PI, about_point=cabinet.hinge_axis.get_center()),
            run_time=1.2,
        )
        analogy = self._text("VISUAL ANALOGY", color=MUTED_TEXT_COLOR).next_to(
            robot, DOWN, buff=0.25
        )
        self.play(FadeIn(analogy), run_time=0.5)
        self._hold_until(140)

        # 02:20–02:30 — end card and the only full fade-out in the sequence.
        end_title = self._text("PARTICULATE", size=TITLE_FONT_SIZE, color=TEXT_COLOR)
        end_subtitle = self._text("STATIC 3D → ARTICULATED 3D", color=OUTPUT_COLOR)
        end_card = VGroup(end_title, end_subtitle).arrange(DOWN, buff=0.42).move_to(UP * 0.20)
        self.play(
            FadeOut(VGroup(callback_title, robot, cabinet, axis, analogy)),
            FadeIn(end_card),
            run_time=0.9,
        )
        self._hold_until(148.0)
        self.play(FadeOut(VGroup(end_card, citation)), run_time=1.0)
