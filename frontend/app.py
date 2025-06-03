from shiny import App
from ui import app_ui         # 🧩 UI components: login/register screen, main app layout, etc.
from logic import server      # ⚙️ Server logic: handles user interaction, state changes, etc.
import pathlib                # 📁 For creating paths to directories/files reliably

# 📁 Path to the folder containing icons (relative to this file)
icon_dir = pathlib.Path(__file__).resolve().parent / "icons"

# 🚀 Create and configure the Shiny app with static route for icons
app = App(app_ui, server, static_assets={"/icons": icon_dir})

# 🐍 Run the app directly using `python app.py` (e.g., for development in PyCharm or CLI)
if __name__ == "__main__":
    from shiny._main import main
    import sys

    # 🎯 Simulate command-line arguments for shiny CLI runner
    sys.argv = ["shiny", "run", "--reload", __file__]
    main()
