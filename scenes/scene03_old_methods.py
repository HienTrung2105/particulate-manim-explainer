"""Scene 03: contrast prior workflows with feed-forward articulation."""

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
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
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
    create_footer_citation,
    create_kinematic_tree,
    create_pipeline_box,
    create_rotation_axis,
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
    SECTION_FONT_SIZE,
    TEXT_COLOR,
    apply_project_style,
)

apply_project_style()


class Scene03OldMethods(MovingCameraScene):
    """Explain why articulation benefits from a single feed-forward model."""

    def _hold_until(self, target_time: float) -> None:
        """Pad the current beat to its absolute storyboard end time."""

        remaining = target_time - self.time
        if remaining < -0.05:
            raise RuntimeError(
                f"Scene 03 exceeded storyboard time {target_time:.2f}s "
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
    def _open_door_geometry(cabinet: CabinetDiagram) -> tuple[Polygon, Dot]:
        """Recreate the restrained pseudo-3D door state at Scene 02's end."""

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

    def _scene02_handoff(self) -> tuple[VGroup, VGroup]:
        """Build the final articulated-object composition from Scene 02."""

        cabinet = create_cabinet_diagram(scale_factor=1.06).shift(
            RIGHT * 2.05 + DOWN * 0.10
        )
        open_door, open_handle = self._open_door_geometry(cabinet)
        cabinet.door_panel.become(open_door)
        cabinet.door_handle.become(open_handle)
        cabinet.drawer.shift(RIGHT * 0.68)

        rotation_cue = create_rotation_axis(length=1.65).scale(0.62)
        rotation_cue.move_to(cabinet.hinge_axis.get_center() + LEFT * 0.03)
        sliding_cue = create_sliding_arrow(length=1.70).scale(0.72)
        sliding_cue.move_to(cabinet.drawer_panel.get_center() + RIGHT * 0.90)

        articulated_object = VGroup(cabinet, rotation_cue, sliding_cue)
        articulated_object.scale(0.78).move_to(LEFT * 2.75 + DOWN * 0.22)
        articulated_object.scale(1.08).shift(RIGHT * 0.12)

        tree = create_kinematic_tree(
            root_label="FIXED",
            child_labels=("REVOLUTE", "PRISMATIC"),
            child_colors=(REVOLUTE_JOINT_COLOR, PRISMATIC_JOINT_COLOR),
        ).scale(0.78)
        tree.move_to(RIGHT * 3.15 + DOWN * 0.40)
        tree_title = self._text("KINEMATIC TREE", weight="SEMIBOLD")
        tree_title.next_to(tree, UP, buff=0.30)
        return articulated_object, VGroup(tree, tree_title)

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

    def _object_gallery(self, cabinet: VGroup) -> VGroup:
        laptop = self._laptop_icon()
        suitcase = self._suitcase_icon()
        faucet = self._faucet_icon()
        gallery = VGroup(cabinet, laptop, suitcase, faucet)
        gallery.arrange(RIGHT, buff=0.95).move_to(DOWN * 0.25)
        return gallery

    def _lane(self, label: str, note: str) -> VGroup:
        box = create_pipeline_box(label, color=FIXED_PART_COLOR, width=3.70, height=0.82)
        note_text = self._text(note, color=MUTED_TEXT_COLOR)
        note_text.next_to(box, RIGHT, buff=0.55)
        arrow = Arrow(
            box.get_right(),
            note_text.get_left(),
            buff=0.16,
            color=MUTED_TEXT_COLOR,
            stroke_width=2.4,
            max_tip_length_to_length_ratio=0.14,
        )
        return VGroup(box, arrow, note_text)

    def _progress_card(self, icon: VGroup) -> tuple[VGroup, Arc]:
        card = RoundedRectangle(
            width=3.10,
            height=2.35,
            corner_radius=0.18,
            color=FIXED_PART_COLOR,
            fill_color=FIXED_PART_COLOR,
            fill_opacity=0.055,
            stroke_width=1.8,
        )
        icon_copy = icon.copy().scale_to_fit_height(0.95).move_to(card.get_center() + UP * 0.34)
        ring_base = Circle(radius=0.25, color=MUTED_TEXT_COLOR, stroke_opacity=0.30)
        ring_base.move_to(card.get_center() + DOWN * 0.72)
        ring = Arc(
            radius=0.25,
            start_angle=PI / 2,
            angle=-TAU * 0.84,
            color=ACCENT_COLOR,
            stroke_width=5,
        ).move_to(ring_base)
        return VGroup(card, icon_copy, ring_base), ring

    def _missing_output(self, label: str, *, missing: bool) -> VGroup:
        width = 2.42
        height = 0.74
        if missing:
            half_w = width / 2
            half_h = height / 2
            border = VGroup(
                DashedLine(LEFT * half_w + UP * half_h, RIGHT * half_w + UP * half_h),
                DashedLine(RIGHT * half_w + UP * half_h, RIGHT * half_w + DOWN * half_h),
                DashedLine(RIGHT * half_w + DOWN * half_h, LEFT * half_w + DOWN * half_h),
                DashedLine(LEFT * half_w + DOWN * half_h, LEFT * half_w + UP * half_h),
            ).set_color(MUTED_TEXT_COLOR).set_stroke(opacity=0.62)
            text_color = MUTED_TEXT_COLOR
        else:
            border = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.12,
                color=OUTPUT_COLOR,
                fill_color=OUTPUT_COLOR,
                fill_opacity=0.10,
                stroke_width=2.2,
            )
            text_color = TEXT_COLOR
        label_text = self._text(label, color=text_color)
        if label_text.width > width - 0.30:
            label_text.scale_to_fit_width(width - 0.30)
        label_text.move_to(border)
        return VGroup(border, label_text)

    def _comparison_branch(self, label: str, *, feed_forward: bool) -> VGroup:
        color = OUTPUT_COLOR if feed_forward else FIXED_PART_COLOR
        title = self._text(label, color=color, weight="SEMIBOLD")
        if feed_forward:
            stages = VGroup(
                create_pipeline_box("STATIC 3D\nMESH", width=1.72, height=1.05),
                create_pipeline_box("PARTICULATE", color=ACCENT_COLOR, width=2.15, height=1.05),
                create_pipeline_box("FULL\nARTICULATION", color=OUTPUT_COLOR, width=2.15, height=1.05),
            ).arrange(RIGHT, buff=0.48)
            arrows = VGroup(
                Arrow(stages[0].get_right(), stages[1].get_left(), buff=0.08, color=ACCENT_COLOR),
                Arrow(stages[1].get_right(), stages[2].get_left(), buff=0.08, color=OUTPUT_COLOR),
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

    def construct(self) -> None:
        # Match Scene 02's final camera and articulated-object composition.
        self.camera.frame.scale(0.96 * 1.03 * 1.02).move_to(RIGHT * 0.08)
        articulated_object, tree_group = self._scene02_handoff()
        self.add(articulated_object, tree_group)

        # 00:00-00:18 - expand one articulated object into a diverse object set.
        self.wait(0.40)
        cabinet_icon = articulated_object[0].copy()
        cabinet_icon.scale_to_fit_height(1.42)
        gallery = self._object_gallery(cabinet_icon)
        gallery_title = self._text(
            "MANY NEW OBJECTS",
            size=SECTION_FONT_SIZE,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.62)
        self.play(
            FadeOut(tree_group, shift=RIGHT * 0.12),
            FadeOut(articulated_object[1:]),
            Transform(articulated_object[0], gallery[0]),
            FadeIn(gallery_title, shift=DOWN * 0.08),
            run_time=1.00,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            LaggedStart(
                *(
                    TransformFromCopy(articulated_object[0], object_icon)
                    for object_icon in gallery[1:]
                ),
                lag_ratio=0.24,
            ),
            run_time=1.55,
        )
        self._hold_until(12.0)
        diversity_label = self._text(
            "A WORKFLOW MUST RUN AGAIN FOR EACH NEW OBJECT",
            color=MUTED_TEXT_COLOR,
        ).next_to(gallery, DOWN, buff=0.62)
        self.play(FadeIn(diversity_label, shift=UP * 0.08), run_time=0.60)
        self._hold_until(18.0)

        # 00:18-00:42 - prior approaches solve different tasks and use different inputs.
        lane_title = self._text(
            "PRIOR APPROACHES ≠ ONE TASK",
            size=SECTION_FONT_SIZE,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.58)
        lanes = VGroup(
            self._lane("SEGMENTATION ONLY", "PARTS"),
            self._lane("IMAGES / VIDEO", "RECONSTRUCTION"),
            self._lane("EXTRA PRIOR / PROMPT", "DIFFERENT ASSUMPTIONS"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.56)
        lanes.move_to(DOWN * 0.20)
        self.play(
            FadeOut(VGroup(articulated_object[0], gallery[1:], diversity_label)),
            ReplacementTransform(gallery_title, lane_title),
            run_time=0.75,
        )
        for lane in lanes:
            self.play(FadeIn(lane[0], shift=RIGHT * 0.10), run_time=0.50)
            self.play(Create(lane[1]), FadeIn(lane[2], shift=RIGHT * 0.08), run_time=0.55)
        self._hold_until(32.0)
        self.play(
            LaggedStart(
                *(Indicate(lane[2], color=ACCENT_COLOR, scale_factor=1.025) for lane in lanes),
                lag_ratio=0.25,
            ),
            run_time=1.20,
        )
        self._hold_until(42.0)

        # 00:42-01:06 - some reconstruction methods optimize each test object separately.
        optimization_title = self._text(
            "PER-OBJECT OPTIMIZATION",
            size=SECTION_FONT_SIZE,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.58)
        source_icons = (
            self._laptop_icon(),
            self._suitcase_icon(),
            self._faucet_icon(),
        )
        card_data = [self._progress_card(icon) for icon in source_icons]
        cards = VGroup(*(card for card, _ in card_data)).arrange(RIGHT, buff=0.68)
        cards.move_to(DOWN * 0.22)
        rings = VGroup(*(ring for _, ring in card_data))
        self.play(
            FadeOut(lanes),
            ReplacementTransform(lane_title, optimization_title),
            FadeIn(cards, shift=UP * 0.08),
            run_time=0.80,
        )
        self.play(LaggedStart(*(Create(ring) for ring in rings), lag_ratio=0.48), run_time=2.20)
        restart_label = self._text(
            "RESTART FOR EACH OBJECT",
            color=ACCENT_COLOR,
            weight="SEMIBOLD",
        ).next_to(cards, DOWN, buff=0.48)
        self.play(FadeIn(restart_label, shift=UP * 0.08), run_time=0.55)
        self._hold_until(56.0)
        self.play(
            LaggedStart(
                *(Indicate(ring, color=ACCENT_COLOR, scale_factor=1.08) for ring in rings),
                lag_ratio=0.32,
            ),
            run_time=1.50,
        )
        self._hold_until(66.0)

        # 01:06-01:30 - Table 1 reports varied runtimes, including unreported entries.
        runtime_title = self._text(
            "REPORTED RUNTIME VARIES",
            size=SECTION_FONT_SIZE,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.58)
        scale_line = Line(LEFT * 4.10, RIGHT * 3.35, color=MUTED_TEXT_COLOR, stroke_width=3)
        scale_line.shift(UP * 0.15)
        scale_line.add_tip(tip_length=0.18)
        seconds_label = self._text("SECONDS", color=MUTED_TEXT_COLOR)
        minutes_label = self._text("MINUTES", color=MUTED_TEXT_COLOR)
        seconds_label.next_to(scale_line.get_start(), DOWN, buff=0.28)
        minutes_label.next_to(scale_line.get_end(), DOWN, buff=0.28)
        markers = VGroup(
            Dot(scale_line.point_from_proportion(0.16), radius=0.09, color=ACCENT_COLOR),
            Dot(scale_line.point_from_proportion(0.54), radius=0.09, color=ACCENT_COLOR),
            Dot(scale_line.point_from_proportion(0.86), radius=0.09, color=ACCENT_COLOR),
        )
        na_badge = create_pipeline_box("N/A", color=FIXED_PART_COLOR, width=1.42, height=0.72)
        na_badge.next_to(scale_line, DOWN, buff=1.10)
        citation = create_footer_citation(
            "Li et al., PARTICULATE, CVPR 2026 — Table 1"
        ).to_edge(DOWN, buff=0.32)
        self.play(
            FadeOut(VGroup(cards, rings, restart_label)),
            ReplacementTransform(optimization_title, runtime_title),
            Create(scale_line),
            run_time=0.85,
        )
        self.play(
            FadeIn(seconds_label),
            FadeIn(minutes_label),
            LaggedStart(*(FadeIn(marker, scale=0.7) for marker in markers), lag_ratio=0.22),
            run_time=1.00,
        )
        self.play(FadeIn(na_badge, shift=UP * 0.08), FadeIn(citation), run_time=0.65)
        self._hold_until(80.0)
        self.play(Indicate(runtime_title, color=ACCENT_COLOR, scale_factor=1.02), run_time=0.70)
        self._hold_until(90.0)

        # 01:30-01:52 - mismatched inputs and assumptions do not form one complete output.
        mismatch_title = self._text(
            "NOT ONE SHARED TASK",
            size=SECTION_FONT_SIZE,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.58)
        inputs = VGroup(
            create_pipeline_box("INPUT A", color=FIXED_PART_COLOR, width=2.15, height=0.72),
            create_pipeline_box("INPUT B", color=FIXED_PART_COLOR, width=2.15, height=0.72),
            create_pipeline_box("INPUT C", color=FIXED_PART_COLOR, width=2.15, height=0.72),
        ).arrange(DOWN, buff=0.38)
        inputs.move_to(LEFT * 3.65 + DOWN * 0.18)
        outputs = VGroup(
            self._missing_output("PARTS", missing=False),
            self._missing_output("KINEMATIC TREE", missing=True),
            self._missing_output("MOTION", missing=True),
        ).arrange(DOWN, buff=0.38)
        outputs.move_to(RIGHT * 3.45 + DOWN * 0.18)
        mismatch_arrows = VGroup(
            *(
                Arrow(
                    inputs[i].get_right(),
                    outputs[i].get_left(),
                    buff=0.20,
                    color=MUTED_TEXT_COLOR,
                    stroke_width=2.2,
                    max_tip_length_to_length_ratio=0.10,
                )
                for i in range(3)
            )
        )
        self.play(
            FadeOut(VGroup(scale_line, seconds_label, minutes_label, markers, na_badge, citation)),
            ReplacementTransform(runtime_title, mismatch_title),
            FadeIn(inputs, shift=RIGHT * 0.08),
            run_time=0.80,
        )
        self.play(LaggedStart(*(Create(arrow) for arrow in mismatch_arrows), lag_ratio=0.20), run_time=0.85)
        self.play(FadeIn(outputs[0], shift=LEFT * 0.08), run_time=0.45)
        self.play(FadeIn(outputs[1], shift=LEFT * 0.08), run_time=0.45)
        self.play(FadeIn(outputs[2], shift=LEFT * 0.08), run_time=0.45)
        self._hold_until(102.0)
        self.play(
            Indicate(outputs[1], color=MUTED_TEXT_COLOR, scale_factor=1.025),
            Indicate(outputs[2], color=MUTED_TEXT_COLOR, scale_factor=1.025),
            run_time=0.75,
        )
        self._hold_until(112.0)

        # 01:52-02:12 - replace heterogeneous lanes with one feed-forward prediction path.
        old_branch = self._comparison_branch("PER-OBJECT PROCESS", feed_forward=False)
        new_branch = self._comparison_branch("ONE FEED-FORWARD PASS", feed_forward=True)
        comparison = VGroup(old_branch, new_branch).arrange(DOWN, buff=0.86)
        comparison.scale_to_fit_width(9.40).move_to(UP * 0.25)
        divider = Line(LEFT * 4.75, RIGHT * 4.75, color=MUTED_TEXT_COLOR, stroke_opacity=0.30)
        divider.move_to(UP * 0.25)
        self.play(
            FadeOut(VGroup(inputs, mismatch_arrows, outputs)),
            FadeOut(mismatch_title, shift=UP * 0.08),
            FadeIn(old_branch, shift=DOWN * 0.08),
            Create(divider),
            run_time=0.90,
        )
        self.play(FadeIn(new_branch[0], shift=DOWN * 0.08), run_time=0.50)
        self.play(
            LaggedStart(*(FadeIn(stage, shift=RIGHT * 0.08) for stage in new_branch[1][0]), lag_ratio=0.22),
            run_time=1.10,
        )
        self.play(LaggedStart(*(Create(arrow) for arrow in new_branch[1][1]), lag_ratio=0.25), run_time=0.80)
        self._hold_until(124.0)
        self.play(
            Indicate(new_branch[1][1][0], color=ACCENT_COLOR, scale_factor=1.03),
            Indicate(new_branch[1][1][1], color=OUTPUT_COLOR, scale_factor=1.03),
            run_time=0.75,
        )
        self._hold_until(132.0)

        # 02:12-02:24 - clarify what feed-forward does and does not claim.
        no_optimization = self._text(
            "NO PER-OBJECT OPTIMIZATION",
            color=OUTPUT_COLOR,
            weight="SEMIBOLD",
        )
        no_optimization.next_to(new_branch, DOWN, buff=0.34)
        caution = self._text(
            "≠ GUARANTEED PERFECT OUTPUT",
            color=MUTED_TEXT_COLOR,
        )
        clarification = VGroup(no_optimization, caution).arrange(RIGHT, buff=0.56)
        clarification.next_to(new_branch, DOWN, buff=0.28)
        self.play(FadeIn(no_optimization, shift=UP * 0.08), run_time=0.55)
        self._hold_until(137.0)
        self.play(FadeIn(caution, shift=LEFT * 0.08), run_time=0.50)
        self.play(Indicate(no_optimization, color=OUTPUT_COLOR, scale_factor=1.025), run_time=0.65)
        self._hold_until(144.0)

        # 02:24-02:30 - hold both branches, with feed-forward emphasized for Scene 04.
        self.play(
            old_branch.animate.set_opacity(0.42),
            divider.animate.set_stroke(opacity=0.18),
            caution.animate.set_opacity(0.55),
            self.camera.frame.animate.shift(DOWN * 0.05).scale(1.02),
            run_time=0.80,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(
            Indicate(new_branch, color=OUTPUT_COLOR, scale_factor=1.012),
            run_time=0.65,
        )
        self._hold_until(150.0)
