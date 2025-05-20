from typing import Any
from shiny import ui
from shinyswatch.theme import flatly as shiny_theme
from pathlib import Path

# Theme: handles optional CSS overrides and base theme
class Theme:
    theme_file = None

    @classmethod
        # Returns the path to theme.css if available, otherwise defaults
    def get_theme_css(cls):
        # Fallback to a static theme.css in the same folder as this file
        default_theme_path = Path(__file__).parent / "theme.css"
        return default_theme_path

    @classmethod
        # Injects a <link> tag into <head> to include theme.css
    def inject_theme_css(cls):
        return ui.head_content(
            ui.include_css(cls.get_theme_css())
        )

    @classmethod
        # Returns the base Bootswatch theme (flatly)
    def get_base_theme(cls):
        return shiny_theme

# Page: reusable layout wrapper for consistent structure and theme
class Page:
    @classmethod
        # Builds a full page layout with a browser tab title and themed content
    def build_view(cls, title: str, content: Any):
        return ui.page_fluid(
                        ui.tags.head(
                ui.tags.title(title)
            ),
                        content,
            theme=Theme.get_base_theme(),
        )
