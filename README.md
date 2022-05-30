# TextsFromComics_Prototype
A GUI-based prototype for semi-automatically extracting written texts from comic page images written in Python. Works only on Microsoft Windows with the necessary requirements listed below.

Please consider the following when using the prototype for your own projects:
I programmed this for my M.A. thesis in the Anglophone Modernities program at the University of Potsdam. At the time, I was much more a humanities student than a programmer. Meaning I was a newbie to programming as well as to Python. I think than will become clear when you see the source code. ;-)
Furthermore, I am not planning on updating the code, since I think this project deserves a completely fresh start.
If you still want to run this script, here are the base requirements that you will need for your Python environment:
In addition to the Python standard libraries sys, os, pathlib, glob, tempfile, math, and time you'll need the packages in the following list.

# Name		Version
matplotlib	3.4.3
numpy		1.21.2
opencv		4.5.3
pytesseract	0.3.8
python		3.9.7
pyunpack	0.2.2
scipy		1.7.1
wxPython	4.1.1

IMPORTANT NOTE #1: In order to use the Tesseract OCR functionality, you will also need to install Tesseract on your Windows computer and add the location of the Tesseract executable in the PATH variable of your environment variables. The last working version of Tesseract this script was tested with was v5.0.0-alpha.20200328.

IMPORTANT NOTE #2: Again, the prototype will only run reliably on Microsoft Windows. Last tested version was Windows 10 Pro Version 21H2.
