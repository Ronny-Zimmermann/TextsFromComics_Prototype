try:
    missingModule = ""

    missingModule = "sys"
    import sys
    missingModule = "os"
    import os
    missingModule = "pathlib"
    import pathlib    
    missingModule = "numpy"
    import numpy as np
    missingModule = "glob"
    import glob
    missingModule = "wx"
    import wx
    missingModule = "wx.lib.scrolledpanel"
    import wx.lib.scrolledpanel
    missingModule = "tmpfile"
    import tempfile
    missingModule = "pyunpack and patool (both via pip!!!)"
    from pyunpack import Archive

    missingModule = "cv2"
    import cv2

    missingModule = "matplotlib"
    from pylab import mean
    missingModule = "scipy.ndimage"
    from scipy.ndimage import measurements
    missingModule = "pytesseract (via pip)"
    import pytesseract

    missingModule = "math"
    import math

    missingModule = "time"
    import time
    
    missingModule = "pprint"
    from pprint import pprint as pp

except ModuleNotFoundError:
    print("ERROR: Module ", missingModule, " is not installed.")
    print("")
    sys.exit()

#======================
# class definitions
#====================================================================

#====================================================================
# This class handles the comic pages and speech bubble images as well as
# their corresponding OCR-texts
class DataHandler:

    #----------------------------------------------------------------------
    def __init__(self, comPageList, comPageIdx, speeBubList, speeBubIdx, dbPath, savDirName):
        # Constructor

        self.comPageList = comPageList
        self.speeBubList = speeBubList

        self.comPageIdx = comPageIdx
        self.speeBubIdx = speeBubIdx

        self.mainList = []

        self.savDirName = savDirName
        self.dbPath = dbPath
        
        # create an wx.image as placeholder for the comic page and speech bubble images
        self.imgDummy = wx.Image(1,1)

        # get the background color of the main panel
        [panR, panG, panB] = MainFrame.mainPanel.GetBackgroundColour()[:3]

        # set the color of the image placeholder to the background color of the panel
        self.imgDummy.Replace(0,0,0,panR,panG,panB)

    #====================================================================
    # get the current, next, or previous item from a list;
    # if either end of the list is reached, the item idx is set to the first
    # or last item of the list - i.o.w., it loops through the list
    # INPUT:   listXY - a list (type: list)
    #          currentItem - current item of listXY (type: ---),
    #          currNextOrPrev - determines which item index is returned (type: integer)
    #                           0 = current item,
    #                           1 = next item in the list,
    #                           2 = previous item in the list
    # OUTPUT:  itemNum - the index of the next item (Type: integer)
    def getNextItem(self, listXY, currentItem, currNextOrPrev):

        itemNum = 0
        
        if currNextOrPrev == 0:
            itemNum = listXY.index(currentItem)
            return itemNum
    
        elif currNextOrPrev == 1:

            if listXY.index(currentItem) + 1 <= len(listXY)-1:

                itemNum = listXY.index(currentItem) + 1
                return itemNum
        
            else:

                itemNum = 0
                return itemNum

        elif currNextOrPrev == 2:

            if listXY.index(currentItem) - 1 >= 0:
                itemNum = listXY.index(currentItem) - 1
                return itemNum

            else:
        	
                itemNum = len(listXY) - 1
                return itemNum

    #====================================================================
    # INPUT:   tmpComPageList - temporary list containing wx.images (type: list)
    #          preOrNext - determines which item is handeled (type: integer)
    #                      1 = next item in the list,
    #                      2 = previous item in the list
    #          updOrRpl - determines whether a singel comic page is deleted or
    #                     the whole list is replaced (type: integer)
    #                      0 = add Bubble
    #                      1 = replace list
    # OUTPUT:  None
    def comPageHandler(self, tmpComPageList, preOrNext, updOrRpl):

        updPanel = 0

        # a single page is removed from the comPageList and the mainList
        if updOrRpl == 0:

            self.comPageList.pop(self.comPageIdx)
            self.mainList.pop(self.comPageIdx)

            # if the list still has items after the deletion of latest bubble item,
            # the next bubble item will be displayed...
            if len(self.comPageList) > 0:

                # if this was the last speech bubble item in the list,
                # the bubble list idx has to be set to the next item
                # else there will be an "out of range"-error
                if self.comPageIdx == len(self.comPageList):
                    # getting the index of the next item in the list
                    self.comPageIdx = self.getNextItem(self.comPageList,\
                                                       self.comPageList[self.comPageIdx-1], 1)

            updPanel = 1

        # the (temporary) tmpComPageList is reset with new comic pages
        elif updOrRpl == 1:

            # reseting all data lists and indices
            self.mainListHandler(1)

            # if this function is called from the ImageCheck-class the tmpComPageList
            # probably has items that have to be written into the comPageList
            if len(tmpComPageList) > 0:

                # writing the images' wx.Images and their file names into the
                # temporary list and the main comic page list:
                # tmpComPageList[x][0] is the comic page image;
                # tmpComPageList[x][1] is the corresponding file name

                for i in range(len(tmpComPageList)):
                    self.comPageList.append(tmpComPageList[i])
                    self.mainList.append([tmpComPageList[i],[]])

            updPanel = 1

        if preOrNext == 1 or preOrNext == 2:

            # if the speech bubble list has any items in it, all data
            # of the currently shown page is saved;
            if len(self.speeBubList) > 0:
                # feed the data from the text box to the current speech bubble item
                self.speeBubList[self.speeBubIdx][2] = BubTextBox.speeBubTxtBox.GetValue()

                self.mainListHandler(0)

            else:
                # 9 is a dummy parameter that is not regarded by the function
                self.speeBubHandler([], 9, 1)

            if len(self.comPageList) > 0:
                self.comPageIdx = self.getNextItem(self.comPageList,\
                                                   self.comPageList[self.comPageIdx],\
                                                   preOrNext)

            MainFrame.mainPanel.lSubPan.btnFindBub.SetFocus()

            updPanel = 1

        if updPanel == 1 and len(self.comPageList) > 0:

            # putting the comic page image into the comic page panel
            updateImage(self.comPageList[self.comPageIdx][0], 0)

            # constructing the string for page count underneath the comic page
            txtNumImgs = "Page " + str(self.comPageIdx+1) + " of " + str(len(self.comPageList))

            # putting the string underneath the comic page
            ComicPageViewer.stTxtNumImg.SetLabel(txtNumImgs)
                
            updateImage(wx.Bitmap(self.imgDummy).ConvertToImage(), 1)
            SpeeBubTextEditor.stTxtNumBubs.SetLabel("")
            BubTextBox.speeBubTxtBox.SetValue("")

            self.speeBubHandler([], 9, 1)

        # all panels are reset to their initial state
        elif updPanel == 1 and len(self.comPageList) == 0:

            updateImage(wx.Bitmap(self.imgDummy).ConvertToImage(), 0)
            updateImage(wx.Bitmap(self.imgDummy).ConvertToImage(), 1)
            ComicPageViewer.stTxtNumImg.SetLabel("")
            SpeeBubTextEditor.stTxtNumBubs.SetLabel("")
            BubTextBox.speeBubTxtBox.SetValue("")

    #====================================================================
    # INPUT:   tmpSpeeBubList - temporary list containing wx.images (type: list)
    #          preOrNext - determines which item is handeled (type: integer)
    #                      0 = current item
    #                      1 = next item in the list,
    #                      2 = previous item in the list
    #          updOrRpl - (type: integer)
    #                      0 = detect text on the speech bubble images and
    #                          save them into the lists
    #                      1 = 
    #                      2 = add Bubble
    #                      3 = delete Bubble
    # OUTPUT:  None
    def speeBubHandler(self, tmpSpeeBubList, preOrNext, updOrRpl):

        updPanel = 0

        # the OCR-texts are put into the list
        if updOrRpl == 0:

            tmpSpeeBubImgsList = []

            for i in range(len(MainFrame.comDat.speeBubList)):
                tmpSpeeBubImgsList.append(MainFrame.comDat.speeBubList[i][0])

            tmpSpeeBubTxtList = ocrSpeeBub(tmpSpeeBubImgsList)

            for i in range(len(tmpSpeeBubTxtList)):
                MainFrame.comDat.speeBubList[i][2] = tmpSpeeBubTxtList[i]

            self.mainListHandler(0)
            
            updPanel = 1

        # the (temporary) speeBubList is reset with new speech bubbles and
        # and the corresponding item in the mainList as well
        elif updOrRpl == 1:

            self.speeBubList = []
            self.speeBubIdx = 0

            # if this function is called from the ImageCheck-class the tmpSpeeBubList
            # probably has items that have to be written into the speeBubList
            if len(tmpSpeeBubList) > 0:

                # writing the bubbles' data as tuple into the speech bubble and main list:
                # speeBubList[x][0] is the speech bubble image;
                # speeBubList[x][1] is file name of the corresponding comic page
                # speeBubList[x][2] is the speech bubble text
                # speeBubList[x][3] are the coordiantes of the text on the comic page image
                for i in range(len(tmpSpeeBubList)):
                    self.speeBubList.append([tmpSpeeBubList[i][0], self.comPageList[self.comPageIdx][1], "", tmpSpeeBubList[i][1]])
                    self.mainList[self.comPageIdx][1].append([tmpSpeeBubList[i][0], self.comPageList[self.comPageIdx][1], "", tmpSpeeBubList[i][1]])

            # if this function is called from the next or previous button in the
            # comic page panel, this query checks whether there is already data
            # for the corresponding page or not and fills the speeBubList with it
            elif isinstance(self.mainList[self.comPageIdx][1], list):
                for i in range(len(self.mainList[self.comPageIdx][1])):
                    self.speeBubList.append(self.mainList[self.comPageIdx][1][i])

            updPanel = 1

        # a bubble is added to the (temporary) speeBubList and the current item
        # in the mainList is updated
        elif updOrRpl == 2:

            # if the speeBubList already has an items in it...
            if len(self.speeBubList) > 0:
                # feed the data from the text box to the current speech bubble item
                self.speeBubList[self.speeBubIdx][2] = BubTextBox.speeBubTxtBox.GetValue()

            # adding a speech bubble item at the end of the list
            self.speeBubList.append([wx.Bitmap(tmpSpeeBubList[0]), self.comPageList[self.comPageIdx][1], "", tmpSpeeBubList[1]])

            # getting the index of the added speech bubble item in the list
            self.speeBubIdx = len(self.speeBubList)-1
            
            updPanel = 1

        # a bubble is deleted from the (temporary) speeBubList and the current item
        # in the mainList is updated
        elif updOrRpl == 3:

            self.speeBubList.pop(self.speeBubIdx)

            # if the list still has items after the deletion of latest bubble item,
            # the next bubble item will be displayed...
            if len(self.speeBubList) > 0:

                # if this was the last speech bubble item in the list,
                # the bubble list idx has to be set to the next item
                # else there will be an "out of range"-error
                if self.speeBubIdx == len(self.speeBubList):
                    # getting the index of the next item in the list
                    self.speeBubIdx = self.getNextItem(self.speeBubList,\
                                                       self.speeBubList[self.speeBubIdx-1], 1)

                updPanel = 1

            else:
                updPanel = 1

        if preOrNext == 0:

            updPanel = 1

        elif preOrNext == 1 or preOrNext == 2:

            # feed the data from the text box to the current speech bubble item...
            self.speeBubList[self.speeBubIdx][2] = BubTextBox.speeBubTxtBox.GetValue()

            self.speeBubIdx = self.getNextItem(self.speeBubList,\
                                               self.speeBubList[self.speeBubIdx], preOrNext)

            MainFrame.mainPanel.rSubPan.btnOCR.SetFocus()

            updPanel = 1

        if updPanel == 1 and len(self.speeBubList) > 0:

            # putting that speech bubble image into the speech bubble image panel
            # that is indiced by the speech bubble index (self.speeBubIdx)
            updateImage(self.speeBubList[self.speeBubIdx][0], 1)

            txtNumImgs = "Bubble " + str(self.speeBubIdx+1) + " of " + str(len(self.speeBubList))
            SpeeBubTextEditor.stTxtNumBubs.SetLabel(txtNumImgs)
            
            BubTextBox.speeBubTxtBox.SetValue(self.speeBubList[self.speeBubIdx][2])

        # all speech bubble panels are reset to their initial state
        elif updPanel == 1 and len(self.speeBubList) == 0:

            updateImage(wx.Bitmap(self.imgDummy).ConvertToImage(), 1)
            SpeeBubTextEditor.stTxtNumBubs.SetLabel("")
            BubTextBox.speeBubTxtBox.SetValue("")

    #====================================================================
    # INPUT:   updOrClr - determines whether the main list is updated
    #                     or cleared (type: integer)
    #                     0 = the main list is updated
    #                     1 = all lists are cleared
    #                     2 = the data in the main list is saved to the drive
    # OUTPUT:  None
    def mainListHandler(self, updOrClr):

        if updOrClr == 0:

            # get the data of the current comic page item
            coPaItem = self.comPageList[self.comPageIdx]

            # replace the data of that item with the new data
            self.mainList[self.comPageIdx] = [coPaItem, self.speeBubList]

        elif updOrClr == 1:

            self.comPageList = []
            self.speeBubList = []
            self.comPageIdx = 0
            self.speeBubIdx = 0
            self.mainList = []

        elif updOrClr == 2:
            
            # if the speeBubList already has items in it,...
            if len(self.speeBubList) > 0:
                # ...feed the data from the text box to the current speech bubble item and...
                self.speeBubList[self.speeBubIdx][2] = BubTextBox.speeBubTxtBox.GetValue()

            # ...call the save function
            self.saveData()

    #====================================================================
    # INPUT:   None
    # OUTPUT:  None
    def saveData(self):

        # if the database path has not been set, make the user do it now
        if not self.dbPath:
            MainFrame.onChoDbDirectory(None, None)

        # constructing the output path
        tcpDbPath = pathlib.Path.joinpath(pathlib.Path(self.dbPath), '_TCPdb')

        outTxtFileName = self.savDirName + ".txt"

        # the output directories are created if they do not exist
        if not os.path.exists(tcpDbPath):
            os.makedirs(tcpDbPath)

        currWorkDir = os.getcwd()
        os.chdir(tcpDbPath)

        outFile = open(outTxtFileName, mode="wt", encoding='utf-8')

        comText = ""

        # collecting the texts from the data list into a single variable
        for i in range(len(self.mainList)):
            if len(self.mainList[i][1]) > 0:
                for j in range(len(self.mainList[i][1])):
                    comText = comText + self.mainList[i][1][j][2] + "\n"

        # writing the collected texts into the specified file
        outFile.write(comText)

        outFile.close()

        os.chdir(currWorkDir)

        msg = "\n" + "The texts have been saved to:\n\n" + str(tcpDbPath) + "\\" + outTxtFileName
        print(msg)

