python-qt-gpib-SR830
====================

This is a simple interface that uses python-qt, and python-gpib to log values read from an SR830 lock-in amplifier, and plots them using embedded pyqtgraph widgets

The interface was designed using QT Designer, and the file is saved as dashboard.ui .

Dependencies include the Pyside toolkit, Pyqtgraph, and python-gpib(Downloaded and built from sourceforge)
After all dependencies and udev rules for Gpib are setup and configured
$python app.py
Launches the application

If you edit the interface using QT designer or similar, a script called run.sh will compile and execute it
$./run.sh
