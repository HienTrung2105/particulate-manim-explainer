"""Scene 05: expand PARTICULATE into its token and decoder pipeline."""

from __future__ import annotations

from collections.abc import Sequence

from manim import (
    DOWN,
    LEFT,
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
    Line,
    MoveToTarget,
    MovingCameraScene,
    ReplacementTransform,
    RoundedRectangle,
    Text,
    VGroup,
    rate_functions,
)

from common import (
    create_cabinet_diagram,
    create_concept_token,
    create_footer_citation,
    create_pipeline_box,
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


class Scene05Pipeline(MovingCameraScene):
    """Explain point tokens, part queries, attention, and decoder heads."""

    HEAD_LABELS: tuple[str, ...] = (
        "Part Segmentation",
        "Kinematic Tree",
        "Articulation Type",
        "Articulation Axis",
        "Articulation Range",
    )

    def _hold_until(self, target_time: float) -> None:
        """Pad the current beat to its absolute storyboard end time."""

        remaining = target_time - self.time
        if remaining < -0.05:
            raise RuntimeError(
                f"Scene 05 exceeded storyboard time {target_time:.2f}s "
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

    def _scene04_handoff(self) -> tuple[VGroup, VGroup, VGroup]:
        """Recreate Scene 04's compact final pipeline."""

        input_box = create_pipeline_box(
            "3D MESH",
            color=INPUT_COLOR,
            width=2.10,
            height=1.15,
        )
        model_box = create_pipeline_box(
            "PARTICULATE",
            color=ACCENT_COLOR,
            width=2.55,
            height=1.15,
        )
        output_box = create_pipeline_box(
            "PARTS\nKINEMATIC TREE\nMOTION",
            color=OUTPUT_COLOR,
            width=3.55,
            height=1.68,
        )
        stages = VGroup(input_box, model_box, output_box).arrange(RIGHT, buff=0.90)
        arrows = VGroup(
            Arrow(
                input_box.get_right(),
                model_box.get_left(),
                buff=0.12,
                color=ACCENT_COLOR,
            ),
            Arrow(
                model_box.get_right(),
                output_box.get_left(),
                buff=0.12,
                color=OUTPUT_COLOR,
            ),
        )
        VGroup(stages, arrows).move_to(DOWN * 0.05)
        return stages, arrows, VGroup(stages, arrows)

    @staticmethod
    def _panel(
        width: float,
        height: float,
        *,
        color: str = MUTED_TEXT_COLOR,
        opacity: float = 0.045,
    ) -> RoundedRectangle:
        return RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.18,
            color=color,
            stroke_width=1.8,
            stroke_opacity=0.60,
            fill_color=color,
            fill_opacity=opacity,
        )

    def _feature_card(self, label: str) -> VGroup:
        return create_pipeline_box(
            label,
            color=INPUT_COLOR,
            width=2.75,
            height=0.78,
        )

    @staticmethod
    def _point_positions() -> tuple[tuple[float, float], ...]:
        """Return deterministic normalized samples over a cabinet silhouette."""

        grid = tuple(
            (x, y)
            for y in (-1.00, -0.66, -0.32, 0.02, 0.36, 0.70, 1.00)
            for x in (-0.92, -0.60, -0.28, 0.04, 0.36, 0.68, 0.92)
        )
        depth = (
            (1.03, -0.90),
            (1.12, -0.55),
            (1.12, -0.18),
            (1.12, 0.20),
            (1.12, 0.58),
            (1.08, 0.95),
            (-0.62, 1.10),
            (-0.18, 1.12),
            (0.28, 1.12),
            (0.72, 1.10),
        )
        return grid + depth

    def _sampled_points(
        self,
        center: Sequence[float],
        *,
        width: float = 2.35,
        height: float = 2.55,
        color: str = INPUT_COLOR,
    ) -> VGroup:
        points = VGroup()
        for x_value, y_value in self._point_positions():
            point = Dot(
                radius=0.035,
                color=color,
                fill_opacity=0.88,
            )
            point.move_to(
                center
                + RIGHT * (x_value * width / 2)
                + UP * (y_value * height / 2)
            )
            points.add(point)
        return points

    def _query_token(self, label: str, *, active: bool = True) -> VGroup:
        token = create_concept_token(label, color=ACCENT_COLOR)
        if not active:
            token.set_opacity(0.28)
        return token

    def _head_box(self, label: str) -> VGroup:
        return create_pipeline_box(
            label,
            color=OUTPUT_COLOR,
            width=3.00,
            height=0.62,
        )

    def _architecture_overview(self) -> tuple[VGroup, VGroup, VGroup]:
        """Create the expanded Figure-2-inspired architecture scaffold."""

        frame = self._panel(12.20, 5.25, color=ACCENT_COLOR, opacity=0.025)
        frame.move_to(DOWN * 0.05)
        dividers = VGroup(
            DashedLine(UP * 2.10, DOWN * 2.10, color=MUTED_TEXT_COLOR).shift(LEFT * 3.55),
            DashedLine(UP * 2.10, DOWN * 2.10, color=MUTED_TEXT_COLOR).shift(RIGHT * 1.35),
            DashedLine(UP * 2.10, DOWN * 2.10, color=MUTED_TEXT_COLOR).shift(RIGHT * 4.15),
        ).set_stroke(opacity=0.30)
        labels = VGroup(
            self._text("INPUT", color=MUTED_TEXT_COLOR, weight="SEMIBOLD"),
            self._text("PAT", color=ACCENT_COLOR, weight="SEMIBOLD"),
            self._text("HEADS", color=MUTED_TEXT_COLOR, weight="SEMIBOLD"),
            self._text("OUTPUT", color=MUTED_TEXT_COLOR, weight="SEMIBOLD"),
        )
        x_positions = (-4.82, -1.10, 2.72, 5.12)
        for label, x_position in zip(labels, x_positions, strict=True):
            label.move_to(RIGHT * x_position + UP * 2.20)
        return VGroup(frame, dividers), labels, VGroup(frame, dividers, labels)

    def _processed_architecture(
        self,
    ) -> tuple[VGroup, VGroup, VGroup, VGroup, VGroup, VGroup]:
        """Build the final token-to-head layout used for the Scene 06 handoff."""

        shell, labels, scaffold = self._architecture_overview()

        point_label = self._text("POINT TOKENS", color=INPUT_COLOR, weight="SEMIBOLD")
        point_tokens = VGroup(
            *(Dot(radius=0.075, color=INPUT_COLOR) for _ in range(7))
        ).arrange(RIGHT, buff=0.20)
        point_bundle = VGroup(point_label, point_tokens).arrange(DOWN, buff=0.24)
        point_bundle.move_to(LEFT * 4.80 + UP * 0.72)

        query_label = self._text("PART QUERIES", color=ACCENT_COLOR, weight="SEMIBOLD")
        query_tokens = VGroup(
            *(Dot(radius=0.095, color=ACCENT_COLOR) for _ in range(5))
        ).arrange(RIGHT, buff=0.24)
        query_bundle = VGroup(query_label, query_tokens).arrange(DOWN, buff=0.24)
        query_bundle.move_to(LEFT * 4.80 + DOWN * 0.92)
        token_bundles = VGroup(point_bundle, query_bundle)

        attention_box = create_pipeline_box(
            "REPEATED\nATTENTION\nBLOCKS ×B",
            color=ACCENT_COLOR,
            width=2.45,
            height=2.55,
        ).move_to(LEFT * 1.05 + DOWN * 0.12)
        into_attention = VGroup(
            Arrow(
                point_bundle.get_right(),
                attention_box.get_left() + UP * 0.52,
                buff=0.16,
                color=INPUT_COLOR,
                stroke_width=2.5,
            ),
            Arrow(
                query_bundle.get_right(),
                attention_box.get_left() + DOWN * 0.52,
                buff=0.16,
                color=ACCENT_COLOR,
                stroke_width=2.5,
            ),
        )

        heads = VGroup(*(self._head_box(label) for label in self.HEAD_LABELS))
        heads.arrange(DOWN, buff=0.20).move_to(RIGHT * 2.72 + DOWN * 0.10)
        head_arrows = VGroup(
            *(
                Arrow(
                    attention_box.get_right(),
                    head.get_left(),
                    buff=0.12,
                    color=OUTPUT_COLOR,
                    stroke_width=1.8,
                    max_tip_length_to_length_ratio=0.10,
                )
                for head in heads
            )
        )

        output_cabinet = create_cabinet_diagram(scale_factor=0.43)
        output_cabinet.move_to(RIGHT * 5.05 + DOWN * 0.10)
        output_arrow = Arrow(
            heads.get_right(),
            output_cabinet.get_left(),
            buff=0.22,
            color=OUTPUT_COLOR,
            stroke_width=2.6,
        )
        full = VGroup(
            scaffold,
            token_bundles,
            attention_box,
            into_attention,
            heads,
            head_arrows,
            output_cabinet,
            output_arrow,
        )
        return full, token_bundles, attention_box, heads, output_cabinet, labels

    def construct(self) -> None:
        # Match Scene 04's compact pipeline handoff.
        self.camera.frame.scale(0.96 * 1.03 * 1.02).move_to(UP * 0.02)
        stages, handoff_arrows, compact_pipeline = self._scene04_handoff()
        self.add(compact_pipeline)

        # 00:00-00:18 - open the model box into Figure 2's four functional regions.
        self.wait(0.40)
        overview_shell, overview_labels, overview = self._architecture_overview()
        overview_title = self._text(
            "PART ARTICULATION TRANSFORMER",
            size=SECTION_FONT_SIZE,
            color=ACCENT_COLOR,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.50)
        input_preview = create_pipeline_box(
            "POINT\nFEATURES",
            color=INPUT_COLOR,
            width=2.15,
            height=1.22,
        ).move_to(LEFT * 4.82 + DOWN * 0.10)
        pat_preview = create_pipeline_box(
            "TOKENS +\nATTENTION",
            color=ACCENT_COLOR,
            width=3.10,
            height=1.45,
        ).move_to(LEFT * 1.10 + DOWN * 0.10)
        heads_preview = create_pipeline_box(
            "5 DECODER\nHEADS",
            color=OUTPUT_COLOR,
            width=2.10,
            height=1.22,
        ).move_to(RIGHT * 2.72 + DOWN * 0.10)
        output_preview = create_pipeline_box(
            "ARTICULATED\nOBJECT",
            color=OUTPUT_COLOR,
            width=1.78,
            height=1.22,
        ).move_to(RIGHT * 5.12 + DOWN * 0.10)
        preview_stages = VGroup(input_preview, pat_preview, heads_preview, output_preview)
        preview_arrows = VGroup(
            Arrow(input_preview.get_right(), pat_preview.get_left(), buff=0.12, color=ACCENT_COLOR),
            Arrow(pat_preview.get_right(), heads_preview.get_left(), buff=0.12, color=OUTPUT_COLOR),
            Arrow(heads_preview.get_right(), output_preview.get_left(), buff=0.12, color=OUTPUT_COLOR),
        )
        self.play(
            FadeOut(stages[0]),
            FadeOut(stages[2]),
            FadeOut(handoff_arrows),
            ReplacementTransform(stages[1], overview_shell[0]),
            FadeIn(overview_shell[1]),
            FadeIn(overview_labels),
            FadeIn(overview_title, shift=DOWN * 0.08),
            run_time=0.95,
        )
        self.play(
            LaggedStart(*(FadeIn(stage, shift=UP * 0.06) for stage in preview_stages), lag_ratio=0.18),
            run_time=1.20,
        )
        self.play(LaggedStart(*(Create(arrow) for arrow in preview_arrows), lag_ratio=0.24), run_time=0.75)
        self._hold_until(10.0)
        self.play(
            Indicate(pat_preview, color=ACCENT_COLOR, scale_factor=1.025),
            run_time=0.65,
        )
        self._hold_until(18.0)

        # 00:18-00:42 - sample a point cloud from the mesh surface.
        sampling_title = self._text(
            "MESH → SAMPLED POINT CLOUD",
            size=SECTION_FONT_SIZE,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.56)
        mesh = create_cabinet_diagram(scale_factor=0.72)
        mesh.set_color(INPUT_COLOR).set_stroke(opacity=0.45)
        mesh.set_fill(opacity=0.035)
        mesh.move_to(LEFT * 2.70 + DOWN * 0.20)
        point_cloud = self._sampled_points(RIGHT * 2.70 + DOWN * 0.20)
        sample_arrow = Arrow(
            mesh.get_right(),
            point_cloud.get_left(),
            buff=0.35,
            color=ACCENT_COLOR,
            stroke_width=3,
        )
        mesh_label = self._text("INPUT MESH", color=MUTED_TEXT_COLOR)
        cloud_label = self._text("SAMPLED POINT CLOUD", color=INPUT_COLOR)
        mesh_label.next_to(mesh, DOWN, buff=0.28)
        cloud_label.next_to(point_cloud, DOWN, buff=0.28)
        self.play(
            FadeOut(VGroup(overview_shell, overview_labels, preview_stages, preview_arrows)),
            ReplacementTransform(overview_title, sampling_title),
            FadeIn(mesh, shift=RIGHT * 0.08),
            FadeIn(mesh_label),
            run_time=0.80,
        )
        self.play(Create(sample_arrow), run_time=0.55)
        self.play(
            LaggedStart(
                *(FadeIn(point, scale=0.55) for point in point_cloud),
                lag_ratio=0.018,
            ),
            run_time=1.65,
        )
        self.play(FadeIn(cloud_label, shift=UP * 0.06), run_time=0.45)
        self._hold_until(34.0)
        mesh_shadow = mesh.copy().move_to(point_cloud).set_stroke(opacity=0.18)
        self.play(FadeIn(mesh_shadow), run_time=0.40)
        self.play(Indicate(point_cloud, color=INPUT_COLOR, scale_factor=1.018), run_time=0.65)
        self._hold_until(42.0)

        # 00:42-01:08 - each point carries XYZ, normal, and PartField features.
        feature_title = self._text(
            "THREE INPUT FEATURES PER POINT",
            size=SECTION_FONT_SIZE,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.56)
        cloud_group = VGroup(point_cloud, mesh_shadow, cloud_label)
        cloud_group.generate_target()
        cloud_group.target.scale(0.82).move_to(LEFT * 4.25 + DOWN * 0.15)
        selected_point = Dot(radius=0.11, color=ACCENT_COLOR).move_to(LEFT * 2.55 + DOWN * 0.10)
        selected_ring = Circle(radius=0.24, color=ACCENT_COLOR, stroke_width=2.5).move_to(selected_point)
        feature_cards = VGroup(
            self._feature_card("XYZ"),
            self._feature_card("SURFACE NORMAL"),
            self._feature_card("PARTFIELD FEATURES"),
        ).arrange(DOWN, buff=0.34)
        feature_cards.move_to(RIGHT * 0.10 + DOWN * 0.05)
        feature_arrows = VGroup(
            *(
                Arrow(
                    selected_point.get_right(),
                    card.get_left(),
                    buff=0.18,
                    color=INPUT_COLOR,
                    stroke_width=2.2,
                    max_tip_length_to_length_ratio=0.11,
                )
                for card in feature_cards
            )
        )
        self.play(
            FadeOut(VGroup(mesh, mesh_label, sample_arrow)),
            ReplacementTransform(sampling_title, feature_title),
            MoveToTarget(cloud_group),
            FadeIn(selected_point, scale=0.70),
            Create(selected_ring),
            run_time=0.85,
        )
        for card, arrow in zip(feature_cards, feature_arrows, strict=True):
            self.play(Create(arrow), FadeIn(card, shift=RIGHT * 0.08), run_time=0.60)
        self._hold_until(56.0)
        feature_notes = VGroup(
            self._text("POSITION", color=MUTED_TEXT_COLOR),
            self._text("GEOMETRY", color=MUTED_TEXT_COLOR),
            self._text("SEMANTIC PART CUE", color=MUTED_TEXT_COLOR),
        )
        for note, card in zip(feature_notes, feature_cards, strict=True):
            note.next_to(card, RIGHT, buff=0.34)
        self.play(
            LaggedStart(*(FadeIn(note, shift=LEFT * 0.06) for note in feature_notes), lag_ratio=0.25),
            run_time=1.00,
        )
        self._hold_until(68.0)

        # 01:08-01:28 - separate MLPs map and sum features into one point token.
        token_title = self._text(
            "FEATURES → POINT TOKEN",
            size=SECTION_FONT_SIZE,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.56)
        mlp_badges = VGroup(
            *(create_pipeline_box("MLP", color=ACCENT_COLOR, width=1.20, height=0.62) for _ in range(3))
        )
        for badge, card in zip(mlp_badges, feature_cards, strict=True):
            badge.next_to(card, RIGHT, buff=0.30)
        sum_node = Circle(radius=0.27, color=ACCENT_COLOR, fill_color=ACCENT_COLOR, fill_opacity=0.10)
        plus = self._text("+", color=ACCENT_COLOR, weight="SEMIBOLD").move_to(sum_node)
        sum_group = VGroup(sum_node, plus).move_to(RIGHT * 3.30 + DOWN * 0.05)
        point_token = create_concept_token("POINT TOKEN", color=INPUT_COLOR)
        point_token.next_to(sum_group, RIGHT, buff=0.52)
        mlp_to_sum = VGroup(
            *(
                Arrow(
                    badge.get_right(),
                    sum_group.get_left(),
                    buff=0.12,
                    color=ACCENT_COLOR,
                    stroke_width=2.0,
                    max_tip_length_to_length_ratio=0.11,
                )
                for badge in mlp_badges
            )
        )
        self.play(
            FadeOut(feature_notes),
            ReplacementTransform(feature_title, token_title),
            LaggedStart(*(FadeIn(badge, shift=RIGHT * 0.06) for badge in mlp_badges), lag_ratio=0.20),
            run_time=0.85,
        )
        self.play(Create(mlp_to_sum), FadeIn(sum_group, scale=0.75), run_time=0.75)
        self.play(FadeIn(point_token, shift=RIGHT * 0.08), run_time=0.55)
        self._hold_until(80.0)
        self.play(
            Indicate(point_token, color=INPUT_COLOR, scale_factor=1.035),
            run_time=0.65,
        )
        self._hold_until(88.0)

        # 01:28-01:52 - add learnable queries because the true part count is unknown.
        query_title = self._text(
            "LEARNABLE PART QUERIES",
            size=SECTION_FONT_SIZE,
            color=ACCENT_COLOR,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.56)
        point_token_label = self._text("POINT TOKENS", color=INPUT_COLOR, weight="SEMIBOLD")
        point_token_row = VGroup(
            *(Dot(radius=0.07, color=INPUT_COLOR) for _ in range(13))
        ).arrange(RIGHT, buff=0.24)
        point_token_bundle = VGroup(point_token_label, point_token_row).arrange(DOWN, buff=0.28)
        point_token_bundle.move_to(UP * 0.78)
        query_tokens = VGroup(
            self._query_token("Q1"),
            self._query_token("Q2"),
            self._query_token("Q3"),
            self._query_token("Q4"),
            self._query_token("Q5", active=False),
            self._query_token("Q6", active=False),
        ).arrange(RIGHT, buff=0.28)
        query_tokens.move_to(DOWN * 0.88)
        unknown_count = self._text(
            "TRUE PART COUNT UNKNOWN",
            color=MUTED_TEXT_COLOR,
            weight="SEMIBOLD",
        ).next_to(query_tokens, DOWN, buff=0.40)
        self.play(
            FadeOut(
                VGroup(
                    cloud_group,
                    selected_point,
                    selected_ring,
                    feature_cards,
                    feature_arrows,
                    mlp_badges,
                    mlp_to_sum,
                    sum_group,
                    point_token,
                )
            ),
            ReplacementTransform(token_title, query_title),
            FadeIn(point_token_bundle, shift=DOWN * 0.06),
            run_time=0.90,
        )
        self.play(
            LaggedStart(*(FadeIn(token, shift=UP * 0.06) for token in query_tokens), lag_ratio=0.16),
            run_time=1.20,
        )
        self.play(FadeIn(unknown_count, shift=UP * 0.06), run_time=0.50)
        self._hold_until(102.0)
        self.play(
            Indicate(query_tokens[:4], color=ACCENT_COLOR, scale_factor=1.025),
            run_time=0.70,
        )
        self._hold_until(112.0)

        # 01:52-02:22 - alternate query self-attention and query-to-point cross-attention.
        self_attention_title = self._text(
            "1  QUERY SELF-ATTENTION",
            size=SECTION_FONT_SIZE,
            color=ACCENT_COLOR,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.56)
        query_tops = [token.get_top() for token in query_tokens[:4]]
        connection_pairs = ((0, 1), (1, 2), (2, 3), (0, 2), (1, 3))
        self_lines = VGroup(
            *(
                VGroup(
                    Line(
                        query_tops[start],
                        (query_tops[start] + query_tops[end]) / 2 + UP * (0.26 + 0.12 * (end - start)),
                        color=ACCENT_COLOR,
                        stroke_width=2.0,
                    ),
                    Line(
                        (query_tops[start] + query_tops[end]) / 2 + UP * (0.26 + 0.12 * (end - start)),
                        query_tops[end],
                        color=ACCENT_COLOR,
                        stroke_width=2.0,
                    ),
                )
                for start, end in connection_pairs
            )
        )
        self.play(
            FadeOut(unknown_count),
            ReplacementTransform(query_title, self_attention_title),
            run_time=0.60,
        )
        self.play(LaggedStart(*(Create(line) for line in self_lines), lag_ratio=0.18), run_time=1.10)
        self._hold_until(124.0)
        self.play(
            LaggedStart(
                *(Indicate(token, color=ACCENT_COLOR, scale_factor=1.04) for token in query_tokens[:4]),
                lag_ratio=0.18,
            ),
            run_time=1.00,
        )
        self._hold_until(128.0)

        cross_title = self._text(
            "2  QUERY-TO-POINT CROSS-ATTENTION",
            size=SECTION_FONT_SIZE,
            color=INPUT_COLOR,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.56)
        selected_points = (point_token_row[1], point_token_row[4], point_token_row[7], point_token_row[10])
        cross_arrows = VGroup(
            *(
                Arrow(
                    query_tokens[index].get_top(),
                    selected_points[index].get_bottom(),
                    buff=0.12,
                    color=INPUT_COLOR,
                    stroke_width=2.2,
                    max_tip_length_to_length_ratio=0.10,
                )
                for index in range(4)
            )
        )
        self.play(
            FadeOut(self_lines),
            ReplacementTransform(self_attention_title, cross_title),
            run_time=0.60,
        )
        self.play(LaggedStart(*(Create(arrow) for arrow in cross_arrows), lag_ratio=0.22), run_time=1.20)
        self._hold_until(136.0)
        self.play(
            LaggedStart(
                *(Indicate(point, color=INPUT_COLOR, scale_factor=1.35) for point in selected_points),
                lag_ratio=0.20,
            ),
            run_time=1.00,
        )
        self._hold_until(142.0)

        # 02:22-02:37 - explicitly exclude self-attention over all point tokens.
        no_point_title = self._text(
            "NO POINT SELF-ATTENTION",
            size=SECTION_FONT_SIZE,
            color=MUTED_TEXT_COLOR,
            weight="SEMIBOLD",
        ).move_to(UP * 0.10)
        prohibition = Cross(
            self._panel(5.70, 1.30, color=MUTED_TEXT_COLOR, opacity=0.025),
            stroke_color=REVOLUTE_JOINT_COLOR,
            stroke_width=7,
        ).move_to(no_point_title)
        scaling_note = self._text(
            "DENSE POINT CLOUD",
            color=INPUT_COLOR,
            weight="SEMIBOLD",
        ).next_to(no_point_title, DOWN, buff=0.72)
        self.play(
            FadeOut(VGroup(query_tokens, point_token_bundle, cross_arrows)),
            ReplacementTransform(cross_title, no_point_title),
            FadeIn(prohibition, scale=0.94),
            run_time=0.85,
        )
        self.play(FadeIn(scaling_note, shift=UP * 0.06), run_time=0.45)
        self._hold_until(150.0)
        self.play(Indicate(no_point_title, color=MUTED_TEXT_COLOR, scale_factor=1.02), run_time=0.60)
        self._hold_until(157.0)

        # 02:37-03:03 - expose the five specialized decoder heads.
        decoder_title = self._text(
            "FIVE DECODER HEADS",
            size=SECTION_FONT_SIZE,
            color=OUTPUT_COLOR,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.50)
        architecture, token_bundles, attention_box, heads, output_cabinet, arch_labels = (
            self._processed_architecture()
        )
        scaffold = architecture[0]
        into_attention = architecture[3]
        head_arrows = architecture[5]
        output_arrow = architecture[7]
        citation = create_footer_citation(
            "Li et al., PARTICULATE, CVPR 2026 — Fig. 2; Sec. 3.2–3.3",
            max_width=11.70,
        ).to_edge(DOWN, buff=0.30)
        self.play(
            FadeOut(VGroup(no_point_title, prohibition, scaling_note)),
            FadeIn(scaffold),
            FadeIn(token_bundles, shift=RIGHT * 0.06),
            FadeIn(attention_box, shift=RIGHT * 0.06),
            Create(into_attention),
            FadeIn(decoder_title, shift=DOWN * 0.06),
            FadeIn(citation),
            run_time=0.95,
        )
        for head, arrow in zip(heads, head_arrows, strict=True):
            self.play(Create(arrow), FadeIn(head, shift=RIGHT * 0.06), run_time=0.55)
        self._hold_until(176.0)
        self.play(
            LaggedStart(*(Indicate(head, color=OUTPUT_COLOR, scale_factor=1.018) for head in heads), lag_ratio=0.16),
            run_time=1.15,
        )
        self._hold_until(183.0)

        # 03:03-03:20 - connect point/part relationships to the articulated output.
        relation_title = self._text(
            "POINT + PART RELATIONSHIPS",
            size=SECTION_FONT_SIZE,
            color=OUTPUT_COLOR,
            weight="SEMIBOLD",
        ).to_edge(UP, buff=0.50)
        segmentation_tag = self._text(
            "POINT + PART",
            size=LABEL_FONT_SIZE * 0.72,
            color=INPUT_COLOR,
            weight="SEMIBOLD",
        )
        axis_tag = self._text(
            "POINT VOTES",
            size=LABEL_FONT_SIZE * 0.72,
            color=REVOLUTE_JOINT_COLOR,
            weight="SEMIBOLD",
        )
        segmentation_tag.scale_to_fit_width(1.28).move_to(RIGHT * 5.06 + UP * 1.12)
        axis_tag.scale_to_fit_width(1.28).move_to(RIGHT * 5.06 + DOWN * 1.12)
        vote_target = output_cabinet.hinge_axis.get_center()
        vote_points = VGroup(
            Dot(vote_target + LEFT * 0.55 + UP * 0.45, radius=0.05, color=REVOLUTE_JOINT_COLOR),
            Dot(vote_target + LEFT * 0.65, radius=0.05, color=REVOLUTE_JOINT_COLOR),
            Dot(vote_target + LEFT * 0.48 + DOWN * 0.46, radius=0.05, color=REVOLUTE_JOINT_COLOR),
        )
        vote_lines = VGroup(
            *(Line(point.get_center(), vote_target, color=REVOLUTE_JOINT_COLOR, stroke_width=1.8) for point in vote_points)
        )
        self.play(
            ReplacementTransform(decoder_title, relation_title),
            FadeIn(output_cabinet, shift=LEFT * 0.06),
            Create(output_arrow),
            run_time=0.75,
        )
        self.play(
            FadeIn(segmentation_tag, shift=LEFT * 0.05),
            FadeIn(axis_tag, shift=LEFT * 0.05),
            run_time=0.55,
        )
        self.play(FadeIn(vote_points), Create(vote_lines), run_time=0.70)
        self._hold_until(193.0)
        self.play(
            Indicate(heads[0], color=OUTPUT_COLOR, scale_factor=1.025),
            Indicate(heads[3], color=REVOLUTE_JOINT_COLOR, scale_factor=1.025),
            run_time=0.75,
        )
        self._hold_until(200.0)

        # 03:20-03:30 - preserve the expanded pipeline and highlight segmentation.
        self.play(
            FadeOut(VGroup(relation_title, segmentation_tag, axis_tag, vote_points, vote_lines)),
            heads[1:].animate.set_opacity(0.34),
            head_arrows[1:].animate.set_opacity(0.24),
            attention_box.animate.set_opacity(0.62),
            token_bundles.animate.set_opacity(0.62),
            self.camera.frame.animate.shift(RIGHT * 0.28).scale(0.985),
            run_time=0.85,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        segmentation_highlight = RoundedRectangle(
            width=heads[0].width + 0.24,
            height=heads[0].height + 0.20,
            corner_radius=0.14,
            color=OUTPUT_COLOR,
            stroke_width=4,
        ).move_to(heads[0])
        self.play(Create(segmentation_highlight), run_time=0.50)
        self.play(
            Indicate(heads[0], color=OUTPUT_COLOR, scale_factor=1.03),
            run_time=0.65,
        )
        # Cairo rounds each partial clip to a whole frame; this offset keeps the
        # concatenated preview at the 210-second production contract.
        self._hold_until(208.94)