#====================================================================
# This class opens a dialog that tells the user that the program is working
# on something.
# INPUT:    msg - contains the massege that is displayed (type: string)
# OUTPUT:   None
class LoadingMonolog(wx.Dialog):

    #----------------------------------------------------------------------
    def __init__(self, parent, msg):
        # Constructor
        wx.Panel.__init__(self, parent, wx.ID_ANY, style=wx.STAY_ON_TOP)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.infoText = wx.StaticText(self, wx.ID_ANY, msg, style=wx.ALIGN_CENTER)

        self.mainSizer.AddStretchSpacer()
        self.mainSizer.Add(self.infoText, 0, wx.CENTER)
        self.mainSizer.AddStretchSpacer()

        self.SetSizer(self.mainSizer)
        self.CentreOnScreen()
        self.Show()
        wx.GetApp().Yield()

    #----------------------------------------------------------------------
    def finished(self):

        self.Destroy()

#====================================================================
# the upper right panel where the speech bubble images are shown
class SpeechBubImgPan(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        # Constructor
        wx.Panel.__init__(self, parent)

        # create a main sizer which stretches all other sizers to the
        # size of the subpanel
        mainSizer = wx.BoxSizer()

        # create the static box with the panel description...
        speeBubStatBox = wx.StaticBox(self, wx.ID_ANY, "Text Cutout")
        # ...and asign a sizer to it
        speeBubStatBoxSizer = wx.StaticBoxSizer(speeBubStatBox, wx.VERTICAL)

        # create an "empty" image as placeholder;
        # it will be replaced by an comic page image later
        SpeechBubImgPan.speeBubImg = wx.Image(1,1)

        # get the background color of the panel
        [panR, panG, panB] = self.GetBackgroundColour()[:3]

        # set the color of the image placeholder to the background color of the panel
        SpeechBubImgPan.speeBubImg.Replace(0,0,0,panR,panG,panB)

        # convert the image placeholder to a static bitmap
        SpeechBubImgPan.speeBubImg = wx.StaticBitmap(self, wx.ID_ANY,\
                                                    wx.Bitmap(SpeechBubImgPan.speeBubImg))

        # add the image placeholder to the sizer of the
        # static box with the panel description; meaning, placing it within the static box
        speeBubStatBoxSizer.Add(SpeechBubImgPan.speeBubImg, wx.ID_ANY, wx.ALL|wx.CENTER)

        # add the static box with the image that is nested in it
        # to the main sizer
        mainSizer.Add(speeBubStatBoxSizer, wx.ID_ANY, wx.EXPAND|wx.ALL)
        
        # fit the main sizer to the subpanel
        self.SetSizer(mainSizer)

#====================================================================
# the lower right panel where the speech bubble text is shown and edited
class BubTextBox(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        # Constructor
        wx.Panel.__init__(self, parent)

        # create a main sizer which stretches all other sizers to the
        # size of the subpanel
        mainSizer = wx.BoxSizer()

        # create the static box with the panel description...
        speeBubStatBox = wx.StaticBox(self, wx.ID_ANY, "Extracted Text")
        # ...and asign a sizer to it
        speeBubStatBoxSizer = wx.StaticBoxSizer(speeBubStatBox, wx.VERTICAL)

        # create another sizer for the actual text box
        speeBubTxtBoxSizer = wx.BoxSizer(wx.VERTICAL)

        # create the text box
        BubTextBox.speeBubTxtBox = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        # add the text box to the text box sizer
        # IMPORTANT NOTE: every sizer needs its own ID in order to
        # stretch into/fill out the nesting sizer
        speeBubTxtBoxSizer.Add(BubTextBox.speeBubTxtBox, wx.ID_ANY, wx.EXPAND|wx.ALL)

        # add the text box sizer to the sizer of the static box
        speeBubStatBoxSizer.Add(speeBubTxtBoxSizer, wx.ID_ANY, wx.EXPAND|wx.ALL)

        # add the static box with the text box that is nested in it
        # to the main sizer
        mainSizer.Add(speeBubStatBoxSizer, wx.ID_ANY, wx.EXPAND|wx.ALL)
        
        # fit the main sizer to the subpanel
        self.SetSizer(mainSizer)

#====================================================================
# the right panel of the window, which shows the speech bubble images and
# their editable texts
class SpeeBubTextEditor(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        # Constructor
        wx.Panel.__init__(self, parent)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # the image viewing panel
        speeBubImg = SpeechBubImgPan(self)
        mainSizer.Add(speeBubImg, 1, wx.EXPAND|wx.ALL, 10)

        txtNumBubs = ""

        SpeeBubTextEditor.stTxtNumBubs = wx.StaticText(self, wx.ID_ANY, txtNumBubs)

        mainSizer.Add(SpeeBubTextEditor.stTxtNumBubs, 0, wx.CENTER, 10)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        # the ctrl-buttons        
        btnPrev = wx.Button(self, label="Previous Text Cutout")
        btnPrev.Bind(wx.EVT_BUTTON, self.onPrev)

        btnNext = wx.Button(self, label="Next Text Cutout")
        btnNext.Bind(wx.EVT_BUTTON, self.onNext)
        
        self.btnOCR = wx.Button(self, label="Apply &OCR to Text Cutouts")
        self.btnOCR.Bind(wx.EVT_BUTTON, self.onOCR)
        
        btnAdd = wx.Button(self, label="&Add Text Cutout")
        btnAdd.Bind(wx.EVT_BUTTON, self.onAdd)

        btnDis = wx.Button(self, label="&Discard Text Cutout")
        btnDis.Bind(wx.EVT_BUTTON, self.onDisBub)

        # positioning the buttons
        btnSizer.Add(btnPrev, wx.EXPAND|wx.ALL)
        btnSizer.Add(btnNext, wx.EXPAND|wx.ALL)
        btnSizer.Add(self.btnOCR, wx.EXPAND|wx.ALL)
        btnSizer.Add(btnAdd, wx.EXPAND|wx.ALL)
        btnSizer.Add(btnDis, wx.EXPAND|wx.ALL)

        mainSizer.Add(btnSizer, 0, wx.EXPAND|wx.ALL, 10)

        SpeeBubTextEditor.speeBubTxt = BubTextBox(self)
        mainSizer.Add(SpeeBubTextEditor.speeBubTxt, 1, wx.EXPAND|wx.ALL, 10)

        self.SetSizer(mainSizer)
        
    #----------------------------------------------------------------------
    def onNext(self, event):

        if hasattr(MainFrame, "comDat") and len(MainFrame.comDat.speeBubList) > 0:

            # 9 is a dummy parameter that is not regarded by the function
            MainFrame.comDat.speeBubHandler([], 1, 9)

    #----------------------------------------------------------------------
    def onPrev(self, event):
        
        if hasattr(MainFrame, "comDat") and len(MainFrame.comDat.speeBubList) > 0:

            # 9 is a dummy parameter that is not regarded by the function
            MainFrame.comDat.speeBubHandler([], 2, 9)

    #----------------------------------------------------------------------
    def onOCR(self, event):

        if hasattr(MainFrame, "comDat") and len(MainFrame.comDat.speeBubList) > 0:

            loadMlg = LoadingMonolog(None, "Trying to detect text in image(s). Please wait...")

            MainFrame.comDat.speeBubHandler([], 9, 0)

            loadMlg.finished()

    #----------------------------------------------------------------------
    def onAdd(self, event):

        # if a comic image is open...
        if hasattr(MainFrame, "comDat"):

            addSpeechBubble(MainFrame.comDat.comPageList[MainFrame.comDat.comPageIdx][0])

    #----------------------------------------------------------------------
    def onDisBub(self, event):
        
        if hasattr(MainFrame, "comDat") and len(MainFrame.comDat.speeBubList) > 0:

            MainFrame.comDat.speeBubHandler([], 9, 3)

#====================================================================
# the upper panel on the left side of the window that shows the image of the comic page
class ComicPagePanel(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        # Constructor
        wx.Panel.__init__(self, parent)

        # create a main sizer which stretches all other sizers to the
        # size of the subpanel
        mainSizer = wx.BoxSizer()

        # create the static box with the panel description...
        comPageStatBox = wx.StaticBox(self, wx.ID_ANY, "Comic Page")
        # ...and asign a sizer to it
        comPageStatBoxSizer = wx.StaticBoxSizer(comPageStatBox, wx.VERTICAL)

        # create an "empty" image as placeholder;
        # it will be replaced by an comic page image later
        ComicPagePanel.comPageImg = wx.Image(1,1)

        # get the background color of the panel
        [panR, panG, panB] = self.GetBackgroundColour()[:3]

        # set the color of the image placeholder to the background color of the panel
        ComicPagePanel.comPageImg.Replace(0,0,0,panR,panG,panB)
        
        # converting the image into a static bitmap
        ComicPagePanel.comPageImg = wx.StaticBitmap(self, wx.ID_ANY,\
                                                    wx.Bitmap(ComicPagePanel.comPageImg))

        # add the image/static bitmap to the sizer of the static box with the
        # panel description; meaning, placing it within the static box
        comPageStatBoxSizer.Add(ComicPagePanel.comPageImg, wx.ID_ANY, wx.CENTER)

        # add the static box with the image that is nested in it
        # to the main sizer
        mainSizer.Add(comPageStatBoxSizer, wx.ID_ANY, wx.EXPAND|wx.ALL)
        
        # fit the main sizer to the subpanel
        self.SetSizer(mainSizer)

#====================================================================
# the left panel of the window, which shows the image of the comic page
class ComicPageViewer(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        # Constructor
        wx.Panel.__init__(self, parent)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # the image viewing panel
        comPage = ComicPagePanel(self)
        mainSizer.Add(comPage, 1, wx.EXPAND|wx.ALL, 10)

        txtNumImgs = ""

        ComicPageViewer.stTxtNumImg = wx.StaticText(self, wx.ID_ANY, txtNumImgs)

        mainSizer.Add(ComicPageViewer.stTxtNumImg, 0, wx.CENTER, 10)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        # the ctrl-buttons
        btnPrev = wx.Button(self, label="Previous Page")
        btnPrev.Bind(wx.EVT_BUTTON, self.onPrev)
        
        btnNext = wx.Button(self, label="Next Page")
        btnNext.Bind(wx.EVT_BUTTON, self.onNext)
        
        self.btnFindBub = wx.Button(self, label="Find &Text On Page")
        self.btnFindBub.Bind(wx.EVT_BUTTON, self.onFindBub)

        btnDisPa = wx.Button(self, label="&Discard Page")
        btnDisPa.Bind(wx.EVT_BUTTON, self.onDisPage)

        self.btnSavDat = wx.Button(self, label="&Save Data")
        self.btnSavDat.Bind(wx.EVT_BUTTON, self.onSavDat)

        # positioning the buttons
        btnSizer.Add(btnPrev, wx.EXPAND|wx.ALL)
        btnSizer.Add(btnNext, wx.EXPAND|wx.ALL)
        btnSizer.Add(self.btnFindBub, wx.EXPAND|wx.ALL)
        btnSizer.Add(btnDisPa, wx.EXPAND|wx.ALL)
        btnSizer.Add(self.btnSavDat, wx.EXPAND|wx.ALL)

        mainSizer.Add(btnSizer, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizer(mainSizer)

    #----------------------------------------------------------------------
    def onNext(self, event):

        if hasattr(MainFrame, "comDat") and len(MainFrame.comDat.comPageList) > 1:

            # updating the panels with the available data of the next comic page
            # 9 is a dummy parameter that is not regarded by the function
            MainFrame.comDat.comPageHandler([],1,9)

    #----------------------------------------------------------------------
    def onPrev(self, event):

        if hasattr(MainFrame, "comDat") and len(MainFrame.comDat.comPageList) > 1:

            # updating the panels with the available data of the previous comic page
            # 9 is a dummy parameter that is not regarded by the function
            MainFrame.comDat.comPageHandler([], 2, 9)

    #----------------------------------------------------------------------
    def onFindBub(self, event):

        if hasattr(MainFrame, "comDat") and len(MainFrame.comDat.comPageList) > 0:

            loadMlg = LoadingMonolog(None, "Trying to detect text on image. Please wait...")
            tmpSpeeBubList = []

            if MainFrame.comDat.comPageList:

                tmpSpeeBubList = findTextOnComicPage(MainFrame.comDat.comPageList[MainFrame.comDat.comPageIdx][0])

            if tmpSpeeBubList:

                ImageCheck(tmpSpeeBubList, 1, 0, title='Text Cutout Check', parent=wx.GetTopLevelParent(self))

            loadMlg.finished()

    #----------------------------------------------------------------------
    def onDisPage(self, event):

        if hasattr(MainFrame, "comDat") and len(MainFrame.comDat.comPageList) > 0:

            # 9 is a dummy parameter that is not regarded by the function
            MainFrame.comDat.comPageHandler([], 9, 0)

    #----------------------------------------------------------------------
    def onSavDat(self, event):

        if hasattr(MainFrame, "comDat") and len(MainFrame.comDat.comPageList) > 0:

            # 2 is the save-mainList parameter of the mainListHandler
            MainFrame.comDat.mainListHandler(2)

#====================================================================
# the main panel which is split vertically in two seperate panels
class MainPanel(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        # Constructor
        wx.Panel.__init__(self, parent)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create a sub panel left and right
        self.lSubPan = ComicPageViewer(self)
        self.rSubPan = SpeeBubTextEditor(self)
        
        lSubPanSizer = wx.BoxSizer()
        lSubPanSizer.Add(self.lSubPan, wx.ID_ANY, wx.EXPAND|wx.ALL)
 
        rSubPanSizer = wx.BoxSizer()
        rSubPanSizer.Add(self.rSubPan, wx.ID_ANY, wx.EXPAND|wx.ALL)
 
        mainSizer.Add(lSubPanSizer, wx.ID_ANY, wx.EXPAND|wx.ALL)
        mainSizer.Add(rSubPanSizer, wx.ID_ANY, wx.EXPAND|wx.ALL)

        self.SetSizer(mainSizer)

#====================================================================
# the main frame of the program
class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title="Text from Comic Pages")

        self.createPanel()

        # positions the app on MY second monitor
        self.SetPosition((-2560,0))
        
        self.Maximize(True)
        
        self.Bind(wx.EVT_CHAR_HOOK, self.onKey)

    #----------------------------------------------------------  
    def createPanel(self):

        self.CreateStatusBar() # wxPython built-in method
        self.createMenu()
        MainFrame.mainPanel = MainPanel(self)

    #----------------------------------------------------------
    def createMenu(self):      

        # create the menu bar
        menuBar = wx.MenuBar()

        # create a file menu
        fileMenu = wx.Menu()

        opFileBut = wx.MenuItem(fileMenu, wx.ID_ANY, 'Open &File', 'Open a Specific File')
        fileMenu.Append(opFileBut)
        
        # bind the open button to the on_open_directory event
        fileMenu.Bind(wx.EVT_MENU, self.onOpenFile, opFileBut)
        
        # add an open directory Button to the file menu
        opDirBut = wx.MenuItem(fileMenu, wx.ID_ANY, 'Open &Directory', 'Open a Directory with Comic Images')
        fileMenu.Append(opDirBut)

        # bind the open button to the on_open_directory event
        fileMenu.Bind(wx.EVT_MENU, self.onOpenDirectory, opDirBut)
        
        # choose a working directory
        choDbDirBut = wx.MenuItem(fileMenu, wx.ID_ANY, '&Choose Database Directory', 'Choose a Database Directory')
        fileMenu.Append(choDbDirBut)

        # bind the open button to the on_open_directory event
        fileMenu.Bind(wx.EVT_MENU, self.onChoDbDirectory, choDbDirBut)

        # add a line separator to the file menu
        fileMenu.AppendSeparator()

        # add a quit button to fileMenu
        quitBut = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit', 'Exit the Programm')
        fileMenu.Append(quitBut)
        
        # connect the quit button to the actual event of quitting the app
        fileMenu.Bind(wx.EVT_MENU, self.OnQuit, quitBut)

        # call OnQuit if the app is closed via x in title bar (in order to do some cleaning up)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        # give the menu a title
        menuBar.Append(fileMenu, "&File(s)")

        # connect the menu bar to the frame        
        self.SetMenuBar(menuBar)

    #----------------------------------------------------------
    # dialog for opening a specific file
    def onOpenFile(self, event):

        # we only want the users to see the file types that the program can handle
        wildcard = "All compatible files (*.*)| *.*|"\
                   "(*.zip; *.rar; *.cbz; *.cbr)| *.zip; *.rar; *.cbz; *.cbr|"\
                   "(*.jpg; *.jpeg; *.bmp; *.png; *.gif; *.tiff; *.tif)| *.jpg; *.jpeg; *.bmp; *.png; *.gif; *.tiff; *.tif"
                   
        # opening the file dialog with the wildcard we prepared beforehand
        with wx.FileDialog(self, "Choose a File", defaultFile="",wildcard=wildcard,
                          style=wx.FD_DEFAULT_STYLE) as fDlg:

            # if the file dialog wasn't cancelled
            if fDlg.ShowModal() == wx.ID_OK:

                # telling the user to wait until the images are loaded
                loadMlg = LoadingMonolog(None, "Loading Image(s). Please wait...")

                # initialize the image paths list and other temporary variables
                # that later feed the attributes in the "database"-class object MainFrame.comDat
                tmpImgPathsList = []
                tmpImgList = []
                tmpComPageList = []
                tmpComPageIdx = 0
                tmpImgCheckIdx = 0
                
                savDirName = ""

                # initialize sclFile with the path/name of the selected file
                slcFile = fDlg.GetPath()

                # if the file is an archive...
                if slcFile[-3:] in {"zip", "rar", "cbz", "cbr"}:

                    # ...feed the images in the archive to the image list
                    [tmpImgList, tmpImgPathsList] = unpackImgArch2ImgList(slcFile)

                    savDirName = os.path.basename(slcFile)[:-4]

                # if the file is not an archive...
                else:

                    # get the path of every image file within the directory with
                    # the file extension that is specified here
                    tmpImgPathsList = glob.glob(os.path.join(os.path.dirname(slcFile),'*.jpg'))\
                                    + glob.glob(os.path.join(os.path.dirname(slcFile),'*.jpeg'))\
                                    + glob.glob(os.path.join(os.path.dirname(slcFile),'*.bmp'))\
                                    + glob.glob(os.path.join(os.path.dirname(slcFile),'*.png'))\
                                    + glob.glob(os.path.join(os.path.dirname(slcFile),'*.gif'))\
                                    + glob.glob(os.path.join(os.path.dirname(slcFile),'*.tiff'))\
                                    + glob.glob(os.path.join(os.path.dirname(slcFile),'*.tif'))
                    # feeding the temporary image list with images
                    tmpImgList = imgPaths2ImgList(tmpImgPathsList)

                    # set the image counter to the selected file so that the
                    # comic page viewer starts with that
                    tmpComPageIdx = tmpImgPathsList.index(slcFile)
                    
                    if tmpComPageIdx == 0:
                        tmpImgCheckIdx = -1
                    else:
                        tmpImgCheckIdx = tmpComPageIdx

                    savDirName = os.path.basename(os.path.dirname(slcFile))

                # writing the wx.images and their filenames as tuples into the
                # temporary 2D-comic page list:
                # tmpComPageList[x][0] is the image; ...[x][1] is the corresponding file name
                for i in range(len(tmpImgList)):
                    tmpComPageList.append([tmpImgList[i], os.path.basename(tmpImgPathsList[i])])

                # if it does not exsist already create the main "database"-object
                if not hasattr(MainFrame, "comDat"):
                    MainFrame.comDat = DataHandler([], 0, [], 0, "", savDirName)
                # else clear all lists and indices
                else:
                    MainFrame.comDat.mainListHandler(1)
                    MainFrame.comDat.savDirName = savDirName

                # destroying the loading monolog window
                loadMlg.finished()

                # calling the image check class to let the users decide which
                # images they want to work with
                ImageCheck(tmpComPageList, 0, tmpImgCheckIdx, title='Comic Page Check', parent=wx.GetTopLevelParent(self))

                # constructing possible database paths
                # 1 = folder of the images
                # 2 = folder of this python script
                tcpDbPath1 = pathlib.Path.joinpath(pathlib.Path(os.path.dirname(fDlg.GetPath()), '_TCPdb'))
                tcpDbPath2 = pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(), '_TCPdb')

                # checking if there is a database directory
                if os.path.exists(tcpDbPath2):
                    dbDir = str(tcpDbPath2)
                    print("Database path is set to: ", dbDir)
                    MainFrame.comDat.dbPath = dbDir[:-6]

                # if both database directories (tcpDbPath1 and tcpDbPath2) exist,
                # the one in the comic's directory is set as the standard db-path
                if os.path.exists(tcpDbPath1):
                    dbDir = str(tcpDbPath1)
                    print("Database path is set to: ", dbDir)
                    MainFrame.comDat.dbPath = dbDir[:-6]
                    
                timingsFilePath = MainFrame.comDat.dbPath + MainFrame.comDat.savDirName + "_BubbleDetectionTimes.csv"
                timingsFilePath = pathlib.PurePath(timingsFilePath)
                with open(str(timingsFilePath), "w", encoding="utf-8") as txtFile:
                    txtFile.write("Filename;PageNum;Duration;Type\n")

            else:
                # if the dialog was canceled do the following
                return

    #----------------------------------------------------------
    # dialog for opening a directory
    def onOpenDirectory(self, event):

        # opening the directory dialog
        with wx.DirDialog(self, "Choose a Directory",
                          style=wx.DD_DEFAULT_STYLE) as dDlg:

            # if the directory dialog wasn't cancelled
            if dDlg.ShowModal() == wx.ID_OK:

                # telling the user to wait until the images are loaded
                loadMlg = LoadingMonolog(None, "Loading Image(s). Please wait...")

                # initialize the image paths list and other temporary variables
                # that later feed the attributes in the "database"-class object MainFrame.comDat
                tmpImgPathsList = []
                tmpImgList = []
                tmpComPageList = []
                tmpComPageIdx = 0
                
                savDirName = ""

                # get every image file within the directory whose type is specified here
                tmpImgPathsList = glob.glob(os.path.join(dDlg.GetPath(),'*.jpg'))\
                                + glob.glob(os.path.join(dDlg.GetPath(),'*.jpeg'))\
                                + glob.glob(os.path.join(dDlg.GetPath(),'*.bmp'))\
                                + glob.glob(os.path.join(dDlg.GetPath(),'*.png'))\
                                + glob.glob(os.path.join(dDlg.GetPath(),'*.gif'))\
                                + glob.glob(os.path.join(dDlg.GetPath(),'*.tiff'))\
                                + glob.glob(os.path.join(dDlg.GetPath(),'*.tif'))

                if tmpImgPathsList:

                    # feeding the temporary image list with images
                    tmpImgList = imgPaths2ImgList(tmpImgPathsList)                    

                    # writing the wx.images and their filenames as tuples into the
                    # temporary 2D-comic page list:
                    # tmpComPageList[x][0] is the image; ...[x][1] is the corresponding file name
                    for i in range(len(tmpImgList)):
                        tmpComPageList.append([tmpImgList[i], os.path.basename(tmpImgPathsList[i])])

                    savDirName = os.path.basename(dDlg.GetPath())

                    # if it does not exsist already create the main "database"-object
                    if not hasattr(MainFrame, "comDat"):
                        MainFrame.comDat = DataHandler([], 0, [], 0, "", savDirName)
                    # else clear all lists and indices
                    else:
                        MainFrame.comDat.mainListHandler(1)
                        MainFrame.comDat.savDirName = savDirName

                    # destroying the loading monolog window
                    loadMlg.finished()

                    # calling the image check class to let the users decide which
                    # images they want to work with
                    ImageCheck(tmpComPageList, 0, tmpComPageIdx, title='Comic Page Check', parent=wx.GetTopLevelParent(self))

                    # constructing possible database paths
                    # 1 = folder of the images
                    # 2 = folder of this python script
                    tcpDbPath1 = pathlib.Path.joinpath(pathlib.Path(dDlg.GetPath(), '_TCPdb'))
                    tcpDbPath2 = pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(), '_TCPdb')

                    # checking if there is a database directory
                    if os.path.exists(tcpDbPath2):
                        dbDir = str(tcpDbPath2)
                        print("Database path is set to: ", dbDir)
                        MainFrame.comDat.dbPath = dbDir[:-6]

                    # if both database directories (tcpDbPath1 and tcpDbPath2) exist,
                    # the one in the comic's directory is set as the standard db-path
                    if os.path.exists(tcpDbPath1):
                        dbDir = str(tcpDbPath1)
                        print("Database path is set to: ", dbDir)
                        MainFrame.comDat.dbPath = dbDir[:-6]
                        
                    timingsFilePath = MainFrame.comDat.dbPath + MainFrame.comDat.savDirName + "_BubbleDetectionTimes.csv"
                    timingsFilePath = pathlib.PurePath(timingsFilePath)
                    with open(str(timingsFilePath), "w", encoding="utf-8") as txtFile:
                        txtFile.write("Filename;PageNum;Duration;Type\n")

                else:

                    # destroying the loading monolog window
                    loadMlg.finished()
                    
                    # telling the user that there are no compatible files and wait 3 seconds
                    loadMlg = LoadingMonolog(None, "Sorry, there are no compatible files in the chosen directory.")
                    time.sleep(3)
                    
                    # destroying the loading monolog window
                    loadMlg.finished()
                    
                    # calling the open directory dialog again
                    self.onOpenDirectory(None)

            else:
                # if the dialog was canceled do the following
                return

    #----------------------------------------------------------
    # dialog for opening a directory
    def onChoDbDirectory(self, event):

        # opening the directory dialog
        with wx.DirDialog(self, "Choose a Directory for the Database Files",
                          style=wx.DD_DEFAULT_STYLE) as dDlg:

            # if the directory dialog wasn't cancelled
            if dDlg.ShowModal() == wx.ID_OK:

                savDirName = dDlg.GetPath()
                dbPath = savDirName + "_TCPdb"
                savDirName = pathlib.PurePath(dDlg.GetPath())
                dbPath = pathlib.PurePath(dbPath)

                # if it does not exsist already create the main "database"-object
                if not hasattr(MainFrame, "comDat"):
                    MainFrame.comDat = DataHandler([], 0, [], 0, "", savDirName)

                MainFrame.comDat.dbPath = dbPath

    #----------------------------------------------------------
    def OnQuit(self, event):
        # get the frame's top level parent and destroy/close it
        wx.GetTopLevelParent(self).Destroy()

    #----------------------------------------------------------
    def onKey(self, event):

        # if the user is not typing in the text box check the following keys
        if not wx.Window.HasFocus(BubTextBox.speeBubTxtBox):

            keyCode = event.GetKeyCode()

            if keyCode == wx.WXK_LEFT:
                ComicPageViewer.onPrev(self, None)
            elif keyCode == wx.WXK_RIGHT:
                ComicPageViewer.onNext(self, None)
            elif keyCode == wx.WXK_UP:
                SpeeBubTextEditor.onPrev(self, None)
            elif keyCode == wx.WXK_DOWN:
                SpeeBubTextEditor.onNext(self, None)
            else:
                event.Skip()
        else:
            event.Skip()

#====================================================================
# the main frame of the program
class App(wx.App):
    def OnInit(self):
        self.frame = MainFrame()
        self.frame.Show()
        self.frame.SetFocus()
        return True

#====================================================================
# opens a seperate window that displays image the user has to choose from
#
#
# INPUT:    tmpImgList - list with images (type: list with either wx._core.image or 
#                                                                     wx._core.bitmap)
# OUTPUT:   None (depending on what images are displayed either the bubble list
#                 for the current page is filled or the comic pages are reset
#                 with the images chosen by the user)

class ImageCheck(wx.Frame):

    bxs = []
    tmpImgList = []
    comPaOrBub = []

    def __init__(self, imgList, comPaOrBub, slcFile, title, parent=None):

        [disX, disY] = wx.GetDisplaySize()
        frameSize = int(disY*0.9)

        wx.Frame.__init__(self, parent=parent, title=title, size=(frameSize, frameSize))

        self.comPaOrBub = comPaOrBub

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Create upper and lower sub panels
        upSubPan = wx.lib.scrolledpanel.ScrolledPanel(self, wx.ID_ANY)
        upSubPan.SetupScrolling()
        upSubPan.SetBackgroundColour("#FFFFFF")

        loSubPan = wx.Panel(self, wx.ID_ANY)

        imgCount = len(imgList)

        self.tmpImgList = imgList

        # if the list contains comic page images
        if self.comPaOrBub == 0:

            gridX = 4
            gridY = math.ceil(imgCount/gridX)

            gridCellSize = math.ceil(frameSize/3.5)

        # if the list contains speech bubble images
        elif self.comPaOrBub == 1:

            gridX = math.ceil(math.sqrt(imgCount))
            gridY = math.ceil(imgCount/gridX)

            gridCellSize = math.ceil(frameSize/gridX/1.1)

        gridSizer = wx.GridBagSizer(gridX, gridY)

#        gridSizer.SetDefaultCellBackgroundColour(0,0,0)

        imgCount = 0
        self.bxs = []
        numSel = 0

        for yPos in range(gridY):

            for xPos in range(gridX):
                if imgCount < len(self.tmpImgList):

                    gridCellSizer = wx.BoxSizer(wx.VERTICAL)

                    # we want to scale the images and therefore we have to
                    # convert possible bitmaps into wx.Image because
                    # wx.Image has a method to do so and wx.Bitmap does not
                    try:
                        img = self.tmpImgList[imgCount][0].ConvertToImage()
                    except Exception:
                        img = self.tmpImgList[imgCount][0]

                    imgH = img.GetHeight()
                    imgW = img.GetWidth()

                    if imgW > imgH:
                     	scaleRatio = imgW/gridCellSize
                    elif imgW < imgH:
                        scaleRatio = imgH/gridCellSize

                    imgH = int(imgH/scaleRatio)
                    imgW = int(imgW/scaleRatio)

                    if imgH < gridCellSize/8:
                        imgH = int(imgH*5)

                    # scaling the image
                    img = img.Scale(imgW, imgH, wx.IMAGE_QUALITY_HIGH)

                    bmpId = "bmp" + str(yPos+1) + str(yPos) + str(xPos)

                    # convert the image back to a bitmap and wrap it into a static bitmap
                    img = wx.StaticBitmap(upSubPan, wx.ID_ANY, wx.Bitmap(img), name=bmpId)
                    img.Bind(wx.EVT_LEFT_DOWN, self.OnLeftMouseButton)
                    
                    # add the image to the cell sizer
                    gridCellSizer.Add(img, 0, wx.CENTER)

                    # all check boxes get a unique name and are checked by default
                    # they are also asigned to the same vertical sizer as the
                    # images, so that they are placed directly underneath them
                    chkBxId = "chkBx" + str(yPos+1) + str(yPos) + str(xPos)
                    chkBx = wx.CheckBox(upSubPan, name=chkBxId)

                    if slcFile == 0:
                        chkBx.SetValue(True)
                        numSel = imgCount+1

                    # check the box if the user selected the first image in the folder
                    if slcFile < 0 and imgCount == 0:
                        chkBx.SetValue(True)
                        numSel = 1
                    # uncheck the box if it is not the first image in the folder/list
                    elif slcFile < 0 and imgCount > 0:
                        chkBx.SetValue(False)

                    # uncheck the box if the user did not select the first
                    # image in the folder and its not the image the user has chosen
                    if slcFile > 0 and imgCount != slcFile:
                        chkBx.SetValue(False)
                    # check the box if it is the image the user has chosen
                    elif imgCount == slcFile:
                        chkBx.SetValue(True)
                        numSel = 1
                    
                    # add the check box to the cell sizer
                    gridCellSizer.Add(chkBx, 0, wx.CENTER)
                    self.bxs.append(chkBx)
                    
                    # add the cell sizer to the grid sizer
                    gridSizer.Add(gridCellSizer, pos=(yPos, xPos))#, flag=wx.EXPAND)
                    
                    imgCount += 1

        upSubPanHoriSizer = wx.BoxSizer(wx.HORIZONTAL)

        upSubPanHoriSizer.AddStretchSpacer()
        upSubPanHoriSizer.Add(gridSizer, wx.ID_ANY, wx.CENTER)
        upSubPanHoriSizer.AddStretchSpacer()

        upSubPan.SetSizer(upSubPanHoriSizer)

        txtNumImg = str(numSel) + " of " + str(len(self.bxs)) + " selected."
        
        ImageCheck.stTxtNumImg = wx.StaticText(loSubPan, wx.ID_ANY, txtNumImg)

        loSubPanVertSizer = wx.BoxSizer(wx.VERTICAL)
        loSubPanVertSizer.AddStretchSpacer()
        loSubPanVertSizer.Add(ImageCheck.stTxtNumImg, 1, wx.CENTER)
        loSubPanVertSizer.AddStretchSpacer()

        loSubPanHoriSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        btnSelectAll = wx.Button(loSubPan, wx.ID_ANY, "&Select All")
        btnSelectAll.Bind(wx.EVT_BUTTON, self.OnSelectAll)
        
        btnDeselectAll = wx.Button(loSubPan, wx.ID_ANY, "&Deselect All")
        btnDeselectAll.Bind(wx.EVT_BUTTON, self.OnUnSelectAll)
        
        self.btnApply = wx.Button(loSubPan, wx.ID_ANY, "&Apply")
        self.Bind(wx.EVT_BUTTON, self.OnApply, self.btnApply)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        loSubPanHoriSizer.AddStretchSpacer()
        loSubPanHoriSizer.Add(btnSelectAll)
        loSubPanHoriSizer.Add(btnDeselectAll)
        loSubPanHoriSizer.Add(self.btnApply)
        loSubPanHoriSizer.AddStretchSpacer()

        loSubPanVertSizer.Add(loSubPanHoriSizer, 1, wx.EXPAND|wx.ALL)
        loSubPanVertSizer.AddStretchSpacer()

        loSubPan.SetSizer(loSubPanVertSizer)

        mainSizer.Add(upSubPan, 1, wx.EXPAND|wx.ALL)
        mainSizer.Add(loSubPan, 0, wx.EXPAND|wx.ALL)

        self.SetSizer(mainSizer)
        self.Show()
        self.Centre()
        self.Raise()
        self.btnApply.SetFocus()

    #----------------------------------------------------------
    def OnLeftMouseButton(self, event):

        imgCtrl = event.GetEventObject()

        chkBxId = "chkBx" + imgCtrl.GetName()[3:]

        j = 0

        for i in self.bxs:
            if i.GetName() == chkBxId:
                i.SetValue(not i.GetValue())

            if i.IsChecked():
                j += 1

        txtNumImgs = str(j) + " of " + str(len(self.bxs)) + " selected."

        ImageCheck.stTxtNumImg.SetLabel(txtNumImgs)
        
        self.btnApply.SetFocus()

    #----------------------------------------------------------
    def OnApply(self, event):

        newImgList = []
        imgCount = 0

        for i in self.bxs:
            if i.IsChecked() and imgCount < len(self.tmpImgList):
                newImgList.append(self.tmpImgList[imgCount])
                
            imgCount += 1

        self.tmpImgList = newImgList

        # if the image list contains bitmaps they are speech bubbles,
        # this is tested by trying to convert them to wx.images (not
        # actually doing it) and calling the speeBubHandler to reset
        # the necessary lists and panels
        try:

            self.tmpImgList[0][0].ConvertToImage()

            MainFrame.comDat.speeBubHandler(self.tmpImgList, 9, 1)

            MainFrame.mainPanel.rSubPan.btnOCR.SetFocus()

        # if the bitmap conversion fails the images are comic pages (wx.images)
        # which means we have to replace the current data with new data
        except Exception:

            MainFrame.comDat.comPageHandler(self.tmpImgList, 9, 1)

            MainFrame.mainPanel.lSubPan.btnFindBub.SetFocus()

        # calling the procedure that closes the window
        self.OnQuit(event)

    #----------------------------------------------------------
    def OnSelectAll(self, event):
        for i in self.bxs:
            if not i.IsChecked():
                i.SetValue(True)

        txtNumImgs = str(len(self.bxs)) + " of " + str(len(self.bxs)) + " selected."

        ImageCheck.stTxtNumImg.SetLabel(txtNumImgs)
        
        self.btnApply.SetFocus()

    #----------------------------------------------------------
    def OnUnSelectAll(self, event):
        for i in self.bxs:
            if i.IsChecked():
                i.SetValue(False)

        txtNumImgs = "0 of " + str(len(self.bxs)) + " selected."

        ImageCheck.stTxtNumImg.SetLabel(txtNumImgs)
        
        self.btnApply.SetFocus()

    #----------------------------------------------------------
    def OnQuit(self, event):

        # destroy the frame/window
        self.Hide()

#====================================================================
# a seperate window with the current comic page on which the users
# can mark a speech bubble they want to add
#
# INPUT:    (type: ?wx._core.bitmap?)
# OUTPUT:   None (depending on what images are displayed either the bubble list
#                 for the current page is filled or the comic pages are reset
#                 with the images chosen by the user)

class addSpeechBubble(wx.Frame):

    def __init__(self, comPage):

        [disX, disY] = wx.GetDisplaySize()
        frameY = int(disY*0.9)

        # get the size of the new image
        [iW, iH] = comPage.GetSize()

        if iH > frameY:
            newH = frameY
            newW = int(frameY * iW / iH)

             # scaling the page image
            comPage = comPage.Scale(newW,newH, wx.IMAGE_QUALITY_HIGH)

        # get the size of the new image
        [iW, iH] = comPage.GetSize()

        wx.Frame.__init__(self, None, title="Add Text Cutout",\
                          size=(iW, iH))

        mainSizer = wx.BoxSizer()

        # creating the sub panel
        subPan = addBubbleImagePanel(comPage, self)

        self.Bind(wx.EVT_CLOSE, self.onQuit)

        mainSizer.Add(subPan, wx.ID_ANY, wx.EXPAND|wx.ALL)

        self.SetSizer(mainSizer)
        self.Show()
        self.Centre()
        self.Raise()

    #----------------------------------------------------------
    def onQuit(self, event):

        # destroy the frame/window
        self.Destroy()

#====================================================================
# the main panel of the "add speech bubble"-frame
class addBubbleImagePanel(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, comPage, parent):
        # Constructor
        wx.Panel.__init__(self, parent=parent)

        self.tmpComPage = comPage

        self.SetBackgroundColour("#FFFFFF")

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_MOTION, self.onMouseMove)

        self.startPos = None
        self.overlay = wx.Overlay()

    #----------------------------------------------------------
    def onPaint(self, evt):
        
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("white"))
        dc.Clear()

        dc.DrawBitmap(self.tmpComPage.ConvertToBitmap(), 0, 0)

    #----------------------------------------------------------
    def onLeftDown(self, evt):
        # Capture the mouse and save the starting posiiton for the
        # rubber-band
        self.CaptureMouse()
        self.startPos = evt.GetPosition()

    #----------------------------------------------------------
    def onMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            rect = wx.Rect(self.startPos, evt.GetPosition())
            
            # Draw the rubber-band rectangle using an overlay so it
            # will manage keeping the rectangle and the former window
            # contents separate.
            dc = wx.ClientDC(self)
            odc = wx.DCOverlay(self.overlay, dc)
            odc.Clear()

            # Mac's DC is already the same as a GCDC, and it causes
            # problems with the overlay if we try to use an actual
            # wx.GCDC so don't try it.
            if 'wxMac' not in wx.PlatformInfo:
                dc = wx.GCDC(dc)
            
            dc.SetPen(wx.Pen("black", 2))
            dc.SetBrush(wx.Brush(wx.Colour(0xC0, 0xC0, 0xC0, 0x80)))
            dc.DrawRectangle(rect)

    #----------------------------------------------------------
    def onLeftUp(self, evt):

        [bubCutX, bubCutY] = self.startPos
        [bubCutW, bubCutH] = evt.GetPosition()

        # the following two if-queries make sure that the rectangle can be
        # drawn from any cornor; all they do, is switch the variables if the
        # starting points are bigger than the end points
        if bubCutX > bubCutW:
            bubCutX, bubCutW = bubCutW, bubCutX

        if bubCutY > bubCutH:
            bubCutY, bubCutH = bubCutH, bubCutY

        # getting the original image and the scaled image
        origImg = MainFrame.comDat.comPageList[MainFrame.comDat.comPageIdx][0]
        sclImg = self.tmpComPage

        # calculating the scale factor between the original and the scaled image
        sclFac = abs(origImg.GetSize()[1] / sclImg.GetSize()[1])

        # applying the scale factor to the coordinates that the user has drawn
        x = int(bubCutX * sclFac)
        y = int(bubCutY * sclFac)
        w = int(bubCutW * sclFac)
        h = int(bubCutH * sclFac)

        if self.HasCapture():
            self.ReleaseMouse()
        self.startPos = None

        # When the mouse is released we reset the overlay and it
        # restores the former content to the window.
        dc = wx.ClientDC(self)
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()
        del odc
        self.overlay.Reset()

        bubCutOut = convertWXimg2CV2img(origImg)

        bubCutOut = [convertCv2Img2WxImg(bubCutOut[y:h, x:w]), [x, y, w, h]]

        # calling the speech bubble handler to add the new bubble
        MainFrame.comDat.speeBubHandler(bubCutOut, 9, 2)

        wx.GetTopLevelParent(self).Destroy()

#====================================================================

#======================
# main OCR functions
#====================================================================
# this function returns a list of images that contain text
# 
def findTextOnComicPage(wxImg):

    contourList = []
    bubContourList =[]
    letterRectList = []
    bubRectList = []
    speeBubImgList = []

    # first we have to convert the wx.Image into an cv2.Image    
    img = convertWXimg2CV2img(wxImg)

    # getting the size of the comic page image using the shape method from cv2
    imgH, imgW = img.shape[:2]

    # letting cv2 search for contours on the page; the parameter "1" sets a pre-processing
    # method specifically designed for better accuracy in finding letters later on
    contourList = findContours(img, 1)

    # parameter "2" sets a image pre-processing method that is better for finding bubble and
    # box contours or simply bigger contours with specific size ratios
    bubContourList = findContours(img, 2)

    # calling the function designed to find small, text-sized contours on the comic page;
    # it returns a list with bounding rectangles for the contours it has found
    letterRectList = findLetterContourRects(contourList, img, imgH, imgW)

    # calling the function designed to find larger contours such as speech bubbles
    # and text boxes; it also returns a list with bounding rectangles
    bubRectList = findBubRectContours(bubContourList, img, imgH, imgW)

    # this function takes the list of bounding letter rectangles and tries to determine
    # the location on the comic image where they cluster; it returns a list of
    # bounding rectangles that mark the outer limits of those clusters
    txtClustersList = findTxtClusters(letterRectList, img, imgH, imgW)

    # finally, this function compares the coordinates of all previously found
    # contours with each other; if they match they are most likely contain text
    bubLetRectList = findTxtBubsBoxs(letterRectList, txtClustersList, bubRectList, img)

    if bubLetRectList:    
        for rect in bubLetRectList:
            x = int(rect[0])
            y = int(rect[1])
            w = int(rect[2])
            h = int(rect[3])
            speeBubImgList.append([convertCv2Img2WxImg(img[y:y+h, x:x+w]), [x, y, w, h]])

    return speeBubImgList

#====================================================================
# converting the wx.Image format to the cv2.Image format
# the input  vakue process defines which processes are used on the image
def findContours(img, process):

    contourList = []

    # in the following are some converting which ensures that the text
    # on the page is easier to find for the cv2 algorithms

    # inverting the image colors
    img = cv2.bitwise_not(img)

    # making the image brighter
    img = cv2.convertScaleAbs(img, alpha=1.0, beta=50)

    # reducing the color space via a threshold operation; this is done
    # in order to get rid of color gradiants which are sometimes used
    # as background for text on the comic page
    img = cv2.threshold(img,140,255,cv2.THRESH_BINARY)[1]

    # inverting the image colors back again
    img = cv2.bitwise_not(img)

    # converting the image colors to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # creating a binary copy of the gray scale image
    binImg = cv2.threshold(img, 149, 255, cv2.THRESH_BINARY)[1]

    if process == 1:
        # trying to "thin" the black lines on the page in order to
        # get more coherent contours
        # currently, this parameter setup does nothing to the image;
        # change the settings in order to adapt its behavior to different
        # sources if needed
        kernel = np.ones((1,1), np.uint8)
        binImg = cv2.dilate(binImg, kernel, iterations = 1)

    elif process == 2:
        # mainly trying to "fatten" the text by filling in possible gaps 
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        binImg = cv2.erode(binImg, kernel, iterations = 1)

    elif process == 3:
        return binImg

    #finally letting cv2 find all the contours in the binary image
    #IMPORTANT: for CV2 and CV4 the return value index has to be [0] and
    #           for CV3 it has to be [1]; this exclusively returns the list of contours
    openCvVer = cv2.__version__.split(".")[0]

    if process <=2 and (openCvVer == "2" or openCvVer == "4"):
        contourList = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        
    elif process <=2 and openCvVer == "3":
        contourList = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

    return contourList

#====================================================================
# trying to find contours that have the size of text on the page and
# that cluster horizontally
def findLetterContourRects(contourList, img, imgH, imgW):

    letterRectList = []
    exPtsList = []

    # specify how big the contours are allowed to be in relation to the
    # size of the image; xMin/xMax 0.004/0.05 & yMin/yMax 0.0025/0.015
    # is approximatly comic letter size
    conLetMinW=int(imgW*0.004)
    conLetMaxW=int(imgW*0.025)
    conLetMinH=int(imgH*0.0025)
    conLetMaxH=int(imgH*0.015)

    # eleminate all contours that are larger than specified above
    for contour in contourList:
        # at first we only need the rough (rectangular) dimensions of the contour
        rect = cv2.boundingRect(contour)
        [x, y, w, h] = rect

        # in order to find the text in the image we have to filter countours
        # with sizes above xMin/xMax 0.004/0.05 & yMin/yMax 0.0025/0.015
        # relative to image size, which is approximatly comic letter size
        if conLetMinW < w < conLetMaxW and\
            conLetMinH < h < conLetMaxH:

            # rectangles of fitting contours are appended to the List
            letterRectList.append(rect)
            
            # calculating the y- and x-positions of the rectangles edges' middle points...
            y1=int((h/2)+y)
            x1=int((w/2)+x)

            # ...and write the coordinates of all edges' middle points into
            # the array that will be used to find proxies;
            # the order is xyLeft, xyRight, xyTop, xyBottom
            exPtsList.append([(x,y1),(x+w,y1),(x1,y),(x1,y+h)])

    #######################################################################
    # in the next step we will try to find clusters of text rectangles by #
    # taking each rectangle and check whether another rectangle is within #
    # a certain range of its most extreme right and left                  #
    #######################################################################
    
    # initializing variables for counting purposes
    i = j = 0
    
    # what range of rectangles to the left and right of the current rectangle
    # should the algorithm search for; the given number defines the range
    # for each direction; for example, 25 will result in the search for 50 rectangles,
    # 25 to the left and 25 to the right
    ptsRange = 25
    
    # what range of pixels around the point should the algorithm search in;
    # also, doublepages get little less range, since their width does not
    # increase the distance between the letters
    if 0.5 <= imgW/imgH <= 0.8:
        xPtsArea = int(imgW*0.025)
    else:
        xPtsArea = int((imgW/2)*0.04)

    # comic pages usually have more or less an identical height, therefore
    # the height of the points' search area is the same for all comic page images
    yPtsArea = int(imgH*0.00165)

    # initializing the final rectangle list
    sortRectList = []

    # if check1 and check2 are True then the algorithm will stop searching
    # for more nearby rectangles
    check1 = check2 = False

    # in the following for-loop the middle points of every rectangel's
    # left and right edge within the array exPtsList are checked wether
    # it is located near another point within the array exPtsList;
    # the middle points of the letf and right edges of the rectangles were
    # chosen because letters are usually written at the same height
    for i in range(len(exPtsList)):
        
        # initialzing the points array which will contain the points nearby
        # the current point; its size will be specified in the next step
        ptsRangeArr = []

        # we take a slice out of the rectangle array with the size of ptsRange
        # because we only want to check this number of points around the currently
        # selected point
        if i < ptsRange:
            ptsRangeArr = exPtsList[:i+ptsRange+1]
        elif i > len(exPtsList)-ptsRange:
            ptsRangeArr = exPtsList[i-ptsRange:]
        else:
            ptsRangeArr = exPtsList[i-ptsRange:i+ptsRange]

        # point in the middle of the left edge of the rectangle
        xL1=exPtsList[i][0][0]
        yL1=exPtsList[i][0][1]
        # point in the middle of the right edge of the rectangle
        xR1=exPtsList[i][1][0]
        yR1=exPtsList[i][1][1]

        # checking every point in ptsRangeArr against the current point in
        # exPtsList; if the booleans check1 or check2 are True, the for loop
        # will be stopped
        for j in range(len(ptsRangeArr)):

            # here we leave out checking the point against itself
            if exPtsList[i] != ptsRangeArr[j]:
            
                # point to compare xL1 & yL1 with
                xL2=ptsRangeArr[j][0][0]
                yL2=ptsRangeArr[j][0][1]
                # point to compare xR1 & yR1 with
                xR2=ptsRangeArr[j][1][0]
                yR2=ptsRangeArr[j][1][1]

                # check whether the nearby point is on the left side of the
                # current rectangle
                if xL2 > xL1-xPtsArea and xL2 < xL1+xPtsArea and\
                   yL2 > yL1-yPtsArea and yL2 < yL1+yPtsArea:

                       sortRectList.append(letterRectList[i])
                       check1 = True

                # check whether the nearby point is on the right side of the
                # current rectangle
                if xR2 > xR1-xPtsArea and xR2 < xR1+xPtsArea and\
                   yR2 > yR1-yPtsArea and yR2 < yR1+yPtsArea:

                       sortRectList.append(letterRectList[i])
                       check2 = True

                if check1 or check2 == True:
                    break

        check1 = check2 = False

    # check the array for doublets
    sortRectList = [q for o, q in enumerate(sortRectList) if q not in sortRectList[:o]]

    # as the function name states: eliminate rectangles enclosed by other rectangles
    sortRectList = eliminateEnclosedRectangles(sortRectList)

    return sortRectList

#====================================================================
# eleminate all rectangles from the list that are enclosed by another rectangle
def eliminateEnclosedRectangles(rectList):

    eliRectList = []

    # every rectangle in the list is checked against...
    for i in range(len(rectList)):
    
        [x1ul,y1ul,w1,h1] = rectList[i]

        # ...every rectangle in the list
        for j in range(len(rectList)):

            [x2ul,y2ul,w2,h2] = rectList[j]

            # if "1" is not the same rectangle as "2" and every corner
            # from rectangle "1" is inside rectangle "2", write "1"
            # in the elimination list and stop the inner for-loop
            if rectList[i] != rectList[j] and\
               x2ul <= x1ul <= x2ul+w2 and\
               y2ul <= y1ul <= y2ul+h2 and\
               x2ul <= x1ul+w1 <= x2ul+w2 and\
               y2ul <= y1ul+h1 <= y2ul+h2:

                   eliRectList.append(rectList[i])
                   break

    # delete all rectangles from the list that are in the elimination list
    rectList = [x for x in rectList if x not in eliRectList]

    return rectList

#====================================================================
# trying to find contours of the speech bubbles / text boxes only by the
# space they occupy on the page
def findBubRectContours(contourList, img, imgH, imgW):

    bubRectList = []

    # eleminate all contours that are larger than specified
    for contour in contourList:

        # we only need the rough (rectangular) dimensions of the contour
        rect = cv2.boundingRect(contour)
        [x, y, w, h] = rect

        # rectangles that are not between 1,5% and 50% of the width of the page
        # as well as between 1,5% and 25% of the height of the page
        # are eliminated
        if imgW*0.015 < w < imgW*0.5 and imgH*0.015 < h < imgH*0.25:
            
            # rectangles of fitting contours are appended to the List
            bubRectList.append(rect)

        # this adds rectangles to the list that are wider than 30% of the
        # page but have a maximum height of only 10% of the page
        if w > imgW*0.3 and h < imgH*0.1:

            # rectangles of fitting contours are appended to the List
            bubRectList.append(rect)

    # check the list for doublets
    bubRectList = [q for o, q in enumerate(bubRectList) if q not in bubRectList[:o]]

    return bubRectList

#====================================================================
# this function searches for rectangle clusters
def findTxtClusters(letterRectList, img, imgH, imgW):

    # at first we initialize a list with rows that match the height of
    # the image and columns that match the images width; each element in this
    # list basically represents a pixel of the given image
    # every element in the list is initialized as '0'
    cluArr = np.array([[0 for x in range(imgW)] for y in range(imgH)])

    # now we fill the those elements in the list with '1's that match the areas or
    # coordinates of the given rectangles that was found in the image;
    # for each rectangle in the given list...
    for i in range(len(letterRectList)):
        # the coordinates of the current rectangle are extracted into x,y,w,h;
        # with those four variables the area of the rectangle on the image can
        # be reconstructed
        [x, y, w, h] = letterRectList[i]

        # for each column in the row of pixels within the height of the given
        # rectangle set the element in the cluster list to "1";
        # j is the index for the vertical pixels or pixel rows that the rectangle
        # covers on the image
        for j in range(h):
            # k is the index for the horizontal pixels or pixel columns that
            # the rectangle covers on the image
            for k in range(w):
                # if the indicies of the elements in the cluster list are within
                # the image dimensions, set the element of the cluster list to "1";
                # this is to prevent "out of bounds"-list errors that could crash
                # the program
                if y+h <= imgH and x+w <= imgW:
                    cluArr[y+j][x+k] = 1

    # now the gabs within smaller clusters are filled by defining how much
    # distance (pixels) a cloud of "1"s/ones is allowed to have in the x and y
    # direction before it gets turned into a zero
    # if the image size ratio is between 0.5 and 0.8 set the horizontal distance
    # rate to 1% of the width of the image; else set it to 0.5%, which works better
    # for double paged images; on an image with a width of 1000 pixels, "1"-elements,
    # are allowed to have a horizontal distance of 10 pixels to the next "1"-element before it
    # is reset as "0"-element
    if 0.5 <= imgW/imgH <= 0.8:
        ptsRangeX = int(len(cluArr[0])*0.01)
    else:
        ptsRangeX = int(len(cluArr[0])*0.005)

    # set the vertical distance rate to 0.006% of the images height
    # on an image with a height of 1500 pixels, "1"-elements,
    # are allowed to have a vertical distance of 9 pixels to the next "1"-element before it
    # is reset as "0"-element
    ptsRangeY = int(len(cluArr)*0.006)

    # filling in the gabs of the array
    # for every row in the cluster list or every pixel row in the image
    for i in range(len(cluArr)):

        # if the row has "1"-elements in it
        if sum(cluArr[i]) != 0:

            # for every element/pixel in the row of the list/image
            for j in range(len(cluArr[i])):

                # if the element is "1", do the following...
                if cluArr[i][j] == 1:

                    # determine the remaining vertical and horizontal elements/pixels
                    # until end of the list
                    maxPtsRangeX = int(len(cluArr[i]) - j)
                    maxPtsRangeY = int(len(cluArr) - i)

                    # this if-statement is to avoid "out of bound"-list errors
                    # that could crash the program;
                    # if the maximal horizontal distance to the current element/pixel
                    # is samller than the list's/image's maximal element/pixel range,
                    # set the checking variable to the list's/image's final index
                    if maxPtsRangeX < ptsRangeX:
                        checkPtsX = maxPtsRangeX
                    # else set it to the maximal horizontal distance from the current element
                    else:
                        checkPtsX = ptsRangeX

                    # see last if-statement above
                    if maxPtsRangeY < ptsRangeY:
                        checkPtsY = maxPtsRangeY
                    else:
                        checkPtsY = ptsRangeY

                    # reseting the "0"-element counter to zero
                    zeroCount = 0

                    # for every element/pixel within the horizontal checking
                    # range do the following...
                    for k in range(checkPtsX):

                        # if-statement that limits the search to the elements
                        # in the list that are within the checking range
                        if k+1 < checkPtsX:

                            # if the element in the cluster list is "0", increase
                            # the "0"-element counter by one
                            if cluArr[i][j+k+1] == 0:
                                zeroCount += 1
                    
                            # if an "1"-element has been found that is within the
                            # range of the currently checked "1"-element...
                            if cluArr[i][j+k+1] == 1 and zeroCount != 0:

                                # reset all the elements between those two
                                # "1"-elements to "1"-elements and exit the for-loop;
                                # in other words the gap is being filled with "1"-elements
                                for l in range(zeroCount):
                                    cluArr[i][j+l+1] = 1
                                break

                            # if no "1"-elements have been found within the
                            # checking range,...
                            if zeroCount == checkPtsX:
                            
                                # reset all elements in that range to "0",
                                # including the currently checked "1"-element
                                for l in range(zeroCount):
                                    cluArr[i][j+l+1] = 0

                            # if the item next to the currently checked "1"-element
                            # is also an "1"-element, break the for-loop;
                            # in other words no gap needs to be filled
                            if cluArr[i][j+k+1] == 1 and zeroCount == 0:
                                break

                    # reset the "0"-element counter to zero
                    zeroCount = 0

                    # for every element/pixel within the vertical checking range
                    # do the same as in the for-loop that checks horizontally
                    for k in range(checkPtsY):

                        if k+1 < checkPtsY:

                            if cluArr[i+k+1][j] == 0:
                                zeroCount += 1

                            if cluArr[i+k+1][j] == 1 and zeroCount != 0:
                                for l in range(zeroCount):
                                    cluArr[i+l+1][j] = 1
                                break
                                
                            if zeroCount == checkPtsY:
                                break

                            if cluArr[i+k+1][j] == 1 and zeroCount == 0:
                                break

    # the cluster list is now used to actually identify the coordinates of the
    # rectangle clusters; this is done by utilizing the measurement-module of the
    # scipy.ndimage module; first we create a list that contains labels of the
    # areas with "1"-elements in the list/array that we just created and use that
    # to create another list that contains the coordinates of the bounding rectangles
    # of those objects
    #
    # s is the structuring element; standard is [[0,1,0],[1,1,1],[0,1,0],]
    # this way elements that touch diagonally are also taken into account
    s = [[1,1,1],[1,1,1],[1,1,1]]

    # creating the list that contains the labels of the "1"-element areas
    labArr, num = measurements.label(cluArr, structure=s)

    # creating the list that contains the bounding rectangles' coordinates
    # of the "1"-element objects
    txtObj = []
    txtObj = measurements.find_objects(labArr)

    rectArea = []

    # extracting the coordinates from the measurements-list into an integer list
    for d in range(len(txtObj)):
        x1 = int(txtObj[d][1].start)
        x2 = int(txtObj[d][1].stop)
        y1 = int(txtObj[d][0].start)
        y2 = int(txtObj[d][0].stop)
        
        rectArea.append((x2-x1)*(y2-y1))

    # this preliminary list of possible "text-objects" needs further refinement;
    # first, rectangles with an area smaller than the average area size are omitted

    # calculate the average area of the rectangles in the list
    aveArea = int(mean(rectArea)*0.34)

    txtClusterList = []
    rectMeanValsList = []
    tempTxtClusterList1 = []

    # converting the given image file/comic page into a binary/black & white image,
    # which is necessary in order to determine the average intensity of the
    # cluster areas later;
    img = findContours(img, 3)

    # extracting the rectangular areas from the image, but only those with an
    # area larger or equal the average area size; these are the possible
    # ("text"-)cluster candidates
    for d in range(len(txtObj)):
        if aveArea <= rectArea[d]:

            x = int(txtObj[d][1].start)
            y = int(txtObj[d][0].start)
            w = int(txtObj[d][1].stop-txtObj[d][1].start)
            h = int(txtObj[d][0].stop-txtObj[d][0].start)

            # extracting the part of the image defined by the rectangle's coordinates
            rect = img[y:y+h, x:x+w]

            # noting the inensity of the the rectangles' areas
            rectMeanValsList.append(rect.mean())

            # writing the rectangles' coordinates of the possible ("text"-)cluster
            # candidates into a list
            tempTxtClusterList1.append([x,y,w,h])

    # determine the average intensity of the ("text"-)cluster candidates' areas
    aveRectIntensity = int((mean(rectMeanValsList)))

    # going through the list of possible ("text"-)cluster candidates, only keeping those
    # that have an intensity higher or equal to 90% of the candidates' average intensity
    for d in range(len(tempTxtClusterList1)):
        
        x = tempTxtClusterList1[d][0]
        y = tempTxtClusterList1[d][1]
        w = tempTxtClusterList1[d][2]
        h = tempTxtClusterList1[d][3]
        
        rect = img[y:y+h, x:x+w]
        if rect.mean() >= aveRectIntensity*0.9:
            txtClusterList.append([x,y,w,h])

    return txtClusterList

#====================================================================
# this function searches for rectangles with text in them
def findTxtBubsBoxs(letRectList, txtClusList, bubRectList, img):

    realTextRectList = []

    # for each rectangle/coordinates-item in the text-cluster list
    for i in range(len(txtClusList)):
        
        distRectList = []
        txtNotInBubOrBox = True

        # assigning the coordinates to seperate variables
        [x1ul, y1ul, w1, h1] = txtClusList[i]

        # calculate the middle point-coordinates of the rectangle/item
        midX1 = x1ul+(w1/2)
        midY1 = y1ul+(h1/2)
        
        # calculate the size of the rectangle area
        areaRect1 = w1*h1

        # for each bounding rectangle in the speech bubble / caption box list...
        for j in range(len(bubRectList)):
        	
            # a counter that increases if a corner of the current text-cluster rectangle
            # fits into the current bounding rectangle of the speech bubble or caption box 
            cornerCount = 0

            # assigning the coordinates to seperate variables
            [x2ul, y2ul, w2, h2] = bubRectList[j]

            # calculate the middle point-coordinates of the rectangle/item
            midX2 = x2ul+(w2/2)
            midY2 = y2ul+(h2/2)

            # calculate the size of the rectangle area
            areaRect2 = w2*h2

            # these if-statements check whether any of the text-clusters' bounding
            # rectangles are within the boundaries of the current speech bubble or
            # text box; if so, the cornor counter is increased by 1
            if x2ul <= x1ul <= x2ul+w2 and y2ul <= y1ul <= y2ul+h2:
                cornerCount += 1
            if x2ul <= x1ul <= x2ul+w2 and y2ul <= y1ul+h1 <= y2ul+h2:
                cornerCount += 1
            if x2ul <= x1ul+w1 <= x2ul+w2 and y2ul <= y1ul+h1 <= y2ul+h2:
                cornerCount += 1
            if x2ul <= x1ul+w1 <= x2ul+w2 and y2ul <= y1ul <= y2ul+h2:
                cornerCount += 1

            # if at least one corner is within the boundaries of the current
            # speech bubble or text box AND the latter's area is within 74% and
            # 400% of the text-cluster's bounding rectangle, the distance between
            # the middle points of both rectangles is written into a list
            if cornerCount >= 1 and areaRect1*0.74 <= areaRect2 <= areaRect1*4:
                distRectList.append([j, int(math.hypot(midX2 - midX1, midY2 - midY1))])

            # this if statement ensures that potential text cluster candidates
            # are not added more than once to the final list
            if cornerCount >= 2:
                txtNotInBubOrBox = False

        # if there are any middle point distances in the respective list, the
        # rectangle with the smallest distance of its middle point to that of the
        # text-cluster bounding rectangle's middle point made it into the final list
        if distRectList:
            [minDistRectItemPos, minDistRect] = min(distRectList, key=lambda x: x[1])

            realTextRectList.append(bubRectList[minDistRectItemPos])            

        # this if statement ensures that texts without speech bubble or caption
        # box outlines around them are also recognized
        if txtNotInBubOrBox:

            # increasing the size of the rectangle by the given percentage in order
            # to avoid clipping of text/letters that are at the edge
            resizedRect = scaleRectProper(txtClusList[i], 30)

            realTextRectList.append(resizedRect)

    # check the array for doublets
    realTextRectList = [q for o, q in enumerate(realTextRectList) if q not in realTextRectList[:o]]

    return realTextRectList

#====================================================================
# scale a rectangle while maintaing its position on the image
# INPUT:    rect - a rectangle (type: tuple with x, y, width, and height data)
#           percent - scale percentage (type: integer/float/... any type of real number)
# OUTPUT:   resizedRect - tuple with the new x, y, width, and height data
def scaleRectProper(rect, percent):

    resizedRect = []
    
    [x,y,w,h] = rect
    
    newX = x - (w * percent/100/2)
    newY = y - (h * percent/100/2)
    
    newW = w * ((percent/100)+1)
    newH = h * ((percent/100)+1)

    resizedRect = [newX, newY, newW, newH]

    return resizedRect

#====================================================================
# apply the ocr engine to the given image and return the recognized script where illegitimate characters are filtered out
def tesseract(image):

    script = pytesseract.image_to_string(image,  lang = 'eng')

    script = script.strip()

    for char in script:
        if char == '\n':
            script = script.replace(char,' ')
        if char not in ' -QWERTYUIOPASDFGHJKLZXCVBNMÄÖÜqwertyuiopasdfghjklzxcvbnmäöüß,.?!1234567890"":;\'':
            script = script.replace(char,'')

    return script

#====================================================================
# simple spelling correction function for English texts that converts upper case
# words into lower case words and looks for grammatical expressions that indicate
# the occurence of prouper nouns
def checkSpelling(script):
    
    ed_script = ""

    for word in script.split():
        
        if word.isupper():
            word = word.lower()
        
            # if the word end on 's or s', it probably is a noun...
            if word.endswith("'s") or word.endswith("s'"):
                # ...except if the word is he, she, or it;
                if word.startswith("he'") or word.startswith("she'") or\
                   word.startswith("it'"):
                    ed_script = ed_script + " " + word
                # ...in any other case its a noun, which should be capitalized
                else:
                    ed_script = ed_script + " " + word.capitalize()
            else:
                ed_script = ed_script + " " + word
        else:
            ed_script = ed_script + " " + word            

    return ed_script

#====================================================================
# simple image processing followed by optical character recognition utilizing
# tesseract; used for clipped image sections that contain text
def ocrSpeeBub(speeBubList):

    speeBubTextList = []

    for speeBub in speeBubList:

        speeBubcv2 = convertWXimg2CV2img(speeBub.ConvertToImage())

        # enlarge
#        speeBubcv2 = cv2.resize(speeBubcv2, (0,0), fx = 3, fy = 3)

        # denoise
        speeBubcv2 = denoiseCv2Image(speeBubcv2, 1)

        # inverting the colors of the image
        speeBubcv2 = cv2.bitwise_not(speeBubcv2)

        # adjust brightness
        speeBubcv2 = cv2.convertScaleAbs(speeBubcv2, alpha=1.0, beta=50)

        # reduce color space
        speeBubcv2 = cv2.threshold(speeBubcv2,140,255,cv2.THRESH_BINARY)[1]

        # inverting the colors back
        speeBubcv2 = cv2.bitwise_not(speeBubcv2)

        # convert colors to gray scale
        speeBubcv2 = cv2.cvtColor(speeBubcv2, cv2.COLOR_BGR2GRAY)

        # binary convertion of colors (pure black and white image)
        speeBubcv2 = cv2.threshold(speeBubcv2,149,255,cv2.THRESH_BINARY)[1]

        # pass cropped image to the ocr engine
        speeBubText = tesseract(speeBubcv2)

        # a few simple text cosmetics
        speeBubText = checkSpelling(speeBubText)

        # lstrip removes all leading white spaces from the line of text
        speeBubTextList.append(speeBubText.lstrip(' '))

    return speeBubTextList

#======================
# helper functions
#====================================================================

#====================================================================
# This function puts images of the specified format from the given archive
# into a list which it returns in the end.
# INPUT:    packedFile - a zip-archive (type: rar or zip)
# OUTPUT:   imgsList - list with images (type: list of wx.Image(s))
#           imgPaths - list with the images paths (type: list of strings)

def unpackImgArch2ImgList(packedFile):
    
    imgPaths = []
    imgsList = []
    
    # create a temporary directory
    with tempfile.TemporaryDirectory() as tmpDir:

        # unpack all files from the archive into the temporary directory
        Archive(packedFile).extractall(tmpDir)

        # write the paths of all files with the specified file types
        # into the image paths list
        for root, dirs, files in os.walk(tmpDir):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.bmp', '.png', '.gif', '.tiff', '.tif')):
                    imgPaths.append(os.path.join(root, file))

        # feeding the image list with the images
        imgsList = imgPaths2ImgList(imgPaths)

    return imgsList, imgPaths

#====================================================================    
# This function, first, sorts the list of image file paths alphabetically and
# then puts the actual images into another list which it returns in the end.
# INPUT:    imgPaths - list with paths of image files (format: list of strings)
# OUTPUT:   imgsList - list with images (format: list of wx.Image(s))

def imgPaths2ImgList(imgPaths):

    imgsList = []

    # sort our list alphabetically
    imgPaths = sortStringLists(imgPaths, ".,;-_ ()[]{}")

    # write the images into the image list
    for i in range(len(imgPaths)):
        imgsList.append(wx.Image(imgPaths[i], wx.BITMAP_TYPE_ANY))
    
    return imgsList

#====================================================================
# sorts a list of strings alphabetically while disregarding the characters
# defined in delChars
# INPUT:    listXY - list of strings (format: list of strings);
#           delChars - string of characters (format: string)
# OUTPUT:   listXY - list of strings sorted alphabetically (format: list of strings)
def sortStringLists(listXY, delChars):

    # in order to show the images in the order they are lying in the
    # directory, we have to use a little trick that involves cleaning
    # the file paths/names from the chars defined in the table variable
    # transCharTable...
    transCharTable = dict.fromkeys(map(ord, delChars), None)

    # ...and now we sort the image list alphabetically while disregarding
    # any upper or lower cases and the chars defined above
    listXY.sort(key=lambda listStrings: (listStrings.upper(),\
                                         [string for string in\
                                         listStrings.translate(transCharTable)]))

    return listXY

#====================================================================
# Updates the image in the specified panel.
# INPUT:    newImg - an image (type: wx.Image)
#           pageOrbub - 0 == page, 1 = bubble (type: integer)
# OUTPUT:   none

def updateImage(newImg, pageOrBub):

    # get the display resolution in order to fit the image into the panel
    [disX, disY] = wx.GetDisplaySize()

    # determine the approximate size of the respective panel 
    disX = int(disX/2-20)

    if pageOrBub == 0:
        disY = int(disY-225)        
    elif pageOrBub == 1:
        disY = int(disY/2-225)        

    # if the image is a bitmap (speech bubble) it is converted to an wx.image
    try:
        newImg = newImg.ConvertToImage()
    except Exception:
        pass

    # get the size of the new image
    [iW, iH] = newImg.GetSize()
        
    # if the image is to big, scale it proportionally        
    if iW > disX and iW > iH:
        newW = disX
        newH = int(disX * iH / iW)

        # scaling the page image
        newImg = newImg.Scale(newW, newH, wx.IMAGE_QUALITY_HIGH)

    elif iH > disY and iH > iW:
        newH = disY
        newW = int(disY * iW / iH)

        # scaling the page image
        newImg = newImg.Scale(newW, newH, wx.IMAGE_QUALITY_HIGH)

    # replace the old image in the panel with the new one
    if pageOrBub == 0:
        ComicPagePanel.comPageImg.SetBitmap(wx.Bitmap(newImg))

    elif pageOrBub == 1:
        SpeechBubImgPan.speeBubImg.SetBitmap(wx.Bitmap(newImg))

    MainFrame.mainPanel.Layout()

#====================================================================
# converting the wx.Image format to the cv2.Image format
def convertWXimg2CV2img(wxImg):

    # get the size of the wx.Image
    [iW, iH] = wxImg.GetSize()

    # writing the image's raw data into the buf variable
    buf = wxImg.GetDataBuffer()

    # putting the raw data into a numpy array
    cv2Img = np.frombuffer(buf, dtype='uint8')

    # giving the raw image data height and width
    # corresponding to the original image
    cv2Img = np.reshape(cv2Img, (iH,iW,3))

    # match colors to original image
    cv2Img = cv2.cvtColor(cv2Img, cv2.COLOR_RGB2BGR)
    
    return cv2Img

#====================================================================
# converting a cv2.Image format to the wx.Image format
def convertCv2Img2WxImg(cv2Img):

    wxImg = wx.Image(1,1)

    cv2Img = cv2.cvtColor(cv2Img, cv2.COLOR_BGR2RGB)

    wxImg = wx.Bitmap.FromBuffer(cv2Img.shape[1], cv2Img.shape[0], cv2Img)

    return wxImg

#====================================================================
# denoise the given image with n iterations
def denoiseCv2Image(image, n):

    i = 0
    
    while i < n:
        image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        i += 1

    return image

#======================
# Start GUI
#====================================================================
if __name__ == '__main__':
    app = App()
    app.MainLoop()
