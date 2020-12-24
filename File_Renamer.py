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

def getInfoFromFolders(filePath,separator = "_",infoTemplate=[],mode = "Retrieve Info",extraParams = None):
    global usefulInfoPosDict
    
    infoList = []
    separator = separator
    infoTemplate = infoTemplate

    def splitString(string, separator = "_"):

        topDir = currentDir.split("\\")[-1]
        topDirPos = filePath.find(topDir)

        folderInfoString = filePath[topDirPos:]

        tempList = folderInfoString.split("\\")
        fileName = tempList[-1]

        folderInfoList = tempList[:-1]

        global currentDirectoryDepth
        if fileCounter == 0:
            currentDirectoryDepth = len(folderInfoList)
        
        newLength = len(folderInfoList)

        if newLength > currentDirectoryDepth:
            print( 3*"\n" + f"{newLength-currentDirectoryDepth} new tag(s) were found!\n")
            newUsefulInfo = folderInfoList[currentDirectoryDepth + 1 :-1]

            nonlocal infoTemplate
            if separatorFlag:
                infoTemplate = getInfoFromFolders(filePath, separator=separator, infoTemplate=infoTemplate, mode="Make Template",extraParams=("Update Template",newUsefulInfo,"Use Separator"))[1]
            else:
                 infoTemplate = getInfoFromFolders(filePath, separator=separator, infoTemplate=infoTemplate, mode="Make Template",extraParams=("Update Template",newUsefulInfo))[1]

        if "Use Separator" in extraParams:
            splitString = folderInfoList.split(separator)
        
        else:
            splitString = folderInfoList
        
        print(folderInfoList)
        
        return splitString,fileName

    if mode == "Make Template":

        if "Update Template" in extraParams:
            usefulInfoList = extraParams[1]
        else: 
            usefulInfoList = splitString(filePath)[0]
            print(3*"\n"+"These are an example the following tags found in the folder names.\nYou will be asked to name them for conveniencce, then choose the tags wou wish to keep in the file name.\nIf any new tags are found you will be prompted if you wish to add them to the naming convention.\nWARNING: Consider what the tag represents rather than the actual tag when deciding the namimg convention. This prompt will show up only once.")
            
        for tag in usefulInfoList:
            tagName = input(f"What does the tag \"{tag}\" represent?\n")
            usefulInfoPosDict[tagName] = usefulInfoList.index(tag)
        
        if infoTemplate == []:
            correctSelection = "N"
            tempDict = {}
            while correctSelection != "Y":
                print(3*"\n"+"These are the tags you named earlier:")
                for i, item in enumerate(usefulInfoPosDict.keys()):
                    print(f"{i}. {item}")
                    tempDict[i] = item

                infoTemplateString = input("Using the numbers, choose which, and in what order the information should be coppied to the file name separated by spaces (unused numbers will be ignored):\n\n")

                tempList2 = []
                print("Your selection was:")
                for i in infoTemplateString.split(" "):
                    print(tempDict[i],end="_")
                    tempList2.append(tempDict[i])
                    
                correctSelection = input("Is this correct?[Y/N]\n")

            infoTemplate = tempList2

            for i in tempDict.values() not in tempList2:
                usefulInfoPosDict[i] = usefulInfoPosDict[i] + "(Unused)"
            
        else:
            changePattern = ("New Tags were added since last selection, do you wish to update naming pattern? [Y/N]\n")
            
            if changePattern == "Y":
                correctSelection = "N"
                tempDict = {}
                while correctSelection != "Y":
                    print(3*"\n"+"This is the updated list of tags:")
                    for i, item in enumerate(usefulInfoPosDict.keys()):
                        print(f"{i}. {item}")
                        tempDict[i] = item

                    infoTemplateString = input("Using the numbers, choose which, and in what order the information should be coppied to the file name separated by spaces (unused numbers will be ignored):\n\n")

                    tempList2 = []
                    print("Your selection was:")
                    for i in infoTemplateString.split(" "):
                        print(tempDict[i],end="_")
                        tempList2.append(tempDict[i])
                        
                    correctSelection = input("Is this correct?[Y/N]\n")

                infoTemplate = tempList2

                for i in tempDict.values() not in tempList2:
                    usefulInfoPosDict[i] = usefulInfoPosDict[i] + "(Unused)"
            else:
                pass

    elif mode == "Get Info":
        allInfoList = splitString(filePath) 
        
        for item in infoTemplate:
            infoPos = usefulInfoPosDict[item]
            infoList.append(allInfoList[infoPos])

    
    return (infoList, infoTemplate)

def renameFile(filePath):
    #TODO:Write #2 renaming routine using information from getInfoFromFolders() and original name.
    pass

def main():
    global currentPath 
    currentPath = os.path.abspath(os.getcwd())

    global directories,dirCount,currentDir
    directories,dirCount,currentDir = getDirs(currentPath)

    if separator := input("Are you using separators to store information in the folder names?[Y/N]\nIf yes, please indicate it:"):
        separator = separator.lstrip("Y ")
        global separatorFlag
        separatorFlag = True
        

    for root, _dirs, files in os.walk(currentDir,topdown=True,followlinks=False):
        for name in files:
            if name.endswith(".tif"):
                filePathString = root + os.sep +name
                global fileCounter,infoTemplate
                if fileCounter == 0:
                    if separatorFlag:
                        infoTemplate = getInfoFromFolders(filePath=filePathString,mode="Make Template",extraParams="Use Separator")[1]
                        infoList = getInfoFromFolders(filePathString, infoTemplate, mode="Get Info",extraParams="Use Separator")[0]
                    else:
                        infoTemplate = getInfoFromFolders(filePath=filePathString,mode="Make Template")[1]
                        infoList = getInfoFromFolders(filePathString, infoTemplate, mode="Get Info")[0] 
                else:
                    pass

                fileCounter += 1 

exitFlag = False
directories,visitedDirs,dirCount,currentDir,currentPath = [],[],0,"",""
infoTemplate = []
usefulInfoPosDict = defaultdict(dict)
fileCounter,currentDirectoryDepth = 0,0
separatorFlag = False


while dirCount >= 0 or exitFlag == True:
    main()
    break