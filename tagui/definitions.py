#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#from __future__ import unicode_literals

import sys, os, random
from time import sleep
import siqt
from siqt import QtCore
from siqt import QtWidgets
import siqt.matplotlib
from siqt.matplotlib import backend_qtagg
from siqt.matplotlib import NavigationToolbar

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

from siqt import __version__, __version_date__, __version_hash__, _resource_path
from siqt.dep_resolv import sync_gui, dependency_graph, calculate_dependencies
from siqt.definitions import (add_actions, create_action,
                    menu_generator, set_dep_flag_recursive, SiqtElement)



def gpr_show_figure(self):
    def f(status=True):
        self.ax.set_visible(status)
        self.cbar_ax.set_visible(status)
    return f



HSLIDER_STEP = 1



class GprMainWindowBase(QtWidgets.QMainWindow):

    # some generic methods defined in gprcore
    add_actions = add_actions
    menu_generator = menu_generator
    create_action = create_action
    set_dep_flag_recursive = set_dep_flag_recursive

    # dependency flags, show if the corresponding data is ready for use
    dep_flags = { key: False for key in ['original']}
    dep_flags[False] = False
    dep_graph = {'original': []}
    menu = {}
    tabs = {}
    controls = {}


    def on_about(self):
        msg = u""" tagui


Version: {version}
Version hash: {version_hash}
Release date: {version_date}

© 2016 tagui
        """.format(version=__version__, version_hash=__version_hash__,
                   version_date=__version_date__)
        QtWidgets.QMessageBox.about(self, "About tagui", msg.strip())


    def create_plot_area(self):
        """ 
        Create the plot area
        """
        # Create the mpl Figure and FigCanvas objects. 
        # 5x4 inches, 100 dots-per-inch
        #
        self.fig_dpi = 100
        self.fig_basesize = 9.0
        self.fig_ratio = 3
        #fig_kw = {'figsize': (self.fig_basesize*self.fig_ratio, self.fig_basesize), 'dpi':  self.fig_dpi}
        #gridspec_kw = {""


        self.fig = Figure((self.fig_basesize*self.fig_ratio, self.fig_basesize),
                            dpi=self.fig_dpi)

        self.canvas = backend_qtagg.FigureCanvasQTAgg(self.fig)
        self.canvas.setParent(self.main_frame)


        self.ax = plt.subplot2grid((1,1),(0, 0))
        cbar_frac = 30
        gridspec = plt.GridSpec(1, cbar_frac)
        subplotspec = gridspec.new_subplotspec((0,0), 1, cbar_frac-1)

        self.ax = self.fig.add_subplot(subplotspec)

        subplotspec = gridspec.new_subplotspec((0,cbar_frac-1), 1, 1)
        self.cbar_ax = self.fig.add_subplot(subplotspec)


        # Bind the 'pick' event for clicking on one of the bars
        #
        #self.canvas.mpl_connect('pick_event', self.on_pick)

        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        self.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
        self.canvas.setFocus()



        self.controls['figure'] = {'show': gpr_show_figure(self), 'depends': ['original']}


    def create_tab_main(self):
        """
        Create the convolution tab
        """

        self.tabs['Main'] = {}
        ctab = self.tabs['Main']

        tab1 = QtWidgets.QWidget()
        tab1.setMinimumWidth(300)
        tab1_layout = QtWidgets.QGridLayout()
        # Defining components of the tab1
        # First row of parameters

        ctab['analyse_btn'] = SiqtElement(QtWidgets.QPushButton('Push button'),
                tab1_layout, (0, 2*2))


        # Second row of parameters
        #self.connect(update_plt_button, QtCore.SIGNAL('clicked()'), self.on_draw)
        ctab['update_plt_btn'] = SiqtElement(QtWidgets.QPushButton("&Update plot"),
                tab1_layout, (2, 2*3))

        ctab['threshold_checkbox_label'] = el =  SiqtElement('Threshold:',
                tab1_layout, (1, 0))
        el.setAlignment(QtCore.Qt.AlignRight)


        self.tab_widget.addTab(tab1, "Main")
        ctab['base'] = {'depends': ['original'], 'qtobj': tab1}


    def create_main_frame(self):
        self.main_frame = QtWidgets.QWidget()

        self.tab_widget = QtWidgets.QTabWidget()

        self.create_plot_area()
        self.create_tab_main()


        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.canvas)

        hslider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        hslider.setRange(0, 100)
        hslider.setValue(0)
        hslider.setTracking(True)
        #hslider.setVisible(False)
        hslider.setTickPosition(QtWidgets.QSlider.TicksBothSides)

        self.controls['hslider'] = SiqtElement(hslider, depends=['original'],
                                 show=hslider.setVisible)

        hslider.valueChanged.connect(self.on_zoom)


        #vbox.addWidget(hslider)
        vbox.addWidget(self.mpl_toolbar)
        #vbox.addLayout(hbox)


        #print(self.mpl_toolbar.geometry())
        #print(self.canvas.geometry())

        logo = QtWidgets.QLabel(self.main_frame)
        filepath = _resource_path(os.path.join('gprcore', 'data', 'groundradar-logo.png'))
        logo_exist = os.path.exists(filepath)

        if logo_exist:
            img =  QtWidgets.QPixmap(filepath)
            logo.setPixmap(img)
            vbox.addSpacing(-25)

        #logo.setScaledContents(True)
        #logo.setFixedWidth(190/2)
        #logo.setFixedHeight(115/2)
        logo.setAlignment(QtCore.Qt.AlignRight)
        logo.raise_()
        vbox.addWidget(logo)
        #if logo_exist:
        #    vbox.addSpacing(-27)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.tab_widget)
        hbox.addLayout(vbox)



        self.main_frame.setLayout(hbox)
        self.setCentralWidget(self.main_frame)

        calculate_dependencies(self, initialize=True)


    def create_status_bar(self):
        self.status_text = QtWidgets.QLabel("Convolution options")
        self.statusBar().addWidget(self.status_text, 1)


    def on_view_handler(self, view_mode):
        if view_mode not in self.menu['view'].elmts:
            raise ValueError('Wrong value for the view_mode argument!')
        def func():
            self.view_mode = view_mode
            self.on_draw()
            return

        return func




    def create_menu(self):

        file_menu_elements = {
            'open_datafile' : {'text': "&Open..", 'shortcut': "Ctrl+O",
                           'tip': "Open file", 'depends': [] },
            #'export_data': {'text': '&Export trace data..',
            #            'tip':  "Export trace data", 'depends': ['original'] },
            'close': {'text': '&Quit', 'shortcut': 'Ctrl+Q',
                'tip':  "Close the application", 'slot': self.close, 'depends': [] },

                }
        file_menu_order = ['open_datafile',
                                None, 'close']

        self.menu_generator('file', 'File', file_menu_elements, file_menu_order)



        debug_menu_elements = {
            'debug_information' : {'text': '&Debug information', 'depends': []}}

        debug_menu_order = ['debug_information']
        self.menu_generator('debug', 'Debug', debug_menu_elements, debug_menu_order)


        # Help menu
        about_menu_elements = {
            'about': {'text': "&About this program", 'shortcut': 'F1', 'depends': [] },
                    }
        about_menu_order = ['about']
        self.menu_generator('about', 'About', about_menu_elements, about_menu_order)




    def closeEvent(self, event):
        for key in list(self.widgets):
            if self.widgets[key] is not None:
                self.widgets[key].close()
        super(GprMainWindowBase, self).closeEvent(event)

