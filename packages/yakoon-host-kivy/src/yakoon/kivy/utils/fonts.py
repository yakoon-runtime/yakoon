from pathlib import Path
from kivy.core.text import LabelBase

BASE = Path(__file__).resolve().parents[1]
FONTS = BASE / "assets" / "fonts"


LabelBase.register(
    name="RobotoMono",
    fn_regular=str(FONTS / "RobotoMono-Regular.ttf"),
    fn_bold=str(FONTS / "RobotoMono-Bold.ttf"),
)
