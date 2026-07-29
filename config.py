"""Shared visual and render configuration for the PARTICULATE video."""

from __future__ import annotations

from collections.abc import Iterable

# Final delivery settings. Low-quality CLI flags intentionally override these
# during development renders.
FINAL_PIXEL_WIDTH = 1920
FINAL_PIXEL_HEIGHT = 1080
FINAL_FRAME_RATE = 30

# Typography. The first installed font in this sequence is used.
FONT_FALLBACKS: tuple[str, ...] = ("Segoe UI", "Arial", "DejaVu Sans")
TITLE_FONT_SIZE = 54
SECTION_FONT_SIZE = 42
BODY_FONT_SIZE = 30
LABEL_FONT_SIZE = 24
CITATION_FONT_SIZE = 19

# Spatial rhythm in Manim coordinate units.
SPACING_XS = 0.12
SPACING_SMALL = 0.24
SPACING_MEDIUM = 0.48
SPACING_LARGE = 0.82
SPACING_XL = 1.20

# Semantic palette. Do not repurpose these colors with conflicting meanings.
BACKGROUND_COLOR = "#0B1020"
TEXT_COLOR = "#F4F7FB"
MUTED_TEXT_COLOR = "#AAB4C8"
FIXED_PART_COLOR = "#8B95A7"
REVOLUTE_JOINT_COLOR = "#FF5A67"
PRISMATIC_JOINT_COLOR = "#35C2D8"
INPUT_COLOR = "#F4F7FB"
OUTPUT_COLOR = "#69D58C"
ACCENT_COLOR = "#F2C14E"

DEFAULT_TRANSITION_DURATION = 0.60


def resolve_default_font(candidates: Iterable[str] = FONT_FALLBACKS) -> str:
    """Return the first available project font, with a deterministic fallback."""

    candidate_list = tuple(candidates)
    if not candidate_list:
        raise ValueError("At least one font candidate is required.")

    try:
        from manimpango import list_fonts

        installed = set(list_fonts())
    except (ImportError, OSError):
        return candidate_list[0]

    return next((font for font in candidate_list if font in installed), candidate_list[-1])


DEFAULT_FONT = resolve_default_font()


def apply_project_style() -> None:
    """Apply project-wide settings that should not defeat Manim quality flags."""

    from manim import config as manim_config

    manim_config.background_color = BACKGROUND_COLOR
