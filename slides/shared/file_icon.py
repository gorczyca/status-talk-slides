from manim import *

from slides.shared.wrappers import TextWrapper


class FileIcon(VGroup):
    """A file icon with extension label and customizable accent color."""

    # Base dimensions (at scale=1.0)
    BASE_WIDTH = 1.0
    BASE_HEIGHT = 1.3
    BASE_FONT_SIZE = 24
    BASE_TITLE_FONT_SIZE = 20
    BASE_CAPTION_FONT_SIZE = 18
    BASE_STROKE_WIDTH = 2
    BASE_TITLE_BUFF = 0.15
    BASE_CAPTION_BUFF = 0.15

    def __init__(
        self,
        extension: str = ".txt",
        accent_color=BLUE,
        scale: float = 1.0,
        fold_size: float = 0.25,
        bg_color=WHITE,
        stroke_color=BLACK,
        title: str | None = None,
        title_color=BLACK,
        caption: str | None = None,
        caption_color=GREY,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Apply scale to all dimensions
        width = self.BASE_WIDTH * scale
        height = self.BASE_HEIGHT * scale
        font_size = self.BASE_FONT_SIZE * scale
        title_font_size = self.BASE_TITLE_FONT_SIZE * scale
        caption_font_size = self.BASE_CAPTION_FONT_SIZE * scale
        stroke_width = self.BASE_STROKE_WIDTH * scale
        title_buff = self.BASE_TITLE_BUFF * scale
        caption_buff = self.BASE_CAPTION_BUFF * scale

        # Scale fold size relative to width
        fold = fold_size * width

        # Main document body (rectangle with cut corner)
        points = [
            [-width/2, -height/2, 0],  # bottom left
            [width/2, -height/2, 0],   # bottom right
            [width/2, height/2 - fold, 0],  # top right (before fold)
            [width/2 - fold, height/2, 0],  # top right (after fold)
            [-width/2, height/2, 0],   # top left
        ]

        body = Polygon(
            *[np.array(p) for p in points],
            color=stroke_color,
            fill_color=bg_color,
            fill_opacity=1,
            stroke_width=stroke_width,
        )

        # Folded corner triangle
        fold_points = [
            [width/2 - fold, height/2, 0],
            [width/2, height/2 - fold, 0],
            [width/2 - fold, height/2 - fold, 0],
        ]

        fold_triangle = Polygon(
            *[np.array(p) for p in fold_points],
            color=stroke_color,
            fill_color=accent_color,
            fill_opacity=1,
            stroke_width=stroke_width,
        )

        # Accent bar in the center of the file (wider than the paper)
        bar_height = height * 0.28
        accent_bar = Rectangle(
            width=width * 1.15,
            height=bar_height,
            color=stroke_color,
            fill_color=accent_color,
            fill_opacity=1,
            stroke_width=stroke_width,
        ).move_to(body.get_center())

        # Extension text (white on the accent bar)
        ext_text = Text(
            extension,
            font_size=font_size,
            color=WHITE,
            weight=BOLD,
        ).move_to(accent_bar.get_center())

        # Scale text to fit in bar if needed
        if ext_text.width > width * 0.85:
            ext_text.scale_to_fit_width(width * 0.85)

        self.add(body, accent_bar, fold_triangle, ext_text)

        # Store references
        self.body = body
        self.fold_triangle = fold_triangle
        self.accent_bar = accent_bar
        self.ext_text = ext_text
        self.title_text = None
        self.caption_text = None
        self._scale = scale
        self._title_color = title_color
        self._caption_color = caption_color

        # Add title above the icon if provided
        if title is not None:
            self.title_text = TextWrapper(
                title,
                font_size=title_font_size,
                color=title_color,
            ).next_to(body, UP, buff=title_buff)
            self.add(self.title_text)

        # Add caption below the icon if provided
        if caption is not None:
            self.caption_text = TextWrapper(
                caption,
                font_size=caption_font_size,
                color=caption_color,
            ).next_to(body, DOWN, buff=caption_buff)
            self.add(self.caption_text)

    def set_accent_color(self, color):
        """Change the accent color of the icon."""
        self.fold_triangle.set_fill(color)
        self.accent_bar.set_fill(color)
        return self

    def set_title(self, text: str, color=None):
        """Set or update the title text above the icon."""
        if self.title_text is not None:
            self.remove(self.title_text)
        self.title_text = TextWrapper(
            text,
            font_size=self.BASE_TITLE_FONT_SIZE * self._scale,
            color=color if color is not None else self._title_color,
        ).next_to(self.body, UP, buff=self.BASE_TITLE_BUFF * self._scale)
        self.add(self.title_text)
        return self

    def set_caption(self, text: str, color=None):
        """Set or update the caption text below the icon."""
        if self.caption_text is not None:
            self.remove(self.caption_text)
        self.caption_text = TextWrapper(
            text,
            font_size=self.BASE_CAPTION_FONT_SIZE * self._scale,
            color=color if color is not None else self._caption_color,
        ).next_to(self.body, DOWN, buff=self.BASE_CAPTION_BUFF * self._scale)
        self.add(self.caption_text)
        return self
