import os
from collections import OrderedDict
from textwrap import dedent

from qtpy import QtCore, QtWidgets, QtGui
from qtpy.QtWidgets import QPushButton
import matplotlib.backends.backend_qt5agg as backend_qtagg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from SiQt.dep_resolv import calculate_dependencies
from SiQt.definitions import SiQtMixin, SiqtItem

from ._version import __version__
# this needs to be copied locally to work
from SiQt.deployement import _resource_path


class NavigationToolbar(backend_qtagg.NavigationToolbar2QT):
    # only display the buttons we need
    toolitems = [t for t in backend_qtagg.NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]


def show_figure(self):
    def f(status=True):
        self.ax.set_visible(status)
    return f


class GUIMainWindowBase(QtWidgets.QMainWindow, SiQtMixin):

    # dependency flags, show if the corresponding data is ready for use
    dep_flags = {key: False for key in ['original']}
    dep_flags[False] = False
    dep_graph = {'original': []}
    menu = {}
    tabs = {}
    controls = {}

    def on_about(self):
        msg = dedent("""GUI Template

                     Version: {version}

                     © 2017 Symerio
                     """.format(version=__version__))
        QtWidgets.QMessageBox.about(self, "About", msg.strip())

    def create_plot_area(self):
        """ Create the plot area """
        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        #
        self.fig_dpi = 100
        self.fig_basesize = 9.0
        self.fig_ratio = 3

        self.fig = Figure((self.fig_basesize*self.fig_ratio,
                           self.fig_basesize),
                          dpi=self.fig_dpi)

        self.canvas = backend_qtagg.FigureCanvasQTAgg(self.fig)
        self.canvas.setParent(self.main_frame)

        self.ax = plt.subplot2grid((1, 1), (0, 0))
        gridspec = plt.GridSpec(1, 1)
        subplotspec = gridspec.new_subplotspec((0, 0), 1, 1)

        self.ax = self.fig.add_subplot(subplotspec)

        # Bind the 'pick' event for clicking on one of the bars
        # self.canvas.mpl_connect('pick_event', self.on_pick)

        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()

        self.controls['figure'] = {'show': show_figure(self),
                                   'depends': ['original']}

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

        ctab['plot_btn'] = SiqtItem(QPushButton('Plot'),
                                    (0, 0), layout=tab1_layout)
        ctab['plot_btn'].clicked.connect(self.on_draw)

        tab1.setLayout(tab1_layout)
        self.tab_widget.addTab(tab1, "Main")
        ctab['base'] = {'depends': [], 'qtobj': tab1}

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
        hslider.setTickPosition(QtWidgets.QSlider.TicksBothSides)

        vbox.addWidget(self.mpl_toolbar)

        logo = QtWidgets.QLabel(self.main_frame)
        filepath = _resource_path(os.path.join('gui', 'data',
                                               'logo.png'))
        logo_exist = os.path.exists(filepath)

        if logo_exist:
            img = QtGui.QPixmap(filepath)
            logo.setPixmap(img)

        logo.setAlignment(QtCore.Qt.AlignRight)
        logo.raise_()
        vbox.addWidget(logo)
        if logo_exist:
            vbox.addSpacing(-7)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.tab_widget)
        hbox.addLayout(vbox)

        self.main_frame.setLayout(hbox)
        self.setCentralWidget(self.main_frame)

        calculate_dependencies(self, initialize=True)

    def create_status_bar(self):
        self.status_text = QtWidgets.QLabel("Tooltip")
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

        file_menu = OrderedDict()
        file_menu['open_datafile'] = {'text': "&Open..", 'shortcut': "Ctrl+O",
                                      'tip': "Open file", 'depends': []}
        file_menu['break1'] = None

        file_menu['close'] = {'text': '&Quit', 'shortcut': 'Ctrl+Q',
                              'tip':  "Close the application",
                              'slot': self.close, 'depends': []}

        self.menu_generator('file', 'File', file_menu)

        debug_menu = OrderedDict()
        debug_menu['debug_information'] = {'text': '&Debug information',
                                           'depends': []}

        self.menu_generator('debug', 'Debug', debug_menu)

        # Help menu
        about_menu = OrderedDict()
        about_menu['about'] = {'text': "&About this program",
                               'shortcut': 'F1', 'depends': []}
        self.menu_generator('about', 'About', about_menu)

    def closeEvent(self, event):
        for key in list(self.widgets):
            if self.widgets[key] is not None:
                self.widgets[key].close()
        super(GUIMainWindowBase, self).closeEvent(event)
