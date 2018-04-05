# A simple (Py)Qt GUI template

A simple template to start a PyQt5/PySide2 based GUI project. It requires Python 3.5+.

By default this uses PySide2 and matplotlib 2.1rc1

## Installation

To install depedencies run,

```
pip install PyQt5 QtPy matplotlib
```

or alternatively using a conda virtualenv,
```
conda create -n qt-template matplotlib pyqt qtpy python=3.6
conda activate qt-template
pip install SiQt
```

finally install this package,
```
pip install git+https://github.com/symerio/Python-Qt-template.git
```

## Starting the GUI

```
python scripts/start_gui.py
```

![GUI example](https://user-images.githubusercontent.com/630936/38364391-16f972ba-38e1-11e8-9518-5170ba1efb50.png)
