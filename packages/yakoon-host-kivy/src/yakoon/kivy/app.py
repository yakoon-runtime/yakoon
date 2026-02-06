# yakoon/kivy/app.py
from pathlib import Path
from kivy.app import App

from yakoon.kivy.utils.loader import load_layouts
from yakoon.kivy.pages.app_root import AppRootPage

# wichtig: Widgets registrieren, bevor KV geladen wird (Factory.register etc.)
from yakoon.kivy import pages, widgets  # noqa: F401
from yakoon.kivy.utils import fonts     # noqa: F401
    
class YakoonKivyApp(App):

    def build(self):
        package_root = Path(__file__).resolve().parent  # .../yakoon/kivy
        load_layouts(package_root)
        return AppRootPage()


if __name__ == "__main__":
    YakoonKivyApp().run()
