#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import nuke


def createWriteNode():
    nodes = nuke.allNodes()
    OLMSmootherNode = []
    head = ''
    for i in range(len(nodes)):
        name = nodes[i].name()
        node = nuke.toNode(name)
        projectPath = nuke.Root().name()
        filed = projectPath.split('/')
        filed.remove(filed[-1])

        for i in range(1,len(filed)):
            head = os.path.join(head,filed[i])
        if node.Class() == 'OLMSmoother':
            OLMSmootherNode.append(node)
    if len(OLMSmootherNode):
        if len(OLMSmootherNode) == 1:
            outfilePathDirs = 'D:' + '\\' + head + '\\chAll'
            if not os.path.isdir(outfilePathDirs):
                os.makedirs(outfilePathDirs)
            outfilePath = (outfilePathDirs +'\\chAll'+ '.%04d.png').replace('\\','/')
            inputNodeName = OLMSmootherNode[0].input(0).name()
            inputNode = nuke.toNode(inputNodeName)
            writeNode = nuke.nodes.Write(inputs=[inputNode],file = outfilePath)
            writeNode['channels'].setValue('rgba')
            writeNode['file_type'].setValue('png')

            #此时开始输出渲染

            nuke.exectue(writeNode)
            readNode = createReadNode(outfilePathDirs.replace('\\','/'))
            OLMSmootherNode[0].setInput(0,readNode)
        else:
            n = 1
            for i in range(len(OLMSmootherNode)):
                outfilePathDirs = 'D:' + '\\' + head + '\\chAll' + str(n)
                if not os.path.isdir(outfilePathDirs):
                    os.makedirs(outfilePathDirs)
                outfilePath = (outfilePathDirs  + '\\chAll' + str(n) + '.%04d.png').replace('\\', '/')
                inputNodeName = OLMSmootherNode[i].input(0).name()
                inputNode = nuke.toNode(inputNodeName)
                writeNode = nuke.nodes.Write(inputs=[inputNode],file = outfilePath)
                writeNode['channels'].setValue('rgba')
                writeNode['file_type'].setValue('png')
                #此时开始渲染输出
                nuke.exectue(writeNode)
                readNode = createReadNode(outfilePathDirs.replace('\\','/'))
                OLMSmootherNode[i].setInput(0,readNode)
                n += 1

def createReadNode(imagePath):
    # SeqsPath = r'F:/Work/Nuke/GF/comp/EP02/shot050/BG_A'
    readNode = nuke.nodes.Read(file = imagePath)
    imagesTypes = "jpg|jpge|tga|iff|dpx|tiff|tif|png"
    rule = r'(.*?)(\d+)(\.(?:%s))' % imagesTypes
    pattern = re.compile(rule)
    nuke_readSeqs = []
    imagesBaseName = []
    for root, dirs, files in os.walk(imagePath):
        imagesSeq = [x for x in files if x.split('.')[-1] in imagesTypes]
        if imagesSeq != []:
            imagesSeq.sort()
            for f in imagesSeq:
                rootR = root.replace("\\", "/")
                if pattern.findall(f) == []:
                    nuke_readSeqs.append([rootR + '/' + f, 1, 1])
                elif (rootR + pattern.findall(f)[0][0]) not in imagesBaseName:
                    firstFrame = int(pattern.findall(f)[0][1])
                    imagesBaseName.append(rootR + pattern.findall(f)[0][0])
                    nuke_readSeqs.append([rootR + '/' + pattern.findall(f)[0][0] + '#' * len(pattern.findall(f)[0][1]) +
                                          pattern.findall(f)[0][2], firstFrame, firstFrame])
                else:
                    nuke_readSeqs[-1][2] = int(pattern.findall(f)[0][1])
    readNode['file'].setValue(nuke_readSeqs[0][0])
    readNode['first'].setValue(nuke_readSeqs[0][1])
    readNode['last'].setValue(nuke_readSeqs[0][-1])
    return readNode

def aa():
    pass
