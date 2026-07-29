"""Short render test for typography, layout, shared components and encoding."""

from manim import (
    DOWN,
    RIGHT,
    UP,
    Arrow,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Scene,
    VGroup,
)

from common import create_footer_citation, create_pipeline_box, create_section_title
from config import (
    DEFAULT_TRANSITION_DURATION,
    FIXED_PART_COLOR,
    INPUT_COLOR,
    OUTPUT_COLOR,
    PRISMATIC_JOINT_COLOR,
    REVOLUTE_JOINT_COLOR,
    TITLE_FONT_SIZE,
    apply_project_style,
)

apply_project_style()


class SmokeTestScene(Scene):
    """Show the paper title and its high-level articulation pipeline."""

    def construct(self) -> None:
        paper_title = create_section_title(
            "PARTICULATE",
            "Feed-Forward 3D Object Articulation",
            font_size=TITLE_FONT_SIZE,
        )

        self.play(FadeIn(paper_title, shift=UP * 0.16), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(paper_title, shift=UP * 0.10), run_time=0.65)

        section_title = create_section_title("From static geometry to motion")
        section_title.scale(0.72).to_edge(UP, buff=0.52)
        self.play(
            FadeIn(section_title, shift=DOWN * 0.10),
            run_time=DEFAULT_TRANSITION_DURATION,
        )

        stage_data = (
            ("Static 3D\nObject", INPUT_COLOR),
            ("Parts", FIXED_PART_COLOR),
            ("Joints", REVOLUTE_JOINT_COLOR),
            ("Motion", OUTPUT_COLOR),
        )
        boxes = VGroup(
            *(create_pipeline_box(label, color=color) for label, color in stage_data)
        )
        boxes.arrange(RIGHT, buff=0.72).shift(DOWN * 0.25)

        arrows = VGroup(
            *(
                Arrow(
                    boxes[index].get_right(),
                    boxes[index + 1].get_left(),
                    buff=0.13,
                    color=PRISMATIC_JOINT_COLOR,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.18,
                )
                for index in range(len(boxes) - 1)
            )
        )

        for index, box in enumerate(boxes):
            self.play(FadeIn(box, shift=UP * 0.10), run_time=0.50)
            if index < len(arrows):
                self.wait(0.12)
                self.play(GrowArrow(arrows[index]), run_time=0.35)

        citation = create_footer_citation(
            "Li et al. | PARTICULATE | CVPR 2026"
        ).to_edge(DOWN, buff=0.30)
        self.play(FadeIn(citation), run_time=0.45)
        self.wait(1.0)
        self.play(
            LaggedStart(
                *(Indicate(box, color=box[0].get_color()) for box in boxes),
                lag_ratio=0.18,
            ),
            run_time=1.25,
        )
        self.wait(1.4)
        self.play(
            FadeOut(VGroup(section_title, boxes, arrows, citation)),
            run_time=0.65,
        )
