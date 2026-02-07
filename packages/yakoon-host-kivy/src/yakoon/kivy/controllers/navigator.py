
class Navigator:
    def __init__(self, app_root):
        self.app_root = app_root

    def go(self, name: str):
        sm = self.app_root.ids.get("sm")
        if sm:
            sm.current = name
