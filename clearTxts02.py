import os
import glob
from pathlib import PurePath as PPath

import wx

import spacy

txtLinesLst, txtsLst = [], []

#initalizing the GUI for the directory dialog
app = wx.App()
app.MainLoop()

# opening the input directory dialog
with wx.DirDialog(None, "Choose a Directory",
                  style=wx.DD_DEFAULT_STYLE) as dDlg:

    # if the directory dialog wasn't cancelled
    if dDlg.ShowModal() == wx.ID_OK:
        # get every txt file within the directory
        txtPathsLst = glob.glob(os.path.join(dDlg.GetPath(),'*.txt'))

# loading all text files and their paths into a list;
# plus some first character stripping
if txtPathsLst:
    for path in txtPathsLst:
        fullTxt = ""
    
        with open(PPath(path), "r", encoding="utf-8") as txtFile:
            linesLst = []
            for line in txtFile:
                if line != "\n":
                    linesLst.append(line.strip())

        txtLinesLst.append([path, linesLst])
    
        fullTxt = " ".join(linesLst)
        
        fullTxtLst = [word.strip(" -*") for word in fullTxt.split()]
        fullTxt = " ".join(fullTxtLst)
        
        txtsLst.append([path, fullTxt])

# writing the paths of the the stop word list and the word association list into variables
stopWordLstPath = PPath("\\".join(PPath(path).parts[:-2]), "stopword_list_en.txt")
terrorWordLstPath = PPath("\\".join(PPath(path).parts[:-2]), "word_list_terrorism.txt")

# loading the content of the stop word list into a list
with open(stopWordLstPath, "r", encoding="utf-8") as txtFile:
    stopWordLst = []
    for line in txtFile:
        if line != "\n":
            stopWordLst.append(line.strip())

# loading the content of the word association list into a list
with open(terrorWordLstPath, "r", encoding="utf-8") as txtFile:
    terrorWordLst = []
    for line in txtFile:
        if line != "\n":
            terrorWordLst.append(line.strip())

# loading the spacy tool
spacyTools = spacy.load("en_core_web_md")

