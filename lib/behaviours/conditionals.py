
class Empty(object):
    """
    Changes the trajectory of a particle if the target particle
    is empty.

    Default is to reverse trajectory but other options are available.
    """
    def __init__(self, arg):
        super(Empty, self).__init__()
        self.arg = arg

