# TextsFromComics_Prototype
A GUI-based prototype for semi-automatic extraction of written texts from comic page images written in Python.<br/>
Works only on **Microsoft Windows** with the necessary Python environment requirements listed below.<br/><br/>
**Please consider the following when using the prototype for your own projects:<br/><br/>**
I programmed this for my M.A. thesis in the Anglophone Modernities program at the University of Potsdam. At the time, I was much more a humanities student than a programmer. Meaning I was a newbie to programming as well as to Python. I think than will become clear when you see the source code. ;-)<br/><br/>
Furthermore, I am not planning on updating the code. A completely fresh start is more realistic at this point.<br/><br/>
If you still want to run this script, here are the base requirements that you will need for your Python environment:<br/>
In addition to the **Python 3.9.7** and its standard libraries **sys, os, pathlib, glob, tempfile, math, and time** you'll need the packages in the following list.<br/><br/>
**Name&emsp;&emsp;&emsp;&emsp;Version<br/>**
matplotlib&emsp;&emsp;&emsp;3.4.3<br/>
numpy&emsp;&emsp;&emsp;&emsp;1.21.2<br/>
opencv&emsp;&emsp;&emsp;&emsp;4.5.3<br/>
patool&emsp;&emsp;&emsp;&emsp;1.1.2<br/>
pytesseract&emsp;&emsp;0.3.8<br/>
pyunpack&emsp;&emsp;&emsp;0.2.2<br/>
scipy&emsp;&emsp;&emsp;&emsp;&emsp;1.7.1<br/>
wxPython&emsp;&emsp;&emsp;4.1.1<br/>
# IMPORTANT NOTE No 1:<br/>
As of the release of this prototype, the wxPython module did not work with Python versions higher than 3.9.7. If you want to run it on newer versions of Python, you'll have to check whether or not compatible versions of wxPython are available. In turn, newer wxPython version might also change up things in such a way that the GUI of this prototype will no longer work correctly. Please, keep that in mind and if possible use only a Python environment with the package version specified in the list above.
# IMPORTANT NOTE No 2:<br/>
In order to use the Tesseract OCR functionality, you will also need to install Tesseract on your Windows system and add the location of the Tesseract executable in the PATH variable of your environment variables. The last working version of Tesseract this prototype was tested with was v5.0.0-alpha.20200328.
# IMPORTANT NOTE No 3:<br/>
Again, the prototype especially the GUI will only run reliably on Microsoft Windows. Last tested version was Windows 10 Pro Version 21H2.
