import threading


class DictObject(object):

    def __init__(self, *args, **kwargs):
        self.from_dict(**kwargs)

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if hasattr(self, key) and not key.startswith('_'):
                result[key] = value
        return result

    def from_dict(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise Exception("%s: missing attribute '%s'." % (
                    self.__class__.__name__, key))



class DefaultObject(DictObject):
    ID: int = 0
    home: int = 0
    name: str = ''
    desc: str = ''
    location: int = 0
    type_str: str = ''

    def __init__(self, *args, **kwargs):
        self.ID = 0
        self.name = ''
        self.home = 0
        self.location = 0
        self.type_str = 'object'
        self.desc = ''
        super().__init__(*args, **kwargs)



class DefaultRoom(DefaultObject):
    """
    """

    zone: str = ''
    tunnels = []
    objects = []

    def __init__(self, *args, **kwargs):
        """
        Constructs a new room.
        """
        self.zone = ''
        self.tunnels = []
        self.objects = []
        kwargs["type_str"] = 'room'
        super().__init__(*args, **kwargs)


class DefaultTunnel(DictObject):
    """
    """

    ID: int
    type_str: str = ''
    room_id: int
    name: str = ''
    state: str = ''
    dir = str = ''

    def __init__(self, *args, **kwargs):
        """
        Constructs a new tunnel.
        """
        self.ID = 0
        self.room_id = 0
        self.name = ''
        self.state = ''
        self.dir = ''
        kwargs["type_str"] = 'tunnel'
        super().__init__(*args, **kwargs)


class DefaultWorld(DictObject):
    type_str: str
    start_location: int

    def __init__(self, *args, **kwargs):

        self.type_str = ''

        kwargs["type_str"] = 'world'
        super().__init__(*args, **kwargs)

