from bokeh.plotting import figure, curdoc, ColumnDataSource
from bokeh.models import ColorBar, LinearColorMapper
from bokeh.driving import repeat
from bokeh.layouts import row
import colorcet
import numpy as np
import itertools


class RPMDPlot2D:

    def __init__(self, data):

        self.raw_data = data

        self.cell = self.raw_data['cell']

        self.setup_plot()

        func = self.get_update_function()
        curdoc().add_periodic_callback(func, 50)

    def setup_plot(self):
        self.particle_movie = figure(toolbar_location=None)
        self.particle_movie.x_range.range_padding = 0
        self.particle_movie.y_range.range_padding = 0

        self.plot_potential()
        self.plot_particles()

        self.energy_plot = figure()
        self.plot_energy()

    def plot_potential(self):
        pot = self.raw_data['potential']

        colors = LinearColorMapper(low=np.min(pot), high=np.max(pot),
                                   palette=colorcet.bmy)
        bar = ColorBar(color_mapper=colors, location=(0, 0))
        self.particle_movie.add_layout(bar, 'right')

        self.particle_movie.image(image=[pot], x=[self.cell[0][0]],
                                  y=[self.cell[1][0]],
                                  dw=[self.cell[0][1]-self.cell[0][0]],
                                  dh=[self.cell[1][1]-self.cell[1][0]],
                                  color_mapper=colors)

    def plot_particles(self):

        self.source = ColumnDataSource(data=dict(x=[], y=[]))
        self.particle_movie.circle('x', 'y', size=10, fill_color='white',
                                   line_color='black', line_width=3,
                                   source=self.source)

    def plot_energy(self):
        colors = itertools.cycle(colorcet.glasbey)

        E_t = self.raw_data['E_t']
        E_kin_t = self.raw_data['E_pot_t']
        E_pot_t = self.raw_data['E_kin_t']
        energies = [E_t, E_kin_t, E_pot_t]
        nparticles = np.shape(E_t)[1]
        x = np.linspace(0, 1, len(E_t))
        for i in range(nparticles):
            for e, color in zip(energies, colors):
                mean = np.mean(e[:, i])
                self.energy_plot.line(x=x, y=(e[:, i]), color=color)

    def get_update_function(self):

        t = range(len(self.raw_data['rb_t']))

        @repeat(sequence=t)
        def update(i):
            self.update_plot(i)

        return update

    def update_plot(self, i):
        r_t = self.raw_data['rb_t']
        x = r_t[i, :, :, 0]
        y = r_t[i, :, :, 1]
        self.source.data = dict(x=x, y=y)

    def get_layout(self):
        return row(self.particle_movie, self.energy_plot)
