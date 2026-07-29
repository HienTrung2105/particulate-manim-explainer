"""Reusable visual components for all PARTICULATE scenes.

The components deliberately use 2D and light pseudo-3D geometry so they remain
fast to render and visually consistent across independently authored scenes.
"""

from __future__ import annotations

from collections.abc import Sequence

from manim import (
    DOWN,
    DR,
    LEFT,
    PI,
    RIGHT,
    UL,
    UP,
    UR,
    Arc,
    Arrow,
    DashedLine,
    Dot,
    Line,
    Polygon,
    RoundedRectangle,
    Text,
    VGroup,
)

from config import (
    ACCENT_COLOR,
    BODY_FONT_SIZE,
    CITATION_FONT_SIZE,
    DEFAULT_FONT,
    FIXED_PART_COLOR,
    INPUT_COLOR,
    LABEL_FONT_SIZE,
    MUTED_TEXT_COLOR,
    PRISMATIC_JOINT_COLOR,
    REVOLUTE_JOINT_COLOR,
    SECTION_FONT_SIZE,
    SPACING_SMALL,
    TEXT_COLOR,
)


def create_section_title(
    title: str,
    subtitle: str | None = None,
    *,
    font_size: int = SECTION_FONT_SIZE,
    subtitle_font_size: int = BODY_FONT_SIZE,
) -> VGroup:
    """Create a compact title block with an accent rule."""

    heading = Text(
        title,
        font=DEFAULT_FONT,
        font_size=font_size,
        color=TEXT_COLOR,
        weight="SEMIBOLD",
    )
    text_group = VGroup(heading)

    if subtitle:
        subtitle_text = Text(
            subtitle,
            font=DEFAULT_FONT,
            font_size=subtitle_font_size,
            color=MUTED_TEXT_COLOR,
        )
        text_group.add(subtitle_text)
        text_group.arrange(DOWN, aligned_edge=LEFT, buff=SPACING_SMALL)

    rule_width = max(2.4, min(text_group.width, 7.2))
    accent_rule = Line(
        LEFT * rule_width / 2,
        RIGHT * rule_width / 2,
        color=ACCENT_COLOR,
        stroke_width=4,
    ).next_to(text_group, DOWN, buff=SPACING_SMALL)

    return VGroup(text_group, accent_rule)


def create_pipeline_box(
    label: str,
    *,
    color: str = INPUT_COLOR,
    width: float = 2.45,
    height: float = 1.25,
) -> VGroup:
    """Create a semantic pipeline stage with a short centered label."""

    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        color=color,
        stroke_width=2.5,
        fill_color=color,
        fill_opacity=0.12,
    )
    text = Text(
        label,
        font=DEFAULT_FONT,
        font_size=LABEL_FONT_SIZE,
        color=TEXT_COLOR,
        line_spacing=0.8,
    )
    if text.width > width - 0.35:
        text.scale_to_fit_width(width - 0.35)
    if text.height > height - 0.25:
        text.scale_to_fit_height(height - 0.25)
    text.move_to(box)
    return VGroup(box, text)


def create_rotation_axis(
    *,
    length: float = 2.2,
    color: str = REVOLUTE_JOINT_COLOR,
) -> VGroup:
    """Create a dashed revolute axis and a restrained curved motion arrow."""

    axis = DashedLine(
        DOWN * length / 2,
        UP * length / 2,
        dash_length=0.12,
        color=color,
        stroke_width=3,
    )
    endpoints = VGroup(
        Dot(axis.get_start(), radius=0.055, color=color),
        Dot(axis.get_end(), radius=0.055, color=color),
    )
    motion_arc = Arc(
        radius=0.66,
        start_angle=-0.70 * PI,
        angle=1.35 * PI,
        color=color,
        stroke_width=3,
    )
    motion_arc.add_tip(tip_length=0.14)
    motion_arc.shift(RIGHT * 0.72)
    return VGroup(axis, endpoints, motion_arc)


def create_sliding_arrow(
    *,
    length: float = 2.2,
    color: str = PRISMATIC_JOINT_COLOR,
) -> VGroup:
    """Create a prismatic-motion guide and its linear direction arrow."""

    guide = DashedLine(
        LEFT * length / 2,
        RIGHT * length / 2,
        dash_length=0.13,
        color=MUTED_TEXT_COLOR,
        stroke_opacity=0.75,
    )
    direction = Arrow(
        LEFT * length * 0.34,
        RIGHT * length * 0.48,
        buff=0,
        color=color,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.16,
    )
    return VGroup(guide, direction)


def create_part_label(text: str, *, color: str = FIXED_PART_COLOR) -> VGroup:
    """Create a small legend-style label for an articulated part."""

    marker = Dot(radius=0.08, color=color)
    label = Text(text, font=DEFAULT_FONT, font_size=LABEL_FONT_SIZE, color=TEXT_COLOR)
    content = VGroup(marker, label).arrange(RIGHT, buff=SPACING_SMALL)
    background = RoundedRectangle(
        width=content.width + 0.42,
        height=content.height + 0.24,
        corner_radius=0.12,
        color=color,
        stroke_width=1.5,
        fill_color="#111A2E",
        fill_opacity=0.92,
    ).move_to(content)
    return VGroup(background, content)


