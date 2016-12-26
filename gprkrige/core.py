#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#from __future__ import unicode_literals

import sys, os, random
from time import sleep

import SiQt
from qtpy import QtCore
from qtpy import QtWidgets
from SiQt.siqt.dep_resolv import sync_gui, calculate_dependencies
from SiQt.siqt.widgets import (DebugInfoWidget,)
#import SiQt.siqt.matplotlib
import matplotlib

matplotlib.rcParams['backend.qt4'] = 'PyQt4'
matplotlib.rcParams['axes.formatter.limits'] = -6,6  # use scientific notation if log10
                # of the axis range is smaller than the first or larger than the second


from matplotlib.figure import Figure
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

from .definitions import GprMainWindowBase,  gpr_show_figure
import numpy as np




HSLIDER_STEP = 1




#def busy_cursor():
#    QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
#
#def restore_cursor():
#    QtGui.QApplication.restoreOverrideCursor()

BASE_WINDOW_TITLE = 'GUI tool'


class GprMainWindow(GprMainWindowBase):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setWindowTitle(BASE_WINDOW_TITLE)

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
        self.gpr = None
        self.dril_holes = None

        #default_pars = { 'spatial_filter': dict(Nx=7, Nt=14),}
        #for key, vals in default_pars.items():
        #    for pkey, pvals in  vals.items():
        #        self.tabs[key][pkey+'_control']['qtobj'].setText(str(pvals))
        #    #self.textbox.setText('1 2 3 4')

        self.widgets = {}
        for key in ['debug']:
            self.widgets[key] = None

        self._scroll_cid = None



    def wheel_event_zoom(self, event):
        """ Zoom on the cursor """
        base_scale = 1.1
        xlim_cur = self.ax.get_xlim()
        ylim_cur = self.ax.get_ylim()
        xrange_cur = (xlim_cur[1] - xlim_cur[0])
        yrange_cur = (ylim_cur[1] - ylim_cur[0])
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        xfrac = (xlim_cur[1] - xdata)/xrange_cur
        yfrac = (ylim_cur[1] - ydata)/yrange_cur

        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print(event.button)
        # set new limits
        
        xrange_new = xrange_cur*scale_factor
        yrange_new = yrange_cur*scale_factor
        
        
        self.ax.set_xlim([xdata - (1-xfrac)*xrange_new,
                     xdata +  xfrac*xrange_new])
        self.ax.set_ylim([ydata - (1-yfrac)*yrange_new,
                     ydata +  yfrac*yrange_new])
        self.canvas.draw()


    @sync_gui(update=['original'], view_mode='original')
    def on_open_datafile(self, state):
        file_choices = "Reflexw (*.*R);;All Files (*)"

        path = QtWidgets.QFileDialog.getOpenFileName(self, 
                        'Save file', '', file_choices,
                        None, QtWidgets.QFileDialog.DontUseNativeDialog
                        )
        path = str(path)
        if not path:
            return

    def on_draw(self):
        """ Redraws the figure
        """
        #mstr = str(self.textbox.text())
        #self.data = [int(el) for el in  mstr.split()]
        if not hasattr(self, 'gpr') or self.gpr is None:
           return 



        Nt, Nx =  self.gpr.data.shape
        Nx_viz = int(self.fig_ratio*Nt)
        

        self.fig.suptitle('My title')

        d = self.gis.data


        ax = self.ax

        #t = self.gpr.t_vect
        #x = self.gpr.x_vect


        # clear the axes and redraw the plot anew
        ax.axes.set_frame_on(False)
        ax.clear()
        gpr_show_figure(self)(True)

        # this is not working for some reason!
        #ax.set_axis_bgcolor('white') 
        
        #self._scroll_cid = self.fig.canvas.mpl_connect('scroll_event', wheel_event_backend)

        #self.ax.plot(d[:,0], d[:,1], 'k')
        self.ax.set_aspect('equal')
        # self.cbar = plt.colorbar(im, cax=self.cbar_ax)



        ax.set_xlabel('Easting position [m]')
        ax.set_ylabel('Northing position [m]')


        #self.axes.grid(self.grid_cb.isChecked())

        self.fig.tight_layout()

        self.canvas.flush_events()
        self.canvas.draw()


    def update_flag_checkbox(self, flag, tab_key, obj_key):
        ctab = self.tabs[tab_key]
        value = ctab[obj_key].value
        self.set_dep_flag_recursive(flag, value)
        calculate_dependencies(self, verbose=False)


    def on_debug_information(self):
        if self.widgets['debug'] is not None:
            self.widgets['debug'].close()
        self.widgets['debug'] = DebugInfoWidget(self)
        self.widgets['debug'].show()

