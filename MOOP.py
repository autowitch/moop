#!/usr/bin/env python

import sys
import argparse
import re
import inspect
import copy


# TODO: Move to visualizer
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.gca(projection='3d')
x_points = []
y_points = []
z_points = []


class ParseError(Exception):
    pass

class BadParticle(Exception):
    pass

class Particle(object):
    """docstring for Particle"""


    def __init__(self, universe, id):
        super(Particle, self).__init__()
        self.universe = universe
        self.debug_level = universe.debug_level
        self.id = id

        self.behaviour = None # A xParticle class
        self.contents = "" # raw contents of the object

        self.name = None
        self.start = None
        self.trajectory = None
        self.speed = 1
        self.path = 'linear'
        self.radius = 0.25
        self.current_location = None
        # Possible - size to trigger collision?


        self.target = None   # Used in orbit, follow, spiral
                        # can be 'closest', 'furthest' for follow
                        # Can also be a coordinate

        # Default modifiers after collision
        self.collision_speed_change = 0
        self.collision_trajectory_change = "none"
        self.collision_radius_change = "none"

        self.in_collision = {}

        self.move_history = []

    def debug(self, level, msg, level_override=0):
        if self.debug_level >= level or level_override >= level:
            print msg

    def signal_universe(self, message, *args, **kwargs):
        self.universe.signal(message, args, kwargs)

    def start_run(self):
        self.current_location = self.start
        # TODO - visualization
        save_point = copy.copy(self.current_location)
        self.move_history.append(save_point)

    def move(self):
        for i in range(0, len(self.current_location)):
            self.current_location[i] = float(self.current_location[i]) + \
                    (float(self.trajectory[i]) * float(self.speed))
        # TODO - visualization
#        save_point = copy.copy(self.current_location)
#        self.move_history.append(save_point)

    def collide(self, another_particle):
        collide = False
        if not another_particle in self.in_collision or \
           not self.in_collision[another_particle]:
            collide = True

        if collide:
            if another_particle in self.in_collision:
                self.debug(3, ">>>> %s" % self.in_collision[another_particle])
                pass
            self.in_collision[another_particle] = True
            self.debug(1, "COLLISION! %s [%s] and %s [%s] (%sx%s to %sx%s)" % \
                       (self.name, self.id, another_particle.name,
                        another_particle.id,
                        self.current_location, self.radius,
                        another_particle.current_location,
                        another_particle.radius))
            self.behaviour.collide(another_particle)
            another_particle.behaviour.collide(self)

        return collide

    def uncollide(self, another_particle):
        if another_particle in self.in_collision and \
           self.in_collision[another_particle]:
            if another_particle in self.in_collision:
                self.debug(3, "UNCOLLIDE: %s %s" % (self.name, another_particle.name))
                pass
            self.in_collision[another_particle] = False

    def __str__(self):
        details = "\n    Start:    : %s\n" % self.start
        details += "    Trajectory: %s\n" % self.trajectory
        details += "    Speed:      %s\n" % self.speed
        details += "    Path:       %s\n" % self.path
        details += "    Diameter:   %s\n" % self.radius
        if not self.name:
            return '%s particle [%s]: (unnamed)%s' % (self.behaviour, self.id, details)
        return '%s particle [%s]: %s%s' % (self.behaviour, self.id, self.name, details)

    def validate(self):
        if not self.name:
            self.name = "[Unknown Particle]"
        if not self.start:
            raise BadParticle('start property missing on %s' % self.name)
        if not self.trajectory:
            raise BadParticle('trajectory property missing on %s' % self.name)
        if self.path not in ['linear', 'orbit', 'follow', 'spiral', 'random']:
            raise BadParticle('Invalid path %s on %s' % (self.path, self.name))

