from cx_Freeze import setup, Executable
import os

#os.environ['TCL_LIBRARY'] = r'C:\Users\mball\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
#os.environ['TK_LIBRARY'] = r'C:\Users\mball\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

setup(name = 'Program List',
      version='0.1',
      description = 'Lists all installed programs on host computer',
      executables = [Executable("Distributer.py")])
