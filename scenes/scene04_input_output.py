"""Scene 04: define PARTICULATE's static-mesh input and articulation output."""

from __future__ import annotations

from manim import (
    DL,
    DOWN,
    LEFT,
    PI,
    RIGHT,
    TAU,
    UL,
    UP,
    Arc,
    Arrow,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MoveToTarget,
    MovingCameraScene,
    Polygon,
    ReplacementTransform,
    RoundedRectangle,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
    rate_functions,
)

from common import (
    CabinetDiagram,
    create_cabinet_diagram,
    create_kinematic_tree,
    create_part_label,
    create_pipeline_box,
    create_rotation_axis,
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
    PRISMATIC_JOINT_COLOR,
    REVOLUTE_JOINT_COLOR,
    SECTION_FONT_SIZE,
    TEXT_COLOR,
    apply_project_style,
)

apply_project_style()


class Scene04InputOutput(MovingCameraScene):
    """Show the semantic interface between a static mesh and its articulation."""

    def _hold_until(self, target_time: float) -> None:
        """Pad the current beat to its absolute storyboard end time."""

        remaining = target_time - self.time
        if remaining < -0.05:
            raise RuntimeError(
                f"Scene 04 exceeded storyboard time {target_time:.2f}s "
                f"at {self.time:.2f}s."
            )
        if remaining > 0:
            self.wait(remaining)

    @staticmethod
    def _text(
        label: str,
        *,
        size: int = LABEL_FONT_SIZE,
        color: str = TEXT_COLOR,
        weight: str = "NORMAL",
    ) -> Text:
        return Text(
            label,
            font=DEFAULT_FONT,
            font_size=size,
            color=color,
            weight=weight,
        )

    @staticmethod
    def _laptop_icon() -> VGroup:
        screen = RoundedRectangle(
            width=1.75,
            height=1.12,
            corner_radius=0.08,
            color=FIXED_PART_COLOR,
            stroke_width=2.5,
            fill_color=FIXED_PART_COLOR,
            fill_opacity=0.10,
        )
        base = Polygon(
            screen.get_corner(DL),
            screen.get_corner(DL) + LEFT * 0.20 + DOWN * 0.24,
            screen.get_corner(DL) + RIGHT * 1.95 + DOWN * 0.24,
            screen.get_corner(DL) + RIGHT * 1.75,
            color=PRISMATIC_JOINT_COLOR,
            fill_color=PRISMATIC_JOINT_COLOR,
            fill_opacity=0.12,
        )
        return VGroup(screen, base)

    @staticmethod
    def _suitcase_icon() -> VGroup:
        body = RoundedRectangle(
            width=1.45,
            height=1.45,
            corner_radius=0.16,
            color=FIXED_PART_COLOR,
            stroke_width=2.5,
            fill_color=FIXED_PART_COLOR,
            fill_opacity=0.10,
        )
        handle = Arc(
            radius=0.34,
            start_angle=0,
            angle=PI,
            color=REVOLUTE_JOINT_COLOR,
            stroke_width=3,
        ).next_to(body, UP, buff=-0.02)
        seam = Line(
            body.get_top() + DOWN * 0.32,
            body.get_bottom() + UP * 0.30,
            color=PRISMATIC_JOINT_COLOR,
            stroke_width=2,
        )
        return VGroup(body, handle, seam)

    @staticmethod
    def _faucet_icon() -> VGroup:
        stem = Line(DOWN * 0.72, UP * 0.35, color=FIXED_PART_COLOR, stroke_width=6)
        spout = Arc(
            radius=0.56,
            start_angle=0,
            angle=PI,
            color=FIXED_PART_COLOR,
            stroke_width=6,
        ).move_to(UP * 0.34 + RIGHT * 0.42)
        outlet = Line(
            spout.get_end(),
            spout.get_end() + DOWN * 0.34,
            color=PRISMATIC_JOINT_COLOR,
            stroke_width=6,
        )
        lever = Line(
            stem.get_top(),
            stem.get_top() + LEFT * 0.48 + UP * 0.16,
            color=REVOLUTE_JOINT_COLOR,
            stroke_width=4,
        )
        return VGroup(stem, spout, outlet, lever)

    def _comparison_branch(self, label: str, *, feed_forward: bool) -> VGroup:
        color = OUTPUT_COLOR if feed_forward else FIXED_PART_COLOR
        title = self._text(label, color=color, weight="SEMIBOLD")
        if feed_forward:
            stages = VGroup(
                create_pipeline_box("STATIC 3D\nMESH", width=1.72, height=1.05),
                create_pipeline_box(
                    "PARTICULATE",
                    color=ACCENT_COLOR,
                    width=2.15,
                    height=1.05,
                ),
                create_pipeline_box(
                    "FULL\nARTICULATION",
                    color=OUTPUT_COLOR,
                    width=2.15,
                    height=1.05,
                ),
            ).arrange(RIGHT, buff=0.48)
            arrows = VGroup(
                Arrow(
                    stages[0].get_right(),
                    stages[1].get_left(),
                    buff=0.08,
                    color=ACCENT_COLOR,
                ),
                Arrow(
                    stages[1].get_right(),
                    stages[2].get_left(),
                    buff=0.08,
                    color=OUTPUT_COLOR,
                ),
            )
            content = VGroup(stages, arrows)
        else:
            icons = VGroup(
                self._laptop_icon().scale(0.42),
                self._suitcase_icon().scale(0.42),
                self._faucet_icon().scale(0.42),
            ).arrange(RIGHT, buff=0.72)
            rings = VGroup()
            for icon in icons:
                ring = Arc(
                    radius=0.22,
                    start_angle=PI / 2,
                    angle=-TAU * 0.80,
                    color=ACCENT_COLOR,
                    stroke_width=4,
                ).next_to(icon, DOWN, buff=0.18)
                rings.add(ring)
            content = VGroup(icons, rings)
        content.next_to(title, DOWN, buff=0.40)
        return VGroup(title, content)

    def _scene03_handoff(self) -> tuple[VGroup, VGroup, Line, VGroup]:
        """Recreate Scene 03's final two-branch comparison."""

        old_branch = self._comparison_branch("PER-OBJECT PROCESS", feed_forward=False)
        new_branch = self._comparison_branch("ONE FEED-FORWARD PASS", feed_forward=True)
        comparison = VGroup(old_branch, new_branch).arrange(DOWN, buff=0.86)
        comparison.scale_to_fit_width(9.40).move_to(UP * 0.25)
        divider = Line(
            LEFT * 4.75,
            RIGHT * 4.75,
            color=MUTED_TEXT_COLOR,
            stroke_opacity=0.18,
        ).move_to(UP * 0.25)

        no_optimization = self._text(
            "NO PER-OBJECT OPTIMIZATION",
            color=OUTPUT_COLOR,
            weight="SEMIBOLD",
        )
        caution = self._text(
            "≠ GUARANTEED PERFECT OUTPUT",
            color=MUTED_TEXT_COLOR,
        ).set_opacity(0.55)
        clarification = VGroup(no_optimization, caution).arrange(RIGHT, buff=0.56)
        clarification.next_to(new_branch, DOWN, buff=0.28)
        old_branch.set_opacity(0.42)
        return old_branch, new_branch, divider, clarification

    @staticmethod
    def _monochrome_cabinet(*, scale_factor: float = 1.0) -> CabinetDiagram:
        cabinet = create_cabinet_diagram(scale_factor=scale_factor)
        cabinet.set_color(INPUT_COLOR)
        cabinet.fixed_body.set_fill(INPUT_COLOR, opacity=0.10)
        cabinet.door_panel.set_fill(INPUT_COLOR, opacity=0.07)
        cabinet.drawer_panel.set_fill(INPUT_COLOR, opacity=0.07)
        return cabinet

    @staticmethod
    def _open_door_geometry(cabinet: CabinetDiagram) -> tuple[Polygon, Dot]:
        hinge_top = cabinet.door_panel.get_corner(UL)
        hinge_bottom = cabinet.door_panel.get_corner(DL)
        open_vector = LEFT * 0.78 + DOWN * 0.10
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
            radius=0.05,
            color=TEXT_COLOR,
        )
        return panel, handle

    def _mesh_cues(self, cabinet: CabinetDiagram) -> tuple[VGroup, VGroup]:
        """Create a sparse wireframe cue over the cabinet's front surface."""

        front = cabinet.front_panel
        center = front.get_center()
        corners = (front.get_corner(UL), front.get_corner(DL), front.get_corner(UL) + RIGHT * front.width, front.get_corner(DL) + RIGHT * front.width)
        vertices = VGroup(
            *(Dot(point, radius=0.045, color=ACCENT_COLOR) for point in (*corners, center))
        )
        edges = VGroup(
            Line(corners[0], center, color=MUTED_TEXT_COLOR, stroke_width=1.6),
            Line(corners[1], center, color=MUTED_TEXT_COLOR, stroke_width=1.6),
            Line(corners[2], center, color=MUTED_TEXT_COLOR, stroke_width=1.6),
            Line(corners[3], center, color=MUTED_TEXT_COLOR, stroke_width=1.6),
        )
        face = Polygon(
            corners[0],
            corners[2],
            center,
            color=ACCENT_COLOR,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.13,
            stroke_opacity=0.45,
        )
        return VGroup(edges, vertices), VGroup(face)

    @staticmethod
    def _range_marks(sliding_cue: VGroup) -> VGroup:
        guide = sliding_cue[0]
        return VGroup(
            Line(UP * 0.18, DOWN * 0.18, color=ACCENT_COLOR, stroke_width=3).move_to(
                guide.get_start()
            ),
            Line(UP * 0.18, DOWN * 0.18, color=ACCENT_COLOR, stroke_width=3).move_to(
                guide.get_end()
            ),
        )

    def construct(self) -> None:
        # Match Scene 03's final camera and two-branch composition.
        self.camera.frame.scale(0.96 * 1.03 * 1.02 * 1.02).move_to(
            RIGHT * 0.08 + DOWN * 0.05
        )
        old_branch, new_branch, divider, clarification = self._scene03_handoff()
        self.add(old_branch, new_branch, divider, clarification)

        # 00:00-00:12 - retain only the feed-forward branch and isolate its input.
        self.wait(0.40)
        self.play(
            FadeOut(old_branch, shift=UP * 0.10),
            FadeOut(divider),
            FadeOut(clarification, shift=DOWN * 0.08),
            run_time=0.75,
        )
        new_branch.generate_target()
        new_branch.target.scale(1.08).move_to(UP * 0.18)
        self.play(
            MoveToTarget(new_branch),
            self.camera.frame.animate.scale(1 / 1.02).move_to(UP * 0.02),
            run_time=0.85,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self._hold_until(5.0)

        stages = new_branch[1][0]
        branch_arrows = new_branch[1][1]
        input_cabinet = self._monochrome_cabinet(scale_factor=0.72)
        input_cabinet.move_to(LEFT * 3.15 + DOWN * 0.65)
        input_label = self._text("INPUT", color=INPUT_COLOR, weight="SEMIBOLD")
        input_label.next_to(input_cabinet, UP, buff=0.34)
        model_box = stages[1]
        model_target = model_box.copy().move_to(RIGHT * 2.55 + DOWN * 0.10)
        input_arrow = Arrow(
            input_cabinet.get_right(),
            model_target.get_left(),
            buff=0.25,
            color=ACCENT_COLOR,
            stroke_width=3,
        )
        self.play(
            FadeOut(new_branch[0], shift=UP * 0.08),
            FadeOut(stages[0]),
            FadeOut(stages[2]),
            FadeOut(branch_arrows),
            Transform(model_box, model_target),
            FadeIn(input_cabinet, shift=RIGHT * 0.10),
            FadeIn(input_label, shift=DOWN * 0.06),
            Create(input_arrow),
            run_time=0.95,
        )
        static_label = create_pipeline_box(
            "STATIC 3D MESH",
            color=INPUT_COLOR,
            width=2.65,
            height=0.76,
        ).next_to(input_cabinet, DOWN, buff=0.30)
        self.play(FadeIn(static_label, shift=UP * 0.06), run_time=0.45)
        self._hold_until(12.0)

        # 00:12-00:30 - a mesh contains vertices and faces in one static state.
        mesh_title = self._text(
            "MESH = VERTICES + FACES",
            size=SECTION_FONT_SIZE,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.58)
        one_state = self._text(
            "ONE STATIC STATE",
            color=MUTED_TEXT_COLOR,
            weight="SEMIBOLD",
        ).next_to(input_cabinet, DOWN, buff=0.48)
        input_cabinet.generate_target()
        input_cabinet.target.scale(1.20).move_to(DOWN * 0.25)
        self.play(
            FadeOut(VGroup(input_label, static_label, input_arrow, model_box)),
            FadeIn(mesh_title, shift=DOWN * 0.08),
            MoveToTarget(input_cabinet),
            run_time=0.85,
        )
        mesh_cues, face_cue = self._mesh_cues(input_cabinet)
        one_state.next_to(input_cabinet, DOWN, buff=0.48)
        self.play(Create(mesh_cues[0]), FadeIn(mesh_cues[1], scale=0.70), run_time=0.90)
        self.play(FadeIn(face_cue, scale=0.92), run_time=0.55)
        self._hold_until(23.0)
        self.play(FadeIn(one_state, shift=UP * 0.06), run_time=0.50)
        self.play(Indicate(face_cue, color=ACCENT_COLOR, scale_factor=1.02), run_time=0.60)
        self._hold_until(30.0)

        # 00:30-00:49 - assign every mesh region to an articulated part.
        segmentation_title = self._text(
            "PART SEGMENTATION",
            size=SECTION_FONT_SIZE,
            color=OUTPUT_COLOR,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.58)
        cabinet = input_cabinet
        cabinet.generate_target()
        cabinet.target.scale(0.82).move_to(LEFT * 2.80 + DOWN * 0.15)
        part_labels = VGroup(
            create_part_label("BODY", color=FIXED_PART_COLOR),
            create_part_label("DOOR", color=REVOLUTE_JOINT_COLOR),
            create_part_label("DRAWER", color=PRISMATIC_JOINT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36)
        part_labels.move_to(RIGHT * 2.75 + DOWN * 0.10)
        self.play(
            FadeOut(VGroup(mesh_cues, face_cue, one_state)),
            ReplacementTransform(mesh_title, segmentation_title),
            MoveToTarget(cabinet),
            run_time=0.80,
        )
        self.play(
            cabinet.fixed_body.animate.set_color(FIXED_PART_COLOR).set_fill(
                FIXED_PART_COLOR, opacity=0.18
            ),
            FadeIn(part_labels[0], shift=RIGHT * 0.08),
            run_time=0.65,
        )
        self.play(
            cabinet.door.animate.set_color(REVOLUTE_JOINT_COLOR),
            cabinet.door_panel.animate.set_fill(REVOLUTE_JOINT_COLOR, opacity=0.18),
            FadeIn(part_labels[1], shift=RIGHT * 0.08),
            run_time=0.65,
        )
        self.play(
            cabinet.drawer.animate.set_color(PRISMATIC_JOINT_COLOR),
            cabinet.drawer_panel.animate.set_fill(PRISMATIC_JOINT_COLOR, opacity=0.20),
            FadeIn(part_labels[2], shift=RIGHT * 0.08),
            run_time=0.65,
        )
        self._hold_until(42.0)
        self.play(
            LaggedStart(
                Indicate(cabinet.fixed_body, color=FIXED_PART_COLOR, scale_factor=1.012),
                Indicate(cabinet.door_panel, color=REVOLUTE_JOINT_COLOR, scale_factor=1.025),
                Indicate(cabinet.drawer_panel, color=PRISMATIC_JOINT_COLOR, scale_factor=1.035),
                lag_ratio=0.20,
            ),
            run_time=1.10,
        )
        self._hold_until(49.0)

        # 00:49-01:08 - organize the segmented parts as a rooted kinematic tree.
        tree_title = self._text(
            "KINEMATIC TREE",
            size=SECTION_FONT_SIZE,
            color=OUTPUT_COLOR,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.58)
        tree = create_kinematic_tree(
            root_label="BODY",
            child_labels=("DOOR", "DRAWER"),
            child_colors=(REVOLUTE_JOINT_COLOR, PRISMATIC_JOINT_COLOR),
        ).scale(0.88)
        tree.move_to(RIGHT * 2.75 + DOWN * 0.25)
        base_badge = self._text("BASE PART", color=FIXED_PART_COLOR, weight="SEMIBOLD")
        base_badge.next_to(tree[1], UP, buff=0.26)
        self.play(
            FadeOut(part_labels),
            ReplacementTransform(segmentation_title, tree_title),
            FadeIn(base_badge, shift=DOWN * 0.06),
            FadeIn(tree[1], shift=DOWN * 0.06),
            run_time=0.75,
        )
        self.play(Create(tree[0][0]), FadeIn(tree[2][0], shift=UP * 0.06), run_time=0.65)
        self.play(Create(tree[0][1]), FadeIn(tree[2][1], shift=UP * 0.06), run_time=0.65)
        self._hold_until(60.0)
        self.play(
            Indicate(tree[1], color=FIXED_PART_COLOR, scale_factor=1.025),
            run_time=0.50,
        )
        self.play(
            Indicate(tree[2][0], color=REVOLUTE_JOINT_COLOR, scale_factor=1.025),
            Indicate(tree[2][1], color=PRISMATIC_JOINT_COLOR, scale_factor=1.025),
            run_time=0.60,
        )
        self._hold_until(68.0)

        # 01:08-01:32 - reveal type, axis/direction and motion range constraints.
        motion_title = self._text(
            "MOTION CONSTRAINTS",
            size=SECTION_FONT_SIZE,
            color=OUTPUT_COLOR,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.58)
        cabinet.generate_target()
        cabinet.target.scale(1.12).move_to(LEFT * 2.45 + DOWN * 0.20)
        rotation_cue = create_rotation_axis(length=1.60).scale(0.60)
        rotation_cue.move_to(cabinet.target.hinge_axis.get_center() + LEFT * 0.02)
        sliding_cue = create_sliding_arrow(length=1.62).scale(0.72)
        sliding_cue.move_to(cabinet.target.drawer_panel.get_center() + RIGHT * 0.88)
        range_marks = self._range_marks(sliding_cue)
        constraint_tokens = VGroup(
            create_pipeline_box("TYPE", color=OUTPUT_COLOR, width=2.40, height=0.72),
            create_pipeline_box(
                "AXIS / DIRECTION",
                color=OUTPUT_COLOR,
                width=2.92,
                height=0.72,
            ),
            create_pipeline_box("RANGE", color=OUTPUT_COLOR, width=2.40, height=0.72),
        ).arrange(DOWN, buff=0.35)
        constraint_tokens.move_to(RIGHT * 3.35 + DOWN * 0.10)
        self.play(
            FadeOut(VGroup(tree, base_badge)),
            ReplacementTransform(tree_title, motion_title),
            MoveToTarget(cabinet),
            FadeIn(constraint_tokens[0], shift=LEFT * 0.08),
            run_time=0.80,
        )
        self.play(
            FadeIn(constraint_tokens[1], shift=LEFT * 0.08),
            Create(rotation_cue),
            Create(sliding_cue),
            run_time=0.85,
        )
        self.play(
            FadeIn(constraint_tokens[2], shift=LEFT * 0.08),
            Create(range_marks),
            run_time=0.65,
        )
        self._hold_until(79.0)

        closed_door = cabinet.door_panel.copy()
        closed_handle = cabinet.door_handle.copy()
        open_door, open_handle = self._open_door_geometry(cabinet)
        self.play(
            Transform(cabinet.door_panel, open_door),
            Transform(cabinet.door_handle, open_handle),
            run_time=0.90,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            cabinet.drawer.animate.shift(RIGHT * 0.62),
            sliding_cue.animate.shift(RIGHT * 0.62),
            run_time=0.85,
            rate_func=rate_functions.ease_out_cubic,
        )
        self._hold_until(86.0)
        self.play(
            Transform(cabinet.door_panel, closed_door),
            Transform(cabinet.door_handle, closed_handle),
            cabinet.drawer.animate.shift(LEFT * 0.62),
            sliding_cue.animate.shift(LEFT * 0.62),
            run_time=0.90,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            Indicate(rotation_cue, color=REVOLUTE_JOINT_COLOR, scale_factor=1.035),
            Indicate(sliding_cue, color=PRISMATIC_JOINT_COLOR, scale_factor=1.035),
            run_time=0.65,
        )
        self._hold_until(92.0)

        # 01:32-01:47 - combine all three layers into valid articulated states.
        states_title = self._text(
            "ARTICULATED STATES",
            size=SECTION_FONT_SIZE,
            color=OUTPUT_COLOR,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.58)
        state_one = create_cabinet_diagram(scale_factor=0.62)
        state_two = create_cabinet_diagram(scale_factor=0.62)
        state_one.move_to(LEFT * 2.75 + DOWN * 0.30)
        state_two.move_to(RIGHT * 2.75 + DOWN * 0.30)
        state_two_open_door, state_two_open_handle = self._open_door_geometry(state_two)
        state_two.door_panel.become(state_two_open_door)
        state_two.door_handle.become(state_two_open_handle)
        state_two.drawer.shift(RIGHT * 0.42)
        state_one_label = self._text("STATE 1", color=MUTED_TEXT_COLOR)
        state_two_label = self._text("STATE 2", color=MUTED_TEXT_COLOR)
        state_one_label.next_to(state_one, DOWN, buff=0.28)
        state_two_label.next_to(state_two, DOWN, buff=0.28)
        state_arrow = Arrow(
            state_one.get_right(),
            state_two.get_left(),
            buff=0.38,
            color=OUTPUT_COLOR,
            stroke_width=3,
        )
        self.play(
            FadeOut(VGroup(cabinet, rotation_cue, sliding_cue, range_marks, constraint_tokens)),
            ReplacementTransform(motion_title, states_title),
            FadeIn(state_one, shift=RIGHT * 0.08),
            FadeIn(state_one_label),
            run_time=0.80,
        )
        self.play(Create(state_arrow), run_time=0.50)
        self.play(
            TransformFromCopy(state_one, state_two),
            FadeIn(state_two_label),
            run_time=0.90,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self._hold_until(101.0)
        self.play(
            Indicate(state_one, color=OUTPUT_COLOR, scale_factor=1.02),
            Indicate(state_two, color=OUTPUT_COLOR, scale_factor=1.02),
            run_time=0.70,
        )
        self._hold_until(107.0)

        # 01:47-01:55 - the articulation parameterization can be exported to URDF.
        urdf_badge = create_pipeline_box(
            "URDF",
            color=ACCENT_COLOR,
            width=1.70,
            height=0.82,
        ).move_to(RIGHT * 4.95 + DOWN * 0.30)
        urdf_arrow = Arrow(
            state_two.get_right(),
            urdf_badge.get_left(),
            buff=0.18,
            color=ACCENT_COLOR,
            stroke_width=3,
        )
        simulator_label = self._text("SIMULATOR", color=MUTED_TEXT_COLOR)
        simulator_label.next_to(urdf_badge, DOWN, buff=0.22)
        self.play(Create(urdf_arrow), FadeIn(urdf_badge, shift=LEFT * 0.08), run_time=0.60)
        self.play(FadeIn(simulator_label, shift=UP * 0.05), run_time=0.45)
        self._hold_until(115.0)

        # 01:55-02:00 - leave Scene 05's compact pipeline handoff.
        final_input = create_pipeline_box(
            "3D MESH",
            color=INPUT_COLOR,
            width=2.10,
            height=1.15,
        )
        final_model = create_pipeline_box(
            "PARTICULATE",
            color=ACCENT_COLOR,
            width=2.55,
            height=1.15,
        )
        final_output = create_pipeline_box(
            "PARTS\nKINEMATIC TREE\nMOTION",
            color=OUTPUT_COLOR,
            width=3.55,
            height=1.68,
        )
        final_stages = VGroup(final_input, final_model, final_output).arrange(RIGHT, buff=0.90)
        final_arrows = VGroup(
            Arrow(final_input.get_right(), final_model.get_left(), buff=0.12, color=ACCENT_COLOR),
            Arrow(final_model.get_right(), final_output.get_left(), buff=0.12, color=OUTPUT_COLOR),
        )
        final_pipeline = VGroup(final_stages, final_arrows).move_to(DOWN * 0.05)
        self.play(
            FadeOut(
                VGroup(
                    states_title,
                    state_one,
                    state_two,
                    state_one_label,
                    state_two_label,
                    state_arrow,
                    urdf_badge,
                    urdf_arrow,
                    simulator_label,
                )
            ),
            FadeIn(final_stages, shift=UP * 0.06),
            run_time=0.70,
        )
        self.play(Create(final_arrows), run_time=0.45)
        self.play(Indicate(final_model, color=ACCENT_COLOR, scale_factor=1.025), run_time=0.60)
        self._hold_until(120.0)
