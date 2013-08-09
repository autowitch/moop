import copy

class Reverse(object):
    """
    Reverses the direction of the particle it hits
    """
    def __init__(self, owning_particle):
        super(ReverseClassName, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):

        for n in range(0, another_partricle.trajectory):
            another_particle.trajectory[n] = -1.0 * another_particle.trajectory[n]

    def __str__(self):
        return "Reverse"


class Interfere(object):
    """
    Interferes with direction of the particle it hits
    Computes angle of hitting particle and itself and uses that
    to set new direction
    """
    def __init__(self, arg):
        super(Interfere, self).__init__()
        self.arg = arg


class Mutate(object):
    """Mutates a particle"""
    def __init__(self, arg):
        super(Mutate, self).__init__()
        self.arg = arg

class Clone(object):
    """
    Clones a particle
    By default the cloned particle is emitted using the reverse of the
    trajectory.

    Can use an angle based on the cloned particle and the cloner.
    """
    def __init__(self, owning_particle):
        super(Clone, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        new_particle = copy.deepcopy(another_particle)
        for n in range(0, new_particle.trajectory):
            new_particle.trajectory[n] *= -1.0
        self.owning_particle.universe.particles.append(new_particle)

    def __str__(self):
        return "Clone"


class Dissovle(object):
    """
    Dissolves a particle
    """
    def __init__(self, owning_particle):
        super(Dissovle, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        self.owning_particle.signal_universe('kill', another_particle)

    def __str__(self):
        return "Dissolve"

class Slow(object):
    """docstring for Slow"""
    def __init__(self, owning_particle):
        super(Slow, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        if isinstance(self.owning_particle.contents, int) or \
           isinstance(self.owning_paritcle.contents, float):
            another_particle.speed -= self.owning_particle.contents

    def __str__(self):
        return "Slow"


class Fast(object):
    """docstring for Fast"""
    def __init__(self, owning_particle):
        super(Fast, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        if isinstance(self.owning_particle.contents, int) or \
           isinstance(self.owning_paritcle.contents, float):
            another_particle.speed += self.owning_particle.contents

    def __str__(self):
        return "Fast"


class Grow(object):
    """docstring for Grow"""
    def __init__(self, owning_particle):
        super(Grow, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        if isinstance(self.owning_particle.contents, int) or \
           isinstance(self.owning_paritcle.contents, float):
            another_particle.radius += self.owning_particle.contents

    def __str__(self):
        return "Grow"


class Shrink(object):
    """docstring for Shrink"""
    def __init__(self, owning_particle):
        super(Shrink, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        if isinstance(self.owning_particle.contents, int) or \
           isinstance(self.owning_paritcle.contents, float):
            another_particle.radius += self.owning_particle.contents

    def __str__(self):
        return "Shrink"


class Absorb(object):
    """
    A quirkly little particle.  It absorbs any particles that it
    runs into.  When colliding with a particle it executes all the
    behaviours of the particles in has absorbed in either order absorbed,
    reverse order or random.

    If a SwitchState particle is collided with, it will no longer absorb, but
    will still execute all saved behaviours on collision.
    """
    def __init__(self, owning_particle):
        super(Absorb, self).__init__()
        self.owning_particle = owning_particle
        self.collecting = True
        self.particles = []

    def collide(self, another_particle):
        if collecting:
            self.particles.append(another_particle)
            self.owning_particle.signal_universe('kill', another_particle)
        else:
            for x in self.particles:
                x.collide(another_particle)

    def switch_state(self):
        self.collecting = not self.collecting

    def __str__(self):
        return "Absorb"


class Sleep(object):
    """
    Puts a particle to sleep so it's behaviours do not fire
    when it collides.
    """
    def __init__(self, arg):
        super(Sleep, self).__init__()
        self.arg = arg

class Wake(object):
    """
    Wakes a sleeping particle up
    """
    def __init__(self, arg):
        super(Wake, self).__init__()
        self.arg = arg

class Rest(object):
    """
    Lets a particle sleep for a while
    """
    def __init__(self, arg):
        super(Rest, self).__init__()
        self.arg = arg


class SwitchState(object):

    """docstring for SwitchState"""

    def __init__(self, owning_particle):
        super(SwitchState, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        try:
            another_particle.behaviour.switch_state()
        except AttributeError:
            pass

    def __str__(self):
        return "SwitchState"


class Nuke(object):
    """
    Explodes on collision.
    Destroys all particles with X units.
    """
    def __init__(self, arg):
        super(Nuke, self).__init__()
        self.arg = arg

class Copy(object):
    """
    Remembers the first particle that it runs into.  Every time that
    it hits a particle after that, it will emit a copy of that first
    particle.

    If a SwitchState is hit, it will forget that particle, remember the
    next one and then start emitting.
    """
    def __init__(self, owning_particle):
        super(Copy, self).__init__()
        self.owning_particle = owning_particle
        self.copied_particle = None

    def collide(self, another_particle):
        if not copied_particle:
            self.copied_particle = another_particle
        else:
            new_particle = copy.deepcopy(self.copied_particle)
            new_particle.current_location = self.owning_particle.current_location
            self.owning_particle.universe.particles.append(new_particle)

    def __str__(self):
        return "Copy"
        self.arg = arg

class Capture(object):
    """
    Captures the first particle it hits. Only releases the particle when it
    collides with a Release particle.  The released particle exists using
    the same parameters it had at the time of capture - except for location.

    CHANGE: Releases with the SwitchState paritcle.  Then goes to capturing
    again.
    """
    def __init__(self, arg):
        super(Archive, self).__init__()
        self.owning_particle = owning_particle
        self.stolen_particle = None

    def collide(self, another_particle):
        if not stolen_particle:
            self.stolen_particle = another_particle
            self.owning_particle.signal_universe('kill', another_particle)

    def switch_state(self):
        if stolen_particle:
            self.stolen_particle.current_location = self.owning_particle.current_location
            self.owning_particle.universe.particles.append(self.stolen_particle)
            self.stolen_particle = None

    def __str__(self):
        return "Capture"

class Grab(object):
    """
    Similar to Capture.  This will grab a particle until it hits another
    particle. It then releases that one (with parameters (save location)
    preserved, and grabs the new one.
    """
    def __init__(self, owning_particle):
        super(Grab, self).__init__()
        self.owning_particle = owning_particle
        self.stolen_particle = None

    def collide(self, another_particle):
        if not stolen_particle:
            self.stolen_particle = another_particle
            self.owning_particle.signal_universe('kill', another_particle)
        else:
            self.stolen_particle.current_location = self.owning_particle.current_location
            self.owning_particle.universe.particles.append(self.stolen_particle)
            self.stolen_particle = None

    def __str__(self):
        return "Grab"


class SwapContents(object):
    """
    Swaps the contents of a particle with itself
    """
    def __init__(self, owning_particle):
        super(Swap, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        t = another_particle.contents
        another_particle.contents = self.owning_particle.contents
        self.owning_particle.contents = t

    def __str__(self):
        return "SwapContents"


class SwapTrajectory(object):
    """
    Swaps
    """
    def __init__(self, owning_particle):
        super(Swap, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        t = another_particle.trajectory
        another_particle.trajectory = self.owning_particle.trajectory
        self.owning_particle.trajectory = t

    def __str__(self):
        return "SwapTrajectory"


class Filter(object):
    """
    Only allows particles with a diameter less than x through.
    Others are reflected"""
    def __init__(self, arg):
        super(Filter, self).__init__()
        self.arg = arg

# other ideas
# binary orbit.  collided Starts a binary orbit with next particle it finds
# orbit - collided particle will orbit the next particle
# follow - collided particle will follow farthest particle
# fixed orbit - collided particle will start orbiting a fixed point
#    this can be a normal path as well.
# break orbit - will break the orbit of a orbiting particle
# Swap next

# MOOP pure only allows behaviours for changing speed, trajectory or size

class Backwards(object):

    """docstring for Backwards"""

    def __init__(self, owning_particle):
        super(Backwards, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):

        for x in self.owning_particle.universe.particles:
            for n in range(0, x.trajectory):
                if x == self and not self.owning_particle.contents:
                    continue
                x.trajectory[n] = -1.0 * x.trajectory[n]

    def __str__(self):
        return "Backwards"

