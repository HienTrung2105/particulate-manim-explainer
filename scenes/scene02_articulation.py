"""Scene 02: explain parts, joints, motion types, and the kinematic tree."""

from __future__ import annotations

from manim import (
    DL,
    DOWN,
    LEFT,
    RIGHT,
    UL,
    UP,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    MoveToTarget,
    MovingCameraScene,
    Polygon,
    Text,
    Transform,
    VGroup,
    rate_functions,
)

from common import (
    CabinetDiagram,
    create_cabinet_diagram,
    create_concept_token,
    create_kinematic_tree,
    create_part_label,
    create_rotation_axis,
    create_sliding_arrow,
)
from config import (
    ACCENT_COLOR,
    DEFAULT_FONT,
    FIXED_PART_COLOR,
    LABEL_FONT_SIZE,
    MUTED_TEXT_COLOR,
    PRISMATIC_JOINT_COLOR,
    REVOLUTE_JOINT_COLOR,
    TEXT_COLOR,
    apply_project_style,
)

apply_project_style()


class Scene02Articulation(MovingCameraScene):
    """Build an articulated representation from the cabinet in Scene 01."""

    def _hold_until(self, target_time: float) -> None:
        """Pad the current beat to its absolute storyboard end time."""

        remaining = target_time - self.time
        if remaining < -0.05:
            raise RuntimeError(
                f"Scene 02 exceeded storyboard time {target_time:.2f}s "
                f"at {self.time:.2f}s."
            )
        if remaining > 0:
            self.wait(remaining)

    @staticmethod
    def _open_door_geometry(cabinet: CabinetDiagram) -> tuple[Polygon, Dot]:
        """Return the same restrained pseudo-3D door state used by Scene 01."""

        hinge_top = cabinet.door_panel.get_corner(UL)
        hinge_bottom = cabinet.door_panel.get_corner(DL)
        open_vector = LEFT * 0.92 + DOWN * 0.13
        panel = Polygon(
            hinge_top,
            hinge_top + open_vector,
            hinge_bottom + open_vector,
            hinge_bottom,
            color=REVOLUTE_JOINT_COLOR,
            stroke_width=2.5,
            fill_color=REVOLUTE_JOINT_COLOR,
            fill_opacity=0.20,
        )
        handle = Dot(
            (hinge_top + open_vector + hinge_bottom + open_vector) / 2,
            radius=0.055,
            color=TEXT_COLOR,
        )
        return panel, handle

    @staticmethod
    def _motion_token(text: str, color: str) -> VGroup:
        token = create_concept_token(text, color=color)
        token[0].set_fill(opacity=0.08)
        return token

    def construct(self) -> None:
        # Recreate Scene 01's handoff without importing live objects from it.
        self.camera.frame.scale(0.96).move_to(RIGHT * 0.15)
        cabinet = create_cabinet_diagram(scale_factor=1.06).shift(
            RIGHT * 2.05 + DOWN * 0.10
        )
        closed_door = cabinet.door_panel.copy()
        closed_handle = cabinet.door_handle.copy()
        open_door, open_handle = self._open_door_geometry(cabinet)
        cabinet.door_panel.become(open_door)
        cabinet.door_handle.become(open_handle)
        cabinet.drawer.shift(RIGHT * 0.68)

        mesh_token = self._motion_token("STATIC 3D MESH", TEXT_COLOR)
        mesh_token.next_to(cabinet, UP, buff=0.30)
        part_token = self._motion_token("PART", ACCENT_COLOR)
        joint_token = self._motion_token("JOINT", ACCENT_COLOR)
        motion_token = self._motion_token("MOTION", ACCENT_COLOR)
        concept_tokens = VGroup(part_token, joint_token, motion_token)
        concept_tokens.arrange(RIGHT, buff=0.38).to_edge(DOWN, buff=0.48)
        self.add(cabinet, mesh_token, concept_tokens)

        # 00:00-00:12 - continue directly from Scene 01 and unpack its three terms.
        self.wait(0.45)
        self.play(
            Indicate(part_token, color=ACCENT_COLOR, scale_factor=1.035),
            run_time=0.65,
        )
        self.play(
            Indicate(joint_token, color=ACCENT_COLOR, scale_factor=1.035),
            run_time=0.65,
        )
        self.play(
            Indicate(motion_token, color=ACCENT_COLOR, scale_factor=1.035),
            run_time=0.65,
        )
        concept_tokens.generate_target()
        concept_tokens.target.arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        concept_tokens.target.to_edge(LEFT, buff=0.72).shift(UP * 0.30)
        self.play(
            MoveToTarget(concept_tokens),
            FadeOut(mesh_token, shift=UP * 0.06),
            run_time=0.90,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self._hold_until(12.0)

        # 00:12-00:30 - reveal that the same object is composed of distinct parts.
        self.play(
            Transform(cabinet.door_panel, closed_door),
            Transform(cabinet.door_handle, closed_handle),
            cabinet.drawer.animate.shift(LEFT * 0.68),
            run_time=0.90,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            Indicate(part_token, color=ACCENT_COLOR, scale_factor=1.04),
            run_time=0.55,
        )

        body_label = create_part_label("PART", color=FIXED_PART_COLOR)
        door_label = create_part_label("PART", color=REVOLUTE_JOINT_COLOR)
        drawer_label = create_part_label("PART", color=PRISMATIC_JOINT_COLOR)
        part_labels = VGroup(body_label, door_label, drawer_label).arrange(
            DOWN, aligned_edge=LEFT, buff=0.24
        )
        part_labels.move_to(LEFT * 3.55 + DOWN * 1.20)

        body_line = Line(
            body_label.get_right(),
            cabinet.front_panel.get_corner(UL) + RIGHT * 0.38 + DOWN * 0.20,
            color=FIXED_PART_COLOR,
            stroke_width=1.8,
            stroke_opacity=0.65,
        )
        door_line = Line(
            door_label.get_right(),
            cabinet.door_panel.get_left(),
            color=REVOLUTE_JOINT_COLOR,
            stroke_width=1.8,
            stroke_opacity=0.65,
        )
        drawer_line = Line(
            drawer_label.get_right(),
            cabinet.drawer_panel.get_left(),
            color=PRISMATIC_JOINT_COLOR,
            stroke_width=1.8,
            stroke_opacity=0.65,
        )
        part_connectors = VGroup(body_line, door_line, drawer_line)

        self.play(
            cabinet.door.animate.shift(LEFT * 0.18),
            cabinet.drawer.animate.shift(RIGHT * 0.18),
            run_time=0.55,
            rate_func=rate_functions.ease_out_cubic,
        )
        self.play(FadeIn(body_label, shift=RIGHT * 0.08), Create(body_line), run_time=0.45)
        self.play(FadeIn(door_label, shift=RIGHT * 0.08), Create(door_line), run_time=0.45)
        self.play(
            FadeIn(drawer_label, shift=RIGHT * 0.08),
            Create(drawer_line),
            run_time=0.45,
        )
        self.play(
            cabinet.door.animate.shift(RIGHT * 0.18),
            cabinet.drawer.animate.shift(LEFT * 0.18),
            run_time=0.55,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self._hold_until(24.0)
        self.play(
            Indicate(cabinet.fixed_body, color=FIXED_PART_COLOR, scale_factor=1.012),
            Indicate(cabinet.door_panel, color=REVOLUTE_JOINT_COLOR, scale_factor=1.025),
            Indicate(cabinet.drawer_panel, color=PRISMATIC_JOINT_COLOR, scale_factor=1.035),
            run_time=0.80,
        )
        self._hold_until(30.0)

        # 00:30-00:47 - establish the base part as fixed.
        fixed_token = self._motion_token("FIXED", FIXED_PART_COLOR)
        fixed_token.move_to(part_token)
        self.play(
            FadeOut(part_labels),
            FadeOut(part_connectors),
            FadeOut(part_token),
            FadeIn(fixed_token),
            cabinet.door_panel.animate.set_stroke(opacity=0.18).set_fill(opacity=0.04),
            cabinet.hinge_axis.animate.set_opacity(0.18),
            cabinet.door_handle.animate.set_opacity(0.18),
            cabinet.drawer_panel.animate.set_stroke(opacity=0.18).set_fill(opacity=0.04),
            cabinet.drawer_handle.animate.set_opacity(0.18),
            run_time=0.65,
        )
        self.play(
            Indicate(cabinet.fixed_body, color=FIXED_PART_COLOR, scale_factor=1.018),
            run_time=0.85,
        )
        anchor = VGroup(
            Line(LEFT * 0.42, RIGHT * 0.42, color=FIXED_PART_COLOR, stroke_width=3),
            Line(DOWN * 0.22, UP * 0.22, color=FIXED_PART_COLOR, stroke_width=3),
        ).move_to(cabinet.front_panel.get_bottom() + DOWN * 0.20)
        self.play(Create(anchor), run_time=0.45)
        self._hold_until(39.0)
        self.play(
            Indicate(fixed_token, color=FIXED_PART_COLOR, scale_factor=1.04),
            Indicate(cabinet.fixed_body, color=FIXED_PART_COLOR, scale_factor=1.012),
            run_time=0.75,
        )
        self._hold_until(47.0)

        # 00:47-01:08 - a revolute child rotates around one axis.
        revolute_token = self._motion_token("REVOLUTE", REVOLUTE_JOINT_COLOR)
        revolute_token.move_to(fixed_token).align_to(joint_token, LEFT)
        rotation_cue = create_rotation_axis(length=1.65).scale(0.62)
        rotation_cue.move_to(cabinet.hinge_axis.get_center() + LEFT * 0.03)
        self.play(
            FadeOut(fixed_token),
            FadeIn(revolute_token),
            cabinet.door_panel.animate.set_stroke(opacity=1).set_fill(opacity=0.20),
            cabinet.door_handle.animate.set_opacity(1),
            cabinet.drawer_panel.animate.set_stroke(opacity=0.12).set_fill(opacity=0.025),
            cabinet.drawer_handle.animate.set_opacity(0.12),
            cabinet.hinge_axis.animate.set_opacity(1),
            FadeOut(anchor),
            run_time=0.65,
        )
        self.play(Create(rotation_cue), run_time=0.70)
        rotation_cue.save_state()
        self.play(
            Transform(cabinet.door_panel, open_door),
            Transform(cabinet.door_handle, open_handle),
            run_time=1.10,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self._hold_until(56.0)
        self.play(
            Transform(cabinet.door_panel, closed_door),
            Transform(cabinet.door_handle, closed_handle),
            run_time=0.90,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            Transform(cabinet.door_panel, open_door),
            Transform(cabinet.door_handle, open_handle),
            run_time=1.00,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            Indicate(rotation_cue, color=REVOLUTE_JOINT_COLOR, scale_factor=1.04),
            run_time=0.70,
        )
        self._hold_until(68.0)

        # 01:08-01:29 - a prismatic child slides along one direction.
        prismatic_token = self._motion_token("PRISMATIC", PRISMATIC_JOINT_COLOR)
        prismatic_token.move_to(revolute_token).align_to(joint_token, LEFT)
        sliding_cue = create_sliding_arrow(length=1.70).scale(0.72)
        sliding_cue.move_to(cabinet.drawer_panel.get_center() + RIGHT * 0.90)
        self.play(
            FadeOut(revolute_token),
            FadeIn(prismatic_token),
            cabinet.door_panel.animate.set_stroke(opacity=0.22).set_fill(opacity=0.04),
            cabinet.hinge_axis.animate.set_opacity(0.22),
            cabinet.door_handle.animate.set_opacity(0.22),
            rotation_cue.animate.set_opacity(0.22),
            cabinet.drawer_panel.animate.set_stroke(opacity=1).set_fill(opacity=0.20),
            cabinet.drawer_handle.animate.set_opacity(1),
            run_time=0.65,
        )
        self.play(Create(sliding_cue), run_time=0.65)
        self.play(
            cabinet.drawer.animate.shift(RIGHT * 0.72),
            sliding_cue.animate.shift(RIGHT * 0.72),
            run_time=0.95,
            rate_func=rate_functions.ease_out_cubic,
        )
        self._hold_until(77.0)
        self.play(
            cabinet.drawer.animate.shift(LEFT * 0.72),
            sliding_cue.animate.shift(LEFT * 0.72),
            run_time=0.85,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            cabinet.drawer.animate.shift(RIGHT * 0.68),
            sliding_cue.animate.shift(RIGHT * 0.68),
            run_time=0.90,
            rate_func=rate_functions.ease_out_cubic,
        )
        self.play(
            Indicate(sliding_cue, color=PRISMATIC_JOINT_COLOR, scale_factor=1.035),
            run_time=0.70,
        )
        self._hold_until(89.0)

        # 01:29-01:43 - name all motion types supported by the representation.
        fixed_legend = self._motion_token("FIXED", FIXED_PART_COLOR)
        revolute_legend = self._motion_token("REVOLUTE", REVOLUTE_JOINT_COLOR)
        prismatic_legend = self._motion_token("PRISMATIC", PRISMATIC_JOINT_COLOR)
        both_legend = self._motion_token("BOTH", ACCENT_COLOR)
        motion_legend = VGroup(
            fixed_legend,
            revolute_legend,
            prismatic_legend,
            both_legend,
        ).arrange(RIGHT, buff=0.24)
        motion_legend.to_edge(UP, buff=0.42)
        both_legend.save_state()
        both_legend.scale(0.86)

        self.play(
            FadeOut(prismatic_token),
            FadeOut(joint_token),
            FadeOut(motion_token),
            cabinet.door_panel.animate.set_stroke(opacity=1).set_fill(opacity=0.20),
            cabinet.hinge_axis.animate.set_opacity(1),
            cabinet.door_handle.animate.set_opacity(1),
            rotation_cue.animate.restore(),
            FadeIn(fixed_legend, shift=DOWN * 0.06),
            run_time=0.65,
        )
        self.play(FadeIn(revolute_legend, shift=DOWN * 0.06), run_time=0.40)
        self.play(FadeIn(prismatic_legend, shift=DOWN * 0.06), run_time=0.40)
        self.play(FadeIn(both_legend, shift=DOWN * 0.06), run_time=0.40)
        self._hold_until(96.0)
        self.play(
            Indicate(cabinet.fixed_body, color=FIXED_PART_COLOR, scale_factor=1.010),
            Indicate(cabinet.door_panel, color=REVOLUTE_JOINT_COLOR, scale_factor=1.018),
            Indicate(cabinet.drawer_panel, color=PRISMATIC_JOINT_COLOR, scale_factor=1.025),
            run_time=0.80,
        )
        self.play(
            both_legend.animate.restore(),
            run_time=0.45,
            rate_func=rate_functions.ease_out_cubic,
        )
        self.play(
            Indicate(both_legend, color=ACCENT_COLOR, scale_factor=1.025),
            run_time=0.60,
        )
        self._hold_until(103.0)

        # 01:43-01:54 - organize parent-child joints as a rooted kinematic tree.
        tree = create_kinematic_tree(
            root_label="FIXED",
            child_labels=("REVOLUTE", "PRISMATIC"),
            child_colors=(REVOLUTE_JOINT_COLOR, PRISMATIC_JOINT_COLOR),
        ).scale(0.78)
        tree.move_to(RIGHT * 3.15 + DOWN * 0.40)
        tree_title = Text(
            "KINEMATIC TREE",
            font=DEFAULT_FONT,
            font_size=LABEL_FONT_SIZE,
            color=TEXT_COLOR,
            weight="SEMIBOLD",
        ).next_to(tree, UP, buff=0.30)

        articulated_object = VGroup(cabinet, rotation_cue, sliding_cue)
        articulated_object.generate_target()
        articulated_object.target.scale(0.78).move_to(LEFT * 2.75 + DOWN * 0.22)
        self.play(
            FadeOut(motion_legend, shift=UP * 0.05),
            MoveToTarget(articulated_object),
            self.camera.frame.animate.scale(1.03).move_to(RIGHT * 0.08),
            run_time=0.90,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(FadeIn(tree_title, shift=DOWN * 0.06), run_time=0.45)
        self.play(Create(tree[1]), run_time=0.45)
        self.play(Create(tree[0]), FadeIn(tree[2], shift=UP * 0.06), run_time=0.85)
        self._hold_until(111.0)
        self.play(
            Indicate(tree[1], color=FIXED_PART_COLOR, scale_factor=1.025),
            run_time=0.50,
        )
        self.play(
            Indicate(tree[2][0], color=REVOLUTE_JOINT_COLOR, scale_factor=1.025),
            Indicate(tree[2][1], color=PRISMATIC_JOINT_COLOR, scale_factor=1.025),
            run_time=0.55,
        )
        self._hold_until(114.0)

        # 01:54-02:00 - leave a clean articulated-object handoff for Scene 03.
        self.play(
            articulated_object.animate.scale(1.08).shift(RIGHT * 0.12),
            self.camera.frame.animate.scale(1.02),
            run_time=0.75,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            Indicate(rotation_cue, color=REVOLUTE_JOINT_COLOR, scale_factor=1.035),
            Indicate(sliding_cue, color=PRISMATIC_JOINT_COLOR, scale_factor=1.035),
            run_time=0.65,
        )
        self._hold_until(120.0)
