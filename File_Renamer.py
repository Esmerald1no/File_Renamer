import os
from collections import defaultdict

#TEMP: Current Directory not the same as working directory.
os.chdir(r"C:\Users\Bruno\Dropbox\ImageProcessing_Bruno")

def getDirs(path):
    directories = [name for name in os.listdir(currentPath) if os.path.isdir(name)]

    global visitedDirs
    if len(visitedDirs) > 0:
        tempDirectories = [item for item in directories not in visitedDirs]
        directories = tempDirectories

    dirCount = len(directories)
    if dirCount>1:
        print("Multiple Directories Found, Select Working Directory:")
        for i in range(dirCount):
            print(f"{i+1}. {directories[i]}")
            currentDir = int(input())

            
            visitedDirs.append(directories[currentDir-1])

            os.chdir(directories[currentDir-1])
            currentDir = os.getcwd()

    elif dirCount == 1:   
        if (currentDir := input(f"The directory found is \"{directories[0]}\" is this the desired directory? [Y/N].\nIf this is not the desired directory, insert the path for the new directory or move this module to that location: \n")) != "Y":
            currentDir = currentDir.lstrip("N ")
            os.chdir(currentDir)
        else:
            os.chdir(directories[0])
            currentDir = os.getcwd()

            visitedDirs.append(directories[0])
    else:
        print("No direcories left to rename.")
        return ([],-1,"")

    return (directories,dirCount,currentDir)

def getInfoFromFolders(filePath,separator = "_",infoTemplate=[],mode = 1):
    infoList = []

    def splitString(string, separator = "_"):

        topDir = currentDir.split("\\")[-1]
        topDirPos = filePath.find(topDir)

        #print(topDirPos)

        folderInfoString = filePath[topDirPos:]

        #print(usefulInfoString)

        tempList = folderInfoString.split("\\")
        fileName = tempList[-1]

        #print(fileName)

        folderInfoList = tempList[:-1]

        global currentDirectoryDepth
        if fileCounter == 0:
         currentDirectoryDepth = len(folderInfoList)
        
        newLength = len(folderInfoList)

        if newLength > currentDirectoryDepth: 
            print("A new tag was found")
            

        splitString = folderInfoList.split(separator)
        
        print(folderInfoList)
        
        return splitString,fileName

    if mode == 0:
        #TODO: #5 Add logic for user to decide which naming pattern they want.

        usefulInfoList = splitString(filePath)[0]

        print(3*"\n"+"These are an example the following tags found in the folder names.\nYou will be asked to name them for conveniencce, then choose the tags wou wish to keep in the file name.\nIf any new tags are found you will be prompted if you wish to add them to the naming convention.\nWARNING: Consider what the tag represents rather than the actual tag when deciding the namimg convention. This prompt will show up only once.")
        global usefulInfoPosDict
        for tag in usefulInfoList:
            tagName = input(f"What does the tag \"{tag}\" represent?\n")
            usefulInfoPosDict[tagName] = usefulInfoList.index(tag)

        infoTemplate = []
    else:
        infoTemplate = infoTemplate
    
    return (infoList, infoTemplate)

def renameFile(filePath):
    #TODO:Write #2 renaming routine using information from getInfoFromFolders() and original name.
    pass

def main():
    global currentPath 
    currentPath = os.path.abspath(os.getcwd())

    global directories,dirCount,currentDir
    directories,dirCount,currentDir = getDirs(currentPath)

    for root, dirs, files in os.walk(currentDir,topdown=True,followlinks=False):
        for name in files:
            if name.endswith(".tif"):
                filePathString = root + os.sep +name
                if fileCounter == 0:
                    infoTemplate = getInfoFromFolders(filePath=filePathString,mode=0)[1]
                else:
                    pass

                global fileCounter
                fileCounter += 1 

exitFlag = False
directories,visitedDirs,dirCount,currentDir,currentPath = [],[],0,"",""
usefulInfoPosDict = defaultdict(dict)
fileCounter,currentDirectoryDepth = 0,0

while dirCount >= 0 or exitFlag == True:
    main()
    break