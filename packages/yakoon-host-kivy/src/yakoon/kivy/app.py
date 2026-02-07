

from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from yakoon.kivy import pages           # noqa: F401
from yakoon.kivy import widgets         # noqa: F401
from yakoon.kivy.utils import fonts     # noqa: F401

from yakoon.kivy.bootstrap.compose import compose_kivy_app


class YakoonKivyApp(App):
    def build(self):
        return compose_kivy_app().root


if __name__ == "__main__":
    YakoonKivyApp().run()
