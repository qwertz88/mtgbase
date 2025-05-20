from shiny import App
from ui import app_ui           # 💬 The layout of your app (login screen, register screen, etc.)
from logic import server        # 💬 The logic handling user actions like login, logout, etc.
import pathlib                  # ✅ Needed to resolve relative icon folder path


# ✅ Define the static path to your icons folder
icon_dir = pathlib.Path(__file__).parent / "icons"

# ✅ Mount /icons as static route (fix: route must start with "/")
app = App(app_ui, server, static_assets={"/icons": icon_dir})

# 💬 Allows you to run the app directly with `python app.py` (e.g. from PyCharm)
if __name__ == "__main__":
    from shiny._main import main
    import sys
    sys.argv = ["shiny", "run", "--reload", __file__]
    main()
