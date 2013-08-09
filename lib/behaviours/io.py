
class Printer(object):

    def __init__(self, owning_particle):
        super(Printer, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        print str(another_particle.contents)

    def __str__(self):
        return 'Printer'

class Reader(object):
    """docstring for Reader"""
    def __init__(self, arg):
        super(Reader, self).__init__()
        self.arg = arg

class FileReader(object):
    """docstring for FileReader"""
    def __init__(self, arg):
        super(FileReader, self).__init__()
        self.arg = arg

class FileWriter(object):
    """docstring for FileWritter"""
    def __init__(self, arg):
        super(FileWritter, self).__init__()
        self.arg = arg

class SocketReader(object):
    """docstring for SocketReader"""
    def __init__(self, arg):
        super(SocketReader, self).__init__()
        self.arg = arg

class SocketWriter(object):
    """docstring for SocketWriter"""
    def __init__(self, arg):
        super(SocketWriter, self).__init__()
        self.arg = arg