def create_concept_token(text: str, *, color: str = ACCENT_COLOR) -> VGroup:
    """Create a compact concept token that can be transformed across scenes."""

    label = Text(
        text,
        font=DEFAULT_FONT,
        font_size=LABEL_FONT_SIZE,
        color=TEXT_COLOR,
        weight="SEMIBOLD",
    )
    token = RoundedRectangle(
        width=max(1.50, label.width + 0.52),
        height=0.66,
        corner_radius=0.18,
        color=color,
        stroke_width=2.3,
        fill_color=color,
        fill_opacity=0.10,
    )
    label.move_to(token)
    return VGroup(token, label)


class CabinetDiagram(VGroup):
    """Structured cabinet group with named sub-parts for scene animation."""

    fixed_body: VGroup
    door: VGroup
    door_panel: RoundedRectangle
    door_handle: Dot
    hinge_axis: DashedLine
    drawer: VGroup
    drawer_panel: RoundedRectangle
    drawer_handle: Line
    front_panel: RoundedRectangle


def create_cabinet_diagram(*, scale_factor: float = 1.0) -> CabinetDiagram:
    """Create a simple pseudo-3D cabinet with fixed, revolute and sliding parts."""

    front = RoundedRectangle(
        width=3.0,
        height=3.35,
        corner_radius=0.08,
        color=FIXED_PART_COLOR,
        stroke_width=2.5,
        fill_color=FIXED_PART_COLOR,
        fill_opacity=0.18,
    )
    depth_offset = RIGHT * 0.38 + UP * 0.25
    top = Polygon(
        front.get_corner(UL),
        front.get_corner(UR),
        front.get_corner(UR) + depth_offset,
        front.get_corner(UL) + depth_offset,
        color=FIXED_PART_COLOR,
        fill_color=FIXED_PART_COLOR,
        fill_opacity=0.28,
    )
    side = Polygon(
        front.get_corner(UR),
        front.get_corner(DR),
        front.get_corner(DR) + depth_offset,
        front.get_corner(UR) + depth_offset,
        color=FIXED_PART_COLOR,
        fill_color=FIXED_PART_COLOR,
        fill_opacity=0.10,
    )

    door = RoundedRectangle(
        width=1.25,
        height=2.05,
        corner_radius=0.05,
        color=REVOLUTE_JOINT_COLOR,
        fill_color=REVOLUTE_JOINT_COLOR,
        fill_opacity=0.18,
    ).move_to(front.get_center() + LEFT * 0.65 + UP * 0.34)
    hinge = DashedLine(
        door.get_corner(UL) + DOWN * 0.08,
        door.get_corner(UL) + DOWN * (door.height - 0.08),
        dash_length=0.10,
        color=REVOLUTE_JOINT_COLOR,
        stroke_width=3,
    )
    door_handle = Dot(door.get_right() + LEFT * 0.14, radius=0.055, color=TEXT_COLOR)

    drawer = RoundedRectangle(
        width=1.22,
        height=0.64,
        corner_radius=0.05,
        color=PRISMATIC_JOINT_COLOR,
        fill_color=PRISMATIC_JOINT_COLOR,
        fill_opacity=0.20,
    ).move_to(front.get_center() + RIGHT * 0.64 + DOWN * 0.92)
    drawer_handle = Line(
        LEFT * 0.16,
        RIGHT * 0.16,
        color=TEXT_COLOR,
        stroke_width=3,
    ).move_to(drawer)

    cabinet = CabinetDiagram(
        top,
        side,
        front,
        door,
        hinge,
        door_handle,
        drawer,
        drawer_handle,
    )
    cabinet.fixed_body = VGroup(top, side, front)
    cabinet.door = VGroup(door, hinge, door_handle)
    cabinet.door_panel = door
    cabinet.door_handle = door_handle
    cabinet.hinge_axis = hinge
    cabinet.drawer = VGroup(drawer, drawer_handle)
    cabinet.drawer_panel = drawer
    cabinet.drawer_handle = drawer_handle
    cabinet.front_panel = front
    return cabinet.scale(scale_factor)


class RobotDiagram(VGroup):
    """Structured robot group with named parts for simple interaction animation."""

    body: RoundedRectangle
    head: RoundedRectangle
    eyes: VGroup
    right_arm: Line
    right_hand: Dot


