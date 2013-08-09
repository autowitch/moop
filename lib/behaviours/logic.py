class And(object):

    """docstring for And"""

    def __init__(self, owning_particle):
        super(And, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):

        if self.owning_particle.contents and another_particle.contents:
            another_particle.contents = True
        else:
            another_particle.contents = False

    def __str__(self):
        return "And"


class Or(object):

    """docstring for Or"""

    def __init__(self, owning_particle):
        super(Or, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):

        if self.owning_particle.contents or another_particle.contents:
            another_particle.contents = True
        else:
            another_particle.contents = False

    def __str__(self):
        return "Or"


class Not(object):

    """docstring for Not"""

    def __init__(self, owning_particle):
        super(Not, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):

        if another_particle.contents:
            another_particle.contents = False
        else:
            another_particle.contents = True

    def __str__(self):
        return "Not"


class Xor(object):

    """docstring for Xor"""

    def __init__(self, owning_particle):
        super(Xor, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):

        if bool(self.owning_particle.contents) != bool(another_particle.contents):
            another_particle.contents = True
        else:
            another_particle.contents = False

    def __str__(self):
        return "Xor"


class Nor(object):

    """docstring for Nor"""

    def __init__(self, owning_particle):
        super(Nor, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):

        if not self.owning_particle.contents or another_particle.contents:
            another_particle.contents = True
        else:
            another_particle.contents = False

    def __str__(self):
        return "Nor"


class Nand(object):

    """docstring for Nand"""

    def __init__(self, owning_particle):
        super(Nand, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):

        if not self.owning_particle.contents and another_particle.contents:
            another_particle.contents = True
        else:
            another_particle.contents = False

    def __str__(self):
        return "Nand"
