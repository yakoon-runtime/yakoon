from kivy.uix.scrollview import ScrollView
from kivy.properties import NumericProperty


class TabsBar(ScrollView):

    wheel_step = NumericProperty(0.08)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == "scrollup":
                self.scroll_x = min(1.0, self.scroll_x + self.wheel_step)
                return True
            if touch.button == "scrolldown":
                self.scroll_x = max(0.0, self.scroll_x - self.wheel_step)
                return True
        return super().on_touch_down(touch)


from kivy.factory import Factory
Factory.register("TabsBar", cls=TabsBar)