def create_robot_diagram(*, scale_factor: float = 1.0) -> RobotDiagram:
    """Create an original, neutral line-art robot for robotics analogies."""

    head = RoundedRectangle(
        width=1.28,
        height=0.82,
        corner_radius=0.18,
        color=MUTED_TEXT_COLOR,
        fill_color="#111A2E",
        fill_opacity=0.92,
        stroke_width=2.5,
    ).shift(UP * 1.02)
    eyes = VGroup(
        Dot(head.get_center() + LEFT * 0.27, radius=0.07, color=ACCENT_COLOR),
        Dot(head.get_center() + RIGHT * 0.27, radius=0.07, color=ACCENT_COLOR),
    )
    antenna = VGroup(
        Line(head.get_top(), head.get_top() + UP * 0.36, color=MUTED_TEXT_COLOR),
        Dot(head.get_top() + UP * 0.40, radius=0.065, color=ACCENT_COLOR),
    )

    body = RoundedRectangle(
        width=1.58,
        height=1.42,
        corner_radius=0.20,
        color=MUTED_TEXT_COLOR,
        fill_color=FIXED_PART_COLOR,
        fill_opacity=0.12,
        stroke_width=2.5,
    ).shift(DOWN * 0.20)
    chest = Line(LEFT * 0.32, RIGHT * 0.32, color=ACCENT_COLOR, stroke_width=3).move_to(
        body.get_center() + UP * 0.18
    )

    left_arm = Line(
        body.get_left() + UP * 0.32,
        body.get_left() + LEFT * 0.62 + DOWN * 0.18,
        color=MUTED_TEXT_COLOR,
        stroke_width=4,
    )
    right_arm = Line(
        body.get_right() + UP * 0.32,
        body.get_right() + RIGHT * 0.62 + DOWN * 0.18,
        color=MUTED_TEXT_COLOR,
        stroke_width=4,
    )
    hands = VGroup(
        Dot(left_arm.get_end(), radius=0.09, color=MUTED_TEXT_COLOR),
        Dot(right_arm.get_end(), radius=0.09, color=MUTED_TEXT_COLOR),
    )

    base = Line(LEFT * 0.62, RIGHT * 0.62, color=MUTED_TEXT_COLOR, stroke_width=4).next_to(
        body, DOWN, buff=0.12
    )
    wheels = VGroup(
        Dot(base.get_left() + RIGHT * 0.14 + DOWN * 0.12, radius=0.12, color=MUTED_TEXT_COLOR),
        Dot(base.get_right() + LEFT * 0.14 + DOWN * 0.12, radius=0.12, color=MUTED_TEXT_COLOR),
    )

    robot = RobotDiagram(
        body,
        chest,
        head,
        eyes,
        antenna,
        left_arm,
        right_arm,
        hands,
        base,
        wheels,
    )
    robot.body = body
    robot.head = head
    robot.eyes = eyes
    robot.right_arm = right_arm
    robot.right_hand = hands[1]
    return robot.scale(scale_factor)


def _create_tree_node(label: str, color: str) -> VGroup:
    text = Text(label, font=DEFAULT_FONT, font_size=LABEL_FONT_SIZE, color=TEXT_COLOR)
    width = max(1.85, text.width + 0.46)
    box = RoundedRectangle(
        width=width,
        height=0.72,
        corner_radius=0.12,
        color=color,
        fill_color=color,
        fill_opacity=0.12,
        stroke_width=2,
    )
    text.move_to(box)
    return VGroup(box, text)


def create_kinematic_tree(
    root_label: str = "Fixed body",
    child_labels: Sequence[str] = ("Door", "Drawer"),
    *,
    child_colors: Sequence[str] = (
        REVOLUTE_JOINT_COLOR,
        PRISMATIC_JOINT_COLOR,
    ),
) -> VGroup:
    """Create a compact parent-child kinematic tree."""

    if len(child_labels) != len(child_colors):
        raise ValueError("Each child label must have a matching semantic color.")

    root = _create_tree_node(root_label, FIXED_PART_COLOR).shift(UP * 1.10)
    children = VGroup()
    edges = VGroup()
    spacing = 2.35

    for index, (label, color) in enumerate(zip(child_labels, child_colors, strict=True)):
        x_position = (index - (len(child_labels) - 1) / 2) * spacing
        child = _create_tree_node(label, color).move_to(RIGHT * x_position + DOWN * 0.85)
        children.add(child)
        edge = Arrow(
            root.get_bottom(),
            child.get_top(),
            buff=0.08,
            color=color,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.12,
        )
        edges.add(edge)

    return VGroup(edges, root, children)


def create_footer_citation(citation: str, *, max_width: float = 12.6) -> VGroup:
    """Create a restrained footer citation suitable for paper-derived visuals."""

    rule = Line(LEFT * max_width / 2, RIGHT * max_width / 2, color=MUTED_TEXT_COLOR)
    text = Text(
        citation,
        font=DEFAULT_FONT,
        font_size=CITATION_FONT_SIZE,
        color=MUTED_TEXT_COLOR,
    )
    if text.width > max_width:
        text.scale_to_fit_width(max_width)
    text.next_to(rule, DOWN, buff=0.10).align_to(rule, LEFT)
    return VGroup(rule, text)
