import types

# Es können weitere Template Klassen angegeben werden


# Status der Funktion kann über .status abgefragt werden.
# Es ist vorgesehen auf der ersten stelle die funktion anzugeben und an der zweiten der Dateipfad.
class WorkWithFile:
    def __init__(self, func=None, *args):
        self.path = args[0]
        self.status = True
        if func is not None:
            self.execute = types.MethodType(func, self)

    def execute(self):
        return self.data


def write(self):
    pass


def read(self):
    try:
        with open(self.path, "r", newline="", encoding="utf-16") as file:
            return list(map(lambda x: x, file))
    except FileNotFoundError:
        self.status = False
        return None
