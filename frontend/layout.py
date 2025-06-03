from typing import Any
from shiny import ui
from shinyswatch.theme import flatly as shiny_theme
from pathlib import Path

# 🎨 Theme class handles base and custom CSS themes
class Theme:
    # Path to a custom theme file (can be set externally if needed)
    theme_file = None

    @classmethod
    def get_theme_css(cls):
        """
        📁 Returns the path to the custom theme.css file.
        Defaults to 'theme.css' in the same folder as this script.
        """
        return Path(__file__).resolve().parent / "theme.css"

    @classmethod
    def inject_theme_css(cls):
        """
        🧩 Injects a <link> tag in the HTML <head> to include the theme CSS.
        """
        return ui.head_content(
            ui.include_css(cls.get_theme_css())
        )

    @classmethod
    def get_base_theme(cls):
        """
        🌈 Returns the base Bootswatch theme ('flatly' from shinyswatch).
        """
        return shiny_theme


# 🧱 Page class builds structured, themed views
class Page:
    @classmethod
    def build_view(cls, title: str, content: Any):
        """
        🏗️ Returns a full Shiny page with:
        - Page title shown in browser tab
        - Optional CSS theme applied
        - Provided content injected
        """
        return ui.page_fluid(
            ui.tags.head(
                ui.tags.title(title),
                Theme.inject_theme_css()  # 💡 Include custom CSS
            ),
            content,
            theme=Theme.get_base_theme()
        )
