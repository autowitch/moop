import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


class MatPlotLib(object):
    """docstring for MatPlotLib"""

    def __init__(self):
        super(MatPlotLib, self).__init__()
        mpl.rcParams['legend.fontsize'] = 10
        self.fig = plt.figure()
        self.ax = fig.gca(projection='3d')

        self.point_list = {}
        self.collisions = []
        self.start_points = {}
        self.end_points = {}
        self.dimensions = 4

    def set_dimensions(self, dimensions):
        self.dimensions = dimensions

    def add_point(particle_name, point):
        pass

    def add_collision(point):
        pass

    def add_start_point(particle_name, point):
        pass

    def add_end_point(particle_name, point):
        pass

    def show(self):
        pass

