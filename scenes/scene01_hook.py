"""Scene 01: motivate articulation through one continuous cabinet interaction."""

from __future__ import annotations

from manim import (
    DL,
    DOWN,
    LEFT,
    RIGHT,
    UL,
    UP,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    MoveAlongPath,
    MoveToTarget,
    MovingCameraScene,
    Polygon,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
    Wiggle,
    rate_functions,
)

from common import (
    create_cabinet_diagram,
    create_concept_token,
    create_footer_citation,
    create_robot_diagram,
    create_rotation_axis,
    create_section_title,
    create_sliding_arrow,
)
from config import (
    ACCENT_COLOR,
    BODY_FONT_SIZE,
    DEFAULT_FONT,
    FIXED_PART_COLOR,
    INPUT_COLOR,
    MUTED_TEXT_COLOR,
    OUTPUT_COLOR,
    PRISMATIC_JOINT_COLOR,
    REVOLUTE_JOINT_COLOR,
    SECTION_FONT_SIZE,
    TEXT_COLOR,
    apply_project_style,
)

apply_project_style()


class Scene01Hook(MovingCameraScene):
    """Show the gap between recognizing an object and understanding its motion."""

    def _hold_until(self, target_time: float) -> None:
        """Pad a storyboard beat to its absolute end time."""

        remaining = target_time - self.time
        if remaining < -0.05:
            raise RuntimeError(
                f"Scene 01 exceeded storyboard time {target_time:.2f}s "
                f"at {self.time:.2f}s."
            )
        if remaining > 0:
            self.wait(remaining)

    @staticmethod
    def _status_token(text: str, color: str) -> VGroup:
        token = create_concept_token(text, color=color)
        token[0].set_fill(opacity=0.06)
        return token

    def construct(self) -> None:
        cabinet = create_cabinet_diagram(scale_factor=1.06).shift(RIGHT * 2.05 + DOWN * 0.10)
        robot = create_robot_diagram(scale_factor=0.86).shift(LEFT * 3.80 + DOWN * 0.48)

        cabinet.door_panel.set_stroke(FIXED_PART_COLOR).set_fill(
            FIXED_PART_COLOR, opacity=0.08
        )
        cabinet.drawer_panel.set_stroke(FIXED_PART_COLOR).set_fill(
            FIXED_PART_COLOR, opacity=0.08
        )
        cabinet.hinge_axis.set_opacity(0)

        floor = Line(
            LEFT * 6.3,
            RIGHT * 6.3,
            color=MUTED_TEXT_COLOR,
            stroke_width=1.4,
            stroke_opacity=0.22,
        ).shift(DOWN * 2.48)

        # 00:00–00:05 — identify the paper and state the visual thesis.
        intro_title = create_section_title(
            "PARTICULATE",
            "Feed-Forward 3D Object Articulation",
            font_size=SECTION_FONT_SIZE,
            subtitle_font_size=BODY_FONT_SIZE,
        ).move_to(LEFT * 3.02 + UP * 0.65)
        intro_thesis = Text(
            "STATIC SHAPE  ≠  MOTION",
            font=DEFAULT_FONT,
            font_size=BODY_FONT_SIZE,
            color=ACCENT_COLOR,
        ).next_to(intro_title, DOWN, buff=0.42)
        intro_cabinet = cabinet.copy().set_opacity(0.25)

        self.play(
            FadeIn(intro_cabinet, shift=UP * 0.08),
            FadeIn(intro_title, shift=RIGHT * 0.08),
            run_time=1.00,
            rate_func=rate_functions.ease_out_cubic,
        )
        self.play(FadeIn(intro_thesis, shift=UP * 0.05), run_time=0.55)
        self._hold_until(4.0)

        # 00:05–00:10 — transform the title composition into the physical setup.
        self.play(
            ReplacementTransform(intro_cabinet, cabinet),
            FadeOut(intro_title, shift=UP * 0.05),
            FadeOut(intro_thesis, shift=LEFT * 0.08),
            Create(floor),
            FadeIn(robot, shift=RIGHT * 0.12),
            self.camera.frame.animate.scale(0.96).shift(RIGHT * 0.25),
            run_time=1.00,
            rate_func=rate_functions.ease_out_cubic,
        )
        self._hold_until(10.0)

        # 00:10–00:19 — geometry is recognized by a single scan.
        scan_height = cabinet.height + 0.34
        scan_field = Rectangle(
            width=0.34,
            height=scan_height,
            stroke_width=0,
            fill_color=PRISMATIC_JOINT_COLOR,
            fill_opacity=0.12,
        )
        scan_beam = Line(
            UP * scan_height / 2,
            DOWN * scan_height / 2,
            color=PRISMATIC_JOINT_COLOR,
            stroke_width=4,
            stroke_opacity=0.85,
        )
        scan = VGroup(scan_field, scan_beam).move_to(cabinet.get_left() + LEFT * 0.12)
        scan_path = Line(scan.get_center(), cabinet.get_right() + RIGHT * 0.12)
        cabinet_outline = RoundedRectangle(
            width=cabinet.width + 0.24,
            height=cabinet.height + 0.24,
            corner_radius=0.14,
            color=INPUT_COLOR,
            stroke_width=1.8,
            stroke_opacity=0.70,
        ).move_to(cabinet)
        mesh_token = self._status_token("STATIC 3D MESH", INPUT_COLOR)
        mesh_token.next_to(cabinet, UP, buff=0.32)
        shape_status = self._status_token("SHAPE: KNOWN", OUTPUT_COLOR)
        shape_status.move_to(LEFT * 4.45 + UP * 1.95)

        self.play(
            MoveAlongPath(scan, scan_path),
            Create(cabinet_outline),
            run_time=1.55,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            FadeOut(scan),
            FadeIn(mesh_token, shift=DOWN * 0.06),
            FadeIn(shape_status, shift=RIGHT * 0.08),
            run_time=0.55,
        )
        self._hold_until(15.5)
        self.play(
            Indicate(cabinet.fixed_body, color=INPUT_COLOR, scale_factor=1.015),
            Indicate(cabinet.door_panel, color=INPUT_COLOR, scale_factor=1.025),
            Indicate(cabinet.drawer_panel, color=INPUT_COLOR, scale_factor=1.035),
            run_time=0.85,
        )
        self._hold_until(19.0)

        # 00:19–00:29 — the robot reaches the fixed shell; motion remains unknown.
        motion_status = self._status_token("MOTION: UNKNOWN", ACCENT_COLOR)
        motion_status.next_to(shape_status, DOWN, buff=0.28).align_to(shape_status, LEFT)

        arm_start = robot.right_arm.get_start()
        original_arm = robot.right_arm.copy()
        original_hand_position = robot.right_hand.get_center()
        contact = cabinet.front_panel.get_center() + LEFT * 0.15 + UP * 0.08
        extended_arm = Line(
            arm_start,
            contact,
            color=MUTED_TEXT_COLOR,
            stroke_width=4,
        )

        self.play(FadeIn(motion_status, shift=RIGHT * 0.08), run_time=0.45)
        self.play(
            Transform(robot.right_arm, extended_arm),
            robot.right_hand.animate.move_to(contact),
            run_time=0.85,
            rate_func=rate_functions.ease_out_cubic,
        )

        contact_ring = Circle(radius=0.12, color=ACCENT_COLOR, stroke_width=3).move_to(contact)
        self.play(Create(contact_ring), run_time=0.25)
        self.play(
            contact_ring.animate.scale(2.6).set_stroke(opacity=0),
            Wiggle(cabinet.fixed_body, scale_value=1.004, rotation_angle=0.010),
            Indicate(motion_status, color=ACCENT_COLOR),
            run_time=0.80,
        )
        self.remove(contact_ring)
        self.play(
            Transform(robot.right_arm, original_arm),
            robot.right_hand.animate.move_to(original_hand_position),
            run_time=0.65,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self._hold_until(23.2)

        # The mesh offers several plausible interaction points but no motion rule.
        for target in (cabinet.door_handle.get_center(), cabinet.drawer_handle.get_center()):
            trial_arm = Line(
                arm_start,
                target,
                color=MUTED_TEXT_COLOR,
                stroke_width=4,
            )
            self.play(
                Transform(robot.right_arm, trial_arm),
                robot.right_hand.animate.move_to(target),
                run_time=0.55,
                rate_func=rate_functions.ease_out_cubic,
            )
            self.play(
                Indicate(motion_status, color=ACCENT_COLOR, scale_factor=1.025),
                run_time=0.40,
            )

        self.play(
            Transform(robot.right_arm, original_arm),
            robot.right_hand.animate.move_to(original_hand_position),
            run_time=0.55,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self._hold_until(29.0)

        # 00:29–00:42 — reveal the actual articulated motions, not just color changes.
        self.play(
            FadeOut(cabinet_outline),
            FadeOut(shape_status),
            FadeOut(motion_status),
            FadeOut(robot),
            self.camera.frame.animate.scale(0.86).move_to(cabinet.get_center() + LEFT * 0.15),
            run_time=0.85,
            rate_func=rate_functions.ease_in_out_cubic,
        )

        self.play(
            cabinet.door_panel.animate.set_stroke(REVOLUTE_JOINT_COLOR).set_fill(
                REVOLUTE_JOINT_COLOR, opacity=0.20
            ),
            cabinet.drawer_panel.animate.set_stroke(PRISMATIC_JOINT_COLOR).set_fill(
                PRISMATIC_JOINT_COLOR, opacity=0.22
            ),
            cabinet.hinge_axis.animate.set_opacity(1),
            run_time=0.70,
        )

        hinge_top = cabinet.door_panel.get_corner(UL)
        hinge_bottom = cabinet.door_panel.get_corner(DL)
        open_vector = LEFT * 0.92 + DOWN * 0.13
        open_door = Polygon(
            hinge_top,
            hinge_top + open_vector,
            hinge_bottom + open_vector,
            hinge_bottom,
            color=REVOLUTE_JOINT_COLOR,
            stroke_width=2.5,
            fill_color=REVOLUTE_JOINT_COLOR,
            fill_opacity=0.20,
        )
        open_handle = Dot(
            (hinge_top + open_vector + hinge_bottom + open_vector) / 2,
            radius=0.055,
            color=TEXT_COLOR,
        )
        closed_door = cabinet.door_panel.copy()
        closed_handle = cabinet.door_handle.copy()

        self.play(
            Transform(cabinet.door_panel, open_door),
            Transform(cabinet.door_handle, open_handle),
            run_time=1.10,
            rate_func=rate_functions.ease_in_out_cubic,
        )

        drawer_track = Line(
            cabinet.drawer_panel.get_center(),
            cabinet.drawer_panel.get_center() + RIGHT * 0.82,
            color=PRISMATIC_JOINT_COLOR,
            stroke_width=2,
            stroke_opacity=0.55,
        )
        self.play(
            Create(drawer_track),
            cabinet.drawer.animate.shift(RIGHT * 0.68),
            run_time=0.90,
            rate_func=rate_functions.ease_out_cubic,
        )

        rotation_cue = create_rotation_axis(length=1.55).scale(0.55)
        rotation_cue.move_to(cabinet.hinge_axis.get_center() + LEFT * 0.02)
        sliding_cue = create_sliding_arrow(length=1.55).scale(0.67)
        sliding_cue.move_to(cabinet.drawer_panel.get_center() + RIGHT * 0.40)
        self.play(
            Create(rotation_cue),
            Create(sliding_cue),
            run_time=0.80,
        )
        self._hold_until(35.5)
        self.play(
            Transform(cabinet.door_panel, closed_door),
            Transform(cabinet.door_handle, closed_handle),
            cabinet.drawer.animate.shift(LEFT * 0.68),
            run_time=0.65,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            Transform(cabinet.door_panel, open_door),
            Transform(cabinet.door_handle, open_handle),
            cabinet.drawer.animate.shift(RIGHT * 0.68),
            run_time=0.80,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            Indicate(rotation_cue, color=REVOLUTE_JOINT_COLOR, scale_factor=1.04),
            Indicate(sliding_cue, color=PRISMATIC_JOINT_COLOR, scale_factor=1.04),
            run_time=0.75,
        )
        self._hold_until(42.0)

        # 00:42–00:55 — concepts emerge from the geometry that motivates them.
        self.play(
            FadeOut(mesh_token),
            self.camera.frame.animate.scale(1 / 0.86).move_to(RIGHT * 0.15),
            run_time=0.75,
            rate_func=rate_functions.ease_in_out_cubic,
        )

        part_token = create_concept_token("PART", color=ACCENT_COLOR)
        joint_token = create_concept_token("JOINT", color=ACCENT_COLOR)
        motion_token = create_concept_token("MOTION", color=ACCENT_COLOR)
        tokens = VGroup(part_token, joint_token, motion_token).arrange(
            DOWN, aligned_edge=LEFT, buff=0.42
        )
        tokens.to_edge(LEFT, buff=0.82).shift(UP * 0.12)

        part_connector = Line(
            part_token.get_right(),
            cabinet.door_panel.get_center(),
            color=ACCENT_COLOR,
            stroke_width=1.6,
            stroke_opacity=0.38,
        )
        joint_connector = Line(
            joint_token.get_right(),
            cabinet.hinge_axis.get_center(),
            color=ACCENT_COLOR,
            stroke_width=1.6,
            stroke_opacity=0.38,
        )
        motion_connector = Line(
            motion_token.get_right(),
            sliding_cue.get_center(),
            color=ACCENT_COLOR,
            stroke_width=1.6,
            stroke_opacity=0.38,
        )

        self.play(
            TransformFromCopy(VGroup(cabinet.door_panel, cabinet.drawer_panel), part_token),
            Create(part_connector),
            run_time=0.75,
        )
        self._hold_until(46.5)
        self.play(
            TransformFromCopy(cabinet.hinge_axis, joint_token),
            Create(joint_connector),
            run_time=0.70,
        )
        self._hold_until(50.0)
        self.play(
            TransformFromCopy(VGroup(rotation_cue, sliding_cue), motion_token),
            Create(motion_connector),
            run_time=0.75,
        )
        self._hold_until(53.5)
        self.play(
            Indicate(part_token, color=ACCENT_COLOR, scale_factor=1.04),
            Indicate(joint_token, color=ACCENT_COLOR, scale_factor=1.04),
            Indicate(motion_token, color=ACCENT_COLOR, scale_factor=1.04),
            run_time=0.75,
        )
        self._hold_until(55.0)

        # 00:55–01:09 — connect the named method to the three predictions.
        method_badge = create_concept_token("PARTICULATE", color=OUTPUT_COLOR)
        method_badge.to_edge(UP, buff=0.38)
        citation = create_footer_citation(
            "Li et al. • PARTICULATE • CVPR 2026"
        ).to_edge(DOWN, buff=0.18)

        self.play(
            FadeOut(part_connector),
            FadeOut(joint_connector),
            FadeOut(motion_connector),
            FadeIn(method_badge, shift=DOWN * 0.06),
            run_time=0.65,
        )
        tokens.generate_target()
        tokens.target.arrange(RIGHT, buff=0.34)
        tokens.target.to_edge(LEFT, buff=0.82).shift(DOWN * 1.35)
        self.play(
            MoveToTarget(tokens),
            FadeIn(citation),
            run_time=0.80,
            rate_func=rate_functions.ease_in_out_cubic,
        )

        knowledge_glow = RoundedRectangle(
            width=cabinet.width + 0.34,
            height=cabinet.height + 0.34,
            corner_radius=0.16,
            color=OUTPUT_COLOR,
            stroke_width=2.4,
            stroke_opacity=0.85,
        ).move_to(cabinet)
        self.play(Create(knowledge_glow), run_time=0.55)
        self.play(
            knowledge_glow.animate.set_stroke(opacity=0).scale(1.04),
            run_time=0.55,
        )
        self.remove(knowledge_glow)
        self._hold_until(61.0)
        self.play(
            Indicate(method_badge, color=OUTPUT_COLOR, scale_factor=1.035),
            run_time=0.75,
        )
        self._hold_until(64.5)
        self.play(
            Indicate(tokens[0], color=ACCENT_COLOR, scale_factor=1.035),
            Indicate(tokens[1], color=ACCENT_COLOR, scale_factor=1.035),
            Indicate(tokens[2], color=ACCENT_COLOR, scale_factor=1.035),
            run_time=0.75,
        )
        self._hold_until(69.0)

        # 01:09–01:20 — preserve the object and three concepts for Scene 02.
        self.play(
            FadeOut(method_badge),
            FadeOut(citation),
            FadeOut(drawer_track),
            FadeOut(rotation_cue),
            FadeOut(sliding_cue),
            run_time=0.65,
        )
        tokens.generate_target()
        tokens.target.arrange(RIGHT, buff=0.38).to_edge(DOWN, buff=0.48)
        self.play(
            MoveToTarget(tokens),
            mesh_token.animate.next_to(cabinet, UP, buff=0.30),
            run_time=0.75,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(FadeIn(mesh_token), run_time=0.40)
        self._hold_until(72.5)
        self.play(Indicate(tokens[0], color=ACCENT_COLOR), run_time=0.65)
        self._hold_until(74.5)
        self.play(Indicate(tokens[1], color=ACCENT_COLOR), run_time=0.65)
        self._hold_until(76.5)
        self.play(Indicate(tokens[2], color=ACCENT_COLOR), run_time=0.65)
        self._hold_until(80.0)