class ValueBehaviour(object):

    def __init__(self, owning_particle):
        super(ValueBehaviour, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        pass

    def __str__(self):
        if self.owning_particle:
            return 'Container (%s)' % self.owning_particle.contents
        return "Container (unowned and contentless)"

class AddBehaviour(object):

    def __init__(self, owning_particle):
        super(AddBehaviour, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):

        self.owning_particle.contents += another_particle.contents

    def __str__(self):
        return "Adder"


class TerminateBehaviour(object):
    def __init__(self, owning_particle):
        super(TerminateBehaviour, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        self.owning_particle.signal_universe('terminate', 0)

    def __str__(self):
        return "Terminator"


class KillBehaviour(object):

    def __init__(self, owning_particle):
        super(TerminateBehaviour, self).__init__()
        self.owning_particle = owning_particle

    def collide(self, another_particle):
        self.owning_particle.signal_universe('kill', another_particle)

    def __str__(self):
        return "Killer"


class Universe(object):

    """docstring for Universe"""

    particles = []
    max_ticks = -1
    dimensions = 4
    min_trajectory = 0.25   # At least one trajectory element for each 
                            # particle must >= this value.  This keeps
                            # all particles in motion.  This can be
                            # overriden

    constraints = None      # Used to bound the universe.  Can be fun to create
                            # particles with random walks and let them bound
                            # around in a confined space for a while.
    constrait_behaviour = "bounce"  # what happens to a particle when it hits
                                    # a "wall" (constraint) of the univers
                                    # bounce, stick, reverse, random
    age = 0
    debug_level = 0
    min_speed = 0.1
    min_radius = 0.1
    end = False

    collision_history = []
    start_pos = []

    def __init__(self, harness):
        super(Universe, self).__init__()
        self.harness = harness

    def debug(self, level, msg, level_override=0):
        if self.debug_level >= level or level_override >= level:
            print msg

    def check_existance(self):
        for particle in self.particles:
            if particle.radius < self.min_radius:
                self.debug(1, "BLIP")
                self.kill_particle(particle)
            # else if speed < self.min_speed) # TODO

    def kill_particle(self, a_particle, *args, **kwargs):
        self.particles.remove(a_particle)

    def terminate(self, *args, **kwargs):
        self.end = True
#        sys.exit()

    def signal(self, message, *args, **kwargs):
        handler = {'terminate': self.terminate,
                   'kill':      self.kill_particle}

        handler[message](args, kwargs)

    def check_particle_collision(self, a, b):
        self.debug(3, "checking %s against %s" % (a.name, b.name))
        collide = True

        for x in range(0, len(a.current_location)):
            apos = a.current_location[x]
            bpos = b.current_location[x]
            if (apos - a.radius <= bpos <= apos + a.radius) or \
               (bpos - b.radius <= apos <= bpos + b.radius):
                pass
            else:
                collide = False
                break

        return collide

    def check_collision(self):
        for i in range(0, len(self.particles) - 1):
            for j in range(i + 1, len(self.particles)):
                if self.check_particle_collision(self.particles[i], self.particles[j]):
                    collided = self.particles[i].collide(self.particles[j])
                    if collided:
                        # TODO - visualization
                        save_point = copy.copy(self.particles[i].current_location)
                        self.collision_history.append(save_point)
                else:
                    self.particles[i].uncollide(self.particles[j])


    def start(self):
        for x in self.particles:
            x.start_run()
            self.start_pos.append(copy.copy(x.current_location))
        self.age = 0

    def move_all_particles(self):
        for x in self.particles:
            x.move()
            x.move_history.append(copy.copy(x.current_location)) # TODO - visualization - odd
            self.debug(2, "Moved %s to %s" % (x.name, x.current_location))

    def step(self):
        while self.age < self.max_ticks:
            self.move_all_particles()
            yield
            if self.max_ticks > 0:
                self.age += 1

    def run(self):
        self.start()
        for x in self.step():
            self.debug(2, "Age: %s" % self.age)
            self.check_collision()
            self.debug(2, "\n\n")
            if self.end:
                break


class Moop(object):

    input_file = None
    debug_level = 0


    def __init__(self):
        super(Moop, self).__init__()
        self.universe = Universe(self)

        self.commands = {'start':self.get_coords,
                         'trajectory':self.get_coords,
                         'radius':self.get_num_value,
                         'path':self.get_value,
                         'speed':self.get_num_value,
                         'debug':self.get_flag,
                         'debuglevel':self.get_int_value}

        self.types = {'container':ValueBehaviour,
                      'adder':AddBehaviour,
                      'terminator':TerminateBehaviour,
                      'killer':KillBehaviour}

    def parse_args(self):
        # args here
        # !! TODO just test code
        parser = argparse.ArgumentParser(description='Execute MOOP programs')
        parser.add_argument('input_file',
                            metavar='FILE',
                            type=argparse.FileType('r'),
                            default=None,
                            help='MOOP source file')
        parser.add_argument('-v', '--verbose', action='count',
                            help='debug level (repeat to increase detail)')

        args = parser.parse_args()
        self.input_file = args.input_file
        self.debug_level = args.verbose
        self.universe.debug_level = self.debug_level

    def debug(self, level, msg, level_override=0):
        if self.debug_level >= level or level_override >= level:
            print msg

    def get_value(self, value):
        return value

    def get_coords(self, value):
        size = self.universe.dimensions

        if ',' in value:
            coords = re.split(',\s*', value)
        else:
            coords = re.split('\s+', value)
        if len(coords) != size:
            raise ParseError("%s must contain exaclty %s elements" % \
                             (value, size))
        return coords

    def get_num_value(self, value):
        return float(value)

    def get_contents(self, value):
        if not value:
            value = ""
        if value.startswith('"') and value.endswith('"'):
            value = value.strip('"')
        elif value.startswith("'") and value.endswith("'"):
            value = value.strip("'")
        elif value.startswith("`") and value.endswith("`"):
            print "CALL EXTERNAl"
        try:
            value = int(value)
            value = float(value)
        except ValueError:
            pass
        if value.lower() == 'false':
            value = False
        elif value.lower() == 'true':
            value = True

        return value

    def get_int_value(self, value):
        return int(value)

    def get_flag(self, value):
        return True

    def parse_command(self, current_particle, line):

        key = line
        value = None
        id = 0
        match = re.match('(?P<key>[^:= ]+)[ :=]+(?P<value>.*)', line)
        self.debug(4, "Command: %s, %s" % (key, value))
        if match:
            key = match.group('key').strip()
            value = match.group('value').strip()
        key = re.sub('[_-]', '', key).lower()

        if key == 'dimension' or key == 'dimensions':
            if self.universe.particles:
                raise ParseError("dimensions can only be specified before describing particles")

            self.debug(1, "Setting dimension to %s" % value)
            self.universe.dimension = int(value)
            return

        elif key == 'maxticks':
            self.debug(1, "Setting max-ticks to %s" % value)
            self.universe.max_ticks = float(value)
            return
        elif key == 'useparticles':
            self.debug(1, 'Loading additional particles from: %s' % value)
            new_lib = __import__('lib.behaviours.%s' % value)
            new_mod = sys.modules['lib.behaviours.%s' % value]
            members = inspect.getmembers(new_mod)
            for obj_name, obj_value in members:
                if not obj_name.startswith('_'):
#                    self.types[obj_name] = obj_value
                    self.types[obj_name.lower()] = obj_value
                    self.debug(1, 'Adding particle: %s %s' % (obj_name, obj_value))

            return

        elif key == "type":
            key = value
            value = None

        if not current_particle:
            print "Attempted to set property %s on non-existant particle" % \
                    line >> sys.stderr
            print "A default (unamed) particle will be created" >> sys.stderr
            current_particle = Particle(self.universe, id)
            id += 1


        if key in self.types:
            self.debug(1, "Setting particle to %s" % \
                       self.types[key].__class__.__name__)
            current_particle.behaviour = self.types[key](current_particle)
            current_particle.contents = self.get_contents(value)
            return

        if hasattr(current_particle, key):
            if key in self.commands:
                value = self.commands[key](value)
            self.debug(2, "    Setting particle property %s to %r" % (key ,value))
            setattr(current_particle, key, value)
        else:
            raise ParseError("Attempting to set unknown particle property: %s" % key)

    def parse_line(self, current_particle, line):
        # match = re.match('particle:[ ]*?P<name>.*', line)
        match = re.match('particle:\w*(?P<name>.*)', line)
        if match:
            if current_particle:
                self.universe.particles.append(current_particle)
            current_particle = Particle(self.universe, len(self.universe.particles) + 1)
            current_particle.name = match.group('name').strip()

        else:
            self.parse_command(current_particle, line)
        return current_particle

    def load_simulation(self):

        current_particle = None
        try:
            for line in self.input_file:
                line = line.strip()
                if re.match('^$', line):
                    continue
                elif re.match('^#', line):
                    continue
                current_particle = self.parse_line(current_particle, line)

            if current_particle:
                self.universe.particles.append(current_particle)
        except ParseError, e:
            print >> sys.stderr, e
            return False

        for x in self.universe.particles:
            try:
                x.validate()
                self.debug(1, x)
            except BadParticle, e:
                print >> sys.stderr, e
                return False

        return True

    def run(self):
        self.universe.run()


def main():
    """docstring for main"""
    m = Moop()
    m.parse_args()
    if not m.load_simulation():
        return
    m.run()

    # TODO: Move to visualizer
    for x in m.universe.particles:
        x_points = []
        y_points = []
        z_points = []
        for y in x.move_history:
            x_points.append(float(y[0])) # TODO - string values are getting here
            y_points.append(float(y[1]))
            z_points.append(float(y[2]))
        label = "%s (%s)" % (x.name, x.id)
        ax.plot(x_points, y_points, z_points, label=label)
    x_points = []
    y_points = []
    z_points = []
    for x in m.universe.collision_history:
        x_points.append(float(x[0]))
        y_points.append(float(x[1]))
        z_points.append(float(y[2]))
    ax.scatter(x_points, y_points, z_points, c='r', marker='o', label='collision')

    x_points = []
    y_points = []
    z_points = []
    for x in m.universe.start_pos:
        x_points.append(float(x[0]))
        y_points.append(float(x[1]))
        z_points.append(float(y[2]))
    ax.scatter(x_points, y_points, z_points, c='g', marker='o', label='start')
    ax.legend()
    plt.show()

if __name__ == '__main__':
    main()