# for every txt in the list do...
for path, txt in txtsLst:

    # augmenting the text as it is
    augTxt01 = spacyTools(txt)

    # initalizing a couple of lists
    nameLst, clrTxt01, clrTxt02, delNameLst, terrorTxtLst01, terrorTxtLst02, namedEntsLst = [], [], [], [], [], [], []

    # removing variants of Captain and Captain America from the text, so that
    # only possible references to the US are left
    tmpTxt01 = txt.replace("Captain America", "")
    tmpTxt02 = tmpTxt01.replace("Capitan America", "")
    tmpTxt03 = tmpTxt02.replace("Captain", "")
    tmpTxt04 = tmpTxt03.replace("CAPTAIN", "")
    caplessTxt = tmpTxt04.replace("Capitan", "")

    # augmenting the text without Captain America references
    augTxt02 = spacyTools(caplessTxt)
    
    # removing variants of "World War" from the text, in order to keep only
    # references to the the more general term "war"
    wWarlessTxt = txt.lower().replace("world war", "")

    # compiling the list of named entities from the unaltered text
    for ent in augTxt01.ents:
        namedEntsLst.append(ent.text)

    # compiling the list of words from the unaltered text that are in the
    # list of words associated with the term terrorism
    for token in augTxt01:
        if token.text in terrorWordLst:
            terrorTxtLst01.append(token.text)

    # compiling the list of words from the text without "Captain America" in it
    # that are in the list of words associated with the term terrorism
    for token in augTxt02:
        if token.text in terrorWordLst:
            terrorTxtLst02.append(token.text)

    # compiling the names of entities in the unaltered text that have been
    # tagged as "person"
    nameLst = [i for i in augTxt01 if i.ent_type_.lower() in ["person"]]

    # writing all tokens into a list that are not in the name list and corresponding
    # names into a seperate list
    for token in augTxt01:
        if token not in nameLst:
            clrTxt01.append(token.text)
        else:
            delNameLst.append(token.text)

    # for reuse purposes the content of clrTxt01 is reassigned
    tokenizedTxt01 = clrTxt01
    
    clrTxt01 = []
    # writing all tokens from the tokenizedTxt01 list into clrTxt01 that
    # are not on the stop word list
    for token in tokenizedTxt01:
        if token not in stopWordLst and token.lower() not in stopWordLst:
            clrTxt01.append(token)

    # writing all tokens from the text without "Captain America" in it into
    # the clrTxt02 list
    for token in augTxt02:
        clrTxt02.append(token.text)

    # for reuse purposes the content of clrTxt02 is reassigned
    tokenizedTxt02 = clrTxt02
    
    clrTxt02 = []
    # writing all tokens from the tokenizedTxt02 list into clrTxt02 that
    # are not on the stop word list
    for token in tokenizedTxt02:
        if token not in stopWordLst and token.lower() not in stopWordLst:
            clrTxt02.append(token)

    # assigning path and file names
    wWarlessTxtFilename = PPath(path).stem + "_wWarless.txt"
    caplessTxtFilename = PPath(path).stem + "_capless.txt"
    namedEntsFilename = PPath(path).stem + "_namedEnts.txt"
    terrorWords01Filename = PPath(path).stem + "_terror01Words.txt"
    terrorWords02Filename = PPath(path).stem + "_terror02Words.txt"
    delNamesFilename = PPath(path).stem + "_delNames.txt"
    cleanTxt01Filename = PPath(path).stem + "_cleanTxt01.txt"
    cleanTxt02Filename = PPath(path).stem + "_cleanTxt02.txt"


    # constructing the save paths
    wWarlessTxtOutPath = PPath("\\".join(PPath(path).parts[:-2]), "output", "wWarlessTxts", wWarlessTxtFilename)
    caplessTxtOutPath = PPath("\\".join(PPath(path).parts[:-2]), "output", "caplessTxts", caplessTxtFilename)
    namedEntsOutPath = PPath("\\".join(PPath(path).parts[:-2]), "output", "namedEnts", namedEntsFilename)
    terrorWords01OutPath = PPath("\\".join(PPath(path).parts[:-2]), "output", "terrors01", terrorWords01Filename)
    terrorWords02OutPath = PPath("\\".join(PPath(path).parts[:-2]), "output", "terrors02", terrorWords02Filename)
    delNamesOutPath = PPath("\\".join(PPath(path).parts[:-2]), "output", "delNames", delNamesFilename)
    cleanTxt01OutPath = PPath("\\".join(PPath(path).parts[:-2]), "output", "cleanTxts01", cleanTxt01Filename)
    cleanTxt02OutPath = PPath("\\".join(PPath(path).parts[:-2]), "output", "cleanTxts02", cleanTxt02Filename)


    # writing the files
    with open(wWarlessTxtOutPath, "w", encoding="utf-8") as txtFile:
        txtFile.write(wWarlessTxt)

    with open(caplessTxtOutPath, "w", encoding="utf-8") as txtFile:
        txtFile.write(caplessTxt)

    with open(namedEntsOutPath, "w", encoding="utf-8") as txtFile:
        for word in namedEntsLst:
            txtFile.write("%s\n" % word)

    with open(terrorWords01OutPath, "w", encoding="utf-8") as txtFile:
        for word in terrorTxtLst01:
            txtFile.write("%s\n" % word)
    
    with open(terrorWords02OutPath, "w", encoding="utf-8") as txtFile:
        for word in terrorTxtLst02:
            txtFile.write("%s\n" % word)

    with open(delNamesOutPath, "w", encoding="utf-8") as txtFile:
        for name in delNameLst:
            txtFile.write("%s\n" % name)
            
    with open(cleanTxt01OutPath, "w", encoding="utf-8") as txtFile:
        txtFile.write("{}".format(" ".join(clrTxt01)))
        
    with open(cleanTxt02OutPath, "w", encoding="utf-8") as txtFile:
        txtFile.write("{}".format(" ".join(clrTxt02)))