#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import nuke


def importImages(imagesPath):
    imagesTypes = "jpg|jpge|tga|iff|dpx|tiff|tif"
    rule = r'(.*?)(\d+)(\.(?:%s))' % imagesTypes
    pattern = re.compile(rule)
    nuke_readSeqs = []
    imagesBaseName = []
    readSeqsDone = []
    readSeqsDone2 = []
    readSeqsC = []
    c = 0
    firstFrame = 0
    pathall = []
    for root, dirs, files in os.walk(imagesPath):
        imagesSeq = [x for x in files if x.split('.')[-1] in imagesTypes]
        if imagesSeq != []:
            imagesSeq.sort()
            for f in imagesSeq:
                rootR = root.replace("\\", "/")
                #  print rootR
                if pattern.findall(f) == []:
                    # nuke.createNode("Read",inpanel=False)["file"].setValue(root+'/'+f)
                    nuke_readSeqs.append([rootR + '/' + f, 1, 1])
                elif (rootR + pattern.findall(f)[0][0]) not in imagesBaseName:
                    firstFrame = int(pattern.findall(f)[0][1])
                    imagesBaseName.append(rootR + pattern.findall(f)[0][0])
                    nuke_readSeqs.append([rootR + '/' + pattern.findall(f)[0][0] + '#' * len(pattern.findall(f)[0][1]) +
                                          pattern.findall(f)[0][2], firstFrame, firstFrame])
                    # else:nuke_readSeqs[-1][2] += 1
                else:
                    nuke_readSeqs[-1][2] = int(pattern.findall(f)[0][1])

    for readSeqsV in nuke_readSeqs:
        readSeqsPathT = readSeqsV[0].split("/")
        readSeqsPathT2 = ""
        for i in range(len(readSeqsPathT) - 1):
            readSeqsPathT2 += readSeqsPathT[i] + "/"

        if readSeqsPathT2.find("Left") >= 0:
            if os.path.isdir(readSeqsPathT2.replace("Left", "Right")) == 1:
                readSeqsV[0] = readSeqsV[0].replace("Left", "%V")
                readSeqsC.append(readSeqsV[0])
                readSeqsDone.append(readSeqsV)
                c = 1
            else:
                readSeqsDone.append(readSeqsV)
        elif readSeqsPathT2.find("Right") >= 0:

            if (readSeqsV[0].replace("Right", "%V")) not in readSeqsC:
                readSeqsDone.append(readSeqsV)
            else:
                pass
        else:
            readSeqsDone.append(readSeqsV)

    # if c == 1:
    #     setUpMultiView()
    r = nuke.allNodes('Read')
    for nod in r:
        pathall.append(nod['file'].value())
    for i in range(len(readSeqsDone)):

        seqs = readSeqsDone[i]
        if seqs[0] not in pathall:
            readSeqsDone2.append(readSeqsDone[i])

    for readSeqa in readSeqsDone2:
        n = nuke.createNode("Read", inpanel=False)
        n["file"].setValue(readSeqa[0])
        n["first"].setValue(readSeqa[1])
        n["last"].setValue(readSeqa[2])
        nuke.delete(nuke.thisNode())


def setUpMultiView(views=[('left', (0, 1, 0)), ('right', (1, 0, 0))]):
    newViews = []
    for v in views:  # CYCLE THROUGH EACH REQUESTED VIEW
        name = v[0]  # GRAB THE CURRENT VIEWS NAME
        col = v[1]  # GRAB THE CURRENT VIEWS COLOUR
        rgb = tuple([int(v * 255) for v in col])  # CONVERT FLOAT TO 8BIT INT AND RETURN A TUPLE
        hexCol = '#%02x%02x%02x' % rgb  # CONVERT INTEGER NUMBERS TO HEX CODE
        curView = '%s %s' % (name, hexCol)  # COMBINE NAME AND HEX COLOUR TO SCRIPT SYNTAX
        newViews.append(curView)  # COLLECT ALL REQUESTED VIEWS

    # COMBINE ALL VIEWS WITH LINE BREAK AND INITIALISE THE VIEWS KNOB WITH THE RESULTING SCRIPT SYNTAX
    nuke.root().knob('views').fromScript('\n'.join(newViews))


def importImagesPanel():
    n = nuke.createNode("PanelNode")
    k1 = nuke.File_Knob("dirPath", "Path")
    k2 = nuke.PyScript_Knob("importImages", "importImages", "importImages(nuke.thisNode()['dirPath'].value())")
    n.addKnob(k1)
    n.addKnob(k2)